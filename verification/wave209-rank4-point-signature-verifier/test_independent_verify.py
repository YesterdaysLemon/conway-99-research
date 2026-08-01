from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import independent_verify as verifier


class Wave209RankFourIndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verifier.build_result()

    def test_frozen_archive_replays(self) -> None:
        expected = json.loads(verifier.RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(self.result, expected)

    def test_all_249_labelled_branches_are_partitioned_once(self) -> None:
        orbits = verifier.branch_orbits()
        nodes = [node for orbit in orbits for node in orbit]
        self.assertEqual(len(nodes), 249)
        self.assertEqual(len(set(nodes)), 249)
        self.assertEqual(Counter(map(len, orbits)), Counter({3: 1, 6: 9, 12: 12, 24: 2}))

    def test_pair_tables_have_exact_margins_and_inner_products(self) -> None:
        for form, subsets in zip(verifier.grams(), map(verifier.accepted_subsets, verifier.grams())):
            for H in subsets:
                for i, j in verifier.combinations(range(8), 2):
                    table = verifier.point_pair_table(form, H, i, j)
                    for left, expected in ((-1, 3), (0, 60), (1, 36)):
                        self.assertEqual(sum(table[left, right] for right in (-1, 0, 1)), expected)
                        self.assertEqual(sum(table[right, left] for right in (-1, 0, 1)), expected)
                    inner = sum(left * right * count for (left, right), count in table.items())
                    self.assertEqual(inner, 18 - 7 * form[i][j])

    def test_projector_saturation_is_exact_for_all_three_forms(self) -> None:
        summaries = verifier.verify_projector()
        self.assertEqual([row["minimum_norm"] for row in summaries], [168, 168, 168])

    def test_hostile_mutations_and_wrong_dual_orientation_are_rejected(self) -> None:
        self.assertTrue(all(verifier.hostile_tests().values()))

    def test_scope_wall_is_retained(self) -> None:
        self.assertEqual(self.result["global_status"], "UNKNOWN")
        self.assertEqual(self.result["verdict"], "PASS_NO_VETO")
        self.assertFalse(self.result["marked_branch_census"]["target_automorphism_assumed"])


if __name__ == "__main__":
    unittest.main()
