# Brief — three tiers side by side

Produces a structured 3-tier EVP brief covering the three tiers where
most B2B buyers live: Tier 2 (problem-aware), Tier 3 (solution-aware),
Tier 4 (product-aware).

## Contents

- Activation
- Workflow
- References

## Activation

`/evp:evp brief`, or:
- "Build an EVP brief"
- "3-tier brief"
- "EVP across awareness levels"

## Workflow

### 1. Confirm the ICP scope

The brief is per-ICP. If the user has multiple ICPs, ask: "Which ICP
are we building this brief for? (Run again per segment.)"

### 2. Capture inputs once

| Input | Source |
|---|---|
| `icp` | `brand-config.icp.segment` |
| `psp` | `brand-config.psp`; fallback `brand-config.psp_drafts.primary`. Neither → stop and point to `/psp:psp` (`/plugin install psp@gtm-operator-skills`) |
| `outcome` | `SOUL.md` → Outcomes I will claim |
| `tradeoff` | `SOUL.md` → Tradeoffs I name |
| `competitors` | `brand-config.competitors` — required for Tier 4 |
| `proof_per_tier` | `SOUL.md` → Proofs in my reservoir |
| existing drafts | `brand-config.evp_drafts.tier_{2,3,4}_*` — start from these, don't discard them |

Missing `brand-config.json` or `SOUL.md` → stop and run the
[setup](setup.md) mode. No competitors → write Tiers 2 and 3, and mark
Tier 4 "blocked: name 2-3 competitors in brand-config first".

### 3. Generate the brief

For each of Tier 2, Tier 3, Tier 4:

- Audience description (what they know, what they don't)
- Tier-appropriate pain framing
- 1 primary EVP (best variant) + 1 alternate
- Proof aligned to that tier (different proofs land at different tiers),
  quoted from the reservoir — if none fits, say so; never invent one
- Where to deploy this EVP (which surfaces)

Score every primary and alternate with
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py --evp "<line>" --tier <N> --icp "<icp>"`
(plain-skills install: `scripts/score_evp.py`). Nothing under 70 goes
in the brief.

### 4. Output

Write the brief to `gtm/evp-brief.md` in the operator's project
(create `gtm/` if it is missing; ask before overwriting an existing
one), then offer to copy each tier's
primary line back into `brand-config.evp_drafts`. Merge at the field
level: write only `evp_drafts` (and `evp`, per [craft](craft.md) Step 7, if
the operator picks the primary-tier line as the outreach line), leave
every other key as it was, and ask before changing a filled field.

```markdown
# EVP Brief — <ICP>

**PSP anchor:** <pain in their vocabulary, one sentence>

---

## Tier 2 — Problem-aware

**Audience knows:** the pain exists; doesn't know solutions exist (or
doesn't think any are worth evaluating yet).

**Best framing:** Pain reveal + reframe.

### Primary EVP
"<22-word line>"

### Alternate
"<22-word line>"

### Proof for this tier
<Demonstration of the pain at scale — e.g., "62% of Series-B SaaS hit
this within 18 months of funding.">

### Deploy on
- Hero copy on landing pages
- Top-of-funnel ad creative
- Cold email line 3 (when targeting based on signal that implies awareness)
- Podcast-appearance pitch lines

---

## Tier 3 — Solution-aware

**Audience knows:** solutions exist; comparing categories of approach
(in-house vs agency vs DIY vs tool).

**Best framing:** Category split — why your category beats the
traditional one.

### Primary EVP
"<22-word line>"

### Alternate
"<22-word line>"

### Proof for this tier
<Comparison: outcome metric of your category vs traditional approach —
e.g., "Targeted outbound: $640 CPM. Generic agency: $2,800 CPM.">

### Deploy on
- Comparison pages
- Mid-funnel ads
- Cold email line 3 (when targeting based on category-discontent signal)
- Sales call opener (when prospect has tried alternatives)

---

## Tier 4 — Product-aware

**Audience knows:** specific vendors exist; comparing options head to head.

**Best framing:** Vendor delta — your specific advantage on a specific
axis vs named competitor.

### Primary EVP
"<22-word line — references competitor>"

### Alternate
"<22-word line — references competitor>"

### Proof for this tier
<Specific competitor delta — e.g., "Versus <competitor>, we ship the
<feature> in <timeframe> instead of <their timeframe>.">

### Deploy on
- Pricing page hero
- Sales-call objection handling
- Battlecards
- Bottom-funnel ads

---

## The single source of truth

This brief is the authoritative messaging document for <ICP>. When
hero copy, ad creative, cold email, or pricing-page lines need to be
written or rewritten, pull from the tier that matches the audience's
actual awareness level.

Re-run this brief every 90 days. EVPs decay as the market catches up
and competitor positioning shifts.
```

## References

- The framework: the main `evp` skill
- [craft.md](craft.md) for single-tier generation
- [Early Value Propositions course](https://jaymountconsulting.com/learn/courses/early-value-propositions) — the human build guide
