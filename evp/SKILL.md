---
name: evp
description: >
  Existential Value Proposition (EVP) generator for B2B operators. Uses the
  Eugene Schwartz awareness model (unaware, problem-aware, solution-aware,
  product-aware, most-aware) to produce a sharp, 22-word EVP for each
  awareness tier — plus a structured 3-tier EVP brief documenting the
  audience, pain, EVP, and proof per tier. EVPs follow the JMC shape:
  "For <ICP> in <pain> we're the <one team> that does <specific outcome>
  without <obvious tradeoff>." Loaded for cold email openers, hero copy,
  pricing pages, and sales-call openings. Triggers on: "write an EVP",
  "value proposition", "elevator pitch", "positioning statement", "hero
  copy", "EVP brief", "what's our angle", "messaging by awareness level".
allowed-tools:
  - Read
  - Write
  - Grep
---

# EVP — Existential Value Proposition Generator

A Claude Code skill that generates **Existential Value Propositions**
(EVPs) — the one sentence that answers: *"For <ICP> in <pain>, we're
the <one team> that does <specific outcome> without <obvious
tradeoff>."*

Uses the Eugene Schwartz awareness model to produce a different EVP
for each tier of your audience — because the line that lands on a
solution-aware prospect won't land on someone unaware they have the
problem.

## Quick reference

| Slash | What it does |
|---|---|
| `/evp` | Interactive — build an EVP for a specific awareness tier |
| `/evp craft <tier>` | Generate 3 EVP variants for one awareness tier |
| `/evp brief` | Build a structured 3-tier brief (Schwartz tiers 2/3/4) |

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
| 5 | Most aware | Ready to buy from someone | "Operator Pass — <specific price + specific outcome>." (Direct ask) |

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

For each variant, validate:

- [ ] ≤22 words
- [ ] One specific outcome (no abstract verbs)
- [ ] One specific tradeoff (no "and more")
- [ ] ICP named explicitly
- [ ] Pain matches the PSP's vocabulary
- [ ] Variant fits the awareness tier (not a Tier-5 line for a Tier-2 reader)

### 4. Offer the brief mode

After delivering single-tier EVPs, offer:

> "Want a 3-tier brief — Tier 2 / Tier 3 / Tier 4 EVPs side-by-side
> with proof per tier?"

## Sub-skills

- [`skills/evp-craft`](../skills/evp-craft) — single-tier EVP generation
- [`skills/evp-brief`](../skills/evp-brief) — structured 3-tier brief

## Plugs into

- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — EVP is line 3 of every cold email
- **[claude-psp](https://github.com/cmj-hub/claude-psp)** — PSP is the pain layer underneath every EVP
- **JMC EVP Generator course** — the deep methodology

## Full course

This skill is the agent-form of the JMC **EVP** course in The
Compounding Engine. The course covers:

- The Schwartz 5-tier awareness model in B2B
- ICP-pain-EVP alignment patterns
- Tier-jumping (when prospects move 1→3 in one campaign)
- A/B testing EVPs across surfaces
- The "EVP brief" as a single source of truth for the company

→ **[jaymountconsulting.com/learn/courses/evp-generator](https://jaymountconsulting.com/learn/courses/evp-generator)**
