---
name: evp
description: "Writes and scores an Early Value Proposition (EVP): one line of 22 words or fewer matched to a Schwartz awareness tier, in the shape \"For {ICP} in {pain}, we're the {one team} that does {outcome} without {tradeoff}.\" Builds a 3-tier brief and publishes the chosen outreach line as the evp block. Use when the operator asks for an EVP, value proposition, positioning or hero line, messaging by awareness level, or a line scored. Not for the pain profile under it (use psp), the cold email (use cold-email), or the landing page (use landing-page)."
argument-hint: "[craft <tier> | brief | score <line> | status | setup]"
allowed-tools: Read Write Grep Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py:*)
license: MIT
models: ""

---

# EVP — Early Value Proposition Generator

A Claude Code skill that generates **Early Value Propositions**
(EVPs) — the one sentence that answers: *"For <ICP> in <pain>, we're
the <one team> that does <specific outcome> without <obvious
tradeoff>."*

Uses the Eugene Schwartz awareness model to produce a different EVP
for each tier of your audience — because the line that lands on a
solution-aware prospect won't land on someone unaware they have the
problem.

## Before you write anything (non-negotiable)

These are the rules in `AGENTS.md`, restated here because a plugin does
not load that file on its own.

1. **Load `brand-config.json` and [SOUL.md](../../SOUL.md) from the
   project root.** Both are shared by every pack in the suite. If
   either is missing, or `SOUL.md` still holds template placeholders
   (`<e.g. ...>`, `<...>`), stop and run the `setup` mode. Do not
   draft a "generic" EVP in the meantime.
2. **Claim only outcomes on the operator's will-claim list** in `SOUL.md`.
   Anything outside it gets refused, with the list shown back.
3. **Cite proof only from the reservoir** in `SOUL.md`. If no proof fits
   the tier, say so and leave the slot empty. Never invent a case study,
   metric, or percentage.
4. **≤22 words.** Hard limit, not a target.
5. **Tier-fit.** Write to the tier the user asked for, else
   `brand-config.primary_outreach_tier`. Never a Tier-5 line for a
   Tier-2 reader.
6. **Schwartz tiers only.** Unaware / problem-aware / solution-aware /
   product-aware / most-aware. Do not translate into TOFU/MOFU/BOFU.
7. **Banned stand-ins:** improve, optimize, enhance, drive growth,
   predictable, scalable, best-in-class. Replace with a number and a
   timeframe from the will-claim list.

## Routing

Route by `$ARGUMENTS`. If it names a mode, go straight to it. If it is
empty, run `status`. Otherwise match the request to a row. Read the
mode file with the Read tool and follow it. Config or SOUL missing →
`setup` first, whatever was asked.

| You say / argument | Mode file |
|---|---|
| (nothing), `status`, "where do I start", "what's next" | [modes/status.md](modes/status.md) |
| `setup`, `onboarding`, "set up EVP" | [modes/setup.md](modes/setup.md) |
| `craft <tier>`, "Tier 3 EVP", "critique this EVP" | [modes/craft.md](modes/craft.md) |
| `brief`, "3-tier brief" | [modes/brief.md](modes/brief.md) |
| `score "<line>" [tier]` | no file: run the scorer (below) and report |

Arguments passed to the skill: `$ARGUMENTS`

The command is `/evp:evp <mode>`, e.g. `/evp:evp craft 3`. Moved in
0.7: the old sub-skills (`evp-kickoff`, `evp-onboarding`, `evp-craft`,
`evp-brief`) are these modes.

Files this pack writes in the operator's project: `brand-config.json`
and `SOUL.md` at the root (shared), and the brief at `gtm/evp-brief.md`.
Create `gtm/` if it is missing.

## The framework

### The EVP shape

```
For <ICP segment>, in <PSP pain>,
we're the <one team> that does <specific outcome>
without <obvious tradeoff>.
```

**Rules:**

- ≤22 words total
- One specific outcome (no "improve" / "optimize" / "enhance")
- One specific tradeoff (no "and more" / etc.)
- The ICP segment named explicitly
- The pain anchored on a real PSP, not a guess

### The 5 awareness tiers (Schwartz)

The same product needs different EVPs depending on what the prospect
already knows:

| # | Tier | Knows | EVP shape |
|---|---|---|---|
| 1 | Unaware | Doesn't know they have the pain | "If your <metric> is <X>, you're losing <consequence>." (Pain reveal) |
| 2 | Problem-aware | Knows the pain, doesn't know solutions exist | "<Pain> isn't a <traditional approach> problem — here's why." (Reframe) |
| 3 | Solution-aware | Knows solutions exist, comparing categories | "Most teams pick <traditional> for <pain>. We do <specific outcome> instead." (Category split) |
| 4 | Product-aware | Comparing specific vendors | "Versus <competitor>: we ship <specific advantage> on <specific axis>." (Vendor delta) |
| 5 | Most aware | Ready to buy from someone | "<product name> — <specific terms + specific outcome>." (Direct ask) |

Most B2B buyers live in Tiers 2-4. Most operators write EVPs for Tier
5 (their internal product team's view) and wonder why nothing lands.

### Where EVPs go

- **Cold email** — the 3rd line of every signal-anchored opener
- **Hero copy** — usually a Tier 2 or Tier 3 EVP
- **Pricing page** — Tier 4 (versus competitors)
- **Sales call opener** — calibrated to where the prospect is on the tier ladder
- **Ad creative** — usually Tier 1 or Tier 2 (problem reveal)

## Score a line

Score every line before showing it:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py \
  --evp "<line>" --tier <N> --icp "<icp segment>"
```

If `${CLAUDE_PLUGIN_ROOT}` is not expanded (the pack was installed as
plain skills, not as a plugin), use `scripts/score_evp.py` from the pack
root. Exit 0 = score ≥70. Exit 1 prints each reason as
`- what is wrong → what to change`; rewrite and score again. Add
`--json` for one JSON object. The scorer is a floor, not the judge: it
cannot tell whether a claim is on the will-claim list, so the
[craft](modes/craft.md) self-check still applies.

**One proposition.** Score each line on its own. A draft that holds a
list (two or more `value_props`, `headlines`, `options`, `pillars`,
`benefits` or `messages`, or two or more bullet lines in a text file)
exits 1 with `Refusal: a list of value props is not one proposition`.
A line that scores 70+ prints under `# Proposition` (`proposition` in
`--json`); that one line is what ships.

If neither `psp` nor `psp_drafts.primary` is in `brand-config.json`,
stop: the psp pack produces it. Point the user to `/psp:psp` (install
with `/plugin install psp@gtm-operator-skills`). Do not invent the
pain or the vocabulary. EVPs without a PSP are guesses.

## Finish every run with the next step

When a line passes and the operator locks it as the `evp` block, end
with one line: `Next: /cold-email:cold-email` for the first touch (or
`/landing-page:page` for the hero, `/sales-offer:cold-offer` for a
give-first offer). If the pack is not installed, give its install line
(`/plugin install cold-email@gtm-operator-skills`).

## Works with the suite

This is step 2 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `psp` (fallback `psp_drafts.primary`), `icp`, `competitors`, `primary_outreach_tier` from `brand-config.json` if present.
- **Writes:** `evp_drafts`, `competitors`, `primary_outreach_tier`, and the chosen outreach line as the `evp` block (`tier`, `primary`, `outcome`, `tradeoff`, `proof`). Merge at the field level; never overwrite another pack's keys.
- **Before this:** psp (`/psp:psp`), when `brand-config.json` has no `psp` block; `/gtm:setup` once, when `operator` or `icp` is empty.
- **After this:** cold-email (`/cold-email:cold-email`) for the first touch, landing-page (`/landing-page:page`) for the hero, sales-offer (`/sales-offer:cold-offer`) for a give-first offer.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.

Human build guide: [Early Value Propositions course](https://jaymountconsulting.com/learn/courses/early-value-propositions).

## Free hosted version

The same job runs in a browser, no install and no key:
[EVP Generator](https://jaymountconsulting.com/tools/evp-generator)
