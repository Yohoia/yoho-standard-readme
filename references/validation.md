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

`--module-root` and `--browser` are optional when the environment already resolves packages and a Playwright browser. The helper saves desktop (900px) and mobile (360px), light and dark, first-screen PNGs, `index.html`, and a machine-readable report. Open the comparison page and show individual images at useful size. For the final README, run the helper on each completed edition and also inspect content below the first screen.

Preview content is sanitized and served only from the target repository. Remote images are not downloaded or loaded by this helper; they are listed as unverified. Use a permitted browser check to inspect real external badges/images, or replace them with appropriate local assets when justified. Mermaid is reported as unrendered unless an external rendering path is used. The preview is not an exact reproduction of GitHub's current sanitizer, Camo image proxy, font rendering, or diagram runtime.

## Content and bilingual review

- Check the seven core roles in [the content template](content.md), allowing merged headings. Remove template placeholders and empty optional chapters; preserve required notices.
- Compare material claims against the evidence note and actual source files.
- Walk the shortest complete install/use example and report what actually ran. Identify missing credentials, infrastructure, or tools accurately.
- Check English/Chinese coverage, example parameters, status, limitations, language links, and destinations. Different wording and heading counts can be legitimate; contradictory behavior cannot.
- Open local destinations, and check important external destinations with available web tools. A private or authenticated URL needs an appropriate access check, not an automatic deletion.
- Preserve notices, attributions, and author-provided constraints. Do not assign a license.

## Visual acceptance

Inspect desktop and mobile first screens in light/dark themes. Confirm the project identity, purpose, and next action are visible; screenshots depict the actual product; images load; essential labels remain readable; prose reflows; and long code/tables scroll within their own containers rather than widening the page. Inspect the complete selected document as well as its first screen. Read Chinese labels at the actual mobile size.

For a centered brand Hero, inspect the actual alignment, title/slogan wrapping, badge/link rows, theme contrast, and transition to left-aligned technical content. A missing logo, badge, homepage, or screenshot should yield an intentional omission or selected design asset, never a broken placeholder or an unsupported claim.

Automated image-loading and overflow checks help locate defects but do not judge contrast, composition, visual quality, or factual truth. Missing browser/image tools remain verification gaps. State them explicitly; do not label unperformed checks as passed.
