---
name: yoho-standard-readme
description: Rewrite and visually redesign project READMEs with an upfront style choice, evidence-based assets, and synchronized English and Chinese editions. Use for comprehensive GitHub README creation or overhaul, including requests to 美化 README or improve project introductions. For standalone image assets, use a dedicated asset workflow.
metadata:
  version: "1.0.0"
---

# Yoho Standard README

Turn a repository into an accurate, useful project introduction with a deliberate visual identity. Serve a developer encountering the project for the first time. Deliver English `README.md` and Simplified Chinese `README.zh-CN.md`, with reciprocal language links.

## Establish the project facts

Read the target repository's agent instructions, current README and translations, package metadata, lockfiles, entry points, examples, tests, documentation, license, and relevant CI workflows. Inspect the files that establish the public behavior; adapt the investigation to the project instead of scanning everything.

Keep a compact [evidence note](references/content.md#evidence-and-uncertainty) in the project's scratch area and reuse it through writing and bilingual review. Verify installation and usage against the current project; existing prose can be stale. External repositories inform presentation, not the target project's capabilities.

Read [content.md](references/content.md) for the baseline content template, project-type adaptations, and bilingual rewrite. Resolve gaps that block a truthful introduction or first successful use. Ask only for facts you cannot establish yourself; omit optional unsupported claims. Preserve legal notices, attribution, and important existing instructions.

## Choose the visual direction

Read [visuals.md](references/visuals.md) before making style, asset, badge, or preview decisions; it owns the detailed rules. When a badge or badge-like visual is warranted, use the direct provider recipe in [badges.md](references/badges.md) instead of rediscovering the tool. Follow the selection flow, including the comparison branch when requested. Resolve the visual direction before editing either final README or publishing final assets, then continue with the selected or delegated direction.

## Complete the selected direction

Write the full English and Chinese READMEs. Keep facts, commands, parameters, requirements, limitations, and link destinations equivalent while allowing natural prose in each language. Retain copyable Markdown text and code for the substantive introduction and usage. Follow the selected family's recipe in the [style repertoire](references/visuals.md#reusable-style-repertoire) and the shared [asset rules](references/visuals.md#asset-selection).

Create deeper API, architecture, deployment, or contribution docs only when the reader needs them and the repository does not already provide a suitable destination. Follow existing documentation conventions. Update moved language links and relevant incoming documentation links deliberately.

## Verify and hand off

Read [validation.md](references/validation.md). Run the bundled structural auditor, inspect the selected rendering at desktop/mobile widths and light/dark backgrounds, and check the first-use path against the actual project. Use the evidence note to review bilingual coverage and claims separately: a structural script cannot establish either.

Report the changed files, chosen direction, checks actually completed, and concrete remaining gaps. Distinguish a local approximation from a check on GitHub itself. Keep the final handoff concise and use the user's language.
