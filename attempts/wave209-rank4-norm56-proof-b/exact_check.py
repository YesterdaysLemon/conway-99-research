#!/usr/bin/env python3
"""Exact Wave 209 rank-four/norm-56 reduction and control checker.

The default path uses only the Python standard library and verifies archived
integer aggregate controls.  ``--generate-controls`` is a discovery helper;
it imports SciPy/HiGHS, writes a mechanically generated JSON artifact, and
then subjects the rounded output to the same exact checks as the default
path.  Solver status is never treated as a certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd, lcm
from pathlib import Path
from typing import Callable, Iterable

Q = 3
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTROLS = HERE / "aggregate-controls.json"
POINT_CONTROLS = HERE / "point-signature-controls.json"
RESULTS = HERE / "exact-results.json"

PROTOCOL = ROOT / "attempts" / "wave209-four-survivor-globalization" / "protocol.md"
WAVE208_MANIFEST = ROOT / "attempts" / "wave208-marked-m7g-proof-b" / "package-manifest.sha256"
WAVE66_MANIFEST = ROOT / "verification" / "wave66-spherical-code-shift" / "package-manifest.sha256"

EXPECTED_INPUT_HASHES = {
    str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"): "3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196",
    str(WAVE208_MANIFEST.relative_to(ROOT)).replace("\\", "/"): "f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc",
    str(WAVE66_MANIFEST.relative_to(ROOT)).replace("\\", "/"): "a6051ebcfccab0fc9b3f9698f0024cc3284549f5148c9a12a4c6bbE08c786486".lower(),
}

FORM_DIAGONALS = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
ALLOWED_POINT_WEIGHTS = {14, 17, 20, 23}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def columns() -> tuple[tuple[int, int, int, int], ...]:
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


def restricted_form(diagonal: tuple[int, int, int]) -> list[list[int]]:
    d1, d2, d3 = diagonal
    alpha = (d1 + d2 + d3) % Q
    return [
        [alpha, 0, 0, 0],
        [0, d1, (-alpha - d3) % Q, (-alpha - d2) % Q],
        [0, (-alpha - d3) % Q, d2, (-alpha - d1) % Q],
        [0, (-alpha - d2) % Q, (-alpha - d1) % Q, d3],
    ]


@lru_cache(maxsize=None)
def gram(diagonal: tuple[int, int, int]) -> tuple[tuple[int, ...], ...]:
    vectors = columns()
    bilinear = restricted_form(diagonal)
    return tuple(
        tuple(
            sum(
                vectors[i][r] * bilinear[r][s] * vectors[j][s]
                for r in range(4)
                for s in range(4)
            )
            % Q
            for j in range(8)
        )
        for i in range(8)
    )


def rank_q(matrix: Iterable[Iterable[int | Fraction]]) -> int:
    work = [[Fraction(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                work[row][j] - scale * work[rank][j]
                for j in range(len(work[0]))
            ]
        rank += 1
    return rank


def selected_f_matrix(D: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    """F=B^T(A-3I)B on selected coordinates: diagonal -3, off-diagonal D."""
    return tuple(
        tuple(-3 if i == j else D[i][j] for j in range(8))
        for i in range(8)
    )


@lru_cache(maxsize=None)
def accepted_subsets(D: tuple[tuple[int, ...], ...]) -> tuple[frozenset[tuple[int, int]], ...]:
    ones = tuple((i, j) for i, j in combinations(range(8), 2) if D[i][j] == 1)
    accepted: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(ones)):
        H = frozenset(edge for bit, edge in enumerate(ones) if mask & (1 << bit))
        if sum(SIGNS[i] * SIGNS[j] for i, j in H) % Q != 1:
            continue
        degrees = [0] * 8
        for i, j in H:
            degrees[i] += 1
            degrees[j] += 1
        values = [SIGNS[i] + SIGNS[j] for i, j in H]
        values.extend(SIGNS[i] for i in range(8) for _ in range(3 - degrees[i]))
        canonical = [value % Q for value in values]
        weight = sum(value != 0 for value in canonical)
        if weight not in ALLOWED_POINT_WEIGHTS:
            continue
        if weight == 14 and (canonical.count(1), canonical.count(2)) != (7, 7):
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


def map_subset(
    H: frozenset[tuple[int, int]], permutation: tuple[int, ...]
) -> frozenset[tuple[int, int]]:
    return frozenset(
        tuple(sorted((permutation[i], permutation[j])))
        for i, j in H
    )


@lru_cache(maxsize=None)
def branch_orbits() -> tuple[
    tuple[tuple[int, frozenset[tuple[int, int]]], ...], ...
]:
    forms = tuple(gram(diagonal) for diagonal in FORM_DIAGONALS)
    subsets = tuple(accepted_subsets(D) for D in forms)
    nodes = {(form_index, H) for form_index in range(3) for H in subsets[form_index]}
    maps = {
        (source, target): form_maps(forms[source], forms[target])
        for source in range(3)
        for target in range(3)
    }
    unseen = set(nodes)
    orbits = []
    while unseen:
        seed = min(unseen, key=lambda node: (node[0], sorted(node[1])))
        frontier = [seed]
        orbit: set[tuple[int, frozenset[tuple[int, int]]]] = set()
        while frontier:
            form_index, H = frontier.pop()
            if (form_index, H) in orbit:
                continue
            orbit.add((form_index, H))
            for target in range(3):
                for permutation in maps[(form_index, target)]:
                    image = (target, map_subset(H, permutation))
                    if image in nodes and image not in orbit:
                        frontier.append(image)
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit, key=lambda node: (node[0], sorted(node[1])))))
    return tuple(orbits)


@lru_cache(maxsize=None)
def signatures(D: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    values = {
        tuple(
            sum(coefficients[k] * D[k][i] for k in range(8)) % Q
            for i in range(8)
        )
        for coefficients in product(range(Q), repeat=8)
    }
    assert len(values) == 81
    return tuple(sorted(values))


TypeRow = tuple[tuple[int, ...], frozenset[int], int]


@lru_cache(maxsize=None)
def aggregate_types(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[TypeRow, ...]:
    rows: list[TypeRow] = []
    for d in signatures(D):
        one_coordinates = tuple(i for i, value in enumerate(d) if value == 1)
        for mask in range(1 << len(one_coordinates)):
            h = frozenset(
                one_coordinates[bit]
                for bit in range(len(one_coordinates))
                if mask & (1 << bit)
            )
            h_degrees = {i: 0 for i in h}
            h_edges = 0
            allowed = True
            for i, j in combinations(sorted(h), 2):
                if (i, j) in H:
                    h_degrees[i] += 1
                    h_degrees[j] += 1
                    h_edges += 1
                    if h_degrees[i] > 1 or h_degrees[j] > 1:
                        allowed = False
                        break
                elif D[i][j] == 0:
                    allowed = False
                    break
            # Each residual triangle has three points.  An H-edge in h uses
            # one common point; all remaining selected intersections use one
            # point apiece.
            if not allowed or len(h) - h_edges > 3:
                continue
            numerator = sum(SIGNS[i] * d[i] for i in range(8))
            assert numerator % 3 == 0
            rows.append((d, h, numerator // 3))
    return tuple(rows)


def pair_residual_intersection_count(
    D: tuple[tuple[int, ...], ...],
    H: frozenset[tuple[int, int]],
    i: int,
    j: int,
) -> int:
    if (i, j) in H:
        # Seven blocks pass through the common point; remove the two selected.
        return 5
    common_selected = sum(
        tuple(sorted((i, k))) in H and tuple(sorted((j, k))) in H
        for k in range(8)
        if k not in (i, j)
    )
    # A disjoint pair has D_ij cross edges.  Each gives its unique block;
    # selected common-neighbor blocks have already consumed that many edges.
    return D[i][j] - common_selected


@lru_cache(maxsize=None)
def constraint_system(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[tuple[TypeRow, ...], tuple[tuple[str, int, Callable[[TypeRow], int]], ...]]:
    rows = aggregate_types(D, H)
    equations: list[tuple[str, int, Callable[[TypeRow], int]]] = []

    equations.append(("total", 223, lambda row: 1))
    for i in range(8):
        for value, full_off_diagonal in ((0, 32), (1, 162), (2, 36)):
            selected = sum(D[k][i] == value for k in range(8) if k != i)
            equations.append(
                (
                    f"d_{i}_{value}",
                    full_off_diagonal - selected,
                    lambda row, i=i, value=value: int(row[0][i] == value),
                )
            )

    F = selected_f_matrix(D)
    for i, j in combinations(range(8), 2):
        full = 252 - 21 * D[i][j]  # (F^2)_ij from F^2=-21F+252J.
        selected = sum(F[k][i] * F[k][j] for k in range(8))
        equations.append(
            (
                f"dprod_{i}_{j}",
                full - selected,
                lambda row, i=i, j=j: row[0][i] * row[0][j],
            )
        )

    equations.extend(
        (
            ("t_sum", 0, lambda row: row[2]),
            ("t_square", 96, lambda row: row[2] * row[2]),
        )
    )
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    for i in range(8):
        equations.append(
            (f"h_{i}", 18 - degrees[i], lambda row, i=i: int(i in row[1]))
        )
        marked_neighbor_sum = 3 * sum(
            SIGNS[j]
            for j in range(8)
            if tuple(sorted((i, j))) in H
        )
        equations.append(
            (
                f"ht_{i}",
                marked_neighbor_sum,
                lambda row, i=i: row[2] * int(i in row[1]),
            )
        )
    for i, j in combinations(range(8), 2):
        target = pair_residual_intersection_count(D, H, i, j)
        assert target >= 0
        equations.append(
            (
                f"hh_{i}_{j}",
                target,
                lambda row, i=i, j=j: int(i in row[1] and j in row[1]),
            )
        )
    return rows, tuple(equations)


def type_key(row: TypeRow) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return row[0], tuple(sorted(row[1]))


def encode_type(row: TypeRow) -> tuple[int, int]:
    d_code = sum(value * (3**i) for i, value in enumerate(row[0]))
    h_mask = sum(1 << i for i in row[1])
    return d_code, h_mask


def decode_type(d_code: int, h_mask: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    d = []
    value = d_code
    for _ in range(8):
        d.append(value % 3)
        value //= 3
    assert value == 0
    h = tuple(i for i in range(8) if h_mask & (1 << i))
    assert h_mask >> 8 == 0
    return tuple(d), h


def verify_control(
    control: dict[str, object],
    orbit: tuple[tuple[int, frozenset[tuple[int, int]]], ...],
) -> dict[str, object]:
    form_index, H = orbit[0]
    diagonal = FORM_DIAGONALS[form_index]
    assert control["form_diagonal"] == list(diagonal)
    assert control["selected_intersections"] == [list(edge) for edge in sorted(H)]
    assert control["branch_count"] == len(orbit)
    D = gram(diagonal)
    allowed_rows, equations = constraint_system(D, H)
    allowed = {type_key(row): row for row in allowed_rows}
    counts: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    for item in control["counts"]:  # type: ignore[index]
        assert isinstance(item, list) and len(item) == 3
        d_code, h_mask, count = item
        assert isinstance(d_code, int) and isinstance(h_mask, int)
        key = decode_type(d_code, h_mask)
        assert isinstance(count, int) and count > 0
        assert key in allowed
        counts[key] += count
    assert len(counts) == len(control["counts"])  # type: ignore[arg-type]
    def check_equations(
        target_D: tuple[tuple[int, ...], ...],
        target_H: frozenset[tuple[int, int]],
        target_counts: Counter[tuple[tuple[int, ...], tuple[int, ...]]],
    ) -> None:
        target_rows, target_equations = constraint_system(target_D, target_H)
        target_allowed = {type_key(row): row for row in target_rows}
        assert set(target_counts) <= set(target_allowed)
        for name, target, feature in target_equations:
            actual = sum(
                count * feature(target_allowed[key])
                for key, count in target_counts.items()
            )
            assert actual == target, (name, target, actual)

    check_equations(D, H, counts)

    transported_checks = 0
    for target_form_index, target_H in orbit:
        target_D = gram(FORM_DIAGONALS[target_form_index])
        permutation = next(
            permutation
            for permutation in form_maps(D, target_D)
            if map_subset(H, permutation) == target_H
        )
        transported: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
        for (d, h), count in counts.items():
            target_d = [0] * 8
            for i in range(8):
                target_d[permutation[i]] = d[i]
            target_h = tuple(sorted(permutation[i] for i in h))
            transported[(tuple(target_d), target_h)] += count
        check_equations(target_D, target_H, transported)
        transported_checks += 1

    t_counts: Counter[int] = Counter()
    h_size_counts: Counter[int] = Counter()
    for key, count in counts.items():
        row = allowed[key]
        t_counts[row[2]] += count
        h_size_counts[len(row[1])] += count
    assert set(t_counts).issubset({-2, -1, 0, 1, 2})
    return {
        "orbit_size": len(orbit),
        "transported_branch_checks": transported_checks,
        "allowed_type_count": len(allowed_rows),
        "nonzero_type_count": len(counts),
        "residual_t_counts": {str(value): t_counts[value] for value in range(-2, 3)},
        "residual_h_size_counts": {
            str(value): h_size_counts[value] for value in sorted(h_size_counts)
        },
    }


def solve_control(
    orbit_id: int,
    orbit: tuple[tuple[int, frozenset[tuple[int, int]]], ...],
) -> dict[str, object]:
    """Find one integer aggregate control; exact verification follows."""
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
        from scipy.sparse import csr_matrix
    except ImportError as exc:  # pragma: no cover - generation-only guard
        raise RuntimeError("control generation requires the repository SciPy environment") from exc

    form_index, H = orbit[0]
    diagonal = FORM_DIAGONALS[form_index]
    rows, equations = constraint_system(gram(diagonal), H)
    matrix = csr_matrix(
        np.asarray([[feature(row) for row in rows] for _, _, feature in equations], dtype=float)
    )
    targets = np.asarray([target for _, target, _ in equations], dtype=float)
    result = milp(
        np.zeros(len(rows)),
        integrality=np.ones(len(rows)),
        bounds=Bounds(np.zeros(len(rows)), np.full(len(rows), np.inf)),
        constraints=LinearConstraint(matrix, targets, targets),
        options={"time_limit": 120, "mip_rel_gap": 0},
    )
    if result.x is None:
        raise RuntimeError(f"orbit {orbit_id}: no candidate aggregate control: {result.message}")
    rounded = np.rint(result.x).astype(int)
    if np.max(np.abs(matrix @ rounded - targets)) != 0:
        raise RuntimeError(f"orbit {orbit_id}: rounded candidate failed exact integer residual test")
    nonzero = [
        [*encode_type(row), int(count)]
        for row, count in zip(rows, rounded)
        if count
    ]
    return {
        "orbit_id": orbit_id,
        "form_diagonal": list(diagonal),
        "selected_intersections": [list(edge) for edge in sorted(H)],
        "branch_count": len(orbit),
        "counts": nonzero,
    }


def generate_controls() -> dict[str, object]:
    orbits = branch_orbits()
    controls = []
    for orbit_id, orbit in enumerate(orbits):
        print(f"generating aggregate control {orbit_id + 1}/{len(orbits)}", flush=True)
        controls.append(solve_control(orbit_id, orbit))
    payload = {
        "format": "wave209-rank4-aggregate-controls-v2",
        "scope": "integer aggregate signature/intersection controls, not residual blocks or a graph",
        "controls": controls,
    }
    CONTROLS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def point_coordinate_profiles() -> tuple[int, Counter[int]]:
    """Enumerate q-value count profiles after |q_x|<=4, sum 0, norm 56."""
    nonzero_values = (-4, -3, -2, -1, 1, 2, 3, 4)
    profiles: list[tuple[tuple[int, ...], int]] = []

    def visit(index: int, used: int, total: int, square: int, counts: list[int]) -> None:
        if index == len(nonzero_values):
            if total or square != 56 or used > 99:
                return
            by_value = dict(zip(nonzero_values, counts))
            row = tuple(by_value.get(value, 99 - used if value == 0 else 0) for value in range(-4, 5))
            odd_weight = sum(row[value + 4] for value in (-3, -1, 1, 3))
            profiles.append((row, odd_weight))
            return
        value = nonzero_values[index]
        for count in range(min(99 - used, (56 - square) // (value * value)) + 1):
            visit(
                index + 1,
                used + count,
                total + value * count,
                square + value * value * count,
                counts + [count],
            )

    visit(0, 0, 0, 0, [])
    admissible = Counter(weight for _, weight in profiles if weight >= 8)
    return len(profiles), admissible


@lru_cache(maxsize=None)
def best_private_split(count: int, target: int) -> tuple[int, tuple[int, ...]] | None:
    candidates = [
        (sum(value * value for value in values), values)
        for values in product(range(-4, 5), repeat=count)
        if sum(values) == target
    ]
    return min(candidates) if candidates else None


def selected_union_control(
    H: frozenset[tuple[int, int]],
) -> tuple[int, tuple[tuple[tuple[int, ...], int], ...]]:
    """Minimum selected-union norm under U^Tq=-3*alpha and |q_x|<=4.

    H is triangle-free, so every selected intersection edge is one distinct
    point and all other selected points are private.  Connected components
    of H are independent convex integer minimizations; each has at most the
    four edges of one ambient C4.
    """
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    unseen = {i for edge in H for i in edge}
    components: list[tuple[set[int], tuple[tuple[int, int], ...]]] = []
    while unseen:
        seed = min(unseen)
        vertices = {seed}
        changed = True
        while changed:
            changed = False
            for i, j in H:
                if i in vertices or j in vertices:
                    before = len(vertices)
                    vertices.update((i, j))
                    changed |= len(vertices) != before
        unseen.difference_update(vertices)
        components.append((vertices, tuple(sorted(edge for edge in H if set(edge) <= vertices))))

    witness: list[tuple[tuple[int, ...], int]] = []
    total_norm = 0
    covered = set()
    for vertices, edges in components:
        best: tuple[int, tuple[int, ...], tuple[tuple[tuple[int, ...], int], ...]] | None = None
        for edge_values in product(range(-4, 5), repeat=len(edges)):
            incident = {i: 0 for i in vertices}
            for edge, value in zip(edges, edge_values):
                incident[edge[0]] += value
                incident[edge[1]] += value
            private_rows = []
            private_norm = 0
            allowed = True
            for i in sorted(vertices):
                split = best_private_split(3 - degrees[i], -3 * SIGNS[i] - incident[i])
                if split is None:
                    allowed = False
                    break
                norm, values = split
                private_norm += norm
                private_rows.extend(((i,), value) for value in values)
            if not allowed:
                continue
            rows = tuple((edge, value) for edge, value in zip(edges, edge_values)) + tuple(private_rows)
            score = sum(value * value for value in edge_values) + private_norm
            candidate = (score, edge_values, rows)
            if best is None or candidate < best:
                best = candidate
        assert best is not None
        total_norm += best[0]
        witness.extend(best[2])
        covered.update(vertices)

    for i in range(8):
        if i in covered:
            continue
        split = best_private_split(3, -3 * SIGNS[i])
        assert split is not None
        total_norm += split[0]
        witness.extend(((i,), value) for value in split[1])

    line_sums = [0] * 8
    for membership, value in witness:
        for i in membership:
            line_sums[i] += value
    assert line_sums == [-3 * sign for sign in SIGNS]
    assert total_norm == sum(value * value for _, value in witness)
    assert all(-4 <= value <= 4 for _, value in witness)
    return total_norm, tuple(witness)


@lru_cache(maxsize=None)
def point_signatures() -> tuple[tuple[int, ...], ...]:
    """All point signatures compatible with coordinatewise divisibility by 3."""
    values = tuple(
        signature
        for signature in product((-1, 0, 1), repeat=8)
        if sum(SIGNS[i] * signature[i] for i in range(8)) % 3 == 0
    )
    assert len(values) == 2187
    return values


def point_signature_code(signature: tuple[int, ...]) -> int:
    return sum((value + 1) * (3**i) for i, value in enumerate(signature))


def decode_point_signature(code: int) -> tuple[int, ...]:
    values = []
    for _ in range(8):
        values.append(code % 3 - 1)
        code //= 3
    assert code == 0
    return tuple(values)


def point_pair_table(
    D: tuple[tuple[int, ...], ...],
    H: frozenset[tuple[int, int]],
    i: int,
    j: int,
) -> dict[tuple[int, int], int]:
    """Exact joint counts for the two {-1,0,+1} point signatures."""
    if (i, j) in H:
        return {
            (-1, -1): 1, (-1, 0): 0, (-1, 1): 2,
            (0, -1): 0, (0, 0): 40, (0, 1): 20,
            (1, -1): 2, (1, 0): 20, (1, 1): 14,
        }
    d = D[i][j]
    return {
        (-1, -1): 0, (-1, 0): 3 - d, (-1, 1): d,
        (0, -1): 3 - d, (0, 0): 39 - 3 * d, (0, 1): 18 + 4 * d,
        (1, -1): d, (1, 0): 18 + 4 * d, (1, 1): 18 - 5 * d,
    }


@lru_cache(maxsize=None)
def point_constraint_system(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[str, int, Callable[[tuple[int, ...]], int]], ...],
]:
    signatures = point_signatures()
    equations: list[tuple[str, int, Callable[[tuple[int, ...]], int]]] = [
        ("total", 99, lambda signature: 1)
    ]
    for i in range(8):
        for value, target in ((-1, 3), (0, 60), (1, 36)):
            equations.append(
                (
                    f"m_{i}_{value}",
                    target,
                    lambda signature, i=i, value=value: int(signature[i] == value),
                )
            )
    for i, j in combinations(range(8), 2):
        table = point_pair_table(D, H, i, j)
        for left in (-1, 0, 1):
            for right in (-1, 0, 1):
                equations.append(
                    (
                        f"p_{i}_{j}_{left}_{right}",
                        table[(left, right)],
                        lambda signature, i=i, j=j, left=left, right=right: int(
                            signature[i] == left and signature[j] == right
                        ),
                    )
                )

    def q_value(signature: tuple[int, ...]) -> int:
        numerator = sum(SIGNS[i] * signature[i] for i in range(8))
        assert numerator % 3 == 0
        return numerator // 3

    equations.append(("q_sum", 0, q_value))
    equations.append(("q_square", 56, lambda signature: q_value(signature) ** 2))
    assert len(equations) == 279
    return signatures, tuple(equations)


def exact_point_control_check(
    D: tuple[tuple[int, ...], ...],
    H: frozenset[tuple[int, int]],
    counts: Counter[tuple[int, ...]],
) -> Counter[int]:
    signatures, equations = point_constraint_system(D, H)
    allowed = set(signatures)
    assert set(counts) <= allowed
    for name, target, feature in equations:
        actual = sum(count * feature(signature) for signature, count in counts.items())
        assert actual == target, (name, target, actual)
    q_counts: Counter[int] = Counter()
    for signature, count in counts.items():
        q_value = sum(SIGNS[i] * signature[i] for i in range(8)) // 3
        assert q_value in {-2, -1, 0, 1, 2}
        q_counts[q_value] += count
    return q_counts


def verify_point_controls(payload: dict[str, object]) -> dict[str, object]:
    assert payload["format"] == "wave209-point-signature-controls-v1"
    orbits = branch_orbits()
    rows = payload["orbits"]
    assert isinstance(rows, list) and len(rows) == len(orbits)
    feasible_orbits = 0
    excluded_orbits = 0
    feasible_branches = 0
    excluded_branches = 0
    summaries = []

    for orbit_id, (item, orbit) in enumerate(zip(rows, orbits)):
        assert item["orbit_id"] == orbit_id
        source_form_index, source_H = orbit[0]
        source_D = gram(FORM_DIAGONALS[source_form_index])
        signatures, equations = point_constraint_system(source_D, source_H)
        allowed_point_set = set(signatures)
        kind = item["kind"]
        q_counts: Counter[int] | None = None
        if kind == "control":
            counts: Counter[tuple[int, ...]] = Counter()
            for code, count in item["counts"]:
                signature = decode_point_signature(code)
                assert isinstance(count, int) and count > 0
                counts[signature] += count
            assert len(counts) == len(item["counts"])
            q_counts = exact_point_control_check(source_D, source_H, counts)
            feasible_orbits += 1
            feasible_branches += len(orbit)
        elif kind == "farkas":
            coefficients = [0] * len(equations)
            for index, coefficient in item["coefficients"]:
                assert 0 <= index < len(equations)
                assert isinstance(coefficient, int) and coefficient
                coefficients[index] += coefficient
            assert len([value for value in coefficients if value]) == len(item["coefficients"])
            rhs = sum(
                coefficient * equation[1]
                for coefficient, equation in zip(coefficients, equations)
            )
            pointwise = [
                sum(
                    coefficient * equation[2](signature)
                    for coefficient, equation in zip(coefficients, equations)
                )
                for signature in signatures
            ]
            assert min(pointwise) >= 0
            assert rhs < 0
            excluded_orbits += 1
            excluded_branches += len(orbit)
        else:
            raise AssertionError(kind)

        transported = 0
        for target_form_index, target_H in orbit:
            target_D = gram(FORM_DIAGONALS[target_form_index])
            permutation = next(
                permutation
                for permutation in form_maps(source_D, target_D)
                if map_subset(source_H, permutation) == target_H
            )
            # Exact system isomorphism under selected-label renaming.
            for signature in signatures:
                target_signature = [0] * 8
                for i in range(8):
                    target_signature[permutation[i]] = signature[i]
                target_signature_tuple = tuple(target_signature)
                assert target_signature_tuple in allowed_point_set
                assert sum(SIGNS[i] * signature[i] for i in range(8)) == sum(
                    SIGNS[i] * target_signature_tuple[i] for i in range(8)
                )
            for i, j in combinations(range(8), 2):
                source_table = point_pair_table(source_D, source_H, i, j)
                target_edge = tuple(sorted((permutation[i], permutation[j])))
                target_table = point_pair_table(
                    target_D, target_H, target_edge[0], target_edge[1]
                )
                if permutation[i] > permutation[j]:
                    target_table = {(right, left): count for (left, right), count in target_table.items()}
                assert source_table == target_table
            if kind == "control":
                transported_counts: Counter[tuple[int, ...]] = Counter()
                for signature, count in counts.items():
                    target_signature = [0] * 8
                    for i in range(8):
                        target_signature[permutation[i]] = signature[i]
                    transported_counts[tuple(target_signature)] += count
                assert exact_point_control_check(target_D, target_H, transported_counts) == q_counts
            transported += 1

        summaries.append(
            {
                "orbit_id": orbit_id,
                "kind": kind,
                "branch_count": len(orbit),
                "representative_form_diagonal": list(FORM_DIAGONALS[source_form_index]),
                "representative_selected_intersections": [list(edge) for edge in sorted(source_H)],
                "selected_intersection_count": len(source_H),
                "same_sign_intersections": sum(
                    SIGNS[i] == SIGNS[j] for i, j in source_H
                ),
                "opposite_sign_intersections": sum(
                    SIGNS[i] != SIGNS[j] for i, j in source_H
                ),
                "transported_branch_checks": transported,
                **(
                    {"q_value_counts": {str(key): q_counts[key] for key in range(-2, 3)}}
                    if q_counts is not None
                    else {
                        "farkas_nonzero_coefficients": len(item["coefficients"]),
                        "farkas_rhs": rhs,
                        "farkas_pointwise_minimum": min(pointwise),
                    }
                ),
            }
        )

    assert feasible_orbits == 7 and excluded_orbits == 17
    assert feasible_branches == 51 and excluded_branches == 198
    return {
        "allowed_signature_count": len(point_signatures()),
        "feasible_orbits": feasible_orbits,
        "excluded_orbits": excluded_orbits,
        "surviving_labelled_branches": feasible_branches,
        "excluded_labelled_branches": excluded_branches,
        "orbit_summaries": summaries,
        "certificate_logic": "Farkas y has A^T y>=0 on all 2187 allowed signatures but b^T y<0",
        "warning": "integer controls are 99-row joint signature censuses, not points with adjacency or a graph",
    }


def point_matrix(
    D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]
):
    """Generation-only SciPy matrix plus exact equation metadata."""
    import numpy as np
    from scipy.sparse import csr_matrix

    signatures, equations = point_constraint_system(D, H)
    matrix = csr_matrix(
        np.asarray(
            [[feature(signature) for signature in signatures] for _, _, feature in equations],
            dtype=float,
        )
    )
    targets = np.asarray([target for _, target, _ in equations], dtype=float)
    return signatures, equations, matrix, targets


def rationalize_farkas(ray, equations, signatures) -> tuple[list[list[int]], int]:
    """Turn a numerical HiGHS ray into a replayed exact integer certificate."""
    for denominator_limit in (100, 1_000, 10_000, 1_000_000):
        fractions = [Fraction(float(value)).limit_denominator(denominator_limit) for value in ray]
        scale = 1
        for value in fractions:
            scale = lcm(scale, value.denominator)
        integers = [-(value.numerator * (scale // value.denominator)) for value in fractions]
        common = 0
        for value in integers:
            common = gcd(common, abs(value))
        if common:
            integers = [value // common for value in integers]
        rhs = sum(value * equation[1] for value, equation in zip(integers, equations))
        pointwise = [
            sum(value * equation[2](signature) for value, equation in zip(integers, equations))
            for signature in signatures
        ]
        if rhs < 0 and min(pointwise) >= 0:
            return [[index, value] for index, value in enumerate(integers) if value], rhs
    raise RuntimeError("could not rationalize the numerical Farkas ray exactly")


def generate_point_controls() -> dict[str, object]:
    try:
        import numpy as np
        from highspy import Highs, HighsModelStatus, kHighsInf
        from scipy.optimize import Bounds, LinearConstraint, linprog, milp
    except ImportError as exc:  # pragma: no cover - generation-only guard
        raise RuntimeError("point-control generation requires SciPy and highspy") from exc

    output = []
    for orbit_id, orbit in enumerate(branch_orbits()):
        print(f"generating point-signature certificate {orbit_id + 1}/24", flush=True)
        form_index, H = orbit[0]
        D = gram(FORM_DIAGONALS[form_index])
        signatures, equations, matrix, targets = point_matrix(D, H)
        relaxation = linprog(
            np.zeros(len(signatures)),
            A_eq=matrix,
            b_eq=targets,
            bounds=(0, None),
            method="highs",
        )
        if relaxation.success:
            candidate = milp(
                np.zeros(len(signatures)),
                integrality=np.ones(len(signatures)),
                bounds=Bounds(np.zeros(len(signatures)), np.full(len(signatures), np.inf)),
                constraints=LinearConstraint(matrix, targets, targets),
                options={"time_limit": 120, "mip_rel_gap": 0},
            )
            if candidate.x is None:
                raise RuntimeError(f"orbit {orbit_id}: LP feasible but no integer control found")
            rounded = np.rint(candidate.x).astype(int)
            if np.max(np.abs(matrix @ rounded - targets)) != 0:
                raise RuntimeError(f"orbit {orbit_id}: rounded point control failed")
            output.append(
                {
                    "orbit_id": orbit_id,
                    "kind": "control",
                    "counts": [
                        [point_signature_code(signature), int(count)]
                        for signature, count in zip(signatures, rounded)
                        if count
                    ],
                }
            )
            continue

        highs = Highs()
        highs.setOptionValue("output_flag", False)
        highs.setOptionValue("presolve", "off")
        column_count = matrix.shape[1]
        highs.addCols(
            column_count,
            np.zeros(column_count),
            np.zeros(column_count),
            np.full(column_count, kHighsInf),
            0,
            np.asarray([0], dtype=np.int32),
            np.asarray([], dtype=np.int32),
            np.asarray([], dtype=float),
        )
        highs.addRows(
            matrix.shape[0],
            targets,
            targets,
            matrix.nnz,
            matrix.indptr.astype(np.int32),
            matrix.indices.astype(np.int32),
            matrix.data,
        )
        highs.run()
        if highs.getModelStatus() != HighsModelStatus.kInfeasible:
            raise RuntimeError(f"orbit {orbit_id}: expected infeasible LP")
        _, exists, ray = highs.getDualRay()
        if not exists:
            raise RuntimeError(f"orbit {orbit_id}: missing dual ray")
        coefficients, _ = rationalize_farkas(ray, equations, signatures)
        output.append(
            {"orbit_id": orbit_id, "kind": "farkas", "coefficients": coefficients}
        )

    payload = {"format": "wave209-point-signature-controls-v1", "orbits": output}
    POINT_CONTROLS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def projector_checks() -> dict[str, object]:
    summaries = []
    for diagonal in FORM_DIAGONALS:
        D = gram(diagonal)
        F = selected_f_matrix(D)
        M = [[1 - F[i][j] for j in range(8)] for i in range(8)]  # 21 P_0[S,S]
        multiplicities = {
            eigenvalue: 8
            - rank_q(
                [
                    [M[i][j] - (eigenvalue if i == j else 0) for j in range(8)]
                    for i in range(8)
                ]
            )
            for eigenvalue in (1, 3, 5, 9)
        }
        assert multiplicities == {1: 1, 3: 4, 5: 2, 9: 1}
        assert [sum(M[i][j] * SIGNS[j] for j in range(8)) for i in range(8)] == [
            9 * sign for sign in SIGNS
        ]
        # b=-3*alpha and P_SS=M/21.  Hence P_SS^-1*b=-7*alpha.
        b = tuple(-3 * sign for sign in SIGNS)
        inverse_action = tuple(-7 * sign for sign in SIGNS)
        assert all(
            sum(Fraction(M[i][j], 21) * inverse_action[j] for j in range(8)) == b[i]
            for i in range(8)
        )
        minimum_norm = sum(b[i] * inverse_action[i] for i in range(8))
        assert minimum_norm == 168
        summaries.append(
            {
                "form_diagonal": list(diagonal),
                "eigenvalues_of_21P_SS": {str(key): value for key, value in multiplicities.items()},
                "marked_minimum_zero_eigen_norm": minimum_norm,
                "inverse_action": list(inverse_action),
            }
        )
    return {
        "identity": "F=231*P_const-21*P_0, hence P_0=(J-F)/21",
        "selected_forms": summaries,
        "point_projector_diagonal": "(E_-4)_(x,x)=4/9",
        "coordinate_bound": "q_x^2 <= (4/9)*56 < 25, hence |q_x|<=4",
    }


def build_result(
    controls_payload: dict[str, object], point_controls_payload: dict[str, object]
) -> dict[str, object]:
    assert controls_payload["format"] == "wave209-rank4-aggregate-controls-v2"
    for relative, expected in EXPECTED_INPUT_HASHES.items():
        assert sha256(ROOT / relative) == expected

    forms = tuple(gram(diagonal) for diagonal in FORM_DIAGONALS)
    subsets = tuple(accepted_subsets(D) for D in forms)
    assert [len(rows) for rows in subsets] == [83, 83, 83]
    assert all(sum(D[i][j] == 1 for i, j in combinations(range(8), 2)) == 8 for D in forms)

    orbits = branch_orbits()
    assert len(orbits) == 24
    assert sum(map(len, orbits)) == 249
    assert Counter(map(len, orbits)) == Counter({12: 12, 6: 9, 24: 2, 3: 1})
    controls = controls_payload["controls"]
    assert isinstance(controls, list) and len(controls) == len(orbits)
    summaries = []
    for orbit_id, (control, orbit) in enumerate(zip(controls, orbits)):
        assert control["orbit_id"] == orbit_id
        summaries.append(verify_control(control, orbit))

    local_norms: Counter[int] = Counter()
    local_odd_supports: Counter[int] = Counter()
    local_examples = []
    for orbit_id, orbit in enumerate(orbits):
        source_form_index, H = orbit[0]
        source_D = gram(FORM_DIAGONALS[source_form_index])
        local_norm, witness = selected_union_control(H)
        odd_support = sum(value % 2 != 0 for _, value in witness)
        local_norms[local_norm] += len(orbit)
        local_odd_supports[odd_support] += len(orbit)
        transported_witness_checks = 0
        for target_form_index, target_H in orbit:
            target_D = gram(FORM_DIAGONALS[target_form_index])
            permutation = next(
                permutation
                for permutation in form_maps(source_D, target_D)
                if map_subset(H, permutation) == target_H
            )
            transported_witness = [
                (tuple(sorted(permutation[i] for i in membership)), value)
                for membership, value in witness
            ]
            line_sums = [0] * 8
            for membership, value in transported_witness:
                for i in membership:
                    line_sums[i] += value
            assert line_sums == [-3 * sign for sign in SIGNS]
            assert sum(value * value for _, value in transported_witness) == local_norm
            transported_witness_checks += 1
        local_examples.append(
            {
                "orbit_id": orbit_id,
                "minimum_selected_union_norm": local_norm,
                "odd_selected_union_coordinates": odd_support,
                "transported_branch_checks": transported_witness_checks,
                "witness": [
                    {"membership": list(membership), "q": value}
                    for membership, value in witness
                ],
            }
        )
    assert sum(local_norms.values()) == 249
    assert max(local_norms) <= 56

    profile_count, odd_weights = point_coordinate_profiles()
    assert profile_count == 872
    assert sum(odd_weights.values()) == 800
    assert odd_weights == Counter(
        {8: 140, 12: 152, 16: 154, 20: 116, 24: 86, 28: 56, 32: 40,
         36: 24, 40: 16, 44: 8, 48: 5, 52: 2, 56: 1}
    )
    point_result = verify_point_controls(point_controls_payload)

    return {
        "claim_label": "DERIVED",
        "conditional_scope": "three Wave208 rank-four forms under the frozen hypothetical endpoint",
        "input_hashes": EXPECTED_INPUT_HASHES,
        "spectral_triangle_reduction": {
            "definitions": "t=B^Tq and C=B^TB-3I",
            "identities": [
                "t.t=168",
                "B*t=3*q",
                "C*t=0",
                "sum(t)=0",
                "t_i=-3*alpha_i on the eight marked triangles",
            ],
            "residual_223": {
                "sum": 0,
                "squared_norm": 96,
                "value_alphabet": [-2, -1, 0, 1, 2],
            },
            "projector": projector_checks(),
        },
        "parity": {
            "q_even_excluded": True,
            "reason": "each marked triangle sum is odd: U^Tq=-3*alpha",
            "odd_support": "p=q mod 2 is nonzero, A*p=0, B_S^T*p=1_8",
            "triangle_word": "s=B^T*p=t mod 2 satisfies C*s=0 and s_S=1_8",
            "imported_kernel_minimum": 8,
            "norm14_division_available": False,
            "point_count_profiles_before_graph_realization": profile_count,
            "point_count_profiles_after_odd_support_minimum": sum(odd_weights.values()),
            "odd_support_weight_distribution": {str(key): value for key, value in sorted(odd_weights.items())},
            "selected_union_integer_controls": {
                "all_249_branches_have_norm_at_most_56": True,
                "minimum_norm_distribution": {str(key): value for key, value in sorted(local_norms.items())},
                "odd_coordinate_distribution": {str(key): value for key, value in sorted(local_odd_supports.items())},
                "orbit_examples": local_examples,
                "warning": "selected-union controls satisfy only the eight marked triangle sums, not Aq=-4q or any outside equation",
            },
        },
        "point_signature_census": {
            "definition": "s_i(x)=-1 on T_i, +1 outside T_i when x is adjacent to its unique T_i point, and 0 otherwise",
            "formula": "q_x=(1/3)*sum_i alpha_i*s_i(x)",
            "single_coordinate_counts": {"-1": 3, "0": 60, "1": 36},
            "pair_tables_forced_by": "selected intersection H_ij and polar cross-edge count D_ij",
            **point_result,
        },
        "marked_branch_census": {
            "forms": [list(diagonal) for diagonal in FORM_DIAGONALS],
            "labelled_subsets_per_form": [len(rows) for rows in subsets],
            "total_labelled_branches": 249,
            "proved_constraint_relabeling_orbits": len(orbits),
            "orbit_size_distribution": {str(key): value for key, value in sorted(Counter(map(len, orbits)).items())},
            "target_automorphism_assumed": False,
        },
        "aggregate_controls": {
            "all_orbits_have_exact_integer_controls": True,
            "covered_labelled_branches": sum(summary["orbit_size"] for summary in summaries),
            "orbit_summaries": summaries,
            "warning": "these are aggregate residual signature/intersection counts, not 223 residual blocks, C*t=0 on residual rows, a 231-block incidence frame, or a 99-vertex graph",
        },
        "status": "UNKNOWN",
        "unresolved_boundary": "for the 51 surviving labelled branches, couple an allowed 99-point joint signature census to actual adjacency and the controlled 223 residual triangle types, or derive a contradiction",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-controls", action="store_true")
    parser.add_argument("--generate-point-controls", action="store_true")
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    payload = generate_controls() if args.generate_controls else json.loads(CONTROLS.read_text(encoding="utf-8"))
    point_payload = (
        generate_point_controls()
        if args.generate_point_controls
        else json.loads(POINT_CONTROLS.read_text(encoding="utf-8"))
    )
    result = build_result(payload, point_payload)
    if args.write_results:
        RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.verify:
        assert result == json.loads(RESULTS.read_text(encoding="utf-8"))
        print("PASS: Wave209 rank-four norm-56 exact reduction and controls")
    elif not args.write_results and not args.generate_controls:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
