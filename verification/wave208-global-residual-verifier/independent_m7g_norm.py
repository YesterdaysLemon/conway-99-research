#!/usr/bin/env python3
"""Clean-room reconstruction of the sealed Wave 208 M7g norm claim.

This module imports no discovery code.  It starts from the published labelled
M7g representatives and exhausts 128 relative column orientations and all
27 affine members of the vanishing symmetric-form space.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

Q = 3
HERE = Path(__file__).resolve().parent
RESULT = HERE / "m7g-norm-independent-results.json"
VECTORS = (
    (1, 0, 0, 0),
    (1, 0, 0, 1),
    (0, 1, 0, 0),
    (0, 1, 0, 1),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (1, 1, 1, 1),
    (1, 1, 1, 2),
)
TERNARY_RELATION = (1, 2, 1, 2, 1, 2, 2, 1)
INTEGER_LIFT = tuple(1 if value == 1 else -1 for value in TERNARY_RELATION)
SYMMETRIC_POSITIONS = tuple((i, j) for i in range(4) for j in range(i, 4))


def inv(value: int) -> int:
    if value % Q == 1:
        return 1
    if value % Q == 2:
        return 2
    raise ZeroDivisionError


def rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    a = [[value % Q for value in row] for row in matrix]
    pivots: list[int] = []
    row = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = inv(a[row][column])
        a[row] = [(scale * value) % Q for value in a[row]]
        for i in range(len(a)):
            if i == row or not a[i][column]:
                continue
            scale = a[i][column]
            a[i] = [(a[i][j] - scale * a[row][j]) % Q for j in range(len(a[0]))]
        pivots.append(column)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank_mod3(matrix: list[list[int]]) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: list[list[int]]) -> list[list[int]]:
    reduced, pivots = rref(matrix)
    columns = len(matrix[0])
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % Q
        basis.append(vector)
    return basis


def symmetric_evaluation_row(vector: tuple[int, ...]) -> list[int]:
    return [
        (vector[i] * vector[j] * (1 if i == j else 2)) % Q
        for i, j in SYMMETRIC_POSITIONS
    ]


def symmetric_matrix(coordinates: list[int]) -> list[list[int]]:
    matrix = [[0] * 4 for _ in range(4)]
    for value, (i, j) in zip(coordinates, SYMMETRIC_POSITIONS):
        matrix[i][j] = matrix[j][i] = value % Q
    return matrix


def dot_form(left, form, right) -> int:
    return sum(left[i] * form[i][j] * right[j] for i in range(4) for j in range(4)) % Q


def oriented_vectors(signs: tuple[int, ...]):
    return [tuple(signs[index] * value % Q for value in vector) for index, vector in enumerate(VECTORS)]


def relative_orientations() -> list[tuple[int, ...]]:
    orientations = []
    for signs in product((1, 2), repeat=8):
        if signs[0] != 1:
            continue
        oriented = oriented_vectors(signs)
        if all(
            sum(TERNARY_RELATION[j] * oriented[j][i] for j in range(8)) % Q == 0
            for i in range(4)
        ):
            orientations.append(signs)
    return orientations


def zero_graph_name(gram: list[list[int]]) -> str:
    adjacency = {
        i: {j for j in range(8) if j != i and gram[i][j] == 0} for i in range(8)
    }
    edges = sum(len(neighbors) for neighbors in adjacency.values()) // 2
    degrees = tuple(sorted(len(neighbors) for neighbors in adjacency.values()))
    unseen = set(range(8))
    components = []
    while unseen:
        stack = [unseen.pop()]
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            new = adjacency[vertex] & unseen
            unseen -= new
            stack.extend(new)
        components.append(len(component))
    signature = (edges, tuple(sorted(components)), degrees)
    return {
        (28, (8,), (7,) * 8): "K8",
        (12, (4, 4), (3,) * 8): "2K4",
        (4, (2, 2, 2, 2), (1,) * 8): "4K2",
        (8, (4, 4), (2,) * 8): "2C4",
    }[signature]


def form_space() -> list[list[list[int]]]:
    evaluation = [symmetric_evaluation_row(vector) for vector in VECTORS]
    basis = nullspace(evaluation)
    assert len(basis) == 3
    forms = []
    for coefficients in product(range(Q), repeat=3):
        coordinates = [
            sum(coefficients[k] * basis[k][j] for k in range(3)) % Q
            for j in range(len(SYMMETRIC_POSITIONS))
        ]
        forms.append(symmetric_matrix(coordinates))
    return forms


def build_result() -> dict[str, object]:
    # Verify the frozen quadratic relation independently.
    veronese = [
        [vector[i] * vector[j] % Q for vector in VECTORS]
        for i, j in SYMMETRIC_POSITIONS
    ]
    assert all(
        sum(row[j] * TERNARY_RELATION[j] for j in range(8)) % Q == 0
        for row in veronese
    )
    assert rank_mod3(veronese) == 7
    assert INTEGER_LIFT.count(1) == INTEGER_LIFT.count(-1) == 4

    orientations = relative_orientations()
    assert len(orientations) == 4
    forms = form_space()
    assert len(forms) == 27

    class_summaries = []
    common_distribution = None
    survivor_records = []
    for orientation_index, signs in enumerate(orientations):
        vectors = oriented_vectors(signs)
        distribution: Counter[tuple[int, str, int]] = Counter()
        survivors = []
        for affine_index, form in enumerate(forms):
            gram = [[dot_form(vectors[i], form, vectors[j]) for j in range(8)] for i in range(8)]
            assert all(gram[i][i] == 0 for i in range(8))
            rank = rank_mod3(form)
            name = zero_graph_name(gram)
            d_value = sum(
                INTEGER_LIFT[i] * INTEGER_LIFT[j] * gram[i][j]
                for i, j in combinations(range(8), 2)
            )
            base_norm = 240 - 2 * d_value
            remainder = base_norm % 9
            distribution[(rank, name, remainder)] += 1
            if remainder == 0:
                ones = sum(gram[i][j] == 1 for i, j in combinations(range(8), 2))
                record = {
                    "orientation": orientation_index,
                    "affine_form": affine_index,
                    "rank": rank,
                    "zero_graph": name,
                    "d": d_value,
                    "base_norm": base_norm,
                    "product_one_pairs": ones,
                }
                survivors.append(record)
                survivor_records.append(record)
        normalized = {
            f"rank{rank}_{name}_remainder{remainder}": count
            for (rank, name, remainder), count in sorted(distribution.items())
        }
        if common_distribution is None:
            common_distribution = normalized
        else:
            assert normalized == common_distribution
        assert len(survivors) == 4
        class_summaries.append(
            {
                "signs": list(signs),
                "distribution": normalized,
                "survivors": survivors,
            }
        )

    survivor_types = Counter(
        (row["rank"], row["zero_graph"], row["d"], row["base_norm"])
        for row in survivor_records
    )
    assert survivor_types == Counter({(4, "2C4", -24, 288): 12, (3, "4K2", 12, 216): 4})
    assert all(row["product_one_pairs"] > 0 for row in survivor_records)

    return {
        "relative_orientation_count": len(orientations),
        "affine_forms_per_orientation": len(forms),
        "integer_lift": list(INTEGER_LIFT),
        "norm_identity": "||AUalpha||^2=240+18s-2d(Q)",
        "necessary_congruence": "d(Q)=3 mod 9",
        "orientation_classes": class_summaries,
        "survivor_type_totals": {
            "rank3_4K2_d12_base216": survivor_types[(3, "4K2", 12, 216)],
            "rank4_2C4_d-24_base288": survivor_types[(4, "2C4", -24, 288)],
        },
        "forms_surviving_per_orientation": 4,
        "forms_excluded_per_orientation": 23,
        "product_one_interpretation_fixed": False,
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "global_status": "UNKNOWN",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        assert result == json.loads(RESULT.read_text(encoding="utf-8"))
        print("PASS: independent M7g norm reconstruction")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

