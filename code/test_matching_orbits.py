#!/usr/bin/env python3
"""Exact coverage tests for the 11 canonical endpoint-fiber branches."""

from __future__ import annotations

import unittest

from matching_orbits import (
    canonical_branch_decisions,
    canonical_matching,
    integer_partitions,
    matching_type,
    orbit_sizes_via_generators,
    orbit_type_counts,
)
from root_model import RootModel


EXPECTED_COUNTS = {
    (6,): 3840,
    (5, 1): 2304,
    (4, 2): 1440,
    (4, 1, 1): 720,
    (3, 3): 640,
    (3, 2, 1): 960,
    (3, 1, 1, 1): 160,
    (2, 2, 2): 120,
    (2, 2, 1, 1): 180,
    (2, 1, 1, 1, 1): 30,
    (1, 1, 1, 1, 1, 1): 1,
}


class MatchingOrbitTests(unittest.TestCase):
    def test_partitions_of_six_have_eleven_types(self) -> None:
        partitions = list(integer_partitions(6))
        self.assertEqual(len(partitions), 11)
        self.assertEqual(set(partitions), set(EXPECTED_COUNTS))

    def test_exhaustive_labeled_matching_counts(self) -> None:
        counts = orbit_type_counts(6)
        self.assertEqual(dict(counts), EXPECTED_COUNTS)
        self.assertEqual(sum(counts.values()), 10395)

    def test_generators_give_exactly_the_same_eleven_orbits(self) -> None:
        self.assertEqual(orbit_sizes_via_generators(6), EXPECTED_COUNTS)

    def test_each_canonical_representative_has_requested_type(self) -> None:
        for partition in EXPECTED_COUNTS:
            self.assertEqual(matching_type(canonical_matching(partition), 6), partition)

    def test_branch_fixes_one_perfect_matching_and_all_nonmatching_edges(self) -> None:
        root = RootModel.build(7)
        for partition in EXPECTED_COUNTS:
            with self.subTest(partition=partition):
                decisions = canonical_branch_decisions(root, 0, partition)
                self.assertEqual(len(decisions), 66)
                self.assertEqual(sum(decisions.values()), 6)
                fiber = set(root.containing(0))
                degrees = {vertex: 0 for vertex in fiber}
                for (first, second), present in decisions.items():
                    self.assertIn(first, fiber)
                    self.assertIn(second, fiber)
                    if present:
                        degrees[first] += 1
                        degrees[second] += 1
                self.assertEqual(set(degrees.values()), {1})


if __name__ == "__main__":
    unittest.main()
