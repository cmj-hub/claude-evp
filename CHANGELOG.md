# Changelog

## [0.4.0] — 2026-10-04

### Fixed
- The main `evp` skill now loads in the plugin. It sat at `evp/SKILL.md`; Claude Code only discovers `skills/<name>/SKILL.md`, so `/evp` was missing from plugin installs. Moved to `skills/evp/`.
- `score_evp.py` tier detection: Tier-4 lines could never be detected (the hallmark was the literal text `versus <name>`), any `$` read as Tier 5, and `vs` matched inside other words. Hallmarks are now word-boundary regexes; Tier 5 keys on a direct ask or a price per period. The pack's own Tier-2/3/4 example drafts now score full tier-fit.
- `score_evp.py --stdin` rejects a tier that is not an integer 1-5 instead of silently mis-scoring.
- `evp-onboarding` wrote to `evp_drafts.tier_3.*`; the key is `tier_3_solution_aware`.
- `evp-kickoff` assumed Tier 3 as primary, never routed to Tier 4, and treated the shipped `SOUL.md` template as a filled-in one.
- Broken relative links and dangling course references in sub-skills.

### Added
- `evp` skill restates the `AGENTS.md` rules (config gate, will-claim list, reservoir-only proof, banned stand-ins) and routes to sub-skills; adds `/evp score`.
- `evp-craft` and `evp-brief` read inputs from `brand-config.json` + `SOUL.md`, score every variant with `score_evp.py`, and never fill an empty proof slot.
- `evp-brief` writes `evp-brief-<icp>.md`; kickoff uses it and `refresh_cadence_days` to flag a stale brief.
- `evp-onboarding` is user-invocable and will not overwrite existing config without a yes.
- `score_evp.py --file`, tradeoff markers beyond "without" (`instead of`, `rather than`, `won't fix`), currency-prefixed metrics, and a stronger penalty for lines under 8 words.
- `tests/test_scoring.py` pins the README numbers (100 / 59) and tier calibration.
- Validator checks the `skills/<name>/SKILL.md` layout and relative links. Smoke test runs the validator, the examples, and the unit tests.
- README skills table and plugin command names.

### Unchanged
- README scores: `examples/t3.good.txt` 100, `examples/t3.bad.txt` 59.

## [0.3.0] — 2026-09-08

Public magnet pass. Instrument stays public. First loop is 15 minutes.

### Added
- Definition-first README (GEO paragraph, 15-minute artifact, FAQ H2s, current Pass price).
- Cross-agent installer: `npx skills add cmj-hub/claude-evp --all -g --full-depth` (Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, and the rest of the skills CLI list). Fallback copies into well-known `*/skills` dirs.
- `package.json` (`jmc-evp`) so `npm install github:cmj-hub/claude-evp` and `npx jmc-evp` work. Not published to npmjs.com.
- `examples/` golden good/bad pair for the first loop.

### Changed
- Removed pricing copy from the public pack; CTAs point at the free hosted tools.
- `plugin.json` description is the definition, homepage is /skills.

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
