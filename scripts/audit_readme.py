#!/usr/bin/env python3
"""Audit local README structure without claiming to verify prose or execution."""

import argparse
from collections import Counter
from dataclasses import dataclass
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


@dataclass
class Link:
    target: str
    image: bool = False
    alt: str = ""


@dataclass
class DocumentAnalysis:
    links: list
    anchors: set
    examples: Counter
    issues: list


_HTML_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?=[\s/>])(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>")
_BACKTICKS = re.compile(r"`+")
_AUTOLINK = re.compile(r"<((?:https?://|mailto:)[^<>\s]+)>")
_RAW_HTML_BLOCK = re.compile(r" {0,3}<(pre|script|style|textarea)(?=[\s>])", re.I)
_HTML_BLOCK = re.compile(
    r" {0,3}</?(?:address|article|aside|base|blockquote|body|caption|center|col|colgroup|"
    r"dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|"
    r"h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|"
    r"ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|"
    r"title|tr|track|ul)(?=[\s/>])", re.I,
)


class _HtmlReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.anchors, self.issues = [], set(), []
        self.literal_tags = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"pre", "code", "script", "style", "textarea"}:
            self.literal_tags.append(tag)
        for key in ("id", "name"):
            if attrs.get(key):
                self.anchors.add(attrs[key])
        if tag in {"script", "iframe", "object", "embed", "form", "button", "input", "style"}:
            self.issues.append(("error", "unsupported-html", f"Unsupported README element: {tag}"))
        if "style" in attrs or "class" in attrs:
            self.issues.append(("warning", "stripped-html-attributes", f"GitHub may strip styling on {tag}"))
        if tag == "a" and attrs.get("href") is not None:
            self.links.append(Link(attrs["href"]))
        if tag == "img":
            if attrs.get("src") is None:
                self.issues.append(("error", "image-source", "HTML image has no src"))
            else:
                self.links.append(Link(attrs["src"], True, attrs.get("alt") or ""))
        if tag == "source" and attrs.get("srcset"):
            for item in attrs["srcset"].split(","):
                if item.strip():
                    self.links.append(Link(item.strip().split()[0], True, "picture source"))

    def handle_endtag(self, tag):
        if tag in self.literal_tags:
            index = len(self.literal_tags) - 1 - self.literal_tags[::-1].index(tag)
            del self.literal_tags[index:]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def _inline_destination(text, start):
    pos = start + 1
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos < len(text) and text[pos] == "<":
        close = text.find(">", pos + 1)
        if close == -1:
            return None
        target, pos = text[pos + 1:close], close + 1
    else:
        begin, nesting = pos, 0
        while pos < len(text):
            char = text[pos]
            if char == "\\":
                pos += 2
                continue
            if char == "(":
                nesting += 1
            elif char == ")":
                if nesting == 0:
                    break
                nesting -= 1
            if char.isspace() and nesting == 0:
                break
            pos += 1
        target = re.sub(r"\\([\\()])", r"\1", text[begin:pos])
    separated = pos < len(text) and text[pos].isspace()
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if separated and pos < len(text) and text[pos] in "\"'(":
        closing = ")" if text[pos] == "(" else text[pos]
        pos += 1
        while pos < len(text) and text[pos] != closing:
            pos += 2 if text[pos] == "\\" else 1
        if pos == len(text):
            return None
        pos += 1
        while pos < len(text) and text[pos].isspace():
            pos += 1
    if pos < len(text) and text[pos] == ")":
        return target, pos + 1
    return None


def _heading_anchors(visible, explicit):
    anchors, counts = set(explicit), Counter()
    lines = visible.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        if match:
            headings.append(match[1])
        elif index and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line) and lines[index - 1].strip():
            headings.append(lines[index - 1].strip())
    for heading in headings:
        heading = html.unescape(heading).strip().lower()
        heading = re.sub(r"[`*~]", "", heading)
        heading = re.sub(r"(?<!\w)_{1,2}|_{1,2}(?!\w)", "", heading)
        slug = "".join(c for c in heading if c in "_- " or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        candidate = slug
        while candidate in counts:
            counts[slug] += 1
            candidate = f"{slug}-{counts[slug]}"
        counts[candidate] = 0
        anchors.add(candidate)
    return anchors


def analyze_document(text):
    parser = _HtmlReferences()
    links, pending, blocks, issues = [], [], [], []
    definitions = {}

    def reference_key(value):
        return " ".join(value.split()).casefold()

    def scan(source, in_label=False):
        visible = []
        pos, html_block, indented = 0, None, False
        while pos < len(source):
            if not in_label and (pos == 0 or source[pos - 1] == "\n"):
                end = source.find("\n", pos)
                end = len(source) if end == -1 else end + 1
                line = source[pos:end]
                if html_block == "end" or (html_block == "blank" and not line.strip()):
                    html_block = None
                if not html_block:
                    raw = _RAW_HTML_BLOCK.match(line)
                    if raw:
                        html_block = raw[1].lower()
                    elif _HTML_BLOCK.match(line) or (not re.match(r"(?: {4}| {0,3}\t)", line) and _HTML_TAG.fullmatch(line.strip())):
                        html_block = "blank"
                if not html_block and not parser.literal_tags:
                    fence = re.match(r" {0,3}(`{3,}|~{3,})([^\n]*)", line)
                    if fence and (fence[1][0] != "`" or "`" not in fence[2]):
                        close = re.compile(r"^ {0,3}" + re.escape(fence[1][0]) + "{" + str(len(fence[1])) + r",}[ \t]*(?:\n|$)", re.M).search(source, end)
                        stop = close.end() if close else len(source)
                        body = source[end:close.start() if close else len(source)].rstrip("\n")
                        if close:
                            blocks.append((fence[2].strip().split(" ")[0].lower(), body))
                        else:
                            issues.append(("error", "unclosed-fence", "A fenced code block is not closed"))
                        visible.append("\n" * source[pos:stop].count("\n"))
                        pos = stop
                        continue
                    previous = source[source.rfind("\n", 0, max(0, pos - 1)) + 1:pos - 1]
                    if re.match(r"(?: {4}|\t)", line) and (pos == 0 or not previous.strip() or indented):
                        visible.append("\n" * line.count("\n"))
                        pos, indented = end, True
                        continue
                    if line.strip():
                        indented = False
                    definition = re.match(r" {0,3}\[([^\]^][^\]]*)\]:[ \t]*", line)
                    if definition:
                        value, stop = line[definition.end():].rstrip("\n"), end
                        if not value.strip():
                            following = source.find("\n", end)
                            stop = len(source) if following == -1 else following + 1
                            value = source[end:stop].rstrip("\n")
                            if re.match(r" {0,3}(?:`{3,}|~{3,})", value):
                                value = ""
                        destination = _inline_destination("(" + value + ")", 0)
                        if destination and destination[0] and destination[1] == len(value) + 2:
                            definitions[reference_key(definition[1])] = destination[0]
                            visible.append("\n" * source[pos:stop].count("\n"))
                            pos = stop
                            continue
            if source.startswith("<!--", pos):
                close = source.find("-->", pos + 4)
                stop = close + 3 if close != -1 else len(source)
                visible.append("\n" * source[pos:stop].count("\n"))
                pos = stop
                continue
            tag = _HTML_TAG.match(source, pos)
            if tag:
                parser.feed(tag[0])
                if html_block not in {None, "blank", "end"} and re.fullmatch(r"</" + html_block + r"\s*>", tag[0], re.I):
                    html_block = "end"
                visible.append("\n" * tag[0].count("\n"))
                pos = tag.end()
                continue
            if html_block or parser.literal_tags:
                if source[pos] == "\n":
                    visible.append("\n")
                pos += 1
                continue
            if source[pos] == "\\":
                visible.append(source[pos:pos + 2])
                pos += 2
                continue
            if source[pos] == "`":
                run = _BACKTICKS.match(source, pos)[0]
                close = re.compile(r"(?<!`)" + run + r"(?!`)").search(source, pos + len(run))
                if close:
                    body = source[pos + len(run):close.start()]
                    visible.append(body.replace("\n", " ") + "\n" * body.count("\n"))
                    pos = close.end()
                    continue
                visible.append(run)
                pos += len(run)
                continue
            autolink = _AUTOLINK.match(source, pos)
            if autolink:
                links.append(Link(autolink[1]))
                visible.append(autolink[1])
                pos = autolink.end()
                continue
            image = source.startswith("![", pos)
            start = pos + 1 if image else pos
            if source[start] != "[" or (in_label and not image):
                visible.append(source[pos])
                pos += 1
                continue
            depth, end = 1, start + 1
            while end < len(source) and depth:
                if source[end] == "\\":
                    end += 2
                    continue
                depth += (source[end] == "[") - (source[end] == "]")
                end += 1
            if depth:
                visible.append(source[pos])
                pos += 1
                continue
            label = source[start + 1:end - 1]
            stop, target = end, None
            if end < len(source) and source[end] == "(":
                destination = _inline_destination(source, end)
                if destination:
                    target, stop = destination
            else:
                key, explicit = reference_key(label), False
                if end < len(source) and source[end] == "[":
                    close = source.find("]", end + 1)
                    if close != -1:
                        key = reference_key(source[end + 1:close] or label)
                        stop, explicit = close + 1, True
                pending.append((key, image, label, explicit))
            if target is not None:
                links.append(Link(target, image, label))
            visible.append(_HTML_TAG.sub("", label) if image else scan(label, True))
            pos = stop
        return "".join(visible)

    visible = scan(text)
    parser.close()
    issues.extend(parser.issues)
    for key, image, label, explicit in pending:
        if key in definitions:
            links.append(Link(definitions[key], image, label))
        elif explicit:
            issues.append(("error", "unresolved-reference", f"Undefined link reference: {key}"))
    if not text.strip():
        issues.append(("error", "empty-document", "README is empty"))
    return DocumentAnalysis(links + parser.links, _heading_anchors(visible, parser.anchors), runnable_examples(blocks), issues)


def runnable_examples(blocks):
    aliases = {"bash": "shell", "sh": "shell", "zsh": "shell", "js": "javascript", "ts": "typescript", "py": "python"}
    runnable = {"shell", "powershell", "cmd", "python", "javascript", "typescript", "go", "rust", "java", "ruby", "php", "sql", "c", "cpp"}
    result = Counter()
    for language, body in blocks:
        language = aliases.get(language, language)
        if language in runnable:
            lines = [line.rstrip() for line in body.splitlines() if line.strip() and not line.lstrip().startswith(("#", "//"))]
            if lines:
                result[(language, "\n".join(lines))] += 1
    return result


def audit(repo, documents, bilingual=True):
    issues, external, inspected, targets = [], set(), [], {}
    analyses = {}

    def document_analysis(path):
        if path not in analyses:
            analyses[path] = analyze_document(path.read_text(encoding="utf-8"))
        return analyses[path]

    def issue(document, severity, code, message):
        issues.append({"document": str(document), "severity": severity, "code": code, "message": message})

    def check_svg(path, document):
        try:
            tree = ET.parse(path)
        except (ET.ParseError, OSError) as error:
            issue(document, "error", "invalid-svg", f"{path.name}: {error}")
            return
        root = tree.getroot()
        if "viewBox" not in root.attrib:
            issue(document, "warning", "svg-viewbox", f"{path.name}: no viewBox")
        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1].lower()
            if tag in {"script", "foreignobject"}:
                issue(document, "error", "unsafe-svg", f"{path.name}: {tag}")
            for key, value in element.attrib.items():
                attribute = key.rsplit("}", 1)[-1].lower()
                if attribute.startswith("on") or (attribute in {"href", "src"} and value and not value.startswith("#")):
                    issue(document, "error", "svg-dependency", f"{path.name}: external or executable resource")
                urls = re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", value, re.I)
                if any(not url.startswith("#") for url in urls):
                    issue(document, "error", "svg-css-resource", f"{path.name}: external CSS resource")
            if tag == "style" and element.text:
                urls = re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", element.text, re.I)
                if "@import" in element.text.lower() or any(not url.startswith("#") for url in urls):
                    issue(document, "error", "svg-css-resource", f"{path.name}: external stylesheet resource")

    for document in documents:
        document = document.resolve()
        try:
            document.relative_to(repo)
        except ValueError:
            issue(document, "error", "outside-repo", "Document is outside the target repository")
            continue
        if not document.is_file():
            issue(document, "error", "missing-document", "Document does not exist")
            continue
        inspected.append(str(document))
        analysis = document_analysis(document)
        for severity, code, message in analysis.issues:
            issue(document, severity, code, message)
        targets[document] = {"links": set(), "examples": analysis.examples}
        for link in analysis.links:
            if link.image and not link.alt.strip():
                issue(document, "error", "missing-alt", f"Image lacks a meaningful description: {link.target}")
            try:
                url = urlsplit(html.unescape(link.target))
            except ValueError:
                issue(document, "error", "invalid-url", f"Invalid URL: {link.target}")
                continue
            if url.scheme in {"http", "https", "mailto", "tel"} or (not url.scheme and url.netloc):
                external.add(link.target)
                continue
            if url.scheme:
                issue(document, "error", "unsupported-scheme", f"Unsupported URL scheme: {url.scheme}")
                continue
            if not link.target.strip():
                issue(document, "error", "empty-target", "Empty link or image destination")
                continue
            local = unquote(url.path)
            destination = ((repo / local.lstrip("/")) if local.startswith("/") else (document.parent / local)).resolve() if local else document
            try:
                destination.relative_to(repo)
            except ValueError:
                issue(document, "error", "outside-repo", f"Reference leaves the repository: {link.target}")
                continue
            targets[document]["links"].add(destination)
            if not destination.exists():
                issue(document, "error", "missing-target", f"Missing local target: {link.target}")
                continue
            if link.image and not destination.is_file():
                issue(document, "error", "image-target", f"Image is not a file: {link.target}")
            if link.image and destination.suffix.lower() == ".svg" and destination.is_file():
                check_svg(destination, document)
            if url.fragment and destination.is_file() and destination.suffix.lower() in {".md", ".markdown"}:
                if unquote(url.fragment) not in document_analysis(destination).anchors:
                    issue(document, "error", "missing-anchor", f"Unresolved local fragment: {link.target}")
    if bilingual and len(documents) == 2:
        first, second = (doc.resolve() for doc in documents)
        if first in targets and second in targets:
            for source, other in ((first, second), (second, first)):
                if other not in targets[source]["links"]:
                    issue(source, "error", "language-link", f"Missing language link to {other.name}")
            if targets[first]["examples"] != targets[second]["examples"]:
                issue(first, "warning", "example-mismatch", "Runnable fenced examples differ between languages; review for equivalent behavior")
    return {
        "documents": inspected,
        "errors": sum(item["severity"] == "error" for item in issues),
        "warnings": sum(item["severity"] == "warning" for item in issues),
        "issues": issues,
        "external_targets_not_checked": sorted(external),
        "manual_checks_required": ["claim accuracy", "English/Chinese semantic equivalence", "command execution", "visual rendering", "external destinations"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--single", type=Path, action="append", help="Audit one document; repeat for multiple independent documents")
    args = parser.parse_args()
    repo = args.repo.resolve()
    names = args.single or [Path("README.md"), Path("README.zh-CN.md")]
    documents = [name if name.is_absolute() else repo / name for name in names]
    try:
        report = audit(repo, documents, bilingual=not args.single)
    except (OSError, UnicodeError) as error:
        parser.exit(2, f"Cannot read documentation: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(report["errors"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
