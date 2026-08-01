#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_baseline as blind  # noqa: E402
import independent_m7g_norm as check  # noqa: E402


class M7gNormTests(unittest.TestCase):
    def test_archived_reconstruction(self) -> None:
        expected = json.loads(check.RESULT.read_text(encoding="utf-8"))
        self.assertEqual(check.build_result(), expected)

    def test_four_orientations_and_all_affine_forms(self) -> None:
        result = check.build_result()
        self.assertEqual(result["relative_orientation_count"], 4)
        self.assertEqual(result["affine_forms_per_orientation"], 27)
        self.assertEqual(len(result["orientation_classes"]), 4)

    def test_integer_lift_is_balanced_plus_minus_one(self) -> None:
        self.assertEqual(check.INTEGER_LIFT.count(1), 4)
        self.assertEqual(check.INTEGER_LIFT.count(-1), 4)
        self.assertNotIn(2, check.INTEGER_LIFT)

    def test_product_one_ambiguity_remains(self) -> None:
        result = check.build_result()
        self.assertFalse(result["product_one_interpretation_fixed"])
        self.assertTrue(
            all(
                survivor["product_one_pairs"] > 0
                for orientation in result["orientation_classes"]
                for survivor in orientation["survivors"]
            )
        )
        baseline = blind.build_result()["product_one_witnesses"]
        self.assertEqual(baseline["intersecting"]["product"], 1)
        self.assertEqual(baseline["disjoint_one_cross_edge"]["product"], 1)

    def test_status_inflation_rejected(self) -> None:
        result = copy.deepcopy(check.build_result())
        result["global_status"] = "NONEXISTENT"
        with self.assertRaises(AssertionError):
            blind.validate_terminal_status(result)


if __name__ == "__main__":
    unittest.main()
