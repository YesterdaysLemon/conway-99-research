#!/usr/bin/env python3
"""SAT scout for the surviving all-``q=2`` Wave 13 active frontier.

The encoded object has fifteen active labels, an 8-regular graph ``K``, and
a linear point hypergraph with point sizes two or three.  Every label occurs
in exactly three points.  The common-point/Berge-triangle rule and every
meeting-point crossing rule are encoded exactly.  A size-three point is also
forbidden from receiving more than twelve units from its overlapping
size-three co-points.

This is intentionally not a completed ``srg(99,14,1,2)`` encoding.  In
particular it does not require the remaining fixed-point support, inactive
vertices, or every global lambda/mu equality.  A SAT output is therefore a
machine-readable weakened survivor.  An UNSAT solver return is recorded only
as ``UNSAT_UNVERIFIED`` because this discovery script does not emit a checked
proof trace.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import pysat
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


ORDER = 15
K_DEGREE = 8
ROOT_POINT = frozenset((0, 1, 2))
ALLOWED_SIZE3_COUNTS = tuple(range(1, 12, 2))
ROOT_MODES = ("111", "122", "222", "223")
SCOUT_VARIANTS = (
    "full",
    "no_overlap_cap",
    "no_common_point",
    "k_degree_at_most",
)
SCAN_BRANCHES = (
    (1, "111"),
    (3, "111"),
    (3, "122"),
    (5, "111"),
    (5, "122"),
    (5, "222"),
    (5, "223"),
    (7, "111"),
    (7, "122"),
    (7, "222"),
    (7, "223"),
    (9, "111"),
    (9, "122"),
    (9, "222"),
    (9, "223"),
    (11, "222"),
    (11, "223"),
)


def edge(left: int, right: int) -> tuple[int, int]:
    if left == right:
        raise ValueError("loops are not graph edges")
    return (left, right) if left < right else (right, left)


def all_edges() -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(ORDER), 2))


def all_points() -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(value)
        for size in (2, 3)
        for value in itertools.combinations(range(ORDER), size)
    )


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def cnf_sha256(cnf: CNF, variable_count: int) -> str:
    """Hash the exact deterministic DIMACS clause stream without writing it."""

    digest = hashlib.sha256()
    digest.update(
        f"p cnf {variable_count} {len(cnf.clauses)}\n".encode("ascii")
    )
    for clause in cnf.clauses:
        digest.update(" ".join(map(str, clause)).encode("ascii"))
        digest.update(b" 0\n")
    return digest.hexdigest()


def add_equals(
    cnf: CNF,
    pool: IDPool,
    literals: Iterable[int],
    bound: int,
) -> None:
    encoded = CardEnc.equals(
        lits=list(literals),
        bound=bound,
        vpool=pool,
        encoding=EncType.seqcounter,
    )
    cnf.extend(encoded.clauses)


def add_at_most(
    cnf: CNF,
    pool: IDPool,
    literals: Iterable[int],
    bound: int,
) -> None:
    values = list(literals)
    if len(values) <= bound:
        return
    encoded = CardEnc.atmost(
        lits=values,
        bound=bound,
        vpool=pool,
        encoding=EncType.seqcounter,
    )
    cnf.extend(encoded.clauses)


def build_instance(
    size3_count: int,
    root_mode: str,
    variant: str = "full",
) -> tuple[
    CNF,
    IDPool,
    tuple[frozenset[int], ...],
    dict[frozenset[int], int],
    dict[tuple[int, int], int],
    dict[tuple[int, int], int],
    dict[tuple[frozenset[int], frozenset[int]], int],
]:
    if size3_count not in ALLOWED_SIZE3_COUNTS:
        raise ValueError(f"size3_count must lie in {ALLOWED_SIZE3_COUNTS}")
    if root_mode not in ROOT_MODES:
        raise ValueError(f"root_mode must lie in {ROOT_MODES}")
    if variant not in SCOUT_VARIANTS:
        raise ValueError(f"variant must lie in {SCOUT_VARIANTS}")
    minimum_points = {"111": 1, "122": 3, "222": 4, "223": 5}
    if size3_count < minimum_points[root_mode]:
        raise ValueError(
            f"root mode {root_mode} needs at least "
            f"{minimum_points[root_mode]} size-three points"
        )

    points = all_points()
    edges = all_edges()
    pool = IDPool()
    selected = {
        point: pool.id(("point", tuple(sorted(point)))) for point in points
    }
    k_edge = {item: pool.id(("K", item)) for item in edges}
    f_edge = {item: pool.id(("F", item)) for item in edges}
    full_overlap: dict[
        tuple[frozenset[int], frozenset[int]], int
    ] = {}
    cnf = CNF()

    # Every active label belongs to exactly three original point sets.
    for vertex in range(ORDER):
        add_equals(
            cnf,
            pool,
            (selected[point] for point in points if vertex in point),
            3,
        )
    add_equals(
        cnf,
        pool,
        (selected[point] for point in points if len(point) == 3),
        size3_count,
    )

    # Every feasible order-fifteen system has at least one size-three point
    # because its total incidence count is odd.  The full S_15 label action
    # therefore allows one selected size-three point to be named {0,1,2}.
    # This is search-label normalization, not a completed-graph automorphism.
    cnf.append([selected[ROOT_POINT]])
    if size3_count == 1:
        for point in points:
            if len(point) == 3 and point != ROOT_POINT:
                cnf.append([-selected[point]])
        # The setwise stabilizer S_3 x S_12 of ROOT_POINT can name the two
        # size-two mates at its three labels in three consecutive pairs.
        # A non-root label cannot be reused across two root labels, since
        # that would create a forbidden primal triangle with an edge of the
        # selected root point.
        normalized_root_mates = (
            (0, 3),
            (0, 4),
            (1, 5),
            (1, 6),
            (2, 7),
            (2, 8),
        )
        for item in normalized_root_mates:
            cnf.append([selected[frozenset(item)]])

    # Cover the four exact local modes of the named root point.  The setwise
    # stabilizer of {0,1,2}, followed by relabeling outside that set, gives
    # the displayed representatives.  For mode 223 the two co-points at the
    # degree-three root occurrence are distinguished by whether their
    # crossing with ROOT_POINT is empty or full in L.
    root_mode_data: dict[
        str, tuple[tuple[tuple[int, int, int], str], ...]
    ] = {
        "111": (),
        "122": (
            ((1, 3, 4), "full_L"),
            ((2, 5, 6), "full_L"),
        ),
        "222": (
            ((0, 3, 4), "full_L"),
            ((1, 5, 6), "full_L"),
            ((2, 7, 8), "full_L"),
        ),
        "223": (
            ((0, 3, 4), "empty_L"),
            ((0, 5, 6), "full_L"),
            ((1, 7, 8), "full_L"),
            ((2, 9, 10), "full_L"),
        ),
    }
    root_co_points = {
        frozenset(point): crossing
        for point, crossing in root_mode_data[root_mode]
    }
    for point in root_co_points:
        cnf.append([selected[point]])
    for point in points:
        if (
            len(point) == 3
            and point != ROOT_POINT
            and point & ROOT_POINT
            and point not in root_co_points
        ):
            cnf.append([-selected[point]])
    for point, crossing in root_co_points.items():
        common = next(iter(point & ROOT_POINT))
        cross_edges = [
            edge(first, second)
            for first in point - {common}
            for second in ROOT_POINT - {common}
        ]
        for item in cross_edges:
            cnf.append(
                [k_edge[item] if crossing == "empty_L" else -k_edge[item]]
            )
    if root_mode == "111" and size3_count > 1:
        # Every other size-three point is disjoint from ROOT_POINT.  One of
        # them may therefore be named {3,4,5}.
        cnf.append([selected[frozenset((3, 4, 5))]])

    # F is the union of point-clique edges.  Linearity is an at-most-one
    # owner constraint for each active-label pair.
    for item in edges:
        owners = [
            selected[point] for point in points if set(item) <= point
        ]
        add_at_most(cnf, pool, owners, 1)
        for owner in owners:
            cnf.append([-owner, f_edge[item]])
        cnf.append([-f_edge[item], *owners])

    # Every selected point is a clique in K.
    for point in points:
        for item in itertools.combinations(sorted(point), 2):
            cnf.append([-selected[point], k_edge[item]])

    # In a linear point hypergraph, the common-point rule says that any
    # triangle of the primal F graph must be owned by its size-three point.
    if variant != "no_common_point":
        for triple in itertools.combinations(range(ORDER), 3):
            ab, ac, bc = itertools.combinations(triple, 2)
            triple_point = frozenset(triple)
            cnf.append(
                [
                    -f_edge[ab],
                    -f_edge[ac],
                    -f_edge[bc],
                    selected[triple_point],
                ]
            )

    size3_points = tuple(point for point in points if len(point) == 3)
    overlap_by_point: dict[frozenset[int], list[int]] = {
        point: [] for point in size3_points
    }

    interaction_points = (
        tuple(
            point
            for point in points
            if len(point) == 2 or point == ROOT_POINT
        )
        if size3_count == 1
        else points
    )

    # Meeting point sets are actual neighboring original vertices.  After
    # deleting their common active triangle, every L-crossing degree is zero
    # or two.  Thus a singleton-side crossing is empty, while a 2-by-2
    # crossing is empty or complete.
    for left_index, left in enumerate(interaction_points):
        for right in interaction_points[left_index + 1 :]:
            intersection = left & right
            if len(intersection) != 1:
                continue
            common = next(iter(intersection))
            left_external = sorted(left - {common})
            right_external = sorted(right - {common})
            crossing = [
                k_edge[edge(first, second)]
                for first in left_external
                for second in right_external
            ]
            if len(left_external) == 1 or len(right_external) == 1:
                for literal in crossing:
                    cnf.append(
                        [-selected[left], -selected[right], literal]
                    )
                continue

            first = crossing[0]
            for literal in crossing[1:]:
                cnf.append(
                    [
                        -selected[left],
                        -selected[right],
                        -first,
                        literal,
                    ]
                )
                cnf.append(
                    [
                        -selected[left],
                        -selected[right],
                        first,
                        -literal,
                    ]
                )

            # With at most three selected size-three points, no one point can
            # have four full overlaps, so the fixed-point upper bound is
            # automatic and these auxiliaries are unnecessary.  Larger
            # branches receive the exact reified cap below.
            if size3_count >= 5 and variant != "no_overlap_cap":
                # w <-> selected(left) & selected(right) & not K(first).
                key = (left, right)
                witness = pool.id(
                    (
                        "full_L_overlap",
                        tuple(sorted(left)),
                        tuple(sorted(right)),
                    )
                )
                full_overlap[key] = witness
                overlap_by_point[left].append(witness)
                overlap_by_point[right].append(witness)
                cnf.append([-witness, selected[left]])
                cnf.append([-witness, selected[right]])
                cnf.append([-witness, -first])
                cnf.append(
                    [
                        -selected[left],
                        -selected[right],
                        first,
                        witness,
                    ]
                )

    # Each full 2-by-2 overlap contributes four to a size-three point's
    # fixed-point total of twelve.
    if size3_count >= 5 and variant != "no_overlap_cap":
        for point in size3_points:
            add_at_most(cnf, pool, overlap_by_point[point], 3)

    # K is exactly 8-regular in the full model.  The named scout mutation
    # keeps only the necessary upper bound to test whether regular completion
    # is doing hidden work.
    for vertex in range(ORDER):
        literals = [
            k_edge[edge(vertex, other)]
            for other in range(ORDER)
            if other != vertex
        ]
        if variant == "k_degree_at_most":
            add_at_most(cnf, pool, literals, K_DEGREE)
        else:
            add_equals(cnf, pool, literals, K_DEGREE)

    return (
        cnf,
        pool,
        points,
        selected,
        k_edge,
        f_edge,
        full_overlap,
    )


def vertex_degrees(
    graph_edges: Iterable[tuple[int, int]],
) -> tuple[int, ...]:
    values = [0] * ORDER
    for left, right in graph_edges:
        values[left] += 1
        values[right] += 1
    return tuple(values)


def validate_candidate(candidate: dict[str, object]) -> dict[str, object]:
    if candidate.get("schema") != "conway99-wave13-n3-45-active-local-v1":
        raise AssertionError("candidate schema mismatch")
    if candidate.get("claim_label") != "CANDIDATE":
        raise AssertionError("candidate status inflation")
    if candidate.get("target_result") != "UNKNOWN":
        raise AssertionError("target status inflation")
    if candidate.get("active_order") != ORDER:
        raise AssertionError("wrong active order")
    if candidate.get("q_values") != [2] * ORDER:
        raise AssertionError("candidate is not the all-q=2 frontier")
    size3_count = int(candidate.get("size3_point_count", -1))
    if size3_count not in ALLOWED_SIZE3_COUNTS:
        raise AssertionError("invalid size-three count")
    root_mode = candidate.get("root_mode")
    if root_mode not in ROOT_MODES:
        raise AssertionError("invalid rooted local mode")

    raw_points = candidate.get("point_sets")
    if not isinstance(raw_points, list):
        raise AssertionError("point_sets must be a list")
    points = tuple(frozenset(map(int, item)) for item in raw_points)
    if len(points) != len(set(points)):
        raise AssertionError("duplicate point set")
    if any(
        len(point) not in (2, 3)
        or not point <= frozenset(range(ORDER))
        for point in points
    ):
        raise AssertionError("invalid point set")
    if ROOT_POINT not in points:
        raise AssertionError("root normalization is absent")
    if sum(len(point) == 3 for point in points) != size3_count:
        raise AssertionError("size-three count mismatch")
    incidence = Counter(vertex for point in points for vertex in point)
    if tuple(incidence[vertex] for vertex in range(ORDER)) != (3,) * ORDER:
        raise AssertionError("point incidence is not three at every label")

    pair_owner: dict[tuple[int, int], frozenset[int]] = {}
    for point in points:
        for item in itertools.combinations(sorted(point), 2):
            if item in pair_owner:
                raise AssertionError("point hypergraph is not linear")
            pair_owner[item] = point
    for triple in itertools.combinations(range(ORDER), 3):
        pair_items = tuple(itertools.combinations(triple, 2))
        if all(item in pair_owner for item in pair_items):
            if frozenset(triple) not in points:
                raise AssertionError("forbidden common-point Berge triangle")

    raw_k = candidate.get("K_edges")
    if not isinstance(raw_k, list):
        raise AssertionError("K_edges must be a list")
    k_edges = frozenset(edge(*map(int, item)) for item in raw_k)
    if len(k_edges) != len(raw_k):
        raise AssertionError("duplicate K edge")
    if vertex_degrees(k_edges) != (K_DEGREE,) * ORDER:
        raise AssertionError("K is not 8-regular")
    if not set(pair_owner) <= k_edges:
        raise AssertionError("a point is not a clique in K")

    crossing_count = 0
    full_overlaps: list[tuple[int, int]] = []
    overlap_degree = [0] * len(points)
    for left_index, left in enumerate(points):
        for right_index in range(left_index + 1, len(points)):
            right = points[right_index]
            intersection = left & right
            if len(intersection) != 1:
                continue
            crossing_count += 1
            common = next(iter(intersection))
            left_external = sorted(left - {common})
            right_external = sorted(right - {common})
            l_matrix = [
                [
                    edge(first, second) not in k_edges
                    for second in right_external
                ]
                for first in left_external
            ]
            row_degrees = [sum(row) for row in l_matrix]
            column_degrees = [
                sum(l_matrix[row][column] for row in range(len(l_matrix)))
                for column in range(len(right_external))
            ]
            if any(
                value not in (0, 2)
                for value in (*row_degrees, *column_degrees)
            ):
                raise AssertionError("meeting crossing degree is not zero or two")
            if len(left) == len(right) == 3 and sum(row_degrees) == 4:
                full_overlaps.append((left_index, right_index))
                overlap_degree[left_index] += 1
                overlap_degree[right_index] += 1

    if any(
        overlap_degree[index] > 3
        for index, point in enumerate(points)
        if len(point) == 3
    ):
        raise AssertionError("size-three overlap contribution exceeds twelve")

    t_values = tuple(
        sum(len(point) == 3 and vertex in point for point in points)
        for vertex in range(ORDER)
    )
    local_types = Counter(
        tuple(sorted(t_values[vertex] for vertex in point))
        for point in points
        if len(point) == 3
    )
    allowed_types = {(1, 1, 1), (1, 2, 2), (2, 2, 2), (2, 2, 3)}
    if not set(local_types) <= allowed_types:
        raise AssertionError("candidate has a forbidden local t-profile")
    observed_root_mode = "".join(
        map(str, sorted(t_values[vertex] for vertex in ROOT_POINT))
    )
    if observed_root_mode != root_mode:
        raise AssertionError("rooted local mode mismatch")

    restrictions = candidate.get("restrictions")
    expected_restrictions = [
        "active_labels_only",
        "point_sizes_restricted_to_2_or_3_after_local_proof",
        "one_size3_point_fixed_by_full_label_relabeling",
        "one_of_four_root_modes_fixed_by_its_label_stabilizer",
        "meeting_crossings_and_overlap_fixed_point_upper_bound_only",
        "remaining_fixed_point_support_not_encoded",
        "inactive_vertices_not_encoded",
        "no_complete_99_vertex_adjacency_matrix",
        "no_global_lambda_mu_equalities",
    ]
    if restrictions != expected_restrictions:
        raise AssertionError("candidate restriction boundary changed")

    semantic = {
        "active_order": ORDER,
        "q_values": [2] * ORDER,
        "point_sets": [sorted(point) for point in points],
        "K_edges": [list(item) for item in sorted(k_edges)],
        "full_L_overlaps": [list(item) for item in full_overlaps],
    }
    return {
        "status": "PASS weakened n3=45 active-local SAT candidate",
        "point_count": len(points),
        "size2_point_count": sum(len(point) == 2 for point in points),
        "size3_point_count": size3_count,
        "K_edge_count": len(k_edges),
        "meeting_crossings_checked": crossing_count,
        "full_L_overlap_count": len(full_overlaps),
        "t_degree_histogram": {
            str(key): value for key, value in sorted(Counter(t_values).items())
        },
        "size3_local_type_histogram": {
            "".join(map(str, key)): value
            for key, value in sorted(local_types.items())
        },
        "semantic_sha256": sha256_bytes(canonical_json_bytes(semantic)),
        "claim_label": "CANDIDATE",
        "target_result": "UNKNOWN",
    }


def weakened_assignment_diagnostics(
    points: Sequence[frozenset[int]],
    k_edges: frozenset[tuple[int, int]],
) -> dict[str, object]:
    """Measure every full-model premise on a deliberately weakened model."""

    incidence = Counter(vertex for point in points for vertex in point)
    owners: dict[tuple[int, int], list[int]] = {
        item: [] for item in all_edges()
    }
    missing_point_clique_edges = 0
    for point_index, point in enumerate(points):
        for item in itertools.combinations(sorted(point), 2):
            owners[item].append(point_index)
            if item not in k_edges:
                missing_point_clique_edges += 1

    berge_triangles = []
    point_set = set(points)
    for triple in itertools.combinations(range(ORDER), 3):
        pair_items = tuple(itertools.combinations(triple, 2))
        if all(owners[item] for item in pair_items):
            if frozenset(triple) not in point_set:
                berge_triangles.append(list(triple))

    crossing_violations = 0
    full_overlap_degree = [0] * len(points)
    full_overlaps = []
    for left_index, left in enumerate(points):
        for right_index in range(left_index + 1, len(points)):
            right = points[right_index]
            intersection = left & right
            if len(intersection) != 1:
                continue
            common = next(iter(intersection))
            left_external = sorted(left - {common})
            right_external = sorted(right - {common})
            l_matrix = [
                [
                    edge(first, second) not in k_edges
                    for second in right_external
                ]
                for first in left_external
            ]
            row_degrees = [sum(row) for row in l_matrix]
            column_degrees = [
                sum(l_matrix[row][column] for row in range(len(l_matrix)))
                for column in range(len(right_external))
            ]
            if any(
                value not in (0, 2)
                for value in (*row_degrees, *column_degrees)
            ):
                crossing_violations += 1
            if len(left) == len(right) == 3 and sum(row_degrees) == 4:
                full_overlaps.append((left_index, right_index))
                full_overlap_degree[left_index] += 1
                full_overlap_degree[right_index] += 1

    size3_overlap_degrees = [
        full_overlap_degree[index]
        for index, point in enumerate(points)
        if len(point) == 3
    ]
    t_values = tuple(
        sum(len(point) == 3 and vertex in point for point in points)
        for vertex in range(ORDER)
    )
    local_types = Counter(
        tuple(sorted(t_values[vertex] for vertex in point))
        for point in points
        if len(point) == 3
    )
    return {
        "point_count": len(points),
        "size2_point_count": sum(len(point) == 2 for point in points),
        "size3_point_count": sum(len(point) == 3 for point in points),
        "incidence_degrees": [incidence[vertex] for vertex in range(ORDER)],
        "linear_pair_owner_violations": sum(
            len(indices) > 1 for indices in owners.values()
        ),
        "missing_point_clique_edges": missing_point_clique_edges,
        "K_degree_sequence": list(vertex_degrees(k_edges)),
        "common_point_Berge_triangle_count": len(berge_triangles),
        "first_common_point_Berge_triangles": berge_triangles[:10],
        "meeting_crossing_violations": crossing_violations,
        "full_L_overlap_count": len(full_overlaps),
        "maximum_size3_full_L_overlap_degree": max(
            size3_overlap_degrees, default=0
        ),
        "size3_points_over_fixed_point_cap": sum(
            value > 3 for value in size3_overlap_degrees
        ),
        "t_degree_histogram": {
            str(key): value for key, value in sorted(Counter(t_values).items())
        },
        "size3_local_type_histogram": {
            "".join(map(str, key)): value
            for key, value in sorted(local_types.items())
        },
    }


def validate_weakened_candidate(
    candidate: dict[str, object],
) -> dict[str, object]:
    if (
        candidate.get("schema")
        != "conway99-wave13-n3-45-active-local-diagnostic-v1"
    ):
        raise AssertionError("diagnostic schema mismatch")
    if candidate.get("claim_label") != "CANDIDATE":
        raise AssertionError("diagnostic status inflation")
    if candidate.get("target_result") != "UNKNOWN":
        raise AssertionError("diagnostic target inflation")
    variant = candidate.get("variant")
    if variant not in {
        "no_overlap_cap",
        "no_common_point",
        "k_degree_at_most",
    }:
        raise AssertionError("diagnostic variant mismatch")
    points = tuple(
        frozenset(map(int, item)) for item in candidate.get("point_sets", ())
    )
    k_edges = frozenset(
        edge(*map(int, item)) for item in candidate.get("K_edges", ())
    )
    observed = weakened_assignment_diagnostics(points, k_edges)
    if observed != candidate.get("diagnostics"):
        raise AssertionError("diagnostic recomputation mismatch")
    if observed["incidence_degrees"] != [3] * ORDER:
        raise AssertionError("diagnostic lost exact point incidence")
    if observed["linear_pair_owner_violations"]:
        raise AssertionError("diagnostic lost linearity")
    if observed["missing_point_clique_edges"]:
        raise AssertionError("diagnostic lost the point-clique premise")
    if variant == "k_degree_at_most":
        if max(observed["K_degree_sequence"], default=0) > K_DEGREE:
            raise AssertionError("upper-bound diagnostic exceeds K-degree eight")
    elif observed["K_degree_sequence"] != [K_DEGREE] * ORDER:
        raise AssertionError("diagnostic K is not 8-regular")
    if observed["meeting_crossing_violations"]:
        raise AssertionError("diagnostic lost the meeting-crossing premise")
    if variant == "no_common_point":
        if observed["common_point_Berge_triangle_count"] == 0:
            raise AssertionError("no-common-point diagnostic does not violate it")
        if observed["size3_points_over_fixed_point_cap"]:
            raise AssertionError("no-common-point diagnostic also violates overlap cap")
    if variant == "no_overlap_cap":
        if observed["common_point_Berge_triangle_count"]:
            raise AssertionError("no-overlap diagnostic violates common-point premise")
        if observed["size3_points_over_fixed_point_cap"] == 0:
            raise AssertionError("no-overlap diagnostic does not violate its omission")
    if variant == "k_degree_at_most":
        if observed["common_point_Berge_triangle_count"]:
            raise AssertionError("K-upper-bound diagnostic violates common point")
        if observed["size3_points_over_fixed_point_cap"]:
            raise AssertionError("K-upper-bound diagnostic violates overlap cap")
        if observed["K_degree_sequence"] == [K_DEGREE] * ORDER:
            raise AssertionError("K-upper-bound diagnostic is already regular")
    semantic = {
        "variant": variant,
        "point_sets": [sorted(point) for point in points],
        "K_edges": [list(item) for item in sorted(k_edges)],
        "diagnostics": observed,
    }
    semantic_sha256 = sha256_bytes(canonical_json_bytes(semantic))
    if semantic_sha256 != candidate.get("semantic_sha256"):
        raise AssertionError("diagnostic semantic digest mismatch")
    return {
        "status": "PASS weakened active-local diagnostic",
        "variant": variant,
        "semantic_sha256": semantic_sha256,
        "omitted_premise_violation_count": (
            observed["common_point_Berge_triangle_count"]
            if variant == "no_common_point"
            else observed["size3_points_over_fixed_point_cap"]
            if variant == "no_overlap_cap"
            else sum(
                K_DEGREE - value
                for value in observed["K_degree_sequence"]
            )
        ),
        "claim_label": "CANDIDATE",
        "target_result": "UNKNOWN",
    }


def candidate_from_model(
    *,
    size3_count: int,
    root_mode: str,
    variant: str,
    points: Sequence[frozenset[int]],
    selected: dict[frozenset[int], int],
    k_edge: dict[tuple[int, int], int],
    model: Sequence[int],
    solver_statistics: dict[str, object],
) -> dict[str, object]:
    positive = {literal for literal in model if literal > 0}
    chosen_points = tuple(
        point for point in points if selected[point] in positive
    )
    chosen_k = tuple(
        item for item, variable in k_edge.items() if variable in positive
    )
    candidate = {
        "schema": (
            "conway99-wave13-n3-45-active-local-v1"
            if variant == "full"
            else "conway99-wave13-n3-45-active-local-diagnostic-v1"
        ),
        "claim_label": "CANDIDATE",
        "target_result": "UNKNOWN",
        "variant": variant,
        "active_order": ORDER,
        "q_values": [2] * ORDER,
        "K_degree": K_DEGREE,
        "size3_point_count": size3_count,
        "root_mode": root_mode,
        "point_sets": [sorted(point) for point in chosen_points],
        "K_edges": [list(item) for item in chosen_k],
        "root_normalization": {
            "point": sorted(ROOT_POINT),
            "local_mode": root_mode,
            "justification": (
                "odd total incidence forces a size-three point; the full "
                "S_15 active-label action names it {0,1,2}, and its setwise "
                "stabilizer gives the recorded rooted-mode representative"
            ),
            "completed_graph_automorphism_assumed": False,
        },
        "restrictions": [
            "active_labels_only",
            "point_sizes_restricted_to_2_or_3_after_local_proof",
            "one_size3_point_fixed_by_full_label_relabeling",
            "one_of_four_root_modes_fixed_by_its_label_stabilizer",
            "meeting_crossings_and_overlap_fixed_point_upper_bound_only",
            "remaining_fixed_point_support_not_encoded",
            "inactive_vertices_not_encoded",
            "no_complete_99_vertex_adjacency_matrix",
            "no_global_lambda_mu_equalities",
        ],
        "solver_statistics": solver_statistics,
    }
    if variant != "full":
        candidate["restrictions"].append(f"diagnostic_variant_{variant}")
    if variant == "full":
        candidate["validation"] = validate_candidate(candidate)
    else:
        candidate["diagnostics"] = weakened_assignment_diagnostics(
            chosen_points, frozenset(chosen_k)
        )
        candidate["omitted_premise"] = {
            "no_overlap_cap": (
                "size-three full-L overlap contribution at most twelve"
            ),
            "no_common_point": "common-point/Berge-triangle prohibition",
            "k_degree_at_most": (
                "exact K-degree eight weakened to K-degree at most eight"
            ),
        }[variant]
        semantic = {
            "variant": variant,
            "point_sets": candidate["point_sets"],
            "K_edges": candidate["K_edges"],
            "diagnostics": candidate["diagnostics"],
        }
        candidate["semantic_sha256"] = sha256_bytes(
            canonical_json_bytes(semantic)
        )
    return candidate


def solve(
    size3_count: int,
    root_mode: str,
    conflict_budget: int | None,
    solver_name: str,
    variant: str = "full",
) -> tuple[str, dict[str, object], dict[str, object] | None]:
    (
        cnf,
        pool,
        points,
        selected,
        k_edge,
        _f_edge,
        full_overlap,
    ) = build_instance(size3_count, root_mode, variant)
    formula_sha256 = cnf_sha256(cnf, pool.top)
    with Solver(
        name=solver_name,
        bootstrap_with=cnf.clauses,
        use_timer=True,
    ) as solver:
        if conflict_budget is None:
            satisfiable = solver.solve()
        else:
            solver.conf_budget(conflict_budget)
            satisfiable = solver.solve_limited()
        model = solver.get_model() if satisfiable is True else None
        statistics: dict[str, object] = {
            "variant": variant,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "python_sat": pysat.__version__,
            "solver": solver_name,
            "conflict_budget": conflict_budget,
            "solver_time_seconds": solver.time_accum(),
            "accumulated_stats": solver.accum_stats(),
            "variables": pool.top,
            "clauses": len(cnf.clauses),
            "cnf_sha256": formula_sha256,
            "candidate_point_variables": len(points),
            "candidate_K_edge_variables": len(k_edge),
            "candidate_full_overlap_variables": len(full_overlap),
        }
    status = (
        "SAT_WEAKENED_MODEL"
        if satisfiable is True
        else "UNSAT_UNVERIFIED"
        if satisfiable is False
        else "UNKNOWN_BUDGET_EXHAUSTED"
    )
    candidate = (
        candidate_from_model(
            size3_count=size3_count,
            root_mode=root_mode,
            variant=variant,
            points=points,
            selected=selected,
            k_edge=k_edge,
            model=model,
            solver_statistics=statistics,
        )
        if model is not None
        else None
    )
    return status, statistics, candidate


def scan_all_branches(
    conflict_budget: int | None,
    solver_name: str,
) -> dict[str, object]:
    rows = []
    for size3_count, root_mode in SCAN_BRANCHES:
        status, statistics, candidate = solve(
            size3_count,
            root_mode,
            conflict_budget,
            solver_name,
            "full",
        )
        rows.append(
            {
                "size3_point_count": size3_count,
                "root_mode": root_mode,
                "status": status,
                "statistics": statistics,
                "candidate_validation": (
                    candidate["validation"] if candidate is not None else None
                ),
            }
        )
        print(
            f"m={size3_count} root={root_mode} status={status} "
            f"conflicts={statistics['accumulated_stats'].get('conflicts')} "
            f"time={statistics['solver_time_seconds']}",
            file=sys.stderr,
            flush=True,
        )
    all_unsat = all(row["status"] == "UNSAT_UNVERIFIED" for row in rows)
    result = {
        "schema": "conway99-wave13-n3-45-active-local-sat-scan-v1",
        "status": (
            "COMPLETE_BRANCH_COVER_UNSAT_UNVERIFIED"
            if all_unsat
            else "BRANCH_COVER_HAS_SURVIVOR_OR_UNKNOWN"
        ),
        "branch_cover": [list(branch) for branch in SCAN_BRANCHES],
        "branch_count": len(rows),
        "branches": rows,
        "cover_justification": [
            "point-incidence parity makes the number m of size-three points odd",
            "the exact local modes are 111,122,222,223",
            "m=13 and m=15 have no integer incidence signatures",
            "a root of type 111,122,222,223 needs at least 1,3,4,5 size-three points respectively",
            "the sole m=11 incidence signature uses only root types 222 and 223",
            "the named root point and each rooted representative use only the full active-label relabeling action",
            "no automorphism of a completed graph is assumed",
        ],
        "proof_boundary": (
            "solver UNSAT returns have no emitted or independently checked "
            "proof trace and are not nonexistence certificates"
        ),
        "claim_label": "CANDIDATE",
        "target_result": "UNKNOWN",
    }
    semantic = {
        "schema": result["schema"],
        "status": result["status"],
        "branch_cover": result["branch_cover"],
        "branches": [
            {
                "size3_point_count": row["size3_point_count"],
                "root_mode": row["root_mode"],
                "status": row["status"],
                "variables": row["statistics"]["variables"],
                "clauses": row["statistics"]["clauses"],
                "cnf_sha256": row["statistics"]["cnf_sha256"],
            }
            for row in rows
        ],
        "claim_label": result["claim_label"],
        "target_result": result["target_result"],
    }
    result["semantic_sha256"] = sha256_bytes(canonical_json_bytes(semantic))
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size3", type=int, choices=ALLOWED_SIZE3_COUNTS)
    parser.add_argument("--root-mode", choices=ROOT_MODES)
    parser.add_argument("--variant", choices=SCOUT_VARIANTS, default="full")
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--conflict-budget", type=int)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--validate", type=Path)
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--scan-output", type=Path)
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)

    if arguments.conflict_budget is not None and arguments.conflict_budget < 1:
        parser.error("--conflict-budget must be positive")
    if arguments.validate is not None:
        candidate = json.loads(arguments.validate.read_text(encoding="utf-8"))
        result = (
            validate_weakened_candidate(candidate)
            if candidate.get("schema")
            == "conway99-wave13-n3-45-active-local-diagnostic-v1"
            else validate_candidate(candidate)
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if arguments.scan:
        if arguments.size3 is not None or arguments.root_mode is not None:
            parser.error("--scan cannot be combined with --size3/--root-mode")
        if arguments.candidate is not None:
            parser.error("--scan cannot write one --candidate")
        if arguments.variant != "full":
            parser.error("--scan uses the full variant only")
        scan = scan_all_branches(
            arguments.conflict_budget,
            arguments.solver,
        )
        rendered = json.dumps(scan, indent=2, sort_keys=True) + "\n"
        if arguments.scan_output is not None:
            arguments.scan_output.parent.mkdir(parents=True, exist_ok=True)
            arguments.scan_output.write_text(
                rendered, encoding="utf-8", newline="\n"
            )
        print(rendered, end="")
        return 0
    if arguments.size3 is None:
        parser.error("--size3 is required unless --validate is used")
    if arguments.root_mode is None:
        parser.error("--root-mode is required unless --validate is used")
    status, statistics, candidate = solve(
        arguments.size3,
        arguments.root_mode,
        arguments.conflict_budget,
        arguments.solver,
        arguments.variant,
    )
    if arguments.candidate is not None:
        if candidate is None:
            raise SystemExit("--candidate requested but no SAT model was found")
        arguments.candidate.parent.mkdir(parents=True, exist_ok=True)
        arguments.candidate.write_text(
            json.dumps(candidate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    output = {
        "status": status,
        "size3_point_count": arguments.size3,
        "root_mode": arguments.root_mode,
        "variant": arguments.variant,
        "statistics": statistics,
        "candidate": (
            str(arguments.candidate).replace("\\", "/")
            if arguments.candidate is not None and candidate is not None
            else None
        ),
        "candidate_validation": (
            (
                candidate.get("validation")
                or candidate.get("diagnostics")
            )
            if candidate is not None
            else None
        ),
        "claim_label": "CANDIDATE",
        "target_result": "UNKNOWN",
    }
    if arguments.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(status)
        print("size3_point_count", arguments.size3)
        print("root_mode", arguments.root_mode)
        print("variant", arguments.variant)
        print("variables", statistics["variables"])
        print("clauses", statistics["clauses"])
        print("solver_time_seconds", statistics["solver_time_seconds"])
        if candidate is not None:
            if "validation" in candidate:
                print(candidate["validation"]["status"])
                print(
                    "semantic_sha256",
                    candidate["validation"]["semantic_sha256"],
                )
            else:
                print(
                    "weakened_candidate_diagnostics",
                    json.dumps(candidate["diagnostics"], sort_keys=True),
                )
        print("claim_label CANDIDATE")
        print("target_result UNKNOWN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
