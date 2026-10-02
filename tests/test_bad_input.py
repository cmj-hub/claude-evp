#!/usr/bin/env python3
"""Bad EVP JSON exits 2 and does not echo the document."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_evp.py"
TOKEN = "super-secret-token"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCORE), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScoreEvpBadInput(unittest.TestCase):
    def test_evp_scores(self):
        result = run(["--evp", "Cut onboarding from 14 days to 2 for series B SaaS"])
        self.assertIn(result.returncode, (0, 1))
        self.assertNotIn("Traceback", result.stderr)

    def test_bad_json_hides_bytes(self):
        result = run(["--stdin"], stdin='{"evp": "' + TOKEN)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(TOKEN, result.stderr + result.stdout)

    def test_array_rejected(self):
        result = run(["--stdin"], stdin="[]")
        self.assertEqual(result.returncode, 2)
        self.assertIn("JSON must be an object", result.stderr)

    def test_empty_evp_still_exits_2(self):
        result = run(["--stdin"], stdin='{"evp":""}')
        self.assertEqual(result.returncode, 2)
        self.assertIn("--evp required", result.stderr)

    def test_value_prop_list_is_refused(self):
        result = run(["--file", str(ROOT / "examples" / "value-props.json")])
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        blob = result.stdout + result.stderr
        self.assertIn("a list of value props is not one proposition", blob)
        self.assertNotIn("# Proposition", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_headline_options_are_refused(self):
        draft = '{"headlines":["Option A: Ship faster","Option B: Spend less"]}'
        result = run(["--stdin"], stdin=draft)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("a list of value props is not one proposition", result.stdout + result.stderr)

    def test_good_file_prints_one_proposition(self):
        result = run([
            "--file", str(ROOT / "examples" / "t3.good.txt"),
            "--tier", "3",
            "--icp", "Series-B SaaS",
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("# Proposition", result.stdout)
        self.assertIn("pipeline gap", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
