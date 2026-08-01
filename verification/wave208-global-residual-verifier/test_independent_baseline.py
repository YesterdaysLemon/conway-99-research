#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_baseline as blind  # noqa: E402


class BaselineTests(unittest.TestCase):
    def test_archived_baseline(self) -> None:
        expected = json.loads(blind.BASELINE.read_text(encoding="utf-8"))
        self.assertEqual(blind.build_result(), expected)

    def test_composition_lists_are_complete(self) -> None:
        expected_counts = {17: 6, 20: 7, 23: 8}
        for weight, count in expected_counts.items():
            self.assertEqual(len(blind.sign_compositions(weight)), count)

    def test_product_one_ambiguity(self) -> None:
        result = blind.build_result()["product_one_witnesses"]
        self.assertEqual(result["intersecting"]["product"], 1)
        self.assertEqual(result["disjoint_one_cross_edge"]["product"], 1)
        self.assertNotEqual(result["intersecting"]["kind"], result["disjoint_one_cross_edge"]["kind"])

    def test_outside_coordinate_is_not_optional(self) -> None:
        control = blind.build_result()["outside_scope_hostile_control"]
        self.assertTrue(control["inside_equation_zero"])
        self.assertFalse(control["full_equation_zero"])
        self.assertNotEqual(control["omitted_outside_coordinate"], 0)

    def test_fractional_or_bad_overlap_is_not_graphical(self) -> None:
        self.assertFalse(blind.graphical_overlap_gate([[Fraction(1, 2)]], [[1]]))
        self.assertFalse(blind.graphical_overlap_gate([[1, 1]], [[1, 2], [2, 1]]))
        self.assertTrue(blind.graphical_overlap_gate([[1, 1], [1, 0]], [[2, 1], [1, 1]]))

    def test_status_inflation_is_rejected(self) -> None:
        result = copy.deepcopy(blind.build_result())
        result["global_status"] = "NONEXISTENT"
        with self.assertRaises(AssertionError):
            blind.validate_terminal_status(result)

    def test_unknown_enumerator_coefficients_stay_unknown(self) -> None:
        result = blind.build_result()
        self.assertFalse(result["unknown_enumerator_coefficients_may_be_zeroed"])


if __name__ == "__main__":
    unittest.main()

