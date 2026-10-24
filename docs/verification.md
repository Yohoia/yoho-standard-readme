# Verification record

Workflow trials were verified on 2026-10-23; document-analysis, preview-helper, product screenshot workflow, and badge-catalog checks were performed on 2026-10-24. This records observed behavior and its limits; it is not a compatibility guarantee or an automated visual regression suite.

## Workflow trials

Trials used isolated target projects, leaving this skill repository's own README unchanged. Style choices were simulated only within those trials.

| Scenario | Observed result |
| --- | --- |
| Line Tally CLI | Reused a completed three-direction trial: twelve rendered candidate views, original README preserved until selection B, then English/Chinese editions with reciprocal links. The recorded 22 CLI checks passed; final editions had eight clean first-screen views and a separate review of full-document captures. The updated auditor also passed the final documents. |
| LabelKit library and migration | Three distinct directions and twelve rendered candidate views preceded selection B. Final English/Chinese introductions used actual library calls. Existing French content, attribution and API/guide destinations were retained; language switches and incoming documentation links were migrated. Final documents and affected references passed structural review. |
| Note Clean with rendering disabled | Three inspectable, explicitly unrendered Markdown candidates preserved the original README until selection A. Final English/Chinese editions had identical runnable examples; six extracted examples executed successfully. No package publication, cloud synchronization, license or compatibility claims were invented. Visual acceptance remained unperformed. |
| Status Count with document/asset defects | Initial audit exited 1 with eleven errors and one warning covering local destinations, anchors, language links, image descriptions, SVG dependencies, unsupported HTML and differing examples. After document/asset repair, it exited 0 with no errors or warnings. Both editions were rendered in eight desktop/mobile light/dark views, with actual first-screen and body inspection. |

Each trial separated source facts, command execution, structural results, bilingual review and visual review. Screenshot reports alone did not establish semantic accuracy or readability. Detailed fixtures, reports and screenshots remain local scratch artifacts rather than installed runtime content.

## Auditor correction (2026-10-23)

CLI regression tests exposed three related problems:

- Literal HTML inside inline code was treated as embedded HTML, producing false image and unsupported-element errors.
- A literal inline HTML anchor incorrectly satisfied a real fragment link.
- Backtick runs of different lengths incorrectly masked embedded HTML.

The auditor now excludes matched inline code spans consistently from HTML reference parsing and link scanning. Explicit anchors use the same exclusion, while heading text retains its code content. Closing backtick runs must match the opening run length.

Each new regression failed before its correction and passed afterwards. The existing real-HTML and explicit-anchor checks remain covered.

## Document analysis refactor (2026-10-24)

The auditor now obtains links, anchors, runnable fenced examples and syntax issues from one context-aware document analysis. Each audit caches that result by resolved document path, so fragment checks reuse the same interpretation as the main document checks.

CLI regressions reproduced context errors in the previous implementation: backticks in destinations were removed, Markdown-like image attributes and link titles were treated as references, and fenced, indented, inline or HTML code examples could hide real references or introduce false ones. The analysis now preserves destination text, handles HTML attributes together, and distinguishes example text from actual HTML links and anchors. Heading text retains inline code content without generating headings from newlines inside a code span.

Follow-up regression tests cover actual HTML inside Markdown link labels, literal HTML in image descriptions, nested reference text, cross-line reference definitions, and recovery after HTML code blocks. Ordinary HTML blocks still require a blank line before Markdown resumes; `pre`, `script`, `style` and `textarea` blocks end on their closing-tag line. Invalid cross-line definitions do not consume a following fenced block.

The CLI options, JSON report fields and exit-status convention are unchanged. The existing README editions and runtime documentation produce the same structural results as before this refactor. The auditor remains a lightweight check rather than a complete GitHub Markdown parser. These checks did not rerun the workflow trials, render pages, execute README commands or validate online destinations.

## Full-page preview (2026-10-24)

Full-page captures now use `scripts/preview_readme.mjs --full-page`, replacing the need to copy the renderer and change its screenshot call. The default remains first-screen capture. Both modes produce four views per document; the JSON report, stdout summary and comparison page identify the capture mode. Existing view dimensions continue to describe the viewport, not the full PNG height.

Process-level tests exercised the actual CLI and Chromium: help and argument errors, first-screen and full-page PNG dimensions, comparison-page original-image links, capture-scope limitations, remote-image and Mermaid notices, and a missing local image returning exit status 1. All four preview tests passed with renderer dependencies and Chromium available. Without configured module roots, the two browser cases explicitly skip while the two dependency-free CLI cases run.

Both repository README editions were also captured in desktop/mobile and light/dark views: eight first-screen and eight full-page PNGs. Automatic checks reported no broken images, empty content or page overflow. Full-page reports remove only the uncaptured-body limitation; human visual review, factual and bilingual review, external resources and Mermaid rendering remain unperformed checks. These captures do not rerun the isolated workflow trials or establish equivalence to GitHub's live renderer.

## Product screenshot workflow (2026-10-24)

Product Showcase now has a style-specific screenshot workflow in [the visual reference](../references/visuals.md#product-showcase-recipe). Its trial used an isolated, runnable two-page Task Board fixture with this direction already selected. It captured the actual task overview and the result of clicking Mark as done in Chromium. Those two images told the fixture's story, so no extra screenshot quota was imposed. Source routes, actions, original captures and verification results remain in local scratch evidence.

Both fixture README editions reused the same PNGs with equivalent captions and localized alt text. The task link, completion confirmation and documented refresh reset were exercised. The documented static-server approach served both pages; the browser and test servers were closed afterwards. Structural review reported zero errors and warnings. Eight full-page desktop/mobile, light/dark README views had no broken images, overflow or empty content. Visual inspection at a 360px README viewport confirmed that task titles, the Completed button and the completion message remained readable; first-use links and instructions remained text.

The repository's own bilingual README summaries also passed structural review and produced eight full-page views without automatic image-loading or overflow defects. Product-page capture and README rendering were separate operations; the preview helper still captures only README layout. This trial used a test fixture rather than a public or authenticated product, and does not verify another project's setup, UI language support or capture suitability. GitHub's live renderer was not checked.

## Skill runtime package (2026-10-24)

The development packaging helper now maintains the runtime file list, stages a real installable copy, compares its SHA256 values with the selected source, and runs the copied auditor against every packaged Markdown document before publication. Runtime references no longer depend on this development-only record. A real package from this checkout passed with zero errors and warnings.

Eighteen process-level CLI tests cover copied contents and hashes, packaged Markdown/HTML references and anchors, omitted runtime dependencies, missing files, unique temporary output, new or empty explicit output, preservation of existing data, source/output path separation, symlinks and cleanup after failure. This validates a local runtime copy; it does not establish dependency availability, npx installation or skill discovery in a new session.

## Badge catalog integration (2026-10-24)

The current awesome-readme Tools section was retrieved and its badge-like dynamic SVG tools were traced to their project documentation. Five working remote recipes are now directly callable from the badge catalog: GitHub Stats Extended, GitHub PR Stats, GitHub Licenses Stats, README Typing SVG, and Telegram Card. Each returned HTTP 200 with the documented image type in a direct request. Sourcerer Hall-of-fame was reviewed but withheld because its documented endpoint failed during the TLS connection; general README generators remain manual design references rather than badge APIs.

The catalog separates ordinary project badges from personal profile cards, records URL-encoding and link-destination rules, and includes the local `user-statistician` GitHub Action path with its write-permission warning. Runtime packaging now includes the catalog. The full Python suite passed 62 tests; preview CLI syntax and non-browser tests passed, while its four browser integration cases were skipped because module roots were not configured. The bundled documentation auditor reported zero errors and warnings. Remote image appearance and GitHub's live renderer were not automatically captured by these checks.

## Repeatable source checks

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/audit_readme.py scripts/package_skill.py tests/test_audit_readme.py tests/test_package_skill.py
node --test tests/test_preview_readme.mjs
node --check scripts/preview_readme.mjs
python3 scripts/audit_readme.py --repo . \
  --single SKILL.md \
  --single references/content.md \
  --single references/visuals.md \
  --single references/validation.md \
  --single docs/verification.md
```

The suite contains process-level auditor tests for both valid documents and specific structural defects. Skill frontmatter was checked with the Codex skill-creator validator during the 2026-10-23 verification. The repository has no configured type checker; Python compilation and Node syntax checks are not described as type checking.

To include the preview suite's real-browser cases, point it at existing tooling:

```sh
YOHO_PREVIEW_MODULE_ROOTS=/path/to/tooling/node_modules \
YOHO_PREVIEW_BROWSER=/path/to/chromium \
node --test tests/test_preview_readme.mjs
```

For multiple module roots, separate paths with the platform's path delimiter (`:` on macOS/Linux, `;` on Windows). The browser variable is optional when Playwright already resolves its browser. These tests create isolated temporary target projects and keep dependencies outside the repository.

Renderer reproduction requirements and commands are in [the helper reference](../references/validation.md). The trials used Python 3.12.10, Marked 17.0.5, sanitize-html 2.18.1, Playwright 1.62.1 and an installed Chromium browser. Preview tooling stayed outside target dependency manifests.

## Limits

- Local rendering is a sanitized GFM approximation. GitHub's live rendering, Camo behavior and Mermaid runtime were not verified.
- Optional image generation, remote images/URLs and a new-session skill-discovery check were not exercised.
- The Line Tally optional pip installation, unreadable-file case and other Python/OS versions were not tested. Source execution was verified instead.
- These representative CLI/library and constrained-environment trials do not establish every project type, platform or tool combination.

The personal installation contains only the skill entry point, interface metadata, three references and two scripts. Delivery compares all seven files against source; tests and scratch artifacts are excluded.
