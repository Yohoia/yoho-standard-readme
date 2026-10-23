# Three real directions

## Make alternatives comparable

Read the project's name, identity, interface, typical output, and audience before selecting visual directions. Offer three project-specific alternatives. Useful contrasts include a task-first engineering introduction, a product-demo presentation, and a mechanism-led visual explanation. These are examples of contrasts, not three mandatory templates.

For each candidate, provide:

- A short direction name and why it suits this project.
- A real first-screen Markdown draft with actual title, value proposition, and next step.
- An actual rendered image and an inspectable Markdown source.
- A proposed chapter order and the trade-off compared with the other directions.

Vary the reading experience through layout, information emphasis, screenshots/diagrams, and typographic treatment inside assets. Markdown prose still uses GitHub's renderer. Keep essential prose, commands, links, and metadata outside images. At least one next section should remain apparent after the introductory block.

Keep candidate paths distinct and review assets local. When choosing filenames, preserve the project's source and asset conventions. Recompute relative paths when moving the selected content from scratch into the final README location.

## GitHub is the publication surface

Use Markdown headings, lists, code fences, tables for actual comparisons, links, simple HTML image sizing/alignment, and `details` for secondary material. GitHub sanitizes rendered HTML; do not base a direction on custom page CSS, scripts, cards, interactive controls, or an independently designed landing page. A local preview is an approximation until checked on GitHub.

Use Mermaid when GitHub's supported diagram syntax is a good fit. Keep its source readable. If the preview renderer does not support Mermaid, render a separate diagram with an available compatible tool or mark that diagram as unverified. A code block containing diagram syntax is not a rendered diagram.

Use simple self-contained SVG for diagrams or identity graphics. Include a `viewBox`, accessible title/description, and safe local shapes/text. Avoid script, `foreignObject`, external fonts/stylesheets, and embedded remote resources. Static PNG/WebP is appropriate for photos, generated artwork, or compositions that depend on raster content. Source text requiring frequent changes should remain in Markdown.

Read graphics at their actual displayed size. A diagram that looks good on a large drawing canvas can be illegible on a phone. Simplify or split diagrams whose labels fail on mobile. Prefer transparent-safe assets or deliberate backgrounds that remain readable in both themes.

## Asset selection

Use real screenshots for product interfaces, actual output for execution evidence, and diagrams for relationships. Generated artwork may express identity or a concept but cannot serve as proof of an interface, benchmark, customer, or feature. Use image generation only when it improves the selected direction; preserve a tool-independent way to complete the documentation.

Keep images purposeful and alt text informative. Avoid text-heavy banner walls, image-only READMEs, excessive decorative separators, long prose inside tables, and copying another project's branding. Add animation only when requested or clearly useful to demonstrate behavior; a clear static fallback is still needed.

## Tools

Prefer available repository preview tools, browser screenshots, diagram renderers, and image-generation tools. Discover runtimes and dependency locations through the current environment instead of carrying machine paths in the skill.

The optional preview helper needs Node, `marked`, `sanitize-html`, and Playwright plus a working Chromium browser. It accepts an explicit module root and browser path. It uses locally served content and GitHub-like typography, strips unsupported raw HTML, records image failures and horizontal overflow, and saves four views per candidate. Its CSS is a review aid, not a publication dependency. Read [validation.md](validation.md) for the command and limits.

## Sources to recheck when compatibility matters

- GitHub markup and sanitization pipeline: https://github.com/github/markup
- GitHub diagrams: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams
- Example information architecture, not a universal standard: https://github.com/microsoft/vscode and https://github.com/cli/cli

These sources were inspected on 2026-10-23. Consult current official documentation when relying on a feature whose behavior may have changed.
