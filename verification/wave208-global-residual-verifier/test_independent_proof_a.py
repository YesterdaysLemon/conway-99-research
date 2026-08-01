#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_proof_a as independent  # noqa: E402
import post_source_proof_a_audit as audit  # noqa: E402


class IndependentProofATests(unittest.TestCase):
    def test_independent_archive_replays(self) -> None:
        expected = json.loads(independent.ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(independent.build_result(), expected)

    def test_post_source_archive_replays(self) -> None:
        expected = json.loads(audit.ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(audit.build_result(), expected)

    def test_full_residue_table_matches_source(self) -> None:
        source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        self.assertEqual(
            independent.residue_shell_table(),
            source["residue_shell_quantization"]["weights"],
        )

    def test_fano_census_and_alpha_one_coupling(self) -> None:
        result = independent.build_result()["norm14_overlap"]
        self.assertEqual(result["capacity"]["1"]["outside_token_capacity_survivors"], 42)
        self.assertTrue(result["alpha_one_excluded"])
        self.assertGreater(result["alpha_one_required_endpoints"], result["alpha_one_maximum_other_side_endpoints"])
        self.assertEqual(result["derived"]["same_sign_overlap"], 0)
        self.assertEqual(result["derived"]["opposite_sign_overlap"], 6)

    def test_q_zero_one_cross_edge_survives(self) -> None:
        result = independent.zero_q_branch()
        survivors = [row for row in result["rows"] if row["status"] == "SURVIVES_THIS_ARGUMENT"]
        self.assertEqual(len(survivors), 1)
        self.assertEqual(survivors[0]["cross_edges"], 1)

    def test_partial_control_does_not_imply_outside_equations(self) -> None:
        result = independent.replay_partial_control()
        self.assertTrue(result["hostile_extension_preserves_upper_caps"])
        self.assertNotEqual(result["hostile_outside_Ax_residual"], 0)
        self.assertFalse(result["full_outside_equations_implied"])
        self.assertFalse(result["global_completion_implied"])

    def test_mutated_alpha_conclusion_is_rejected(self) -> None:
        source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        clean = json.loads(audit.INDEPENDENT_RESULT.read_text(encoding="utf-8"))
        mutant = copy.deepcopy(source)
        mutant["balanced_weight14"]["derived_overlap_conclusion"]["same_sign_overlap"] = 1
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, clean)

    def test_weight_or_status_promotion_is_rejected(self) -> None:
        source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        clean = json.loads(audit.INDEPENDENT_RESULT.read_text(encoding="utf-8"))
        mutant = copy.deepcopy(source)
        mutant["conclusions"]["balanced_weight14_excluded"] = True
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, clean)


if __name__ == "__main__":
    unittest.main()
