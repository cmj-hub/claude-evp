#!/usr/bin/env python3
"""Scorer CLI convention: --json, fix lines on exit 1, Next: line on every run."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_evp.py"
GOOD = ["--file", str(ROOT / "examples" / "t3.good.txt"), "--tier", "3", "--icp", "Series-B SaaS"]
BAD = ["--file", str(ROOT / "examples" / "t3.bad.txt"), "--tier", "3"]


def run(*args):
    return subprocess.run([sys.executable, str(SCORE), *args], capture_output=True, text=True)


class ScorerCli(unittest.TestCase):
    def test_json_flag_matches_format_json(self):
        a, b = run(*GOOD, "--json"), run(*GOOD, "--format", "json")
        self.assertEqual(a.returncode, 0)
        ja, jb = json.loads(a.stdout), json.loads(b.stdout)
        for key in ("total", "proposition", "next", "reasons"):
            self.assertEqual(ja[key], jb[key], key)

    def test_pass_names_next_suite_step(self):
        result = run(*GOOD)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip().splitlines()[-1], "Next: /cold-email:cold-email")
        data = json.loads(run(*GOOD, "--json").stdout)
        self.assertEqual(data["next"], "/cold-email:cold-email")
        self.assertEqual(data["reasons"], [])

    def test_fail_lines_say_what_to_change(self):
        result = run(*BAD)
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], "Next: fix the lines above and run this again.")
        fixes = [line for line in lines if line.startswith("- ")]
        self.assertTrue(fixes)
        for line in fixes:
            self.assertIn(" → ", line)
        data = json.loads(run(*BAD, "--json").stdout)
        self.assertEqual(len(data["reasons"]), len(data["fixes"]))
        self.assertTrue(data["next"].startswith("fix the lines above"))

    def test_list_refusal_says_what_to_change(self):
        result = run("--file", str(ROOT / "examples" / "value-props.json"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("→ pick one line", result.stdout)
        data = json.loads(run("--file", str(ROOT / "examples" / "value-props.json"), "--json").stdout)
        self.assertEqual(data["refusal"], "a list of value props is not one proposition")
        self.assertEqual(data["fixes"], ["pick one line and score that line alone"])

    def test_help_shows_example(self):
        self.assertIn("examples/t3.good.txt", run("--help").stdout)



class StableOutput(unittest.TestCase):
    def test_same_output_under_any_hash_seed(self):
        import os
        outs = set()
        for seed in ("1", "2", "3"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "score_evp.py"), '--file', 'examples/t3.bad.txt', '--tier', '3'],
                capture_output=True, text=True, cwd=ROOT, env=env,
            )
            outs.add(proc.stdout)
        self.assertEqual(len(outs), 1)

if __name__ == "__main__":
    unittest.main()
