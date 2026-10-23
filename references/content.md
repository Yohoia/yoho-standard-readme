# Content decisions

## The reading path

The first screen should identify the project, explain who benefits and how, and offer a useful next step. Follow with concrete evidence, the shortest working first-use path, and the details needed to adopt or contribute. A long table of contents should not displace the introduction.

Choose sections according to reader tasks. A small utility does not need an enterprise architecture chapter; a complex service needs more than installation and a feature list. Move long reference material to an existing documentation destination or a focused new page.

| Project type | What establishes value | First successful use | Deeper topics when relevant |
| --- | --- | --- | --- |
| Library or SDK | A concrete input/output example | Install with the actual package manager and call a public API | Compatibility, API reference, migration, errors |
| CLI | A real task and its output | Install, run one command, understand the result | Options, configuration, shell integration |
| Web or desktop app | A real product screenshot and user workflow | Open a working demo or start the app locally | Environment setup, persistence, deployment |
| Backend or service | Request/response behavior and system role | Start dependencies and make a minimal request | Configuration, operational limits, authentication |
| Agent skill or developer tooling | The task it improves and the artifact it produces | Install or invoke it in the supported environment | Workflow gates, dependencies, output locations |
| Research or data project | The question, method, and available evidence | Reproduce the smallest supported result | Data access, methodology, reproducibility, limitations |

Core coverage normally includes identity/value, demonstrated capabilities, prerequisites, first use, a minimal useful example, and adoption-relevant limits. Link license and contribution information when present. Add status, support channels, security policy, citation, or roadmap only when the project has a real basis for them. Explain a missing license accurately rather than selecting one for the author.

## Evidence and uncertainty

Keep evidence notes outside the published README unless the source benefits readers. A short table is sufficient:

| Claim or instruction | Source | Confidence/check |
| --- | --- | --- |
| Actual capability or command | File, symbol, example, or official source | Executed / supported by source / unresolved |

Trace badges to real repository URLs and workflows. Trace package names, versions, prerequisites, and flags to manifests or implementations. Benchmarks require a real method and measured result. Logos, customer claims, sponsorship, production-readiness, and compatibility are not decorative filler.

Run an appropriate quick-start example in a suitable local or temporary environment when possible. Use existing project commands and declared dependencies. If a command would operate on real external state, choose a supported local/dry-run path or explain the execution gap. Never present a command as executed just because a process or installer started.

## English and Chinese editions

Always make `README.md` English and `README.zh-CN.md` Simplified Chinese. Add reciprocal language links near the top. Inventory existing translations before replacing anything; preserve useful technical details and original legal/credit wording. Update language-switch links and affected documentation references when migrating names. Preserve other language editions and explain any additional migration that cannot be completed safely within the documentation scope.

Translate explanations and captions, not identifiers, package names, command flags, paths, or output that the program actually emits. Both editions need the same material facts, feature status, prerequisites, parameters, warnings, and useful destinations. Adapt heading text naturally and regenerate local anchors for each edition. Use identical runnable code when the task is identical; explain an intentional locale-specific difference in the evidence note.

New deep docs should follow the repository's language conventions. A shared reference can remain in its original language if both READMEs identify it accurately. Do not imply a destination is translated when it is not.

## Scope of the rewrite

Change the README pair, necessary documentation, and selected assets. Preserve unrelated work and project behavior. Use existing docs rather than reproducing them with new names. Avoid empty sections, untracked TODO claims, synthetic adoption numbers, ornamental badges, repeated slogans, and a forced universal chapter list.
