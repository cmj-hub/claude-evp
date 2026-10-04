#!/usr/bin/env python3
"""
score_evp.py — Deterministic EVP scorer.

Scores any EVP draft 0-100 across 5 axes:
- Length (≤22 words)
- Outcome specificity (concrete noun + metric)
- Tradeoff specificity (concrete thing they'd give up)
- ICP named (specific segment)
- Tier-fit (matches the requested Schwartz tier)

USAGE:
    python3 score_evp.py --evp "<line>" --tier 3
    python3 score_evp.py --evp "<line>" --tier 3 --icp "Series-B SaaS"
    python3 score_evp.py --file examples/t3.good.txt --tier 3
    echo '{"evp": "<line>", "tier": 3}' | python3 score_evp.py --stdin
    python3 score_evp.py --file gtm/evp.json   # {"evp": ..., "tier": ..., "icp": ...}
    python3 score_evp.py --file examples/t3.good.txt --tier 3 --json   # one JSON object

OUTPUT:
    Text by default. On exit 1 every reason prints as
    "- <what is wrong> → <what to change>", then
    "Next: fix the lines above and run this again." On exit 0 the last
    line names the next suite step (Next: /cold-email:cold-email).
    --json (alias of --format json) adds "reasons", "fixes" (parallel
    lists) and "next"; existing keys are unchanged.

ONE PROPOSITION:
    A score >= 70 prints the line under "# Proposition" (and "proposition"
    in --format json). A list of value props, headline options or message
    house lines (2+ items under value_props / headlines / options / pillars /
    benefits / messages, or 2+ bullet lines in a text file) is refused.

EXIT CODES:
    0  score >= 70 (ship or tighten)
    1  score < 70 (rewrite), or a list of value props instead of one line
    2  bad input

NO LLM. NO network. Pure regex + heuristics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple


MAX_INPUT_BYTES = 2_000_000


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_json(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")
    if not isinstance(data, dict):
        fail_input("JSON must be an object")
    return data


def read_stdin_text() -> str:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        fail_input("input is too large")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("input is not UTF-8 text")


ABSTRACT_OUTCOMES = {
    "improve", "optimize", "enhance", "scale", "grow", "drive",
    "boost", "accelerate", "streamline", "transform", "elevate",
    "modernize", "unlock", "leverage", "enable", "empower",
}

VAGUE_TRADEOFFS = {
    "and more", "etc", "etc.", "without compromise", "without compromising",
    "without sacrificing quality",
}

# Phrases that mark a real tradeoff clause. "without" is the canonical
# JMC shape; the others carry the same job in Tier 2-4 reframes.
# Keys that hold a list of lines: what a copy deck ships, not one proposition.
LIST_KEYS = ("value_props", "headlines", "options", "pillars", "benefits", "messages")

REFUSAL = "a list of value props is not one proposition"


def string_items(value: object) -> List[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def prop_list(data: dict) -> List[str]:
    """Two or more distinct lines under a list key (or inside message_house)."""
    found: List[str] = []
    for key in LIST_KEYS:
        found.extend(string_items(data.get(key)))
    house = data.get("message_house")
    if isinstance(house, dict):
        for key in LIST_KEYS:
            found.extend(string_items(house.get(key)))
    seen: List[str] = []
    for item in found:
        if item not in seen:
            seen.append(item)
    return seen if len(seen) >= 2 else []


def bullet_props(text: str) -> List[str]:
    """Two or more bulleted or numbered lines in a text draft."""
    lines = []
    for line in text.splitlines():
        match = re.match(r"^(?:[-*•]|\d+[.)])\s+(.+)$", line.strip())
        if match and match.group(1).strip():
            lines.append(match.group(1).strip())
    return lines if len(lines) >= 2 else []


TRADEOFF_MARKERS = [
    r"\bwithout\b", r"\binstead of\b", r"\brather than\b",
    r"\bno need to\b", r"\bwon'?t fix\b", r"\bskip(ping)? the\b",
]

# Regex hallmarks per Schwartz tier. Word-boundary matched so "vs" does not
# fire inside other words. "versus"/"vs" is shared by Tier 3 (category split)
# and Tier 4 (vendor delta). Tier 5 keys on a direct ask or a price-per-period,
# not on any dollar sign, so a Tier-4 CPM comparison is not read as Tier 5.
TIER_HALLMARKS = {
    1: [r"\bif your\b", r"\byou'?re losing\b", r"\byou don'?t know\b",
        r"\bmost teams aren'?t\b"],
    2: [r"\bthe problem is upstream\b", r"\bisn'?t an? \b", r"\breal lever\b",
        r"\bnot a fix\b", r"\bwon'?t fix\b"],
    3: [r"\bversus\b", r"\bvs\.?(?=\s)", r"\binstead of\b", r"\bwe ship\b",
        r"\bwe deliver\b", r"\bmost teams pick\b", r"\brather than\b"],
    4: [r"\bversus\b", r"\bvs\.?(?=\s)", r"\bcompared to\b", r"\bwe beat\b",
        r"\bspecifically on\b", r"\bunlike\b", r"\bswitch(ing)? from\b"],
    5: [r"\bget started\b", r"\bstart today\b", r"\bbook a (demo|call)\b",
        r"\bsign up\b", r"\bsubscribe\b", r"\bfree trial\b",
        r"[$€£]\s?\d[\d,]*(\.\d+)?\s*/\s*(mo|month|seat|user)\b"],
}


@dataclass
class AxisScore:
    name: str
    score: int
    max_score: int
    notes: List[str] = field(default_factory=list)


@dataclass
class EVPScore:
    evp: str
    total: int
    max_total: int
    word_count: int
    verdict: str
    axes: List[AxisScore]
    detected_tier: Optional[int] = None


def score_length(evp: str) -> AxisScore:
    """20 points. ≤22 words = full score; -2 per word over."""
    words = len(evp.split())
    score = 20
    notes = [f"Word count: {words}"]
    if words > 22:
        score -= min(20, (words - 22) * 2)
        notes.append(f"Over 22-word limit by {words - 22}")
    elif words < 8:
        score -= 10
        notes.append("Too short — likely missing a block")
    return AxisScore("length", max(0, score), 20, notes)


def score_outcome(evp: str) -> AxisScore:
    """25 points. Specific noun + metric vs abstract verbs."""
    score = 25
    notes = []
    evp_lower = evp.lower()

    abstract_hits = [w for w in sorted(ABSTRACT_OUTCOMES) if re.search(rf"\b{re.escape(w)}\b", evp_lower)]
    if abstract_hits:
        score -= min(15, len(abstract_hits) * 6)
        notes.append(f"Abstract verbs: {abstract_hits} — use concrete outcome")

    # Look for numbers / metrics
    has_number = bool(
        re.search(r"[$€£]\s?\d", evp_lower)
        or re.search(r"\d+(\.\d+)?\s*(\+|%|\$|x|×|k|m\b|day|week|month|quarter|hour|min|sql|mql|lead|meeting|reply|sec|client|customer|account|deal)", evp_lower)
    )
    if not has_number:
        score -= 8
        notes.append("No specific metric / number — outcome should be measurable")

    return AxisScore("outcome", max(0, score), 25, notes)


def score_tradeoff(evp: str) -> AxisScore:
    """20 points. 'without <specific thing>' present, not vague."""
    score = 20
    notes = []
    evp_lower = evp.lower()

    has_marker = any(re.search(m, evp_lower) for m in TRADEOFF_MARKERS)
    if not has_marker:
        score -= 10
        notes.append("No 'without <tradeoff>' clause — EVPs need the tradeoff explicit")
    else:
        # Check for vague tradeoffs
        for vague in sorted(VAGUE_TRADEOFFS):
            if vague in evp_lower:
                score -= 8
                notes.append(f"Vague tradeoff '{vague}' — replace with specific thing they'd give up")
                break

    return AxisScore("tradeoff", max(0, score), 20, notes)


def score_icp(evp: str, icp: Optional[str]) -> AxisScore:
    """15 points. ICP named in the line."""
    score = 15
    notes = []
    if icp:
        # Look for ICP segment words in the EVP
        icp_words = set(re.findall(r"\b[A-Za-z]+\b", icp.lower()))
        evp_words = set(re.findall(r"\b[A-Za-z]+\b", evp.lower()))
        # Need at least one notable ICP word
        notable_overlap = [w for w in sorted(icp_words) if w in evp_words and len(w) > 3 and w not in {"with", "from", "that", "this", "their", "have", "they"}]
        if not notable_overlap:
            score -= 8
            notes.append(f"ICP '{icp}' not represented in line — name the segment explicitly")
        else:
            notes.append(f"ICP signals in line: {notable_overlap[:3]}")
    else:
        # Heuristic: look for any segment-shaped noun (Series-B, SaaS, etc.)
        segment_signals = re.findall(r"\b(Series-?[A-Z]|SaaS|PLG|B2B|DevTools|Bootstrap)\b", evp, re.IGNORECASE)
        if not segment_signals:
            score -= 6
            notes.append("No segment indicator in line — ICP should be named explicitly")

    return AxisScore("icp", max(0, score), 15, notes)


def detect_tiers(evp: str) -> List[int]:
    """Every tier whose hallmarks appear in the line, lowest first."""
    evp_lower = evp.lower()
    return [
        tier for tier, hallmarks in TIER_HALLMARKS.items()
        if any(re.search(h, evp_lower) for h in hallmarks)
    ]


def score_tier_fit(evp: str, requested_tier: Optional[int]) -> Tuple[AxisScore, Optional[int]]:
    """20 points. Detect which tier the line fits + score against requested."""
    score = 20
    notes = []

    matches = detect_tiers(evp)
    if requested_tier in matches:
        detected = requested_tier
    else:
        detected = matches[0] if matches else None

    if requested_tier is not None:
        if requested_tier in matches:
            notes.append(f"Tier-fit confirmed: line signals Tier {requested_tier}")
        elif matches:
            score -= 12
            notes.append(f"Requested Tier {requested_tier} but line signals Tier {matches}")
        else:
            score -= 5
            notes.append(f"No tier hallmarks detected — line is tier-ambiguous")
    elif not matches:
        score -= 5
        notes.append("No tier hallmarks — calibrate awareness signaling")

    axis = AxisScore("tier-fit", max(0, score), 20, notes)
    return axis, detected


def score_evp(evp: str, tier: Optional[int], icp: Optional[str]) -> EVPScore:
    length = score_length(evp)
    outcome = score_outcome(evp)
    tradeoff = score_tradeoff(evp)
    icp_axis = score_icp(evp, icp)
    tier_axis, detected = score_tier_fit(evp, tier)

    axes = [length, outcome, tradeoff, icp_axis, tier_axis]
    total = sum(a.score for a in axes)
    max_total = sum(a.max_score for a in axes)

    if total >= 85:
        verdict = "Strong EVP — ship"
    elif total >= 70:
        verdict = "Solid — tighten 1-2 axes"
    elif total >= 50:
        verdict = "Workable but generic — re-do outcome/tradeoff"
    else:
        verdict = "Too abstract — rewrite"

    return EVPScore(
        evp=evp,
        total=total,
        max_total=max_total,
        word_count=len(evp.split()),
        verdict=verdict,
        axes=axes,
        detected_tier=detected,
    )


NEXT_STEP = "/cold-email:cold-email"
RETRY = "fix the lines above and run this again."

# Notes that are information, not problems.
INFO_NOTE = re.compile(r"^(Word count:|ICP signals in line:|Tier-fit confirmed)")

# Notes whose text after the dash is a reason, not a change to make.
PREFIX_FIXES = (
    ("Over 22-word limit", "cut words until it is 22 or fewer; keep the outcome and the tradeoff"),
    ("Too short", "add the missing block: segment, outcome with a number, or 'without' tradeoff"),
    ("No specific metric", "add a number and a timeframe from your will-claim list"),
    ("No 'without <tradeoff>' clause", "add 'without <the thing they would otherwise give up>'"),
    ("No segment indicator", "name the segment in the line (e.g. Series-B SaaS)"),
    ("Requested Tier", "rewrite in the requested tier's shape, or score it at the tier it signals"),
    ("No tier hallmarks detected", "use the requested tier's shape (see the tier table in the skill)"),
    ("No tier hallmarks", "pass --tier and write in that tier's shape"),
)

LIST_FIX = "pick one line and score that line alone"


def fix_lines(s: EVPScore) -> Tuple[List[str], List[str]]:
    """Parallel reasons/fixes for a line that scores under 70."""
    reasons = [f"score {s.total}/{s.max_total} is under 70"]
    fixes = ["work through the axis lines below, lowest axis first"]
    for axis in sorted(s.axes, key=lambda a: a.score - a.max_score):
        for note in axis.notes:
            if INFO_NOTE.search(note):
                continue
            what, _, fix = note.partition(" — ")
            for prefix, better in PREFIX_FIXES:
                if note.startswith(prefix):
                    fix = better
                    break
            reasons.append(f"{axis.name}: {what}")
            fixes.append(fix or "rewrite this part and score again")
    return reasons, fixes


def format_fixes(reasons: List[str], fixes: List[str]) -> List[str]:
    lines = ["", "## What to fix"]
    lines.extend(f"- {what} → {fix}" for what, fix in zip(reasons, fixes))
    lines.extend(["", f"Next: {RETRY}"])
    return lines


def format_text(s: EVPScore) -> str:
    lines = [
        f"# EVP Score",
        f"",
        f"EVP: \"{s.evp}\"",
        f"Words: {s.word_count}",
        f"Detected tier: {s.detected_tier or '—'}",
        f"Score: {s.total}/{s.max_total} — {s.verdict}",
        f"",
        f"## Per-axis",
    ]
    for a in s.axes:
        lines.append(f"  {a.name.ljust(15)} {a.score}/{a.max_score}")
        for n in a.notes:
            lines.append(f"    • {n}")
    return "\n".join(lines)


def fields_from_json(data: dict, cli_tier: Optional[int], cli_icp: Optional[str]):
    """evp / tier / icp from a JSON draft. Tier must be an integer 1-5."""
    evp = data.get("evp", "")
    if not isinstance(evp, str):
        evp = ""
    tier = data.get("tier")
    if tier is not None and (isinstance(tier, bool) or tier not in (1, 2, 3, 4, 5)):
        fail_input("tier must be an integer 1-5")
    if tier is None:
        tier = cli_tier
    icp = data.get("icp")
    if icp is not None and not isinstance(icp, str):
        icp = None
    if icp is None:
        icp = cli_icp
    return evp.strip(), tier, icp


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score one EVP line 0-100. Exit 0 at 70+, 1 under 70 or a list of lines, 2 bad input.",
        epilog="example: python3 scripts/score_evp.py --file examples/t3.good.txt --tier 3 --icp \"Series-B SaaS\"",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--evp", default="")
    parser.add_argument("--tier", type=int, default=None, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--icp", default=None)
    parser.add_argument("--stdin", action="store_true",
                        help='read {"evp": ..., "tier": ..., "icp": ...} JSON from stdin')
    parser.add_argument("--file", default=None,
                        help="read the EVP line from a text file (e.g. examples/t3.good.txt)")
    parser.add_argument("--json", dest="format", action="store_const", const="json",
                        help="print one JSON object (same as --format json)")
    parser.add_argument("--format", dest="format", default="text", choices=["text", "json"],
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    props: List[str] = []
    if args.stdin:
        data = parse_json(read_stdin_text())
        props = prop_list(data)
        evp, tier, icp = fields_from_json(data, args.tier, args.icp)
    elif args.file:
        try:
            with open(args.file, encoding="utf-8-sig") as fh:
                text = fh.read(MAX_INPUT_BYTES + 1)
        except (OSError, UnicodeDecodeError):
            fail_input("cannot read --file as UTF-8 text")
        if len(text) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        if args.file.endswith(".json"):
            data = parse_json(text)
            props = prop_list(data)
            evp, tier, icp = fields_from_json(data, args.tier, args.icp)
        else:
            props = bullet_props(text)
            evp = text.strip()
            tier = args.tier
            icp = args.icp
    else:
        evp = args.evp
        tier = args.tier
        icp = args.icp

    if props:
        if args.format == "json":
            print(json.dumps({"refusal": REFUSAL, "items": len(props), "proposition": "",
                              "reasons": [REFUSAL], "fixes": [LIST_FIX], "next": RETRY}, indent=2))
        else:
            print(f"Refusal: {REFUSAL}")
            print(f"  {len(props)} lines found. Pick one and score that line alone.")
            print("\n".join(format_fixes([f"{REFUSAL} ({len(props)} lines found)"], [LIST_FIX])))
        return 1

    if not evp:
        print("--evp required.", file=sys.stderr)
        return 2

    result = score_evp(evp, tier, icp)
    passed = result.total >= 70
    reasons, fixes = ([], []) if passed else fix_lines(result)
    if args.format == "json":
        payload = asdict(result)
        payload["proposition"] = result.evp if passed else ""
        payload["reasons"] = reasons
        payload["fixes"] = fixes
        payload["next"] = NEXT_STEP if passed else RETRY
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(result))
        if passed:
            print()
            print("# Proposition")
            print(result.evp)
            print()
            print(f"Next: {NEXT_STEP}")
        else:
            print("\n".join(format_fixes(reasons, fixes)))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
