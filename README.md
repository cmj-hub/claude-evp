<p align="center">
  <img src="./assets/header.svg" alt="claude-evp — Early Value Proposition (Schwartz tiers)" width="100%">
</p>

# claude-evp

> Same product. Five readers. Five lines. Twenty-two words each.

An Early Value Proposition is a ≤22-word line matched to a Schwartz awareness tier. Same product, five lines, because the unaware buyer and the vendor-comparing buyer are not the same reader.

Most operators write the line they would buy.
That is a Tier-5 line.
Most of the market is not there.

We scored a specific T3 line at **100**.
"We help companies improve their growth and optimize outcomes" scored **59**.

The scorer is Python in this repo. No LLM. No paid API.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-evp?style=social)](https://github.com/cmj-hub/claude-evp)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-evp — terminal demo of scoring a Tier-3 EVP" width="100%">
</p>

## Install

Two commands. Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, and the rest of the [skills CLI](https://skills.sh) list.

```bash
npx skills add cmj-hub/claude-evp --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install evp
```

Also: `npm install github:cmj-hub/claude-evp` then `npx jmc-evp`. Or `curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-evp/main/install.sh | bash`.

## What you walk out with in 15 minutes

Artifact: `examples/t3.good.txt`.

```bash
python3 scripts/score_evp.py \
  --evp "For Series-B SaaS in a pipeline gap, we ship 14+ SQLs per month without hiring 2 more SDRs." \
  --tier 3 --icp "Series-B SaaS"
python3 scripts/score_evp.py --evp "We help companies improve their growth and optimize outcomes." --tier 3
```

Three tier lines from the sample PSP. Then yours.

## What this pack will not do

It will not pick this quarter's PSP.
It will not invent proof you did not hand it.
It will not write five ads from a blank page.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Why 22 words?

Long enough for ICP, pain, outcome, and one tradeoff.
Short enough to sit in a cold-email third line.
If it does not fit, you have two claims. Cut one.

## Which Schwartz tier should I write first?

Tiers 2–4.
That is where B2B buyers live.
Tier 5 is a direct ask — your internal product view. Unaware (Tier 1) is a pain reveal, not a product sentence.

## Do I need Operator Pass to use this?

No. The pack, the scorer, and the sample are MIT. Pass is compounding: the catalog, the calibrated tools, the Friday room.

## Suite, course, Operator Pass

- Suite: [gtm-operator-skills](https://github.com/cmj-hub/gtm-operator-skills) · [jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [EVP Generator](https://jaymountconsulting.com/learn/courses/evp-generator)
- Operator Pass: [jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — five-part buying brief
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — signal, pain, EVP, binary ask
- [claude-founder-brand](https://github.com/cmj-hub/claude-founder-brand) — Pillar / Proof / Process / Person
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — three-tier contrast + pocket-price leaks

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
