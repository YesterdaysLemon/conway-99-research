#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_proof_b as independent  # noqa: E402
import post_source_proof_b_audit as audit  # noqa: E402


class IndependentProofBTests(unittest.TestCase):
    def test_independent_archive_replays(self) -> None:
        expected = json.loads(independent.ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(independent.build_result(), expected)

    def test_post_source_archive_replays(self) -> None:
        expected = json.loads(audit.ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(audit.build_result(), expected)

    def test_linear_tensor_and_matching_objects_are_distinct(self) -> None:
        result = independent.build_result()
        self.assertEqual(result["projective_linear_weight_eight_relation_classes"], 4)
        self.assertEqual(result["projective_tensor_weight_eight_relation_classes"], 1)
        self.assertEqual(result["concurrent_secant_matching_count"], 4)
        self.assertFalse(result["relation_matching_objects_identified"])

    def test_all_marked_counts_and_rank3_weights(self) -> None:
        result = independent.build_result()
        self.assertEqual(sum(result["minus24_intersection_profiles"].values()), 83)
        self.assertEqual(result["plus12_coarse_profile"], {
            "same0_opposite2_w20_m2": 66,
            "same0_opposite5_w14_m5": 792,
        })

    def test_outside_equation_and_completion_are_not_implied(self) -> None:
        result = independent.build_result()
        for control in result["local_controls"]:
            self.assertNotEqual(control["hostile_outside_row_dot_b"], 0)
            self.assertTrue(control["hostile_extension_preserves_upper_caps"])
            self.assertFalse(control["full_outside_equation_implied"])
            self.assertFalse(control["global_completion_implied"])

    def test_mutated_subset_count_is_rejected(self) -> None:
        source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        clean = json.loads(audit.INDEPENDENT_RESULT.read_text(encoding="utf-8"))
        mutant = copy.deepcopy(source)
        mutant["plus12_intersection_profiles"]["m2_same0_opposite2_w20_p10_n10_norm20"] = 65
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, clean)

    def test_status_promotion_is_rejected(self) -> None:
        source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        clean = json.loads(audit.INDEPENDENT_RESULT.read_text(encoding="utf-8"))
        mutant = copy.deepcopy(source)
        mutant["claim_label"] = "VERIFIED"
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, clean)


if __name__ == "__main__":
    unittest.main()
