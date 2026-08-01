#!/usr/bin/env python3
"""Tests for the post-source Wave 209 delta audit."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import post_source_audit as audit  # noqa: E402


class PostSourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.build_post_source_result()

    def test_sealed_manifest(self) -> None:
        manifest = self.result["source_manifest"]
        self.assertEqual(
            manifest["outer_sha256"],
            "521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1",
        )
        self.assertEqual(manifest["entries_checked"], 10)

    def test_complete_result_sets_match(self) -> None:
        comparisons = self.result["comparisons"]
        self.assertTrue(comparisons["weight20_aggregate_352"]["full_set_equal"])
        self.assertTrue(comparisons["weight14_marked_subsets"]["full_set_equal"])
        self.assertTrue(comparisons["weight20_m2_lower_bounds"]["all_66_labelled_bounds_equal"])
        self.assertEqual(comparisons["aggregate_shells"]["7"]["rows"], 5)
        self.assertEqual(comparisons["aggregate_shells"]["10"]["rows"], 425)

    def test_deficit_and_line_witness_delta(self) -> None:
        comparisons = self.result["comparisons"]
        self.assertTrue(comparisons["weight14_deficit_bijections"]["residual_profiles_equal"])
        self.assertTrue(comparisons["line_type_witnesses"]["all_source_witnesses_independently_replayed"])

    def test_six_row_narrowing_is_explicit_not_silent(self) -> None:
        finding = self.result["findings"]["post_aggregate_selected_line_degree_cap"]
        self.assertEqual(finding["claim_label"], "DERIVED")
        self.assertEqual(finding["aggregate_rows_removed"], 6)
        self.assertEqual(finding["combined_remaining_rows"], 346)
        self.assertTrue(finding["promotion_status"].startswith("requires"))
        for row in finding["removed_rows"]:
            self.assertEqual(row["x"], 4)
            self.assertTrue(
                row["plus_cross_degree_histogram"][4]
                or row["minus_cross_degree_histogram"][4]
            )

    def test_upstream_audit_hash_delta_is_pinned(self) -> None:
        public_audit = audit.ROOT / "verification" / "2026-07-31-wave208-integration-audit.md"
        current = hashlib.sha256(public_audit.read_bytes()).hexdigest()
        self.assertEqual(current, "eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754")
        original_freeze = (HERE / "input-freeze.sha256").read_text(encoding="utf-8")
        post_freeze = (HERE / "post-freeze-inputs.sha256").read_text(encoding="utf-8")
        self.assertIn("61b3279f9c48cf3b72755ce047cdb8b30a3125596452c7fa5ff72bd8ed3548e8", original_freeze)
        self.assertIn(current, post_freeze)

    def test_unknown_wall_survives(self) -> None:
        self.assertEqual(self.result["source_global_status"], "UNKNOWN")
        walls = self.result["scope_walls"]
        self.assertEqual(walls["conway_99_status"], "UNKNOWN")
        self.assertFalse(walls["aggregate_or_combined_rows_are_graphs"])
        self.assertFalse(walls["complete_nonexistence_certificate"])


if __name__ == "__main__":
    unittest.main()
