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


def visible_markdown(text):
    lines, blocks = [], []
    fence = None
    body = []
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                blocks.append((fence[2], "\n".join(body)))
                fence, body = None, []
            else:
                body.append(line)
            lines.append("")
        elif match:
            fence = (match[1][0], len(match[1]), match[2].strip().split(" ")[0].lower())
            lines.append("")
        else:
            lines.append(line)
    visible = re.sub(r"<!--[\s\S]*?-->", "", "\n".join(lines))
    return visible, blocks, fence is not None


def inline_links(text, inherited=None):
    definitions = dict(inherited or {})
    definition = re.compile(r"^ {0,3}\[([^\]^][^\]]*)\]:\s*(<[^>]+>|\S+).*$", re.M)
    for match in definition.finditer(text):
        definitions[" ".join(match[1].split()).casefold()] = match[2].strip("<>")
    text = definition.sub("", text)
    text = re.sub(r"(`+).*?\1", "", text, flags=re.S)
    links = [Link(match[1]) for match in re.finditer(r"<((?:https?://|mailto:)[^<>\s]+)>", text)]
    unresolved = []
    i = 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        image = text.startswith("![", i)
        start = i + 1 if image else i
        if start >= len(text) or text[start] != "[":
            i += 1
            continue
        depth, end = 1, start + 1
        while end < len(text) and depth:
            if text[end] == "\\":
                end += 2
                continue
            depth += (text[end] == "[") - (text[end] == "]")
            end += 1
        if depth:
            i += 1
            continue
        label = text[start + 1:end - 1]
        if "![" in label:
            nested, missing = inline_links(label, definitions)
            links.extend(nested)
            unresolved.extend(missing)
        pos = end
        target = None
        if pos < len(text) and text[pos] == "(":
            pos += 1
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos < len(text) and text[pos] == "<":
                close = text.find(">", pos + 1)
                if close != -1:
                    target = text[pos + 1:close]
                    pos = close + 1
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
            if target is not None:
                links.append(Link(target, image, label))
        else:
            key = " ".join(label.split()).casefold()
            if pos < len(text) and text[pos] == "[":
                close = text.find("]", pos + 1)
                if close != -1:
                    key = " ".join((text[pos + 1:close] or label).split()).casefold()
                    pos = close + 1
                    if key not in definitions:
                        unresolved.append(key)
            if key in definitions:
                links.append(Link(definitions[key], image, label))
        i = max(end, pos)
    return links, unresolved


class HtmlReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.anchors, self.issues = [], set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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

    handle_startendtag = handle_starttag


def heading_anchors(text):
    visible, _, _ = visible_markdown(text)
    parser = HtmlReferences()
    parser.feed(visible)
    anchors, counts = set(parser.anchors), Counter()
    lines = visible.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        if match:
            headings.append(match[1])
        elif index and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line) and lines[index - 1].strip():
            headings.append(lines[index - 1].strip())
    for heading in headings:
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).strip().lower()
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
        text = document.read_text(encoding="utf-8")
        visible, blocks, unclosed = visible_markdown(text)
        if unclosed:
            issue(document, "error", "unclosed-fence", "A fenced code block is not closed")
        parser = HtmlReferences()
        parser.feed(visible)
        for severity, code, message in parser.issues:
            issue(document, severity, code, message)
        links, unresolved = inline_links(visible)
        links.extend(parser.links)
        for reference in unresolved:
            issue(document, "error", "unresolved-reference", f"Undefined link reference: {reference}")
        targets[document] = {"links": set(), "examples": runnable_examples(blocks)}
        for link in links:
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
                if unquote(url.fragment) not in heading_anchors(destination.read_text(encoding="utf-8")):
                    issue(document, "error", "missing-anchor", f"Unresolved local fragment: {link.target}")
        if not text.strip():
            issue(document, "error", "empty-document", "README is empty")
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
