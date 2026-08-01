from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "wave206_three_center_exact_check", HERE / "exact_check.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load checker")
CHECK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK
SPEC.loader.exec_module(CHECK)
RESULT = CHECK.analyze()


class ThreeCenterProofATests(unittest.TestCase):
    def test_frozen_inputs(self) -> None:
        self.assertEqual(RESULT["inputs"], CHECK.EXPECTED_INPUTS)

    def test_operator_gram_theorem(self) -> None:
        theorem = RESULT["three_center_operator_theorem"]
        self.assertTrue(theorem["symmetric"])
        self.assertEqual(theorem["rank_bound"], 21)
        self.assertTrue(theorem["row_sums_zero"])
        self.assertEqual(theorem["diagonal"], "T_y[x,x]=h_yx")
        self.assertEqual(theorem["root_row"], "T_y[y,x]=g_yx")

    def test_coordinate_moment_model(self) -> None:
        model = RESULT["coordinate_moment_model"]
        self.assertEqual(
            model["global_coordinate_sum"],
            "sum_x r_x^(y)=0 coordinatewise, from sum_x P_x=0",
        )
        self.assertEqual(
            model["weighted_relation_projection"],
            "for every c with sum_x c_x P_x=0, "
            "sum_x c_x r_x^(y)=0 coordinatewise",
        )
        for control in model["control_checks"].values():
            self.assertEqual(
                control["g"], control["two_times_coordinate_sum"]
            )
            self.assertEqual(
                control["h"], control["quadratic_coordinate_value"]
            )
            self.assertEqual(
                control["coordinate_sum_mod_3"],
                control["claimed_t_integer"] % 3,
            )

    def test_graph_pattern_counts(self) -> None:
        geometry = RESULT["graph_patterns_and_fibers"]
        self.assertEqual(
            geometry["fixed_nonedge_xy_pattern_counts"],
            {
                "z_adjacent_to_both": 2,
                "z_adjacent_to_y_only": 12,
                "z_adjacent_to_x_only": 12,
                "z_adjacent_to_neither": 71,
            },
        )
        self.assertEqual(
            geometry["nonedge_third_center_marked_pair_distribution"],
            {"star_block_pairs": 21, "vertices_per_pair": 4, "total": 84},
        )

    def test_fiber_matching_lemma(self) -> None:
        geometry = RESULT["graph_patterns_and_fibers"]
        self.assertTrue(
            geometry["fiber_graph_is_subgraph_of_opposite_corner_matching"]
        )
        self.assertEqual(geometry["possible_induced_fiber_graph_count"], 4)
        self.assertEqual(
            geometry[
                "same_endpoint_hypothetical_edge_forces_prism_cross_edges"
            ],
            [["y", "a_p"], ["b0", "x_p0"], ["b1", "x_p1"]],
        )

    def test_marked_coordinate_census(self) -> None:
        census = RESULT["marked_coordinate_low_t_census"]["census"]
        self.assertEqual(
            census["6"]["counts_by_h_and_r"], {"1,1": 18}
        )
        self.assertEqual(
            census["7"]["counts_by_h_and_r"],
            {
                "0,0": 288,
                "0,1": 9,
                "1,0": 144,
                "1,1": 180,
                "2,0": 144,
            },
        )

    def test_edge_module_census(self) -> None:
        census = RESULT["edge_module_census"]
        self.assertEqual(
            census["labelled_degree_two_biadjacency_matrices"], 67_950
        )
        self.assertEqual(census["unique_compressions"], 130)

    def test_every_edge_placement_has_every_tau(self) -> None:
        for control in RESULT["marginal_tau_census"].values():
            for values in control[
                "edge_tau_values_by_common_block"
            ].values():
                self.assertEqual(values, [0, 1, 2])

    def test_every_nonedge_placement_has_every_tau(self) -> None:
        for control in RESULT["marginal_tau_census"].values():
            for values in control[
                "nonedge_tau_values_by_marked_pair"
            ].values():
                self.assertEqual(values, [0, 1, 2])

    def test_scalar_contraction_ledgers(self) -> None:
        for control in RESULT["marginal_tau_census"].values():
            self.assertEqual(control["marginal_assignment_size"], 97)
            self.assertEqual(
                control["marginal_tau_sum"],
                control["required_remaining_tau_sum"],
            )
            self.assertFalse(
                control[
                    "shared_operator_sum_or_shared_231_columns_imposed"
                ]
            )
            self.assertTrue(
                control["root_relative_placement_multiplicities_imposed"]
            )
            self.assertFalse(
                control["x_z_adjacency_or_pair_module_imposed"]
            )

    def test_formal_zero_sum_controls(self) -> None:
        for control in RESULT["formal_zero_sum_operator_controls"].values():
            self.assertEqual(control["operator_count"], 99)
            self.assertTrue(control["operator_sum_zero"])
            self.assertTrue(control["tau_gram_symmetric"])
            self.assertTrue(control["tau_gram_row_sums_zero"])
            self.assertLessEqual(control["tau_gram_rank"], 21)
            self.assertFalse(
                control[
                    "residual_is_claimed_to_be_a_graph_projector_compression"
                ]
            )

    def test_status_wall(self) -> None:
        conclusions = RESULT["conclusions"]
        self.assertFalse(
            conclusions[
                "root_relation_and_forced_y_star_placement_determine_tau"
            ]
        )
        self.assertEqual(
            conclusions[
                "full_labelled_three_center_graph_type_determines_tau"
            ],
            "UNKNOWN",
        )
        self.assertEqual(
            conclusions["combined_shared_operator_and_graph_module_completion"],
            "UNKNOWN",
        )
        self.assertFalse(conclusions["rank_11_endpoint_excluded"])
        self.assertEqual(conclusions["conway_99_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
