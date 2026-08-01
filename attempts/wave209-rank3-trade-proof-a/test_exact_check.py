from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("exact_check.py")
SPEC = importlib.util.spec_from_file_location("wave209_rank3_exact", MODULE_PATH)
CHECK = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECK)


class Wave209RankThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = CHECK.build_results()

    def test_frozen_inputs(self) -> None:
        self.assertEqual(CHECK.verify_inputs(), CHECK.INPUT_HASHES)

    def test_exact_aggregate_catalogs(self) -> None:
        self.assertEqual(self.result["raw_catalogs"]["weight14"]["rows_by_x"], {"1": 4, "3": 1})
        self.assertEqual(
            self.result["raw_catalogs"]["weight20"]["rows_by_x"],
            {"0": 73, "2": 109, "4": 157, "6": 76, "8": 10},
        )

    def test_selected_row_identity(self) -> None:
        identity = CHECK.selected_row_identity()
        self.assertEqual(identity["all_four_matched_q0_cross_counts"], [0, 0, 0, 0])
        self.assertEqual(len(identity["rows"]), 8)

    def test_weight14_intersection_obstruction(self) -> None:
        obstruction = CHECK.x3_intersection_obstruction()
        self.assertEqual(obstruction["labelled_five_edge_subsets_checked"], 792)
        self.assertEqual(obstruction["subsets_compatible_with_all_intersection_signatures_t_le_1"], 0)

    def test_rooted_support_census(self) -> None:
        census = CHECK.rooted_support_census()
        self.assertEqual(census["degree_sequence_graphs"], 810)
        self.assertEqual(census["lambda_cap_graphs"], 360)
        self.assertEqual(census["lambda_mu_cap_graphs"], 180)
        self.assertEqual(census["lambda_mu_cap_rooted_types"], 1)

    def test_deficit_and_cross_capacity(self) -> None:
        self.assertEqual(len(CHECK.deficit_edges()), 7)
        census = CHECK.cross_deficit_bijection_census()
        self.assertEqual(census["capacity_compatible_bijections"], 4480)
        self.assertEqual(census["t1_incidence_degrees_each_side"], [9, 9, 9, 9, 9, 8, 8])

    def test_marked_line_census(self) -> None:
        packing = CHECK.marked_line_census()
        self.assertEqual(packing["external_third_edge_matching_number"], 2)
        self.assertEqual(
            packing["representative_ordered_packing_counts"],
            {"3,2,0,0": 0, "3,1,1,0": 4, "2,2,1,0": 12, "2,1,1,1": 0},
        )
        self.assertEqual(
            CHECK.labelled_m5_census()["labelled_subsets_after_marked_line_and_root_cross_edge_tests"],
            204,
        )

    def test_weight20_selected_zero_capacity(self) -> None:
        census = CHECK.labelled_m2_capacity_census()
        self.assertEqual(census["all_labelled_two_edge_subsets"], 66)
        self.assertEqual(census["maximum_dynamic_states"], 256)
        self.assertEqual(
            census["after_even_parity_and_global_moments"]["shared_endpoint_24_subsets"],
            [6, 8],
        )

    def test_hostile_controls(self) -> None:
        controls = {row["name"]: row for row in CHECK.imported_controls()}
        self.assertEqual(controls["weight14_five_intersections"]["x"], 1)
        self.assertEqual(controls["weight20_two_intersections"]["x"], 6)
        self.assertTrue(all(row["internal_Ac_equals_3c"] for row in controls.values()))

    def test_line_witnesses_and_norms(self) -> None:
        self.assertTrue(all(CHECK.verify_line_witness(row) for row in CHECK.LINE_WITNESSES.values()))
        self.assertEqual(CHECK.line_graph_moments(7, 5, 20)["unselected_line_squared_norm"], 108)
        self.assertEqual(CHECK.line_graph_moments(10, 2, 6)["unselected_line_squared_norm"], 146)

    def test_status_wall(self) -> None:
        self.assertEqual(self.result["claim_label"], "DERIVED")
        self.assertEqual(self.result["global_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
