# Changelog

## [0.2.1] — 2026-05-24

Marketplace-submission compliance pass. No functional changes.

### Fixed
- `plugin.json` `author` field now an object `{ "name": "..." }` per Claude Code plugin manifest schema. `claude plugin validate` now passes.

## [0.2.0] — 2026-05-23

Polish pass matching claude-cold-email + claude-psp v0.2.

### Added
- 3-tier config: brand-config.example.json + SOUL.md + AGENTS.md
- skills/evp-onboarding (10-min setup), skills/evp-kickoff (state router)
- scripts/score_evp.py — 5-axis scoring (length, outcome, tradeoff, ICP, tier-fit)
- README rewrite: cost-replacement positioning, mermaid

### Verified
- score_evp.py: strong T3 EVP → 100/100; abstract → 59/100

## [0.1.0] — 2026-05-23

Initial release.
