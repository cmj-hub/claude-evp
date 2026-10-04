#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@" > /dev/null 2>&1; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }
reject() { local n="$1"; shift; if "$@" > /dev/null 2>&1; then echo "  ✗ $n (expected non-zero exit)"; FAILED=$((FAILED+1)); else echo "  ✓ $n"; PASSED=$((PASSED+1)); fi; }

echo "=== skill structure ==="
check "SKILL.md frontmatter + layout" python3 scripts/validate-skill-frontmatter.py

echo "=== score_evp.py ==="
check "examples/t3.good.txt passes" \
  python3 scripts/score_evp.py --file examples/t3.good.txt --tier 3 --icp "Series-B SaaS"
reject "examples/t3.bad.txt rejected" \
  python3 scripts/score_evp.py --file examples/t3.bad.txt --tier 3

echo "=== unit tests ==="
check "tests/" python3 -m unittest discover -s tests

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
