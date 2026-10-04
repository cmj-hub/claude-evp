"""brand-config.example.json: the `psp` and `evp` blocks match the suite contract and each other."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "brand-config.example.json").read_text())

PSP_KEYS = {"signal_anchors", "primary_pain", "timing_trigger", "felt_pain_role", "vocabulary"}
EVP_KEYS = {"tier", "primary", "outcome", "tradeoff", "proof"}
TIER_KEYS = {2: "tier_2_problem_aware", 3: "tier_3_solution_aware", 4: "tier_4_product_aware"}


class SharedBlocks(unittest.TestCase):
    def test_psp_shape(self):
        self.assertEqual(set(CONFIG["psp"]), PSP_KEYS)
        self.assertIsInstance(CONFIG["psp"]["signal_anchors"], list)
        self.assertIsInstance(CONFIG["psp"]["vocabulary"], list)

    def test_evp_shape(self):
        evp = CONFIG["evp"]
        self.assertEqual(set(evp), EVP_KEYS)
        self.assertIn(evp["tier"], range(1, 6))

    def test_evp_is_the_primary_outreach_draft(self):
        evp = CONFIG["evp"]
        self.assertEqual(evp["tier"], CONFIG["primary_outreach_tier"])
        draft = CONFIG["evp_drafts"][TIER_KEYS[evp["tier"]]]
        for key in ("primary", "outcome", "tradeoff", "proof"):
            with self.subTest(key=key):
                self.assertEqual(evp[key], draft[key])

    def test_evp_speaks_the_psp_vocabulary(self):
        line = CONFIG["evp"]["primary"].lower()
        self.assertTrue(any(v.lower() in line for v in CONFIG["psp"]["vocabulary"]))


if __name__ == "__main__":
    unittest.main()
