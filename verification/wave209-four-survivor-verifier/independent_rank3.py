#!/usr/bin/env python3
"""Clean-room Wave 209 verifier for the conditional rank-three trade.

This module uses only Python's standard library.  It does not import or call
the Wave 209 discovery package.  All finite sets are labelled; symmetries are
used only in tests and canonical display, never to discard search cases.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
from typing import Iterable, Iterator, Sequence

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "exact-results.json"

SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
LINE_PAIRS = tuple(combinations(range(8), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(LINE_PAIRS)}
PRODUCT_PAIRS = tuple((i, j + 4) for i in range(4) for j in range(4) if i != j)
MATCHED_PAIRS = tuple((i, i + 4) for i in range(4))

# Canonical integer residues for the rank-three (2,2,2) polar form.  For
# disjoint selected triangles, lambda=1 makes their cross graph a matching,
# hence its size is at most three and this residue is already the exact size,
# except at residue zero where size three must still be excluded.
CANONICAL_GRAM = (
    (0, 2, 2, 2, 0, 1, 1, 1),
    (2, 0, 2, 2, 1, 0, 1, 1),
    (2, 2, 0, 2, 1, 1, 0, 1),
    (2, 2, 2, 0, 1, 1, 1, 0),
    (0, 1, 1, 1, 0, 2, 2, 2),
    (1, 0, 1, 1, 2, 0, 2, 2),
    (1, 1, 0, 1, 2, 2, 0, 2),
    (1, 1, 1, 0, 2, 2, 2, 0),
)

# A representative of the unique rooted seven-vertex sign-side graph.  Vertex
# zero is the endpoint of the sole opposite-sign support edge.
ROOTED_GRAPH = frozenset(
    {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (4, 6),
        (5, 6),
    }
)


def canonical_json_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def adjacency(vertex_count: int, edges: Iterable[tuple[int, int]]) -> list[set[int]]:
    rows = [set() for _ in range(vertex_count)]
    for left, right in edges:
        if left == right:
            raise AssertionError("loop")
        rows[left].add(right)
        rows[right].add(left)
    return rows


def r3k_residual(
    intersections: Iterable[tuple[int, int]], matched_three: Sequence[int]
) -> tuple[int, ...]:
    """Return (R-3K)alpha for four possible q=0 size-three crosses."""

    selected = {tuple(sorted(edge)) for edge in intersections}
    if len(matched_three) != 4 or any(value not in (0, 1) for value in matched_three):
        raise ValueError("matched_three must contain four bits")
    k_matrix = [[0] * 8 for _ in range(8)]
    r_matrix = [[0] * 8 for _ in range(8)]
    for index in range(8):
        k_matrix[index][index] = 3
        r_matrix[index][index] = 6
    for left, right in LINE_PAIRS:
        if (left, right) in selected:
            k_value, r_value = 1, 4
        elif (left, right) in MATCHED_PAIRS:
            k_value, r_value = 0, 3 * matched_three[left if left < 4 else right]
        else:
            k_value, r_value = 0, CANONICAL_GRAM[left][right]
        k_matrix[left][right] = k_matrix[right][left] = k_value
        r_matrix[left][right] = r_matrix[right][left] = r_value
    return tuple(
        sum((r_matrix[i][j] - 3 * k_matrix[i][j]) * SIGNS[j] for j in range(8))
        for i in range(8)
    )


def r3k_census() -> dict[str, object]:
    all_marked = list(combinations(PRODUCT_PAIRS, 2)) + list(combinations(PRODUCT_PAIRS, 5))
    checked = 0
    for marked in all_marked:
        for mask in range(16):
            flags = tuple((mask >> index) & 1 for index in range(4))
            residual = r3k_residual(marked, flags)
            if (not any(residual)) != (mask == 0):
                raise AssertionError("(R-3K)alpha does not isolate the matched q=0 crosses")
            expected = tuple(
                -3 * flags[index] if index < 4 else 3 * flags[index - 4]
                for index in range(8)
            )
            if residual != expected:
                raise AssertionError("coordinate formula for matched crosses differs")
            checked += 1
    return {
        "coordinate_formula": "(-3*h0,-3*h1,-3*h2,-3*h3,3*h0,3*h1,3*h2,3*h3)",
        "matched_q0_cross_counts": [0, 0, 0, 0],
        "marked_and_mask_cases_checked": checked,
        "labelled_marked_sets_checked": len(all_marked),
        "uses_automorphism_quotient": False,
    }


def graph_code(edges: Iterable[tuple[int, int]]) -> int:
    normalized = {tuple(sorted(edge)) for edge in edges}
    return sum(1 << PAIR_INDEX_7[edge] for edge in normalized)


PAIRS_7 = tuple(combinations(range(7), 2))
PAIR_INDEX_7 = {pair: index for index, pair in enumerate(PAIRS_7)}


def rooted_canonical_code(edges: Iterable[tuple[int, int]]) -> int:
    normalized = {tuple(sorted(edge)) for edge in edges}
    best: int | None = None
    for tail in permutations(range(1, 7)):
        image = (0,) + tail
        transformed = {tuple(sorted((image[left], image[right]))) for left, right in normalized}
        code = graph_code(transformed)
        best = code if best is None else min(best, code)
    if best is None:
        raise AssertionError("empty canonical orbit")
    return best


def rooted_graph_census() -> dict[str, object]:
    labelled: list[frozenset[tuple[int, int]]] = []
    tail_pairs = tuple(combinations(range(1, 7), 2))
    for root_neighbors in combinations(range(1, 7), 4):
        root_set = set(root_neighbors)
        required = {vertex: 3 - int(vertex in root_set) for vertex in range(1, 7)}
        for chosen in combinations(tail_pairs, 7):
            degrees = Counter(vertex for edge in chosen for vertex in edge)
            if any(degrees[vertex] != required[vertex] for vertex in range(1, 7)):
                continue
            edges = frozenset({(0, vertex) for vertex in root_set} | set(chosen))
            adj = adjacency(7, edges)
            if any(
                len(adj[left] & adj[right]) > (1 if right in adj[left] else 2)
                for left, right in PAIRS_7
            ):
                continue
            labelled.append(edges)
    codes = {rooted_canonical_code(edges) for edges in labelled}
    if len(labelled) != 180 or len(codes) != 1:
        raise AssertionError("rooted graph census differs")
    if rooted_canonical_code(ROOTED_GRAPH) not in codes:
        raise AssertionError("display representative is outside the unique orbit")
    return {
        "labelled_graphs": len(labelled),
        "rooted_isomorphism_classes": len(codes),
        "representative_edges": [list(edge) for edge in sorted(ROOTED_GRAPH)],
        "degree_sequence": sorted((len(row) for row in adjacency(7, ROOTED_GRAPH)), reverse=True),
    }


def deficit_edges(edges: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    normalized = {tuple(sorted(edge)) for edge in edges}
    adj = adjacency(7, normalized)
    deficits: list[tuple[int, int]] = []
    for left, right in PAIRS_7:
        required = 1 if (left, right) in normalized else 2
        missing = required - len(adj[left] & adj[right])
        if missing < 0:
            raise AssertionError("common-neighbor cap exceeded")
        deficits.extend([(left, right)] * missing)
    return tuple(deficits)


def deficit_triangle_free(deficits: Sequence[tuple[int, int]]) -> bool:
    edges = set(deficits)
    return not any(all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2)) for triple in combinations(range(7), 3))


def valid_deficit_bijection(
    plus: Sequence[tuple[int, int]], minus_permuted: Sequence[tuple[int, int]]
) -> bool:
    if len(plus) != 7 or len(minus_permuted) != 7:
        return False
    if Counter(minus_permuted) != Counter(deficit_edges(ROOTED_GRAPH)):
        return False
    multiplicity: Counter[tuple[int, int]] = Counter()
    for plus_edge, minus_edge in zip(plus, minus_permuted):
        for positive in plus_edge:
            for negative in minus_edge:
                multiplicity[(positive, negative)] += 1
    return max(multiplicity.values(), default=0) <= 2


def deficit_census() -> dict[str, object]:
    deficits = deficit_edges(ROOTED_GRAPH)
    if len(deficits) != 7 or len(set(deficits)) != 7:
        raise AssertionError("deficit graph is not a seven-edge simple graph")
    if any(0 in edge for edge in deficits):
        raise AssertionError("root unexpectedly occurs in a deficit pair")
    if not deficit_triangle_free(deficits):
        raise AssertionError("deficit graph contains a triangle")
    valid = 0
    invalid_max_three = 0
    for row in permutations(deficits):
        if valid_deficit_bijection(deficits, row):
            valid += 1
        else:
            invalid_max_three += 1
    if valid != 4480 or invalid_max_three != 560:
        raise AssertionError("deficit-bijection census differs")
    return {
        "deficit_edges": [list(edge) for edge in deficits],
        "triangle_free": True,
        "root_isolated": True,
        "labelled_bijections": factorial(7),
        "valid_bijections": valid,
        "invalid_bijections": invalid_max_three,
        "validity_rule": "each opposite-sign support pair receives at most two outside common neighbors",
    }


def partition_root_sets() -> dict[tuple[int, int, int, int], frozenset[int]]:
    """Root locations for support-side partitions into four selected lines."""

    root_sets: defaultdict[tuple[int, int, int, int], set[int]] = defaultdict(set)
    for assignment in product(range(4), repeat=7):
        sizes = tuple(assignment.count(label) for label in range(4))
        if any(size > 3 for size in sizes):
            continue
        ok = True
        for label in range(4):
            vertices = [vertex for vertex in range(7) if assignment[vertex] == label]
            if any(tuple(sorted(edge)) not in ROOTED_GRAPH for edge in combinations(vertices, 2)):
                ok = False
                break
        if not ok:
            continue
        for left, right in combinations(range(4), 2):
            cross = [
                edge
                for edge in ROOTED_GRAPH
                if {assignment[edge[0]], assignment[edge[1]]} == {left, right}
            ]
            endpoints = [vertex for edge in cross for vertex in edge]
            if len(endpoints) != len(set(endpoints)):
                ok = False
                break
        if ok:
            root_sets[sizes].add(assignment[0])
    return {sizes: frozenset(roots) for sizes, roots in root_sets.items()}


def local_marked_subset(marked: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    row = tuple(sorted(tuple(edge) for edge in marked))
    if any(not (0 <= left < 4 and 0 <= right < 4 and left != right) for left, right in row):
        raise ValueError("marked edge is not an off-diagonal 4x4 pair")
    if len(set(row)) != len(row):
        raise ValueError("duplicate marked edge")
    return row


def marked_weight14_census() -> dict[str, object]:
    root_sets = partition_root_sets()
    accepted: list[list[list[int]]] = []
    rejected: Counter[str] = Counter()
    for marked_tuple in combinations(tuple((i, j) for i in range(4) for j in range(4) if i != j), 5):
        marked = set(marked_tuple)
        plus_sizes = tuple(3 - sum(left == i for left, _ in marked) for i in range(4))
        minus_sizes = tuple(3 - sum(right == j for _, right in marked) for j in range(4))
        plus_roots = root_sets.get(plus_sizes, frozenset())
        minus_roots = root_sets.get(minus_sizes, frozenset())
        allowed_roots = [
            (left, right)
            for left in plus_roots
            for right in minus_roots
            if left != right and (left, right) not in marked
        ]
        if allowed_roots:
            accepted.append([list(edge) for edge in marked_tuple])
        elif not plus_roots:
            rejected["positive_partition"] += 1
        elif not minus_roots:
            rejected["negative_partition"] += 1
        elif not any(left != right for left in plus_roots for right in minus_roots):
            rejected["root_matched_q0"] += 1
        else:
            rejected["root_pair_already_intersected"] += 1
    if len(accepted) != 204 or sum(rejected.values()) != 588:
        raise AssertionError("marked weight-14 census differs")
    return {
        "total_labelled_subsets": comb(12, 5),
        "accepted_labelled_subsets": len(accepted),
        "accepted_subsets": accepted,
        "accepted_subsets_sha256": canonical_json_hash(accepted),
        "rejected_reason_counts": dict(sorted(rejected.items())),
        "partition_profiles_with_a_root": len(root_sets),
        "uses_automorphism_quotient": False,
        "scope": "rooted support-graph/selected-line partition compatibility only",
    }


def weight14_census() -> dict[str, object]:
    # If x is the cross-support edge count, then e(P)=e(N)=(21+x)/2.
    # Exact common-neighbor wedge capacity outside either side is
    # D=(21-7x)/2 - sum C(cross_degree,2).  Thus only x=1 or x=3
    # survive nonnegativity.  At x=3 equality forces a cross matching and
    # forces every same-sign internal edge into an internal triangle; internal
    # degrees (4,4,4,3,3,3,3) then contradict triangle-edge parity.
    rooted = rooted_graph_census()
    deficits = deficit_census()
    marked = marked_weight14_census()
    outside = (17, 61, 7)
    if sum(outside) != 85 or outside[1] + 2 * outside[2] != 75 or outside[2] != 7:
        raise AssertionError("weight-14 outside signature moments differ")
    return {
        "cross_edge_candidates_after_wedge_capacity": [1, 3],
        "x3_equality_case": {
            "cross_degree_sequence_each_side": [1, 1, 1, 0, 0, 0, 0],
            "same_sign_degree_sequence": [4, 4, 4, 3, 3, 3, 3],
            "outside_same_sign_pair_deficit": 0,
            "excluded_by_internal_triangle_degree_parity": True,
        },
        "forced_cross_edges": 1,
        "rooted_sign_graph": rooted,
        "outside_signature_z0_z1_z2": list(outside),
        "outside_k_at_most_2_reason": "the seven-edge same-sign deficit graph is triangle-free",
        "deficit_bijections": deficits,
        "marked_lines": marked,
    }


def memberships_for_selected(marked_full: Iterable[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    selected = tuple(sorted(tuple(sorted(edge)) for edge in marked_full))
    incidence = [0] * 8
    for left, right in selected:
        incidence[left] += 1
        incidence[right] += 1
    if any(value > 3 for value in incidence):
        raise ValueError("a selected triangle has too many intersections")
    memberships: list[tuple[int, ...]] = [tuple(edge) for edge in selected]
    for index, value in enumerate(incidence):
        memberships.extend([(index,)] * (3 - value))
    return tuple(memberships)


def pair_contribution(
    memberships: Sequence[tuple[int, ...]], left_vertex: int, right_vertex: int
) -> tuple[int, ...]:
    row = [0] * len(LINE_PAIRS)
    for left_line in memberships[left_vertex]:
        for right_line in memberships[right_vertex]:
            if left_line == right_line:
                continue
            row[PAIR_INDEX[tuple(sorted((left_line, right_line)))]] += 1
    return tuple(row)


def selected_union_model(marked_full: Iterable[tuple[int, int]]) -> dict[str, object]:
    selected = {tuple(sorted(edge)) for edge in marked_full}
    memberships = memberships_for_selected(selected)
    point_values = tuple(sum(SIGNS[line] for line in membership) for membership in memberships)
    fixed = {
        edge
        for edge in combinations(range(len(memberships)), 2)
        if set(memberships[edge[0]]) & set(memberships[edge[1]])
    }
    target = tuple(
        4 if pair in selected else CANONICAL_GRAM[pair[0]][pair[1]] for pair in LINE_PAIRS
    )
    used = [0] * len(LINE_PAIRS)
    for edge in fixed:
        for index, value in enumerate(pair_contribution(memberships, *edge)):
            used[index] += value
    residual = tuple(target[index] - used[index] for index in range(len(target)))
    if any(value < 0 for value in residual):
        raise AssertionError("fixed selected triangles already exceed R")
    candidates: list[dict[str, object]] = []
    for edge in combinations(range(len(memberships)), 2):
        if edge in fixed:
            continue
        contribution = pair_contribution(memberships, *edge)
        if not any(contribution):
            continue
        if any(contribution[index] > residual[index] for index in range(len(residual))):
            continue
        left, right = edge
        candidates.append(
            {
                "edge": edge,
                "contribution": contribution,
                "cross_support": point_values[left] * point_values[right] == -1,
            }
        )
    return {
        "memberships": memberships,
        "point_values": point_values,
        "fixed_edges": fixed,
        "residual": residual,
        "candidates": candidates,
    }


def protected_q1_pairs(marked_local: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    local = local_marked_subset(marked_local)
    full = tuple((left, right + 4) for left, right in local)
    model = selected_union_model(full)
    residual = model["residual"]
    candidates = model["candidates"]
    protected: list[tuple[int, int]] = []
    for pair in PRODUCT_PAIRS:
        index = PAIR_INDEX[pair]
        if pair in full:
            continue
        if residual[index] != 1:
            raise AssertionError("unintersected q=1 pair does not have residual one")
        accessible_without_cross_support = any(
            (not bool(candidate["cross_support"])) and candidate["contribution"][index]
            for candidate in candidates
        )
        if not accessible_without_cross_support:
            protected.append(pair)
    # Exact Farkas-style check: the sum of the protected R rows is at most
    # the cross-support-edge row, coefficient by coefficient.
    protected_indices = [PAIR_INDEX[pair] for pair in protected]
    for candidate in candidates:
        coefficient = sum(candidate["contribution"][index] for index in protected_indices)
        if coefficient > int(bool(candidate["cross_support"])):
            raise AssertionError("protected-row lower-bound certificate fails")
    return tuple(protected)


def marked_shape(marked: Sequence[tuple[int, int]]) -> str:
    (a, b), (c, d) = marked
    if a == c:
        return "share_positive_line"
    if b == d:
        return "share_negative_line"
    if a == d and c == b:
        return "swapped_disjoint"
    return "other_disjoint"


def marked_weight20_census() -> dict[str, object]:
    labelled = tuple((i, j) for i in range(4) for j in range(4) if i != j)
    rows = []
    lower_bound_distribution: Counter[tuple[str, int]] = Counter()
    for marked in combinations(labelled, 2):
        protected = protected_q1_pairs(marked)
        shape = marked_shape(marked)
        lower_bound_distribution[(shape, len(protected))] += 1
        rows.append(
            {
                "marked": [list(edge) for edge in marked],
                "shape": shape,
                "protected_q1_pairs": [list((left, right - 4)) for left, right in protected],
                "cross_edge_lower_bound": len(protected),
            }
        )
    x_survivors = {
        str(x): [row["marked"] for row in rows if row["cross_edge_lower_bound"] <= x]
        for x in (0, 2, 4, 6, 8)
    }
    if len(x_survivors["0"]) != 0 or len(x_survivors["2"]) != 6:
        raise AssertionError("x=0 exclusion or x=2 marked census differs")
    if any(marked_shape(tuple(tuple(edge) for edge in row)) != "swapped_disjoint" for row in x_survivors["2"]):
        raise AssertionError("an x=2 survivor is not swapped-disjoint")
    return {
        "total_labelled_m2_subsets": comb(12, 2),
        "protected_lower_bound_distribution": {
            f"{shape}:lower_{bound}": count
            for (shape, bound), count in sorted(lower_bound_distribution.items())
        },
        "x0_survivors": len(x_survivors["0"]),
        "x2_survivors": len(x_survivors["2"]),
        "x2_swapped_disjoint_cases": x_survivors["2"],
        "x4_survivors": len(x_survivors["4"]),
        "x6_survivors": len(x_survivors["6"]),
        "x8_survivors": len(x_survivors["8"]),
        "all_rows": rows,
        "all_rows_sha256": canonical_json_hash(rows),
        "uses_automorphism_quotient": False,
        "scope": "exact selected-line lower bound; a surviving marked case is not a graph",
    }


def degree_histograms(vertex_count: int, degree_sum: int, maximum_degree: int) -> tuple[tuple[int, ...], ...]:
    rows: list[tuple[int, ...]] = []

    def recurse(degree: int, remaining_vertices: int, remaining_sum: int, prefix: tuple[int, ...]) -> None:
        if degree == maximum_degree:
            if remaining_sum == degree * remaining_vertices:
                rows.append(prefix + (remaining_vertices,))
            return
        for count in range(remaining_vertices + 1):
            cost = degree * count
            if cost <= remaining_sum:
                recurse(
                    degree + 1,
                    remaining_vertices - count,
                    remaining_sum - cost,
                    prefix + (count,),
                )

    recurse(0, vertex_count, degree_sum, tuple())
    return tuple(rows)


def expanded_degrees(histogram: Sequence[int]) -> tuple[int, ...]:
    return tuple(sorted((degree for degree, count in enumerate(histogram) for _ in range(count)), reverse=True))


def gale_ryser(left_histogram: Sequence[int], right_histogram: Sequence[int]) -> bool:
    left = expanded_degrees(left_histogram)
    right = expanded_degrees(right_histogram)
    if sum(left) != sum(right):
        return False
    return all(
        sum(left[:size]) <= sum(min(size, degree) for degree in right)
        for size in range(1, len(left) + 1)
    )


def second_factorial_moment(histogram: Sequence[int]) -> int:
    return sum(comb(degree, 2) * count for degree, count in enumerate(histogram))


def outside_histograms(vertex_count: int, incidence: int, deficit: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate z_0,...,z_7 with exact first and second factorial moments."""

    rows: list[tuple[int, ...]] = []

    def recurse(
        degree: int,
        remaining_deficit: int,
        used_vertices: int,
        used_incidence: int,
        high_counts: tuple[int, ...],
    ) -> None:
        if degree == 8:
            if remaining_deficit:
                return
            z1 = incidence - used_incidence
            z0 = vertex_count - used_vertices - z1
            if z0 >= 0 and z1 >= 0:
                rows.append((z0, z1) + high_counts)
            return
        coefficient = comb(degree, 2)
        maximum = min(vertex_count - used_vertices, remaining_deficit // coefficient)
        for count in range(maximum + 1):
            recurse(
                degree + 1,
                remaining_deficit - coefficient * count,
                used_vertices + count,
                used_incidence + degree * count,
                high_counts + (count,),
            )

    if deficit >= 0:
        recurse(2, deficit, 0, 0, tuple())
    return tuple(rows)


def aggregate_row_valid(row: dict[str, object]) -> bool:
    x = int(row["x"])
    plus = tuple(int(value) for value in row["plus_cross_degree_histogram"])
    minus = tuple(int(value) for value in row["minus_cross_degree_histogram"])
    outside = tuple(int(value) for value in row["outside_balanced_degree_histogram"])
    if len(plus) != 6 or len(minus) != 6 or len(outside) != 8:
        return False
    if min(plus + minus + outside) < 0:
        return False
    if sum(plus) != 10 or sum(minus) != 10:
        return False
    if sum(index * count for index, count in enumerate(plus)) != x:
        return False
    if sum(index * count for index, count in enumerate(minus)) != x:
        return False
    if not gale_ryser(plus, minus):
        return False
    if sum(outside) != 79:
        return False
    if sum(index * count for index, count in enumerate(outside)) != 110 - 2 * x:
        return False
    collision = second_factorial_moment(plus) + second_factorial_moment(minus)
    expected_deficit = 45 - 7 * x // 2 - collision
    if sum(comb(index, 2) * count for index, count in enumerate(outside)) != expected_deficit:
        return False
    return True


def weight20_aggregate_rows() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for x in (2, 4, 6, 8):
        support_histograms = degree_histograms(10, x, 5)
        for plus in support_histograms:
            for minus in support_histograms:
                if not gale_ryser(plus, minus):
                    continue
                collision = second_factorial_moment(plus) + second_factorial_moment(minus)
                deficit = 45 - 7 * x // 2 - collision
                for outside in outside_histograms(79, 110 - 2 * x, deficit):
                    row = {
                        "x": x,
                        "plus_cross_degree_histogram": list(plus),
                        "minus_cross_degree_histogram": list(minus),
                        "outside_balanced_degree_histogram": list(outside),
                    }
                    if not aggregate_row_valid(row):
                        raise AssertionError("aggregate row failed direct replay")
                    rows.append(row)
    rows.sort(
        key=lambda row: (
            row["x"],
            row["plus_cross_degree_histogram"],
            row["minus_cross_degree_histogram"],
            row["outside_balanced_degree_histogram"],
        )
    )
    return tuple(rows)


def weight20_census() -> dict[str, object]:
    marked = marked_weight20_census()
    aggregate = weight20_aggregate_rows()
    distribution = Counter(int(row["x"]) for row in aggregate)
    if distribution != Counter({2: 109, 4: 157, 6: 76, 8: 10}):
        raise AssertionError("weight-20 aggregate distribution differs")
    # A zero-coordinate outside vertex has k neighbors of each sign.  At
    # x=10, 90 positive incidences among 79 outside vertices force at least
    # eleven same-sign pairs, while the exact wedge equation allows at most
    # ten even before support collisions.
    x10_minimum_outside_pairs = 90 - 79
    x10_maximum_outside_pairs = 45 - 7 * 10 // 2
    if x10_minimum_outside_pairs <= x10_maximum_outside_pairs:
        raise AssertionError("x=10 lower-bound contradiction disappeared")
    # The 352-row census is deliberately aggregate.  Combining the already
    # verified selected-line fact that each support point can meet at most the
    # three nonmatched opposite selected lines removes the degree-four rows.
    line_cap_rows = [
        row
        for row in aggregate
        if row["plus_cross_degree_histogram"][4] or row["plus_cross_degree_histogram"][5]
        or row["minus_cross_degree_histogram"][4] or row["minus_cross_degree_histogram"][5]
    ]
    if len(line_cap_rows) != 6:
        raise AssertionError("selected-line degree-cap delta differs")
    return {
        "initial_even_x_domain": [0, 2, 4, 6, 8, 10],
        "x0_excluded_by_selected_line_lower_bound": True,
        "x10_outside_pair_lower_bound": x10_minimum_outside_pairs,
        "x10_outside_pair_upper_bound": x10_maximum_outside_pairs,
        "x10_excluded": True,
        "marked_lines": marked,
        "aggregate_row_distribution": {str(key): distribution[key] for key in sorted(distribution)},
        "aggregate_rows_total": len(aggregate),
        "aggregate_rows": list(aggregate),
        "aggregate_rows_sha256": canonical_json_hash(aggregate),
        "aggregate_scope": "degree histograms, bipartite graphicality, and outside first/two-star moments; not selected-line coupling or a graph",
        "post_aggregate_selected_line_degree_cap": {
            "claim_label": "DERIVED",
            "maximum_cross_degree": 3,
            "rows_removed_from_aggregate_table": len(line_cap_rows),
            "remaining_rows": len(aggregate) - len(line_cap_rows),
            "removed_rows_sha256": canonical_json_hash(line_cap_rows),
            "requires_independent_promotion": True,
        },
    }


LINE_TYPES = tuple((positive, negative) for positive in range(4) for negative in range(4 - positive))


def selected_line_minima(marked_local: Iterable[tuple[int, int]]) -> Counter[tuple[int, int]]:
    marked = set(local_marked_subset(marked_local))
    minima: Counter[tuple[int, int]] = Counter()
    for positive_line in range(4):
        minima[(3 - sum(left == positive_line for left, _ in marked), 0)] += 1
    for negative_line in range(4):
        minima[(0, 3 - sum(right == negative_line for _, right in marked))] += 1
    return minima


def line_type_tables(side_size: int, x: int, marked_local: Iterable[tuple[int, int]]) -> tuple[dict[tuple[int, int], int], ...]:
    minima = selected_line_minima(marked_local)
    edge_count_twice = 3 * side_size + x
    if edge_count_twice % 2:
        return tuple()
    same_edges = edge_count_twice // 2
    rows: list[dict[tuple[int, int], int]] = []
    for n21 in range(x // 2 + 1):
        for n12 in range(x // 2 - n21 + 1):
            n11 = x - 2 * n21 - 2 * n12
            for n30 in range(same_edges // 3 + 1):
                n20 = same_edges - n21 - 3 * n30
                if n20 < 0:
                    continue
                for n03 in range(same_edges // 3 + 1):
                    n02 = same_edges - n12 - 3 * n03
                    if n02 < 0:
                        continue
                    n10 = 7 * side_size - (2 * n20 + n11 + 3 * n30 + 2 * n21 + n12)
                    n01 = 7 * side_size - (2 * n02 + n11 + 3 * n03 + n21 + 2 * n12)
                    counts = {line_type: 0 for line_type in LINE_TYPES}
                    counts.update(
                        {
                            (1, 0): n10,
                            (0, 1): n01,
                            (2, 0): n20,
                            (0, 2): n02,
                            (1, 1): n11,
                            (3, 0): n30,
                            (0, 3): n03,
                            (2, 1): n21,
                            (1, 2): n12,
                        }
                    )
                    counts[(0, 0)] = 231 - sum(value for key, value in counts.items() if key != (0, 0))
                    if min(counts.values()) < 0:
                        continue
                    if any(counts[line_type] < minimum for line_type, minimum in minima.items()):
                        continue
                    if not line_type_table_valid(counts, side_size, x):
                        raise AssertionError("constructed line table failed replay")
                    rows.append(counts)
    rows.sort(key=lambda row: tuple(row[line_type] for line_type in LINE_TYPES))
    return tuple(rows)


def line_type_table_valid(counts: dict[tuple[int, int], int], side_size: int, x: int) -> bool:
    if set(counts) != set(LINE_TYPES) or min(counts.values()) < 0:
        return False
    if sum(counts.values()) != 231:
        return False
    if sum(positive * counts[(positive, negative)] for positive, negative in LINE_TYPES) != 7 * side_size:
        return False
    if sum(negative * counts[(positive, negative)] for positive, negative in LINE_TYPES) != 7 * side_size:
        return False
    same = (3 * side_size + x) // 2
    if sum(comb(positive, 2) * counts[(positive, negative)] for positive, negative in LINE_TYPES) != same:
        return False
    if sum(comb(negative, 2) * counts[(positive, negative)] for positive, negative in LINE_TYPES) != same:
        return False
    if sum(positive * negative * counts[(positive, negative)] for positive, negative in LINE_TYPES) != x:
        return False
    histogram = line_sum_histogram(counts)
    weight = 2 * side_size
    if sum(histogram.values()) != 231:
        return False
    if sum(value * count for value, count in histogram.items()) != 0:
        return False
    if sum(value * value * count for value, count in histogram.items()) != 10 * weight:
        return False
    return True


def line_sum_histogram(counts: dict[tuple[int, int], int]) -> dict[int, int]:
    histogram: Counter[int] = Counter()
    for (positive, negative), count in counts.items():
        histogram[positive - negative] += count
    return {value: histogram[value] for value in range(-3, 4)}


def serialize_line_table(counts: dict[tuple[int, int], int]) -> dict[str, int]:
    return {f"p{positive}_n{negative}": counts[(positive, negative)] for positive, negative in LINE_TYPES}


def line_moment_census(weight14: dict[str, object], weight20: dict[str, object]) -> dict[str, object]:
    accepted14 = weight14["marked_lines"]["accepted_subsets"]
    witnesses14 = []
    for marked_lists in accepted14:
        marked = tuple(tuple(edge) for edge in marked_lists)
        tables = line_type_tables(7, 1, marked)
        if not tables:
            raise AssertionError("an accepted weight-14 marked set has no line-moment witness")
        witnesses14.append(tables[0])

    marked20 = weight20["marked_lines"]
    rows20 = marked20["all_rows"]
    checked20 = 0
    example20: dict[str, object] = {}
    for x in (2, 4, 6, 8):
        for row in rows20:
            if row["cross_edge_lower_bound"] > x:
                continue
            marked = tuple(tuple(edge) for edge in row["marked"])
            tables = line_type_tables(10, x, marked)
            if not tables:
                raise AssertionError("a retained weight-20 marked/x pair has no line-moment witness")
            checked20 += 1
            example20.setdefault(
                str(x),
                {
                    "marked": row["marked"],
                    "line_types": serialize_line_table(tables[0]),
                    "line_sum_histogram": {str(key): value for key, value in line_sum_histogram(tables[0]).items()},
                },
            )
    example14 = witnesses14[0]
    return {
        "identity": {
            "line_vector": "d=B^T*c",
            "sum_d": 0,
            "sum_d_squared": "10*weight",
            "source": "BB^T=A+7I and Ac=3c",
        },
        "weight14_accepted_marked_sets_checked": len(witnesses14),
        "weight14_all_feasible": True,
        "weight14_example": {
            "marked": accepted14[0],
            "line_types": serialize_line_table(example14),
            "line_sum_histogram": {str(key): value for key, value in line_sum_histogram(example14).items()},
        },
        "weight20_marked_x_pairs_checked": checked20,
        "weight20_all_retained_pairs_feasible": True,
        "weight20_examples": example20,
        "scope": "necessary line-composition/moment tables only; no 231-column incidence realization",
    }


def build_result() -> dict[str, object]:
    rank3 = r3k_census()
    weight14 = weight14_census()
    weight20 = weight20_census()
    moments = line_moment_census(weight14, weight20)
    return {
        "schema_version": 1,
        "source_code_imported": False,
        "claim_scope": "conditional rank-three (2,2,2) marked M7g trade under a hypothetical srg(99,14,1,2) endpoint",
        "r_minus_3k": rank3,
        "weight14_m5": weight14,
        "weight20_m2": weight20,
        "line_vector_moments": moments,
        "scope_walls": {
            "conditional_on_hypothetical_endpoint": True,
            "aggregate_rows_are_graphs": False,
            "rooted_support_graph_is_completion": False,
            "deficit_bijection_is_completion": False,
            "marked_subset_is_completion": False,
            "line_histogram_is_incidence_realization": False,
            "rank_four_branches_excluded": False,
            "full_99_vertex_adjacency_supplied": False,
            "complete_nonexistence_certificate": False,
            "outside_row_hostile_witness": "add a zero-coordinate vertex adjacent to one positive support point: internal signed equations are unchanged but the new outside row has dot(c)=1",
            "conway_99_status": "UNKNOWN",
            "rank11_endpoint_status": "UNKNOWN",
            "n3_4158_endpoint_status": "UNKNOWN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.write:
        ARCHIVE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"WROTE {ARCHIVE}")
    elif args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("independent exact-results archive differs")
        print("PASS: independent Wave 209 rank-three reconstruction")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
