#!/usr/bin/env python3
"""Regression and hostile-mutation tests for the Wave 210 coupling census."""

from __future__ import annotations

import unittest
from collections import Counter
from itertools import combinations

import exact_check as wave


class Wave210CouplingTests(unittest.TestCase):
    def test_frozen_inputs(self) -> None:
        self.assertEqual(wave.verify_inputs(), wave.INPUT_HASHES)

    def test_complete_label_expansion(self) -> None:
        self.assertEqual(len(wave.marked_graphs()), 204)
        self.assertEqual(len(wave.labelled_cases()), 20_928)
        self.assertEqual(len(wave.requirement_patterns()), 232)
        self.assertEqual(len(wave.valid_deficit_matchings()), 4480)

    def test_ordered_packing_counts(self) -> None:
        self.assertEqual(len(wave.ordered_packings((3, 1, 1, 0))), 4)
        self.assertEqual(len(wave.ordered_packings((2, 2, 1, 0))), 12)
        self.assertEqual(len(wave.ordered_packings((3, 2, 0, 0))), 0)
        self.assertEqual(len(wave.ordered_packings((2, 1, 1, 1))), 0)

    def test_symmetry_partition_is_explicit(self) -> None:
        self.assertEqual(wave.symmetry_audit()["polar_line_group_order"], 48)
        orbits = wave.case_orbits()
        self.assertEqual(len(orbits), 33)
        self.assertEqual(sum(size for _, size in orbits), 20_928)
        self.assertEqual(Counter(size for _, size in orbits), Counter({768: 22, 384: 10, 192: 1}))

    def test_exact_F_columns(self) -> None:
        for matching_index in (0, 4479):
            columns, _ = wave.concrete_columns(matching_index)
            self.assertTrue(wave.verify_F_identity(columns))
        census = wave.base_local_matching_census()
        self.assertEqual(census["configurations_admitting_all_14_local_matchings"], 4480)

    def test_containment_only_does_not_close(self) -> None:
        rows = wave.containment_catalog()
        counts = [row["compatible_deficit_bijections"] for row in rows]
        self.assertEqual((len(rows), min(counts), max(counts)), (232, 422, 2116))
        self.assertTrue(all(count > 0 for count in counts))

    def test_full_selected_union_cut(self) -> None:
        rows = wave.orbit_coupling_catalog()
        surviving = [row for row in rows if row["witness"]]
        self.assertEqual(len(surviving), 3)
        self.assertEqual(
            sum(row["labelled_case_orbit_size"] for row in surviving), 1536
        )
        self.assertEqual(
            sum(
                row["labelled_case_orbit_size"]
                * row["deficit_bijections_after_local_matching_extension"]
                for row in rows
            ),
            55_296,
        )
        self.assertTrue(all(
            row["deficit_bijections_after_polar_and_induced_caps"]
            == row["deficit_bijections_after_local_matching_extension"]
            for row in rows
        ))

    def test_hostile_controls_replay(self) -> None:
        controls = wave.build_hostile_controls()["controls"]
        self.assertEqual(len(controls), 3)
        self.assertTrue(all(all(control["checks"].values()) for control in controls))
        self.assertEqual({control["orbit_index"] for control in controls}, {0, 4, 29})

    def test_hostile_F_mutation_is_rejected(self) -> None:
        columns, _ = wave.concrete_columns(0)
        corrupted = list(columns)
        corrupted[0] = frozenset(tuple(corrupted[0])[:-1])
        with self.assertRaises(AssertionError):
            wave.verify_F_identity(tuple(corrupted))

    def test_hostile_t2_and_local_edge_mutations_are_rejected(self) -> None:
        matching_index = 0
        matching = wave.matching_data()[0][matching_index]
        wrong_n = (matching[0] + 1) % 7
        self.assertFalse(
            (wave.availability_masks()[(2, 0, wrong_n, 1)] >> matching_index) & 1
        )

        columns, _ = wave.concrete_columns(matching_index)
        bad_pair = next(
            wave.edge(a, b)
            for a, b in combinations(range(85), 2)
            if len(columns[a] & columns[b]) >= 2
        )
        self.assertIsNone(wave.local_matching_counts(columns, frozenset({bad_pair})))


if __name__ == "__main__":
    unittest.main()
