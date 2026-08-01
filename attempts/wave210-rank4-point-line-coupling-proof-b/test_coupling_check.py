from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave210_coupling", HERE / "coupling_check.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Wave210CouplingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        MODULE.check_frozen_inputs()
        cls.certificates = json.loads(MODULE.CERTIFICATES.read_text(encoding="utf-8"))
        cls.coarse = json.loads(MODULE.COARSE_CONTROLS.read_text(encoding="utf-8"))
        cls.reconstruction = MODULE.verify_wave209_survivors()
        cls.transport = MODULE.verify_coupling_transport()
        cls.certificate_summaries = MODULE.verify_certificates(cls.certificates)
        cls.coarse_summaries = MODULE.verify_coarse_controls(cls.coarse)

    def test_independent_wave209_reconstruction(self) -> None:
        self.assertEqual(self.reconstruction["survivor_orbits"], list(MODULE.SURVIVOR_ORBITS))
        self.assertEqual(self.reconstruction["surviving_labelled_branches"], 51)

    def test_all_seven_integer_farkas_certificates(self) -> None:
        self.assertEqual(len(self.certificate_summaries), 7)
        self.assertEqual(sum(row["labelled_branches"] for row in self.certificate_summaries), 51)
        self.assertTrue(all(row["rhs"] < 0 for row in self.certificate_summaries))
        self.assertTrue(all(row["pattern_minimum"] >= 0 for row in self.certificate_summaries))
        self.assertTrue(all(row["point_minimum"] >= 0 for row in self.certificate_summaries))

    def test_constraint_transport_covers_every_labelled_branch(self) -> None:
        self.assertEqual(self.transport["transported_branch_checks"], 51)
        self.assertGreater(self.transport["transported_local_pattern_checks"], 500_000)

    def test_coarse_relaxation_has_exact_positive_controls(self) -> None:
        self.assertEqual(len(self.coarse_summaries), 7)
        self.assertTrue(all(row["residual_nonzero_types"] > 0 for row in self.coarse_summaries))

    def test_generated_local_decomposition_obeys_direct_predicate(self) -> None:
        orbit_id = 14
        form_index, H = MODULE.branch_orbits()[orbit_id][0]
        D = MODULE.polar_matrix(MODULE.FORM_DIAGONALS[form_index])
        row = next(
            row
            for row in MODULE.triangle_types(D, H)
            if row[1] and MODULE.local_decompositions(H, row)
        )
        triple = MODULE.local_decompositions(H, row)[0]
        self.assertTrue(MODULE.is_local_decomposition(H, row, triple))
        self.assertFalse(MODULE.is_local_decomposition(H, row, (triple[0], triple[0], triple[2])))

    def test_erased_farkas_vector_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            MODULE.certificate_metrics(0, [])

    def test_one_count_coarse_mutation_is_rejected(self) -> None:
        hostile = copy.deepcopy(self.coarse)
        hostile["orbits"][0]["residual_counts"][0][1] += 1
        with self.assertRaises(AssertionError):
            MODULE.verify_coarse_controls(hostile)


if __name__ == "__main__":
    unittest.main()
