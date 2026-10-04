---
name: evp
description: >
  Early Value Proposition (EVP) generator for B2B operators. Uses the
  Eugene Schwartz awareness model (unaware, problem-aware, solution-aware,
  product-aware, most-aware) to produce a sharp, 22-word EVP for each
  awareness tier — plus a structured 3-tier EVP brief documenting the
  audience, pain, EVP, and proof per tier. EVPs follow the JMC shape:
  "For <ICP> in <pain> we're the <one team> that does <specific outcome>
  without <obvious tradeoff>." Loaded for cold email openers, hero copy,
  pricing pages, and sales-call openings. Triggers on: "write an EVP",
  "value proposition", "elevator pitch", "positioning statement", "hero
  copy", "EVP brief", "what's our angle", "messaging by awareness level".
argument-hint: "[craft <tier> | brief | score <line>]"
allowed-tools: Read Write Grep
license: MIT

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

1. **Load `brand-config.json` and `SOUL.md` from the project root.** If
   either is missing, or `SOUL.md` still holds template placeholders
   (`<e.g. ...>`, `<...>`), stop and route to `evp-onboarding`. Do not
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

| User says | Load |
|---|---|
| `/evp` with no arguments, "where do I start" | `evp-kickoff` |
| config or SOUL missing, "set up EVP" | `evp-onboarding` |
| `/evp craft <tier>`, "Tier 3 EVP", "critique this EVP" | `evp-craft` |
| `/evp brief`, "3-tier brief" | `evp-brief` |
| `/evp score "<line>"` | Run the scorer (below) and report |

Arguments passed to the skill: `$ARGUMENTS`

## Quick reference

| Slash | What it does |
|---|---|
| `/evp` | Interactive — build an EVP for a specific awareness tier |
| `/evp craft <tier>` | Generate 3 EVP variants for one awareness tier |
| `/evp brief` | Build a structured 3-tier brief (Schwartz tiers 2/3/4) |
| `/evp score "<line>" [tier]` | Score an existing line 0-100 with the deterministic scorer |

In a plugin install the command is namespaced: `/evp:evp craft 3`.

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

## Workflow

### 1. Capture the inputs

| Input | Source |
|---|---|
| `icp` | ICP segment (specific, not "B2B SaaS") |
| `psp` | PSP pain (load from `claude-psp` if available) |
| `outcome` | The specific result you deliver |
| `tradeoff` | The obvious tradeoff you spare them |
| `awareness_tier` | Which Schwartz tier (1-5) we're writing for |
| `proof` | (Optional) Case study / metric / social proof for the tier |

If `psp` is missing, push the user to build one first via
`claude-psp` — EVPs without a PSP are guesses.

### 2. Generate 3 EVP variants for the tier

Each variant uses the shape but explores a different emphasis:

- **Variant A** — emphasis on the outcome
- **Variant B** — emphasis on the tradeoff
- **Variant C** — emphasis on the ICP segment

Validate each against the 22-word constraint.

### 3. Self-check

Score every variant with the deterministic scorer before showing it:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py" \
  --evp "<variant>" --tier <N> --icp "<icp segment>"
```

If `${CLAUDE_PLUGIN_ROOT}` is not expanded (the pack was installed as
plain skills, not as a plugin), use `scripts/score_evp.py` from the pack
root. Exit 0 = score ≥70. Rewrite any variant that exits 1 and show the
score next to each line you deliver. The scorer is a floor, not the
judge: it cannot tell whether a claim is on the will-claim list, so the
checklist below still applies.

For each variant, validate:

- [ ] ≤22 words
- [ ] One specific outcome (no abstract verbs)
- [ ] One specific tradeoff (no "and more")
- [ ] ICP named explicitly
- [ ] Pain matches the PSP's vocabulary
- [ ] Variant fits the awareness tier (not a Tier-5 line for a Tier-2 reader)
- [ ] Outcome is on the SOUL.md will-claim list
- [ ] Proof, if cited, is quoted from the SOUL.md reservoir

### 4. Offer the brief mode

After delivering single-tier EVPs, offer:

> "Want a 3-tier brief — Tier 2 / Tier 3 / Tier 4 EVPs side-by-side
> with proof per tier?"

## Sub-skills

- [`evp-kickoff`](../evp-kickoff/SKILL.md) — state router for bare `/evp`
- [`evp-onboarding`](../evp-onboarding/SKILL.md) — first-run brand-config + SOUL setup
- [`evp-craft`](../evp-craft/SKILL.md) — single-tier EVP generation and critique
- [`evp-brief`](../evp-brief/SKILL.md) — structured 3-tier brief

## Plugs into

- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — EVP is line 3 of every cold email
- **[claude-psp](https://github.com/cmj-hub/claude-psp)** — PSP is the pain layer underneath every EVP
- **[Early Value Propositions course](https://jaymountconsulting.com/learn/courses/early-value-propositions)** — the human build guide

## Free hosted version

The same job runs in a browser, no install and no key:
[EVP Generator](https://jaymountconsulting.com/tools/evp-generator)
