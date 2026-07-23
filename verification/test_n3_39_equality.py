#!/usr/bin/env python3
"""Regression tests for the compact Wave 11 equality checker."""

from __future__ import annotations

import importlib.util
import unittest
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERIFIER_PATH = ROOT / "n3-39-equality" / "verify.py"
SPEC = importlib.util.spec_from_file_location("n3_39_equality_verifier", VERIFIER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load the n3=39 equality verifier")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class N339EqualityVerifierTests(unittest.TestCase):
    def test_committed_checker_passes(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(VERIFIER.main([]), 0)
        rendered = output.getvalue()
        self.assertIn("PASS n3=39 equality exclusion arithmetic", rendered)
        self.assertIn("global_n3_lower_bound 42", rendered)
        self.assertIn("global_p6_lower_bound 209328", rendered)
        self.assertIn("target_result UNKNOWN", rendered)

    def test_active_profiles_and_k_degrees(self) -> None:
        profiles = VERIFIER.active_q_sequences(39)
        self.assertEqual(
            profiles,
            (
                (2,) * 13,
                (2,) * 10 + (3, 3),
                (2,) * 7 + (3,) * 4,
                (2,) * 4 + (3,) * 6,
            ),
        )
        self.assertEqual(Counter(VERIFIER.k_degree_profile(profiles[1])), Counter({5: 10, 2: 2}))
        with self.assertRaises(ValueError):
            VERIFIER.active_q_sequences(1)

    def test_singleton_forcing(self) -> None:
        self.assertEqual(VERIFIER.forced_singletons_at_triangle(2), 1)
        self.assertEqual(VERIFIER.forced_singletons_at_triangle(1), 2)
        self.assertEqual(VERIFIER.forced_singletons_at_triangle(0), 3)
        with self.assertRaises(ValueError):
            VERIFIER.forced_singletons_at_triangle(-1)

    def test_crossing_tables(self) -> None:
        expected_counts = {
            (1, 1): 1,
            (1, 2): 1,
            (1, 3): 1,
            (2, 2): 2,
            (2, 3): 4,
            (3, 3): 16,
        }
        self.assertEqual(
            {pair: len(VERIFIER.crossing_masks(*pair)) for pair in expected_counts},
            expected_counts,
        )
        self.assertEqual(VERIFIER.crossing_edge_counts(1, 4), frozenset((0,)))
        with self.assertRaises(ValueError):
            VERIFIER.crossing_masks(-1, 2)

    def test_common_point_rule(self) -> None:
        self.assertTrue(
            VERIFIER.forbidden_common_point_triple(
                (
                    frozenset((0, 1, 2)),
                    frozenset((0, 3)),
                    frozenset((1, 3)),
                )
            )
        )
        self.assertFalse(
            VERIFIER.forbidden_common_point_triple(
                (
                    frozenset((0, 1, 2)),
                    frozenset((0, 3)),
                    frozenset((0, 4)),
                )
            )
        )

    def test_expansion_and_local_types(self) -> None:
        self.assertEqual(
            tuple(size for size in range(2, 14) if VERIFIER.expansion_bound(size)[2]),
            (2, 3, 4),
        )
        self.assertEqual(
            VERIFIER.local_point_types(),
            (
                (2, 2, 2),
                (2, 2, 3),
                (2, 2, 4),
                (2, 2, 5),
                (2, 3, 3),
                (2, 3, 4),
                (3, 3, 3),
            ),
        )
        with self.assertRaises(ValueError):
            VERIFIER.expansion_bound(1)

    def test_size_four_flowers(self) -> None:
        self.assertEqual(
            VERIFIER.size_four_flower_statistics(),
            {
                "total_profiles": 6_561,
                "capacity_rejections": 6_552,
                "feasible_profiles": 9,
                "minimum_type_224_occurrences": 3,
                "crossing_extensions": 33,
                "minimum_root_degree_lower": 7,
            },
        )

    def test_f_u_table_and_size_three_flowers(self) -> None:
        self.assertEqual(tuple(VERIFIER.u_degree(value) for value in range(4)), (3, 2, 1, 0))
        self.assertEqual(
            VERIFIER.size_three_flower_statistics(),
            {
                "total_profiles": 64,
                "capacity_rejections": 7,
                "type_233_rejections": 50,
                "root_u_degree_rejections": 7,
                "type_233_crossing_extensions": 700,
                "root_u_crossing_extensions": 217,
                "feasible_crossing_extensions": 917,
            },
        )
        with self.assertRaises(ValueError):
            VERIFIER.u_degree(4)

    def test_resource_profiles_and_parity(self) -> None:
        profiles = VERIFIER.point_resource_profiles()
        self.assertEqual(len(profiles), 20)
        self.assertTrue(all(x3 % 2 for _x2, x3, _x4 in profiles))
        self.assertEqual((VERIFIER.ACTIVE_ORDER * 3) % 2, 1)

    def test_wave11_branch_bounds(self) -> None:
        self.assertEqual(
            tuple(
                max(42, VERIFIER.ceil_multiple_of_three(4 * degree))
                for degree in VERIFIER.WAVE6_BRANCH_DEGREES
            ),
            (42, 42, 42, 48, 48, 42, 42, 48, 42, 48, 42, 48),
        )


if __name__ == "__main__":
    unittest.main()
