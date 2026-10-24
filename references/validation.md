# Verification and helper tools

## Structural audit

Run from any directory, replacing the paths with the actual skill and target repository:

```sh
python3 /path/to/yoho-standard-readme/scripts/audit_readme.py --repo /path/to/project
```

Defaults are `README.md` and `README.zh-CN.md`. The script checks local Markdown/HTML links and images, local heading fragments, reciprocal language links, missing image descriptions, risky SVG dependencies, selected GitHub-incompatible raw HTML, and divergent runnable fenced examples. It prints a JSON report and returns a nonzero status for structural errors. Review warnings rather than treating them as proof of a content problem.

For a first-screen candidate or one document, use:

```sh
python3 /path/to/yoho-standard-readme/scripts/audit_readme.py --repo /path/to/project --single .scratch/readme-previews/a/README.md
```

This is a lightweight structural auditor, not a complete GitHub Markdown parser. It does not establish claims, translate prose, execute commands, resolve the whole GitHub sanitizer, or test external URLs. It reports unsupported/ambiguous references for review. Use a repository-provided Markdown checker when available.

Links, anchors and runnable fenced examples share one document analysis. Fenced, indented and inline code, HTML comments, image attributes and link titles retain their own contexts; Markdown-like example text does not create references. Actual HTML links and explicit anchors remain subject to checks, including inside HTML code regions.

## Render Markdown and capture four views

The optional Node helper uses `marked`, `sanitize-html`, and `playwright`. Resolve existing tools first. If dependencies are missing, use an available environment-native renderer or install dependencies only in a separate tooling directory, keeping the target project's manifests unchanged. Select an installed Chromium executable when Playwright's own browser is unavailable.

```sh
node /path/to/yoho-standard-readme/scripts/preview_readme.mjs \
  --repo /path/to/project \
  --out /path/to/project/.scratch/readme-review \
  --module-root /path/to/tooling/node_modules \
  --browser /path/to/chromium \
  .scratch/readme-previews/a/README.md \
  .scratch/readme-previews/b/README.md \
  .scratch/readme-previews/c/README.md
```

`--module-root` and `--browser` are optional when the environment already resolves packages and a Playwright browser. By default the helper saves desktop (900px) and mobile (360px), light and dark, first-screen PNGs, `index.html`, and a machine-readable report. Use this default for comparing style proposals.

For the final README, capture the complete rendered page with the same helper:

```sh
node /path/to/yoho-standard-readme/scripts/preview_readme.mjs \
  --repo /path/to/project \
  --out /path/to/project/.scratch/readme-full-review \
  --full-page \
  README.md README.zh-CN.md
```

Supply the same optional module roots and browser path when required. Each mode produces four views per document. The report and comparison page identify the capture mode; `width` and `height` remain viewport dimensions in either mode. Use separate output directories to retain both first-screen and full-page captures. Open the comparison page, follow each original-image link, and inspect long images at their native width or in readable crops. A full-page capture still requires human visual review; it does not inspect collapsed sections or interact with the document.

Preview content is sanitized and served only from the target repository. Remote images are not downloaded or loaded by this helper; they are listed as unverified. Use a permitted browser check to inspect real external badges/images, or replace them with appropriate local assets when justified. Mermaid is reported as unrendered unless an external rendering path is used. The preview is not an exact reproduction of GitHub's current sanitizer, Camo image proxy, font rendering, or diagram runtime.

The helper waits for the local document, system fonts and image decoding before capture. Missing images still appear in its error report. Content-readiness failures are bounded and release the browser and local server; capture completion does not establish factual or visual acceptance.

## Content and bilingual review

- Check the seven core roles in [the content template](content.md), allowing merged headings. Remove template placeholders and empty optional chapters; preserve required notices.
- Reuse the task facts in the [evidence note](content.md#evidence-and-uncertainty) to trace material claims to their sources; revisit changed, missing or contradictory evidence.
- Trace every badge to its data source; confirm the selected provider URL works and describes that same claim. Treat remote badges as unverified when the available renderer cannot load them.
- Walk the shortest complete install/use example and report what actually ran. Identify missing credentials, infrastructure, or tools accurately.
- Follow each important task through both editions, comparing its conditions, action, result and limits against the same checked facts. Also check status, language links and destinations. Different wording and heading counts can be legitimate; contradictory behavior cannot.
- Open local destinations, and check important external destinations with available web tools. A private or authenticated URL needs an appropriate access check, not an automatic deletion.
- Preserve notices, attributions, and author-provided constraints. Do not assign a license.

## Visual acceptance

Inspect desktop and mobile first screens in light/dark themes. Confirm the project identity, purpose, and next action are visible; screenshots depict the actual product; images load; essential labels remain readable; prose reflows; and long code/tables scroll within their own containers rather than widening the page. Inspect the complete selected document as well as its first screen. Read Chinese labels at the actual mobile size.

Apply the selected recipe's specific checks as well: [Engineering Quickstart](visuals.md#engineering-quickstart-recipe), [Editorial Overview](visuals.md#editorial-overview-recipe), or [Workflow Guide](visuals.md#workflow-guide-recipe). A clean structural report or an image without overflow does not establish that the chosen reading path works.

For a centered brand Hero, inspect the actual alignment, title/slogan wrapping, badge/link rows, theme contrast, and transition to left-aligned technical content. A missing logo should yield a text-only project title; missing badges, homepage, or screenshot should yield an intentional omission, never a broken placeholder or an unsupported claim.

For Product Showcase or another direction using product screenshots, follow the [product screenshot workflow](visuals.md#product-showcase-recipe). Check each selected asset against its source and demonstrated product state, its caption and alt text, and its readability at the actual display size. Review this product evidence separately from README rendering: the preview helper checks the document layout, not whether the target application runs or implements the depicted capability. Report unavailable product access or capture tools separately from unavailable README rendering.

Automated image-loading and overflow checks help locate defects but do not judge contrast, composition, visual quality, or factual truth. Missing browser/image tools remain verification gaps. State them explicitly; do not label unperformed checks as passed.
