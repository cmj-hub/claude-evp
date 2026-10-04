# Status — where you are and what's next

State-aware router for EVP work.

## Activation

Runs on a bare `/evp:evp` or `/evp:evp status`, or:
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
    # psp is what the psp pack publishes; psp_drafts.primary is the fallback.
    "has_psp":            brand_config.psp.primary_pain != "" or brand_config.psp_drafts.primary.pain != "",
    "primary_tier_set":   primary in [1, 2, 3, 4, 5],
    "locked":             {t: brand_config.evp_drafts[k].primary != "" for t, k in TIER_KEYS.items()},
    "evp_published":      brand_config.evp.primary != "",  # the block cold-email, landing-page, sales-offer read
    "has_proofs":         len(soul.proofs_reservoir) >= 3,
    "has_competitors":    len(brand_config.competitors) > 0,
    "brief_built":        file_exists("gtm/evp-brief.md") or glob("evp-brief-*.md") != [],  # old name before 0.7
    "brief_stale":        brief_age_days > brand_config.refresh_cadence_days,  # default 90
}
```

Evaluate top to bottom; the first matching row wins.

| State | Route to |
|---|---|
| `!has_brand_config OR !has_soul` | [setup](setup.md) mode |
| `!has_psp` | "No PSP in brand-config.json. Install `/plugin install psp@gtm-operator-skills`, run `/psp:psp`. EVPs without a PSP are guesses." |
| `!primary_tier_set` | "Pick your primary outreach tier (most common is Tier 3)" |
| primary tier not locked | [craft](craft.md) mode for the primary tier |
| `!evp_published` | craft mode Step 7 — publish the primary-tier line as the `evp` block |
| `!has_proofs` | "Mine 3 proofs into SOUL.md before publishing the EVP" |
| `!locked[2]` | craft mode for Tier 2 (reframe) |
| `!has_competitors` | "Name 2-3 competitors + the axis you beat each on" (Step 6 of the setup mode) |
| `!locked[4]` | craft mode for Tier 4 (vendor delta) |
| `!locked[3]` | craft mode for Tier 3 (category split) |
| `!brief_built` | [brief](brief.md) mode (build the 3-tier brief) |
| `brief_stale` | brief mode — "Your brief is past its refresh date. Re-score and rebuild." |
| otherwise | "EVPs operational. Re-run every 90 days. Plug into `/cold-email:cold-email` next." |

Before routing, report what you detected in one line per item (✓ / ⬜),
so the operator sees why they landed where they did. End with one
`Next:` line: the mode or command for the first unmet row, or
`Next: /cold-email:cold-email` once everything is done. `/gtm:next`
(hub plugin) names the next pack across the whole suite.

## Welcome flow

```
> /evp:evp

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

- [setup.md](setup.md)
- [craft.md](craft.md)
- [brief.md](brief.md)
