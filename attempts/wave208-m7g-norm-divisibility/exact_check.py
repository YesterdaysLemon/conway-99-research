#!/usr/bin/env python3
"""Exact standard-library checker for the Wave 208 M7g norm obstruction."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Sequence

P = 3
HERE = Path(__file__).resolve().parent
RESULT = HERE / "exact-results.json"
TENSOR_RELATION = (1, 2, 1, 2, 1, 2, 2, 1)
INTEGER_LIFT = tuple(1 if value == 1 else -1 for value in TENSOR_RELATION)
EXPECTED_SIGN_CLASSES = (
    (1, 1, 1, 1, 2, 2, 1, 1),
    (1, 1, 2, 2, 1, 1, 1, 1),
    (1, 1, 2, 2, 2, 2, 2, 2),
    (1, 2, 1, 2, 1, 2, 1, 2),
)


def original_points() -> tuple[tuple[int, ...], ...]:
    return (
        (1, 0, 0, 0),
        (1, 0, 0, 1),
        (0, 1, 0, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
        (1, 1, 1, 2),
    )


def rank_mod3(matrix: Sequence[Sequence[int]]) -> int:
    a = [[value % P for value in row] for row in matrix]
    rank = 0
    columns = len(a[0]) if a else 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(a)) if a[row][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = 1 if a[rank][column] == 1 else 2
        a[rank] = [(inverse * value) % P for value in a[rank]]
        for row in range(len(a)):
            if row == rank or not a[row][column]:
                continue
            scale = a[row][column]
            a[row] = [
                (a[row][j] - scale * a[rank][j]) % P
                for j in range(columns)
            ]
        rank += 1
    return rank


def nullspace_mod3(matrix: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    a = [[value % P for value in row] for row in matrix]
    columns = len(a[0]) if a else 0
    pivot_columns: list[int] = []
    row = 0
    for column in range(columns):
        pivot = next((r for r in range(row, len(a)) if a[r][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inverse = 1 if a[row][column] == 1 else 2
        a[row] = [(inverse * value) % P for value in a[row]]
        for other in range(len(a)):
            if other == row or not a[other][column]:
                continue
            scale = a[other][column]
            a[other] = [
                (a[other][j] - scale * a[row][j]) % P
                for j in range(columns)
            ]
        pivot_columns.append(column)
        row += 1
        if row == len(a):
            break
    free_columns = [column for column in range(columns) if column not in pivot_columns]
    basis: list[tuple[int, ...]] = []
    for free in free_columns:
        vector = [0] * columns
        vector[free] = 1
        for pivot_row, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = (-a[pivot_row][free]) % P
        basis.append(tuple(vector))
    return basis


def quadratic_evaluation_row(vector: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        (vector[i] * vector[j] * (1 if i == j else 2)) % P
        for i in range(4)
        for j in range(i, 4)
    )


def symmetric_matrix(coordinates: Sequence[int]) -> list[list[int]]:
    matrix = [[0] * 4 for _ in range(4)]
    cursor = 0
    for i in range(4):
        for j in range(i, 4):
            matrix[i][j] = matrix[j][i] = coordinates[cursor] % P
            cursor += 1
    return matrix


def bilinear(left: Sequence[int], form: Sequence[Sequence[int]], right: Sequence[int]) -> int:
    return sum(
        left[i] * form[i][j] * right[j]
        for i in range(4)
        for j in range(4)
    ) % P


def linearizing_sign_classes() -> tuple[tuple[int, ...], ...]:
    points = original_points()
    classes: list[tuple[int, ...]] = []
    for signs in product((1, 2), repeat=8):
        if signs[0] != 1:
            continue
        signed = [
            tuple(signs[i] * coordinate % P for coordinate in points[i])
            for i in range(8)
        ]
        if all(
            sum(TENSOR_RELATION[i] * signed[i][coordinate] for i in range(8)) % P == 0
            for coordinate in range(4)
        ):
            classes.append(signs)
    return tuple(classes)


def zero_graph(matrix: Sequence[Sequence[int]]) -> str:
    adjacency = [set() for _ in range(8)]
    for i, j in combinations(range(8), 2):
        if matrix[i][j] == 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    unseen = set(range(8))
    component_sizes: list[int] = []
    while unseen:
        stack = [min(unseen)]
        unseen.remove(stack[0])
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in sorted(adjacency[vertex] & unseen):
                unseen.remove(neighbor)
                stack.append(neighbor)
        component_sizes.append(size)
    degrees = tuple(sorted(len(neighbors) for neighbors in adjacency))
    edges = sum(degrees) // 2
    key = (edges, tuple(sorted(component_sizes)), degrees)
    names = {
        (28, (8,), (7,) * 8): "K8",
        (12, (4, 4), (3,) * 8): "2K4",
        (4, (2, 2, 2, 2), (1,) * 8): "4K2",
        (8, (4, 4), (2,) * 8): "2C4",
    }
    if key not in names:
        raise AssertionError(f"unexpected zero graph {key}")
    return names[key]


def polar_forms() -> list[tuple[tuple[int, int, int], list[list[int]]]]:
    evaluations = [quadratic_evaluation_row(point) for point in original_points()]
    basis = nullspace_mod3(evaluations)
    if len(basis) != 3:
        raise AssertionError("M7g polar net must have dimension three")
    forms = []
    for coefficients in product(range(P), repeat=3):
        coordinates = tuple(
            sum(coefficients[i] * basis[i][j] for i in range(3)) % P
            for j in range(10)
        )
        form = symmetric_matrix(coordinates)
        if any(bilinear(point, form, point) for point in original_points()):
            raise AssertionError("polar form does not vanish on M7g")
        forms.append((coefficients, form))
    return forms


def gram(points: Sequence[Sequence[int]], form: Sequence[Sequence[int]]) -> list[list[int]]:
    return [[bilinear(left, form, right) for right in points] for left in points]


def form_record(
    coefficients: Sequence[int], form: Sequence[Sequence[int]], signs: Sequence[int]
) -> dict[str, object]:
    points = original_points()
    signed = [
        tuple(signs[i] * coordinate % P for coordinate in points[i])
        for i in range(8)
    ]
    matrix = gram(signed, form)
    if any(matrix[i][i] for i in range(8)):
        raise AssertionError("nonzero polar diagonal")
    d_value = sum(
        INTEGER_LIFT[i] * INTEGER_LIFT[j] * matrix[i][j]
        for i, j in combinations(range(8), 2)
    )
    base_norm = 240 - 2 * d_value
    return {
        "coefficients": list(coefficients),
        "rank": rank_mod3(form),
        "zero_graph": zero_graph(matrix),
        "d": d_value,
        "base_norm": base_norm,
        "remainder_mod9": base_norm % 9,
        "matrix": matrix,
    }


def build_result() -> dict[str, object]:
    if INTEGER_LIFT != (1, -1, 1, -1, 1, -1, -1, 1):
        raise AssertionError("wrong ordinary integer lift")
    if sum(INTEGER_LIFT) != 0:
        raise AssertionError("integer lift is not balanced")
    sign_classes = linearizing_sign_classes()
    if sign_classes != EXPECTED_SIGN_CLASSES:
        raise AssertionError(f"unexpected sign classes: {sign_classes}")
    forms = polar_forms()
    if len(forms) != 27:
        raise AssertionError("polar net is not complete")

    class_results: list[dict[str, object]] = []
    common_distribution = None
    for class_index, signs in enumerate(sign_classes):
        records = [form_record(coefficients, form, signs) for coefficients, form in forms]
        distribution = Counter(
            (record["rank"], record["zero_graph"], record["remainder_mod9"])
            for record in records
        )
        expected_distribution = Counter(
            {
                (0, "K8", 6): 1,
                (2, "2K4", 6): 12,
                (3, "4K2", 6): 6,
                (3, "4K2", 3): 1,
                (3, "4K2", 0): 1,
                (4, "2C4", 3): 3,
                (4, "2C4", 0): 3,
            }
        )
        if distribution != expected_distribution:
            raise AssertionError(f"unexpected remainder distribution: {distribution}")
        serialized_distribution = {
            f"rank{rank}_{graph}_rem{remainder}": count
            for (rank, graph, remainder), count in sorted(distribution.items())
        }
        if common_distribution is None:
            common_distribution = serialized_distribution
        elif serialized_distribution != common_distribution:
            raise AssertionError("orientation classes have different distributions")
        survivors = [record for record in records if record["remainder_mod9"] == 0]
        if Counter((record["rank"], record["zero_graph"], record["d"], record["base_norm"]) for record in survivors) != Counter(
            {(3, "4K2", 12, 216): 1, (4, "2C4", -24, 288): 3}
        ):
            raise AssertionError("unexpected survivor types")
        class_results.append(
            {
                "class_index": class_index,
                "signs": list(signs),
                "distribution": serialized_distribution,
                "eliminated_forms": len(records) - len(survivors),
                "surviving_forms": survivors,
            }
        )

    # The unknown exact intersection set changes (3) only by 18s.  This
    # purely symbolic check records that no value of s changes the mod-nine
    # remainder; it does not enumerate or posit an intersection graph.
    for s_value in range(-28, 29):
        for remainder in range(9):
            if (remainder + 18 * s_value) % 9 != remainder:
                raise AssertionError("intersection correction changed the remainder")

    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "m7g": {
            "original_points": [list(point) for point in original_points()],
            "tensor_relation": list(TENSOR_RELATION),
            "integer_lift": list(INTEGER_LIFT),
            "integer_lift_sum": sum(INTEGER_LIFT),
            "relative_sign_classes": len(sign_classes),
            "affine_polar_forms_per_class": len(forms),
        },
        "norm_identity": "||AU alpha||^2 = 240 + 18s - 2d(Q)",
        "necessary_congruence": "240 - 2d(Q) = 0 (mod 9)",
        "common_distribution": common_distribution,
        "classes": class_results,
        "summary": {
            "forms_per_orientation": 27,
            "eliminated_per_orientation": 23,
            "survivors_per_orientation": 4,
            "survivor_types": {
                "rank3_4K2_d12_base216": 1,
                "rank4_2C4_d-24_base288": 3,
            },
        },
        "limitations": [
            "the four surviving forms are necessary residue data, not graph constructions",
            "the unknown intersection set and its sum s are not reconstructed",
            "no 99-vertex adjacency matrix or counterexample is produced",
            "the global Conway-99 status remains UNKNOWN",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        expected = json.loads(RESULT.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("archived exact result differs from replay")
        print("PASS: Wave208 M7g norm-divisibility exact checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

