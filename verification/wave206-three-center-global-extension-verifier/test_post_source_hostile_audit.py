"""Tests for the independent audit of the released hostile/literature lane."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("post_source_hostile_audit.py")
SPEC = importlib.util.spec_from_file_location("wave206_post_source_hostile", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)


class PostSourceHostileAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = AUDITOR.analyze()

    def test_projector_pool_and_simplices(self) -> None:
        pool = self.result["projector_pool"]
        self.assertEqual(pool["count"], 34)
        self.assertEqual(pool["distinct_count"], 34)
        self.assertTrue(pool["all_rank_6"])
        self.assertTrue(pool["all_self_adjoint_idempotent"])
        self.assertTrue(pool["all_seven_simplices_valid"])

    def test_incidence_and_premise_failures(self) -> None:
        incidence = self.result["incidence"]
        self.assertEqual(incidence["connected_component_sizes"], [27, 36, 36])
        self.assertEqual(incidence["point_graph_edge_count"], 693)
        self.assertEqual(incidence["extra_graph_triangle_count"], 1098)
        self.assertNotEqual(incidence["edge_common_neighbor_distribution"], {"1": 693})
        self.assertIn("0", incidence["nonedge_common_neighbor_distribution"])

    def test_shared_realizations(self) -> None:
        for realization in self.result["realizations"].values():
            self.assertTrue(realization["star_projector_coupling"])
            self.assertTrue(realization["sum_projectors_zero"])
            self.assertTrue(realization["global_column_frame_zero"])
            self.assertEqual(realization["column_span_rank"], 11)
            self.assertEqual(realization["centered_gram_rank"], 11)
            self.assertTrue(realization["centered_gram_square_zero"])
            self.assertEqual(realization["distinct_projective_direction_count"], 19)

    def test_complete_pair_matrices_and_tau_collision(self) -> None:
        collision = self.result["collision"]
        self.assertTrue(collision["same_complete_labelled_g"])
        self.assertTrue(collision["same_complete_labelled_H"])
        self.assertEqual(collision["different_ordered_tau_entries"], 209952)
        self.assertTrue(collision["all_differences_cross_component"])
        self.assertFalse(collision["target_endpoint_counterexample"])

    def test_rank_21_controls(self) -> None:
        for control in self.result["rank21_controls"].values():
            self.assertEqual(control["unique_coordinate_rank"], 21)
            self.assertEqual(control["unique_slice_rank"], 21)
            self.assertEqual(control["full_slice_rank"], 21)
            self.assertTrue(control["seven_star_21_coordinate_model_used"])

    def test_mutations_are_rejected(self) -> None:
        self.assertTrue(all(self.result["mutations"].values()))

    def test_source_hypothesis_ledger(self) -> None:
        ledger = self.result["source_ledger"]
        self.assertEqual(ledger["ledger_entry_count"], 7)
        self.assertTrue(ledger["all_required_entries_present"])
        self.assertTrue(ledger["finite_frame_spanning_scope_retained"])
        self.assertTrue(ledger["real_positive_fusion_frame_scope_retained"])
        self.assertTrue(ledger["complex_design_angle_annihilator_scope_retained"])
        self.assertTrue(ledger["triple_regularity_extra_hypotheses_retained"])
        self.assertTrue(ledger["terwilliger_actual_graph_basepoint_scope_retained"])
        self.assertTrue(ledger["bounded_non_discovery_remains_UNKNOWN"])

    def test_frozen_result_and_status_wall(self) -> None:
        self.assertTrue(all(self.result["frozen_comparison"].values()))
        self.assertEqual(self.result["status"]["Conway-99"], "UNKNOWN")
        self.assertEqual(self.result["status"]["rank-11 endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["n3=4158 endpoint"], "UNKNOWN")
        self.assertEqual(self.result["status"]["Q>=7060"], "NOT PROVED")
        self.assertEqual(self.result["status"]["automorphism assumption"], "NONE")


if __name__ == "__main__":
    unittest.main()
