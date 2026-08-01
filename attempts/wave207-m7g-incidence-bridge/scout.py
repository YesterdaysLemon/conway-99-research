#!/usr/bin/env python3
"""Restricted local scout for the Wave 207 M7g incidence bridge.

This is a discovery aid, not a proof-producing graph search.  It restricts
selected-triangle intersections to pair-specific vertices (no vertex belongs
to three selected triangles), then asks Z3 for an induced graph on the union
of the selected triangles.  A returned model can be checked independently by
``exact_check.py``.  Failure to find a model proves nothing.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, product

from z3 import And, Bool, BoolVal, If, Not, Or, Solver, Sum, sat

Q = 3
SIGNS = (1, 1, 1, 1, 2, 2, 2, 2)


def inv(value: int) -> int:
    value %= Q
    if value == 1:
        return 1
    if value == 2:
        return 2
    raise ZeroDivisionError


def rank_mod3(matrix: list[list[int]]) -> int:
    work = [[value % Q for value in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][column])
        work[rank] = [(scale * value) % Q for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                (work[row][j] - scale * work[rank][j]) % Q
                for j in range(len(work[0]))
            ]
        rank += 1
    return rank


def canonical_columns() -> list[tuple[int, int, int, int]]:
    positive = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    center = (1, 1, 1)
    negative = tuple(
        tuple((2 * center[j] - point[j]) % Q for j in range(3))
        for point in positive
    )
    columns = [(1, *point) for point in positive + negative]
    return [
        (column[0], *((column[j] - column[0]) % Q for j in range(1, 4)))
        for column in columns
    ]


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


def gram(
    columns: list[tuple[int, int, int, int]], form: list[list[int]]
) -> list[list[int]]:
    return [
        [
            sum(
                columns[i][r] * form[r][s] * columns[j][s]
                for r in range(4)
                for s in range(4)
            )
            % Q
            for j in range(8)
        ]
        for i in range(8)
    ]


def zero_graph_name(matrix: list[list[int]]) -> str:
    degrees = sorted(
        sum(matrix[i][j] == 0 for j in range(8) if i != j) for i in range(8)
    )
    zeros = sum(matrix[i][j] == 0 for i in range(8) for j in range(i + 1, 8))
    return {
        (28, (7,) * 8): "K8",
        (12, (3,) * 8): "2K4",
        (4, (1,) * 8): "4K2",
        (8, (2,) * 8): "2C4",
    }[(zeros, tuple(degrees))]


def norm_ok(intersections: frozenset[tuple[int, int]]) -> bool:
    value = 2 * sum(SIGNS[i] * SIGNS[j] for i, j in intersections)
    return value % Q == sum(value * value for value in SIGNS) % Q


def intersection_subgraphs(matrix: list[list[int]]):
    possible = [
        (i, j)
        for i in range(8)
        for j in range(i + 1, 8)
        if matrix[i][j] == 1
    ]
    # Pair-specific intersections use one distinct triangle vertex per
    # incident pair, so selected-triangle intersection degree is at most 3.
    for mask in range(1 << len(possible)):
        chosen = frozenset(
            edge for index, edge in enumerate(possible) if (mask >> index) & 1
        )
        degree = [0] * 8
        for i, j in chosen:
            degree[i] += 1
            degree[j] += 1
        if max(degree, default=0) <= 3 and norm_ok(chosen):
            yield chosen


def make_vertices(
    intersections: frozenset[tuple[int, int]],
) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    vertices: list[tuple[int, ...]] = [tuple(edge) for edge in sorted(intersections)]
    triangles: list[list[int]] = [[] for _ in range(8)]
    for vertex, membership in enumerate(vertices):
        for triangle in membership:
            triangles[triangle].append(vertex)
    for triangle in range(8):
        while len(triangles[triangle]) < 3:
            vertex = len(vertices)
            vertices.append((triangle,))
            triangles[triangle].append(vertex)
    return vertices, triangles


def selected_internal_edges(triangles: list[list[int]]) -> set[tuple[int, int]]:
    return {
        tuple(sorted(edge))
        for triangle in triangles
        for edge in combinations(triangle, 2)
    }


def find_local_model(
    matrix: list[list[int]],
    intersections: frozenset[tuple[int, int]],
    *,
    enforce_common_neighbor_caps: bool = True,
    random_seed: int = 0,
) -> dict[str, object] | None:
    memberships, triangles = make_vertices(intersections)
    internal = selected_internal_edges(triangles)
    count = len(memberships)

    candidates: list[tuple[int, int]] = []
    for u, v in combinations(range(count), 2):
        edge = (u, v)
        if edge in internal:
            continue
        # An extra outer edge between two intersecting selected triangles
        # would give an edge a second common neighbor, since their shared
        # point is already one.
        if any(
            tuple(sorted((i, j))) in intersections
            for i in memberships[u]
            for j in memberships[v]
            if i != j
        ):
            continue
        candidates.append(edge)

    solver = Solver()
    solver.set(random_seed=random_seed)
    variables = {edge: Bool(f"e_{edge[0]}_{edge[1]}") for edge in candidates}

    def edge_boolean(u: int, v: int):
        if u == v:
            return BoolVal(False)
        edge = tuple(sorted((u, v)))
        if edge in internal:
            return BoolVal(True)
        if edge in variables:
            return variables[edge]
        return BoolVal(False)

    def edge_indicator(u: int, v: int):
        return If(edge_boolean(u, v), 1, 0)

    # Exact centered products: intersecting pairs have no outer edge;
    # disjoint pairs have exactly D_ij matching/cross edges.
    for i, j in combinations(range(8), 2):
        total = Sum(
            [edge_indicator(u, v) for u in triangles[i] for v in triangles[j]]
        )
        if (i, j) in intersections:
            # Four ordered-by-block incidences come from the common point;
            # on the simple induced graph the union has exactly the two
            # selected triangles and no additional outer edge.
            expected = 4
        else:
            expected = matrix[i][j]
        solver.add(total == expected)

    b = [sum(SIGNS[i] for i in membership) % Q for membership in memberships]

    # Ab=0.  Vertices outside this union have b-coordinate zero, so this is
    # an exact equation on the induced graph, not a closure assumption.
    for u in range(count):
        neighbor_sum = Sum(
            [edge_indicator(u, v) * b[v] for v in range(count) if v != u]
        )
        solver.add(Or(*[neighbor_sum == 3 * value for value in range(10)]))

    # Necessary local SRG conditions and the target degree cap.
    for u in range(count):
        solver.add(
            Sum([edge_indicator(u, v) for v in range(count) if v != u]) <= 14
        )

    # Every edge internal to a selected triangle already has its unique
    # selected third vertex.  Forbid a second common neighbor up front.
    for u, v in sorted(internal):
        selected_thirds = [
            w
            for triangle in triangles
            if u in triangle and v in triangle
            for w in triangle
            if w not in (u, v)
        ]
        if len(selected_thirds) != 1:
            raise AssertionError("selected internal edge lacks a unique third")
        third = selected_thirds[0]
        for w in range(count):
            if w in (u, v, third):
                continue
            solver.add(Not(And(edge_boolean(u, w), edge_boolean(v, w))))

    # The same lambda cap for an edge not internal to a selected triangle is
    # conditional on that edge being chosen.
    for u, v in combinations(range(count), 2):
        if (u, v) in internal:
            continue
        possible_common = [
            w
            for w in range(count)
            if w not in (u, v)
            and not (str(edge_boolean(u, w)) == "False")
            and not (str(edge_boolean(v, w)) == "False")
        ]
        for w1, w2 in combinations(possible_common, 2):
            solver.add(
                Not(
                    And(
                        edge_boolean(u, v),
                        edge_boolean(u, w1),
                        edge_boolean(v, w1),
                        edge_boolean(u, w2),
                        edge_boolean(v, w2),
                    )
                )
            )
    # Add common-neighbor caps lazily.  This keeps the discovery solver in
    # propositional/pseudo-Boolean territory and every returned model is
    # still checked against every pair below (and again independently).
    for _ in range(10000):
        if solver.check() != sat:
            return None
        model = solver.model()

        def is_edge(u: int, v: int) -> bool:
            return bool(model.eval(edge_boolean(u, v), model_completion=True))

        violation = None
        if not enforce_common_neighbor_caps:
            break
        for u, v in combinations(range(count), 2):
            common = [
                w
                for w in range(count)
                if w not in (u, v) and is_edge(u, w) and is_edge(v, w)
            ]
            limit = 1 if is_edge(u, v) else 2
            if len(common) > limit:
                violation = (u, v, common[: limit + 1], limit)
                break
        if violation is None:
            break
        u, v, witnesses, limit = violation
        terms = [edge_boolean(u, w) for w in witnesses] + [
            edge_boolean(v, w) for w in witnesses
        ]
        if limit == 1:
            terms.append(edge_boolean(u, v))
        else:
            terms.append(Not(edge_boolean(u, v)))
        solver.add(Not(And(*terms)))
    else:
        return None
    extra = [
        list(edge)
        for edge, variable in sorted(variables.items())
        if bool(model.eval(variable, model_completion=True))
    ]
    return {
        "vertex_memberships": [list(membership) for membership in memberships],
        "triangles": triangles,
        "selected_triangle_intersections": [list(edge) for edge in sorted(intersections)],
        "internal_edges": [list(edge) for edge in sorted(internal)],
        "extra_edges": extra,
        "b": b,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="keep one model for each form subtype")
    args = parser.parse_args()
    columns = canonical_columns()
    found: list[dict[str, object]] = []
    seen_ranks: set[int] = set()
    for diagonal in product(range(Q), repeat=3):
        form = restricted_form(diagonal)
        rank = rank_mod3(form)
        if rank == 0:
            continue
        if not args.all and rank in seen_ranks:
            continue
        matrix = gram(columns, form)
        for intersections in intersection_subgraphs(matrix):
            local = find_local_model(matrix, intersections)
            if local is None:
                continue
            found.append(
                {
                    "form_diagonal": list(diagonal),
                    "form_rank": rank,
                    "zero_graph": zero_graph_name(matrix),
                    "gram": matrix,
                    **local,
                }
            )
            seen_ranks.add(rank)
            break
    print(json.dumps({"restricted_scope": "pair-specific selected-triangle intersections", "models": found}, indent=2))


if __name__ == "__main__":
    main()
