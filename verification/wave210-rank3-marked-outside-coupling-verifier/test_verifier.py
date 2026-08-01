#!/usr/bin/env python3
"""Fast regression and hostile checks for the sealed verifier artifacts."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import independent_check as independent
import post_source_audit as post


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Wave210IndependentVerifierTests(unittest.TestCase):
    def test_pre_source_seal(self) -> None:
        for digest, relative in post.parse_manifest_text(
            (HERE / "pre-source-comparison-seal.sha256").read_text(encoding="utf-8")
        ):
            self.assertEqual(sha256(HERE / relative), digest)

    def test_independent_counts_and_scope(self) -> None:
        payload = json.loads((HERE / "independent-results.json").read_text(encoding="utf-8"))
        self.assertTrue(independent.validate_summary(payload))
        self.assertEqual(payload["surviving_case_orbits"], [0, 4, 29])
        self.assertEqual(payload["F_audit"]["common_gram_rank_over_Q"], 13)
        self.assertEqual(
            payload["base_local_one_factor"]["configurations_feasible_at_all_14_support_vertices"],
            4480,
        )
        self.assertFalse(payload["outside_block_D"]["constructed"])
        self.assertFalse(payload["outside_block_D"]["excluded"])
        self.assertEqual(payload["global_status"], "UNKNOWN")

    def test_complete_set_digests_and_post_source_verdict(self) -> None:
        payload = json.loads((HERE / "post-source-audit.json").read_text(encoding="utf-8"))
        comparison = payload["complete_set_comparison"]
        self.assertEqual(payload["verdict"], "PASS / NO VETO")
        self.assertEqual(comparison["digests"]["H"]["count"], 204)
        self.assertEqual(comparison["digests"]["cases"]["count"], 20_928)
        self.assertEqual(comparison["digests"]["surviving_H"]["count"], 96)
        self.assertEqual(comparison["digests"]["surviving_cases"]["count"], 1_536)
        self.assertEqual(comparison["digests"]["surviving_triples"]["count"], 55_296)
        self.assertTrue(comparison["all_55296_surviving_labelled_triples_equal"])

    def test_hostile_mutations_are_sealed_as_rejected(self) -> None:
        independent_hostile = json.loads(
            (HERE / "independent-hostile-tests.json").read_text(encoding="utf-8")
        )
        post_payload = json.loads((HERE / "post-source-audit.json").read_text(encoding="utf-8"))
        self.assertTrue(independent_hostile["all_hostile_controls_rejected"])
        self.assertTrue(all(independent_hostile["checks"].values()))
        self.assertTrue(
            post_payload["manifest_audit"]["in_memory_manifest_corruption_rejected"]
        )
        self.assertTrue(
            post_payload["hostile_control_audit"]["mandatory_triangle_edge_deletion_rejected"]
        )

    def test_outer_manifest_live(self) -> None:
        source = post.load_source()
        audit = post.validate_manifests(source)
        self.assertEqual(audit["observed_outer_manifest_sha256"], post.EXPECTED_OUTER_SHA256)
        self.assertTrue(audit["all_outer_manifest_entries_valid"])

    def test_live_quick_hostile_F_mutation(self) -> None:
        matching = independent.deficit_configurations()[0][0]
        built = independent.columns_for_matching(matching)
        self.assertIsNotNone(built)
        columns = list(built[0])
        columns[0] ^= columns[0] & -columns[0]
        self.assertNotEqual(independent.observed_gram(tuple(columns)), independent.GRAM)

    def test_all_deficit_bijections_closed_under_all_induced_support_actions(self) -> None:
        valid = set(independent.deficit_configurations()[0])
        # Line permutations do not act on F; the 768 case actions induce only
        # 32 distinct support actions (4 x 4, with or without sign swap).
        support_actions = {
            action[1] for action in independent.full_case_group()
        }
        self.assertEqual(len(support_actions), 32)
        identity_lines = tuple(range(8))
        for matching in valid:
            for support_map in support_actions:
                transformed = independent.transform_matching(
                    matching, (identity_lines, support_map)
                )
                self.assertIn(transformed, valid)


if __name__ == "__main__":
    unittest.main()
