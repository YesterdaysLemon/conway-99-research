from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave207_code_bridge", HERE / "exact_check.py")
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class TernaryAdjacencyCodeBridgeTests(unittest.TestCase):
    def test_frozen_inputs(self) -> None:
        self.assertEqual(CHECK.check_frozen_inputs(), CHECK.FROZEN_INPUTS)

    def test_adjacency_algebra(self) -> None:
        result = CHECK.adjacency_algebra_checks()
        self.assertTrue(result["G_squared_equals_G_minus_J"])
        self.assertTrue(result["A_E_equals_zero"])
        self.assertTrue(result["E_squared_equals_E"])

    def test_weight_eight_bridge(self) -> None:
        result = CHECK.bridge_checks()
        self.assertEqual(result["a_dot_a_mod_3"], 2)
        self.assertEqual(result["b_dot_b_mod_3"], 2)
        self.assertEqual(result["possible_weights_after_distance_floor"], [14, 17, 20, 23])

    def test_base_pointwise_inequality(self) -> None:
        result = CHECK.signed_distance_checks()
        self.assertTrue(result["pointwise_F_nonnegative"])

    def test_weight_ten_contradiction(self) -> None:
        result = CHECK.signed_distance_checks()["weight_10"]
        self.assertEqual(result["only_survivor"], [5, 5])
        self.assertEqual(result["forced_same_sign_common_neighbor_sum"], 20)
        self.assertTrue(result["contradiction"])

    def test_weight_eleven_farkas_certificate(self) -> None:
        result = CHECK.signed_distance_checks()["weight_11"]
        self.assertTrue(result["all_phi_nonnegative"])
        self.assertEqual(result["global_farkas_sum"], -60)
        self.assertTrue(result["contradiction"])

    def test_distance_floor(self) -> None:
        self.assertEqual(
            CHECK.signed_distance_checks()["derived_minimum_distance_lower_bound"],
            12,
        )

    def test_formal_control_moments(self) -> None:
        result = CHECK.formal_control_checks()
        self.assertEqual(result["category_counts"], {"P": 7, "N": 7, "O": 85})
        self.assertEqual(result["edge_counts"], {"e_P": 6, "e_N": 6, "e_PN": 0})
        self.assertEqual(
            result["pair_moments"],
            {"sum_choose_i_2": 36, "sum_choose_j_2": 36, "sum_i_j": 98},
        )
        self.assertEqual(result["matching_totals"], {"h_pp": 6, "h_nn": 6, "h_pn": 0})

    def test_formal_control_is_explicitly_not_graph_or_codeword(self) -> None:
        result = CHECK.formal_control_checks()
        self.assertTrue(result["declared_nongraphical"])
        self.assertFalse(result["is_graph"])
        self.assertFalse(result["is_codeword"])

    def test_submitted_result_matches(self) -> None:
        submitted = json.loads((HERE / "exact-results.json").read_text(encoding="utf-8"))
        self.assertEqual(submitted, CHECK.build_result())


if __name__ == "__main__":
    unittest.main()
