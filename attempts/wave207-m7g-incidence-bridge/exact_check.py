#!/usr/bin/env python3
"""Independent exact checker for the Wave 207 M7g incidence bridge."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

Q = 3
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "local-rank4-certificate.json"
RESULT = HERE / "exact-results.json"
SIGNS = (1, 1, 1, 1, 2, 2, 2, 2)


def rank_mod3(matrix: list[list[int]]) -> int:
    a = [[value % Q for value in row] for row in matrix]
    rank = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((row for row in range(rank, len(a)) if a[row][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        if a[rank][column] == 2:
            a[rank] = [(2 * value) % Q for value in a[rank]]
        for row in range(len(a)):
            if row != rank and a[row][column]:
                scale = a[row][column]
                a[row] = [
                    (a[row][j] - scale * a[rank][j]) % Q
                    for j in range(len(a[0]))
                ]
        rank += 1
    return rank


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


def form(diagonal: tuple[int, int, int]) -> list[list[int]]:
    d1, d2, d3 = diagonal
    alpha = (d1 + d2 + d3) % Q
    return [
        [alpha, 0, 0, 0],
        [0, d1, (-alpha - d3) % Q, (-alpha - d2) % Q],
        [0, (-alpha - d3) % Q, d2, (-alpha - d1) % Q],
        [0, (-alpha - d2) % Q, (-alpha - d1) % Q, d3],
    ]


def gram(vectors, bilinear):
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


def zero_graph(matrix: list[list[int]]) -> str:
    degrees = tuple(
        sorted(sum(matrix[i][j] == 0 for j in range(8) if j != i) for i in range(8))
    )
    zeros = sum(matrix[i][j] == 0 for i, j in combinations(range(8), 2))
    return {
        (28, (7,) * 8): "K8",
        (12, (3,) * 8): "2K4",
        (4, (1,) * 8): "4K2",
        (8, (2,) * 8): "2C4",
    }[(zeros, degrees)]


def relation_data(vectors):
    words = [
        word
        for word in product(range(Q), repeat=8)
        if all(sum(word[j] * vectors[j][i] for j in range(8)) % Q == 0 for i in range(4))
    ]
    supports = {frozenset(i for i, value in enumerate(word) if value) for word in words if any(word)}
    circuits = {support for support in supports if not any(other < support for other in supports)}
    return words, circuits


def build_result(certificate_path: Path = CERTIFICATE) -> dict[str, object]:
    vectors = columns()
    # The fixed 4+4 word has both its first and second moments zero.
    assert all(sum(SIGNS[j] * vectors[j][i] for j in range(8)) % Q == 0 for i in range(4))
    assert all(
        sum(SIGNS[k] * vectors[k][i] * vectors[k][j] for k in range(8)) % Q == 0
        for i in range(4)
        for j in range(4)
    )

    form_classes: Counter[tuple[int, str, int]] = Counter()
    no_one: Counter[int] = Counter()
    row_relation_weights: dict[int, set[int]] = {}
    for diagonal in product(range(Q), repeat=3):
        bilinear = form(diagonal)
        matrix = gram(vectors, bilinear)
        assert all(matrix[i][i] == 0 for i in range(8))
        rank = rank_mod3(bilinear)
        ones = sum(matrix[i][j] == 1 for i, j in combinations(range(8), 2))
        name = zero_graph(matrix)
        form_classes[(rank, name, ones)] += 1
        if ones == 0:
            no_one[rank] += 1
        weights = {
            sum(SIGNS[j] * matrix[i][j] % Q != 0 for j in range(8))
            for i in range(8)
        }
        row_relation_weights.setdefault(rank, set()).update(weights)
        for i in range(8):
            row_word = [SIGNS[j] * matrix[i][j] % Q for j in range(8)]
            assert all(
                sum(row_word[j] * vectors[j][coordinate] for j in range(8)) % Q == 0
                for coordinate in range(4)
            )

    assert no_one == Counter({2: 3, 0: 1})

    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    triangles = [tuple(row) for row in certificate["triangles"]]
    memberships = [tuple(row) for row in certificate["vertex_memberships"]]
    assert len(triangles) == 8 and all(len(set(row)) == 3 for row in triangles)
    for vertex, membership in enumerate(memberships):
        assert membership == tuple(i for i, triangle in enumerate(triangles) if vertex in triangle)

    intersections = {
        (i, j)
        for i, j in combinations(range(8), 2)
        if set(triangles[i]) & set(triangles[j])
    }
    assert intersections == {tuple(row) for row in certificate["selected_triangle_intersections"]}
    assert all(len(set(triangles[i]) & set(triangles[j])) == 1 for i, j in intersections)

    diagonal = tuple(certificate["form_diagonal"])
    matrix = gram(vectors, form(diagonal))
    assert rank_mod3(form(diagonal)) == certificate["form_rank"] == 4
    assert zero_graph(matrix) == certificate["zero_graph"] == "2C4"
    assert all(matrix[i][j] == 1 for i, j in intersections)

    internal = {tuple(sorted(row)) for row in certificate["internal_edges"]}
    expected_internal = {
        tuple(sorted(edge)) for triangle in triangles for edge in combinations(triangle, 2)
    }
    assert internal == expected_internal
    extra = {tuple(sorted(row)) for row in certificate["extra_edges"]}
    assert not internal & extra
    edges = internal | extra
    vertex_count = len(memberships)

    # Exact selected-pair incidence realizes the polar Gram: four adjacency
    # incidences for an intersecting pair, and D_ij cross edges when disjoint.
    for i, j in combinations(range(8), 2):
        adjacency_count = sum(
            u != v and tuple(sorted((u, v))) in edges
            for u in triangles[i]
            for v in triangles[j]
        )
        if (i, j) in intersections:
            assert adjacency_count == 4 and matrix[i][j] == 1
        else:
            assert adjacency_count == matrix[i][j]

    b = [sum(SIGNS[i] for i in membership) % Q for membership in memberships]
    assert b == certificate["b"]
    assert sum(value * value for value in b) % Q == 2
    assert sum(value * value for value in SIGNS) % Q == 2
    assert sum(b) % Q == 0
    for vertex in range(vertex_count):
        assert (
            sum(b[other] for other in range(vertex_count) if tuple(sorted((vertex, other))) in edges)
            % Q
            == 0
        )

    degrees = [sum(tuple(sorted((u, v))) in edges for v in range(vertex_count) if u != v) for u in range(vertex_count)]
    common_histogram: Counter[tuple[str, int]] = Counter()
    for u, v in combinations(range(vertex_count), 2):
        common = sum(
            tuple(sorted((u, w))) in edges and tuple(sorted((v, w))) in edges
            for w in range(vertex_count)
            if w not in (u, v)
        )
        adjacent = (u, v) in edges
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
        cross = [(u, v) for u in left for v in right if tuple(sorted((u, v))) in edges]
        if len(cross) == 3 and len({u for u, _ in cross}) == len({v for _, v in cross}) == 3:
            prisms.append((left, right))
    assert not prisms

    words, circuits = relation_data(vectors)
    weights = Counter(sum(value != 0 for value in word) for word in words)
    circuit_weights = Counter(len(support) for support in circuits)
    assert weights == Counter({6: 32, 4: 24, 5: 16, 8: 8, 0: 1})
    assert circuit_weights == Counter({4: 12, 5: 8})
    cross_realization_histogram: Counter[tuple[int, int]] = Counter()
    for support in circuits:
        realizations = 0
        for x, y in combinations(range(vertex_count), 2):
            hits = [int(x in triangles[i]) + int(y in triangles[i]) for i in support]
            if all(hit == 1 for hit in hits) and any(x in triangles[i] for i in support) and any(y in triangles[i] for i in support):
                realizations += 1
        cross_realization_histogram[(len(support), realizations)] += 1
    assert cross_realization_histogram == Counter({(4, 0): 12, (5, 0): 8})

    return {
        "no_product_one_exclusions": {
            "total_forms": sum(no_one.values()),
            "by_rank": {str(rank): no_one[rank] for rank in sorted(no_one)},
            "zero_graphs": ["K8", "2K4"],
        },
        "form_classes": {
            f"rank{rank}_{name}_ones{ones}": count
            for (rank, name, ones), count in sorted(form_classes.items())
        },
        "polar_row_relation_weights_by_rank": {
            str(rank): sorted(values) for rank, values in sorted(row_relation_weights.items())
        },
        "local_rank4_certificate": {
            "vertices": vertex_count,
            "edges": len(edges),
            "selected_intersections": len(intersections),
            "graph_triangles": len(graph_triangles),
            "induced_triangular_prisms": len(prisms),
            "maximum_local_degree": max(degrees),
            "Ab_zero": True,
            "b_norm": 2,
            "lambda_local_cap": True,
            "mu_local_cap": True,
            "common_neighbor_histogram": {
                f"{kind}_{value}": count
                for (kind, value), count in sorted(common_histogram.items())
            },
        },
        "internal_circuits": {
            "weight_enumerator": {str(weight): weights[weight] for weight in sorted(weights)},
            "projective_circuits": {str(weight): circuit_weights[weight] for weight in sorted(circuit_weights)},
            "certificate_cross_realizations": {
                f"weight{weight}_multiplicity{multiplicity}": count
                for (weight, multiplicity), count in sorted(cross_realization_histogram.items())
            },
        },
        "limitations": [
            "the certificate is an induced 23-vertex necessary-condition model, not a 99-vertex SRG completion",
            "edges with no common neighbor inside the certificate require outside completion",
            "the other 223 triangle blocks and the full 231-column rank-11 frame are absent",
            "internal weight-four and weight-five circuits are not asserted to lie in im(B^T)",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    args = parser.parse_args()
    result = build_result(args.certificate)
    if args.verify:
        assert result == json.loads(RESULT.read_text(encoding="utf-8"))
        print("PASS: Wave207 M7g incidence bridge exact checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

