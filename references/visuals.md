# Visual style, assets, and badge choices

This reference owns the visual-direction workflow, style recipes, asset rules, and badge decisions.

## Decide the visual direction

Inventory the target project's existing logos, screenshots, diagrams, and verifiable badge sources. Identify its primary languages, runtimes, frameworks, and platforms from source and configuration.

| User's current intent | Action |
| --- | --- |
| A style is already chosen | Reuse the choice and continue with that direction. |
| The choice is delegated | State a project-specific recommendation and proceed. |
| No choice or delegation exists | Ask a short style question: choose a family, delegate the choice, or request a comparison. Present the five families below with a brief project-specific recommendation and any asset requirement. |
| A comparison is requested | Follow [Make alternatives comparable](#make-alternatives-comparable), then wait for the user to select a candidate. |

Resolve the direction before editing either final README or publishing final assets. After a direct choice, delegated recommendation, or preview selection, implement and verify without another routine approval round. Record the chosen style, technology badge sources, and status badge decisions in the evidence note.

## Reusable style repertoire

Adapt these five families to the actual project. When the user is undecided, offer a comparison; create it only after they request it.

| Family | Composition and emphasis | Best fit / trade-off |
| --- | --- | --- |
| Centered Brand Hero / 居中品牌 Hero | Optional existing logo, project title, slogan, tags or badges, navigation, and introduction; optional real demo follows | A memorable project identity; keep the first useful action close to the title |
| Engineering Quickstart / 工程速览 | Left-aligned value statement, small input/output or command example, immediate quick start | Libraries and CLI tools; practical use leads, with lighter brand treatment |
| Product Showcase / 产品演示 | Actual interface or output capture leads into a user task and capabilities | Apps and visual tools; requires an authentic capture rather than conceptual UI |
| Editorial Overview / 品牌叙事 | Restrained cover or illustration, clear typography, short explanation of the problem and approach | Projects needing context; conceptual artwork must be identified as such |
| Workflow Guide / 流程导览 | Readable process or architecture diagram, inputs/outputs, and a route to first use | Services, skills, and developer workflows; simplify diagrams for phone readability |

If there is no real interface to capture, favor engineering, editorial, or workflow alternatives over a fabricated product showcase.

## Centered Brand Hero recipe

Build a compact stack, typically **existing logo (if present) → project title → one-sentence slogan → badges/tags → useful links → brief introduction or real demonstration**. Without a repository logo, start with the project title as text. Move a one- or two-sentence introduction above the badges when that reads better. Keep the language switch near the top within this block.

- Use the logo and badge row selected under [Asset selection](#asset-selection) and [Badge decisions and tools](#badge-decisions-and-tools).
- Offer a real homepage, docs, demo, install, or repository destination as appropriate. Omit absent destinations and preserve a clear next action using a body-section link.
- Keep the slogan, links, and introduction as selectable text. Let badge/link rows wrap naturally; keep the logo modest in size and avoid spacer walls that push first use off the screen.
- Center the Hero, then return to normal left-aligned prose, lists, and code for the technical body. A compact centered introduction is optional; long paragraphs remain in the body.

Use a simple HTML block for alignment, with HTML links and emphasis inside it. Close the block and leave a blank line before resuming Markdown. This pattern also works with the bundled preview helper without relying on heading-specific alignment attributes:

```html
<div align="center">
  <p><img src="docs/assets/logo.svg" alt="Project name logo" width="88"></p>
  <h1>Project name</h1>
  <p><strong>A concrete, project-specific value proposition.</strong></p>
  <p>English · <a href="README.zh-CN.md">简体中文</a></p>
  <p>
    <a href="#getting-started">Get started</a> ·
    <a href="#usage">Usage</a>
  </p>
  <p>A brief introduction explaining the audience and outcome.</p>
</div>
```

This is a structural example, not output to copy unchanged. Substitute real names, asset paths, language links, and body anchors; omit the image paragraph when no project logo exists. Insert verified technology badges in the selected family's placement, and use plain descriptive text when no working badge provider can represent a verified claim. Use supported HTML inside the block rather than Markdown syntax that may remain literal. Navigation should target the actual Markdown body headings, with anchors regenerated for each language. Avoid layout tables, fixed-width containers, inline CSS, and JavaScript.

Check the rendered stack at mobile width: title and slogan can wrap, badges remain readable, links do not widen the page, and the first body section follows without excessive empty space. Verify any existing logo and badges against both light and dark backgrounds.

## Make alternatives comparable

Use this branch only when the user requests a comparison. Read the project's name, identity, interface, typical output, and audience, then create exactly three genuinely distinct first-screen previews from the repertoire or another explicitly requested direction. Use the actual project name, value proposition, and available evidence. Include Centered Brand Hero unless the user's preferences or project requirements favor a different set.

For each candidate, provide:

- A short direction name, its audience, and why it suits this project.
- A real first-screen Markdown draft with actual title, value proposition, and next step.
- An actual rendered image and an inspectable Markdown source.
- A proposed chapter order using the [baseline content coverage](content.md#baseline-content-template), and the trade-off compared with the other directions.

Vary composition, narrative emphasis, asset treatment, and chapter plans; recoloring one layout is insufficient. Markdown prose still uses GitHub's renderer. Keep essential prose, commands, links, and metadata outside images. At least one next section should remain apparent after the introductory block. The comparison may show English first screens; explain the choices in the user's language and retain room for the Chinese counterpart.

Use the target project's scratch convention, otherwise `.scratch/readme-previews/`. Each candidate has a Markdown source and the assets needed to render it. Keep paths distinct and review assets local, preserving the project's source and asset conventions. Recompute relative paths when moving selected content into the final README location.

Render the previews with available local browser or document tools, then show the images inline or open the comparison page, with inspectable source paths. The optional [preview helper](../scripts/preview_readme.mjs) captures desktop/mobile, light/dark views; see [validation.md](validation.md#render-markdown-and-capture-four-views) for usage and limits. A prose description or a link that was never rendered is not a completed visual preview.

Wait for the user to choose a candidate before writing the final README pair or publishing assets. If rendering is unavailable, report the specific limitation and offer inspectable candidate sources or an explicitly labeled Markdown-only fallback. A fallback is never reported as visual verification.

## GitHub is the publication surface

Use Markdown headings, lists, code fences, tables for actual comparisons, links, simple HTML image sizing/alignment, and `details` for secondary material. GitHub sanitizes rendered HTML; do not base a direction on custom page CSS, scripts, cards, interactive controls, or an independently designed landing page. A local preview is an approximation until checked on GitHub.

Use Mermaid when GitHub's supported diagram syntax is a good fit. Keep its source readable. If the preview renderer does not support Mermaid, render a separate diagram with an available compatible tool or mark that diagram as unverified. A code block containing diagram syntax is not a rendered diagram.

Use simple self-contained SVG for diagrams and explanatory graphics. Include a `viewBox`, accessible title/description, and safe local shapes/text. Avoid script, `foreignObject`, external fonts/stylesheets, and embedded remote resources. Static PNG/WebP is appropriate for photos, generated artwork, or compositions that depend on raster content. Source text requiring frequent changes should remain in Markdown.

Read graphics at their actual displayed size. A diagram that looks good on a large drawing canvas can be illegible on a phone. Simplify or split diagrams whose labels fail on mobile. Prefer transparent-safe assets or deliberate backgrounds that remain readable in both themes.

## Asset selection

Choose assets from the project content and selected style:

- Reuse a verified project logo. If none exists, show the project name as text and omit the logo image; do not invent a replacement mark.
- Use real screenshots for product interfaces, actual output for execution evidence, and diagrams for relationships or workflows.
- Derive additional visuals from the project's actual concepts. Use simple self-contained SVG for diagrams and explanatory graphics, or available image-generation tools / the `imagegen` skill for suitable conceptual raster artwork. Label conceptual artwork; it cannot stand in for the project's logo or evidence of an interface, behavior, benchmark, customer, or feature.
- When a tool is unavailable, complete the direction with existing assets, simple SVG, or Markdown. The skill remains independent of another README skill or a particular service.

Follow existing asset conventions. Publish only the selected assets; keep review variants in scratch rather than adding them to the README.

Keep images purposeful and alt text informative. Avoid text-heavy banner walls, image-only READMEs, excessive decorative separators, long prose inside tables, and copying another project's branding. Add animation only when requested or clearly useful to demonstrate behavior; a clear static fallback is still needed.

## Badge decisions and tools

Distinguish descriptive technology badges from live status badges:

- Automatically include a small, consistent set for verified primary languages, runtimes, frameworks, and platforms when a working provider supports the claim; do not ask whether to show them. Exclude development-only or test-only tools unless they are part of the reader's required setup. Choose provider, treatment, and placement to fit the selected family. Ask about treatment only when the user explicitly requests a comparison or multiple treatments would materially change the design.
- Include live status badges such as CI, coverage, release, or package version only when a relevant maintained source adds value: an exact workflow, release, package, license, coverage endpoint, or other maintained data source. Recommend a suitable treatment; ask about it only when comparison or user preference materially affects the result.

Use only providers that support the verified claim, assessing their actual appearance and maintenance requirements when choosing among them. Omit unsupported claims and unavailable badges; omission or delegated treatment remains an option for optional live status badges.

Place technology badges according to the selected family unless the user requests another arrangement:

| Family | Default technology-badge placement |
| --- | --- |
| Centered Brand Hero | After the title and slogan, before navigation links; keep the row compact. |
| Engineering Quickstart | Beside the short value statement and before the first command or API example. |
| Product Showcase | Near the concise capability introduction, while the authentic interface or output remains the visual lead. |
| Editorial Overview | After the problem-and-approach introduction, before the deeper narrative. |
| Workflow Guide | Beside the process or architecture explanation, before the first-use path. |

| Tool | Available effect / best use | Generation and source |
| --- | --- | --- |
| [Shields.io](https://shields.io/badges) | `flat` for a compact row; `flat-square` for square corners; `for-the-badge` for a more prominent uppercase treatment | Generate a static badge from verified text or select a documented live integration. Adjust `style`, label/color, and optional verified technology icon. |
| [Badgen](https://badgen.net/) | Classic or flat treatments for a compact metadata row | Use a documented service endpoint; [the Badgen library](https://github.com/badgen/badgen) can generate local SVG with `classic` or `flat` styling. |
| [GitHub Actions](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge) | Native workflow name and live status | Use the exact workflow's `badge.svg` URL, with matching branch/event filters when needed. This choice represents workflow status, not arbitrary project metadata. |
| Text labels / no badges | Quiet typography when a badge row adds little value | Use ordinary text or omit the row. |

When comparing providers or styles, generate small samples using the same verified content, colors, and data scope wherever supported. Show rendered samples inline or in the review preview when tools permit; label unavailable rendering clearly. Keep one consistent treatment in the final row rather than showcasing generators.

Generate badges through the selected tool's documented URL/API or local library. Inspect official documentation before using service-specific endpoints or parameters. For offline static SVG, resolve an existing Badgen or [badge-maker](https://github.com/badges/shields/tree/master/badge-maker) installation, or install only in a separate tooling directory. Keep static technology labels factual and trace them to source or configuration; a technology version may be static only when the project declares that version. Release versions, coverage, statuses, and other changing metrics should use their live data source rather than a static success image. Link each badge to its underlying source, workflow, package, license, or relevant documentation and give it meaningful alt text.

Select only working badges for the final README. Remote badge URLs may not load in the local preview helper; inspect them in an available browser or report them as unverified. Do not bake live badges into local images just to pass the preview. Recheck provider availability and current documentation before using endpoints or parameters.

## Other tools

Prefer available repository preview tools, browser screenshots, diagram renderers, and image-generation tools. Discover runtimes and dependency locations through the current environment instead of carrying machine paths in the skill.

The optional preview helper needs Node, `marked`, `sanitize-html`, and Playwright plus a working Chromium browser. It accepts an explicit module root and browser path. It uses locally served content and GitHub-like typography, strips unsupported raw HTML, records image failures and horizontal overflow, and saves four views per candidate. Its CSS is a review aid, not a publication dependency. Read [validation.md](validation.md) for the command and limits.

For additional tools, consult [awesome-readme's tools](https://github.com/matiassingers/awesome-readme#tools) and [recording tools](https://github.com/matiassingers/awesome-readme#creating-gifs) when needed. Select by purpose: evidence-backed badges, actual terminal recordings (for example, VHS), or screenshot/GIF preparation. Verify current tool behavior before use; a listing is not a dependency or an endorsement of every profile widget. Keep a static, tool-independent path available.

## Sources to recheck when compatibility matters

- GitHub markup and sanitization pipeline: https://github.com/github/markup
- GitHub diagrams: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- Centered HTML Hero and baseline chapter structure: https://github.com/othneildrew/Best-README-Template
- Curated project READMEs, architecture examples, and tools: https://github.com/matiassingers/awesome-readme
- Example information architecture, not a universal standard: https://github.com/microsoft/vscode and https://github.com/cli/cli

These sources were inspected on 2026-10-23. Consult current official documentation when relying on a feature whose behavior may have changed.
