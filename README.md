<p align="center">
  <img src="./assets/header.svg" alt="claude-evp — Early Value Proposition (Schwartz tiers)" width="100%">
</p>

# claude-evp

> Replace a $10K–15K positioning sprint with a 22-word line per Schwartz awareness tier — as an agent skill pack.

An Early Value Proposition is a ≤22-word line matched to a Schwartz awareness tier. Same product, five lines, because the unaware buyer and the vendor-comparing buyer are not the same reader.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-evp?style=social)](https://github.com/cmj-hub/claude-evp)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-evp — terminal demo of scoring a Tier-3 EVP" width="100%">
</p>

Verified: strong T3 EVP → **100/100**. "We help companies improve their growth and optimize outcomes." → **59/100**. Catches abstract verbs, missing metrics, missing tradeoffs, tier mismatch.

## Install

Two commands. Works in Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, Continue, Roo, and the rest of the [skills CLI](https://skills.sh) agent list.

```bash
npx skills add cmj-hub/claude-evp --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/claude-evp
/plugin install evp
```

The first line is the cross-harness install. The second is Claude Code's plugin (slash commands + reviewer agents).

npm (from GitHub — this pack is not on npmjs.com):

```bash
npm install github:cmj-hub/claude-evp
npx jmc-evp
```

`npx jmc-evp` runs the same installer as `curl` below.

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-evp/main/install.sh | bash
```

Windows: `iwr https://raw.githubusercontent.com/cmj-hub/claude-evp/main/install.ps1 -useb | iex`

## What you walk out with in 15 minutes

Artifact: three tier lines from the sample PSP (`examples/t3.good.txt`). Score them, then write yours.

```bash
python3 scripts/score_evp.py \
  --evp "For Series-B SaaS in a pipeline gap, we ship 14+ SQLs per month without hiring 2 more SDRs." \
  --tier 3 --icp "Series-B SaaS"
python3 scripts/score_evp.py --evp "We help companies improve their growth and optimize outcomes." --tier 3
```

One loop. One ICP. Example data. Then do yours.

## What this pack will not do

- It will not pick this quarter's PSP.
- It will not invent proof you did not supply.
- It will not write five market-ready ads from a blank page.
- Operator Pass is not required to run the scorer.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Also in the pack

| Piece | Job |
|---|---|
| `evp` orchestrator | Craft / brief / route |
| `scripts/score_evp.py` | Length, outcome, tradeoff, ICP, tier-fit |
| `evp-brief` | Tiers 2 / 3 / 4 side by side |

Sub-skills stay in the repo. First run is the loop above, not the operating system.

## Why 22 words?

Long enough for ICP + pain + outcome + tradeoff. Short enough to drop into a cold-email third line or a hero. If it does not fit, you have two claims. Cut one.

## Which Schwartz tier should I write first?

Most B2B buyers live in Tiers 2–4. Write those three. Tier 5 is a direct ask; most operators start there (their internal view) and wonder why nothing lands. Unaware (Tier 1) is a pain reveal, not a product sentence.

## Do I need Operator Pass to use this?

No. The pack, the scorer, and the sample are MIT. Pass is the catalog, the calibrated endpoints, and the Friday room — compounding, not a gate on the 22-word line.

## Suite, course, Operator Pass

- Suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [EVP Generator](https://jaymountconsulting.com/learn/courses/evp-generator)
- Operator Pass: [https://jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- **[Pain Signal Profile](https://github.com/cmj-hub/claude-psp)** — `claude-psp`
- **[Signal-anchored cold email](https://github.com/cmj-hub/claude-cold-email)** — `claude-cold-email`
- **[Four-pillar founder brand](https://github.com/cmj-hub/claude-founder-brand)** — `claude-founder-brand`
- **[Pricing surgery](https://github.com/cmj-hub/claude-pricing)** — `claude-pricing`
- **[Breakthrough Advertising (Schwartz)](https://github.com/cmj-hub/claude-breakthrough-advertising)** — `claude-breakthrough-advertising`
- **[Johanson / Stanley tutorial email](https://github.com/cmj-hub/claude-johanson-stanley)** — `claude-johanson-stanley`

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com). Public build: [https://jaymountconsulting.com/build](https://jaymountconsulting.com/build). Skill suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills).
