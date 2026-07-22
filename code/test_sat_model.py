#!/usr/bin/env python3
"""Calibration tests for the rooted SAT encodings."""

from __future__ import annotations

import unittest

from sat_model import EncodedRootModel, solve_model


class DirectSatEncodingTests(unittest.TestCase):
    def test_pair_count_two_is_sat_and_decodes_srg_9_4_1_2(self) -> None:
        for variant in ("compact", "direct"):
            with self.subTest(variant=variant):
                encoded = EncodedRootModel.build(2, variant)
                satisfiable, model, _ = solve_model(encoded, "cadical300")
                self.assertTrue(satisfiable)
                self.assertIsNotNone(model)
                certificate = encoded.full_certificate(model or [])
                self.assertEqual(certificate["vertices"], 9)
                self.assertEqual(len(certificate["edges"]), 18)

                adjacency = [set() for _ in range(9)]
                for first, second in certificate["edges"]:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
                self.assertEqual([len(neighbors) for neighbors in adjacency], [4] * 9)
                for first in range(9):
                    for second in range(first + 1, 9):
                        common = len(adjacency[first].intersection(adjacency[second]))
                        self.assertEqual(common, 1 if second in adjacency[first] else 2)

    def test_native_pair_count_two_is_sat_and_decodes_srg_9_4_1_2(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "native")
        satisfiable, model, _ = solve_model(encoded, "minicard")
        self.assertTrue(satisfiable)
        self.assertIsNotNone(model)
        certificate = encoded.full_certificate(model or [])
        self.assertEqual(certificate["vertices"], 9)
        self.assertEqual(len(certificate["edges"]), 18)

    def test_pair_count_three_is_unsat_negative_control(self) -> None:
        for variant in ("compact", "direct"):
            with self.subTest(variant=variant):
                encoded = EncodedRootModel.build(3, variant)
                satisfiable, model, _ = solve_model(encoded, "cadical300")
                self.assertIs(satisfiable, False)
                self.assertIsNone(model)

    def test_small_encoding_statistics_are_deterministic(self) -> None:
        statistics = EncodedRootModel.build(2, "compact").statistics()
        self.assertEqual(statistics["named_edge_variables"], 6)
        self.assertEqual(statistics["named_wedge_variables"], 12)
        self.assertGreater(statistics["total_variables"], 18)
        self.assertGreater(statistics["clauses"], 24)

    def test_compact_encoding_is_smaller_than_direct_encoding(self) -> None:
        compact = EncodedRootModel.build(3, "compact").statistics()
        direct = EncodedRootModel.build(3, "direct").statistics()
        self.assertLess(compact["total_variables"], direct["total_variables"])
        self.assertLess(compact["clauses"], direct["clauses"])

    def test_native_target_statistics_are_deterministic(self) -> None:
        statistics = EncodedRootModel.build(7, "compact", "native").statistics()
        self.assertEqual(statistics["cardinality_backend"], "native")
        self.assertEqual(statistics["total_variables"], 289_338)
        self.assertEqual(statistics["clauses"], 285_852)
        self.assertEqual(statistics["native_atmost_constraints"], 5_838)

    def test_native_constraints_reject_non_cardinality_solver(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "native")
        with self.assertRaisesRegex(ValueError, "minicard"):
            solve_model(encoded, "cadical300")

    def test_only_small_matching_branch_is_still_sat(self) -> None:
        encoded = EncodedRootModel.build(2, "compact")
        encoded.add_matching_branch(0, (1,))
        satisfiable, _, _ = solve_model(encoded, "cadical300")
        self.assertTrue(satisfiable)


if __name__ == "__main__":
    unittest.main()
