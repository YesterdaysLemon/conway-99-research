#!/usr/bin/env python3
"""Focused regression tests for the Wave 13 ``n3=45`` computation lane."""

from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

import wave13_n3_45_active_sat as SAT
import wave13_n3_45_profiles as PROFILES


ROOT = Path(__file__).resolve().parents[1]
ATTEMPTS = ROOT / "attempts" / "wave13-computation"


class Wave13ProfileTests(unittest.TestCase):
    def test_nine_profiles_and_two_final_arithmetic_frontiers(self) -> None:
        self.assertEqual(len(PROFILES.active_q_profiles()), 9)
        rows = PROFILES.profile_table()
        self.assertEqual(
            sum(row["survives_no_singleton_degree_filter"] for row in rows),
            3,
        )
        self.assertEqual(
            sum(row["survives_degree_three_obstruction"] for row in rows),
            2,
        )

    def test_large_point_flowers_have_no_degree_survivor(self) -> None:
        result = PROFILES.audit()
        flowers = result["flower_censuses"]
        self.assertEqual(
            {
                key: value["statistics"]["capacity_feasible"]
                for key, value in flowers.items()
            },
            {
                "order15_size5": 1,
                "order15_size4": 157,
                "order14_size4": 45,
            },
        )
        self.assertTrue(
            all(
                value["statistics"].get("k_degree_survivors", 0) == 0
                for value in flowers.values()
            )
        )

    def test_mixed_order14_profile_is_locally_excluded(self) -> None:
        result = PROFILES.mixed_order14_reduction()
        self.assertEqual(result["size_three_branch_survivors"], 0)
        self.assertEqual(result["profile_survivors"], 0)
        self.assertTrue(
            result["all_size_two_branch"]["contradiction"]
        )
        self.assertEqual(
            result["all_size_two_branch"]["forced_K_degree_lower_bound"],
            5,
        )
        self.assertEqual(
            result["small_cubic_census"][6][
                "labeled_triangle_free_cubic"
            ],
            10,
        )

    def test_four_order15_root_modes_and_59_signatures(self) -> None:
        modes = PROFILES.size_three_local_modes(15, (2, 2, 2))
        self.assertEqual(
            {
                tuple(sorted(mode["t_values"])) for mode in modes
            },
            {(1, 1, 1), (1, 2, 2), (2, 2, 2), (2, 2, 3)},
        )
        signatures = PROFILES.all_q2_incidence_signatures()
        self.assertEqual(len(signatures), 59)
        self.assertEqual(
            Counter(row["size3_points"] for row in signatures),
            Counter({1: 2, 3: 7, 5: 16, 7: 21, 9: 12, 11: 1}),
        )


class Wave13SatArtifactTests(unittest.TestCase):
    def test_scan_covers_17_unsat_unverified_branches(self) -> None:
        scan = json.loads(
            (ATTEMPTS / "n3-45-active-local-sat-scan.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(scan["branch_count"], 17)
        self.assertEqual(
            tuple(tuple(row) for row in scan["branch_cover"]),
            SAT.SCAN_BRANCHES,
        )
        self.assertEqual(
            scan["status"], "COMPLETE_BRANCH_COVER_UNSAT_UNVERIFIED"
        )
        self.assertTrue(
            all(
                row["status"] == "UNSAT_UNVERIFIED"
                for row in scan["branches"]
            )
        )
        self.assertTrue(
            all(
                len(row["statistics"]["cnf_sha256"]) == 64
                for row in scan["branches"]
            )
        )
        self.assertEqual(scan["claim_label"], "CANDIDATE")
        self.assertEqual(scan["target_result"], "UNKNOWN")

    def test_first_scan_formula_rebuilds_to_the_recorded_hash(self) -> None:
        scan = json.loads(
            (ATTEMPTS / "n3-45-active-local-sat-scan.json").read_text(
                encoding="utf-8"
            )
        )
        cnf, pool, *_rest = SAT.build_instance(1, "111", "full")
        first = scan["branches"][0]["statistics"]
        self.assertEqual(pool.top, first["variables"])
        self.assertEqual(len(cnf.clauses), first["clauses"])
        self.assertEqual(
            SAT.cnf_sha256(cnf, pool.top), first["cnf_sha256"]
        )

    def test_weakened_survivor_replays_and_mutation_is_rejected(self) -> None:
        path = ATTEMPTS / "n3-45-no-common-point-m5-111.json"
        candidate = json.loads(path.read_text(encoding="utf-8"))
        result = SAT.validate_weakened_candidate(candidate)
        self.assertEqual(
            result["status"], "PASS weakened active-local diagnostic"
        )
        self.assertEqual(result["omitted_premise_violation_count"], 18)
        mutated = copy.deepcopy(candidate)
        mutated["K_edges"].pop()
        with self.assertRaises(AssertionError):
            SAT.validate_weakened_candidate(mutated)


if __name__ == "__main__":
    unittest.main()
