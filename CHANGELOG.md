# Changelog

## [0.7.0] — 2026-10-04

One skill per pack. The four sub-skills are modes of `evp`, read on demand.

### Moved
- `/evp:evp-onboarding` → `/evp:evp setup` (`skills/evp/modes/setup.md`). `onboarding` still routes there.
- `evp-kickoff` → `/evp:evp status` (`skills/evp/modes/status.md`). Also runs on a bare `/evp:evp`.
- `evp-craft` → `/evp:evp craft <tier>` (`skills/evp/modes/craft.md`).
- `evp-brief` → `/evp:evp brief` (`skills/evp/modes/brief.md`).
- The brief is saved to `gtm/evp-brief.md` (was `evp-brief-<icp-slug>.md` at the project root). `status` still finds an old-named brief.

### Changed
- Always-on cost drops from ~873 to ~208 tokens: one skill description instead of five.
- `argument-hint` lists the modes; `$ARGUMENTS` routes straight to one.
- Setup asks the shared `operator`/`icp` questions only when they are empty, and points at `/gtm:setup` to ask them once for the suite.
- A locked outreach line ends with `Next: /cold-email:cold-email`.
- `score_evp.py`: `--json` (alias of `--format json`); exit-1 output lists every reason as `- what is wrong → what to change` and ends `Next: fix the lines above and run this again.`; exit 0 ends `Next: /cold-email:cold-email`. JSON gains `reasons`, `fixes` and `next`; existing keys are unchanged. `--help` shows an example.

### Added
- `evals/`: five trigger cases (four should fire `evp`, one cold-email near-miss should not). `.github/workflows/evals.yml` runs them on manual dispatch when `ANTHROPIC_API_KEY` is set.
- README "In 60 seconds".
- `tests/test_cli.py`.

## [0.6.0] — 2026-10-04

Ports the one-proposition rule from `feat/one-proposition` onto current main.

### Added
- A line that scores 70+ prints under `# Proposition`; `--format json` gains `proposition`.
- A list is refused, exit 1: `Refusal: a list of value props is not one proposition`. Two or more items under `value_props`, `headlines`, `options`, `pillars`, `benefits` or `messages` (also inside `message_house`), or two or more bullet lines in a text file. `examples/value-props.json` shows it.
- `--file` reads a `.json` draft (`evp`, `tier`, `icp`) with the same tier check as `--stdin`.
- `SECURITY.md`, and a Privacy and security section in the README.

## [0.5.0] — 2026-10-04

Suite pass. EVP is step 2 of the GTM operator suite, after psp.

### Added
- Picking the line for `primary_outreach_tier` publishes an `evp` block to `brand-config.json` (`tier`, `primary`, `outcome`, `tradeoff`, `proof`) for cold-email, landing-page, sales-offer and email-sequence. `evp-craft` Step 7 writes it; `evp-kickoff` routes there until it exists.
- `brand-config.example.json` carries a full `psp` block (the shape the psp pack publishes) and an `evp` block matching the Tier 3 draft; `tests/test_example_config.py` pins both.
- "Works with the suite" section in `evp`: what it reads, writes, and hands off to.

### Changed
- PSP input reads `psp`, then falls back to `psp_drafts.primary`. Neither → name the psp pack (`/plugin install psp@gtm-operator-skills`, `/psp:psp`) and stop. Onboarding no longer asks whether claude-psp is installed, and never writes `psp` itself.
- `brand-config.json` and `SOUL.md` merge at the field level. The pack writes only its own keys, fills `operator` and `icp` gaps only, and asks before changing a filled field. AGENTS.md rules 7-9.
- Skill descriptions say when to use each skill and what each is not for. The main description drops the `<ICP>`-style placeholders. Every SKILL.md carries `models: ""`.
- Scorer calls use `${CLAUDE_PLUGIN_ROOT}/scripts/score_evp.py` unquoted, pre-approved in `allowed-tools`.
- README install lines use `npx skills add` and `/plugin install evp@gtm-operator-skills`.
- `plugin.json`: author URL.

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
