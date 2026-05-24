# claude-evp

A Claude Code skill that generates **Existential Value Propositions**
— the one sentence that says: *"For <ICP> in <pain>, we're the <one
team> that does <specific outcome> without <obvious tradeoff>."*

Uses the **Eugene Schwartz 5-tier awareness model** so you get a
different EVP for each tier of your audience — because the line that
lands on a solution-aware prospect won't land on someone unaware they
have the problem.

Based on the **[EVP course](https://jaymountconsulting.com/learn/courses/evp-generator)**
in The Compounding Engine.

## What it does

Generate sharp, 22-word EVPs for any awareness tier (most B2B buyers
live in Tiers 2-4):

| Tier | They know | EVP shape |
|---|---|---|
| 1 — Unaware | Doesn't know they have the pain | Pain reveal |
| 2 — Problem-aware | Pain exists; no solutions known | Pain + reframe |
| 3 — Solution-aware | Solutions exist; comparing categories | Category split |
| 4 — Product-aware | Comparing vendors | Vendor delta |
| 5 — Most aware | Ready to buy from someone | Direct ask |

Plus a structured 3-tier brief (Tier 2 / 3 / 4 side-by-side with
audience, pain, EVP, and proof per tier) — the single source of truth
your hero, ads, cold email, and pricing pages pull from.

## Sub-skills

| Sub-skill | Job |
|---|---|
| `evp-craft` | Generate 3 EVP variants for one awareness tier (outcome-led / tradeoff-led / ICP-led) |
| `evp-brief` | Build the structured 3-tier brief (Tier 2 / 3 / 4 side-by-side) |

## Install

### Claude Code

```bash
/plugin marketplace add cmj-hub/claude-evp
/plugin install evp
```

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-evp/main/install.sh | bash
```

## Usage

```
> Write an EVP for Series-B SaaS in the pipeline-gap pain, Tier 3 (solution-aware)
```

Claude returns 3 EVP variants (outcome-led, tradeoff-led, ICP-led) —
all ≤22 words, all using the prospect's vocabulary, all matched to
the awareness tier.

Or:

```
> Build me an EVP brief for our Series-B SaaS ICP
```

Claude generates the full Tier 2 / 3 / 4 brief with proof per tier and
deployment notes per surface.

## EVP shape

```
For <ICP segment>,
in <PSP pain>,
we're the <one team> that does <specific outcome>
without <obvious tradeoff>.
```

**Rules:**

- ≤22 words total
- One specific outcome (no "improve" / "optimize")
- One specific tradeoff (no "and more")
- ICP segment named explicitly
- Pain in their vocabulary, not yours

## Where EVPs go

- **Cold email** — line 3 of every signal-anchored opener (see [claude-cold-email](https://github.com/cmj-hub/claude-cold-email))
- **Hero copy** — usually a Tier 2 or Tier 3 EVP
- **Pricing page** — Tier 4 (versus competitors)
- **Sales call opener** — calibrated to where the prospect is on the tier ladder
- **Ad creative** — usually Tier 1 or Tier 2 (problem reveal)

## Plugs into

- **[claude-psp](https://github.com/cmj-hub/claude-psp)** — PSP is the pain layer underneath every EVP
- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — EVP is line 3 of every cold email

## Course

This skill is the agent-form of the **EVP** course. The full course
covers Schwartz tiers in B2B, ICP-pain-EVP alignment patterns,
tier-jumping campaigns, A/B testing EVPs across surfaces, and using
the EVP brief as a single source of truth.

→ [jaymountconsulting.com/learn/courses/evp-generator](https://jaymountconsulting.com/learn/courses/evp-generator)

Want it all-access? **[Operator Pass](https://jaymountconsulting.com/operator-pass)**.

## License

MIT. Built by [Jay Mount Consulting](https://jaymountconsulting.com).
