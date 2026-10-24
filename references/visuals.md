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
| [Engineering Quickstart / 工程速览](#engineering-quickstart-recipe) | Left-aligned value statement, small input/output or command example, immediate quick start | Libraries and CLI tools; practical use leads, with lighter brand treatment |
| [Product Showcase / 产品演示](#product-showcase-recipe) | A representative interface or output capture leads into a small gallery of real user tasks and capabilities | Apps and visual tools; requires authentic captures rather than conceptual UI |
| [Editorial Overview / 品牌叙事](#editorial-overview-recipe) | Restrained cover or illustration, clear typography, short explanation of the problem and approach | Projects needing context; conceptual artwork must be identified as such |
| [Workflow Guide / 流程导览](#workflow-guide-recipe) | Readable process or architecture diagram, inputs/outputs, and a route to first use | Services, skills, and developer workflows; simplify diagrams for phone readability |

If there is no real interface to capture, favor engineering, editorial, or workflow alternatives over a fabricated product showcase.

After selection, follow the matching recipe below. Each recipe changes the reading path and evidence treatment, while the [core content coverage](content.md#baseline-content-template) stays consistent. Keep shared asset and badge decisions in their sections rather than repeating them in each recipe.

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

## Engineering Quickstart recipe

Use this family when one real operation explains the target project's value: a command, a public library call, or another concrete entry action.

- **Lead with a small working example.** Use a left-aligned project title, one-sentence outcome, language switch and useful next link, then a concise command or call with a labeled result. For a file-based CLI, show the relevant input, actual invocation and resulting summary; for a library, show a complete public call and its return. Keep commands and results selectable, and distinguish observed output from an expectation supported only by source.
- **Connect the example to first use.** State the example's starting conditions and where to run it. Follow with the actual prerequisites, install/access and necessary configuration so a new reader can reproduce the same result. Reuse that task in Usage when it already teaches the main operation; move long options or additional examples into the body or existing reference docs.
- **Use a truthful fallback.** When there is no command or public call, demonstrate the project's real entry action and outcome. If execution is unavailable, retain a source-supported example, record the gap, and label the expected result accurately. A terminal screenshot is supplementary; the usable example remains text.
- **Inspect the engineering path.** Check that the lead example and quick start use the same supported options and prerequisites, results agree with the evidence, and long commands scroll within their code block on mobile. Confirm the reader can find installation before attempting an example that assumes it.

## Product Showcase recipe

Use this family when the target project has a real interface or visual output that helps explain its value. Product screenshots show the running target project; README preview screenshots show the document's layout. The [preview helper](../scripts/preview_readme.mjs) produces the latter and does not launch or capture product pages.

After selecting this direction, prepare the product screenshots before completing the final README pair:

1. **Plan the story.** Choose one representative overview or successful task as the lead image, usually with two or three supporting screenshots showing distinct capabilities or steps. Reduce the set when fewer images explain the product; avoid repeated pages and a fixed screenshot quota. Keep the first-use action easy to reach.
2. **Obtain authentic captures.** Reuse existing screenshots after confirming that they match the current product. When new captures are needed, follow the project's setup instructions and use available browser or native screenshot tools on the running application or an accessible real demo. Use demonstration data and exclude credentials and personal information. Record each image's source route or file, demonstrated state, setup/capture steps, and verification status in the evidence note.
3. **Prepare the selected assets.** Crop to the relevant interface or result without changing what the product shows. Keep enough context to identify the task, and consistent scale across comparable screens. Use PNG or WebP for UI captures, descriptive filenames and the project's asset convention. Keep originals and rejected variants in scratch; publish only the selected captures.
4. **Place images with their explanation.** Put the lead capture near the value proposition and useful entry links. Place supporting images beside the relevant Features or Usage explanation, or in a short Screenshots section when that reads better. Give each a concise, factual caption and specific alt text. Prefer a readable vertical sequence of normal Markdown images; keep essential instructions as text and avoid image walls that delay installation or first use.
5. **Localize and inspect.** Reuse the same truthful assets across both editions where possible, with equivalent captions and localized alt text. Capture another UI language only if the product actually supports it. Inspect the images at their displayed desktop and mobile sizes; use focused crops when important controls or results become unreadable. Follow [visual acceptance](validation.md#visual-acceptance) for the final document views.

For a requested three-direction comparison, use an authentic lead capture in the Product Showcase candidate; build its supporting gallery after selection. A gallery does not trigger a new style comparison or approval round.

If new capture is blocked, use verified existing captures or actual visual output where they suffice, and report what could not be checked. If no authentic capture is available, omit the gallery and state the gap; conceptual artwork cannot replace product evidence. Prefer Engineering Quickstart, Editorial Overview or Workflow Guide when there is no real interface or visual output to show. Preserve an explicitly chosen direction unless the user changes it or has delegated the choice.

Other families may borrow a small screenshot section when it explains a concrete capability, while retaining their own visual lead. Product-page capture is not a mandatory step for every README or style.

## Editorial Overview recipe

Use this family when the reader needs to understand the problem and approach before the project's capabilities make sense.

- **Build a short narrative lead.** Put the project identity, one-sentence value proposition, language switch and first-use link near the top. Follow with a specific problem and the project's approach, using restrained typography and optional artwork. Continue into one concrete capability or example before expanding the background. The sequence is problem → approach → evidence → first use, with the first-use link already available in the opening.
- **Give the story a useful destination.** Connect the explanation to the reader's actual task, then place the shortest working start before longer history, comparisons or design rationale. Merge repeated introduction and feature prose. Retain the other core content roles at the depth the target project needs.
- **Make artwork optional.** Use existing or clearly labeled conceptual artwork according to [asset selection](#asset-selection). A text-led composition is complete when no useful visual exists. Derive the narrative from source and actual behavior rather than inventing project history, adoption, customer outcomes or benchmark claims.
- **Inspect the editorial path.** Check that the cover does not displace the purpose and useful entry, the problem and approach are distinct rather than repeated slogans, and the stated capability has concrete support. Review the transition to technical instructions and the mobile hierarchy, including essential prose outside artwork.

## Workflow Guide recipe

Use this family when understanding the route from input to result helps the reader operate the target project or choose the right entry point.

- **Draw one useful path.** Start with project identity, a concise outcome, language switch and first-use link. Show a compact flow of the real input, processing or decisions, and output. Include only steps and transitions supported by implementation or evidence; distinguish optional branches and user actions from automatic behavior. A CSV tool might show file → validated rows → summary, with invalid input described where it changes the outcome.
- **Connect the flow to executable steps.** Pair the visual with an ordered text path whose step names match the diagram, then show the actual setup and smallest run. Keep commands, configuration and important limits outside the image. Explain where a reader starts and what confirms completion; an architecture overview alone is insufficient for first use.
- **Keep the path readable without rendering.** Follow the shared [diagram guidance](#github-is-the-publication-surface). Use a small maintainable diagram; split detailed branches into the body when labels become too small on a phone. When Mermaid or image rendering is unavailable, provide the equivalent ordered Markdown steps and state the visual gap. A text-led workflow remains a valid selected direction.
- **Inspect the workflow path.** Trace each step and transition to real behavior, check that the text and diagram describe the same starting state and result, and read every essential label at mobile display size. Verify the text path remains usable if the diagram fails to render, including any error or persistence limitation that affects the task.

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

Generate badges through the selected tool's direct recipe in [badges.md](badges.md). For a service-specific endpoint or parameter not covered there, inspect current official documentation before using it. For offline static SVG, resolve an existing Badgen or [badge-maker](https://github.com/badges/shields/tree/master/badge-maker) installation, or install only in a separate tooling directory. Keep static technology labels factual and trace them to source or configuration; a technology version may be static only when the project declares that version. Release versions, coverage, statuses, and other changing metrics should use their live data source rather than a static success image. Link each badge to its underlying source, workflow, package, license, public profile, or relevant documentation and give it meaningful alt text.

Select only working badges for the final README. Remote badge URLs may not load in the local preview helper; inspect them in an available browser or report them as unverified. Do not bake live badges into local images just to pass the preview. Recheck provider availability and current documentation before using endpoints or parameters.

## Other tools

Prefer available repository preview tools, browser screenshots, diagram renderers, and image-generation tools. Discover runtimes and dependency locations through the current environment instead of carrying machine paths in the skill.

The optional preview helper needs Node, `marked`, `sanitize-html`, and Playwright plus a working Chromium browser. It accepts an explicit module root and browser path. It uses locally served content and GitHub-like typography, strips unsupported raw HTML, records image failures and horizontal overflow, and saves four views per candidate. Its CSS is a review aid, not a publication dependency. Read [validation.md](validation.md) for the command and limits.

For additional tools, consult [awesome-readme's recording tools](https://github.com/matiassingers/awesome-readme#creating-gifs) when an actual terminal recording is needed. Its Tools list is already distilled into the [badge catalog](badges.md); a listing is not a dependency or an endorsement of every profile widget. Keep a static, tool-independent path available.

## Sources to recheck when compatibility matters

- GitHub markup and sanitization pipeline: https://github.com/github/markup
- GitHub diagrams: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- Centered HTML Hero and baseline chapter structure: https://github.com/othneildrew/Best-README-Template
- Curated project READMEs, architecture examples, and tools: https://github.com/matiassingers/awesome-readme
- Example information architecture, not a universal standard: https://github.com/microsoft/vscode and https://github.com/cli/cli

These sources were inspected on 2026-10-23. Consult current official documentation when relying on a feature whose behavior may have changed.
