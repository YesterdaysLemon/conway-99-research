import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave207_kernel_endpoint", HERE / "exact_check.py")
CHECK = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECK)


class KernelEndpointChecks(unittest.TestCase):
    def test_frozen_inputs(self) -> None:
        self.assertEqual(len(CHECK.check_frozen_inputs()), 3)

    def test_weight_fourteen_compositions(self) -> None:
        result = CHECK.composition_reduction()
        self.assertEqual(result["surviving_composition"], [7, 7])
        self.assertFalse(result["weight_14_excluded"])

    def test_one_thirteen_certificate(self) -> None:
        result = CHECK.certificate_check(1, 13)
        self.assertTrue(result["all_pointwise_values_nonnegative"])
        self.assertEqual(result["global_sum"], -35)

    def test_four_ten_certificate(self) -> None:
        result = CHECK.certificate_check(4, 10)
        self.assertTrue(result["all_pointwise_values_nonnegative"])
        self.assertEqual(result["global_sum"], -12)

    def test_hostile_control_is_not_promoted(self) -> None:
        result = CHECK.hostile_control_check()
        self.assertTrue(result["all_recorded_aggregate_equations_hold"])
        self.assertTrue(result["declared_nongraphical"])
        self.assertFalse(result["is_graph"])
        self.assertFalse(result["is_codeword"])

    def test_integer_lift_aggregate_collapse(self) -> None:
        result = CHECK.lift_collapse_check()
        self.assertTrue(result["category_summed_lift_adds_no_equation"])

    def test_unknown_wall(self) -> None:
        conclusions = CHECK.build_result()["conclusions"]
        for weight in (14, 17, 20, 23):
            self.assertFalse(conclusions[f"weight_{weight}_excluded"])
        self.assertEqual(conclusions["kernel_minimum_distance_at_least_24"], "UNKNOWN")
        self.assertEqual(conclusions["conway_99"], "UNKNOWN")

    def test_exact_results_match(self) -> None:
        expected = json.loads((HERE / "exact-results.json").read_text(encoding="utf-8"))
        self.assertEqual(CHECK.build_result(), expected)


if __name__ == "__main__":
    unittest.main()

