# Badge and dynamic SVG recipes

This is the direct-call catalog for badge and badge-like README visuals. [Visual style and selection](visuals.md#badge-decisions-and-tools) decides whether a visual belongs; this guide decides how to call the selected provider. Substitute placeholders only with values verified from the target repository, public profile, or user-provided facts. Keep the final Markdown copyable and give every image meaningful alternate text.

The dynamic-image entries below were selected from the Tools section of [awesome-readme](https://github.com/matiassingers/awesome-readme#tools) on 2026-10-24. General README generators and editors in that list are authoring interfaces, not badge APIs, and are not invoked automatically by this skill.

During that source review, direct requests to the five remote card endpoints documented below returned HTTP 200 with their documented image type. The Sourcerer Hall-of-fame endpoint did not complete its TLS connection. Availability is not a compatibility guarantee, so repeat the direct check whenever a final README uses a remote URL.

## Calling rules

- URL-encode every substituted path and query value. In particular, encode spaces, `#`, `?`, `&`, and commas unless a documented parameter explicitly uses commas as a separator.
- Prefer a linked Markdown image: `[![Descriptive alt](image-url)](destination)`. Link to the data source, exact workflow, package, license, public profile/account, or relevant documentation—not to an unrelated marketing page.
- Before publication, make a direct request to every remote image URL and accept only a successful response of the expected image type. A convenient check is:

```sh
curl -fsSL -o /dev/null \
  -w '%{http_code} %{content_type}\n' \
  'https://example.invalid/badge.svg'
```

- Inspect the rendered image in an available browser as well as the bundled README preview. The local preview intentionally does not fetch remote resources.
- Do not turn a remote live value into a static SVG or PNG merely to satisfy the preview. If the endpoint, required account, or browser check is unavailable, either omit the optional visual or report it as unverified.
- Keep one consistent badge treatment in the final row. Use a dynamic card only when its claim and reader value are clearer than text or omission.

## Core badge calls

### Shields.io

Use Shields for verified descriptive labels and for documented live package, license, workflow-adjacent, or service integrations. A static technology label may state a version only when the target project declares that version.

```md
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](#requirements)
```

Use `flat` for a compact row, `flat-square` for square corners, or `for-the-badge` for a prominent uppercase row. Prefer the style already selected for the README family. For an unsupported service parameter, consult Shields' current documentation rather than guessing an endpoint.

### GitHub Actions

Use the exact workflow filename and branch. This badge reports that workflow's status, not general project quality.

```md
[![CI](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml/badge.svg?branch=main)](https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml)
```

### Badgen

Use a documented Badgen service endpoint, or generate an offline SVG with an existing local Badgen installation. There is no single universal Badgen URL: treat an endpoint without current documentation as unsupported. If an offline badge is required, resolve an existing Badgen or `badge-maker` installation; install a generator only in a separate tooling directory.

## Profile and portfolio dynamic cards

These cards describe a person or account. Do not add them to an ordinary project README merely to fill the hero. Use one when the target is a GitHub profile/portfolio README, the user explicitly asks for that identity story, or an existing section already serves that purpose.

| Need | Direct call | Notes |
| --- | --- | --- |
| Public GitHub aggregate statistics | `https://github-stats-extended.vercel.app/api?username=USERNAME` | Also supports top-language, WakaTime, repository-pin, and gist cards. |
| Public pull-request contribution story | `https://github-pr-stats-five.vercel.app/api/github-pr-stats?username=USERNAME` | Add `mode=repo-aggregate` for a repository overview or focused filters such as `status=merged`. |
| Licenses across a user's public repositories | `https://github-licenses-stats.vercel.app/api/top-licenses?username=USERNAME&count=5` | `count` is capped at 10. |
| Animated typed introduction | `https://readme-typing-svg.demolab.com/?lines=FIRST;SECOND` | Decorative animation; use only when requested or clearly useful. |
| Public Telegram identity and audience | `https://telegram-card.malith.dev/?username=USERNAME` | Verify that the public account and displayed counts are appropriate to expose. |

### GitHub Stats Extended

Use the relevant card endpoint and link to the public GitHub profile, repository, gist, or WakaTime account that supplies the data. Common calls are:

```md
[![USERNAME's GitHub stats](https://github-stats-extended.vercel.app/api?username=USERNAME)](https://github.com/USERNAME)
[![USERNAME's top languages](https://github-stats-extended.vercel.app/api/top-langs/?username=USERNAME&langs_count=4)](https://github.com/USERNAME)
[![REPO](https://github-stats-extended.vercel.app/api/pin/?username=USERNAME&repo=REPO)](https://github.com/USERNAME/REPO)
```

Add only documented parameters such as `theme`, `show_icons`, or card-specific fields. Check the rendered dimensions at mobile width; a card can overwhelm a small profile README.

### GitHub PR Stats

Use this for a personal contribution timeline or aggregate impact overview, not as evidence that a target project is high quality.

```md
[![USERNAME's recent pull requests](https://github-pr-stats-five.vercel.app/api/github-pr-stats?username=USERNAME&limit=5)](https://github.com/USERNAME)
[![USERNAME's repository impact](https://github-pr-stats-five.vercel.app/api/github-pr-stats?username=USERNAME&mode=repo-aggregate&limit=5)](https://github.com/USERNAME)
```

Documented filters include `status`, `min_stars`, `limit`, and `theme`. For a long-lived or high-traffic profile, consider the project's deployment guide so the visual does not depend on a shared demo deployment.

### GitHub Licenses Stats

Use this only when a user's license distribution across public repositories is relevant information rather than decoration.

```md
[![USERNAME's public repository licenses](https://github-licenses-stats.vercel.app/api/top-licenses?username=USERNAME&count=5&theme=light)](https://github.com/USERNAME?tab=repositories)
```

`count` defaults to 5 and cannot exceed 10. Select a theme that remains readable in both GitHub themes.

### README Typing SVG

Use concise factual text. Separate lines with the documented `;` separator and encode spaces (`First+line` or `First%20line`). Set a width that fits the longest line without forcing mobile overflow.

```md
[![Typing introduction](https://readme-typing-svg.demolab.com/?lines=Verified+headline;Useful+next+action&width=380&height=50)](#introduction)
```

Common options include `font`, `size`, `color`, `background`, `center`, `duration`, `pause`, and `repeat`. Do not animate unsupported claims, adoption numbers, or release statuses.

### Telegram Card

Use this when the profile legitimately centers a public Telegram channel, group, bot, or account. The endpoint supports `theme`; color and font parameters include `bgColor`, `textColor`, `subtleTextColor`, `extraColor`, `shadowColor`, and `fontFamily`.

```md
[![@USERNAME on Telegram](https://telegram-card.malith.dev/?username=USERNAME&theme=dark)](https://t.me/USERNAME)
```

The service returns a raster image, unlike the SVG endpoints above. Confirm that exposing subscriber, member, usage, or online counts is useful and acceptable to the account owner.

## Generated local profile statistics

The [user-statistician](https://github.com/cicirello/user-statistician) GitHub Action generates a local SVG and commits it to the profile repository. This avoids a remote card dependency, but it changes repository behavior and grants the workflow contents write permission, so do not introduce it silently during a README-only rewrite.

When the user has requested that workflow, the minimal scheduled form is:

```yml
name: user-statistician

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v6
      - name: Generate the user stats image
        uses: cicirello/user-statistician@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The default output is `images/userstats.svg`, referenced as:

```md
[![USERNAME's GitHub statistics](images/userstats.svg)](https://github.com/USERNAME)
```

Run the workflow once and inspect the committed SVG before presenting the README as complete. Use the action's current inputs for themes, sections, output filename, locale, and animations.

## Reviewed but not enabled

[Hall-of-fame](https://github.com/sourcerer-io/hall-of-fame) appears in the awesome-readme Tools list and documents eight linked avatar images per repository, but its documented `sourcerer.io` image endpoint did not complete a TLS connection during the 2026-10-24 availability check. Do not emit those URLs unless a current request succeeds or the user supplies a working self-hosted endpoint. A plain contributor list or GitHub's contributor view remains the tool-independent fallback.

The other awesome-readme Tools entries are README templates, editors, or whole-document generators. They can inform manual design work when explicitly requested, but they have no badge API to call and do not replace the evidence-driven README workflow.
