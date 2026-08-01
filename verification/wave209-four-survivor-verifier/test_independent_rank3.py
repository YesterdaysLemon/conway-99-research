#!/usr/bin/env python3
"""Hostile tests for the clean-room Wave 209 rank-three verifier."""

from __future__ import annotations

import copy
import sys
import unittest
from collections import Counter
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import independent_rank3 as rank3  # noqa: E402


class IndependentRankThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = rank3.build_result()

    def test_r_minus_3k_is_coordinatewise_and_mutation_fails(self) -> None:
        marked = ((0, 5), (1, 4))
        self.assertEqual(rank3.r3k_residual(marked, (0, 0, 0, 0)), (0,) * 8)
        self.assertEqual(
            rank3.r3k_residual(marked, (0, 1, 0, 0)),
            (0, -3, 0, 0, 0, 3, 0, 0),
        )
        self.assertEqual(self.result["r_minus_3k"]["marked_and_mask_cases_checked"], 13_728)

    def test_weight14_graph_deficits_and_bijections(self) -> None:
        row = self.result["weight14_m5"]
        self.assertEqual(row["forced_cross_edges"], 1)
        self.assertEqual(row["rooted_sign_graph"]["labelled_graphs"], 180)
        self.assertEqual(row["rooted_sign_graph"]["rooted_isomorphism_classes"], 1)
        self.assertEqual(row["outside_signature_z0_z1_z2"], [17, 61, 7])
        self.assertEqual(row["deficit_bijections"]["valid_bijections"], 4480)
        self.assertEqual(row["deficit_bijections"]["invalid_bijections"], 560)
        deficits = rank3.deficit_edges(rank3.ROOTED_GRAPH)
        self.assertFalse(rank3.valid_deficit_bijection(deficits, (deficits[0],) * 7))
        invalid = next(order for order in permutations(deficits) if not rank3.valid_deficit_bijection(deficits, order))
        self.assertFalse(rank3.valid_deficit_bijection(deficits, invalid))

    def test_weight14_marked_census_is_label_complete_and_symmetric(self) -> None:
        row = self.result["weight14_m5"]["marked_lines"]
        self.assertEqual(row["total_labelled_subsets"], 792)
        self.assertEqual(row["accepted_labelled_subsets"], 204)
        self.assertEqual(
            row["accepted_subsets_sha256"],
            "d16cbf04d03f4637be24f80bcdeb31a122cc13b9a890439fca4a17c9c022f967",
        )
        accepted = {
            tuple(sorted(tuple(edge) for edge in marked)) for marked in row["accepted_subsets"]
        }
        for permutation in permutations(range(4)):
            image = {
                tuple(sorted((permutation[left], permutation[right]) for left, right in marked))
                for marked in accepted
            }
            self.assertEqual(image, accepted)
        transposed = {
            tuple(sorted((right, left) for left, right in marked)) for marked in accepted
        }
        self.assertEqual(transposed, accepted)

    def test_weight20_selected_line_lower_bound_and_six_cases(self) -> None:
        row = self.result["weight20_m2"]["marked_lines"]
        self.assertEqual(row["x0_survivors"], 0)
        self.assertEqual(row["x2_survivors"], 6)
        expected = {
            tuple(sorted(((left, right), (right, left))))
            for left in range(4)
            for right in range(left + 1, 4)
        }
        actual = {
            tuple(sorted(tuple(edge) for edge in marked))
            for marked in row["x2_swapped_disjoint_cases"]
        }
        self.assertEqual(actual, expected)
        self.assertEqual(row["x4_survivors"], 42)
        self.assertEqual(row["x6_survivors"], 66)
        self.assertEqual(row["x8_survivors"], 66)

    def test_weight20_aggregate_rows_replay_exactly(self) -> None:
        row = self.result["weight20_m2"]
        self.assertEqual(row["aggregate_rows_total"], 352)
        self.assertEqual(row["aggregate_row_distribution"], {"2": 109, "4": 157, "6": 76, "8": 10})
        self.assertEqual(
            row["aggregate_rows_sha256"],
            "06e597e1321b1e2143cc162497c37670cbcb33695fe93923361e66a7953d984a",
        )
        self.assertTrue(all(rank3.aggregate_row_valid(candidate) for candidate in row["aggregate_rows"]))
        mutant = copy.deepcopy(row["aggregate_rows"][0])
        mutant["outside_balanced_degree_histogram"][0] += 1
        self.assertFalse(rank3.aggregate_row_valid(mutant))

    def test_x10_is_excluded_by_an_exact_integer_gap(self) -> None:
        row = self.result["weight20_m2"]
        self.assertEqual(row["x10_outside_pair_lower_bound"], 11)
        self.assertEqual(row["x10_outside_pair_upper_bound"], 10)
        self.assertTrue(row["x10_excluded"])

    def test_aggregate_scope_does_not_hide_selected_line_delta(self) -> None:
        row = self.result["weight20_m2"]
        delta = row["post_aggregate_selected_line_degree_cap"]
        self.assertEqual(delta["claim_label"], "DERIVED")
        self.assertEqual(delta["rows_removed_from_aggregate_table"], 6)
        self.assertEqual(delta["remaining_rows"], 346)
        removed = [
            candidate
            for candidate in row["aggregate_rows"]
            if candidate["plus_cross_degree_histogram"][4]
            or candidate["plus_cross_degree_histogram"][5]
            or candidate["minus_cross_degree_histogram"][4]
            or candidate["minus_cross_degree_histogram"][5]
        ]
        self.assertEqual(Counter(candidate["x"] for candidate in removed), Counter({4: 6}))

    def test_line_moment_witness_and_mutation(self) -> None:
        row = self.result["line_vector_moments"]
        self.assertEqual(row["weight14_accepted_marked_sets_checked"], 204)
        self.assertEqual(row["weight20_marked_x_pairs_checked"], 180)
        serialized = row["weight14_example"]["line_types"]
        counts = {}
        for key, value in serialized.items():
            positive, negative = key.split("_")
            counts[(int(positive[1:]), int(negative[1:]))] = value
        self.assertTrue(rank3.line_type_table_valid(counts, 7, 1))
        counts[(0, 0)] += 1
        self.assertFalse(rank3.line_type_table_valid(counts, 7, 1))

    def test_scope_walls_remain_unknown(self) -> None:
        walls = self.result["scope_walls"]
        self.assertEqual(walls["conway_99_status"], "UNKNOWN")
        self.assertEqual(walls["rank11_endpoint_status"], "UNKNOWN")
        self.assertEqual(walls["n3_4158_endpoint_status"], "UNKNOWN")
        self.assertFalse(walls["aggregate_rows_are_graphs"])
        self.assertFalse(walls["full_99_vertex_adjacency_supplied"])
        self.assertFalse(walls["complete_nonexistence_certificate"])


if __name__ == "__main__":
    unittest.main()
