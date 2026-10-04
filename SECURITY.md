# Security

## What this pack does on your machine

- One script, `scripts/score_evp.py`: stdlib Python, run locally. It reads the line you pass (`--evp`, a text or JSON file, or stdin) and prints a score. It writes nothing.
- The skills read `brand-config.json` and `SOUL.md` from your project root.
- The skills write only to your project root: `brand-config.json` (this pack's keys, merged at the field level), this pack's sections of `SOUL.md`, and `evp-brief-<icp-slug>.md`. They ask before changing a filled field.
- Network: none. No script opens a network connection, and no skill allows WebFetch.
- `install.sh` / `install.ps1` print the repo URL and exit. They download and run nothing.
- No telemetry. No credentials asked for or stored.
- Nothing is sent, posted or published by the pack.

## Reporting a vulnerability

Email jay@jaymountconsulting.com with "security" and the repo name in the subject, or open a private advisory under this repo's Security tab. Do not open a public issue for a vulnerability. Expect a reply within five business days.

## Supported versions

Only the latest release on `main` gets fixes.
