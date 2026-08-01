"""Tests for the Wave 206 tensor-balance weight addendum."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("exact_check.py")
SPEC = importlib.util.spec_from_file_location("wave206_tensor_weight", MODULE_PATH)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class Wave206TensorWeightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = CHECK.analyze()
        CHECK.verify(cls.data)

    def test_frozen_inputs(self) -> None:
        self.assertEqual(CHECK.verify_inputs(), CHECK.EXPECTED_INPUTS)

    def test_operator_form_is_removed_only_by_ambient_invertibility(self) -> None:
        transfer = self.data["operator_to_coefficient_form"]
        self.assertEqual(transfer["ordinary_tensor_equation"], "V Lambda V^T=0")
        self.assertIn("F^{-1}", transfer["ambient_form_step"])
        self.assertIn("need not be nondegenerate", transfer["support_span_step"])

    def test_witt_bound_uses_nondegenerate_coefficient_form(self) -> None:
        witt = self.data["witt_audit"]
        self.assertTrue(witt["nondegenerate"])
        self.assertIn("rank(V)<=WittIndex", witt["row_space_consequence"])
        for dimension, rows in witt["exact_diagonal_form_table"].items():
            self.assertTrue(
                all(row["witt_index"] <= int(dimension) // 2 for row in rows)
            )

    def test_small_cap_maxima_are_exact(self) -> None:
        caps = self.data["cap_audit"]["exact_exhaustion"]
        self.assertEqual(
            [caps[str(rank)]["maximum_no_three_collinear"] for rank in (1, 2, 3)],
            [1, 2, 4],
        )
        self.assertEqual(caps["3"]["projective_points"], 13)

    def test_every_support_at_most_seven_is_excluded(self) -> None:
        exclusion = self.data["small_support_exclusion"]
        self.assertTrue(all(row["excluded"] for row in exclusion["cases"]))
        self.assertEqual(
            exclusion["conclusion"],
            "every nonzero tensor-balance word has weight at least eight",
        )

    def test_weight_eight_control_saturates_witt_bound(self) -> None:
        control = self.data["weight_eight_control"]
        self.assertEqual(control["support_size"], 8)
        self.assertEqual(control["span_rank"], 4)
        self.assertEqual(control["coefficient_form_witt_index"], 4)
        self.assertTrue(control["tensor_sum_zero"])

    def test_weight_eight_boundary_forces_even_coefficient_composition(self) -> None:
        boundary = self.data["weight_eight_boundary"]
        self.assertEqual(boundary["forced_span_rank"], 4)
        self.assertEqual(
            boundary["allowed_number_of_coefficient_2_entries"],
            [0, 2, 4, 6, 8],
        )

    def test_weight_eight_control_retains_local_endpoint_geometry(self) -> None:
        control = self.data["weight_eight_control"]
        self.assertTrue(control["projectively_distinct"])
        self.assertTrue(control["every_three_columns_independent"])
        self.assertTrue(control["all_support_columns_singular"])
        self.assertEqual(control["ambient_dimension"], 11)
        self.assertEqual(control["ambient_form_determinant"], 2)

    def test_weight_eight_control_limitations_are_explicit(self) -> None:
        failures = self.data["weight_eight_control"]["failed_endpoint_premises"]
        self.assertTrue(any("231-column" in item for item in failures))
        self.assertTrue(any("im(B^T)" in item for item in failures))

    def test_hostile_weight_nine_promotion_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.data))
        mutated["conclusions"]["weight_nine_lower_bound_proved"] = True
        with self.assertRaises(AssertionError):
            CHECK.verify(mutated)

    def test_hostile_endpoint_promotion_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.data))
        mutated["conclusions"]["rank11_endpoint_excluded"] = True
        with self.assertRaises(AssertionError):
            CHECK.verify(mutated)


if __name__ == "__main__":
    unittest.main()
