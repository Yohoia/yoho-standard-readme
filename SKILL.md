---
name: yoho-standard-readme
description: Rewrite and visually redesign project READMEs with three project-specific visual previews and synchronized English and Chinese editions. Use for comprehensive GitHub README creation or overhaul, including requests to 美化 README or improve project introductions. For standalone image assets, use a dedicated asset workflow.
---

# Yoho Standard README

Turn a repository into an accurate, useful project introduction with a deliberate visual identity. Serve a developer encountering the project for the first time. Deliver English `README.md` and Simplified Chinese `README.zh-CN.md`, with reciprocal language links.

## Establish the project facts

Read the target repository's agent instructions, current README and translations, package metadata, lockfiles, entry points, examples, tests, documentation, license, and relevant CI workflows. Inspect the files that establish the public behavior; adapt the investigation to the project instead of scanning everything.

Keep a compact evidence note in the project's scratch area: important claim, source, and whether it was executed, corroborated by code, or remains unresolved. Existing prose can be stale. Verify installation and usage against the current project. External repositories inform presentation, not the target project's capabilities.

Read [content.md](references/content.md) to choose the content structure and manage the bilingual rewrite. Resolve gaps that block a truthful introduction or first successful use. Ask only for facts you cannot establish yourself; omit optional unsupported claims. Preserve legal notices, attribution, and important existing instructions.

## Offer three visual directions

Read [visuals.md](references/visuals.md). Produce exactly three genuinely distinct first-screen previews using the actual project name, value proposition, and available evidence. Vary composition, narrative emphasis, and asset treatment; recoloring one layout is insufficient. Explain each direction's intended audience, trade-off, and proposed chapter order.

Use the target project's existing scratch convention; otherwise stage candidates under `.scratch/readme-previews/`. Each candidate has a Markdown source and the assets needed to render it. The review preview may show the English first screen; describe the choices in the user's language and retain room for the Chinese counterpart.

Render and show actual previews with available local browser or document tools. The optional [preview helper](scripts/preview_readme.mjs) renders Markdown and captures desktop/mobile, light/dark screenshots; usage and its limitations are in [validation.md](references/validation.md). Show the images inline or open the comparison page, with source paths available for inspection. A prose description or a link that was never rendered is not a completed visual preview.

If rendering is unavailable, report the specific limitation and offer inspectable candidate sources or an explicitly labeled Markdown-only fallback. Obtain a style choice before continuing to the full rewrite. A fallback is never reported as visual verification.

**Wait for the user's style selection.** If the user already selected one of this project's current previews, use that choice. Do not silently pick a style or replace the target READMEs while the choice is pending. Once selected, implement and verify without another routine approval round.

## Complete the selected direction

Write the full English and Chinese READMEs. Keep facts, commands, parameters, requirements, limitations, and link destinations equivalent while allowing natural prose in each language. Retain copyable Markdown text and code for the substantive introduction and usage.

Use project-specific screenshots and diagrams as evidence. When generated artwork would strengthen the chosen direction, use available image-generation tools or the `imagegen` skill if installed. Generated artwork illustrates an idea; actual interface or execution claims require real captures. Keep an alternative path using existing assets, simple SVG, or Markdown when a tool is missing. The skill does not depend on another README skill or a particular service.

Create deeper API, architecture, deployment, or contribution docs only when the reader needs them and the repository does not already provide a suitable destination. Follow existing documentation and asset conventions. Publish only the selected assets; keep review variants in scratch rather than adding them to the README. Update moved language links and relevant incoming documentation links deliberately.

## Verify and hand off

Read [validation.md](references/validation.md). Run the bundled structural auditor, inspect the selected rendering at desktop/mobile widths and light/dark backgrounds, and check the first-use path against the actual project. Review bilingual equivalence and claims separately: a structural script cannot establish either.

Report the changed files, chosen direction, checks actually completed, and concrete remaining gaps. Distinguish a local approximation from a check on GitHub itself. Keep the final handoff concise and use the user's language.
