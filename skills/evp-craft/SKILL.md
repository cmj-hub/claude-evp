---
name: evp-craft
description: "Generates and scores 3 EVP variants for one Schwartz awareness tier (outcome-led, tradeoff-led, ICP-led), each in the 22-word shape, and critiques a pasted line. Publishes the chosen primary-tier line to brand-config.json as the evp block. Use when the main evp skill routes a request for a line at one tier or a critique of an existing line."
user-invocable: false
allowed-tools: Read Write Grep Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py:*)
license: MIT
models: ""

---

# EVP Craft — sub-skill

Generates 3 EVP variants for a specific awareness tier.

## Activation

Loaded by `evp` on:
- "Write an EVP for <tier>"
- "EVP for solution-aware prospects"
- "Tier 3 EVP"

## Workflow

### 1. Lock the awareness tier

Ask the user which Schwartz tier (1-5). If they don't know, walk them
through the 5-tier table from `../evp/SKILL.md` and ask: "Which
describes your audience right now?"

If the user names no tier, default to
`brand-config.primary_outreach_tier`.

Most B2B buyers are in Tiers 2-4. If the user says "Tier 5," push
back once — that's product-team thinking, not buyer-where-they-are
thinking. If they confirm the reader really is ready to buy, write
the Tier-5 line.

### 2. Capture the inputs

Read these from the project files before asking the user for anything:

| Input | Where it lives |
|---|---|
| `icp` | `brand-config.icp.segment` |
| `psp_pain` | `brand-config.psp.primary_pain` + `psp.vocabulary`; fallback `psp_drafts.primary.pain` + `.vocabulary` |
| `outcome` | `SOUL.md` → Outcomes I will claim |
| `tradeoff` | `SOUL.md` → Tradeoffs I name |
| `proof` | `SOUL.md` → Proofs in my reservoir |
| `competitors` (Tier 4) | `brand-config.competitors` |

If `brand-config.json` or `SOUL.md` is missing, stop and load
`evp-onboarding`. If neither `psp` nor `psp_drafts.primary` exists,
stop: the psp pack produces it (`/psp:psp`; install with
`/plugin install psp@gtm-operator-skills`). Never invent the pain.
EVPs without a PSP are guesses.

If the user asks for an outcome that is not on the will-claim list,
refuse it and show the list. If the outcome is vague ("more pipeline",
"better efficiency"), ask for the number and timeframe instead of
guessing one.

### 3. Generate 3 variants

Each variant uses the shape but with different emphasis:

**Variant A — outcome-led**

> "For <ICP>, in <pain>, we're the <one team> that does <SPECIFIC
> OUTCOME> without <tradeoff>."

The outcome carries the line. Use when the outcome is differentiated
and concrete (e.g., "ships 14 qualified meetings in 30 days").

**Variant B — tradeoff-led**

> "For <ICP>, in <pain>, we're the team that hits <outcome> WITHOUT
> <SPECIFIC TRADEOFF>."

The tradeoff carries the line. Use when the tradeoff is the
elephant-in-the-room reason the audience hesitates (e.g., "without
hiring 2 more SDRs" or "without sacrificing self-serve").

**Variant C — ICP-led**

> "<SPECIFIC ICP> in <pain> use us when they want <outcome> without
> <tradeoff>."

The ICP carries the line. Use when the audience is hyper-niche and
you want immediate exclusion-by-segment (signals fit fast).

### 4. Validate each variant

Score each variant with the deterministic scorer:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py \
  --evp "<variant>" --tier <N> --icp "<icp segment>"
```

(Plain-skills install: `scripts/score_evp.py` from the pack root.)
Exit 1 means under 70 — rewrite before showing it. Then run the
self-check, which covers what the scorer cannot see:

| Check | Pass criterion |
|---|---|
| Word count | ≤22 |
| Outcome specificity | A concrete noun + metric, not a verb like "improve" |
| Tradeoff specificity | A concrete thing they'd otherwise have to give up |
| ICP named | Segment is specific enough to exclude wrong-fit |
| Pain vocabulary | Uses their words from the PSP, not category jargon |
| Tier-appropriate | Matches the awareness tier (no Tier-5 line for a Tier-2 audience) |
| Claim allowed | Outcome is on the SOUL.md will-claim list |
| Proof real | Proof is quoted from the SOUL.md reservoir, or the slot says "none yet" |

### 5. Output

```markdown
# EVP — <ICP> · Tier <N>: <tier name>

**Pain anchor:** <PSP pain in their language>

## Variant A — outcome-led
"<22-word line>" — <score>/100

## Variant B — tradeoff-led
"<22-word line>" — <score>/100

## Variant C — ICP-led
"<22-word line>" — <score>/100

## Recommended primary
<A / B / C> — <one-sentence rationale>

## Where this fits
- Cold email line 3 (works on Tier 2-4 audiences)
- Hero copy (Tier <N> only — calibrate per page)
- Pricing-page tagline (Tier 4)
- Sales call opener (calibrate to where prospect is)

## Proof to back it
<Quoted from the SOUL.md reservoir. If nothing fits this tier, write
"None in reservoir yet — add one before this line ships." Never invent.>
```

### 6. Surgical critique mode

If user pastes an existing EVP for critique, return:

```
Original: "<their EVP>"
Word count: <N>
Score: <scorer total>/100
Tier-fit: <which tier this actually lands on>

Issues:
  - <issue 1>
  - <issue 2>

Rewrite (same voice):
"<rewritten>"
Rationale: <one sentence>
```

### 7. Lock the outreach line

When the operator picks a line, offer to save it to
`brand-config.evp_drafts.<tier key>.primary` (with its `outcome`,
`tradeoff`, `proof`). If that tier is `primary_outreach_tier`, also
publish the `evp` block that cold-email, landing-page, sales-offer and
email-sequence read:

```json
"evp": {
  "tier": 3,
  "primary": "<the chosen line>",
  "outcome": "<outcome from the will-claim list>",
  "tradeoff": "<tradeoff>",
  "proof": "<proof quoted from the reservoir, or empty>"
}
```

`tier` is `primary_outreach_tier` (an integer 1-5). Copy the values
from the draft; do not reword them. Leave `proof` as `""` when the
reservoir has none — never fill it.

`brand-config.json` is shared by every pack in the suite. Merge at the
field level: read the existing file, write only `evp_drafts` and
`evp`, leave every other key exactly as it was, and show the diff and
ask before changing a field that already has a value.

## References

- `../evp/SKILL.md` — the framework
- [Early Value Propositions course](https://jaymountconsulting.com/learn/courses/early-value-propositions) — the human build guide
