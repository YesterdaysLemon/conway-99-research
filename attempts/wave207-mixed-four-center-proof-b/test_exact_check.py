"""Tests for the Wave 207 mixed four-center symbolic checker."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "wave207_mixed_four_center_exact_check", HERE / "exact_check.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load exact checker")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class MixedFourCenterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((HERE / "exact-results.json").read_text("utf-8"))

    def test_replay_matches_frozen_json(self) -> None:
        self.assertEqual(self.data, CHECK.build_results())

    def test_transition_rank_formula(self) -> None:
        table = self.data["transition_rank_audit"]["cross_rank_table"]
        for rank in range(7):
            self.assertEqual(
                table[str(rank)]["transition_rank"], rank * (rank + 1) // 2
            )
        self.assertEqual(
            self.data["transition_rank_audit"]["same_center_J_star_rank"],
            21,
        )
        self.assertEqual(
            self.data["transition_rank_audit"][
                "same_center_J_star_determinant"
            ],
            2,
        )

    def test_characteristic_three_radical(self) -> None:
        audit = self.data["characteristic_three_radical_audit"]
        self.assertEqual(audit["trace_zero_feature_synthesis_rank"], 20)
        self.assertEqual(audit["trace_zero_feature_gram_rank"], 19)
        self.assertEqual(audit["trace_zero_radical"], "span{I_6}")
        self.assertEqual(audit["gram_nullity_minus_true_relation_nullity"], 1)
        self.assertTrue(
            audit["adding_one_trace_nonzero_feature"][
                "identity_radical_is_detected"
            ]
        )

    def test_four_center_certificate(self) -> None:
        audit = self.data["four_center_certificate_audit"]
        self.assertEqual(
            audit["cumulative_symmetric_square_span_ranks"], [21, 41, 56, 66]
        )
        self.assertEqual(audit["two_additional_center_restriction_rank_on_K"], 25)
        self.assertTrue(audit["four_center_symmetric_square_span_is_full"])
        self.assertTrue(
            audit["irreducibility_rabin_checks"]["irreducible"]
        )
        self.assertEqual(audit["local_standard_form_gram_ranks"], [6, 6, 6, 6])

    def test_scope_wall(self) -> None:
        conclusions = self.data["conclusions"]
        self.assertFalse(conclusions["rank_66_certificate_established_for_endpoint"])
        self.assertFalse(conclusions["rank_11_endpoint_excluded"])
        self.assertFalse(conclusions["conway_99_resolved"])
        self.assertEqual(conclusions["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
