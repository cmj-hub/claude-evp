# AGENTS.md — Behavior rules for claude-evp

## Rules

1. **Always load brand-config.json + SOUL.md first.** Missing either → run the `setup` mode (`skills/evp/modes/setup.md`).
2. **Refuse vague outcomes.** "Improve" / "optimize" / "drive growth" — push back with the operator's outcomes-I-will-claim list.
3. **Refuse made-up proof.** Every EVP variant must cite proof from the operator's reservoir, not invented case studies.
4. **Enforce the 22-word limit.** Hard constraint.
5. **Tier-fit check.** Never produce a Tier-5 line when the buyer is Tier 2. Calibrate to brand-config.primary_outreach_tier or the explicit tier the user requested.
6. **Schwartz model is the canon.** 5 tiers: unaware / problem-aware / solution-aware / product-aware / most-aware. Refuse to substitute marketing-funnel terms.
7. **Read the PSP, never invent it.** Pain and vocabulary come from `brand-config.psp` (published by the psp pack), falling back to `psp_drafts.primary`. Neither → name the psp pack and its install line (`/plugin install psp@gtm-operator-skills`, then `/psp:psp`).
8. **Merge, never overwrite.** `brand-config.json` and `SOUL.md` are shared by every pack in the suite. Read the existing file, add or update only this pack's fields (`evp_drafts`, `competitors`, `primary_outreach_tier`, `refresh_cadence_days`, `evp`), and leave every other key exactly as it was. Never rewrite the file from the example, never delete another pack's keys. Show the diff and ask before changing a field that already has a value. `operator` and `icp` are shared: fill gaps only. In `SOUL.md`, touch only this pack's own `## ` sections.
9. **Publish the outreach line.** When the operator picks the line for `primary_outreach_tier`, write the `evp` block: `tier`, `primary`, `outcome`, `tradeoff`, `proof`. Downstream packs (cold-email, landing-page, sales-offer, email-sequence) read `evp`.

## What the agent NEVER does

- Generates an EVP without brand-config + SOUL (refuses)
- Claims outcomes outside the operator's "will claim" list
- Cites invented case studies / metrics
- Substitutes "predictable", "scalable", "best-in-class" for specific outcomes
- Produces Tier-mismatched lines (e.g., Tier-5 close on Tier-2 audience)
- Rewrites `brand-config.json` or `SOUL.md` wholesale, or drops another pack's keys or sections
- Writes the `psp` block (that belongs to the psp pack)

## Onboarding flow

Missing brand-config + SOUL on first invocation → run the `setup` mode,
`skills/evp/modes/setup.md`. Shared `operator`/`icp` questions are asked
once for the suite by `/gtm:setup`.

## Work files

The 3-tier brief goes to `gtm/evp-brief.md` in the operator's project
(create `gtm/` if missing). `brand-config.json` and `SOUL.md` stay at
the root.
