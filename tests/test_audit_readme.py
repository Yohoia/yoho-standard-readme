import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_readme.py"


class ReadmeAuditTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.write("README.md", "# Tool\n\n[中文](README.zh-CN.md)\n")
        self.write("README.zh-CN.md", "# 工具\n\n[English](README.md)\n")

    def write(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def append(self, name, text):
        self.write(name, (self.root / name).read_text(encoding="utf-8") + text)

    def run_audit(self, *extra):
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root), *extra], capture_output=True, text=True)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def codes(self, report):
        return {item["code"] for item in report["issues"]}

    def test_valid_pair_with_unicode_anchors_and_same_commands(self):
        self.append("README.md", "\n[Install](#install)\n\n## Install\n\n```sh\npython tool.py\n```\n")
        self.append("README.zh-CN.md", "\n[安装](#安装)\n\n## 安装\n\n```bash\n# 运行示例\npython tool.py\n```\n")
        code, report = self.run_audit()
        self.assertEqual((code, report["errors"], report["warnings"]), (0, 0, 0))

    def test_missing_local_destination_fails(self):
        self.append("README.md", "\n[Guide](docs/absent.md)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("missing-target", self.codes(report))

    def test_missing_anchor_fails(self):
        self.append("README.md", "\n[Wrong](#not-a-heading)\n")
        self.assertIn("missing-anchor", self.codes(self.run_audit()[1]))

    def test_reference_links_and_balanced_parentheses(self):
        self.write("docs/guide(v2).md", "# Setup\n")
        self.append("README.md", '\n[Guide](docs/guide(v2).md#setup)\n\n[More][guide]\n[guide]: docs/guide(v2).md "Guide"\n')
        self.assertEqual(self.run_audit()[0], 0)

    def test_undefined_explicit_reference_fails(self):
        self.append("README.md", "\n[Guide][missing]\n")
        self.assertIn("unresolved-reference", self.codes(self.run_audit()[1]))

    def test_code_and_inline_code_are_not_links(self):
        self.append("README.md", "\n```md\n[Demo](missing.md)\n```\n\n`[Example](missing.md)`\n")
        self.assertEqual(self.run_audit()[0], 0)

    def test_inline_html_examples_are_not_embedded_elements(self):
        self.append("README.md", '\nLiteral examples: `<script>alert(1)</script>` and `` `<img src="missing.png">` ``.\n')
        code, report = self.run_audit()
        self.assertEqual((code, report["errors"]), (0, 0))

    def test_inline_html_anchor_example_is_not_a_real_anchor(self):
        self.append("README.md", '\nExample: `<a id="phantom"></a>`\n\n[Jump](#phantom)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("missing-anchor", self.codes(report))

    def test_backticks_in_markdown_and_html_destinations_are_preserved(self):
        self.write("docs/`v2`.md", "# Setup\n")
        for kind, links in {
            "markdown": "[Guide](docs/`v2`.md#setup) [Wrong](docs/`v2`.md#absent)",
            "html": '<a href="docs/`v2`.md#setup">Guide</a> <a href="docs/`v2`.md#absent">Wrong</a>',
        }.items():
            with self.subTest(kind=kind):
                self.write("README.md", "# Tool\n\n[中文](README.zh-CN.md)\n\n" + links + "\n")
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                self.assertEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    [("missing-anchor", "Unresolved local fragment: docs/`v2`.md#absent")],
                )

    def test_markdown_like_html_image_alt_is_not_a_reference(self):
        self.write("assets/example.png", "fixture")
        self.append("README.md", '\n<img src="assets/example.png" alt="[Guide](missing.md)">\n\n[Real](real-missing.md)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )

    def test_indented_and_html_code_links_are_not_references(self):
        self.append("README.md", '\n    [Example](indented-missing.md)\n\n<pre><code>[Example](pre-missing.md) &lt;a href="html-missing.md"&gt;Example&lt;/a&gt;</code></pre>\n\n[Real](real-missing.md)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )

    def test_link_title_is_not_parsed_for_references(self):
        self.append("README.md", '\n[Docs](https://example.invalid/docs "[fake](missing.md)")\n\n[Real](real-missing.md)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )
        self.assertEqual(report["external_targets_not_checked"], ["https://example.invalid/docs"])

    def test_fences_in_html_comments_do_not_hide_following_references(self):
        self.append("README.md", "\n<!--\n```md\n[Draft](draft-missing.md)\n-->\n\n[Real](real-missing.md)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )

    def test_escaped_opening_backtick_does_not_hide_unsupported_html(self):
        self.append("README.md", '\n\\`<script>alert(1)</script>`\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("unsupported-html", "Unsupported README element: script")],
        )

    def test_indented_and_html_code_anchors_do_not_satisfy_fragments(self):
        self.append("README.md", '\n    <a id="indented-phantom"></a>\n\n<pre><code>&lt;a id="html-phantom"&gt;&lt;/a&gt;</code></pre>\n\n[Indented](#indented-phantom) [HTML](#html-phantom)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [
                ("missing-anchor", "Unresolved local fragment: #indented-phantom"),
                ("missing-anchor", "Unresolved local fragment: #html-phantom"),
            ],
        )

    def test_real_html_links_and_anchors_inside_pre_are_checked(self):
        self.write("docs/guide.md", "# Guide\n")
        for target in ("docs/guide.md", "docs/missing.md"):
            with self.subTest(target=target):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'<pre><code><a id="real" href="{target}">Guide</a></code></pre>\n\n'
                           '[Real](#real) [Missing](#absent)\n')
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                expected = [("missing-anchor", "Unresolved local fragment: #absent")]
                if target == "docs/missing.md":
                    expected.append(("missing-target", "Missing local target: docs/missing.md"))
                self.assertCountEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    expected,
                )

    def test_single_indented_html_line_is_code(self):
        for example in ('<a href="indented-missing.md">Example</a>', '<script>alert(1)</script>'):
            with self.subTest(example=example):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'    {example}\n\n[Real](real-missing.md)\n')
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                self.assertEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    [("missing-target", "Missing local target: real-missing.md")],
                )

    def test_multiline_inline_code_does_not_create_heading_anchors(self):
        self.append("README.md", '\nIntro `code\n## phantom\ncode`\n\n[Fake](#phantom)\n\n## Use `code`\n\n[Real](#use-code)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-anchor", "Unresolved local fragment: #phantom")],
        )

    def test_html_inside_markdown_link_labels_is_audited(self):
        self.append("README.md", '\n[<img src="missing.png" alt="Badge"><span id="foo" class="badge">Guide</span>](https://example.invalid/docs)\n\n[Jump](#foo)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertCountEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [
                ("missing-target", "Missing local target: missing.png"),
                ("stripped-html-attributes", "GitHub may strip styling on span"),
            ],
        )
        self.assertEqual(report["external_targets_not_checked"], ["https://example.invalid/docs"])

    def test_nested_reference_text_inside_link_label_is_not_a_reference(self):
        self.append("README.md", '\n[Label [item][missing]](https://example.invalid/docs)\n\n[Real](real-missing.md)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )
        self.assertEqual(report["external_targets_not_checked"], ["https://example.invalid/docs"])

    def test_reference_definition_destination_on_next_line(self):
        self.write("target.md", "# Target\n")
        for target in ("target.md", "missing.md"):
            with self.subTest(target=target):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'[go][x]\n\n[x]:\n  {target}\n')
                code, report = self.run_audit()
                expected = [] if target == "target.md" else [("missing-target", "Missing local target: missing.md")]
                self.assertEqual(code, int(bool(expected)))
                self.assertEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    expected,
                )

    def test_invalid_reference_definition_does_not_consume_following_blocks(self):
        for block in ('## Live\n\n[Live](#live)', '```md example\n[Hidden](ignored.md)\n```', '```sh\nls\n```'):
            with self.subTest(block=block):
                self.write("README.zh-CN.md", '# 工具\n\n[English](README.md)\n'
                           + ('\n```sh\nls\n```\n' if block.startswith('```sh') else ''))
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'[go][x]\n\n[x]:\n{block}\n\n[Real](real-missing.md)\n')
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                self.assertCountEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    [
                        ("unresolved-reference", "Undefined link reference: x"),
                        ("missing-target", "Missing local target: real-missing.md"),
                    ],
                )

    def test_markdown_after_raw_html_closing_tag_needs_no_blank_line(self):
        for tag in ("pre", "script", "style", "textarea"):
            with self.subTest(tag=tag):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'<{tag}>\nexample\n</{tag}>\n[real](missing.md)\n')
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                expected = [("missing-target", "Missing local target: missing.md")]
                if tag in {"script", "style"}:
                    expected.append(("unsupported-html", f"Unsupported README element: {tag}"))
                self.assertCountEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    expected,
                )

    def test_html_in_markdown_image_alt_is_only_description(self):
        self.write("real.png", "fixture")
        self.append("README.md", '\n![<img src="phantom.png">](real.png)\n\n[Real](real-missing.md)\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(
            [(item["code"], item["message"]) for item in report["issues"]],
            [("missing-target", "Missing local target: real-missing.md")],
        )

    def test_code_spans_inside_link_labels_contribute_text_only(self):
        for code_span, fragment in (('<tag>', 'use-tag'), ('<img src="phantom.png">', 'use-img-srcphantompng')):
            with self.subTest(code_span=code_span):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'## [Use `{code_span}`](https://example.invalid/docs)\n\n[Jump](#{fragment})\n')
                code, report = self.run_audit()
                self.assertEqual((code, report["issues"]), (0, []))
                self.assertEqual(report["external_targets_not_checked"], ["https://example.invalid/docs"])

    def test_generic_html_blocks_end_at_blank_lines(self):
        for tag in ("code", "div"):
            with self.subTest(tag=tag):
                self.write("README.md", '# Tool\n\n[中文](README.zh-CN.md)\n\n'
                           f'<{tag}>\nexample\n</{tag}>\n[fake](fake-missing.md)\n\n[real](real-missing.md)\n')
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                self.assertEqual(
                    [(item["code"], item["message"]) for item in report["issues"]],
                    [("missing-target", "Missing local target: real-missing.md")],
                )

    def test_unmatched_backtick_runs_do_not_hide_embedded_html(self):
        self.append("README.md", '\n`` literal <script>alert(1)</script> ```\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("unsupported-html", self.codes(report))

    def test_empty_image_description_fails(self):
        self.write("assets/example.png", "fixture")
        self.append("README.md", "\n![](assets/example.png)\n")
        self.assertIn("missing-alt", self.codes(self.run_audit()[1]))

    def test_html_image_and_picture_sources_are_checked(self):
        self.append("README.md", '<picture><source media="(prefers-color-scheme: dark)" srcset="missing.svg"><img src="also-missing.png" alt="Demo"></picture>\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(sum(item["code"] == "missing-target" for item in report["issues"]), 2)

    def test_missing_reciprocal_language_link_fails(self):
        self.write("README.zh-CN.md", "# 工具\n")
        self.assertIn("language-link", self.codes(self.run_audit()[1]))

    def test_different_runnable_examples_need_review(self):
        self.append("README.md", "\n```sh\npython tool.py --fast\n```\n")
        self.append("README.zh-CN.md", "\n```sh\npython tool.py --slow\n```\n")
        code, report = self.run_audit()
        self.assertEqual(code, 0)
        self.assertIn("example-mismatch", self.codes(report))

    def test_svg_script_and_external_dependency_fail(self):
        self.write("assets/unsafe.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><script>alert(1)</script><image href="https://example.invalid/a.png"/></svg>')
        self.append("README.md", "\n![Example](assets/unsafe.svg)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertTrue({"unsafe-svg", "svg-dependency"}.issubset(self.codes(report)))

    def test_remote_resources_are_reported_without_fetching(self):
        self.append("README.md", "\n[Docs](https://example.invalid/docs)\n![Build](https://example.invalid/badge.svg)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 0)
        self.assertEqual(len(report["external_targets_not_checked"]), 2)

    def test_reference_outside_repository_fails(self):
        self.append("README.md", "\n[Outside](../outside.md)\n")
        self.assertIn("outside-repo", self.codes(self.run_audit()[1]))

    def test_unsafe_raw_html_fails_and_css_warns(self):
        self.append("README.md", '<div style="color:red">Note</div>\n<script>alert(1)</script>\n')
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("unsupported-html", self.codes(report))
        self.assertIn("stripped-html-attributes", self.codes(report))

    def test_duplicate_and_explicit_anchors(self):
        self.append("README.md", '\n## Usage\n\n## Usage\n\n<a name="custom"></a>\n\n[Second](#usage-1) [Custom](#custom)\n')
        self.assertEqual(self.run_audit()[0], 0)

    def test_root_relative_and_encoded_paths(self):
        self.write("docs/space name.md", "# Guide\n")
        self.append("README.md", "\n[Guide](/docs/space%20name.md#guide)\n")
        self.assertEqual(self.run_audit()[0], 0)

    def test_unclosed_fence_fails(self):
        self.append("README.md", "\n```sh\npython tool.py\n")
        self.assertIn("unclosed-fence", self.codes(self.run_audit()[1]))

    def test_single_document_does_not_require_a_translation(self):
        self.write("preview.md", "# Preview\n\nReal introduction.\n")
        code, report = self.run_audit("--single", "preview.md")
        self.assertEqual(code, 0)
        self.assertEqual(len(report["documents"]), 1)

    def test_linked_badge_image_is_checked(self):
        self.append("README.md", "\n[![Build](missing-badge.svg)](https://example.invalid/build)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("missing-target", self.codes(report))

    def test_html_comments_are_not_rendered_references(self):
        self.append("README.md", "\n<!-- [Draft](missing.md) -->\n")
        self.assertEqual(self.run_audit()[0], 0)

    def test_autolinks_are_listed_for_manual_review(self):
        self.append("README.md", "\n<https://example.invalid/docs>\n")
        _, report = self.run_audit()
        self.assertIn("https://example.invalid/docs", report["external_targets_not_checked"])

    def test_svg_local_gradient_is_valid(self):
        self.write("assets/gradient.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><defs><linearGradient id="a"/></defs><rect width="10" height="10" fill="url(\'#a\')"/></svg>')
        self.append("README.md", "\n![Gradient illustration](assets/gradient.svg)\n")
        self.assertEqual(self.run_audit()[0], 0)

    def test_svg_external_stylesheet_fails(self):
        self.write("assets/external.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><style>@import url("https://example.invalid/fonts.css");</style></svg>')
        self.append("README.md", "\n![Illustration](assets/external.svg)\n")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertIn("svg-css-resource", self.codes(report))


if __name__ == "__main__":
    unittest.main()
