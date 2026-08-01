"""Exact three-center placement and compression checks for Wave 206 proof A.

The checker is solver-free.  It reuses only the frozen Wave 205 exact
finite-field routines after checking their sealed package manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


FIELD = 3
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EXPECTED_INPUTS = {
    "attempts/wave206-three-center-global-extension/protocol.md":
        "66c20334e284a26cc771ee86d97e678cb67b6efb4648b2af2fffe480fb5a9103",
    "verification/2026-07-29-wave205-integration-audit.md":
        "f50b5591cb0e1e3dfdd835a22fd9156dd3a2a039323388889a6fa5e756a0a297",
    "verification/2026-07-29-wave205-orchestrator.md":
        "9b9711ad4b9ac902161833b4a5825404e95ba6f443462ac3d79532df704b2deb",
    "verification/wave205-fourth-trace-globalization-verifier/package-manifest.sha256":
        "b93f65f72db94539c7d42d7eca6debbaf3a5c4a401db3b812a80549bcb9b8325",
    "attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256":
        "2c9976b6cb07a3036df07fd0e7ceb7ffce6a339651d604fcecdcf8c0c3da3d96",
    "attempts/wave205-global-fourth-moment-proof-b/package-manifest.sha256":
        "a91a2a1cdbc129fa66e9d63b34031a774d5af78c458d18d9a1aadd7e4be217e7",
}
WAVE205_REQUIRED = {
    "attempts/wave205-nonedge-fourth-trace-proof-a/controls.json":
        "e52c068f5fdba18110debdd1455195ec22145f07993437b5438e8f77ae03fdcf",
    "attempts/wave205-nonedge-fourth-trace-proof-a/exact_check.py":
        "3532d6ac65c46003ae313409fa5f6e7e3b99131a51982d2171eda2697f772297",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_inputs() -> dict[str, str]:
    observed = {
        relative: sha256(ROOT / relative) for relative in EXPECTED_INPUTS
    }
    if observed != EXPECTED_INPUTS:
        raise AssertionError(
            {"expected_inputs": EXPECTED_INPUTS, "observed_inputs": observed}
        )
    manifest_path = (
        ROOT
        / "attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256"
    )
    manifest_entries = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        manifest_entries[relative] = digest
    for relative, digest in WAVE205_REQUIRED.items():
        if manifest_entries.get(relative) != digest:
            raise AssertionError("Wave205 manifest entry changed")
        if sha256(ROOT / relative) != digest:
            raise AssertionError("Wave205 required file bytes changed")
    return observed


def load_wave205() -> Any:
    path = ROOT / "attempts/wave205-nonedge-fourth-trace-proof-a/exact_check.py"
    spec = importlib.util.spec_from_file_location(
        "wave205_nonedge_frozen_for_wave206", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load frozen Wave205 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


W = load_wave205()
Matrix = list[list[int]]


def flatten(matrix: Matrix) -> tuple[int, ...]:
    return tuple(value for row in matrix for value in row)


def matrix_zero(size: int) -> Matrix:
    return [[0] * size for _ in range(size)]


def matrix_sum(matrices: Iterable[Matrix]) -> Matrix:
    result = matrix_zero(7)
    for matrix in matrices:
        result = W.matrix_add(result, matrix)
    return result


def matrix_negative(matrix: Matrix) -> Matrix:
    return W.scalar_matrix(2, matrix)


def trace_pair(left: Matrix, right: Matrix) -> int:
    return W.trace(W.matrix_multiply(left, right))


def permute_matrix_base_to_target(matrix: Matrix, mapping: list[int]) -> Matrix:
    """Relabel base index i as target index mapping[i]."""

    inverse = [0] * 7
    for base, target in enumerate(mapping):
        inverse[target] = base
    return [
        [matrix[inverse[row]][inverse[column]] for column in range(7)]
        for row in range(7)
    ]


def controls() -> list[dict[str, Any]]:
    path = ROOT / "attempts/wave205-nonedge-fourth-trace-proof-a/controls.json"
    return json.loads(path.read_text(encoding="utf-8"))["controls"]


def cross_from_control(certificate: dict[str, Any]) -> Matrix:
    return [
        [int(value) for value in row]
        for row in certificate["cross_gram_rows"]
    ]


def y_compression_from_fixed_pair(certificate: dict[str, Any]) -> Matrix:
    # Wave205 writes rows for x and columns for y.
    cross = cross_from_control(certificate)
    return W.matrix_multiply(W.transpose(cross), cross)


def y_compression_from_third_nonedge(certificate: dict[str, Any]) -> Matrix:
    # Here the displayed special rows are assigned to the fixed root y.
    cross = cross_from_control(certificate)
    return W.matrix_multiply(cross, W.transpose(cross))


def binary_degree_two_matrices() -> Iterable[Matrix]:
    patterns = [
        list(pattern)
        for pattern in itertools.product((0, 1), repeat=6)
        if sum(pattern) == 2
    ]

    def recurse(
        rows: Matrix, row_index: int, remaining_columns: list[int]
    ) -> Iterable[Matrix]:
        if row_index == 6:
            if remaining_columns == [0] * 6:
                yield rows
            return
        rows_after = 5 - row_index
        for row in patterns:
            remaining = [
                remaining_columns[column] - row[column]
                for column in range(6)
            ]
            if min(remaining) < 0:
                continue
            if any(value > rows_after for value in remaining):
                continue
            yield from recurse(rows + [row], row_index + 1, remaining)

    yield from recurse([], 0, [2] * 6)


def full_edge_cross_gram(incidence: Matrix) -> Matrix:
    return (
        [[0] + [1] * 6]
        + [
            [1]
            + [W.mod(1 + incidence[row][column]) for column in range(6)]
            for row in range(6)
        ]
    )


def edge_compression_records() -> tuple[int, list[dict[str, Any]]]:
    unique: dict[tuple[int, ...], dict[str, Any]] = {}
    labelled_count = 0
    for incidence in binary_degree_two_matrices():
        cross = full_edge_cross_gram(incidence)
        compression = W.matrix_multiply(cross, W.transpose(cross))
        unique.setdefault(
            flatten(compression),
            {
                "compression": compression,
                "incidence": incidence,
            },
        )
        labelled_count += 1
    records = [unique[key] for key in sorted(unique)]
    if labelled_count != 67_950 or len(records) != 130:
        raise AssertionError("edge-module census changed")
    return labelled_count, records


def edge_options_at_block(
    base_records: list[dict[str, Any]], common_block: int
) -> list[dict[str, Any]]:
    mapping = list(range(7))
    mapping[0], mapping[common_block] = (
        mapping[common_block],
        mapping[0],
    )
    return [
        {
            "compression": permute_matrix_base_to_target(
                record["compression"], mapping
            ),
            "base_record_index": index,
            "base_incidence": record["incidence"],
            "base_to_target_mapping": mapping,
        }
        for index, record in enumerate(base_records)
    ]


def nonedge_options_at_pair(
    pair: tuple[int, int], base_controls: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    unique: dict[tuple[int, ...], dict[str, Any]] = {}
    remaining = [index for index in range(7) if index not in pair]
    for certificate in base_controls:
        base = y_compression_from_third_nonedge(certificate)
        for special_order in (list(pair), list(pair)[::-1]):
            for ordinary_order in itertools.permutations(remaining):
                mapping = special_order + list(ordinary_order)
                compression = permute_matrix_base_to_target(base, mapping)
                unique.setdefault(
                    flatten(compression),
                    {
                        "compression": compression,
                        "source_control": certificate["name"],
                        "base_to_target_mapping": mapping,
                    },
                )
    records = [unique[key] for key in sorted(unique)]
    if len(records) != 270:
        raise AssertionError("nonedge placement-module count changed")
    return records


def three_center_operator_theorem() -> dict[str, Any]:
    return {
        "fixed_root": "y",
        "compression": "A_x^(y)=P_y P_x P_y restricted to E_y",
        "tau_gram": "T_y[x,z]=tr(A_x^(y) A_z^(y))",
        "symmetric": True,
        "self_adjoint_operator_dimension_on_E_y": 21,
        "rank_bound": 21,
        "operator_sum": "sum_x A_x^(y)=0",
        "row_sums_zero": True,
        "diagonal": "T_y[x,x]=h_yx",
        "root_row": "T_y[y,x]=g_yx",
        "nonedge_pair_contraction": (
            "sum_(z not in {x,y}) tau_(xy;z)=-h_xy-g_xy"
        ),
    }


def coordinate_moment_model(base_controls: list[dict[str, Any]]) -> dict[str, Any]:
    """Check the 21-coordinate form of the fixed-root operator model.

    For the seven root-star vectors, put G=J-I.  The symmetric matrix
    R_x=Z_y^* P_x Z_y has zero row sums, so its 21 off-diagonal entries
    determine its diagonal.  The represented operator is Z_y R_x Z_y^*.
    """

    star_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    records = {}
    for certificate in base_controls:
        compression = y_compression_from_fixed_pair(certificate)
        coordinate_matrix = matrix_negative(compression)
        if W.matrix_vector(coordinate_matrix, [1] * 7) != [0] * 7:
            raise AssertionError("coordinate matrix lost its zero row sums")

        reconstructed = matrix_zero(7)
        for left, right in itertools.combinations(range(7), 2):
            value = coordinate_matrix[left][right]
            reconstructed[left][right] = value
            reconstructed[right][left] = value
        for index in range(7):
            reconstructed[index][index] = W.mod(
                -sum(reconstructed[index][other] for other in range(7))
            )
        if reconstructed != coordinate_matrix:
            raise AssertionError("off-diagonal coordinates do not reconstruct R")

        coordinate_sum = W.mod(
            sum(
                coordinate_matrix[left][right]
                for left, right in itertools.combinations(range(7), 2)
            )
        )
        g_value = W.trace(compression)
        h_value = W.trace(
            W.matrix_multiply(compression, compression)
        )
        quadratic_value = W.trace(
            W.matrix_multiply(
                W.matrix_multiply(
                    W.matrix_multiply(
                        coordinate_matrix, star_gram
                    ),
                    coordinate_matrix,
                ),
                star_gram,
            )
        )
        if g_value != W.mod(2 * coordinate_sum):
            raise AssertionError("linear coordinate moment changed")
        if coordinate_sum != W.mod(certificate["claimed_t"]):
            raise AssertionError("coordinate sum no longer equals t modulo 3")
        if h_value != quadratic_value:
            raise AssertionError("quadratic coordinate moment changed")
        records[certificate["name"]] = {
            "claimed_t_integer": certificate["claimed_t"],
            "coordinate_sum_mod_3": coordinate_sum,
            "g": g_value,
            "two_times_coordinate_sum": W.mod(2 * coordinate_sum),
            "h": h_value,
            "quadratic_coordinate_value": quadratic_value,
            "coordinate_matrix": coordinate_matrix,
        }

    return {
        "root_star_gram": star_gram,
        "coordinate_definition": (
            "r_x^(y)[i,j]=<z_i,P_x z_j>, i<j; these are the 21 "
            "off-diagonal entries of R_x=Z_y^* P_x Z_y"
        ),
        "diagonal_reconstruction": (
            "R_x[i,i]=-sum_(j != i) r_x^(y)[i,j], because R_x 1=0"
        ),
        "operator_reconstruction": (
            "A_x^(y)=Z_y R_x Z_y^* on E_y"
        ),
        "linear_moment": (
            "g_xy=tr(A_x^(y))=2 sum_(i<j) r_x^(y)[i,j]"
        ),
        "nonedge_t_moment": (
            "sum_(i<j) r_x^(y)[i,j]=t_xy modulo 3"
        ),
        "quadratic_moment": (
            "h_xy=tr(R_x G R_x G), a fixed quadratic form in the "
            "21-coordinate row"
        ),
        "global_coordinate_sum": (
            "sum_x r_x^(y)=0 coordinatewise, from sum_x P_x=0"
        ),
        "weighted_relation_projection": (
            "for every c with sum_x c_x P_x=0, "
            "sum_x c_x r_x^(y)=0 coordinatewise"
        ),
        "nonneighbor_fiber_ownership": (
            "the four nonneighbors in y-star block-pair {i,j} own the "
            "marked coordinate r[i,j], although their other coordinates "
            "need not vanish"
        ),
        "control_checks": records,
    }


def graph_pattern_and_fibers() -> dict[str, Any]:
    # For x nonadjacent y, the other 97 vertices split by adjacency to x,y.
    pattern_counts = {
        "z_adjacent_to_both": 2,
        "z_adjacent_to_y_only": 12,
        "z_adjacent_to_x_only": 12,
        "z_adjacent_to_neither": 71,
    }
    if sum(pattern_counts.values()) != 97:
        raise AssertionError("three-center pattern count changed")

    # A fixed root-star has seven disjoint endpoint pairs.  Each pair of
    # root blocks gives four endpoint choices and hence four nonneighbors.
    fiber_count = 0
    owned_vertices = 0
    for left, right in itertools.combinations(range(7), 2):
        del left, right
        fiber_count += 1
        owned_vertices += 4
    if (fiber_count, owned_vertices) != (21, 84):
        raise AssertionError("four-vertex fiber decomposition changed")

    vertices = ["x00", "x01", "x10", "x11"]
    forbidden_edges = {
        tuple(sorted(edge))
        for edge in (
            ("x00", "x01"),
            ("x10", "x11"),
            ("x00", "x10"),
            ("x01", "x11"),
        )
    }
    allowed_diagonals = {
        tuple(sorted(edge))
        for edge in (("x00", "x11"), ("x01", "x10"))
    }
    possible_fiber_graphs = []
    for mask in range(4):
        edges = {
            edge
            for index, edge in enumerate(sorted(allowed_diagonals))
            if mask & (1 << index)
        }
        if edges & forbidden_edges:
            raise AssertionError("forbidden fiber edge survived")
        degrees = Counter(vertex for edge in edges for vertex in edge)
        if degrees and max(degrees.values()) > 1:
            raise AssertionError("fiber graph is not a matching")
        possible_fiber_graphs.append(sorted([list(edge) for edge in edges]))

    # If x_p0~x_p1, lambda=1 makes {a_p,x_p0,x_p1} a triangle.
    # The root block {y,b0,b1} is disjoint.  The three forced cross edges
    # are a matching; all six possible extras are excluded by the local
    # matching at y and mu=2 for y with x_pq.
    prism_cross_edges = [
        ["y", "a_p"],
        ["b0", "x_p0"],
        ["b1", "x_p1"],
    ]
    return {
        "fixed_nonedge_xy_pattern_counts": pattern_counts,
        "edge_third_center_common_block_placements": {
            "z_adjacent_to_both": (
                "one in each of the two distinguished y-star blocks"
            ),
            "z_adjacent_to_y_only": (
                "one in each distinguished block and two in each of "
                "the five ordinary blocks"
            ),
        },
        "nonedge_third_center_marked_pair_distribution": {
            "star_block_pairs": fiber_count,
            "vertices_per_pair": 4,
            "total": owned_vertices,
        },
        "fiber_vertices": vertices,
        "fiber_forbidden_edges_sharing_an_endpoint_choice": sorted(
            [list(edge) for edge in forbidden_edges]
        ),
        "fiber_allowed_edges": sorted(
            [list(edge) for edge in allowed_diagonals]
        ),
        "possible_induced_fiber_graphs": possible_fiber_graphs,
        "possible_induced_fiber_graph_count": len(possible_fiber_graphs),
        "same_endpoint_hypothetical_edge_forces_prism_cross_edges":
            prism_cross_edges,
        "fiber_graph_is_subgraph_of_opposite_corner_matching": True,
    }


def marked_coordinate_census() -> dict[str, Any]:
    result: dict[str, Any] = {}
    expected = {
        "6": {
            "1,1": 18,
        },
        "7": {
            "0,0": 288,
            "0,1": 9,
            "1,0": 144,
            "1,1": 180,
            "2,0": 144,
        },
    }
    for t_value in (6, 7):
        counts: Counter[tuple[int, int]] = Counter()
        admissible = 0
        for cross in W.normalized_low_t_matrices(t_value):
            full_gram = W.full_two_star_gram(cross)
            _, pivots = W.rref(full_gram)
            gram_rank = len(pivots)
            discriminant = 0
            if gram_rank <= 11:
                discriminant = W.determinant(
                    [[full_gram[i][j] for j in pivots] for i in pivots]
                )
            kernel_distance = W.minimum_linear_code_weight(
                W.nullspace(full_gram)
            )
            if (
                gram_rank != 11
                or discriminant != 2
                or kernel_distance < 4
            ):
                continue
            compression = W.matrix_multiply(cross, W.transpose(cross))
            h_value = W.trace(
                W.matrix_multiply(compression, compression)
            )
            marked_r = W.mod(-compression[0][1])
            counts[(h_value, marked_r)] += 1
            admissible += 1
        table = {
            f"{h_value},{marked_r}": counts[(h_value, marked_r)]
            for h_value, marked_r in sorted(counts)
        }
        if table != expected[str(t_value)]:
            raise AssertionError("marked-coordinate census changed")
        result[str(t_value)] = {
            "admissible_normalized_modules": admissible,
            "counts_by_h_and_r": table,
        }
    return {
        "definition": (
            "r_x^(y)[i,j]=<z_i,P_x z_j>=-(C C^T)[i,j] "
            "for the two marked y-star blocks"
        ),
        "special_row_formula": {
            "ordinary_extra_two_positions_aligned": "r=0",
            "ordinary_extra_two_positions_distinct": "r=1",
        },
        "census": result,
        "consequence": (
            "at t=7, r=1 excludes h=2; r=0 permits h=0,1,2; "
            "at t=6, r=1 and h=1 are forced within the censused branch"
        ),
    }


def marginal_tau_census(
    edge_base: list[dict[str, Any]], base_controls: list[dict[str, Any]]
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    edge_options = {
        block: edge_options_at_block(edge_base, block) for block in range(7)
    }
    nonedge_options = {
        pair: nonedge_options_at_pair(pair, base_controls)
        for pair in itertools.combinations(range(7), 2)
    }
    for fixed in base_controls:
        fixed_compression = y_compression_from_fixed_pair(fixed)
        edge_values = {
            str(block): sorted(
                {
                    trace_pair(
                        fixed_compression, option["compression"]
                    )
                    for option in edge_options[block]
                }
            )
            for block in range(7)
        }
        nonedge_values = {
            f"{pair[0]},{pair[1]}": sorted(
                {
                    trace_pair(
                        fixed_compression, option["compression"]
                    )
                    for option in nonedge_options[pair]
                }
            )
            for pair in itertools.combinations(range(7), 2)
        }
        if any(values != [0, 1, 2] for values in edge_values.values()):
            raise AssertionError("edge third-center tau lost a residue")
        if any(values != [0, 1, 2] for values in nonedge_values.values()):
            raise AssertionError("nonedge third-center tau lost a residue")

        pair_trace = W.trace(fixed_compression)
        fourth_trace = W.trace(
            W.matrix_multiply(fixed_compression, fixed_compression)
        )
        target = W.mod(-pair_trace - fourth_trace)

        # Build a deterministic scalar contraction ledger.  It assigns two
        # y-neighbors to each root block and four y-nonneighbors to each
        # marked pair, except that the frozen x occupies one of the four
        # positions in pair {0,1}.  Each selected entry is a genuine
        # y-rooted pair-local module.  The ledger does not impose the
        # prescribed x--z adjacency or x,z pair module, and different entries
        # are not asserted to share one global column realization.
        assignments = []
        first_edge = True
        for block in range(7):
            for copy in range(2):
                wanted = target if first_edge else 0
                first_edge = False
                option_index = next(
                    index
                    for index, option in enumerate(edge_options[block])
                    if trace_pair(
                        fixed_compression, option["compression"]
                    )
                    == wanted
                )
                assignments.append(
                    {
                        "relation_to_y": "edge",
                        "common_block": block,
                        "copy": copy,
                        "tau": wanted,
                        "module_index": option_index,
                    }
                )
        for pair in itertools.combinations(range(7), 2):
            multiplicity = 3 if pair == (0, 1) else 4
            option_index = next(
                index
                for index, option in enumerate(nonedge_options[pair])
                if trace_pair(fixed_compression, option["compression"]) == 0
            )
            for copy in range(multiplicity):
                assignments.append(
                    {
                        "relation_to_y": "nonedge",
                        "marked_pair": list(pair),
                        "copy": copy,
                        "tau": 0,
                        "module_index": option_index,
                    }
                )
        if len(assignments) != 97:
            raise AssertionError("marginal contraction ledger size changed")
        if W.mod(sum(item["tau"] for item in assignments)) != target:
            raise AssertionError("marginal scalar contraction failed")
        result[fixed["name"]] = {
            "pair_trace_g": pair_trace,
            "fourth_trace_h": fourth_trace,
            "required_remaining_tau_sum": target,
            "edge_tau_values_by_common_block": edge_values,
            "nonedge_tau_values_by_marked_pair": nonedge_values,
            "marginal_assignment": assignments,
            "marginal_assignment_size": len(assignments),
            "marginal_tau_sum": target,
            "root_relative_placement_multiplicities_imposed": True,
            "x_z_adjacency_or_pair_module_imposed": False,
            "shared_operator_sum_or_shared_231_columns_imposed": False,
        }
    return result


def formal_zero_sum_controls(base_controls: list[dict[str, Any]]) -> dict[str, Any]:
    star_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    root_identity = W.matrix_multiply(star_gram, star_gram)
    zero = matrix_zero(7)
    result = {}
    for fixed in base_controls:
        fixed_compression = y_compression_from_fixed_pair(fixed)
        residual = matrix_negative(
            W.matrix_add(root_identity, fixed_compression)
        )
        operators = [root_identity, fixed_compression, residual] + [
            zero for _ in range(96)
        ]
        if matrix_sum(operators) != zero:
            raise AssertionError("formal operator control lost zero sum")
        tau_gram = [
            [trace_pair(left, right) for right in operators]
            for left in operators
        ]
        if tau_gram != W.transpose(tau_gram):
            raise AssertionError("formal tau Gram is not symmetric")
        if W.matrix_vector(tau_gram, [1] * 99) != [0] * 99:
            raise AssertionError("formal tau row sums changed")
        fixed_h = trace_pair(fixed_compression, fixed_compression)
        fixed_g = trace_pair(root_identity, fixed_compression)
        if (tau_gram[1][1], tau_gram[0][1]) != (fixed_h, fixed_g):
            raise AssertionError("formal control lost h or g")
        result[fixed["name"]] = {
            "operator_count": len(operators),
            "operator_sum_zero": True,
            "tau_gram_symmetric": True,
            "tau_gram_rank": W.rank(tau_gram),
            "tau_gram_row_sums_zero": True,
            "fixed_pair_h": fixed_h,
            "fixed_pair_g": fixed_g,
            "residual_operator": residual,
            "residual_is_claimed_to_be_a_graph_projector_compression": False,
        }
    return result


def analyze() -> dict[str, Any]:
    inputs = verify_frozen_inputs()
    base_controls = controls()
    labelled_edge_count, edge_base = edge_compression_records()
    edge_summary = Counter(
        (
            W.rank(record["compression"]),
            W.trace(record["compression"]),
            W.trace(
                W.matrix_multiply(
                    record["compression"], record["compression"]
                )
            ),
        )
        for record in edge_base
    )
    expected_edge_summary = {
        (3, 0, 0): 15,
        (4, 0, 0): 60,
        (4, 0, 1): 45,
        (6, 0, 0): 10,
    }
    if dict(edge_summary) != expected_edge_summary:
        raise AssertionError("unique edge compression profile changed")
    return {
        "claim_label": "DERIVED",
        "scope": (
            "conditional prism-free rank-11 endpoint; exact fixed-root "
            "three-center operator identities, graph placements, low-t "
            "marked-coordinate census, and marginal tau compatibility"
        ),
        "field": FIELD,
        "inputs": inputs,
        "three_center_operator_theorem": three_center_operator_theorem(),
        "coordinate_moment_model": coordinate_moment_model(base_controls),
        "graph_patterns_and_fibers": graph_pattern_and_fibers(),
        "marked_coordinate_low_t_census": marked_coordinate_census(),
        "edge_module_census": {
            "labelled_degree_two_biadjacency_matrices": labelled_edge_count,
            "unique_compressions": len(edge_base),
            "profile_rank_g_h": [
                {
                    "rank": key[0],
                    "g": key[1],
                    "h": key[2],
                    "count": edge_summary[key],
                }
                for key in sorted(edge_summary)
            ],
        },
        "marginal_tau_census": marginal_tau_census(
            edge_base, base_controls
        ),
        "formal_zero_sum_operator_controls": formal_zero_sum_controls(
            base_controls
        ),
        "conclusions": {
            "rank21_zero_row_three_center_gram": "DERIVED",
            "twenty_one_coordinate_first_quadratic_moment_model": "DERIVED",
            "four_vertex_fiber_matching_lemma": "DERIVED",
            "t7_marked_r_one_excludes_h_two": "DERIVED_LOW_T_ONLY",
            "root_relation_and_forced_y_star_placement_determine_tau": False,
            "full_labelled_three_center_graph_type_determines_tau": "UNKNOWN",
            "scalar_contraction_plus_marginal_modules_determine_h": False,
            "combined_shared_operator_and_graph_module_completion": "UNKNOWN",
            "rank_11_endpoint_excluded": False,
            "conway_99_status": "UNKNOWN",
            "newly_named_missing_invariant": (
                "the joint four-operator fiber law for the four compressions "
                "owned by each y-star block pair, coupled across all 21 "
                "fibers by one shared 231-column realization"
            ),
        },
        "omitted_target_premises": [
            "one simultaneous choice of 98 graph-derived compressions whose operator sum is zero",
            "one shared set of 231 projectively distinct centered columns for all marginal modules",
            "compatibility of the four compression operators inside each nonneighbor fiber",
            "compatibility between the 21 fibers and the 14 edge compressions",
            "the prescribed x-z adjacency and pair module for each third center",
            "all t>=8 nonedge modules",
            "global point-triangle incidence, square-zero Gram, and rank-11 endpoint realization",
            "a 99-vertex srg(99,14,1,2), construction, or nonexistence proof",
        ],
    }


def verify(data: dict[str, Any]) -> None:
    conclusions = data["conclusions"]
    if conclusions["root_relation_and_forced_y_star_placement_determine_tau"]:
        raise AssertionError("status inflation: root-relative marginal tau remains free")
    if conclusions["full_labelled_three_center_graph_type_determines_tau"] != "UNKNOWN":
        raise AssertionError("status inflation: full labelled triple type is unresolved")
    if conclusions["combined_shared_operator_and_graph_module_completion"] != "UNKNOWN":
        raise AssertionError("status inflation: joint completion is unknown")
    if conclusions["rank_11_endpoint_excluded"]:
        raise AssertionError("status inflation: endpoint not excluded")
    if conclusions["conway_99_status"] != "UNKNOWN":
        raise AssertionError("status inflation: Conway-99 changed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    data = analyze()
    verify(data)
    if args.verify:
        observed = json.loads(args.verify.read_text(encoding="utf-8"))
        if observed != data:
            raise AssertionError("frozen result differs")
    if args.write:
        args.write.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    if not args.write and not args.verify:
        print(json.dumps(data, indent=2, sort_keys=True))
    print("PASS: Wave206 proof-A three-center checks")


if __name__ == "__main__":
    main()
