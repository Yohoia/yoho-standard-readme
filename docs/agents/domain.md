# Domain Docs

This repo uses a single-context layout: `GLOSSARY.md` at the repo root and ADRs under `docs/adr/`.

## Before exploring, read these

- `GLOSSARY.md` at the repo root.
- If `GLOSSARY-MAP.md` exists at the repo root, follow it to each glossary relevant to the topic.
- ADRs in `docs/adr/` that touch the area you are about to work in. If the repo later adopts multiple contexts, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files do not exist, proceed silently. Do not flag their absence or suggest creating them upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates them lazily when terms or decisions actually get resolved.

## File structure

- `/GLOSSARY.md`: shared domain vocabulary.
- `/docs/adr/NNNN-<decision-slug>.md`: architectural decisions, numbered from `0001`.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, or a test name), use the term as defined in `GLOSSARY.md`. Avoid synonyms the glossary explicitly rejects.

If a needed concept is missing, reconsider whether the language fits the project. Note genuine gaps for `/domain-modeling`.

## Flag ADR conflicts

If your output contradicts an existing ADR, surface the conflict explicitly, identifying the ADR and explaining why the decision is worth reopening.
