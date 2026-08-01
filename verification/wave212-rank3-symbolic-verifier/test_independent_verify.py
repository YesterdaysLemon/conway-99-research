#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import independent_verify


class IndependentVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = independent_verify.analyze()

    def test_common_lane(self):
        lane = self.result["common_neighbor"]
        self.assertEqual(lane["verdict"], "PASS / NO VETO")
        self.assertEqual([r["FD_satisfied"] for r in lane["controls"]], [499, 534, 532])
        self.assertEqual([r["quadratic_satisfied"] for r in lane["controls"]], [1256, 1259, 1299])
        self.assertTrue(all(r["target_zero_pairs"] == 104 and not r["target_zero_violations"] for r in lane["controls"]))

    def test_algebra_split_verdict(self):
        lane = self.result["quadratic_algebra"]
        self.assertEqual(lane["core_verdict"], "PASS / NO VETO")
        self.assertEqual(lane["allocation_statement_verdict"], "VETO / REFUTED")
        for row in lane["orbits"]:
            self.assertEqual(row["q_power_ranks"], [12, 8, 4, 2, 0])
            self.assertEqual(row["u_action_power_ranks"], [8, 4, 2, 0])
            derived = row["verifier_derived_allocation_pending_independent_promotion"]
            self.assertEqual(derived["conditional_D_power_ranks"], [52, 48, 44, 42, 40])
            self.assertEqual(derived["promotion_status"], "PENDING_INDEPENDENT_VERIFICATION")

    def test_hostile_mutations_and_manifests(self):
        self.assertTrue(self.result["common_neighbor"]["hostile_mutation_rejected"])
        self.assertTrue(self.result["quadratic_algebra"]["hostile_mutation_rejected"])
        self.assertTrue(all(row["exact_file_coverage"] for row in self.result["manifests"].values()))


if __name__ == "__main__":
    unittest.main()
