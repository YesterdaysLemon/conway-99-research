"""Focused tests for the clean-room Wave 207 verifier."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "wave207_clean_room", HERE / "independent_check.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load independent verifier")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class Wave207CleanRoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = CHECK.build_result()

    def test_m7g_applicability_invariants(self) -> None:
        m7g = self.result["m7g"]
        self.assertEqual(m7g["column_rank"], 4)
        self.assertTrue(m7g["every_three_independent"])
        self.assertEqual(m7g["veronese_rank"], 7)
        self.assertEqual(m7g["quadratic_relation_nullity"], 1)
        self.assertTrue(m7g["displayed_relation_is_linear"])
        self.assertTrue(m7g["displayed_relation_is_quadratic"])
        self.assertEqual(m7g["tensor_relation_composition"], {"1": 4, "2": 4})
        self.assertEqual(m7g["linearizing_relative_sign_classes"], 4)
        for sign_class in m7g["no_one_offdiagonal_audit_by_sign_class"]:
            self.assertEqual(
                sign_class["no_one_offdiagonal_forms_by_rank"],
                {"0": 1, "2": 3},
            )

    def test_concurrent_secant_geometry(self) -> None:
        concurrency = self.result["m7g"]["concurrency"]
        self.assertEqual(concurrency["perfect_matchings_checked"], 105)
        self.assertEqual(concurrency["valid_external_concurrent_matchings"], 4)
        self.assertTrue(concurrency["each_matching_has_a_unique_common_point"])
        self.assertTrue(concurrency["expected_source_pairing_is_recovered"])
        self.assertTrue(
            concurrency["all_valid_matchings_have_no_three_secants_coplanar"]
        )

    def test_relation_enumerator(self) -> None:
        code = self.result["m7g"]["linear_relation_code"]
        self.assertEqual(code["words"], 81)
        self.assertEqual(code["dimension"], 4)
        self.assertEqual(
            code["weight_enumerator"],
            {"0": 1, "4": 24, "5": 16, "6": 32, "8": 8},
        )

    def test_polar_net(self) -> None:
        polar = self.result["m7g"]["polar_net"]
        self.assertEqual(polar["form_space_dimension"], 3)
        self.assertEqual(polar["rank_counts"], {"0": 1, "2": 12, "3": 8, "4": 6})
        self.assertEqual(
            polar["zero_graph_counts"],
            {"2C4": 6, "2K4": 12, "4K2": 8, "K8": 1},
        )

    def test_gram_radical_exact_sequence(self) -> None:
        audit = self.result["gram_radical"]
        self.assertEqual(audit["synthesis_maps_exhausted"], 729)
        self.assertTrue(audit["exact_sequence_checked"])
        example = audit["nontrivial_radical_example"]
        self.assertGreater(example["synthesis_rank"], example["gram_rank"])

    def test_transition_rank_formula_and_rectangular_edges(self) -> None:
        transition = self.result["transition_rank"]
        self.assertEqual(
            transition["square_6_by_6_ranks"],
            {"0": 0, "1": 1, "2": 3, "3": 6, "4": 10, "5": 15, "6": 21},
        )
        for case in transition["rectangular_edge_cases"]:
            self.assertEqual(case["symmetric_transition_rank"], case["expected"])

    def test_four_center_abstract_control(self) -> None:
        control = self.result["four_center_control"]
        self.assertEqual(control["cumulative_symmetric_square_ranks"], [21, 41, 56, 66])
        self.assertEqual(control["restriction_rank_on_25_K_coordinates"], 25)
        self.assertEqual(control["local_six_space_gram_ranks"], [6, 6, 6, 6])

    def test_point_code_supplement(self) -> None:
        supplement = self.result["point_code_supplement"]
        self.assertEqual(supplement["a_dot_a_mod3"], 2)
        self.assertEqual(supplement["b_dot_b_mod3_from_G_squared_equals_G_minus_J"], 2)
        self.assertTrue(supplement["b_is_nonzero"])
        self.assertEqual(supplement["sharpened_weight_upper"], 23)
        self.assertEqual(
            supplement["rank_zero_K8_case"]["verdict"], "EXCLUDED_CONDITIONALLY"
        )
        self.assertEqual(
            supplement["no_one_offdiagonal_extension"][
                "excluded_affine_forms_per_relative_sign_class"
            ],
            {"rank_0": 1, "rank_2": 3},
        )

    def test_signed_neighbor_distance_certificate(self) -> None:
        audit = self.result["signed_neighbor_distance"]
        self.assertTrue(audit["base_function_nonnegative_on_all_neighbor_ranges"])
        self.assertEqual(audit["base_table_entries_checked"], 75)
        self.assertEqual(
            audit["weight_10"]["base_equality_types"],
            [[0, 0], [0, 3], [1, 1], [3, 0]],
        )
        self.assertEqual(audit["weight_11"]["global_farkas_sum"], -60)
        self.assertTrue(audit["weight_11"]["all_phi_values_nonnegative"])
        self.assertEqual(audit["derived_minimum_distance_lower_bound"], 12)

    def test_weight_fourteen_control_is_nongraphical(self) -> None:
        control = self.result["weight_fourteen_aggregate_control"]
        self.assertTrue(control["all_local_7K2_records_feasible"])
        self.assertEqual(
            control["aggregate_identities"]["matching_totals"],
            {"h_pp": 6, "h_nn": 6, "h_pn": 0},
        )
        self.assertEqual(
            control["positive_internal_degree_multiset"],
            [0, 0, 0, 0, 0, 6, 6],
        )
        self.assertFalse(control["is_graph"])
        self.assertFalse(control["is_codeword"])

    def test_restricted_rank_four_local_certificate(self) -> None:
        certificate = self.result["local_rank_four_certificate"]
        self.assertEqual(certificate["vertices"], 23)
        self.assertEqual(certificate["edges"], 51)
        self.assertEqual(certificate["selected_intersections"], [[0, 3]])
        self.assertEqual(certificate["form_rank"], 4)
        self.assertEqual(certificate["zero_graph"], "2C4")
        self.assertTrue(certificate["local_adjacency_times_b_zero_on_23_coordinates"])
        self.assertTrue(certificate["does_not_check_76_outside_coordinates_of_Ab"])
        self.assertEqual(certificate["b_norm_mod3"], 2)
        self.assertEqual(certificate["maximum_induced_degree"], 8)
        self.assertEqual(certificate["graph_triangles"], 11)
        self.assertEqual(certificate["induced_triangular_prisms"], 0)
        self.assertEqual(certificate["edges_missing_their_required_common_neighbor_inside"], 18)
        self.assertEqual(certificate["verdict"], "RESTRICTED_LOCAL_COMPATIBILITY_ONLY")

    def test_weight_fourteen_composition_reduction(self) -> None:
        reduction = self.result["weight_fourteen_composition"]
        self.assertEqual(reduction["one_plus_thirteen"]["admissible_types_checked"], 24)
        self.assertEqual(reduction["one_plus_thirteen"]["global_sum"], -35)
        self.assertEqual(reduction["four_plus_ten"]["admissible_types_checked"], 51)
        self.assertEqual(reduction["four_plus_ten"]["global_sum"], -12)
        self.assertTrue(reduction["one_plus_thirteen"]["all_pointwise_values_nonnegative"])
        self.assertTrue(reduction["four_plus_ten"]["all_pointwise_values_nonnegative"])
        self.assertEqual(reduction["only_surviving_composition"], [7, 7])
        self.assertFalse(reduction["weight_14_excluded"])
        self.assertEqual(reduction["balanced_branch"], "UNKNOWN")

    def test_global_scope_wall(self) -> None:
        wall = self.result["scope_wall"]
        self.assertEqual(wall["rank_11_endpoint"], "UNKNOWN")
        self.assertEqual(wall["conway_99"], "UNKNOWN")
        self.assertFalse(wall["graph_constructed"])
        self.assertFalse(wall["counterexample_or_nonexistence_proof"])


if __name__ == "__main__":
    unittest.main()
