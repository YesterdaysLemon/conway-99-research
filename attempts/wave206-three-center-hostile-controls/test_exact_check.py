"""Mutation-focused tests for the Wave 206 hostile-control certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "wave206_hostile_exact_check", HERE / "exact_check.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.fixture(scope="module")
def result() -> dict:
    return MODULE.analyze()


def test_frozen_results_reproduce(result: dict) -> None:
    frozen = json.loads((HERE / "exact-results.json").read_text(encoding="utf-8"))
    assert result == frozen


def test_shared_incidence_keeps_g_and_H_but_changes_tau(result: dict) -> None:
    collision = result["shared_incidence_tau_collision"]
    assert collision["same_labelled_99x231_incidence"]
    assert collision["same_full_g_matrix"]
    assert collision["same_full_H_matrix"]
    assert collision["different_ordered_tau_entries"] == 209952
    assert collision["tau_contraction_sum_z_zero"]
    assert collision["claim_label"] == "REFUTED"


def test_fixed_y_rank_bound_is_sharp_and_data_vary(result: dict) -> None:
    package = result["fixed_y_rank21_controls"]
    assert package["universal_dimension_bound"] == 21
    assert package["rank_bound_attained_in_both_controls"]
    assert package["diagonal_distribution_varies"]
    assert package["tau_entry_distribution_varies"]
    for control in package["controls"].values():
        assert control["fixed_y_slice_rank_over_F3"] == 21
        assert control["compressed_operator_coordinate_rank_over_F3"] == 21
        assert control["fixed_y_slice_row_sums_zero"]
        assert control["fixed_y_slice_y_row_equals_g_y_star"]
        assert control["fixed_y_slice_diagonal_equals_H_y_star"]


def test_missing_target_premises_and_status_wall_are_explicit(result: dict) -> None:
    collision = result["shared_incidence_tau_collision"]
    assert len(collision["missing_target_premises"]) >= 8
    assert collision["incidence"]["connected_component_sizes"] == [27, 36, 36]
    assert collision["realizations"]["A"]["distinct_projective_direction_count"] == 19
    assert result["fixed_y_rank21_controls"]["missing_target_premises"]
    assert result["bounded_search_ledger"]["nonhit_is_evidence_of_nonexistence"] is False
    assert result["status"]["Conway-99"] == "UNKNOWN"
    assert result["status"]["Q>=7060"] == "NOT PROVED"
    assert result["status"]["automorphism_assumption"] == "NONE"


def test_reflection_word_mutation_is_rejected() -> None:
    certificate = MODULE.load_certificate()
    mutated = copy.deepcopy(certificate)
    mutated["projector_pool"]["reflection_vectors"][0] = [0] * 11
    with pytest.raises(AssertionError, match="singular root"):
        MODULE.projector_pool(mutated)


def test_simplex_mutation_is_rejected() -> None:
    certificate = MODULE.load_certificate()
    mutated = copy.deepcopy(certificate)
    mutated["simplex_coefficient_vectors"][0][0] = 1
    with pytest.raises(AssertionError, match="simplex 0"):
        MODULE.projector_pool(mutated)


def test_incidence_orbit_mutation_is_rejected() -> None:
    certificate = MODULE.load_certificate()
    mutated = copy.deepcopy(certificate)
    mutated["shared_incidence"]["full_orbits"][1]["starter"] = [0, 1, 5]
    with pytest.raises(AssertionError):
        MODULE.build_incidence(mutated)
