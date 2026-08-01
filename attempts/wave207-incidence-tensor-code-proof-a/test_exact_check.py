"""Focused tests for the Wave 207 canonical symbolic audit."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave207_proof_a_exact", HERE / "exact_check.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Wave207ProofATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = MODULE.build_result()

    def test_incidence_linear_normal_form(self) -> None:
        support = self.data["canonical_support"]
        self.assertEqual(support["composition"], {"1": 4, "2": 4})
        self.assertEqual(support["column_rank"], 4)
        self.assertTrue(support["every_three_independent"])
        self.assertEqual(support["signed_first_moment"], [0, 0, 0, 0])
        self.assertTrue(support["signed_second_moment_zero"])
        self.assertEqual(support["quadratic_veronese_rank"], 7)
        self.assertEqual(support["quadratic_relation_nullity"], 1)

    def test_relation_code_portfolio(self) -> None:
        code = self.data["relation_code"]
        self.assertEqual(code["words"], 81)
        self.assertEqual(
            code["weight_enumerator"],
            {"0": 1, "4": 24, "5": 16, "6": 32, "8": 8},
        )
        self.assertEqual(code["projective_circuit_supports"], {"4": 12, "5": 8})
        self.assertEqual(code["weight4_circuits_from_two_concurrent_pairs"], 6)

    def test_restricted_polar_forms(self) -> None:
        forms = self.data["restricted_polar_forms"]
        self.assertEqual(forms["forms"], 27)
        self.assertEqual(forms["rank_counts"], {"0": 1, "2": 12, "3": 8, "4": 6})
        self.assertEqual(
            forms["zero_graph_by_rank"],
            {"0": ["K8"], "2": ["2K4"], "3": ["4K2"], "4": ["2C4"]},
        )


if __name__ == "__main__":
    unittest.main()
