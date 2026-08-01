from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave209_rank4_exact", HERE / "exact_check.py")
assert SPEC and SPEC.loader
EC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EC)


class Wave209Rank4ExactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.controls = json.loads((HERE / "aggregate-controls.json").read_text(encoding="utf-8"))
        cls.point_controls = json.loads((HERE / "point-signature-controls.json").read_text(encoding="utf-8"))
        cls.expected = json.loads((HERE / "exact-results.json").read_text(encoding="utf-8"))
        cls.actual = EC.build_result(cls.controls, cls.point_controls)

    def test_archived_result_replays_exactly(self) -> None:
        self.assertEqual(self.actual, self.expected)

    def test_input_hashes_are_pinned(self) -> None:
        for relative, expected in EC.EXPECTED_INPUT_HASHES.items():
            self.assertEqual(EC.sha256(EC.ROOT / relative), expected)

    def test_all_labelled_branches_are_covered_once(self) -> None:
        forms = tuple(EC.gram(diagonal) for diagonal in EC.FORM_DIAGONALS)
        nodes = {
            (form_index, H)
            for form_index, D in enumerate(forms)
            for H in EC.accepted_subsets(D)
        }
        orbits = EC.branch_orbits()
        flattened = [node for orbit in orbits for node in orbit]
        self.assertEqual(len(nodes), 249)
        self.assertEqual(len(flattened), 249)
        self.assertEqual(set(flattened), nodes)

    def test_projector_bound_is_saturated(self) -> None:
        projector = self.actual["spectral_triangle_reduction"]["projector"]
        for row in projector["selected_forms"]:
            self.assertEqual(row["marked_minimum_zero_eigen_norm"], 168)
            self.assertEqual(row["inverse_action"], [-7, -7, -7, -7, 7, 7, 7, 7])

    def test_parity_precludes_division_by_two(self) -> None:
        parity = self.actual["parity"]
        self.assertTrue(parity["q_even_excluded"])
        self.assertFalse(parity["norm14_division_available"])
        self.assertEqual(parity["point_count_profiles_after_odd_support_minimum"], 800)

    def test_point_signature_farkas_exclusions(self) -> None:
        census = self.actual["point_signature_census"]
        self.assertEqual(census["excluded_orbits"], 17)
        self.assertEqual(census["excluded_labelled_branches"], 198)
        self.assertEqual(census["feasible_orbits"], 7)
        self.assertEqual(census["surviving_labelled_branches"], 51)
        for row in census["orbit_summaries"]:
            if row["kind"] == "farkas":
                self.assertLess(row["farkas_rhs"], 0)
                self.assertGreaterEqual(row["farkas_pointwise_minimum"], 0)

    def test_every_aggregate_and_local_witness_is_transported(self) -> None:
        aggregate = self.actual["aggregate_controls"]
        self.assertEqual(aggregate["covered_labelled_branches"], 249)
        self.assertEqual(sum(row["transported_branch_checks"] for row in aggregate["orbit_summaries"]), 249)
        local = self.actual["parity"]["selected_union_integer_controls"]
        self.assertEqual(sum(row["transported_branch_checks"] for row in local["orbit_examples"]), 249)
        self.assertLessEqual(max(map(int, local["minimum_norm_distribution"])), 56)

    def test_mutated_control_is_rejected(self) -> None:
        payload = copy.deepcopy(self.controls)
        payload["controls"][0]["counts"][0][2] += 1
        with self.assertRaises(AssertionError):
            EC.build_result(payload, self.point_controls)

    def test_erased_farkas_certificate_is_rejected(self) -> None:
        payload = copy.deepcopy(self.point_controls)
        farkas = next(row for row in payload["orbits"] if row["kind"] == "farkas")
        farkas["coefficients"] = []
        with self.assertRaises(AssertionError):
            EC.build_result(self.controls, payload)


if __name__ == "__main__":
    unittest.main()
