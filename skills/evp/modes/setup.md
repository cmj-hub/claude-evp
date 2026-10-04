# Setup — first-run EVP config

10 minutes of setup that makes every downstream EVP differentiated
instead of generic.

## Contents

- Activation
- Workflow
- References

## Activation

Runs first when `brand-config.json` or `SOUL.md` is missing.

Also `/evp:evp setup` (`onboarding` works too), "Set up EVP brand
config", "EVP onboarding".

Templates: `brand-config.example.json` and `SOUL.md` ship at the pack
root (`${CLAUDE_PLUGIN_ROOT}` in a plugin install). Use them as the
shape for what you write, not as files to copy. Both files are shared
by every pack in the suite (psp, cold-email and the rest write to them
too). If the project already has either file, read it, show what is
filled, and only ask for the gaps. Step 8 has the merge rules.

Every answer is the operator's own. Do not suggest outcomes, metrics,
or proofs for them to accept; the examples below show the shape only.

## Workflow

### Step 0 — Shared basics (once for the whole suite)

`operator` (name, company, title, calendar_url) and `icp` (segment,
role_targets, exclusion_criteria; stage, size_range, geos optional) are
shared by every pack. If they are filled, skip this step.

If they are missing, say: "Run `/gtm:setup` once for the whole suite."
If the gtm plugin is not installed (`/plugin install
gtm@gtm-operator-skills`), ask only those shared questions inline, in
one short batch, and fill gaps only. Then go on with the EVP questions
below; do not ask the shared ones again.

### Step 1 — ICP + PSP carry-forward

Read the PSP from `brand-config.json`, in this order:

1. `psp` — the block the psp pack publishes when a primary PSP is
   locked. Use `psp.primary_pain` and `psp.vocabulary`.
2. Fallback: `psp_drafts.primary` — an unlocked draft. Use
   `psp_drafts.primary.pain` and `.vocabulary`, and tell the operator
   it is a draft, not a locked PSP.
3. Neither → stop and say:

```
No PSP in brand-config.json. The psp pack produces it.

Install:  /plugin install psp@gtm-operator-skills
Then run: /psp:psp

EVP without a PSP is a guess.
```

Do not invent the pain or the vocabulary, and do not write a `psp`
block yourself; that block belongs to the psp pack. Take `icp.segment`
as it is; fill it only if it is empty.

### Step 2 — Primary outreach tier

```
Where is YOUR buyer on the Schwartz tier ladder when they meet you?

Most B2B buyers live in Tiers 2-4. Pick the most common one for your outreach:

  Tier 1 (unaware)         — you have to reveal the pain first
  Tier 2 (problem-aware)   — they know the pain, no solutions evaluated
  Tier 3 (solution-aware)  — they're comparing categories (in-house / agency / tool)
  Tier 4 (product-aware)   — comparing specific vendors
  Tier 5 (most aware)      — ready to buy

If you don't know, default to Tier 3 — most outbound campaigns target
that tier.
```

Save to `brand-config.primary_outreach_tier`.

### Step 3 — Outcomes-I-will-claim list

```
What specific outcomes are you willing to claim in writing?

Each outcome needs:
1. A specific noun (not a verb — "14 SQLs", not "more pipeline")
2. A specific timeframe (in 30 days, per month, per quarter)
3. A proof point you can back it with

Examples of GOOD outcomes:
  "14+ SQLs per month"
  "Targeted-outbound CPM under $700"
  "First positive reply within 7 days"

Examples of BAD outcomes (refuse to claim):
  "Better demand-gen"
  "Improved efficiency"
  "Best-in-class outreach"

Give me 3-5 outcomes you're willing to claim. These constrain every
downstream EVP variant.
```

Save to `SOUL.md` (outcomes-I-will-claim list) + `brand-config.evp_drafts.tier_3_solution_aware.outcome`.

### Step 4 — Tradeoffs you name

```
For each outcome, what's the obvious tradeoff you spare them from?

The EVP shape is "<outcome> without <tradeoff>". The tradeoff carries
the line — name something they'd otherwise have to give up.

Examples:
  "without hiring 2 more SDRs"
  "without breaking the PLG self-serve motion"
  "without paying agency retainer rates"
```

Save to `brand-config.evp_drafts.tier_3_solution_aware.tradeoff` + `SOUL.md`.

### Step 5 — Proofs reservoir

```
Give me 3-5 concrete proofs you can cite. Each is anonymized but
specific.

Examples:
  "Series-B SaaS hit 14 SQLs in 30 days from a PSP rewrite — case study at /case-studies/X"
  "Bootstrapped agency went 2% → 11% reply rate by killing demographic targeting"

These become the proof reservoir — EVP variants pull from here, not
fabricated case studies.
```

Save to `SOUL.md`.

### Step 6 — Competitors (for Tier 4 EVPs)

```
For Tier 4 EVPs, you need to name competitors and your delta on a
specific axis.

Top 2-3 competitors + the axis you beat them on:
  1. Generic outbound agency — CPM efficiency
  2. AI SDR vendor — reply quality vs volume
  3. In-house SDR build — time-to-payback
```

Save to `brand-config.competitors`.

### Step 7 — Voice (SOUL.md)

```
Per-tier voice settings:

Tier 2 (problem-aware) — tone: ?
Tier 3 (solution-aware) — tone: ?
Tier 4 (product-aware) — tone: ?

Won't-write list:
  • <e.g. industry guarantees you don't actually back>
  • <e.g. competitor names you won't reference by full brand>
```

Save to `SOUL.md`.

### Step 8 — Write the files + smoke test

Write `brand-config.json` + `SOUL.md` at project root. Both are shared
by every pack in the suite, so merge at the field level:

- Read the existing file first. Add or update only the fields this
  pack owns (`evp_drafts`, `competitors`, `primary_outreach_tier`,
  `refresh_cadence_days`, `evp`); leave every other key exactly as it
  was. Never rewrite the file from `brand-config.example.json`, never
  delete another pack's keys (`psp`, `psp_drafts`, `tone`, `pricing`
  and the rest stay as they are).
- Show the diff and ask before changing a field that already has a
  value.
- `operator` and `icp` are shared: fill gaps only.
- `SOUL.md`: append or update only this pack's own `## ` sections (the
  ones in the pack's [SOUL.md](../../../SOUL.md) template); never rewrite
  another pack's section.

Replace every `<...>` placeholder in this pack's SOUL sections — a
placeholder left behind makes the [status](status.md) mode route back here. Leave `evp_drafts.*.primary` empty
unless the operator already has a line they want to keep. If they
keep one for the primary outreach tier, publish it as the `evp` block
(shape in [craft](craft.md) Step 7); otherwise `evp` waits until they pick a
line. Show:

```
✓ brand-config.json — Tier 3 primary + 3 outcomes + 3 competitors
✓ SOUL.md — outcomes-will-claim list + 4 proofs + tier voice

Try a smoke test:
> Generate a Tier 3 EVP for my ICP

The output will use:
- Your outcomes-will-claim list (refuses outside it)
- Your tradeoffs
- Proofs from your reservoir

Next: /evp:evp craft
```

## References

- `brand-config.example.json` (pack root)
- [SOUL.md](../../../SOUL.md)
- `AGENTS.md` (pack root)
- Other modes: [craft.md](craft.md), [brief.md](brief.md)
