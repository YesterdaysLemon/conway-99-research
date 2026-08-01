from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave208_marked_m7g_exact", HERE / "exact_check.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MarkedM7gSpectralTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = MODULE.build_result()

    def test_divisibility_reduces_to_four_forms(self) -> None:
        self.assertEqual(self.result["additional_wave207_survivors_excluded"], 19)
        self.assertEqual(self.result["surviving_forms"], 4)

    def test_unique_tensor_relation(self) -> None:
        self.assertEqual(self.result["projective_linear_weight_eight_relation_classes"], 4)
        self.assertEqual(self.result["projective_tensor_weight_eight_relation_classes"], 1)

    def test_residual_types(self) -> None:
        rows = self.result["survivor_classes"][0]["surviving_forms"]
        self.assertEqual([row["signed_polar_sum"] for row in rows], [-24, -24, -24, 12])
        self.assertEqual([row["divided_residual_squared_norm"] for row in rows], [56, 56, 56, 0])

    def test_complete_intersection_counts(self) -> None:
        self.assertEqual(sum(self.result["minus24_intersection_profiles"].values()), 83)
        self.assertEqual(sum(self.result["plus12_intersection_profiles"].values()), 858)

    def test_local_controls(self) -> None:
        controls = self.result["local_controls"]
        self.assertEqual([row["point_weight"] for row in controls], [20, 14])
        self.assertTrue(all(row["exact_AUb_equals_3b"] for row in controls))
        self.assertTrue(all(row["induced_triangular_prisms"] == 0 for row in controls))


if __name__ == "__main__":
    unittest.main()
