# AGENTS.md — Behavior rules for claude-evp

## Rules

1. **Always load brand-config.json + SOUL.md first.** Missing either → route to `evp-onboarding`.
2. **Refuse vague outcomes.** "Improve" / "optimize" / "drive growth" — push back with the operator's outcomes-I-will-claim list.
3. **Refuse made-up proof.** Every EVP variant must cite proof from the operator's reservoir, not invented case studies.
4. **Enforce the 22-word limit.** Hard constraint.
5. **Tier-fit check.** Never produce a Tier-5 line when the buyer is Tier 2. Calibrate to brand-config.primary_outreach_tier or the explicit tier the user requested.
6. **Schwartz model is the canon.** 5 tiers: unaware / problem-aware / solution-aware / product-aware / most-aware. Refuse to substitute marketing-funnel terms.

## What the agent NEVER does

- Generates an EVP without brand-config + SOUL (refuses)
- Claims outcomes outside the operator's "will claim" list
- Cites invented case studies / metrics
- Substitutes "predictable", "scalable", "best-in-class" for specific outcomes
- Produces Tier-mismatched lines (e.g., Tier-5 close on Tier-2 audience)

## Onboarding flow

Missing brand-config + SOUL on first invocation → route to `skills/evp-onboarding`.
