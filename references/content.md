# Content decisions

## The reading path

The first screen should identify the project, explain who benefits and how, and offer a useful next step. Follow with concrete evidence, the shortest working first-use path, and the details needed to adopt or contribute. A long table of contents should not displace the introduction.

Start from the baseline below, then adapt headings and depth to reader tasks. A small utility can merge sections; a complex service needs more than installation and a feature list. Move long reference material to an existing documentation destination or a focused new page.

## Baseline content template

Cover these seven roles in both editions. They are required information, not seven compulsory heading strings; combine overlapping material without repeating examples. Visual styles change the composition and emphasis, while this coverage stays consistent.

| Role | Minimum useful content |
| --- | --- |
| Hero / identity | Project name, one-sentence value proposition, intended reader, language switch, and a useful next action. Logo, badges, and homepage links depend on real assets and destinations. |
| About | The problem, the project's approach, and who should use it. Explain scope in concrete terms. |
| Features | The main supported capabilities and a useful example, output, or real screenshot when available. Distinguish released behavior from plans. |
| Getting started | Actual prerequisites, installation or access, required configuration, and the shortest first successful run with its expected result. |
| Usage | A complete practical task with copyable commands or code and enough explanation to understand the outcome. It may share the getting-started example for a small project. |
| Documentation and limitations | Adoption-relevant requirements and known boundaries, plus next reading where it exists. Keep important constraints visible even when linking to deeper docs; avoid inventing limitations or creating empty docs sections. |
| License status | Link and accurately describe the existing license; if no declaration exists, say so without choosing a license or implying permission. Retain legal notices and attribution. |

Use this editable skeleton when planning chapters. Replace every brace/comment with verified content, remove unused optional sections, and localize headings and anchors for the Chinese edition:

```markdown
# {Project name}
{Slogan, short introduction, language switch, and useful entry links}

## Contents
{Optional for a long README; place after the introduction}

## About
{Problem, audience, and approach}

### Features
{Supported capabilities and concrete evidence}

### Built with
{Optional: technologies that help readers understand or adopt the project}

## Getting started
### Prerequisites
{Actual requirements}
### Installation
{Install or access and required configuration}
### First run
{Smallest working task and expected result}

## Usage
{Practical examples; merge with first run when they cover the same task}

## Documentation and limitations
{Known boundaries and existing deeper documentation}

## Roadmap
{Optional: maintainer-backed plans or a real issue/milestone destination}

## Contributing
{Conditional: actual development/test instructions or contribution policy}

## License
{Existing license link or accurate absence statement}

## Contact and support
{Optional: verified, author-published support destinations}

## Acknowledgments
{When relevant; preserve required credits and notices}
```

Keep a development/contribution path when the repository supports one, linking existing guidelines rather than replacing them with a generic fork/PR recipe. Roadmap, support, security, citation, and acknowledgments follow the evidence and project needs. Preserve required credits even when the selected style has no dedicated acknowledgments chapter.

The baseline adapts [Best-README-Template](https://github.com/othneildrew/Best-README-Template)'s About / Getting Started / Usage / community and legal structure. Its sample package commands, framework badges, contact details, and license belong to that example, not the target project. [awesome-readme](https://github.com/matiassingers/awesome-readme) supplies curated examples, architecture references, articles, and tools; use it to find suitable presentation ideas rather than treating it as a mandatory specification. Both were inspected on 2026-10-23. The skill can apply this baseline offline without fetching either repository on every invocation.

## Adapt to project type

| Project type | What establishes value | First successful use | Deeper topics when relevant |
| --- | --- | --- | --- |
| Library or SDK | A concrete input/output example | Install with the actual package manager and call a public API | Compatibility, API reference, migration, errors |
| CLI | A real task and its output | Install, run one command, understand the result | Options, configuration, shell integration |
| Web or desktop app | A real product screenshot and user workflow | Open a working demo or start the app locally | Environment setup, persistence, deployment |
| Backend or service | Request/response behavior and system role | Start dependencies and make a minimal request | Configuration, operational limits, authentication |
| Agent skill or developer tooling | The task it improves and the artifact it produces | Install or invoke it in the supported environment | Workflow gates, dependencies, output locations |
| Research or data project | The question, method, and available evidence | Reproduce the smallest supported result | Data access, methodology, reproducibility, limitations |

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

Change the README pair, necessary documentation, and selected assets. Preserve unrelated work and project behavior. Use existing docs rather than reproducing them with new names. Avoid empty sections, untracked TODO claims, synthetic adoption numbers, ornamental badges, and repeated slogans. Adapt the baseline's heading names and optional chapters while retaining its core information.
