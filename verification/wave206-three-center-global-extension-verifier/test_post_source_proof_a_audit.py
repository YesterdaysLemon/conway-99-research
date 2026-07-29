"""Tests for the independent post-source Wave 206 Proof-A audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("post_source_proof_a_audit.py")
SPEC = importlib.util.spec_from_file_location("wave206_post_source_proof_a", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


class PostSourceProofAAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = AUDITOR.analyze()

    def test_offdiagonal_21_coordinate_model(self) -> None:
        model = self.result["fixed_y_operator_and_coordinate_model"]
        self.assertEqual(model["coordinate_dimension"], 21)
        self.assertEqual(model["offdiagonal_coordinate_metric_rank"], 21)
        self.assertTrue(model["weighted_relation_requires_genuine_operator_relation"])
        self.assertTrue(model["gram_kernel_word_alone_is_not_accepted"])
        for control in model["controls"].values():
            self.assertEqual(control["g"], 2 * control["coordinate_sum_mod_3"] % 3)
            self.assertEqual(control["h"], control["quadratic_value"])

    def test_fiber_matching_lemma(self) -> None:
        graph = self.result["graph_patterns_and_fibers"]
        self.assertEqual(graph["fiber_count"], 21)
        self.assertEqual(graph["total_nonneighbors_partitioned"], 84)
        self.assertEqual(graph["possible_induced_fiber_graph_count"], 4)
        self.assertTrue(graph["representative_forbidden_edge_forces_induced_triangular_prism"])

    def test_edge_census(self) -> None:
        edge = self.result["edge_module_census"]
        self.assertEqual(edge["labelled_degree_two_biadjacency_matrices"], 67_950)
        self.assertEqual(edge["unique_compressions"], 130)
        self.assertEqual(
            edge["profile_rank_g_h"],
            {"3,0,0": 15, "4,0,0": 60, "4,0,1": 45, "6,0,0": 10},
        )

    def test_marked_low_t_census(self) -> None:
        census = self.result["marked_coordinate_low_t_census"]
        self.assertEqual(census["6"]["counts_by_h_and_r"], {"1,1": 18})
        self.assertEqual(
            census["7"]["counts_by_h_and_r"],
            {"0,0": 288, "0,1": 9, "1,0": 144, "1,1": 180, "2,0": 144},
        )

    def test_marginal_residues_and_scalar_ledgers(self) -> None:
        for ledger in self.result["marginal_tau_and_scalar_ledgers"].values():
            self.assertEqual(ledger["ledger_entry_count"], 97)
            self.assertEqual(ledger["ledger_sum"], ledger["required_sum"])
            self.assertTrue(
                all(values == [0, 1, 2] for values in ledger["edge_values_by_block"].values())
            )
            self.assertTrue(
                all(values == [0, 1, 2] for values in ledger["nonedge_values_by_pair"].values())
            )

    def test_formal_operator_controls_are_scoped(self) -> None:
        for control in self.result["formal_zero_sum_operator_controls"].values():
            self.assertEqual(control["operator_count"], 99)
            self.assertTrue(control["operator_sum_zero"])
            self.assertLessEqual(control["tau_gram_rank"], 21)
            self.assertFalse(control["residual_graph_derived"])

    def test_missing_xz_pair_scope_gate(self) -> None:
        scope = self.result["scope_correction"]
        self.assertFalse(scope["x_z_pair_module_imposed"])
        self.assertEqual(scope["full_labelled_three_center_graph_type_determines_tau"], "UNKNOWN")
        self.assertEqual(scope["simultaneous_shared_operator_completion"], "UNKNOWN")
        self.assertFalse(scope["shared_231_column_realization"])
        self.assertEqual(scope["t_at_least_8_modules"], "UNTESTED")

    def test_frozen_comparison_and_status(self) -> None:
        self.assertTrue(all(self.result["frozen_comparison"].values()))
        self.assertEqual(self.result["status"]["Conway-99"], "UNKNOWN")
        self.assertEqual(self.result["status"]["rank-11 endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["n3=4158 endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["actual nonedge h"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
