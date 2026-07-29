"""Tests for the Wave 206 source-blind verifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("independent_verifier.py")
SPEC = importlib.util.spec_from_file_location("wave206_independent_verifier", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class SourceBlindVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = VERIFIER.analyze()

    def test_projector_control_and_zero_sum(self) -> None:
        self.assertTrue(self.result["all_projectors_self_adjoint_idempotent_rank_6"])
        self.assertTrue(self.result["zero_frame_sum"])
        self.assertEqual(self.result["center_count"], 99)
        self.assertFalse(self.result["scope"]["is_srg_incidence_configuration"])

    def test_seven_column_star_frame(self) -> None:
        self.assertTrue(self.result["star_columns_singular"])
        self.assertTrue(self.result["star_gram_is_E_minus_I"])
        self.assertEqual(self.result["star_gram_rank"], 6)
        self.assertTrue(self.result["star_relation_Z_one_zero"])
        self.assertTrue(self.result["middle_projector_equals_minus_ZZstar"])

    def test_fixed_middle_symmetry_and_diagonals(self) -> None:
        self.assertTrue(self.result["tensor_outer_symmetric"])
        self.assertTrue(self.result["tensor_diagonal_equals_h"])
        self.assertTrue(self.result["tensor_middle_column_equals_g"])

    def test_exact_contraction(self) -> None:
        self.assertTrue(self.result["tensor_contraction_all_rows_zero"])
        self.assertTrue(self.result["all_ones_is_true_feature_relation"])

    def test_six_space_compression_gram(self) -> None:
        self.assertTrue(self.result["tensor_equals_six_space_compression_gram"])
        self.assertTrue(self.result["compression_reconstruction_A_equals_ZKZstar"])

    def test_seven_star_gram_model(self) -> None:
        self.assertTrue(self.result["seven_star_matrices_symmetric"])
        self.assertTrue(self.result["seven_star_matrices_annihilate_one"])
        self.assertTrue(self.result["tensor_equals_seven_star_trace_gram"])

    def test_natural_21_coordinate_model(self) -> None:
        self.assertEqual(self.result["coordinate_dimension"], 21)
        self.assertTrue(self.result["coordinate_roundtrip"])
        self.assertEqual(self.result["coordinate_metric_rank"], 21)
        self.assertTrue(self.result["tensor_equals_21_coordinate_metric_gram"])
        self.assertLessEqual(self.result["control_tensor_rank"], 21)

    def test_characteristic_three_isotropic_not_radical(self) -> None:
        self.assertTrue(self.result["identity_coordinate_is_nonzero"])
        self.assertTrue(self.result["identity_coordinate_is_isotropic"])
        self.assertTrue(self.result["identity_coordinate_is_not_ambient_radical"])
        self.assertEqual(self.result["single_identity_feature_span_rank"], 1)
        self.assertEqual(self.result["single_identity_feature_gram_rank"], 0)

    def test_trace_zero_radical(self) -> None:
        self.assertEqual(self.result["trace_zero_subspace_dimension"], 20)
        self.assertEqual(self.result["trace_zero_restricted_metric_rank"], 19)
        self.assertEqual(self.result["trace_zero_restricted_radical_dimension"], 1)
        self.assertTrue(self.result["identity_lies_in_trace_zero_subspace"])
        self.assertTrue(self.result["identity_is_orthogonal_to_trace_zero_subspace"])

    def test_endpoint_scope_wall(self) -> None:
        self.assertFalse(self.result["scope"]["supports_endpoint_tau_classification"])
        self.assertEqual(self.result["status"]["Conway_99"], "UNKNOWN")
        self.assertEqual(self.result["status"]["rank_11_endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["n3_4158_endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["actual_nonedge_h"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
