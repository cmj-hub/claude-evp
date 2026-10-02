<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Value proposition skill for Claude Code. A value proposition is one line that says why this buyer should care.">
</p>

# Value proposition skill for Claude Code

A value proposition is one line that says why this buyer should care. The same product needs a different line for each buyer.

> Same product. Five readers. Twenty-two words each. Because they are not standing in the same place.

An early value proposition is a line of 22 words or fewer, matched to an awareness tier. Same product, five lines, because the unaware buyer and the vendor-comparing buyer are not the same reader.

You have been writing one line — the line *you* would buy. That is a Most-Aware line. Most of the people who land on your page are not there. They are still naming the pain, or comparing categories, or lining you up against a vendor they already know.

Five stages name where the buyer is standing: unaware, problem-aware, solution-aware, product-aware, most-aware. One product. Five openings. The scorer in this repo checks length, outcome, tradeoff, ICP, and tier-fit.

A specific Tier-3 line scored **100**. "We help companies improve their growth and optimize outcomes" scored **59**. The Python is in `scripts/score_evp.py`. No LLM. No paid API.

The build guide teaches a human. The pack teaches an agent.

<p align="center">
  <img src="./assets/demo.gif" alt="Value proposition skill — Tier-3 line 100, vague line 59" width="100%">
</p>

## What this replaces

A $10K–15K positioning sprint's first output: one hero line, written from inside the building.

## Install

```bash
npx skills add cmj-hub/claude-evp --all -g --full-depth
```

`--all` writes this pack for every host the installer knows. One host:

```bash
npx skills add cmj-hub/claude-evp --skill '*' -g --full-depth -y -a claude-code
```

Swap `claude-code` for `cursor`, `codex`, `grok`, `github-copilot`, `windsurf`, `cline`, or `opencode`.

### Claude Code only

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install evp
```

## What you walk out with in 15 minutes

Artifact: `examples/t3.good.txt`.

```bash
python3 scripts/score_evp.py \
  --evp "For Series-B SaaS in a pipeline gap, we ship 14+ SQLs per month without hiring 2 more SDRs." \
  --tier 3 --icp "Series-B SaaS"
python3 scripts/score_evp.py --evp "We help companies improve their growth and optimize outcomes." --tier 3
```

Three tier lines from the sample Pain Signal Profile. Then yours.

## What this pack will not do

It will not pick this quarter's PSP. It will not invent proof you did not hand it. It will not write five ads from a blank page.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## Why 22 words?

Long enough for ICP, pain, one outcome, and one tradeoff. Short enough to sit in a cold-email third line or a hero. If it does not fit, you have two claims. Cut one.

## Which tier should I write first?

Tiers 2–4. That is where B2B buyers live. Tier 5 is a direct ask — your internal product view. Unaware (Tier 1) is a pain reveal, not a product sentence.

## Do I need Operator Pass to use this?

No, and there is no key to enter. The pack, the scorer, and the sample are MIT. If you would rather not install anything, the [EVP Generator](https://jaymountconsulting.com/tools/evp-generator) writes the same line in your browser.

## On the site

- [Early Value Propositions pack](https://jaymountconsulting.com/skills/claude-evp) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack
- [Course twin](https://jaymountconsulting.com/learn/courses/early-value-propositions) — human build guide for this pack

## Free, no signup

- **[EVP Generator](https://jaymountconsulting.com/tools/evp-generator)** — the same job as this pack, hosted. No account, no key.
- [Early Value Propositions framework](https://jaymountconsulting.com/frameworks/early-value-propositions)
- [EVP Brief Generator](https://jaymountconsulting.com/tools/evp-brief-generator)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.


## Next

Previous: [Ideal customer profile](https://github.com/cmj-hub/claude-psp)

Next: [Pricing strategy](https://github.com/cmj-hub/claude-pricing)

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
