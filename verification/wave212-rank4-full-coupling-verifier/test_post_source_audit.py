from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave212_post_source_tests_target", HERE / "post_source_audit.py")
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class Wave212RankFourFullCouplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = json.loads(AUDIT.RESULTS.read_text(encoding="utf-8"))

    def test_blind_and_source_manifests_still_match(self) -> None:
        checked = AUDIT.verify_seals()
        self.assertEqual(checked["blind_input_entries"], 7)
        self.assertEqual(checked["blind_output_entries"], 3)
        self.assertEqual(checked["source_manifest_entries"], 12)

    def test_all_filtered_matrix_dimensions_are_archived(self) -> None:
        systems = self.result["membership_filtered_source_comparison"]["systems"]
        self.assertEqual([row["orbit_id"] for row in systems], [0, 2, 4, 11, 12, 14, 23])
        self.assertEqual(
            [row["row_count"] for row in systems],
            [1266, 1530, 1442, 1442, 1354, 1398, 1266],
        )
        self.assertEqual(
            [row["w_column_count"] for row in systems],
            [12110, 11444, 11672, 11672, 11888, 12003, 12110],
        )
        self.assertTrue(all(row["complete_source_matrix_match"] for row in systems))

    def test_archived_duals_and_all_labelled_transports_are_exact(self) -> None:
        replay = self.result["archived_integer_dual_replay"]
        self.assertTrue(replay["all_exact_integer_replays"])
        self.assertEqual(
            [row["rhs"] for row in replay["certificates"]],
            [-4, -239020, -18, -18, -239020, -3240, -4],
        )
        self.assertEqual(self.result["transport"]["transported_branch_checks"], 51)
        self.assertEqual(self.result["transport"]["transported_dual_replays"], 51)
        self.assertEqual(self.result["transport"]["transported_local_pattern_checks"], 601377)
        self.assertFalse(self.result["transport"]["target_automorphism_assumed"])

    def test_relaxation_embedding_and_hostile_controls_are_retained(self) -> None:
        self.assertTrue(self.result["relaxation_inclusion"]["larger_system_is_a_necessary_relaxation"])
        self.assertTrue(all(self.result["hostile_tests"].values()))

    def test_scope_wall(self) -> None:
        self.assertEqual(self.result["claim_label"], "VERIFIED")
        self.assertEqual(self.result["verdict"], "PASS_NO_VETO")
        self.assertEqual(self.result["rank_three_status"], "UNKNOWN")
        self.assertEqual(self.result["global_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
