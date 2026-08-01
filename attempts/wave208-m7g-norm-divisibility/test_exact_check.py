#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exact_check  # noqa: E402


class ExactCheckTests(unittest.TestCase):
    def test_archived_result_replays(self) -> None:
        expected = json.loads(exact_check.RESULT.read_text(encoding="utf-8"))
        self.assertEqual(exact_check.build_result(), expected)

    def test_integer_lift_is_literal_plus_minus_one(self) -> None:
        self.assertEqual(exact_check.INTEGER_LIFT, (1, -1, 1, -1, 1, -1, -1, 1))
        self.assertEqual(sum(exact_check.INTEGER_LIFT), 0)

    def test_all_relative_sign_classes_are_retained(self) -> None:
        self.assertEqual(exact_check.linearizing_sign_classes(), exact_check.EXPECTED_SIGN_CLASSES)

    def test_polar_net_has_all_27_affine_forms(self) -> None:
        forms = exact_check.polar_forms()
        self.assertEqual(len(forms), 27)
        self.assertEqual(Counter(exact_check.rank_mod3(form) for _, form in forms), Counter({2: 12, 3: 8, 4: 6, 0: 1}))

    def test_exact_rank_remainder_distribution(self) -> None:
        result = exact_check.build_result()
        expected = {
            "rank0_K8_rem6": 1,
            "rank2_2K4_rem6": 12,
            "rank3_4K2_rem0": 1,
            "rank3_4K2_rem3": 1,
            "rank3_4K2_rem6": 6,
            "rank4_2C4_rem0": 3,
            "rank4_2C4_rem3": 3,
        }
        self.assertEqual(result["common_distribution"], expected)
        self.assertTrue(all(row["distribution"] == expected for row in result["classes"]))

    def test_survivor_types_and_counts(self) -> None:
        result = exact_check.build_result()
        for row in result["classes"]:
            survivors = row["surviving_forms"]
            self.assertEqual(len(survivors), 4)
            self.assertEqual(
                Counter((entry["rank"], entry["zero_graph"], entry["d"], entry["base_norm"]) for entry in survivors),
                Counter({(3, "4K2", 12, 216): 1, (4, "2C4", -24, 288): 3}),
            )

    def test_intersection_correction_cannot_change_remainder(self) -> None:
        for base in range(9):
            for s_value in (-28, -7, -1, 0, 1, 9, 28):
                self.assertEqual((base + 18 * s_value) % 9, base)

    def test_status_wall_is_explicit(self) -> None:
        result = exact_check.build_result()
        self.assertEqual(result["claim_label"], "DERIVED")
        self.assertEqual(result["global_status"], "UNKNOWN")
        self.assertIn("not graph constructions", result["limitations"][0])


if __name__ == "__main__":
    unittest.main()

