"""Small exact checks for the Wave 207 incidence-linear weight-eight lemma.

This audits one canonical M_7g orbit, its 81-word relation code, its
quadratic Veronese rank, and the 27 restricted polar forms.  It does not
search for a graph or for a 231-column endpoint realization.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path

Q = 3
HERE = Path(__file__).resolve().parent
RESULT = HERE / "exact-results.json"


def inv(x: int) -> int:
    x %= Q
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ZeroDivisionError


def rank_mod3(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    a = [[x % Q for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col])
        a[rank] = [(scale * x) % Q for x in a[rank]]
        for i in range(rows):
            if i == rank or not a[i][col]:
                continue
            scale = a[i][col]
            a[i] = [
                (a[i][j] - scale * a[rank][j]) % Q
                for j in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) % Q for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def canonical_columns() -> tuple[list[tuple[int, ...]], list[int], list[tuple[int, int]]]:
    p = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    center = (1, 1, 1)
    n = [tuple((2 * center[j] - x[j]) % Q for j in range(3)) for x in p]
    columns = [(1, *x) for x in p + n]
    signs = [1] * 4 + [2] * 4
    pairs = [(i, i + 4) for i in range(4)]
    return columns, signs, pairs


def column_matrix(columns: list[tuple[int, ...]]) -> list[list[int]]:
    return [[columns[j][i] for j in range(len(columns))] for i in range(4)]


def vector_sum(columns: list[tuple[int, ...]], coeffs: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(
        sum(coeffs[j] * columns[j][i] for j in range(len(columns))) % Q
        for i in range(4)
    )


def tensor_sum(columns: list[tuple[int, ...]], coeffs: list[int]) -> list[list[int]]:
    return [
        [
            sum(coeffs[k] * columns[k][i] * columns[k][j] for k in range(len(columns))) % Q
            for j in range(4)
        ]
        for i in range(4)
    ]


def veronese_columns(columns: list[tuple[int, ...]]) -> list[list[int]]:
    monomials = [(i, j) for i in range(4) for j in range(i, 4)]
    return [[v[i] * v[j] % Q for v in columns] for i, j in monomials]


def relation_code_summary(columns: list[tuple[int, ...]], pairs: list[tuple[int, int]]) -> dict[str, object]:
    words: list[tuple[int, ...]] = []
    for coeffs in product(range(Q), repeat=8):
        if vector_sum(columns, coeffs) == (0, 0, 0, 0):
            words.append(coeffs)
    weights = Counter(sum(x != 0 for x in word) for word in words)

    dependent_supports: set[frozenset[int]] = set()
    for word in words:
        support = frozenset(i for i, x in enumerate(word) if x)
        if support:
            dependent_supports.add(support)
    circuit_supports = {
        support
        for support in dependent_supports
        if not any(other < support for other in dependent_supports)
    }
    circuits_by_weight = Counter(len(support) for support in circuit_supports)

    pair_sets = [frozenset(pair) for pair in pairs]
    paired_plane_circuits = sum(
        1
        for support in circuit_supports
        if len(support) == 4
        and sum(pair <= support for pair in pair_sets) == 2
    )
    return {
        "dimension": 4,
        "words": len(words),
        "weight_enumerator": {str(k): weights[k] for k in sorted(weights)},
        "projective_circuit_supports": {
            str(k): circuits_by_weight[k] for k in sorted(circuits_by_weight)
        },
        "weight4_circuits_from_two_concurrent_pairs": paired_plane_circuits,
    }


def graph_components(vertices: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    adjacency = {i: set() for i in range(vertices)}
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    components: list[list[int]] = []
    unseen = set(range(vertices))
    while unseen:
        root = min(unseen)
        queue = deque([root])
        unseen.remove(root)
        component: list[int] = []
        while queue:
            v = queue.popleft()
            component.append(v)
            for w in sorted(adjacency[v] & unseen):
                unseen.remove(w)
                queue.append(w)
        components.append(sorted(component))
    return sorted(components, key=lambda c: (len(c), c))


def restricted_form(diagonal: tuple[int, int, int]) -> list[list[int]]:
    d1, d2, d3 = diagonal
    alpha = (d1 + d2 + d3) % Q
    c12 = (-alpha - d3) % Q
    c13 = (-alpha - d2) % Q
    c23 = (-alpha - d1) % Q
    return [
        [alpha, 0, 0, 0],
        [0, d1, c12, c13],
        [0, c12, d2, c23],
        [0, c13, c23, d3],
    ]


def gram(columns: list[tuple[int, ...]], form: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(columns[i][r] * form[r][s] * columns[j][s] for r in range(4) for s in range(4)) % Q
            for j in range(8)
        ]
        for i in range(8)
    ]


def classify_zero_graph(matrix: list[list[int]]) -> str:
    edges = {(i, j) for i in range(8) for j in range(i + 1, 8) if matrix[i][j] == 0}
    components = graph_components(8, edges)
    degrees = [sum(matrix[i][j] == 0 for j in range(8) if i != j) for i in range(8)]
    signature = (len(edges), tuple(sorted(map(len, components))), tuple(sorted(degrees)))
    names = {
        (28, (8,), (7,) * 8): "K8",
        (12, (4, 4), (3,) * 8): "2K4",
        (4, (2, 2, 2, 2), (1,) * 8): "4K2",
        (8, (4, 4), (2,) * 8): "2C4",
    }
    if signature not in names:
        raise AssertionError(f"unexpected zero graph {signature}")
    return names[signature]


def polar_form_summary(columns: list[tuple[int, ...]], pairs: list[tuple[int, int]]) -> dict[str, object]:
    # The three-parameter form is written after translating the common
    # affine center (1,1,1) to the origin.
    centered = [
        (column[0], *((column[j] - column[0]) % Q for j in range(1, 4)))
        for column in columns
    ]
    rank_counts: Counter[int] = Counter()
    graph_by_rank: dict[int, set[str]] = {}
    center_values: dict[int, Counter[int]] = {}
    for diagonal in product(range(Q), repeat=3):
        form = restricted_form(diagonal)
        matrix = gram(centered, form)
        if any(matrix[i][i] for i in range(8)):
            raise AssertionError("canonical support point is not singular")
        rank = rank_mod3(form)
        rank_counts[rank] += 1
        graph_by_rank.setdefault(rank, set()).add(classify_zero_graph(matrix))
        values = {matrix[i][j] for i, j in pairs}
        if len(values) != 1:
            raise AssertionError("concurrent-pair inner products differ")
        center_values.setdefault(rank, Counter())[next(iter(values))] += 1

    return {
        "form_space_dimension": 3,
        "forms": 27,
        "rank_counts": {str(k): rank_counts[k] for k in sorted(rank_counts)},
        "zero_graph_by_rank": {
            str(k): sorted(graph_by_rank[k]) for k in sorted(graph_by_rank)
        },
        "concurrent_pair_gram_value_counts_by_rank": {
            str(rank): {str(value): count for value, count in sorted(counter.items())}
            for rank, counter in sorted(center_values.items())
        },
    }


def build_result() -> dict[str, object]:
    columns, signs, pairs = canonical_columns()
    matrix = column_matrix(columns)
    cap = all(
        rank_mod3([[columns[j][i] for j in subset] for i in range(4)]) == 3
        for subset in combinations(range(8), 3)
    )
    first_moment = vector_sum(columns, signs)
    second_moment = tensor_sum(columns, signs)
    veronese = veronese_columns(columns)
    return {
        "scope": (
            "canonical symbolic audit of the conditional weight-eight support; "
            "no graph or 231-column endpoint search"
        ),
        "canonical_support": {
            "columns": [list(column) for column in columns],
            "coefficients": signs,
            "composition": {"1": 4, "2": 4},
            "column_rank": rank_mod3(matrix),
            "every_three_independent": cap,
            "signed_first_moment": list(first_moment),
            "signed_second_moment_zero": not any(map(any, second_moment)),
            "quadratic_veronese_rank": rank_mod3(veronese),
            "quadratic_relation_nullity": 8 - rank_mod3(veronese),
            "concurrent_pairs": [[i, j] for i, j in pairs],
        },
        "relation_code": relation_code_summary(columns, pairs),
        "restricted_polar_forms": polar_form_summary(columns, pairs),
        "limitations": [
            "the canonical support is not a 231-column endpoint construction",
            "membership of the signed word in a target im(B^T) is not constructed",
            "the four forced anticompleteness patterns are not excluded",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        archived = json.loads(RESULT.read_text(encoding="utf-8"))
        if result != archived:
            raise AssertionError("archived exact result does not match reconstruction")
        print("PASS: Wave207 incidence-tensor canonical checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
