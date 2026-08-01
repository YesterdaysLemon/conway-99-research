#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import post_source_m7g_audit as audit  # noqa: E402


class PostSourceM7gAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(audit.SOURCE_RESULT.read_text(encoding="utf-8"))
        self.independent = json.loads(audit.INDEPENDENT_RESULT.read_text(encoding="utf-8"))

    def test_archived_audit_replays(self) -> None:
        expected = json.loads(audit.ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(audit.build_result(), expected)

    def test_original_finding_and_correction_are_both_retained(self) -> None:
        result = audit.build_result()
        history = result["documentation_history"]
        self.assertIn("other 91 vertices", history["original_finding"])
        self.assertIn("not fixed", history["correction_verified"])
        self.assertTrue(history["computational_artifacts_unchanged"])

    def test_missing_orientation_is_rejected(self) -> None:
        mutant = copy.deepcopy(self.source)
        mutant["classes"].pop()
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, self.independent)

    def test_aggregate_only_survivor_mutation_is_rejected(self) -> None:
        mutant = copy.deepcopy(self.source)
        mutant["classes"][0]["surviving_forms"][0]["d"] = -15
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, self.independent)

    def test_product_one_resolution_is_rejected(self) -> None:
        mutant = copy.deepcopy(self.independent)
        mutant["product_one_interpretation_fixed"] = True
        with self.assertRaises(AssertionError):
            audit.validate_source(self.source, mutant)

    def test_global_status_inflation_is_rejected(self) -> None:
        mutant = copy.deepcopy(self.source)
        mutant["global_status"] = "NONEXISTENT"
        with self.assertRaises(AssertionError):
            audit.validate_source(mutant, self.independent)


if __name__ == "__main__":
    unittest.main()
