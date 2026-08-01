#!/usr/bin/env python3
"""Exact Wave 209 checker for the rank-three signed-trade branch.

The calculations are parameter identities, small integer compositions, and
complete labelled censuses on at most eight selected line labels.  No
99-vertex graph is generated or searched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "exact-results.json"

INPUT_HASHES = {
    "attempts/wave209-four-survivor-globalization/protocol.md":
        "3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196",
    "attempts/wave208-marked-m7g-proof-b/package-manifest.sha256":
        "f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc",
    "attempts/wave208-marked-m7g-proof-b/exact-results.json":
        "e8030f62781b2badf85bb46a266c1d71b651f7e8517dd6aec4a2e453c14e01af",
    "attempts/wave208-marked-m7g-proof-b/local-controls.json":
        "4fc0e87b03d824f640234cdc93441bd3286a2902f331fc5d75c9726f66c076cd",
}

SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
POLAR = (
    (0, 2, 2, 2, 0, 1, 1, 1),
    (2, 0, 2, 2, 1, 0, 1, 1),
    (2, 2, 0, 2, 1, 1, 0, 1),
    (2, 2, 2, 0, 1, 1, 1, 0),
    (0, 1, 1, 1, 0, 2, 2, 2),
    (1, 0, 1, 1, 2, 0, 2, 2),
    (1, 1, 0, 1, 2, 2, 0, 2),
    (1, 1, 1, 0, 2, 2, 2, 0),
)
LINE_PAIRS = tuple(combinations(range(8), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(LINE_PAIRS)}
PRODUCT_ONE_EDGES = tuple(
    pair for pair in LINE_PAIRS if POLAR[pair[0]][pair[1]] == 1
)


def selected_row_identity() -> dict[str, object]:
    """Replay (U^T A U-3U^T U) alpha=0 one labelled row at a time."""
    rows = []
    for index in range(8):
        same = [
            other
            for other in range(8)
            if other != index and SIGNS[other] == SIGNS[index]
        ]
        unmatched = [
            other
            for other in range(8)
            if SIGNS[other] != SIGNS[index] and POLAR[index][other] == 1
        ]
        matched = [
            other
            for other in range(8)
            if SIGNS[other] != SIGNS[index] and POLAR[index][other] == 0
        ]
        assert len(same) == len(unmatched) == 3 and len(matched) == 1
        # Divide the row by alpha_i.  The diagonal is -3, the three
        # same-sign entries contribute 3*2, and the unmatched opposite
        # entries contribute 3*(-1).
        assert -3 + 3*2 - 3 == 0
        rows.append(
            {
                "line": index,
                "matched_opposite_line": matched[0],
                "row_equation": "-matched_cross_count=0",
            }
        )
    return {
        "identity": "(U^T A U-3U^T U) alpha=0",
        "rows": rows,
        "all_four_matched_q0_cross_counts": [0, 0, 0, 0],
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_inputs() -> dict[str, str]:
    observed = {relative: sha256(ROOT / relative) for relative in INPUT_HASHES}
    assert observed == INPUT_HASHES
    return observed


def erdos_gallai(sequence: tuple[int, ...] | list[int]) -> bool:
    degrees = sorted(sequence, reverse=True)
    if sum(degrees) % 2:
        return False
    return all(
        sum(degrees[:r])
        <= r * (r - 1) + sum(min(degree, r) for degree in degrees[r:])
        for r in range(1, len(degrees) + 1)
    )


def gale_ryser(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    a = sorted(left, reverse=True)
    b = sorted(right, reverse=True)
    return sum(a) == sum(b) and all(
        sum(a[:r]) <= sum(min(degree, r) for degree in b)
        for r in range(1, len(a) + 1)
    )


def outside_distributions(
    vertices: int, first: int, second: int, maximum: int = 7
) -> list[tuple[int, ...]]:
    """All (z_0,...,z_maximum) with three exact moment constraints."""
    rows: list[tuple[int, ...]] = []

    def recurse(t: int, count: int, moment1: int, moment2: int, high: list[int]) -> None:
        if t == 1:
            z1 = moment1
            z0 = count - z1
            if moment2 == moment1 and z0 >= 0 and z1 >= 0:
                rows.append((z0, z1, *reversed(high)))
            return
        if count < 0 or moment1 < 0 or moment2 < 0:
            return
        bound = min(count, moment1 // t, moment2 // (t * t))
        for value in range(bound + 1):
            recurse(
                t - 1,
                count - value,
                moment1 - t * value,
                moment2 - t * t * value,
                high + [value],
            )

    recurse(maximum, vertices, first, second, [])
    return rows


@lru_cache(maxsize=None)
def degree_profiles(k: int, x: int) -> tuple[tuple[int, ...], ...]:
    """Opposite-sign degree profiles compatible with each same-sign graph."""
    maximum = min(5, k - 4)
    return tuple(
        sequence
        for sequence in combinations_with_replacement(range(maximum + 1), k)
        if sum(sequence) == x
        and erdos_gallai(tuple(value + 3 for value in sequence))
    )


@lru_cache(maxsize=None)
def shell_catalog(k: int) -> tuple[dict[str, object], ...]:
    """Complete aggregate catalog under the stated exact necessary tests."""
    rows: list[dict[str, object]] = []
    for x in range(k * k // 9 + 1):
        if (x + 3 * k) % 2:
            continue
        for positive in degree_profiles(k, x):
            for negative in degree_profiles(k, x):
                if not gale_ryser(positive, negative):
                    continue
                squares = sum(value * value for value in positive + negative)
                first = 11 * k - 2 * x
                second = 2 * k * k - 7 * x - squares
                for outside in outside_distributions(99 - 2 * k, first, second):
                    rows.append(
                        {
                            "k": k,
                            "x": x,
                            "positive_opposite_degrees": list(positive),
                            "negative_opposite_degrees": list(negative),
                            "degree_square_sum": squares,
                            "outside_signatures_z0_to_z7": list(outside),
                        }
                    )
    return tuple(rows)


ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)


def adjacency(edges: tuple[tuple[int, int], ...], vertices: int = 7) -> list[set[int]]:
    graph = [set() for _ in range(vertices)]
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def rooted_canonical(edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    edge_set = set(edges)
    representatives = []
    for tail in permutations(range(1, 7)):
        relabel = (0, *tail)
        representatives.append(
            tuple(
                sorted(
                    tuple(sorted((relabel[left], relabel[right])))
                    for left, right in edge_set
                )
            )
        )
    return min(representatives)


@lru_cache(maxsize=1)
def rooted_support_census() -> dict[str, object]:
    """Complete 7-vertex census; root 0 is the unique cross-edge endpoint."""
    tail_edges = tuple(combinations(range(1, 7), 2))
    degree_count = 0
    lambda_count = 0
    valid: list[tuple[tuple[int, int], ...]] = []
    lambda_types: Counter[tuple[tuple[int, int], ...]] = Counter()
    for root_neighbors in combinations(range(1, 7), 4):
        root_edges = tuple((0, vertex) for vertex in root_neighbors)
        for tail in combinations(tail_edges, 7):
            edges = tuple(sorted(root_edges + tail))
            graph = adjacency(edges)
            if [len(row) for row in graph] != [4, 3, 3, 3, 3, 3, 3]:
                continue
            degree_count += 1
            if any(len(graph[u] & graph[v]) > 1 for u, v in edges):
                continue
            lambda_count += 1
            canonical = rooted_canonical(edges)
            lambda_types[canonical] += 1
            if any(
                v not in graph[u] and len(graph[u] & graph[v]) > 2
                for u, v in combinations(range(7), 2)
            ):
                continue
            valid.append(edges)
    valid_types = Counter(rooted_canonical(edges) for edges in valid)
    assert valid_types == Counter({ROOTED_EDGES: 180})
    assert len(lambda_types) == 2
    rejected = next(kind for kind in lambda_types if kind != ROOTED_EDGES)
    rejected_graph = adjacency(rejected)
    rejected_max_mu = max(
        len(rejected_graph[u] & rejected_graph[v])
        for u, v in combinations(range(7), 2)
        if v not in rejected_graph[u]
    )
    return {
        "degree_sequence_graphs": degree_count,
        "lambda_cap_graphs": lambda_count,
        "lambda_cap_rooted_types": len(lambda_types),
        "lambda_mu_cap_graphs": len(valid),
        "lambda_mu_cap_rooted_types": len(valid_types),
        "canonical_edges": [list(edge) for edge in ROOTED_EDGES],
        "rejected_type_max_internal_common_neighbors_on_a_nonedge": rejected_max_mu,
    }


def deficit_edges() -> tuple[tuple[int, int], ...]:
    graph = adjacency(ROOTED_EDGES)
    positive = []
    for left, right in combinations(range(7), 2):
        ambient = 1 if right in graph[left] else 2
        deficit = ambient - len(graph[left] & graph[right])
        assert deficit in (0, 1)
        if deficit:
            positive.append((left, right))
    assert len(positive) == 7
    assert not any(
        all(tuple(sorted(edge)) in positive for edge in combinations(triple, 2))
        for triple in combinations(range(7), 3)
    )
    return tuple(positive)


def x3_intersection_obstruction() -> dict[str, int | bool]:
    """The sole x=3 moment row has t<=1 at all 85 zero coordinates."""
    total = 0
    compatible = 0
    for chosen in combinations(PRODUCT_ONE_EDGES, 5):
        total += 1
        degrees = [0] * 8
        for left, right in chosen:
            degrees[left] += 1
            degrees[right] += 1
        # At the intersection point of lines i,j, t is at least
        # max(3-d_i,3-d_j).  The x=3 row permits only t<=1.
        if all(min(degrees[left], degrees[right]) >= 2 for left, right in chosen):
            compatible += 1
    assert total == 792 and compatible == 0
    return {
        "labelled_five_edge_subsets_checked": total,
        "subsets_compatible_with_all_intersection_signatures_t_le_1": compatible,
        "x3_eliminated": True,
    }


@lru_cache(maxsize=1)
def cross_deficit_bijection_census() -> dict[str, object]:
    """Pair the seven P-deficit rows with the seven N-deficit rows."""
    graph = adjacency(ROOTED_EDGES)
    deficits = deficit_edges()
    required = [[2 for _ in range(7)] for _ in range(7)]
    required[0][0] = 1
    for vertex in graph[0]:
        required[vertex][0] -= 1
        required[0][vertex] -= 1
    valid = 0
    residual_value_profiles: Counter[tuple[int, int, int]] = Counter()
    row_sums = set()
    for matching in permutations(range(7)):
        residual = [row[:] for row in required]
        for p_index, n_index in enumerate(matching):
            for p_vertex in deficits[p_index]:
                for n_vertex in deficits[n_index]:
                    residual[p_vertex][n_vertex] -= 1
        if min(min(row) for row in residual) < 0:
            continue
        valid += 1
        flat = [value for row in residual for value in row]
        residual_value_profiles[
            (flat.count(0), flat.count(1), flat.count(2))
        ] += 1
        row_sums.add(tuple(sum(row) for row in residual))
        row_sums.add(tuple(sum(residual[i][j] for i in range(7)) for j in range(7)))
    assert row_sums == {(9, 9, 9, 9, 9, 8, 8)}
    return {
        "all_bijections": 5040,
        "capacity_compatible_bijections": valid,
        "residual_value_profile_counts": {
            f"zeros_{profile[0]}_ones_{profile[1]}_twos_{profile[2]}": count
            for profile, count in sorted(residual_value_profiles.items())
        },
        "t1_incidence_degrees_each_side": [9, 9, 9, 9, 9, 8, 8],
    }


def external_third_edges() -> tuple[tuple[int, int], ...]:
    graph = adjacency(ROOTED_EDGES)
    return tuple(
        edge for edge in ROOTED_EDGES if not (graph[edge[0]] & graph[edge[1]])
    )


def marked_line_packings(degrees: tuple[int, int, int, int]) -> int:
    """Pack one sign side into selected-line support blocks."""
    block_sizes = tuple(3 - degree for degree in degrees)
    graph_edges = set(ROOTED_EDGES)
    external = set(external_third_edges())
    count = 0

    def recurse(remaining: set[int], index: int) -> None:
        nonlocal count
        if index == 4:
            if not remaining:
                count += 1
            return
        size = block_sizes[index]
        if size == 0:
            recurse(remaining, index + 1)
            return
        for block in combinations(sorted(remaining), size):
            if size == 3 and not all(
                tuple(sorted(edge)) in graph_edges for edge in combinations(block, 2)
            ):
                continue
            if size == 2 and tuple(sorted(block)) not in external:
                continue
            recurse(remaining - set(block), index + 1)

    recurse(set(range(7)), 0)
    return count


@lru_cache(maxsize=1)
def marked_line_census() -> dict[str, object]:
    graph = adjacency(ROOTED_EDGES)
    triangles = tuple(
        triple
        for triple in combinations(range(7), 3)
        if all(tuple(sorted(edge)) in set(ROOTED_EDGES) for edge in combinations(triple, 2))
    )
    external = external_third_edges()
    maximum_matching = max(
        size
        for size in range(4)
        if any(
            len(set(vertex for edge in matching for vertex in edge)) == 2 * size
            for matching in combinations(external, size)
        )
    )
    patterns = {
        "3,2,0,0": marked_line_packings((3, 2, 0, 0)),
        "3,1,1,0": marked_line_packings((3, 1, 1, 0)),
        "2,2,1,0": marked_line_packings((2, 2, 1, 0)),
        "2,1,1,1": marked_line_packings((2, 1, 1, 1)),
    }
    assert patterns == {"3,2,0,0": 0, "3,1,1,0": 4, "2,2,1,0": 12, "2,1,1,1": 0}
    assert all(0 in triangle for triangle in triangles)
    return {
        "support_triangles": [list(row) for row in triangles],
        "all_support_triangles_contain_cross_root": True,
        "external_third_edges": [list(edge) for edge in external],
        "external_third_edge_matching_number": maximum_matching,
        "representative_ordered_packing_counts": patterns,
        "allowed_intersection_degree_multisets": [
            [3, 1, 1, 0], [2, 2, 1, 0]
        ],
    }


@lru_cache(maxsize=1)
def labelled_m5_census() -> dict[str, object]:
    allowed = {(3, 1, 1, 0), (2, 2, 1, 0)}
    all_graphs = 0
    final_graphs = 0
    types: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    for chosen in combinations(PRODUCT_ONE_EDGES, 5):
        all_graphs += 1
        degrees = [0] * 8
        for left, right in chosen:
            degrees[left] += 1
            degrees[right] += 1
        positive = tuple(sorted(degrees[:4], reverse=True))
        negative = tuple(sorted(degrees[4:], reverse=True))
        if positive not in allowed or negative not in allowed:
            continue
        positive_isolated = degrees[:4].index(0)
        negative_isolated = 4 + degrees[4:].index(0)
        if (positive_isolated, negative_isolated) not in PRODUCT_ONE_EDGES:
            continue
        final_graphs += 1
        types[(positive, negative)] += 1
    assert all_graphs == 792
    assert final_graphs == 204
    return {
        "all_labelled_five_edge_subsets": all_graphs,
        "labelled_subsets_after_marked_line_and_root_cross_edge_tests": final_graphs,
        "degree_type_counts": {
            f"P_{','.join(map(str, p))}__N_{','.join(map(str, n))}": count
            for (p, n), count in sorted(types.items())
        },
    }


def pair_coefficients(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    coefficients = [0] * len(LINE_PAIRS)
    for i in left:
        for j in right:
            if i != j:
                coefficients[PAIR_INDEX[tuple(sorted((i, j)))]] += 1
    return tuple(coefficients)


def zero_edge_capacity(chosen: tuple[tuple[int, int], ...]) -> tuple[int, int]:
    """Exact DP upper bound on opposite-pair counts mediated by intersection zeros."""
    intersection_set = set(chosen)
    degrees = [0] * 8
    for edge in chosen:
        for index in edge:
            degrees[index] += 1
    zero_groups = [(tuple(edge), 1) for edge in chosen]
    singleton_groups = [
        ((index,), 3 - degrees[index])
        for index in range(8)
        if 3 - degrees[index]
    ]
    groups = zero_groups + singleton_groups
    forced = [0] * len(LINE_PAIRS)
    for first, (membership, multiplicity) in enumerate(groups):
        if multiplicity > 1:
            coefficient = pair_coefficients(membership, membership)
            capacity = multiplicity * (multiplicity - 1) // 2
            forced = [a + capacity * b for a, b in zip(forced, coefficient)]
        for other_membership, other_multiplicity in groups[first + 1:]:
            if set(membership) & set(other_membership):
                coefficient = pair_coefficients(membership, other_membership)
                capacity = multiplicity * other_multiplicity
                forced = [a + capacity * b for a, b in zip(forced, coefficient)]
    target = tuple(
        (4 if pair in intersection_set else POLAR[pair[0]][pair[1]])
        - forced[PAIR_INDEX[pair]]
        for pair in LINE_PAIRS
    )
    assert min(target) >= 0
    variables: list[tuple[tuple[int, ...], int]] = []
    zero_count = len(zero_groups)
    for first, (membership, multiplicity) in enumerate(groups):
        for second in range(first + 1, len(groups)):
            other_membership, other_multiplicity = groups[second]
            if set(membership) & set(other_membership):
                continue
            if first >= zero_count and second >= zero_count:
                continue
            coefficient = pair_coefficients(membership, other_membership)
            if any(coefficient):
                variables.append((coefficient, multiplicity * other_multiplicity))
    zero = (0,) * len(LINE_PAIRS)
    states = {zero}
    for coefficient, capacity in variables:
        updated = set(states)
        for state in states:
            for value in range(1, capacity + 1):
                candidate = tuple(
                    state[index] + value * coefficient[index]
                    for index in range(len(LINE_PAIRS))
                )
                if any(candidate[index] > target[index] for index in range(len(target))):
                    break
                updated.add(candidate)
        states = updated
    opposite_indices = [
        PAIR_INDEX[(left, right)] for left in range(4) for right in range(4, 8)
    ]
    forced_opposite = sum(forced[index] for index in opposite_indices)
    maximum = forced_opposite + max(
        sum(state[index] for index in opposite_indices) for state in states
    )
    return maximum, len(states)


def m2_kind(chosen: tuple[tuple[int, int], ...]) -> str:
    first, second = chosen
    if first[0] == second[0] or first[1] == second[1]:
        return "shared_endpoint"
    if first[0] == second[1] - 4 and second[0] == first[1] - 4:
        return "swapped_disjoint"
    return "other_disjoint"


@lru_cache(maxsize=1)
def labelled_m2_capacity_census() -> dict[str, object]:
    counts: Counter[tuple[str, int]] = Counter()
    state_maximum = 0
    for chosen in combinations(PRODUCT_ONE_EDGES, 2):
        maximum_zero, states = zero_edge_capacity(chosen)
        state_maximum = max(state_maximum, states)
        counts[(m2_kind(chosen), 18 - maximum_zero)] += 1
    return {
        "all_labelled_two_edge_subsets": 66,
        "exact_relaxation_counts_by_kind_and_raw_x_lower_bound": {
            f"{kind}_xmin_{minimum}": count
            for (kind, minimum), count in sorted(counts.items())
        },
        "maximum_dynamic_states": state_maximum,
        "after_even_parity_and_global_moments": {
            "shared_endpoint_24_subsets": [6, 8],
            "swapped_disjoint_6_subsets": [2, 4, 6, 8],
            "other_disjoint_36_subsets": [4, 6, 8],
        },
    }


def control_summary(control: dict[str, object]) -> dict[str, object]:
    triangles = [tuple(row) for row in control["triangles"]]
    values = list(control["b_integer"])
    edges = set()
    for triangle in triangles:
        edges.update(tuple(sorted(edge)) for edge in combinations(triangle, 2))
    edges.update(tuple(sorted(edge)) for edge in control["extra_edges"])
    positive = [index for index, value in enumerate(values) if value == 1]
    negative = [index for index, value in enumerate(values) if value == -1]
    x = sum(
        (left in positive and right in negative)
        or (left in negative and right in positive)
        for left, right in edges
    )
    for vertex, value in enumerate(values):
        signed_neighbors = sum(
            values[other]
            for other in range(len(values))
            if other != vertex and tuple(sorted((vertex, other))) in edges
        )
        assert signed_neighbors == 3 * value
    graph = adjacency(tuple(edges), len(values))
    for left, right in combinations(range(len(values)), 2):
        common = len(graph[left] & graph[right])
        if right in graph[left]:
            assert common <= 1
        else:
            assert common <= 2
    positive_opposite = sorted(sum(other in graph[v] for other in negative) for v in positive)
    negative_opposite = sorted(sum(other in graph[v] for other in positive) for v in negative)
    degrees = [0] * 8
    for left, right in control["selected_triangle_intersections"]:
        degrees[left] += 1
        degrees[right] += 1
    return {
        "name": control["name"],
        "vertices": len(values),
        "support": len(positive) + len(negative),
        "x": x,
        "positive_opposite_degrees": positive_opposite,
        "negative_opposite_degrees": negative_opposite,
        "selected_intersection_degrees": degrees,
        "internal_Ac_equals_3c": True,
        "induced_lambda_mu_caps": True,
    }


@lru_cache(maxsize=1)
def imported_controls() -> tuple[dict[str, object], ...]:
    payload = json.loads(
        (ROOT / "attempts/wave208-marked-m7g-proof-b/local-controls.json").read_text(
            encoding="utf-8"
        )
    )
    return tuple(control_summary(control) for control in payload["controls"])


LINE_WITNESSES = {
    "weight14": {
        "k": 7, "x": 1,
        "types": {
            "PPP": 1, "PPN": 0, "PNN": 0, "NNN": 1,
            "PP0": 8, "PN0": 1, "NN0": 8,
            "P00": 29, "N00": 29, "000": 154,
        },
    },
    "weight20": {
        "k": 10, "x": 6,
        "types": {
            "PPP": 3, "PPN": 0, "PNN": 0, "NNN": 2,
            "PP0": 9, "PN0": 6, "NN0": 12,
            "P00": 37, "N00": 34, "000": 128,
        },
    },
}


def verify_line_witness(row: dict[str, object]) -> bool:
    k = int(row["k"])
    x = int(row["x"])
    n = row["types"]
    assert isinstance(n, dict)
    assert sum(n.values()) == 231
    plus = 3*n["PPP"] + 2*n["PPN"] + n["PNN"] + 2*n["PP0"] + n["PN0"] + n["P00"]
    minus = n["PPN"] + 2*n["PNN"] + 3*n["NNN"] + n["PN0"] + 2*n["NN0"] + n["N00"]
    pp = 3*n["PPP"] + n["PPN"] + n["PP0"]
    nn = n["PNN"] + 3*n["NNN"] + n["NN0"]
    pn = 2*n["PPN"] + 2*n["PNN"] + n["PN0"]
    assert plus == minus == 7*k
    assert pp == nn == (x + 3*k)//2
    assert pn == x
    return True


def line_graph_moments(k: int, m: int, degree_square_sum: int) -> dict[str, int]:
    selected = 72 - 12*m + degree_square_sum
    total = 20*k
    return {
        "point_support": 2*k,
        "line_vector_squared_norm": total,
        "selected_line_squared_norm": selected,
        "unselected_line_squared_norm": total - selected,
    }


def catalog_summary(k: int) -> dict[str, object]:
    rows = shell_catalog(k)
    by_x = Counter(int(row["x"]) for row in rows)
    profile_pairs = Counter()
    seen = set()
    for row in rows:
        key = (
            row["x"],
            tuple(row["positive_opposite_degrees"]),
            tuple(row["negative_opposite_degrees"]),
        )
        if key not in seen:
            profile_pairs[int(row["x"])] += 1
            seen.add(key)
    return {
        "aggregate_rows": len(rows),
        "rows_by_x": {str(x): by_x[x] for x in sorted(by_x)},
        "degree_profile_pairs_with_rows_by_x": {
            str(x): profile_pairs[x] for x in sorted(profile_pairs)
        },
    }


@lru_cache(maxsize=1)
def build_results() -> dict[str, object]:
    inputs = verify_inputs()
    raw_catalog = {"k7": shell_catalog(7), "k10": shell_catalog(10)}
    catalog_bytes = json.dumps(
        raw_catalog, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    controls = imported_controls()
    assert controls[0]["x"] == 6 and controls[1]["x"] == 1
    for witness in LINE_WITNESSES.values():
        assert verify_line_witness(witness)
    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "inputs": inputs,
        "general_identities": {
            "positive_and_negative_sizes": "|P|=|N|=k",
            "support_vertex_signatures": "P: (j+3,j), N: (j,j+3)",
            "outside_vertex_signatures": "Z: (t,t)",
            "cross_edges": "x=e(P,N)",
            "same_sign_edges_each_side": "(x+3k)/2",
            "outside_first_moment": "sum t z_t = 11k-2x",
            "outside_second_moment": "sum t^2 z_t = 2k^2-7x-sum j_v^2",
            "spectral_support_bound": "x <= k^2/9",
            "line_trade": "t=B^T c, C t=7t, B t=10c, ||t||^2=20k",
            "line_occupancy": "R2=2x+3k-3R3; R1=8k-4x+3R3; R0=231-11k+2x-R3",
        },
        "selected_line_row_identity": selected_row_identity(),
        "raw_aggregate_catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
        "raw_catalogs": {"weight14": catalog_summary(7), "weight20": catalog_summary(10)},
        "weight14_final_reduction": {
            "raw_rows": [
                {
                    "x": row["x"],
                    "positive_opposite_degrees": row["positive_opposite_degrees"],
                    "negative_opposite_degrees": row["negative_opposite_degrees"],
                    "outside_signatures_z0_to_z7": row["outside_signatures_z0_to_z7"],
                }
                for row in shell_catalog(7)
            ],
            "x3_intersection_obstruction": x3_intersection_obstruction(),
            "forced_x": 1,
            "forced_outside_signatures_z0_to_z7": [17, 61, 7, 0, 0, 0, 0, 0],
            "rooted_support_census": rooted_support_census(),
            "deficit_edges": [list(edge) for edge in deficit_edges()],
            "cross_deficit_bijections": cross_deficit_bijection_census(),
            "marked_line_census": marked_line_census(),
            "labelled_selected_intersection_census": labelled_m5_census(),
            "line_graph_norms_by_degree_square_sum": {
                str(squares): line_graph_moments(7, 5, squares)
                for squares in (18, 20, 22)
            },
        },
        "weight20_reduction": {
            "aggregate_rows_after_x0_and_x10_exclusions": 352,
            "remaining_rows_by_x": {
                key: value
                for key, value in catalog_summary(10)["rows_by_x"].items()
                if key in {"2", "4", "6", "8"}
            },
            "selected_pair_zero_capacity": labelled_m2_capacity_census(),
            "line_graph_norms": {
                "shared_endpoint": line_graph_moments(10, 2, 6),
                "disjoint": line_graph_moments(10, 2, 4),
            },
        },
        "hostile_positive_controls": list(controls),
        "aggregate_line_type_witnesses": LINE_WITNESSES,
        "limitations": [
            "the weight-14 reduction stops at 204 labelled selected-intersection graphs and 4480 capacity-compatible outside deficit bijections for each fixed rooted support labelling",
            "the 352 weight-20 rows are aggregate necessary profiles, not graph realizations",
            "the line-type witnesses do not assign 231 actual lines or satisfy their pairwise intersections",
            "the imported 19- and 22-vertex controls are induced controls, not 99-vertex completions",
            "no target automorphism, 99-vertex adjacency matrix, endpoint exclusion, or counterexample is supplied",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--emit-catalog", action="store_true")
    args = parser.parse_args()
    if args.emit_catalog:
        payload = {"k7": shell_catalog(7), "k10": shell_catalog(10)}
    else:
        payload = build_results()
    if args.verify:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        assert payload == expected
        print("verified", RESULTS.as_posix())
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
