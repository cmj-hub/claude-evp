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
    python3 score_evp.py --stdin

NO LLM. NO network. Pure regex + heuristics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional


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

TIER_HALLMARKS = {
    1: ["if your", "you're losing", "you don't know", "most teams aren't"],
    2: ["the problem is upstream", "isn't a", "real lever", "not a fix"],
    3: ["versus", "vs", "instead of", "we ship", "we deliver"],
    4: ["versus <name>", "compared to", "we beat", "specifically on"],
    5: ["operator pass", "get started", "$", "/month", "subscribe"],
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
        score -= 3
        notes.append("Too short — likely missing a block")
    return AxisScore("length", max(0, score), 20, notes)


def score_outcome(evp: str) -> AxisScore:
    """25 points. Specific noun + metric vs abstract verbs."""
    score = 25
    notes = []
    evp_lower = evp.lower()

    abstract_hits = [w for w in ABSTRACT_OUTCOMES if re.search(rf"\b{re.escape(w)}\b", evp_lower)]
    if abstract_hits:
        score -= min(15, len(abstract_hits) * 6)
        notes.append(f"Abstract verbs: {abstract_hits} — use concrete outcome")

    # Look for numbers / metrics
    has_number = bool(re.search(r"\d+(\.\d+)?\s*(\+|%|\$|x|×|k|K|M|day|week|month|quarter|hour|min|sql|mql|lead|meeting|reply|sec|client|customer|account|deal)", evp_lower))
    if not has_number:
        score -= 8
        notes.append("No specific metric / number — outcome should be measurable")

    return AxisScore("outcome", max(0, score), 25, notes)


def score_tradeoff(evp: str) -> AxisScore:
    """20 points. 'without <specific thing>' present, not vague."""
    score = 20
    notes = []
    evp_lower = evp.lower()

    has_without = "without" in evp_lower
    if not has_without:
        score -= 10
        notes.append("No 'without <tradeoff>' clause — EVPs need the tradeoff explicit")
    else:
        # Check for vague tradeoffs
        for vague in VAGUE_TRADEOFFS:
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
        notable_overlap = [w for w in icp_words if w in evp_words and len(w) > 3 and w not in {"with", "from", "that", "this", "their", "have", "they"}]
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


def score_tier_fit(evp: str, requested_tier: Optional[int]) -> AxisScore:
    """20 points. Detect which tier the line fits + score against requested."""
    score = 20
    notes = []
    evp_lower = evp.lower()

    matches = []
    for tier, hallmarks in TIER_HALLMARKS.items():
        if any(h in evp_lower for h in hallmarks):
            matches.append(tier)

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evp", default="")
    parser.add_argument("--tier", type=int, default=None, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--icp", default=None)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()

    if args.stdin:
        data = parse_json(read_stdin_text())
        evp = data.get("evp", "")
        if not isinstance(evp, str):
            evp = ""
        tier = data.get("tier")
        icp = data.get("icp")
        if icp is not None and not isinstance(icp, str):
            icp = None
    else:
        evp = args.evp
        tier = args.tier
        icp = args.icp

    if not evp:
        print("--evp required.", file=sys.stderr)
        return 2

    result = score_evp(evp, tier, icp)
    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_text(result))
    return 0 if result.total >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
