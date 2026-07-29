"""Tests for the independent post-source Wave 206 Proof-B audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("post_source_proof_b_audit.py")
SPEC = importlib.util.spec_from_file_location("wave206_post_source_proof_b", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


class PostSourceProofBAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = AUDITOR.analyze()

    def test_source_integrity(self) -> None:
        integrity = self.result["source_integrity"]
        self.assertTrue(integrity["proof_b"]["all_entries_match"])
        self.assertEqual(integrity["proof_b"]["entry_count"], 10)
        self.assertTrue(integrity["weight_addendum"]["all_entries_match"])
        self.assertEqual(integrity["weight_addendum"]["entry_count"], 11)
        self.assertTrue(integrity["wave174"]["all_entries_match"])
        self.assertTrue(integrity["blind_files_unchanged"])

    def test_crossing_feature(self) -> None:
        crossing = self.result["crossing_and_localizer"]
        self.assertEqual(crossing["synthesis_rank"], 11)
        self.assertTrue(crossing["D_square_zero"])
        self.assertEqual(crossing["each_M_rank"], 6)
        self.assertEqual(crossing["W_rank"], crossing["projector_span_rank"])
        self.assertTrue(crossing["W_transpose_W_zero"])

    def test_localizer_coordinates_and_signs(self) -> None:
        crossing = self.result["crossing_and_localizer"]
        self.assertEqual(crossing["J_star_rank"], 21)
        self.assertTrue(crossing["J_star_equals_edge_incidence_gram_plus_2I"])
        self.assertEqual(crossing["localizer_sign_checks"], 24 * 24)
        self.assertEqual(crossing["g_formula"], "g_xy=sum_e m_x^(y)[e]")

    def test_gamma_identities(self) -> None:
        crossing = self.result["crossing_and_localizer"]
        self.assertTrue(crossing["Gamma_equals_sum_fixed_middle_tau"])
        self.assertTrue(crossing["Gamma_diagonal_equals_H_row_sum"])
        self.assertTrue(crossing["Gamma_row_sum_zero"])
        self.assertGreater(crossing["Gamma_rank"], 0)
        self.assertLessEqual(crossing["Gamma_rank"], crossing["W_rank"])

    def test_true_kernel_quotient(self) -> None:
        quotient = self.result["true_kernel_quotient"]
        self.assertEqual(quotient["inherited_rank_B_interval"], [66, 82])
        self.assertEqual(quotient["inherited_dim_L_interval"], [17, 33])
        self.assertEqual(quotient["projector_span_upper_bound"], 65)
        self.assertEqual(quotient["dim_KP_lower_bound"], 34)
        self.assertEqual(quotient["dim_A_Delta_lower_bound"], 1)
        self.assertTrue(quotient["map_ledger"]["L_contained_in_KP"])
        self.assertIn("iff", quotient["map_ledger"]["Theta_equivalence"])

    def test_nonconstant_pullback(self) -> None:
        audit = self.result["nonconstant_and_three_class_balance"]
        self.assertEqual(audit["im_Bt_intersects_constant_line"], "zero only")
        for scalar, row in audit["nonzero_constant_cases"].items():
            self.assertEqual(row["forced_sum_c"], 0)
            self.assertEqual(row["G_times_Gc"], 0)
            self.assertEqual(row["G_minus_J_times_c"], int(scalar))
            self.assertTrue(row["contradiction"])

    def test_three_class_balance(self) -> None:
        audit = self.result["nonconstant_and_three_class_balance"]
        self.assertEqual(audit["class_balance"], "R_0=R_1=R_2")
        self.assertIn("not equality of class sizes", audit["interpretation_guard"])

    def test_support_strengthened_to_eight(self) -> None:
        support = self.result["tensor_support"]
        self.assertEqual(support["submitted_bound"], 4)
        self.assertEqual(support["verified_strengthened_bound"], 8)
        self.assertTrue(support["coefficient_metric_nondegenerate"])
        self.assertTrue(support["totally_isotropic_row_space"])
        maxima = support["projective_cap_enumeration"]
        self.assertEqual(
            {dimension: row["maximum_no_dependent_triple_subset"]
             for dimension, row in maxima.items()},
            {"1": 1, "2": 2, "3": 4},
        )
        self.assertEqual(maxima["3"]["number_of_maximum_subsets"], 234)
        self.assertTrue(all(row["excluded"] for row in support["support_exclusions"].values()))

    def test_weight_eight_boundary_and_relaxed_control(self) -> None:
        support = self.result["tensor_support"]
        boundary = support["weight_eight_boundary"]
        self.assertEqual(boundary["forced_span_rank"], 4)
        self.assertTrue(boundary["coefficient_form_must_be_split"])
        self.assertEqual(
            boundary["allowed_number_of_coefficient_2_entries"],
            [0, 2, 4, 6, 8],
        )
        control = support["weight_eight_relaxed_control"]
        self.assertEqual(control["support_size"], 8)
        self.assertEqual(control["span_rank"], 4)
        self.assertTrue(control["every_three_columns_independent"])
        self.assertTrue(control["all_columns_singular"])
        self.assertTrue(control["tensor_and_operator_sum_zero"])
        self.assertFalse(control["proves_target_weight_eight_word_exists"])
        self.assertTrue(control["blocks_weight_nine_from_local_ingredients_alone"])

    def test_common_kernel_is_true_operator_kernel(self) -> None:
        common = self.result["common_true_kernel"]
        self.assertTrue(common["contained_in_every_fixed_middle_kernel"])
        self.assertTrue(common["contained_in_Gamma_kernel"])
        self.assertIn("operator equality", common["true_relation_guard"])

    def test_scope_wall(self) -> None:
        scope = self.result["scope_wall"]
        self.assertFalse(scope["fixed_middle_trace_class_nullities_are_true_relations"])
        self.assertEqual(scope["trace_class_nullity_kind"], "Gram only unless radical controlled")
        self.assertFalse(scope["rank11_endpoint_excluded"])
        self.assertFalse(scope["n3_improved"])
        self.assertFalse(scope["Conway_99_resolved"])
        self.assertEqual(scope["endpoint_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
