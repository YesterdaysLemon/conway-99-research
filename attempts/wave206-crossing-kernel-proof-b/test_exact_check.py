"""Hostile and exact tests for the Wave 206 proof-B package."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("exact_check.py")
SPEC = importlib.util.spec_from_file_location("wave206_crossing", MODULE_PATH)
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class Wave206CrossingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = CHECK.analyze()
        CHECK.verify(cls.data)

    def test_frozen_inputs(self) -> None:
        self.assertEqual(CHECK.verify_inputs(), CHECK.EXPECTED_INPUTS)

    def test_twenty_one_star_coordinates_are_complete(self) -> None:
        star = self.data["star_coordinate_theorem"]
        self.assertEqual(star["coordinate_map_rank"], 21)
        self.assertEqual(star["J_star_rank"], 21)
        self.assertEqual(star["J_star_determinant"], 2)

    def test_characteristic_three_trace_zero_radical(self) -> None:
        star = self.data["star_coordinate_theorem"]
        self.assertEqual(star["trace_zero_dimension"], 20)
        self.assertEqual(star["trace_zero_restricted_rank"], 19)
        self.assertEqual(star["trace_zero_radical"], "span{I_6}")

    def test_ambient_nondegeneracy_does_not_remove_restricted_radical(self) -> None:
        hostile = self.data["star_coordinate_theorem"][
            "hostile_restricted_span"
        ]
        self.assertEqual(hostile["operator_span_rank"], 1)
        self.assertEqual(hostile["restricted_Gram_rank"], 0)

    def test_localizer_entries_reconstruct_the_compression(self) -> None:
        localizer = self.data["theorem_ledger"]["target_localizer_coordinates"]
        self.assertIn("determine P_y P_x P_y completely", localizer["reconstruction"])
        self.assertEqual(
            localizer["g_formula"], "g_xy=sum_e m_x^(y)[e]"
        )

    def test_crossing_toy_replays_all_global_identities(self) -> None:
        toy = self.data["crossing_toy"]
        self.assertEqual(toy["synthesis_rank"], 11)
        self.assertTrue(toy["D_square_zero"])
        self.assertTrue(toy["W_transpose_W_zero"])
        self.assertEqual(toy["W_rank"], toy["projector_span_rank"])
        self.assertTrue(toy["Gamma_equals_sum_fixed_middle_tau"])
        self.assertEqual(toy["tau_coordinate_formula_directly_checked_middles"], 3)

    def test_common_true_kernel_exceeds_incidence_dependencies(self) -> None:
        common = self.data["theorem_ledger"]["common_true_kernel"]
        self.assertEqual(common["dimension_lower_bound"], 34)
        self.assertEqual(common["inherited_incidence_dimension"], "17<=dim(L)<=33")
        self.assertEqual(
            common["new_quotient_lower_bound"],
            "dim(ker(mathcal P)/L)>=1",
        )
        self.assertIn("outside span{1_231}", common["nonconstant"])
        self.assertEqual(
            common["matrix_consequences"],
            ["D diag(a) D=0", "(D o D) a=0 from the diagonal entries"],
        )
        self.assertIn("R_0=R_1=R_2", common["three_class_balance"])

    def test_quadratic_relation_has_support_at_least_four(self) -> None:
        audit = self.data["veronese_short_relation_audit"]
        self.assertEqual(audit["projective_points_checked_in_PG_2_3"], 13)
        self.assertEqual(
            audit["minimum_rank_by_distinct_point_count"],
            {"1": 1, "2": 2, "3": 3},
        )
        self.assertIn(
            "wt(a)>=4",
            self.data["theorem_ledger"]["common_true_kernel"]["support_bound"],
        )

    def test_nonconstant_relation_is_not_the_global_frame_word(self) -> None:
        audit = self.data["nonconstant_pullback_audit"]
        self.assertEqual(
            audit["conclusion"], "im(B^T) intersect span{1_231}={0}"
        )
        self.assertTrue(
            all(
                case["contradiction"]
                for case in audit["nonzero_constant_cases"].values()
            )
        )

    def test_trace_class_centered_Gram_bound(self) -> None:
        trace_class = self.data["theorem_ledger"]["trace_class_consequence"]
        self.assertEqual(trace_class["centered_feature_dimension"], 20)
        self.assertEqual(trace_class["centered_trace_form_rank"], 19)
        self.assertEqual(trace_class["centered_Gram_rank_bound"], 19)
        self.assertIn("nullity>=8", trace_class["nonneighbor_pigeonhole"])

    def test_strong_control_separates_slice_and_global_ranks(self) -> None:
        control = self.data["strong_hostile_control"]
        self.assertEqual(control["projector_labels"], 99)
        self.assertEqual(control["distinct_projectors"], 96)
        self.assertTrue(control["sum_projectors_zero"])
        self.assertEqual(
            control["fixed_middle_tau_rank_distribution"], {"21": 99}
        )
        self.assertEqual(control["fourth_trace_matrix_rank"], 96)

    def test_strong_control_limitations_are_explicit(self) -> None:
        failures = self.data["strong_hostile_control"]["failed_target_premises"]
        self.assertTrue(any("231 shared" in item for item in failures))
        self.assertTrue(any("srg(99,14,1,2)" in item for item in failures))

    def test_hostile_status_inflation_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.data))
        mutated["conclusions"]["rank11_endpoint_excluded"] = True
        with self.assertRaises(AssertionError):
            CHECK.verify(mutated)

    def test_hostile_rank_mutation_is_rejected(self) -> None:
        mutated = json.loads(json.dumps(self.data))
        mutated["star_coordinate_theorem"]["J_star_rank"] = 20
        with self.assertRaises(AssertionError):
            CHECK.verify(mutated)


if __name__ == "__main__":
    unittest.main()
