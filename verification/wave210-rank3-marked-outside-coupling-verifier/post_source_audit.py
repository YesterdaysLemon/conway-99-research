#!/usr/bin/env python3
"""Post-freeze comparison against the sealed Wave 210 discovery package."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

import independent_check as independent


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_DIR = ROOT / "attempts" / "wave210-rank3-marked-outside-coupling-proof-a"
SOURCE_SCRIPT = SOURCE_DIR / "exact_check.py"
OUTPUT = HERE / "post-source-audit.json"
EXPECTED_OUTER_SHA256 = "d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_source():
    spec = importlib.util.spec_from_file_location("sealed_wave210_discovery", SOURCE_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_manifest_text(text: str) -> tuple[tuple[str, str], ...]:
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        digest, path = line.split(maxsplit=1)
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest)
        rows.append((digest, path.replace("\\", "/")))
    return tuple(rows)


def manifest_text_valid(text: str) -> bool:
    try:
        rows = parse_manifest_text(text)
        return bool(rows) and all(sha256(ROOT / path) == digest for digest, path in rows)
    except (AssertionError, FileNotFoundError, ValueError):
        return False


def validate_manifests(source) -> dict[str, object]:
    outer = SOURCE_DIR / "package-manifest.sha256"
    outer_text = outer.read_text(encoding="utf-8")
    outer_rows = parse_manifest_text(outer_text)
    assert sha256(outer) == EXPECTED_OUTER_SHA256
    assert manifest_text_valid(outer_text)

    package_entries = {
        Path(path).name
        for _, path in outer_rows
        if path.startswith("attempts/wave210-rank3-marked-outside-coupling-proof-a/")
    }
    actual_package_files = {path.name for path in SOURCE_DIR.iterdir() if path.is_file() and path.name != outer.name}
    assert package_entries == actual_package_files
    assert "agents/2026-07-31-wave210-rank3-coupling-proof-a.md" in {path for _, path in outer_rows}

    input_text = (SOURCE_DIR / "input-freeze.sha256").read_text(encoding="utf-8")
    assert manifest_text_valid(input_text)
    assert dict(source.verify_inputs()) == {path: digest for digest, path in parse_manifest_text(input_text)}

    mutated = list(outer_text)
    first_hex = next(i for i, c in enumerate(mutated) if c in "0123456789abcdef")
    mutated[first_hex] = "0" if mutated[first_hex] != "0" else "1"
    corrupt_manifest_rejected = not manifest_text_valid("".join(mutated))
    assert corrupt_manifest_rejected
    return {
        "expected_outer_manifest_sha256": EXPECTED_OUTER_SHA256,
        "observed_outer_manifest_sha256": sha256(outer),
        "all_outer_manifest_entries_valid": True,
        "package_file_coverage_exact": True,
        "frozen_upstream_inputs_valid": True,
        "in_memory_manifest_corruption_rejected": corrupt_manifest_rejected,
    }


def source_group_actions(source):
    support_autos = tuple(source.support_automorphisms())
    for swap in (False, True):
        for line_perm4 in permutations(range(4)):
            line_map = tuple(
                (4 + line_perm4[i] if swap else line_perm4[i]) for i in range(4)
            ) + tuple(
                (line_perm4[i] if swap else 4 + line_perm4[i]) for i in range(4)
            )
            for p_auto in support_autos:
                for n_auto in support_autos:
                    support_map = [0] * 14
                    for old in range(14):
                        old_negative = old >= 7
                        destination_negative = old_negative ^ swap
                        auto = n_auto if destination_negative else p_auto
                        support_map[old] = (7 if destination_negative else 0) + auto[old % 7]
                    yield swap, line_perm4, p_auto, n_auto, (line_map, tuple(support_map))


def discovery_orbits(source) -> tuple[tuple[independent.Case, ...], ...]:
    actions = tuple(source_group_actions(source))
    rows = []
    for representative, claimed_size in source.case_orbits():
        orbit = tuple(sorted({
            source.transform_case(representative, line_perm, p_auto, n_auto, swap)
            for swap, line_perm, p_auto, n_auto, _ in actions
        }))
        assert len(orbit) == claimed_size
        rows.append(orbit)
    return tuple(rows)


def source_final_rows(source) -> tuple[dict[str, object], ...]:
    rows = []
    for orbit_index, (representative, orbit_size) in enumerate(source.case_orbits()):
        solutions = source.abstract_solutions(representative)
        solution_rows = []
        preliminary = 0
        assignment_branches = 0
        for solution, optional in solutions:
            mask = source.solution_availability(solution)
            preliminary |= mask
            assignment_branches += mask.bit_count()
            solution_rows.append((solution, optional, mask))
        final = 0
        for matching_index in source.bit_indices(preliminary):
            for solution, optional, mask in solution_rows:
                if (mask >> matching_index) & 1 and source.selected_local_extension(
                    representative, solution, optional, matching_index
                ) is not None:
                    final |= 1 << matching_index
                    break
        rows.append({
            "orbit_index": orbit_index,
            "representative": representative,
            "orbit_size": orbit_size,
            "abstract_solutions": tuple(solutions),
            "assignment_branches": assignment_branches,
            "preliminary_indices": tuple(source.bit_indices(preliminary)),
            "final_indices": tuple(source.bit_indices(final)),
        })
    return tuple(rows)


def expand_source_triples(source, rows: tuple[dict[str, object], ...]) -> tuple[set[independent.Case], set[tuple[independent.Case, tuple[int, ...]]]]:
    source_matchings = tuple(source.valid_deficit_matchings())
    actions = tuple(source_group_actions(source))
    cases: set[independent.Case] = set()
    triples: set[tuple[independent.Case, tuple[int, ...]]] = set()
    for row in rows:
        if not row["final_indices"]:
            continue
        representative = row["representative"]
        for swap, line_perm, p_auto, n_auto, action in actions:
            transformed_case = source.transform_case(representative, line_perm, p_auto, n_auto, swap)
            cases.add(transformed_case)
            for index in row["final_indices"]:
                transformed_matching = independent.transform_matching(source_matchings[index], action)
                triples.add((transformed_case, transformed_matching))
    return cases, triples


def compare_complete_sets(source) -> dict[str, object]:
    own_h = set(independent.marked_graphs())
    source_h = set(source.marked_graphs())
    own_cases = set(independent.labelled_cases())
    source_cases = set(source.labelled_cases())
    own_matchings = set(independent.deficit_configurations()[0])
    source_matchings = set(source.valid_deficit_matchings())
    assert own_h == source_h
    assert own_cases == source_cases
    assert own_matchings == source_matchings

    own_orbits = {tuple(orbit) for orbit in independent.case_orbits()}
    src_orbits_tuple = discovery_orbits(source)
    source_orbit_set = {tuple(orbit) for orbit in src_orbits_tuple}
    assert own_orbits == source_orbit_set

    own_rows = independent.orbit_coupling()
    src_rows = source_final_rows(source)
    assert len(own_rows) == len(src_rows) == 33
    for own, submitted in zip(own_rows, src_rows):
        assert own["representative"] == submitted["representative"]
        assert own["orbit_size"] == submitted["orbit_size"]
        assert set(independent.abstract_solutions(own["representative"])) == set(submitted["abstract_solutions"])
        assert own["abstract_assignment_branches_per_representative"] == submitted["assignment_branches"]
        assert own["pre_local_matching_indices"] == submitted["preliminary_indices"]
        assert own["final_matching_indices"] == submitted["final_indices"]

    own_surviving_cases, own_triples = independent.expanded_survivors()
    source_surviving_cases, source_triples = expand_source_triples(source, src_rows)
    assert own_surviving_cases == source_surviving_cases
    assert own_triples == source_triples
    own_surviving_h = {case[0] for case in own_surviving_cases}
    source_surviving_h = {case[0] for case in source_surviving_cases}
    assert own_surviving_h == source_surviving_h

    orbit_records = tuple(tuple(orbit) for orbit in sorted(independent.case_orbits(), key=lambda row: row[0]))
    return {
        "all_204_labelled_H_equal": True,
        "all_20928_labelled_cases_equal": True,
        "all_4480_deficit_bijections_equal": True,
        "all_33_orbit_member_sets_equal": True,
        "all_orbit_abstract_solution_sets_equal": True,
        "all_orbit_matching_index_sets_equal": True,
        "all_96_surviving_labelled_H_equal": True,
        "all_1536_surviving_labelled_cases_equal": True,
        "all_55296_surviving_labelled_triples_equal": True,
        "digests": {
            "H": independent.digest_records(own_h),
            "cases": independent.digest_records(own_cases),
            "deficit_bijections": independent.digest_records(own_matchings),
            "orbit_partition": independent.digest_records(orbit_records),
            "surviving_H": independent.digest_records(own_surviving_h),
            "surviving_cases": independent.digest_records(own_surviving_cases),
            "surviving_triples": independent.digest_records(own_triples),
        },
    }


def compare_all_f_and_local(source) -> dict[str, object]:
    own_matchings = independent.deficit_configurations()[0]
    source_matchings = tuple(source.valid_deficit_matchings())
    source_index = {matching: index for index, matching in enumerate(source_matchings)}
    local_vectors_equal = True
    for matching in own_matchings:
        own_built = independent.columns_for_matching(matching)
        assert own_built is not None
        own_columns, own_residual = own_built
        source_columns_frozen, _ = source.concrete_columns(source_index[matching])
        source_columns = tuple(sum(1 << v for v in column) for column in source_columns_frozen)
        source_row = source.deficit_columns(matching)
        assert source_row is not None
        source_residual = source_row[1]
        assert own_columns == source_columns
        assert own_residual == source_residual
        assert independent.observed_gram(own_columns) == independent.GRAM
        assert source.verify_F_identity(source_columns_frozen)
        own_local = independent.local_one_factor_counts(own_columns)
        submitted_local = source.local_matching_counts(source_columns_frozen)
        if own_local != submitted_local:
            local_vectors_equal = False
            break
    assert local_vectors_equal
    source_census = source.base_local_matching_census()
    own_census = independent.base_local_census()
    assert source_census["configurations_admitting_all_14_local_matchings"] == own_census["configurations_feasible_at_all_14_support_vertices"] == 4480
    assert source_census["individual_neighborhood_perfect_matching_count_distribution"] == own_census["perfect_matching_count_distribution"]
    return {
        "all_4480_column_multisets_equal_in_canonical_order": True,
        "all_4480_residual_matrices_equal": True,
        "all_4480_gram_checks_equal": True,
        "all_62720_local_matching_count_vectors_equal": True,
        "rank_over_Q": independent.integer_rank(independent.GRAM),
        "local_count_distribution": own_census["perfect_matching_count_distribution"],
    }


def replay_control(control: dict[str, object]) -> dict[str, object]:
    columns = tuple(sum(1 << v for v in support) for support in control["F_columns_support_neighbors"])
    assert len(columns) == 85
    gram_ok = independent.observed_gram(columns) == independent.GRAM
    case_data = control["case"]
    h = tuple(tuple(edge) for edge in case_data["H"])
    case = (
        h,
        tuple(tuple(block) for block in case_data["P_blocks"]),
        tuple(tuple(block) for block in case_data["N_blocks"]),
    )
    selected_ids = tuple(control["selected_outside_column_indices"])
    selected_vertices = tuple(control["selected_outside_vertex_ids"])
    assert selected_vertices == tuple(14 + index for index in selected_ids)
    assert len(selected_ids) == len(set(selected_ids)) == 5

    edges = frozenset(tuple(edge) for edge in control["selected_union_edges"])
    rows = independent.adjacency(99, edges)
    triangles = tuple(tuple(line) for line in control["selected_triangles"])
    triangle_cliques = all(all((rows[a] >> b) & 1 for a, b in combinations(line, 2)) for line in triangles)
    polar_counts = all(
        sum((rows[a] >> b) & 1 for a in triangles[i] for b in triangles[j] if a != b)
        == (4 if (i, j) in h else independent.POLAR[i][j])
        for i, j in independent.LINE_PAIRS
    )
    selected_union = set(range(14)) | set(selected_vertices)
    caps = all(
        ((rows[a] & rows[b]) & sum(1 << v for v in selected_union)).bit_count()
        <= (1 if (rows[a] >> b) & 1 else 2)
        for a, b in combinations(sorted(selected_union), 2)
    )
    signed = [1] * 7 + [-1] * 7 + [0] * 85
    eigen = all(
        sum(signed[v] for v in selected_union if (rows[u] >> v) & 1) == 3 * signed[u]
        for u in selected_union
    )
    fixed_outside = frozenset(
        independent.pair(a - 14, b - 14)
        for a, b in edges if a >= 14 and b >= 14
    )
    local = independent.local_one_factor_counts(columns, fixed_outside)
    local_ok = local is not None and list(local) == control["local_perfect_matching_counts"]

    blocks, _ = independent.block_and_incidence(case)
    containment = all(
        (blocks[a] | blocks[b]) & ~columns[selected_ids[z]] == 0
        for z, (a, b) in enumerate(h)
    )
    outside_outside_edges = sum(a >= 14 and b >= 14 for a, b in edges)
    degree_sequence = tuple(row.bit_count() for row in rows)
    not_completion = (
        len(selected_union) == 19
        and outside_outside_edges <= 10
        and degree_sequence.count(0) >= 80
        and not all(degree == 14 for degree in degree_sequence)
    )
    checks = {
        "F_gram": gram_ok,
        "distinct_selected_column_copies": True,
        "required_support_containment": containment,
        "selected_triangles_are_cliques": triangle_cliques,
        "all_28_polar_counts": polar_counts,
        "induced_lambda_mu_caps": caps,
        "induced_Ac_equals_3c": eigen,
        "all_14_local_one_factors": local_ok,
        "demonstrably_not_a_D_completion": not_completion,
    }
    assert all(checks.values())
    return checks


def replay_hostile_controls(source) -> dict[str, object]:
    sealed = json.loads((SOURCE_DIR / "hostile-controls.json").read_text(encoding="utf-8"))
    rebuilt = source.build_hostile_controls()
    assert sealed == rebuilt
    assert len(sealed["controls"]) == 3
    replays = {str(control["orbit_index"]): replay_control(control) for control in sealed["controls"]}

    mutated = json.loads(json.dumps(sealed["controls"][0]))
    mutated["F_columns_support_neighbors"][0] = mutated["F_columns_support_neighbors"][0][1:]
    coordinate_mutation_rejected = independent.observed_gram(
        tuple(sum(1 << v for v in support) for support in mutated["F_columns_support_neighbors"])
    ) != independent.GRAM
    assert coordinate_mutation_rejected

    edge_mutated = json.loads(json.dumps(sealed["controls"][0]))
    first_triangle = edge_mutated["selected_triangles"][0]
    removed = list(independent.pair(first_triangle[0], first_triangle[1]))
    edge_mutated["selected_union_edges"].remove(removed)
    try:
        replay_control(edge_mutated)
        triangle_mutation_rejected = False
    except AssertionError:
        triangle_mutation_rejected = True
    assert triangle_mutation_rejected
    return {
        "sealed_controls_equal_fresh_discovery_rebuild": True,
        "independent_replays": replays,
        "single_F_coordinate_mutation_rejected": coordinate_mutation_rejected,
        "mandatory_triangle_edge_deletion_rejected": triangle_mutation_rejected,
        "controls_are_partial_19_point_objects_not_99_vertex_completions": True,
    }


def audit_discovery_outputs(source) -> dict[str, object]:
    sealed_results = json.loads((SOURCE_DIR / "exact-results.json").read_text(encoding="utf-8"))
    fresh_results = source.build_results()
    assert sealed_results == fresh_results
    assert sealed_results["claim_label"] == "DERIVED"
    assert sealed_results["global_status"] == "UNKNOWN"
    unresolved = sealed_results["unresolved_outside_block"]
    assert unresolved["status"].startswith("not solved")
    assert "D^2+D" in unresolved["bottom_right_block_equation"]
    return {
        "sealed_exact_results_equal_fresh_discovery_rebuild": True,
        "claim_label": sealed_results["claim_label"],
        "global_status": sealed_results["global_status"],
        "D_block_status": unresolved["status"],
        "no_global_completion_or_exclusion": True,
    }


def build_audit() -> dict[str, object]:
    source = load_source()
    manifests = validate_manifests(source)
    complete_sets = compare_complete_sets(source)
    f_and_local = compare_all_f_and_local(source)
    controls = replay_hostile_controls(source)
    outputs = audit_discovery_outputs(source)
    verdict_checks = {
        "manifests": all(value is True or isinstance(value, str) for value in manifests.values()),
        "complete_labelled_sets": all(value is True or isinstance(value, dict) for value in complete_sets.values()),
        "F_and_local": all(value is True or isinstance(value, (int, dict)) for value in f_and_local.values()),
        "hostile_controls": controls["controls_are_partial_19_point_objects_not_99_vertex_completions"],
        "status_wall": outputs["claim_label"] == "DERIVED" and outputs["global_status"] == "UNKNOWN",
    }
    assert all(verdict_checks.values())
    return {
        "verdict": "PASS / NO VETO",
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "manifest_audit": manifests,
        "complete_set_comparison": complete_sets,
        "F_and_local_comparison": f_and_local,
        "hostile_control_audit": controls,
        "discovery_output_rebuild": outputs,
        "restriction_audit": {
            "204_H_generated_labelled_before_any_quotient": True,
            "20928_packings_generated_labelled_before_any_quotient": True,
            "4480_F_configurations_generated_from_all_5040_bijections": True,
            "polar_order_48_proved_by_bruteforce_full_8_point_automorphism_enumeration": True,
            "support_order_4_proved_by_bruteforce_full_7_point_automorphism_enumeration": True,
            "case_action_order_768_closed_faithful_and_Burnside_checked": True,
            "no_target_graph_automorphism_assumed": True,
            "no_D_completion_constructed_or_excluded": True,
        },
        "verdict_checks": verdict_checks,
        "limitations": [
            "the verified result is conditional on the frozen Wave 209 weight-14 branch",
            "the 55296 survivors satisfy selected-union and local necessary conditions only",
            "the unknown 85x85 outside adjacency block D and all global SRG equations remain unresolved",
            "Conway-99 remains UNKNOWN",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payload = build_audit()
    if args.write:
        OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", OUTPUT)
    elif args.verify:
        assert json.loads(OUTPUT.read_text(encoding="utf-8")) == payload
        print("post-source audit PASS / NO VETO")
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
