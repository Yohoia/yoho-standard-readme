<div align="center">
  <h1>Yoho Standard README</h1>
  <p><strong>A clear introduction. A considered design. Two languages.</strong></p>
  <p>English · <a href="README.zh-CN.md">简体中文</a></p>
  <p>
    <a href="#quick-start">Get started</a> ·
    <a href="#design-choices">Choose a style</a> ·
    <a href="#helper-tools">Helper tools</a>
  </p>
  <p><img src="docs/assets/readme/cover-en.svg" alt="Conceptual artwork showing document designs and English/Chinese editions" width="880"></p>
</div>

A Codex skill for developers who want their repository to be easier to understand and try. It investigates the project, asks you to choose a visual direction, and writes matching English and Simplified Chinese READMEs.

- **Facts first.** Ground capabilities, commands, and visual assets in the target repository.
- **A style you choose.** Pick from five style families, ask the skill to recommend one, or request three visual previews to compare.
- **Two complete editions.** Deliver `README.md` and `README.zh-CN.md` with equivalent facts, examples, and limitations.

## Quick start

### 1. Install the skill

Use Codex with local skill support and choose either installation method.

**Option A · Install with `npx`**

Requires Node.js 22.20 or later, npm with `npx`, and Git. Run this from the project where you want to use the skill:

```sh
npx skills add Yohoia/yoho-standard-readme --agent codex
```

The default scope is the current project. Add `--global` to make the skill available across projects. See the [Skills CLI documentation](https://skills.sh/docs/cli) for installation options and agent support.

**Option B · Ask your agent to install from GitHub**

Send the repository URL and an installation request to an agent that can access GitHub and install local skills:

```text
Install the yoho-standard-readme skill for Codex from:
https://github.com/Yohoia/yoho-standard-readme
The skill is at the repository root. Keep SKILL.md, agents/, references/,
and scripts/ together in the installed skill directory.
```

### 2. Use it in your project

Once Codex has loaded the skill, open the repository you want to document and send:

```text
Use $yoho-standard-readme to redesign this project's README.
Inspect the project, then ask me to choose a visual style before editing.
Show three visual previews only if I ask to compare styles.
Complete README.md and README.zh-CN.md after the choice.
```

The skill checks the project and available assets before asking for your style choice. After you choose, it completes both READMEs, adds necessary supporting material, and verifies the result. Both editions link to one another near the top; commands stay copyable and technical content stays equivalent.

## Design choices

### Five style families

These are visual directions, not fixed page templates. The skill adapts their composition and chapter order to the project's audience and first useful task.

| Style | What leads the page |
| --- | --- |
| **Centered Brand Hero** | A text title or existing logo, slogan, useful links, and a compact introduction |
| **Engineering Quickstart** | A real command or API call and its expected result |
| **Product Showcase** | An authentic interface or output capture and a user workflow |
| **Editorial Overview** | A restrained cover, the problem, and the project's approach |
| **Workflow Guide** | A readable process or architecture diagram and a route to first use |

Choose a family directly or ask the skill to recommend one. Request three first-screen previews when you want a comparison; those vary in composition, emphasis, and chapter plan. Existing READMEs stay in place while you choose. A Centered Brand Hero returns to left-aligned prose and code after the opening block.

### Assets and badges

The skill reuses a verified project logo. Without one, it uses the project name as text. Diagrams and generated illustrations follow the project's actual subject matter; conceptual artwork is identified as such and never stands in for a real interface or performance evidence.

Verified primary-stack technology badges are added automatically when a working provider can represent them. Live status badges depend on useful, maintained data sources. Their presentation follows the selected visual style.

This repository's cover is conceptual artwork; it has no separate logo or CI, coverage, release, or license badge sources.

See the [style and asset recipes](references/visuals.md) for composition, badge providers, and validation rules.

### A shared content baseline

Every final README covers **identity, About, Features, Getting started, Usage, Documentation and limitations, and License status**. Sections can be merged or reordered. Installation, prerequisites, required configuration, and a first successful result remain easy to find.

The [content guide](references/content.md) adapts this baseline to libraries, CLIs, applications, services, skills, and research projects. Existing translations, legal notices, attribution, and useful docs are retained; deeper documentation is added only where it helps readers.

## Workflow

1. **Investigate.** Read the target project's instructions, source, configuration, examples, docs, and assets. Record which claims were executed, supported by source, or remain unresolved.
2. **Choose.** Resolve the visual direction before editing final files, using your existing choice, a direct selection, or a delegated recommendation. Compare three first-screen previews when requested.
3. **Write.** Complete the English and Chinese editions with equivalent facts, prerequisites, commands, parameters, and limitations. Publish only the selected assets.
4. **Verify.** Check structure, actual usage, bilingual equivalence, and desktop/mobile presentation in light and dark themes. Report completed checks and concrete gaps.

Rendering and image generation are optional capabilities. When a requested preview cannot be rendered, the skill provides inspectable Markdown and labels it as unrendered. Existing assets, simple SVG, or Markdown can support the selected design.

## Helper tools

The skill instructions coordinate the rewrite. The scripts support checks; they are not a standalone README generator.

### Structural audit

Requires **Python 3**, using only its standard library. From this skill's checkout:

```sh
python3 scripts/audit_readme.py --repo /path/to/project
```

By default, it checks `README.md` and `README.zh-CN.md`. For an individual document or first-screen candidate:

```sh
python3 scripts/audit_readme.py \
  --repo /path/to/project --single path/to/document.md
```

The JSON report covers local links and fragments, language links, image descriptions, selected incompatible HTML, risky SVG dependencies, and differing runnable examples. Exit `0`: no structural errors; `1`: structural errors; `2`: argument or reading failure. Review warnings separately. The auditor does not execute examples, check remote URLs, establish facts, or judge translation quality.

### Local visual preview

Requires **Node.js, `marked`, `sanitize-html`, Playwright, and a working Chromium browser**. Use existing tooling or install extra dependencies in a separate tooling directory; the checkout does not include a package manifest for them.

```sh
node scripts/preview_readme.mjs \
  --repo /path/to/project \
  --out /path/to/project/.scratch/readme-review \
  --module-root /path/to/tooling/node_modules \
  --browser /path/to/chromium \
  README.md README.zh-CN.md
```

Repeat `--module-root` for multiple module locations. Omit it or `--browser` when dependencies or a Playwright browser already resolve. By default, each document produces four first-screen PNGs—900px desktop and 360px mobile, each in light and dark themes—plus a shared `index.html` and `report.json`. Add `--full-page` to capture the complete rendered page in all four views, using a separate output directory to retain both modes.

Exit `0`: ready for visual review; `1`: broken image, page overflow, or empty content; `2`: runtime failure. Remote images are blocked and reported as unverified; Mermaid remains unrendered. Captures approximate GitHub's GFM presentation. Inspect the images and the content below the first screen as well.

Full commands and checking boundaries: [validation guide](references/validation.md).

## Documentation

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main workflow and required decision gates |
| [agents/openai.yaml](agents/openai.yaml) | Codex interface metadata and default prompt |
| [references/content.md](references/content.md) | Content baseline, evidence, and bilingual decisions |
| [references/visuals.md](references/visuals.md) | Style selection, preview, asset, and badge rules |
| [references/validation.md](references/validation.md) | Helper usage and acceptance boundaries |
| [docs/verification.md](docs/verification.md) | Recorded tests and isolated workflow trials |
| [tests/test_audit_readme.py](tests/test_audit_readme.py) | Auditor CLI regression tests |
| [tests/test_preview_readme.mjs](tests/test_preview_readme.mjs) | Preview CLI and optional Chromium integration tests |

### Verification and development

From the checkout, run the auditor and preview CLI tests and the preview helper's syntax check:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_preview_readme.mjs
node --check scripts/preview_readme.mjs
```

The preview suite skips Chromium cases unless `YOHO_PREVIEW_MODULE_ROOTS` identifies existing renderer dependencies; set `YOHO_PREVIEW_BROWSER` when a browser path is required. See the [verification record](docs/verification.md) for full test commands, auditor CLI coverage, and isolated trials covering a CLI, a library with translation migration, unavailable rendering, and document/asset defect repair. For changes to the skill's decisions, also try an isolated target project and inspect its artifacts; the helper tests do not cover complete README redesigns.

Recorded tools include Python 3.12.10, Marked 17.0.5, sanitize-html 2.18.1, Playwright 1.62.1, and an installed Chromium browser. The helper scripts do not declare a minimum Python/Node support policy. These checks do not establish support for every project or environment.

Local previews do not verify GitHub's live renderer, Camo proxy, or Mermaid runtime. Image generation, remote image/URL checks, and skill discovery in a new Codex session were not part of the recorded acceptance.

## Acknowledgments

The content baseline adapts [Best-README-Template](https://github.com/othneildrew/Best-README-Template). [awesome-readme](https://github.com/matiassingers/awesome-readme) supplies additional presentation examples and tools. These references inform structure and design; project claims come from the target repository.

## License

This repository currently contains no license file or license declaration. No license permission is implied by this README.
