---
name: evp-kickoff
description: Adaptive router for the EVP skill pack. Detects state (brand-config? SOUL? primary EVP locked per tier? competitors named? proofs reservoir?) and picks the next-best step. Loaded by the main evp skill on bare invocation.
user-invocable: false
allowed-tools: Read Grep
license: MIT

---

# EVP Kickoff — adaptive router

State-aware router for EVP work.

## Activation

Loaded by `evp` on bare invocation, or:
- "Where do I start with EVPs"
- "What's next for our positioning"

## State detection

```python
TIER_KEYS = {2: "tier_2_problem_aware", 3: "tier_3_solution_aware", 4: "tier_4_product_aware"}
primary = brand_config.primary_outreach_tier
state = {
    "has_brand_config":   file_exists("brand-config.json"),
    # The pack ships SOUL.md as a template. Unfilled placeholders = not set up.
    "has_soul":           file_exists("SOUL.md") and "<e.g." not in soul_text,
    "has_psp":            brand_config.psp.primary_pain != "",
    "primary_tier_set":   primary in [1, 2, 3, 4, 5],
    "locked":             {t: brand_config.evp_drafts[k].primary != "" for t, k in TIER_KEYS.items()},
    "has_proofs":         len(soul.proofs_reservoir) >= 3,
    "has_competitors":    len(brand_config.competitors) > 0,
    "brief_built":        glob("evp-brief-*.md") != [],
    "brief_stale":        brief_age_days > brand_config.refresh_cadence_days,  # default 90
}
```

Evaluate top to bottom; the first matching row wins.

| State | Route to |
|---|---|
| `!has_brand_config OR !has_soul` | `evp-onboarding` |
| `!has_psp` | "Install cmj-hub/claude-psp first — EVPs without a PSP are guesses" |
| `!primary_tier_set` | "Pick your primary outreach tier (most common is Tier 3)" |
| primary tier not locked | `evp-craft` for the primary tier |
| `!has_proofs` | "Mine 3 proofs into SOUL.md before publishing the EVP" |
| `!locked[2]` | `evp-craft` for Tier 2 (reframe) |
| `!has_competitors` | "Name 2-3 competitors + the axis you beat each on" (Step 6 of `evp-onboarding`) |
| `!locked[4]` | `evp-craft` for Tier 4 (vendor delta) |
| `!locked[3]` | `evp-craft` for Tier 3 (category split) |
| `!brief_built` | `evp-brief` (build the 3-tier brief) |
| `brief_stale` | `evp-brief` — "Your brief is past its refresh date. Re-score and rebuild." |
| otherwise | "EVPs operational. Re-run every 90 days. Plug into claude-cold-email next." |

Before routing, report what you detected in one line per item (✓ / ⬜),
so the operator sees why they landed where they did.

## Welcome flow

```
> /evp

Welcome.

[Detected: brand-config.json missing]
(Example — print the real detected state, not this text.)

You're at step 1 of 5:
1. ⬜ Onboarding — capture tier + outcomes + tradeoffs + proofs   ← YOU ARE HERE
2. ⬜ Lock primary-tier EVP (3 variants generated, pick 1)
3. ⬜ Lock Tier 2 + Tier 4 EVPs for full coverage
4. ⬜ Build 3-tier brief (the canonical messaging doc)
5. ⬜ Re-evaluate every 90 days

Step 1 takes ~10 minutes. Ready? (y/n)
```

## References

- `../evp-onboarding/SKILL.md`
- `../evp-craft/SKILL.md`
- `../evp-brief/SKILL.md`
