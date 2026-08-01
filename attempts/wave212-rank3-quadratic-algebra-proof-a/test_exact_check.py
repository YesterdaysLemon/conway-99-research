#!/usr/bin/env python3
"""Stdlib tests for the Wave 212 proof-A exact replay."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exact_check


class ExactCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = exact_check.analyze()

    def test_mod_2_jordan_type_all_orbits(self):
        self.assertEqual([row["orbit_index"] for row in self.result["orbits"]], [0, 4, 29])
        for row in self.result["orbits"]:
            mod2 = row["mod_2_artin_schreier"]
            self.assertEqual(mod2["rank_F_transpose_F_powers_1_through_5"], [12, 8, 4, 2, 0])
            self.assertEqual(
                mod2["jordan_type_of_F_transpose_F"]["blocks_of_exact_size"],
                {"1": 69, "3": 2, "5": 2},
            )

    def test_projector_local_closure_all_orbits(self):
        for row in self.result["orbits"]:
            projector = row["K_projector_local_multiplicities"]
            self.assertEqual(
                (projector["trace_P_K"], projector["trace_E_3_on_K"], projector["trace_E_minus4_on_K"]),
                (71, 40, 31),
            )
            self.assertEqual(
                projector["two_by_two_PSD_pair_choices"],
                {
                    "both_0_and_1_allowed": 3570,
                    "forced_0": 0,
                    "forced_1": 0,
                    "neither_allowed": 0,
                },
            )

    def test_alternating_characteristic_polynomial_is_compatible(self):
        data = self.result["conditional_characteristic_polynomial_mod_2"]
        self.assertEqual(data["expanded_nonzero_degrees"], [85, 77, 53, 45])
        self.assertEqual(data["alternating_odd_order_form"], "x * (x^22 (x+1)^20)^2")

    def test_committed_results_are_exact_replay(self):
        committed = json.loads(exact_check.RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(committed, self.result)


if __name__ == "__main__":
    unittest.main()
