#!/usr/bin/env python3
"""Tests for the deterministic rooted residual scaffold."""

from __future__ import annotations

import unittest

from root_model import RootModel


class ConwayRootModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.model = RootModel.build(7)

    def test_conway_dimensions(self) -> None:
        self.assertEqual(self.model.coordinate_count, 14)
        self.assertEqual(self.model.residual_count, 84)
        self.assertEqual(self.model.residual_degree, 12)
        self.assertEqual(self.model.edge_variable_count, 3486)

    def test_fixed_incidence_identities(self) -> None:
        self.model.validate_fixed_identities()

    def test_each_coordinate_occurs_twelve_times(self) -> None:
        self.assertEqual(
            [len(self.model.containing(coordinate)) for coordinate in range(14)],
            [12] * 14,
        )

    def test_neighbor_incidence_targets_force_degree_twelve(self) -> None:
        for label_index in range(84):
            target_sum = sum(
                self.model.coordinate_neighbor_target(coordinate, label_index)
                for coordinate in range(14)
            )
            self.assertEqual(target_sum // 2, 12)

    def test_common_neighbor_target_table(self) -> None:
        intersecting = next(
            (i, j)
            for i in range(84)
            for j in range(i + 1, 84)
            if set(self.model.labels[i]).intersection(self.model.labels[j])
        )
        disjoint = next(
            (i, j)
            for i in range(84)
            for j in range(i + 1, 84)
            if not set(self.model.labels[i]).intersection(self.model.labels[j])
        )
        self.assertEqual(self.model.common_neighbor_target(*intersecting, True), 0)
        self.assertEqual(self.model.common_neighbor_target(*intersecting, False), 1)
        self.assertEqual(self.model.common_neighbor_target(*disjoint, True), 1)
        self.assertEqual(self.model.common_neighbor_target(*disjoint, False), 2)

    def test_scaffold_generators_are_safe_label_permutations(self) -> None:
        generators = self.model.label_generators()
        self.assertEqual(len(generators), 13)
        for generator in generators:
            self.assertEqual(sorted(generator), list(range(84)))
            for i, image_i in enumerate(generator):
                for j, image_j in enumerate(generator):
                    before = len(set(self.model.labels[i]).intersection(self.model.labels[j]))
                    after = len(
                        set(self.model.labels[image_i]).intersection(
                            self.model.labels[image_j]
                        )
                    )
                    self.assertEqual(before, after)

    def test_pair_count_two_is_small_calibration_scaffold(self) -> None:
        small = RootModel.build(2)
        small.validate_fixed_identities()
        self.assertEqual(small.coordinate_count, 4)
        self.assertEqual(small.residual_count, 4)
        self.assertEqual(small.residual_degree, 2)

    def test_summary_constraint_counts(self) -> None:
        summary = self.model.summary()
        self.assertEqual(summary["residual_edge_count"], 504)
        self.assertEqual(summary["coordinate_incidence_equalities"], 1176)
        self.assertEqual(summary["common_neighbor_equalities"], 3486)
        self.assertEqual(summary["direct_and_auxiliaries"], 285852)
        self.assertEqual(len(summary["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
