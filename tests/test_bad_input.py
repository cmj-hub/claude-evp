#!/usr/bin/env python3
"""Bad EVP JSON exits 2 and does not echo the document."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_evp.py"
PROBE = "super-secret-token"


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
        result = run(["--stdin"], stdin='{"evp": "' + PROBE)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(PROBE, result.stderr + result.stdout)

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

    def test_bulleted_text_file_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "variants.txt"
            path.write_text("- Variant A: ship 14 SQLs\n- Variant B: cut SDR cost\n", encoding="utf-8")
            result = run(["--file", str(path), "--tier", "3"])
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("a list of value props is not one proposition", result.stdout)

    def test_good_file_prints_one_proposition(self):
        result = run([
            "--file", str(ROOT / "examples" / "t3.good.txt"),
            "--tier", "3",
            "--icp", "Series-B SaaS",
        ])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("# Proposition", result.stdout)
        self.assertIn("pipeline gap", result.stdout.lower())

    def test_json_proposition_key(self):
        line = (ROOT / "examples" / "t3.good.txt").read_text(encoding="utf-8").strip()
        draft = json.dumps({"evp": line, "tier": 3, "icp": "Series-B SaaS"})
        result = run(["--stdin", "--format", "json"], stdin=draft)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["proposition"], line)

    def test_json_file_keeps_tier_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.json"
            path.write_text('{"evp": "' + PROBE + '", "tier": 9}', encoding="utf-8")
            result = run(["--file", str(path)])
        self.assertEqual(result.returncode, 2)
        self.assertIn("tier must be an integer 1-5", result.stderr)
        self.assertNotIn(PROBE, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
