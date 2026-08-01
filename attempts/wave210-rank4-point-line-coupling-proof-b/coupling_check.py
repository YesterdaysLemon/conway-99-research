#!/usr/bin/env python3
"""Exact Wave 210 point--line coupling for the Wave 209 rank-four survivors.

The default path is a standard-library replay.  It reconstructs the three
rank-four forms, all 249 marked branches and their 24 constraint-relabeling
orbits, independently replays the sealed Wave 209 point-census certificates,
then checks the archived Wave 210 integer Farkas certificates against every
locally possible residual-triangle decomposition.

``--generate`` is discovery-only.  It imports SciPy and highspy to obtain
candidate dual rays, rationalizes them, and accepts them only after the same
integer replay used by the default path.  Solver status is never evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import gcd, lcm
from pathlib import Path
from typing import Callable, Iterable


Q = 3
SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
FORM_DIAGONALS = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
ALLOWED_POINT_WEIGHTS = {14, 17, 20, 23}
SURVIVOR_ORBITS = (0, 2, 4, 11, 12, 14, 23)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERTIFICATES = HERE / "coupling-certificates.json"
COARSE_CONTROLS = HERE / "coarse-q-type-controls.json"
RESULTS = HERE / "exact-results.json"
WAVE209_POINT_CONTROLS = (
    ROOT / "attempts" / "wave209-rank4-norm56-proof-b" / "point-signature-controls.json"
)

FROZEN_HASHES = {
    "AGENTS.md": "4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3",
    "attempts/wave209-four-survivor-globalization/protocol.md":
        "3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196",
    "attempts/wave209-rank4-norm56-proof-b/package-manifest.sha256":
        "2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b",
    "verification/wave209-rank4-point-signature-verifier/package-manifest.sha256":
        "62c32cfa278a677053353d5a3c21c01600cadc867d597f5135ab32a6fdb1c07a",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sha256_manifest(path: Path) -> int:
    entries = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        relative = relative.strip().lstrip("*")
        actual = sha256(ROOT / relative)
        assert actual == expected.lower(), (relative, expected, actual)
        entries += 1
    return entries


def check_frozen_inputs() -> None:
    for relative, expected in FROZEN_HASHES.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, (relative, expected, actual)
    assert verify_sha256_manifest(
        ROOT / "attempts" / "wave209-rank4-norm56-proof-b" / "package-manifest.sha256"
    ) == 12
    assert verify_sha256_manifest(
        ROOT / "verification" / "wave209-rank4-point-signature-verifier" / "package-manifest.sha256"
    ) == 7


def m7g_columns() -> tuple[tuple[int, int, int, int], ...]:
    return (
        (1, 2, 2, 2),
        (1, 0, 2, 2),
        (1, 2, 0, 2),
        (1, 2, 2, 0),
        (1, 1, 1, 1),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
    )


def restricted_form(diagonal: tuple[int, int, int]) -> tuple[tuple[int, ...], ...]:
    d1, d2, d3 = diagonal
    a = (d1 + d2 + d3) % Q
    return (
        (a, 0, 0, 0),
        (0, d1, (-a - d3) % Q, (-a - d2) % Q),
        (0, (-a - d3) % Q, d2, (-a - d1) % Q),
        (0, (-a - d2) % Q, (-a - d1) % Q, d3),
    )


@lru_cache(maxsize=None)
def polar_matrix(diagonal: tuple[int, int, int]) -> tuple[tuple[int, ...], ...]:
    columns = m7g_columns()
    form = restricted_form(diagonal)
    return tuple(
        tuple(
            sum(
                columns[i][r] * form[r][s] * columns[j][s]
                for r in range(4)
                for s in range(4)
            )
            % Q
            for j in range(8)
        )
        for i in range(8)
    )


@lru_cache(maxsize=None)
def accepted_intersection_sets(
    D: tuple[tuple[int, ...], ...]
) -> tuple[frozenset[tuple[int, int]], ...]:
    one_pairs = tuple((i, j) for i, j in combinations(range(8), 2) if D[i][j] == 1)
    accepted: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(one_pairs)):
        H = frozenset(edge for bit, edge in enumerate(one_pairs) if mask & (1 << bit))
        if sum(SIGNS[i] * SIGNS[j] for i, j in H) % Q != 1:
            continue
        degrees = [sum(i in edge for edge in H) for i in range(8)]
        if max(degrees) > 3:
            continue
        point_values = [SIGNS[i] + SIGNS[j] for i, j in H]
        point_values.extend(SIGNS[i] for i in range(8) for _ in range(3 - degrees[i]))
        residues = [value % Q for value in point_values]
        weight = sum(value != 0 for value in residues)
        if weight not in ALLOWED_POINT_WEIGHTS:
            continue
        if weight == 14 and (residues.count(1), residues.count(2)) != (7, 7):
            continue
        accepted.append(H)
    return tuple(accepted)


@lru_cache(maxsize=None)
def sign_preserving_permutations() -> tuple[tuple[int, ...], ...]:
    return tuple(
        positive + negative
        for positive in permutations(range(4))
        for negative in permutations(range(4, 8))
    )


@lru_cache(maxsize=None)
def form_maps(
    source: tuple[tuple[int, ...], ...], target: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in sign_preserving_permutations()
        if all(
            source[i][j] == target[permutation[i]][permutation[j]]
            for i in range(8)
            for j in range(8)
        )
    )


def rename_H(
    H: frozenset[tuple[int, int]], permutation: tuple[int, ...]
) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted((permutation[i], permutation[j]))) for i, j in H)


@lru_cache(maxsize=None)
def branch_orbits() -> tuple[
    tuple[tuple[int, frozenset[tuple[int, int]]], ...], ...
]:
    forms = tuple(polar_matrix(diagonal) for diagonal in FORM_DIAGONALS)
    subsets = tuple(accepted_intersection_sets(D) for D in forms)
    nodes = {(form_index, H) for form_index in range(3) for H in subsets[form_index]}
    maps = {
        (source, target): form_maps(forms[source], forms[target])
        for source in range(3)
        for target in range(3)
    }
    unseen = set(nodes)
    answer = []
    while unseen:
        seed = min(unseen, key=lambda item: (item[0], sorted(item[1])))
        orbit: set[tuple[int, frozenset[tuple[int, int]]]] = set()
        stack = [seed]
        while stack:
            form_index, H = stack.pop()
            if (form_index, H) in orbit:
                continue
            orbit.add((form_index, H))
            for target in range(3):
                for permutation in maps[(form_index, target)]:
                    image = (target, rename_H(H, permutation))
                    if image in nodes and image not in orbit:
                        stack.append(image)
        unseen.difference_update(orbit)
        answer.append(tuple(sorted(orbit, key=lambda item: (item[0], sorted(item[1])))))
    return tuple(answer)


def signature_code(signature: tuple[int, ...]) -> int:
    return sum((value + 1) * (3**i) for i, value in enumerate(signature))


def decode_signature(code: int) -> tuple[int, ...]:
    answer = []
    for _ in range(8):
        answer.append(code % 3 - 1)
        code //= 3
    assert code == 0
    return tuple(answer)


@lru_cache(maxsize=None)
def point_signatures() -> tuple[tuple[int, ...], ...]:
    answer = tuple(
        signature
        for signature in product((-1, 0, 1), repeat=8)
        if sum(SIGNS[i] * signature[i] for i in range(8)) % 3 == 0
    )
    assert len(answer) == 2187
    return answer


def q_value(signature: tuple[int, ...]) -> int:
    numerator = sum(SIGNS[i] * signature[i] for i in range(8))
    assert numerator % 3 == 0
    return numerator // 3


def selected_membership(signature: tuple[int, ...]) -> frozenset[int]:
    return frozenset(i for i, value in enumerate(signature) if value == -1)


@lru_cache(maxsize=None)
def admissible_point_signatures(
    H: frozenset[tuple[int, int]],
) -> tuple[tuple[int, ...], ...]:
    """Point rows allowed by the known selected-triangle intersections.

    A point is on no selected triangle, on one selected triangle, or on the
    two selected triangles of one edge of H.  Three selected triangles cannot
    share a point here because every accepted H is triangle-free; a pair not
    in H is disjoint by definition.
    """
    answer = []
    for signature in point_signatures():
        membership = selected_membership(signature)
        if not membership or len(membership) == 1:
            answer.append(signature)
        elif len(membership) == 2 and tuple(sorted(membership)) in H:
            answer.append(signature)
    return tuple(answer)


def pair_table(
    D: tuple[tuple[int, ...], ...],
    H: frozenset[tuple[int, int]],
    i: int,
    j: int,
) -> dict[tuple[int, int], int]:
    if (i, j) in H:
        rows = ((1, 0, 2), (0, 40, 20), (2, 20, 14))
    else:
        d = D[i][j]
        rows = (
            (0, 3 - d, d),
            (3 - d, 39 - 3 * d, 18 + 4 * d),
            (d, 18 + 4 * d, 18 - 5 * d),
        )
    values = (-1, 0, 1)
    return {(values[r], values[c]): rows[r][c] for r in range(3) for c in range(3)}


@dataclass(frozen=True)
class Equation:
    name: str
    target: int
    feature: Callable[[object], int]


@lru_cache(maxsize=None)
def point_equations(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[Equation, ...]:
    equations = [Equation("total", 99, lambda signature: 1)]
    for i in range(8):
        for value, target in ((-1, 3), (0, 60), (1, 36)):
            equations.append(
                Equation(
                    f"m_{i}_{value}",
                    target,
                    lambda signature, i=i, value=value: int(signature[i] == value),
                )
            )
    for i, j in combinations(range(8), 2):
        table = pair_table(D, H, i, j)
        for left in (-1, 0, 1):
            for right in (-1, 0, 1):
                equations.append(
                    Equation(
                        f"p_{i}_{j}_{left}_{right}",
                        table[(left, right)],
                        lambda signature, i=i, j=j, left=left, right=right: int(
                            signature[i] == left and signature[j] == right
                        ),
                    )
                )
    equations.extend(
        (
            Equation("q_sum", 0, lambda signature: q_value(signature)),
            Equation("q_square", 56, lambda signature: q_value(signature) ** 2),
        )
    )
    assert len(equations) == 279
    return tuple(equations)


@lru_cache(maxsize=None)
def polar_words(D: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    answer = {
        tuple(sum(coefficients[k] * D[k][i] for k in range(8)) % Q for i in range(8))
        for coefficients in product(range(Q), repeat=8)
    }
    assert len(answer) == 81
    return tuple(sorted(answer))


TriangleType = tuple[tuple[int, ...], frozenset[int], int]


@lru_cache(maxsize=None)
def triangle_types(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[TriangleType, ...]:
    answer: list[TriangleType] = []
    for d in polar_words(D):
        ones = tuple(i for i, value in enumerate(d) if value == 1)
        for mask in range(1 << len(ones)):
            h = frozenset(ones[bit] for bit in range(len(ones)) if mask & (1 << bit))
            degrees = {i: 0 for i in h}
            edges = 0
            allowed = True
            for i, j in combinations(sorted(h), 2):
                if (i, j) in H:
                    degrees[i] += 1
                    degrees[j] += 1
                    edges += 1
                    if degrees[i] > 1 or degrees[j] > 1:
                        allowed = False
                        break
                elif D[i][j] == 0:
                    allowed = False
                    break
            if not allowed or len(h) - edges > 3:
                continue
            numerator = sum(SIGNS[i] * d[i] for i in range(8))
            assert numerator % 3 == 0
            t = numerator // 3
            assert -2 <= t <= 2
            answer.append((d, h, t))
    return tuple(answer)


def selected_pair_residual_count(
    D: tuple[tuple[int, ...], ...],
    H: frozenset[tuple[int, int]],
    i: int,
    j: int,
) -> int:
    if (i, j) in H:
        return 5
    already_selected = sum(
        tuple(sorted((i, k))) in H and tuple(sorted((j, k))) in H
        for k in range(8)
        if k not in (i, j)
    )
    return D[i][j] - already_selected


@lru_cache(maxsize=None)
def aggregate_equations(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[Equation, ...]:
    equations = [Equation("total", 223, lambda row: 1)]
    for i in range(8):
        for value, full in ((0, 32), (1, 162), (2, 36)):
            selected = sum(D[k][i] == value for k in range(8) if k != i)
            equations.append(
                Equation(
                    f"d_{i}_{value}",
                    full - selected,
                    lambda row, i=i, value=value: int(row[0][i] == value),
                )
            )
    F = tuple(tuple(-3 if i == j else D[i][j] for j in range(8)) for i in range(8))
    for i, j in combinations(range(8), 2):
        target = 252 - 21 * D[i][j] - sum(F[k][i] * F[k][j] for k in range(8))
        equations.append(
            Equation(
                f"dprod_{i}_{j}",
                target,
                lambda row, i=i, j=j: row[0][i] * row[0][j],
            )
        )
    equations.extend(
        (
            Equation("t_sum", 0, lambda row: row[2]),
            Equation("t_square", 96, lambda row: row[2] ** 2),
        )
    )
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    for i in range(8):
        equations.append(
            Equation(f"h_{i}", 18 - degrees[i], lambda row, i=i: int(i in row[1]))
        )
        neighbor_sum = 3 * sum(
            SIGNS[j] for j in range(8) if tuple(sorted((i, j))) in H
        )
        equations.append(
            Equation(
                f"ht_{i}",
                neighbor_sum,
                lambda row, i=i: row[2] * int(i in row[1]),
            )
        )
    for i, j in combinations(range(8), 2):
        target = selected_pair_residual_count(D, H, i, j)
        assert target >= 0
        equations.append(
            Equation(
                f"hh_{i}_{j}",
                target,
                lambda row, i=i, j=j: int(i in row[1] and j in row[1]),
            )
        )
    assert len(equations) == 99
    return tuple(equations)


@lru_cache(maxsize=None)
def local_decompositions(
    H: frozenset[tuple[int, int]], row: TriangleType
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]], ...]:
    """All unordered three-point signature rows realizing one triangle type."""
    d, h, t = row
    h_edges = [edge for edge in H if edge[0] in h and edge[1] in h]
    used = {vertex for edge in h_edges for vertex in edge}
    groups = [frozenset(edge) for edge in h_edges]
    groups.extend(frozenset((i,)) for i in sorted(h - used))
    assert len(groups) <= 3
    answer = set()
    allowed_points = set(point_signatures())
    for positions in permutations(range(3), len(groups)):
        negative_position = {
            i: position for group, position in zip(groups, positions) for i in group
        }
        flexible = [i for i in range(8) if i not in h and d[i] in (1, 2)]
        for choices in product(range(3), repeat=len(flexible)):
            signatures = [[0] * 8 for _ in range(3)]
            for i in h:
                negative = negative_position[i]
                for point in range(3):
                    signatures[point][i] = -1 if point == negative else 1
            for i, distinguished in zip(flexible, choices):
                for point in range(3):
                    signatures[point][i] = int(
                        point == distinguished if d[i] == 1 else point != distinguished
                    )
            triple = tuple(sorted(tuple(signature) for signature in signatures))
            if all(signature in allowed_points for signature in triple):
                assert sum(q_value(signature) for signature in triple) == t
                answer.add(triple)
    return tuple(sorted(answer))


def residual_degree(signature: tuple[int, ...]) -> int:
    return 7 - sum(value == -1 for value in signature)


def residual_t_demand(signature: tuple[int, ...]) -> int:
    selected_sum = sum(SIGNS[i] for i, value in enumerate(signature) if value == -1)
    return 3 * q_value(signature) + 3 * selected_sum


def row_names_and_targets(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[tuple[str, int], ...]:
    rows = [(f"aggregate/{equation.name}", equation.target) for equation in aggregate_equations(D, H)]
    rows.extend((f"point/{equation.name}", equation.target) for equation in point_equations(D, H))
    for signature in admissible_point_signatures(H):
        code = signature_code(signature)
        rows.append((f"incidence/{code}", 0))
        rows.append((f"demand/{code}", 0))
    return tuple(rows)


def verify_wave209_survivors() -> dict[str, object]:
    payload = json.loads(WAVE209_POINT_CONTROLS.read_text(encoding="utf-8"))
    assert payload["format"] == "wave209-point-signature-controls-v1"
    assert len(payload["orbits"]) == 24
    forms = tuple(polar_matrix(diagonal) for diagonal in FORM_DIAGONALS)
    assert [len(accepted_intersection_sets(D)) for D in forms] == [83, 83, 83]
    assert all(len(form_maps(source, target)) == 8 for source in forms for target in forms)
    orbits = branch_orbits()
    assert len(orbits) == 24
    assert Counter(map(len, orbits)) == Counter({3: 1, 6: 9, 12: 12, 24: 2})
    assert sum(map(len, orbits)) == 249
    reconstructed_survivors = []
    for orbit_id, (item, orbit) in enumerate(zip(payload["orbits"], orbits)):
        assert item["orbit_id"] == orbit_id
        form_index, H = orbit[0]
        D = polar_matrix(FORM_DIAGONALS[form_index])
        equations = point_equations(D, H)
        if item["kind"] == "control":
            counts = Counter()
            for code, count in item["counts"]:
                assert isinstance(count, int) and count > 0
                counts[decode_signature(code)] += count
            for equation in equations:
                assert sum(count * equation.feature(signature) for signature, count in counts.items()) == equation.target
            reconstructed_survivors.append(orbit_id)
        else:
            assert item["kind"] == "farkas"
            coefficients = [0] * len(equations)
            for index, coefficient in item["coefficients"]:
                coefficients[index] += coefficient
            rhs = sum(coefficient * equation.target for coefficient, equation in zip(coefficients, equations))
            pointwise_minimum = min(
                sum(coefficient * equation.feature(signature) for coefficient, equation in zip(coefficients, equations))
                for signature in point_signatures()
            )
            assert rhs < 0 and pointwise_minimum >= 0
    assert tuple(reconstructed_survivors) == SURVIVOR_ORBITS
    assert sum(len(orbits[index]) for index in reconstructed_survivors) == 51
    for orbit_id in reconstructed_survivors:
        _, H = orbits[orbit_id][0]
        assert not any(
            all(tuple(sorted(edge)) in H for edge in combinations(vertices, 2))
            for vertices in combinations(range(8), 3)
        )
    return {
        "orbit_count": len(orbits),
        "labelled_branch_count": sum(map(len, orbits)),
        "survivor_orbits": reconstructed_survivors,
        "surviving_labelled_branches": 51,
    }


def rename_signature(
    signature: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    answer = [0] * 8
    for i, value in enumerate(signature):
        answer[permutation[i]] = value
    return tuple(answer)


def is_local_decomposition(
    H: frozenset[tuple[int, int]],
    row: TriangleType,
    triple: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
) -> bool:
    d, h, t = row
    if tuple(sorted(triple)) != triple or sum(q_value(signature) for signature in triple) != t:
        return False
    h_edges = [frozenset(edge) for edge in H if edge[0] in h and edge[1] in h]
    used = {vertex for edge in h_edges for vertex in edge}
    expected_memberships = Counter(h_edges)
    expected_memberships.update(frozenset((i,)) for i in h - used)
    actual_memberships = Counter(
        selected_membership(signature)
        for signature in triple
        if selected_membership(signature)
    )
    if actual_memberships != expected_memberships:
        return False
    for i in range(8):
        actual = sorted(signature[i] for signature in triple)
        if i in h:
            expected = [-1, 1, 1]
        else:
            expected = [0] * (3 - d[i]) + [1] * d[i]
        if actual != expected:
            return False
    return True


def verify_coupling_transport() -> dict[str, int]:
    """Replay the variable bijection from each representative to all 51 branches."""
    checked_branches = 0
    checked_local_patterns = 0
    for orbit_id in SURVIVOR_ORBITS:
        orbit = branch_orbits()[orbit_id]
        source_form, source_H = orbit[0]
        source_D = polar_matrix(FORM_DIAGONALS[source_form])
        source_points = admissible_point_signatures(source_H)
        source_types = triangle_types(source_D, source_H)
        for target_form, target_H in orbit:
            target_D = polar_matrix(FORM_DIAGONALS[target_form])
            permutation = next(
                permutation
                for permutation in form_maps(source_D, target_D)
                if rename_H(source_H, permutation) == target_H
            )
            mapped_points = {rename_signature(signature, permutation) for signature in source_points}
            assert mapped_points == set(admissible_point_signatures(target_H))
            for signature in source_points:
                mapped = rename_signature(signature, permutation)
                assert q_value(mapped) == q_value(signature)
                assert residual_degree(mapped) == residual_degree(signature)
                assert residual_t_demand(mapped) == residual_t_demand(signature)

            target_type_set = set(triangle_types(target_D, target_H))
            mapped_type_count = 0
            for row in source_types:
                d, h, t = row
                mapped_d_list = [0] * 8
                for i, value in enumerate(d):
                    mapped_d_list[permutation[i]] = value
                mapped_row = (
                    tuple(mapped_d_list),
                    frozenset(permutation[i] for i in h),
                    t,
                )
                assert mapped_row in target_type_set
                source_decompositions = local_decompositions(source_H, row)
                mapped_decompositions = {
                    tuple(
                        sorted(rename_signature(signature, permutation) for signature in triple)
                    )
                    for triple in source_decompositions
                }
                assert len(mapped_decompositions) == len(source_decompositions)
                assert all(
                    is_local_decomposition(target_H, mapped_row, triple)
                    for triple in mapped_decompositions
                )
                checked_local_patterns += len(source_decompositions)
                mapped_type_count += 1
            assert mapped_type_count == len(target_type_set)
            checked_branches += 1
    assert checked_branches == 51
    return {
        "transported_branch_checks": checked_branches,
        "transported_local_pattern_checks": checked_local_patterns,
    }


def representative_point_counts(orbit_id: int) -> Counter[tuple[int, ...]]:
    payload = json.loads(WAVE209_POINT_CONTROLS.read_text(encoding="utf-8"))
    item = payload["orbits"][orbit_id]
    assert item["orbit_id"] == orbit_id and item["kind"] == "control"
    counts: Counter[tuple[int, ...]] = Counter()
    for code, count in item["counts"]:
        counts[decode_signature(code)] += count
    return counts


def selected_q_triples(
    counts: Counter[tuple[int, ...]],
) -> tuple[tuple[int, int, int], ...]:
    answer = []
    for i in range(8):
        values = []
        for signature, count in counts.items():
            if signature[i] == -1:
                values.extend((q_value(signature),) * count)
        assert len(values) == 3
        answer.append(tuple(sorted(values)))
    return tuple(answer)


def verify_coarse_controls(payload: dict[str, object]) -> list[dict[str, object]]:
    """Replay the deliberately failed 35 q-triple-type relaxation."""
    assert payload["format"] == "wave210-coarse-q-triple-controls-v1"
    all_types = tuple(combinations_with_replacement(range(-2, 3), 3))
    assert len(all_types) == 35
    allowed_residual_types = {triple for triple in all_types if abs(sum(triple)) <= 2}
    assert len(allowed_residual_types) == 21
    summaries = []
    for item in payload["orbits"]:
        orbit_id = item["orbit_id"]
        assert orbit_id in SURVIVOR_ORBITS
        point_counts = representative_point_counts(orbit_id)
        q_profile = Counter()
        for signature, count in point_counts.items():
            q_profile[q_value(signature)] += count
        selected = selected_q_triples(point_counts)
        assert [list(triple) for triple in selected] == item["selected_q_triples"]
        for i, triple in enumerate(selected):
            assert sum(triple) == -3 * SIGNS[i]

        residual_counts: Counter[tuple[int, int, int]] = Counter()
        for triple_values, count in item["residual_counts"]:
            triple = tuple(triple_values)
            assert triple in allowed_residual_types
            assert isinstance(count, int) and count > 0
            residual_counts[triple] += count
        assert len(residual_counts) == len(item["residual_counts"])
        assert sum(residual_counts.values()) == 223
        for value in range(-2, 3):
            selected_occurrences = sum(triple.count(value) for triple in selected)
            residual_occurrences = sum(
                count * triple.count(value) for triple, count in residual_counts.items()
            )
            assert selected_occurrences + residual_occurrences == 7 * q_profile[value]
        assert sum(count * sum(triple) for triple, count in residual_counts.items()) == 0
        assert sum(count * sum(triple) ** 2 for triple, count in residual_counts.items()) == 96
        summaries.append(
            {
                "orbit_id": orbit_id,
                "selected_q_triples": [list(triple) for triple in selected],
                "residual_nonzero_types": len(residual_counts),
            }
        )
    assert [item["orbit_id"] for item in summaries] == list(SURVIVOR_ORBITS)
    return summaries


def generate_coarse_controls() -> dict[str, object]:
    """Discovery helper for positive controls; exact replay follows."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp

    residual_types = tuple(
        triple
        for triple in combinations_with_replacement(range(-2, 3), 3)
        if abs(sum(triple)) <= 2
    )
    output = []
    for orbit_id in SURVIVOR_ORBITS:
        point_counts = representative_point_counts(orbit_id)
        q_profile = Counter()
        for signature, count in point_counts.items():
            q_profile[q_value(signature)] += count
        selected = selected_q_triples(point_counts)
        equations = [[1] * len(residual_types)]
        targets = [223]
        for value in range(-2, 3):
            equations.append([triple.count(value) for triple in residual_types])
            targets.append(
                7 * q_profile[value] - sum(triple.count(value) for triple in selected)
            )
        equations.append([sum(triple) for triple in residual_types])
        targets.append(0)
        equations.append([sum(triple) ** 2 for triple in residual_types])
        targets.append(96)
        matrix = np.asarray(equations, dtype=float)
        target = np.asarray(targets, dtype=float)
        candidate = milp(
            np.zeros(len(residual_types)),
            integrality=np.ones(len(residual_types)),
            bounds=Bounds(np.zeros(len(residual_types)), np.full(len(residual_types), np.inf)),
            constraints=LinearConstraint(matrix, target, target),
        )
        if candidate.x is None:
            raise RuntimeError(f"orbit {orbit_id}: missing coarse positive control")
        rounded = np.rint(candidate.x).astype(int)
        assert np.max(np.abs(matrix @ rounded - target)) == 0
        output.append(
            {
                "orbit_id": orbit_id,
                "selected_q_triples": [list(triple) for triple in selected],
                "residual_counts": [
                    [list(triple), int(count)]
                    for triple, count in zip(residual_types, rounded)
                    if count
                ],
            }
        )
    payload = {"format": "wave210-coarse-q-triple-controls-v1", "orbits": output}
    COARSE_CONTROLS.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    verify_coarse_controls(payload)
    return payload


def certificate_metrics(
    orbit_id: int, sparse_coefficients: list[list[object]]
) -> dict[str, int]:
    orbit = branch_orbits()[orbit_id]
    form_index, H = orbit[0]
    D = polar_matrix(FORM_DIAGONALS[form_index])
    rows = row_names_and_targets(D, H)
    allowed_names = {name for name, _ in rows}
    coefficients: dict[str, int] = {}
    for name, coefficient in sparse_coefficients:
        assert name in allowed_names
        assert isinstance(coefficient, int) and coefficient
        assert name not in coefficients
        coefficients[name] = coefficient
    rhs = sum(coefficients.get(name, 0) * target for name, target in rows)

    aggregate = aggregate_equations(D, H)
    pattern_minimum: int | None = None
    pattern_count = 0
    type_count = 0
    for row in triangle_types(D, H):
        decompositions = local_decompositions(H, row)
        if not decompositions:
            continue
        type_count += 1
        base = sum(
            coefficients.get(f"aggregate/{equation.name}", 0) * equation.feature(row)
            for equation in aggregate
        )
        for triple in decompositions:
            score = base
            for signature, multiplicity in Counter(triple).items():
                code = signature_code(signature)
                score += multiplicity * coefficients.get(f"incidence/{code}", 0)
                score += multiplicity * row[2] * coefficients.get(f"demand/{code}", 0)
            pattern_minimum = score if pattern_minimum is None else min(pattern_minimum, score)
            pattern_count += 1
    assert pattern_minimum is not None

    point_minimum: int | None = None
    point_equation_rows = point_equations(D, H)
    for signature in admissible_point_signatures(H):
        code = signature_code(signature)
        score = sum(
            coefficients.get(f"point/{equation.name}", 0) * equation.feature(signature)
            for equation in point_equation_rows
        )
        score -= residual_degree(signature) * coefficients.get(f"incidence/{code}", 0)
        score -= residual_t_demand(signature) * coefficients.get(f"demand/{code}", 0)
        point_minimum = score if point_minimum is None else min(point_minimum, score)
    assert point_minimum is not None
    assert rhs < 0
    assert pattern_minimum >= 0
    assert point_minimum >= 0
    return {
        "rhs": rhs,
        "pattern_minimum": pattern_minimum,
        "point_minimum": point_minimum,
        "local_pattern_count": pattern_count,
        "realizable_triangle_type_count": type_count,
        "nonzero_coefficients": len(coefficients),
    }


def verify_certificates(payload: dict[str, object]) -> list[dict[str, object]]:
    assert payload["format"] == "wave210-rank4-point-line-farkas-v1"
    rows = payload["orbits"]
    assert [item["orbit_id"] for item in rows] == list(SURVIVOR_ORBITS)
    summaries = []
    for item in rows:
        orbit_id = item["orbit_id"]
        metrics = certificate_metrics(orbit_id, item["coefficients"])
        summaries.append(
            {
                "orbit_id": orbit_id,
                "labelled_branches": len(branch_orbits()[orbit_id]),
                **metrics,
            }
        )
    assert sum(item["labelled_branches"] for item in summaries) == 51
    return summaries


def build_sparse_system(orbit_id: int):
    """Generation-only SciPy matrix, with exact metadata retained separately."""
    import numpy as np
    from scipy.sparse import coo_matrix

    form_index, H = branch_orbits()[orbit_id][0]
    D = polar_matrix(FORM_DIAGONALS[form_index])
    patterns = [
        (row, triple)
        for row in triangle_types(D, H)
        for triple in local_decompositions(H, row)
    ]
    signatures = admissible_point_signatures(H)
    signature_index = {signature: index for index, signature in enumerate(signatures)}
    row_metadata = row_names_and_targets(D, H)
    row_index = {name: index for index, (name, _) in enumerate(row_metadata)}
    pattern_count = len(patterns)
    entries_r: list[int] = []
    entries_c: list[int] = []
    entries_v: list[int] = []

    def add(row_name: str, column: int, value: int) -> None:
        if value:
            entries_r.append(row_index[row_name])
            entries_c.append(column)
            entries_v.append(value)

    for column, (row, triple) in enumerate(patterns):
        for equation in aggregate_equations(D, H):
            add(f"aggregate/{equation.name}", column, equation.feature(row))
        for signature, multiplicity in Counter(triple).items():
            code = signature_code(signature)
            add(f"incidence/{code}", column, multiplicity)
            add(f"demand/{code}", column, multiplicity * row[2])

    for index, signature in enumerate(signatures):
        column = pattern_count + index
        for equation in point_equations(D, H):
            add(f"point/{equation.name}", column, equation.feature(signature))
        code = signature_code(signature)
        add(f"incidence/{code}", column, -residual_degree(signature))
        add(f"demand/{code}", column, -residual_t_demand(signature))

    matrix = coo_matrix(
        (entries_v, (entries_r, entries_c)),
        shape=(len(row_metadata), pattern_count + len(signatures)),
        dtype=float,
    ).tocsr()
    targets = np.asarray([target for _, target in row_metadata], dtype=float)
    return row_metadata, patterns, matrix, targets


def rationalize_candidate(
    orbit_id: int, candidate, row_metadata: tuple[tuple[str, int], ...]
) -> list[list[object]]:
    for denominator_limit in (100, 1_000, 10_000, 1_000_000):
        fractions = [
            Fraction(float(value)).limit_denominator(denominator_limit)
            for value in candidate
        ]
        scale = 1
        for value in fractions:
            scale = lcm(scale, value.denominator)
        integers = [value.numerator * (scale // value.denominator) for value in fractions]
        common = 0
        for value in integers:
            common = gcd(common, abs(value))
        if common:
            integers = [value // common for value in integers]
        sparse = [[name, value] for (name, _), value in zip(row_metadata, integers) if value]
        try:
            certificate_metrics(orbit_id, sparse)
        except AssertionError:
            continue
        return sparse
    raise RuntimeError(f"orbit {orbit_id}: numerical ray did not rationalize exactly")


def generation_row_ids(
    orbit_id: int,
    row_metadata: tuple[tuple[str, int], ...],
    H: frozenset[tuple[int, int]],
) -> list[int]:
    """A proved relaxation chosen before dual generation for each orbit class."""
    selected_codes = {
        signature_code(signature)
        for signature in admissible_point_signatures(H)
        if selected_membership(signature)
    }
    answer = []
    for index, (name, _) in enumerate(row_metadata):
        take = False
        if orbit_id in (0, 2, 12, 23):
            if name.startswith(("aggregate/h_", "aggregate/hh_", "aggregate/ht_")):
                take = True
            elif name.startswith("point/m_"):
                take = name.endswith("_-1")
            elif name.startswith("point/p_"):
                fields = name.split("_")
                take = int(fields[-2]) == -1 or int(fields[-1]) == -1
            elif name.startswith(("incidence/", "demand/")):
                take = int(name.split("/")[1]) in selected_codes
        else:
            if name == "aggregate/total" or name.startswith(
                (
                    "aggregate/d_",
                    "aggregate/h_",
                    "aggregate/hh_",
                    "aggregate/ht_",
                )
            ) or name in ("aggregate/t_sum", "aggregate/t_square"):
                take = True
            elif name in ("point/total", "point/q_sum", "point/q_square"):
                take = True
            elif orbit_id == 14 and name.startswith("point/p_"):
                take = True
            elif name.startswith(("incidence/", "demand/")):
                take = True
        if take:
            answer.append(index)
    return answer


def generate_certificates() -> dict[str, object]:
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, hstack, vstack

    output = []
    for orbit_id in SURVIVOR_ORBITS:
        print(f"building orbit {orbit_id}", flush=True)
        row_metadata, patterns, matrix, targets = build_sparse_system(orbit_id)
        form_index, H = branch_orbits()[orbit_id][0]
        del form_index, patterns
        selected_rows = generation_row_ids(orbit_id, row_metadata, H)
        reduced_matrix = matrix[selected_rows]
        reduced_targets = targets[selected_rows]
        reduced_metadata = tuple(row_metadata[index] for index in selected_rows)
        row_count = len(selected_rows)

        # Discovery helper: find a low-L1 dual candidate.  The floating result
        # is discarded unless rationalization passes the full exact replay.
        inequalities = vstack(
            (
                hstack((-reduced_matrix.T, reduced_matrix.T), format="csr"),
                csr_matrix(
                    np.concatenate((reduced_targets, -reduced_targets)).reshape(1, -1)
                ),
            ),
            format="csr",
        )
        bounds = np.concatenate((np.zeros(reduced_matrix.shape[1]), np.asarray((-1.0,))))
        result = linprog(
            np.ones(2 * row_count),
            A_ub=inequalities,
            b_ub=bounds,
            bounds=(0, None),
            method="highs",
        )
        if result.x is None:
            raise RuntimeError(f"orbit {orbit_id}: dual candidate generation failed")
        candidate = result.x[:row_count] - result.x[row_count:]
        coefficients = rationalize_candidate(orbit_id, candidate, reduced_metadata)
        metrics = certificate_metrics(orbit_id, coefficients)
        print(f"orbit {orbit_id}: {metrics}", flush=True)
        output.append({"orbit_id": orbit_id, "coefficients": coefficients})
    payload = {"format": "wave210-rank4-point-line-farkas-v1", "orbits": output}
    CERTIFICATES.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def build_results(
    certificate_payload: dict[str, object], coarse_payload: dict[str, object]
) -> dict[str, object]:
    reconstructed = verify_wave209_survivors()
    transport = verify_coupling_transport()
    certificate_summaries = verify_certificates(certificate_payload)
    coarse_summaries = verify_coarse_controls(coarse_payload)
    equation_counts = {}
    admissible_counts = {}
    for orbit_id in SURVIVOR_ORBITS:
        form_index, H = branch_orbits()[orbit_id][0]
        D = polar_matrix(FORM_DIAGONALS[form_index])
        equation_counts[str(orbit_id)] = len(row_names_and_targets(D, H))
        admissible_counts[str(orbit_id)] = len(admissible_point_signatures(H))
    return {
        "claim_label": "DERIVED",
        "conditional_scope": "the 51 independently reconstructed Wave209 rank-four branches under the frozen hypothetical endpoint",
        "frozen_input_hashes": FROZEN_HASHES,
        "wave209_reconstruction": reconstructed,
        "local_coupling": {
            "integral_point_signature_count_before_membership_filter": len(point_signatures()),
            "admissible_point_signature_counts": admissible_counts,
            "equation_counts": equation_counts,
            "certificate_summaries": certificate_summaries,
            "constraint_transport": transport,
            "excluded_constraint_orbits": len(certificate_summaries),
            "excluded_labelled_branches": sum(item["labelled_branches"] for item in certificate_summaries),
            "certificate_logic": "for z>=0 and Az=b, each integer y has A^T y>=0 but b^T y<0",
        },
        "failed_coarse_relaxation": {
            "possible_unordered_q_triples": 35,
            "residual_types_after_abs_t_at_most_2": 21,
            "positive_control_orbits": len(coarse_summaries),
            "summaries": coarse_summaries,
            "warning": "these controls couple only q-value multiplicities to triangle sums; they are not 99 points, 223 residual triangles, or a graph",
        },
        "status": "DERIVED",
        "limitations": [
            "The exclusions are conditional on the Wave208/209 rank-four reduction and frozen endpoint assumptions.",
            "This proof agent does not promote its own certificates to VERIFIED.",
            "The rank-three branch and the global Conway-99 target are untouched and remain UNKNOWN.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    check_frozen_inputs()
    if args.generate:
        payload = generate_certificates()
        coarse_payload = generate_coarse_controls()
    else:
        payload = json.loads(CERTIFICATES.read_text(encoding="utf-8"))
        coarse_payload = json.loads(COARSE_CONTROLS.read_text(encoding="utf-8"))
    result = build_results(payload, coarse_payload)
    if args.generate:
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
