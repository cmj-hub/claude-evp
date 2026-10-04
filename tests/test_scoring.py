#!/usr/bin/env python3
"""Calibration cases for score_evp.py. The README quotes 100 and 59."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_evp.py"
CONFIG = json.loads((ROOT / "brand-config.example.json").read_text())


def score(*args, stdin=None):
    result = subprocess.run(
        [sys.executable, str(SCORE), "--format", "json", *args],
        input=stdin,
        capture_output=True,
        text=True,
    )
    return result, (json.loads(result.stdout) if result.stdout else None)


class ReadmeNumbers(unittest.TestCase):
    def test_good_example_scores_100(self):
        result, data = score("--file", str(ROOT / "examples/t3.good.txt"),
                             "--tier", "3", "--icp", "Series-B SaaS")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["total"], 100)

    def test_bad_example_scores_59(self):
        result, data = score("--file", str(ROOT / "examples/t3.bad.txt"), "--tier", "3")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["total"], 59)


class TierFit(unittest.TestCase):
    def tier_axis(self, data):
        return next(a for a in data["axes"] if a["name"] == "tier-fit")

    def test_example_drafts_fit_their_tier(self):
        drafts = CONFIG["evp_drafts"]
        for key, tier in [("tier_2_problem_aware", 2),
                          ("tier_3_solution_aware", 3),
                          ("tier_4_product_aware", 4)]:
            with self.subTest(key=key):
                _, data = score("--evp", drafts[key]["primary"], "--tier", str(tier))
                self.assertEqual(self.tier_axis(data)["score"], 20)
                self.assertEqual(data["detected_tier"], tier)

    def test_price_comparison_is_not_tier_5(self):
        _, data = score("--evp", "Versus agencies: $640 CPM vs $2,800.", "--tier", "5")
        self.assertLess(self.tier_axis(data)["score"], 20)

    def test_direct_ask_is_tier_5(self):
        _, data = score("--evp", "Acme Outbound: 14 SQLs a month at $4,000/month. Book a demo.",
                        "--tier", "5")
        self.assertEqual(self.tier_axis(data)["score"], 20)

    def test_vs_inside_word_is_not_a_hallmark(self):
        _, data = score("--evp", "Our canvses and advsors help.", "--tier", "3")
        self.assertIsNone(data["detected_tier"])

    def test_tier_mismatch_penalised(self):
        _, data = score("--evp", "Start a free trial and get started today.", "--tier", "2")
        self.assertEqual(self.tier_axis(data)["score"], 8)


class InputValidation(unittest.TestCase):
    def test_string_tier_rejected(self):
        result, _ = score("--stdin", stdin='{"evp": "x", "tier": "3"}')
        self.assertEqual(result.returncode, 2)
        self.assertIn("tier must be an integer 1-5", result.stderr)

    def test_out_of_range_tier_rejected(self):
        result, _ = score("--stdin", stdin='{"evp": "x", "tier": 9}')
        self.assertEqual(result.returncode, 2)

    def test_missing_file_exits_2(self):
        result, _ = score("--file", str(ROOT / "examples/missing.txt"))
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_two_word_line_fails(self):
        result, data = score("--evp", "x y")
        self.assertEqual(result.returncode, 1)
        self.assertLess(data["total"], 70)


if __name__ == "__main__":
    unittest.main()
