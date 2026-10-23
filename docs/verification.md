# Verification record

Verified on 2026-10-23. This records observed behavior and its limits; it is not a compatibility guarantee or an automated visual regression suite.

## Workflow trials

Trials used isolated target projects, leaving this skill repository's own README unchanged. Style choices were simulated only within those trials.

| Scenario | Observed result |
| --- | --- |
| Line Tally CLI | Reused a completed three-direction trial: twelve rendered candidate views, original README preserved until selection B, then English/Chinese editions with reciprocal links. The recorded 22 CLI checks passed; final editions had eight clean first-screen views and a separate review of full-document captures. The updated auditor also passed the final documents. |
| LabelKit library and migration | Three distinct directions and twelve rendered candidate views preceded selection B. Final English/Chinese introductions used actual library calls. Existing French content, attribution and API/guide destinations were retained; language switches and incoming documentation links were migrated. Final documents and affected references passed structural review. |
| Note Clean with rendering disabled | Three inspectable, explicitly unrendered Markdown candidates preserved the original README until selection A. Final English/Chinese editions had identical runnable examples; six extracted examples executed successfully. No package publication, cloud synchronization, license or compatibility claims were invented. Visual acceptance remained unperformed. |
| Status Count with document/asset defects | Initial audit exited 1 with eleven errors and one warning covering local destinations, anchors, language links, image descriptions, SVG dependencies, unsupported HTML and differing examples. After document/asset repair, it exited 0 with no errors or warnings. Both editions were rendered in eight desktop/mobile light/dark views, with actual first-screen and body inspection. |

Each trial separated source facts, command execution, structural results, bilingual review and visual review. Screenshot reports alone did not establish semantic accuracy or readability. Detailed fixtures, reports and screenshots remain local scratch artifacts rather than installed runtime content.

## Auditor correction

CLI regression tests exposed three related problems:

- Literal HTML inside inline code was treated as embedded HTML, producing false image and unsupported-element errors.
- A literal inline HTML anchor incorrectly satisfied a real fragment link.
- Backtick runs of different lengths incorrectly masked embedded HTML.

The auditor now excludes matched inline code spans consistently from HTML reference parsing and link scanning. Explicit anchors use the same exclusion, while heading text retains its code content. Closing backtick runs must match the opening run length.

Each new regression failed before its correction and passed afterwards. The existing real-HTML and explicit-anchor checks remain covered.

## Repeatable source checks

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/audit_readme.py tests/test_audit_readme.py
node --check scripts/preview_readme.mjs
python3 scripts/audit_readme.py --repo . \
  --single SKILL.md \
  --single references/content.md \
  --single references/visuals.md \
  --single references/validation.md \
  --single docs/verification.md
```

The suite contains 26 process-level auditor tests. Skill frontmatter was also checked with the Codex skill-creator validator. The repository has no configured type checker; Python compilation and Node syntax checks are not described as type checking.

Renderer reproduction requirements and commands are in [the helper reference](../references/validation.md). The trials used Python 3.12.10, Marked 17.0.5, sanitize-html 2.18.1, Playwright 1.62.1 and an installed Chromium browser. Preview tooling stayed outside target dependency manifests.

## Limits

- Local rendering is a sanitized GFM approximation. GitHub's live rendering, Camo behavior and Mermaid runtime were not verified.
- Optional image generation, remote images/URLs and a new-session skill-discovery check were not exercised.
- The Line Tally optional pip installation, unreadable-file case and other Python/OS versions were not tested. Source execution was verified instead.
- These representative CLI/library and constrained-environment trials do not establish every project type, platform or tool combination.

The personal installation contains only the skill entry point, interface metadata, three references and two scripts. Delivery compares all seven files against source; tests and scratch artifacts are excluded.
