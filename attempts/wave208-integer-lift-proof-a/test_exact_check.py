"""Unit tests for the Wave 208 proof-A exact checker."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("exact_check.py")
SPEC = importlib.util.spec_from_file_location("wave208_integer_lift_exact_check", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load exact_check.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class IntegerLiftTests(unittest.TestCase):
    def test_frozen_inputs(self) -> None:
        self.assertEqual(len(CHECK.verify_frozen_inputs()), 8)

    def test_spectral_split(self) -> None:
        result = CHECK.spectral_split_identities()
        self.assertEqual(result["Q_equation"], "A*Q=-4*Q")
        self.assertEqual(result["R_equation"], "A*R=3*R")

    def test_residue_shell_quantization(self) -> None:
        result = CHECK.residue_shell_rows()
        self.assertIn("17", result["weights"])
        self.assertIn("23", result["weights"])

    def test_balanced_shells(self) -> None:
        rows = CHECK.balanced_weight14_shells()["rows"]
        self.assertEqual([row["q_squared"] for row in rows], [70, 56, 42, 28, 14, 0])

    def test_zero_q_branch(self) -> None:
        result = CHECK.zero_q_three_eigen_branch()
        statuses = [row["status"] for row in result["rows"]]
        self.assertEqual(statuses.count("SURVIVES_THIS_ARGUMENT"), 1)

    def test_overlap_census(self) -> None:
        summary, records = CHECK.overlap_capacity_enumeration()
        self.assertEqual(summary["0"]["outside_token_capacity_survivors"], 651)
        self.assertEqual(summary["2"]["outside_token_capacity_survivors"], 0)
        self.assertEqual(len([r for r in records if r["same_overlap"] == 1]), 42)

    def test_same_overlap_one_coupling(self) -> None:
        _, records = CHECK.overlap_capacity_enumeration()
        result = CHECK.eliminate_same_overlap_one(records)
        self.assertEqual(result["status"], "EXCLUDED_BY_COUPLED_X_OR_Y_ENDPOINTS")

    def test_exclusive_shapes(self) -> None:
        result = CHECK.exclusive_graph_shapes()
        self.assertEqual(result["universal_bound"], [2, 4])
        self.assertEqual(result["k_3"]["labelled_C4_survivors"], 3)

    def test_hostile_partial_control(self) -> None:
        result = CHECK.hostile_partial_control()
        self.assertEqual(result["edge_count"], 52)
        self.assertTrue(result["pair_common_neighbor_caps_hold"])
        self.assertIn("NOT_A_COMPLETION", result["status"])

    def test_global_status_wall(self) -> None:
        result = CHECK.build_results()
        self.assertFalse(result["conclusions"]["balanced_weight14_excluded"])
        self.assertEqual(result["conclusions"]["conway_99"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()

