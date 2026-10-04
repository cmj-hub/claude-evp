<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Value proposition skill for Claude Code. A value proposition is one line that says why this buyer should care.">
</p>

# Value proposition skill for Claude Code

A value proposition is one line that says why this buyer should care. The same product needs a different line for each buyer.

## In 60 seconds

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install evp@gtm-operator-skills
/evp:evp
```

Or score the sample without an agent:

```bash
python3 scripts/score_evp.py --file examples/t3.good.txt --tier 3 --icp "Series-B SaaS"   # exit 0, prints 100/100, the proposition and "Next: /cold-email:cold-email"
python3 scripts/score_evp.py --file examples/t3.bad.txt --tier 3                          # exit 1: - score 59/100 is under 70 → work through the axis lines below, lowest axis first
```

Part of the GTM operator suite — `/plugin install gtm@gtm-operator-skills` installs all ten.

> Same product. Five readers. Twenty-two words each. Because they are not standing in the same place.

An early value proposition is a line of 22 words or fewer, matched to an awareness tier. Same product, five lines, because the unaware buyer and the vendor-comparing buyer are not the same reader.

You have been writing one line — the line *you* would buy. That is a Most-Aware line. Most of the people who land on your page are not there. They are still naming the pain, or comparing categories, or lining you up against a vendor they already know.

Five stages name where the buyer is standing: unaware, problem-aware, solution-aware, product-aware, most-aware. One product. Five openings. The scorer in this repo checks length, outcome, tradeoff, ICP, and tier-fit.

A specific Tier-3 line scored **100**. "We help companies improve their growth and optimize outcomes" scored **59**. The Python is in `scripts/score_evp.py`. No LLM. No paid API.

The build guide teaches a human. The pack teaches an agent.

<p align="center">
  <img src="./assets/demo.gif" alt="Value proposition skill — Tier-3 line 100, vague line 59" width="100%">
</p>

## What this replaces

A $10K–15K positioning sprint's first output: one hero line, written from inside the building.

## Install

```bash
npx skills add cmj-hub/claude-evp --all -g --full-depth
```

`--all` writes this pack for every host the installer knows. One host:

```bash
npx skills add cmj-hub/claude-evp --skill '*' -g --full-depth -y -a claude-code
```

Swap `claude-code` for `cursor`, `codex`, `grok`, `github-copilot`, `windsurf`, `cline`, or `opencode`.

Claude Code: see [In 60 seconds](#in-60-seconds).

## What is in the pack

One skill, `evp`, with modes. It enforces the rules, routes to the mode, and scores every line.

| Mode | You type | What it does |
|---|---|---|
| `status` | `/evp:evp` (no args) | Reads your files, shows what is done, and picks the next step. |
| `setup` | `/evp:evp setup` | 10-minute setup: writes `brand-config.json` + `SOUL.md` (outcomes you will claim, proofs, competitors, voice). Shared operator/ICP questions come from `/gtm:setup` once for the suite. |
| `craft` | `/evp:evp craft <tier>` | Three variants for one tier (outcome-, tradeoff-, ICP-led), each scored. Also critiques a pasted line. |
| `brief` | `/evp:evp brief` | Tier 2 / 3 / 4 side by side with proof and where to deploy each. Writes `gtm/evp-brief.md`. |
| `score` | `/evp:evp score "<line>" 3` | Runs `scripts/score_evp.py` on one line. |

Moved in 0.7: `/evp:evp-onboarding` is now `/evp:evp setup`. The sub-skills `evp-kickoff`, `evp-craft` and `evp-brief` are the `status`, `craft` and `brief` modes.

The skill will not write a line until `brand-config.json` and `SOUL.md` exist in your project. It claims only outcomes on your will-claim list and cites only proofs from your reservoir. The rules are in [`AGENTS.md`](./AGENTS.md).

## What you walk out with in 15 minutes

Artifact: `examples/t3.good.txt`.

```bash
python3 scripts/score_evp.py --file examples/t3.good.txt --tier 3 --icp "Series-B SaaS"   # 100, exit 0
python3 scripts/score_evp.py --file examples/t3.bad.txt --tier 3                          # 59, exit 1
python3 scripts/score_evp.py --evp "<your line>" --tier 3 --json
python3 scripts/score_evp.py --file examples/value-props.json                             # refused, exit 1
```

A passing line prints under `# Proposition`. A list of value props is refused: `a list of value props is not one proposition`. Every exit-1 reason prints as `- what is wrong → what to change`; `--json` adds `reasons`, `fixes` and `next`.

Three tier lines from the sample Pain Signal Profile. Then yours.

Exit codes: `0` = 70 or above, `1` = rewrite (or a list instead of one line), `2` = bad input. Run `bash scripts/smoke-test.sh` to check the pack itself.

## What this pack will not do

This pack drafts and scores. It will not pick this quarter's PSP, invent proof you did not hand it, write five ads from a blank page, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## Why 22 words?

Long enough for ICP, pain, one outcome, and one tradeoff. Short enough to sit in a cold-email third line or a hero. If it does not fit, you have two claims. Cut one.

## Which tier should I write first?

Tiers 2–4. That is where B2B buyers live. Tier 5 is a direct ask — your internal product view. Unaware (Tier 1) is a pain reveal, not a product sentence.

## Do I need Operator Pass to use this?

No, and there is no key to enter. The pack, the scorer, and the sample are MIT. If you would rather not install anything, the [EVP Generator](https://jaymountconsulting.com/tools/evp-generator) writes the same line in your browser.

## On the site

- [Early Value Propositions pack](https://jaymountconsulting.com/skills/claude-evp) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack
- [Course twin](https://jaymountconsulting.com/learn/courses/early-value-propositions) — human build guide for this pack

## Free, no signup

- **[EVP Generator](https://jaymountconsulting.com/tools/evp-generator)** — the same job as this pack, hosted. No account, no key.
- [Early Value Propositions framework](https://jaymountconsulting.com/frameworks/early-value-propositions)
- [EVP Brief Generator](https://jaymountconsulting.com/tools/evp-brief-generator)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.


## Next

Previous: [Ideal customer profile](https://github.com/cmj-hub/claude-psp)

Next: [Pricing strategy](https://github.com/cmj-hub/claude-pricing)

## Privacy and security

The scorer is stdlib Python and runs locally. No script opens a network connection, and no skill fetches pages. The pack writes `brand-config.json` and `SOUL.md` in your project root and `gtm/evp-brief.md`, and nothing else. No telemetry, no credentials, nothing sent or posted. See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
