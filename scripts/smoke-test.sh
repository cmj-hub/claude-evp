#!/usr/bin/env bash
set -euo pipefail
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@"; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }

echo "=== score_evp.py ==="
check "strong T3 EVP" \
  python3 scripts/score_evp.py \
    --evp "For Series-B SaaS in a pipeline gap, we ship 14+ SQLs per month without hiring 2 more SDRs." \
    --tier 3 \
    --icp "Series-B SaaS"

# Abstract EVP should fail
echo "  (testing inverse — abstract EVP should exit non-zero)"
if python3 scripts/score_evp.py --evp "We help companies improve their growth and optimize outcomes." --tier 3 > /dev/null 2>&1; then
  echo "  ✗ abstract EVP should have failed but passed"
  FAILED=$((FAILED+1))
else
  echo "  ✓ abstract EVP correctly rejected"
  PASSED=$((PASSED+1))
fi

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
