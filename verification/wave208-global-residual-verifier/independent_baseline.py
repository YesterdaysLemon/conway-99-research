#!/usr/bin/env python3
"""Source-blind Wave 208 obligation and hostile-boundary checker."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "baseline-results.json"


def sign_compositions(weight: int) -> list[tuple[int, int, int]]:
    rows = []
    for p in range(weight + 1):
        n = weight - p
        if (p - n) % 3 == 0:
            rows.append((p, n, (p - n) // 3))
    return rows


def centered_product(triangle_a, triangle_b, edges) -> tuple[int, str]:
    left, right = set(triangle_a), set(triangle_b)
    intersection = left & right
    if len(intersection) == 1:
        return 1, "intersecting"
    if intersection:
        raise AssertionError("distinct graph triangles cannot share an edge")
    cross = sum(tuple(sorted((u, v))) in edges for u in left for v in right)
    if cross > 2:
        raise AssertionError("prism-free cross-edge cap")
    return cross % 3, "disjoint"


def validate_terminal_status(result: dict[str, object]) -> None:
    terminal = bool(result.get("complete_graph_certificate")) or bool(
        result.get("complete_nonexistence_certificate")
    )
    if not terminal:
        assert result["global_status"] == "UNKNOWN"


def is_binary_matrix(matrix: list[list[object]]) -> bool:
    return bool(matrix) and all(value in (0, 1) for row in matrix for value in row)


def graphical_overlap_gate(matrix: list[list[object]], claimed_gram: list[list[int]]) -> bool:
    if not is_binary_matrix(matrix):
        return False
    rows, columns = len(matrix), len(matrix[0])
    if any(len(row) != columns for row in matrix):
        return False
    actual = [
        [sum(matrix[r][i] * matrix[r][j] for r in range(rows)) for j in range(columns)]
        for i in range(columns)
    ]
    return actual == claimed_gram


def build_result() -> dict[str, object]:
    all_compositions = {weight: sign_compositions(weight) for weight in (14, 17, 20, 23)}
    retained = {
        14: [(7, 7, 0)],
        17: all_compositions[17],
        20: all_compositions[20],
        23: all_compositions[23],
    }

    # Two exact witnesses to the product-one ambiguity.
    bowtie_triangles = ((0, 1, 2), (0, 3, 4))
    bowtie_edges = {
        tuple(sorted(edge)) for triangle in bowtie_triangles for edge in combinations(triangle, 2)
    }
    disjoint_triangles = ((0, 1, 2), (3, 4, 5))
    disjoint_edges = {
        tuple(sorted(edge)) for triangle in disjoint_triangles for edge in combinations(triangle, 2)
    } | {(0, 3)}
    bowtie = centered_product(*bowtie_triangles, bowtie_edges)
    one_cross = centered_product(*disjoint_triangles, disjoint_edges)
    assert bowtie == (1, "intersecting")
    assert one_cross == (1, "disjoint")

    # Logical scope witness: the inside equation can hold while one omitted
    # outside row violates the full point-code equation.
    b_inside = [1, 2]
    a_inside = [[0, 0], [0, 0]]
    assert [sum(a_inside[i][j] * b_inside[j] for j in range(2)) % 3 for i in range(2)] == [0, 0]
    omitted_outside_row = [1, 0]
    omitted_value = sum(omitted_outside_row[j] * b_inside[j] for j in range(2)) % 3
    assert omitted_value == 1

    # Aggregate-versus-graphical hostile controls.
    impossible_overlap = [[1, 2], [2, 1]]
    # Diagonal one with overlap two cannot be M^T M for a binary M.
    assert not graphical_overlap_gate([[1, 1]], impossible_overlap)
    fractional_control = [[Fraction(1, 2), Fraction(1, 2)]]
    assert not graphical_overlap_gate(fractional_control, [[1, 1], [1, 1]])
    valid_binary = [[1, 1], [1, 0]]
    valid_gram = [[2, 1], [1, 1]]
    assert graphical_overlap_gate(valid_binary, valid_gram)

    # A1--A6 are symbolic consequences of the target polynomial and spectrum.
    spectral = {
        "eigenvalues": {"14": 1, "3": 54, "-4": 44},
        "integer_lift": "Az=4x-z+2t*1",
        "sum_z": "14t",
        "three_norm_z": "4w-x_dot_z+6t^2",
        "u3": "(3*x_dot_z+4*w-18*t^2/11)/7",
        "u_minus4": "(3*w-3*x_dot_z+t^2)/7",
        "coordinate_z_values": list(range(-4, 5)),
        "neighborhood_graph": "7K2",
    }

    result = {
        "source_blind": True,
        "sign_compositions": {
            str(weight): [list(row) for row in retained[weight]] for weight in retained
        },
        "parameter_only_compositions_weight14": [list(row) for row in all_compositions[14]],
        "spectral_integer_lift_obligations": spectral,
        "product_one_witnesses": {
            "intersecting": {"product": bowtie[0], "kind": bowtie[1]},
            "disjoint_one_cross_edge": {"product": one_cross[0], "kind": one_cross[1]},
        },
        "outside_scope_hostile_control": {
            "inside_equation_zero": True,
            "omitted_outside_coordinate": omitted_value,
            "full_equation_zero": False,
        },
        "outside_block_obligations": {
            "point_kernel": "M*b_U=0",
            "overlap_gram": "M^T*M=12I-A_U+2J-A_U^2",
            "outside_rows_for_23_vertex_union": 76,
            "binary_required": True,
            "full_A_O_completion_required": True,
        },
        "aggregate_graphical_gates": {
            "impossible_overlap_rejected": True,
            "fractional_matrix_rejected": True,
            "valid_binary_gram_accepted": True,
        },
        "unknown_enumerator_coefficients_may_be_zeroed": False,
        "restricted_nonhit_is_nonexistence": False,
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "global_status": "UNKNOWN",
    }
    validate_terminal_status(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        assert result == json.loads(BASELINE.read_text(encoding="utf-8"))
        print("PASS: Wave208 source-blind baseline")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

