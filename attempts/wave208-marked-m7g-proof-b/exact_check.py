#!/usr/bin/env python3
"""Exact checker for the Wave 208 marked-M7g spectral obstruction."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path

Q = 3
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "exact-results.json"
CONTROLS = HERE / "local-controls.json"
ALLOWED_POINT_WEIGHTS = {14, 17, 20, 23}


def columns() -> list[tuple[int, int, int, int]]:
    return [
        (1, 2, 2, 2),
        (1, 0, 2, 2),
        (1, 2, 0, 2),
        (1, 2, 2, 0),
        (1, 1, 1, 1),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
    ]


def restricted_form(diagonal: tuple[int, int, int]) -> list[list[int]]:
    d1, d2, d3 = diagonal
    alpha = (d1 + d2 + d3) % Q
    return [
        [alpha, 0, 0, 0],
        [0, d1, (-alpha - d3) % Q, (-alpha - d2) % Q],
        [0, (-alpha - d3) % Q, d2, (-alpha - d1) % Q],
        [0, (-alpha - d2) % Q, (-alpha - d1) % Q, d3],
    ]


def gram(vectors: list[tuple[int, ...]], bilinear: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(
                vectors[i][r] * bilinear[r][s] * vectors[j][s]
                for r in range(4)
                for s in range(4)
            )
            % Q
            for j in range(8)
        ]
        for i in range(8)
    ]


def rank_mod3(matrix: list[list[int]]) -> int:
    work = [[entry % Q for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        if work[rank][column] == 2:
            work[rank] = [(2 * entry) % Q for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [
                    (work[row][j] - scale * work[rank][j]) % Q
                    for j in range(len(work[0]))
                ]
        rank += 1
    return rank


def projective_weight_eight_relations(vectors: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    words = [
        word
        for word in product(range(Q), repeat=8)
        if all(word)
        and all(
            sum(word[j] * vectors[j][coordinate] for j in range(8)) % Q == 0
            for coordinate in range(4)
        )
    ]
    representatives = [
        word
        for word in words
        if word < tuple((2 * entry) % Q for entry in word)
    ]
    assert len(words) == 8
    assert len(representatives) == 4
    return representatives


def tensor_weight_eight_relation(vectors: list[tuple[int, ...]]) -> tuple[int, ...]:
    projective = projective_weight_eight_relations(vectors)
    tensor_relations = [
        word
        for word in projective
        if all(
            sum(word[k] * vectors[k][i] * vectors[k][j] for k in range(8)) % Q == 0
            for i in range(4)
            for j in range(4)
        )
    ]
    assert tensor_relations == [(1, 1, 1, 1, 2, 2, 2, 2)]
    return tensor_relations[0]


def integer_signs(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 if entry == 1 else -1 for entry in word)


def signed_polar_sum(matrix: list[list[int]], signs: tuple[int, ...]) -> int:
    return sum(
        matrix[i][j] * signs[i] * signs[j]
        for i, j in combinations(range(8), 2)
    )


def point_memberships(
    selected_edges: tuple[tuple[int, int], ...],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Realize a triangle-free selected-intersection graph without quotienting labels."""
    memberships: list[tuple[int, ...]] = [tuple(edge) for edge in selected_edges]
    triangles: list[list[int]] = [[] for _ in range(8)]
    for point, edge in enumerate(selected_edges):
        for index in edge:
            triangles[index].append(point)
    for index in range(8):
        while len(triangles[index]) < 3:
            triangles[index].append(len(memberships))
            memberships.append((index,))
        assert len(triangles[index]) == 3
    return memberships, [tuple(row) for row in triangles]


def intersection_profile(
    ones_edges: tuple[tuple[int, int], ...], signs: tuple[int, ...]
) -> tuple[dict[str, int], int]:
    """Complete labelled subset census for one triangle-free product-one graph."""
    counter: Counter[tuple[int, int, int, int, int, int, int]] = Counter()
    accepted = 0
    for mask in range(1 << len(ones_edges)):
        chosen = tuple(edge for bit, edge in enumerate(ones_edges) if mask & (1 << bit))
        memberships, _ = point_memberships(chosen)
        signed_intersection_sum = sum(signs[i] * signs[j] for i, j in chosen)
        if signed_intersection_sum % Q != 1:
            continue
        point_values = [sum(signs[index] for index in membership) for membership in memberships]
        canonical = [value % Q for value in point_values]
        weight = sum(value != 0 for value in canonical)
        if weight not in ALLOWED_POINT_WEIGHTS:
            continue
        positive = canonical.count(1)
        negative = canonical.count(2)
        if weight == 14 and (positive, negative) != (7, 7):
            continue
        same = sum(signs[i] == signs[j] for i, j in chosen)
        opposite = len(chosen) - same
        integer_norm = sum(value * value for value in point_values)
        counter[(len(chosen), same, opposite, weight, positive, negative, integer_norm)] += 1
        accepted += 1
    rows = {
        (
            f"m{key[0]}_same{key[1]}_opposite{key[2]}_w{key[3]}_"
            f"p{key[4]}_n{key[5]}_norm{key[6]}"
        ): count
        for key, count in sorted(counter.items())
    }
    return rows, accepted


def verify_local_controls(
    matrix: list[list[int]], signs: tuple[int, ...]
) -> list[dict[str, int | str | bool]]:
    payload = json.loads(CONTROLS.read_text(encoding="utf-8"))
    assert payload["form_diagonal"] == [2, 2, 2]
    assert tuple(payload["relation"]) == (1, 1, 1, 1, 2, 2, 2, 2)
    summaries: list[dict[str, int | str | bool]] = []
    for control in payload["controls"]:
        triangles = [tuple(row) for row in control["triangles"]]
        vertex_count = max(vertex for row in triangles for vertex in row) + 1
        assert len(triangles) == 8
        assert all(len(set(row)) == 3 for row in triangles)
        intersections = {
            (i, j)
            for i, j in combinations(range(8), 2)
            if set(triangles[i]) & set(triangles[j])
        }
        assert intersections == {tuple(row) for row in control["selected_triangle_intersections"]}
        assert all(len(set(triangles[i]) & set(triangles[j])) == 1 for i, j in intersections)
        assert all(matrix[i][j] == 1 for i, j in intersections)

        internal = {
            tuple(sorted(edge))
            for triangle in triangles
            for edge in combinations(triangle, 2)
        }
        extra = {tuple(sorted(edge)) for edge in control["extra_edges"]}
        assert not internal & extra
        edges = internal | extra

        for i, j in combinations(range(8), 2):
            adjacency_count = sum(
                u != v and tuple(sorted((u, v))) in edges
                for u in triangles[i]
                for v in triangles[j]
            )
            if (i, j) in intersections:
                assert adjacency_count == 4
            else:
                assert adjacency_count == matrix[i][j]

        memberships = [
            tuple(index for index, triangle in enumerate(triangles) if vertex in triangle)
            for vertex in range(vertex_count)
        ]
        b = [sum(signs[index] for index in membership) for membership in memberships]
        assert b == control["b_integer"]
        for vertex in range(vertex_count):
            signed_neighbor_sum = sum(
                b[other]
                for other in range(vertex_count)
                if other != vertex and tuple(sorted((vertex, other))) in edges
            )
            assert signed_neighbor_sum == 3 * b[vertex]

        common_histogram: Counter[tuple[str, int]] = Counter()
        degrees = []
        for vertex in range(vertex_count):
            degrees.append(
                sum(
                    tuple(sorted((vertex, other))) in edges
                    for other in range(vertex_count)
                    if other != vertex
                )
            )
        for left, right in combinations(range(vertex_count), 2):
            common = sum(
                tuple(sorted((left, other))) in edges
                and tuple(sorted((right, other))) in edges
                for other in range(vertex_count)
                if other not in (left, right)
            )
            adjacent = (left, right) in edges
            assert common <= (1 if adjacent else 2)
            common_histogram[("edge" if adjacent else "nonedge", common)] += 1
        assert max(degrees) <= 14

        graph_triangles = [
            triple
            for triple in combinations(range(vertex_count), 3)
            if all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2))
        ]
        prisms = []
        for left, right in combinations(graph_triangles, 2):
            if set(left) & set(right):
                continue
            cross = [
                (u, v)
                for u in left
                for v in right
                if tuple(sorted((u, v))) in edges
            ]
            if (
                len(cross) == 3
                and len({u for u, _ in cross}) == 3
                and len({v for _, v in cross}) == 3
            ):
                prisms.append((left, right))
        assert not prisms

        summaries.append(
            {
                "name": control["name"],
                "vertices": vertex_count,
                "edges": len(edges),
                "selected_intersections": len(intersections),
                "point_weight": sum(value % Q != 0 for value in b),
                "integer_b_norm": sum(value * value for value in b),
                "graph_triangles": len(graph_triangles),
                "induced_triangular_prisms": len(prisms),
                "maximum_induced_degree": max(degrees),
                "exact_AUb_equals_3b": True,
                "lambda_mu_caps": True,
            }
        )
    return summaries


def build_result() -> dict[str, object]:
    vectors = columns()
    projective_linear_relations = projective_weight_eight_relations(vectors)
    relations = [tensor_weight_eight_relation(vectors)]
    relation_rows: list[dict[str, object]] = []
    common_distribution: Counter[int] | None = None
    common_minus24_profiles: dict[str, int] | None = None
    common_plus12_profiles: dict[str, int] | None = None

    for relation_index, relation in enumerate(relations):
        signs = integer_signs(relation)
        distribution: Counter[int] = Counter()
        no_one = 0
        survivor_rows: list[dict[str, object]] = []
        minus24_profiles_for_relation: list[dict[str, int]] = []
        plus12_profiles_for_relation: list[dict[str, int]] = []
        for diagonal in product(range(Q), repeat=3):
            bilinear = restricted_form(diagonal)
            matrix = gram(vectors, bilinear)
            assert all(matrix[i][i] == 0 for i in range(8))
            ones_edges = tuple(
                (i, j) for i, j in combinations(range(8), 2) if matrix[i][j] == 1
            )
            if not ones_edges:
                no_one += 1
            polar_sum = signed_polar_sum(matrix, signs)
            distribution[polar_sum] += 1
            residual_norm = 7 * (24 - 2 * polar_sum)
            survives_divisibility = residual_norm % 9 == 0
            if survives_divisibility:
                assert polar_sum in (-24, 12)
                degrees = [sum(index in edge for edge in ones_edges) for index in range(8)]
                same = sum(signs[i] == signs[j] for i, j in ones_edges)
                profiles, accepted = intersection_profile(ones_edges, signs)
                if polar_sum == -24:
                    assert len(ones_edges) == 8
                    assert sorted(degrees) == [2] * 8
                    assert same == 4
                    assert accepted == 83
                    minus24_profiles_for_relation.append(profiles)
                else:
                    assert len(ones_edges) == 12
                    assert sorted(degrees) == [3] * 8
                    assert same == 0
                    assert accepted == comb(12, 2) + comb(12, 5) == 858
                    plus12_profiles_for_relation.append(profiles)
                survivor_rows.append(
                    {
                        "diagonal": list(diagonal),
                        "rank": rank_mod3(bilinear),
                        "product_one_edges": len(ones_edges),
                        "same_sign_product_one_edges": same,
                        "signed_polar_sum": polar_sum,
                        "residual_squared_norm": residual_norm,
                        "divided_residual_squared_norm": residual_norm // 9,
                        "accepted_labelled_intersection_subsets": accepted,
                    }
                )
        assert no_one == 4
        assert distribution == Counter({0: 19, -12: 4, -24: 3, 12: 1})
        assert len(survivor_rows) == 4
        assert len(minus24_profiles_for_relation) == 3
        assert len(plus12_profiles_for_relation) == 1
        assert all(rows == minus24_profiles_for_relation[0] for rows in minus24_profiles_for_relation)
        if common_distribution is None:
            common_distribution = distribution
            common_minus24_profiles = minus24_profiles_for_relation[0]
            common_plus12_profiles = plus12_profiles_for_relation[0]
        else:
            assert distribution == common_distribution
            assert minus24_profiles_for_relation[0] == common_minus24_profiles
            assert plus12_profiles_for_relation[0] == common_plus12_profiles
        relation_rows.append(
            {
                "relation_index": relation_index,
                "relation": list(relation),
                "surviving_forms": survivor_rows,
            }
        )

    assert len(projective_linear_relations) == 4
    assert len(relations) == 1
    assert common_distribution is not None
    assert common_minus24_profiles is not None
    assert common_plus12_profiles is not None
    canonical_matrix = gram(vectors, restricted_form((2, 2, 2)))
    local_summaries = verify_local_controls(canonical_matrix, integer_signs(relations[0]))

    return {
        "claim_label": "DERIVED",
        "projective_linear_weight_eight_relation_classes": len(projective_linear_relations),
        "projective_tensor_weight_eight_relation_classes": len(relations),
        "concurrent_secant_matchings_retained_without_choice": 4,
        "restricted_polar_forms": 27,
        "signed_polar_sum_distribution": {
            str(value): common_distribution[value] for value in sorted(common_distribution)
        },
        "spectral_divisibility": {
            "residual": "r=(A-3I)B*a_integer",
            "residual_eigenvalue": -4,
            "forced_squared_norm": "7*(24-2*S_D)",
            "coordinate_divisor": 3,
            "required_squared_norm_modulus": 9,
            "admissible_signed_polar_sums": [-24, 12],
        },
        "wave207_no_product_one_forms": 4,
        "additional_wave207_survivors_excluded": 19,
        "surviving_forms": 4,
        "survivor_classes": relation_rows,
        "minus24_intersection_profiles": common_minus24_profiles,
        "plus12_intersection_profiles": common_plus12_profiles,
        "local_controls": local_summaries,
        "limitations": [
            "all conclusions remain conditional on a hypothetical weight-eight endpoint word",
            "the three S_D=-24 forms retain a divided residual -4 eigenvector of squared norm 56",
            "the S_D=12 form retains exact integer A*b=3*b branches of point weight 14 and 20",
            "the local controls omit 77 or 80 graph vertices, outside completion, and the full 231-column frame",
            "no target graph, nonexistence proof, endpoint exclusion, or Conway-99 resolution follows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        assert result == json.loads(RESULTS.read_text(encoding="utf-8"))
        print("PASS: Wave208 marked-M7g spectral-divisibility checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
