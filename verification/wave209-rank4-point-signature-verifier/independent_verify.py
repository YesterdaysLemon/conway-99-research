#!/usr/bin/env python3
"""Independent exact audit of the sealed Wave 209 rank-four package.

This module imports no discovery code.  It reconstructs the three labelled
forms from their vanishing-quadratic space, rebuilds all 249 marked branches
and their 24 constraint-relabeling orbits, then checks every archived exact
certificate after transport to every labelled branch.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Iterable

Q = 3
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "attempts" / "wave209-rank4-norm56-proof-b"
POINT_ARCHIVE = SOURCE / "point-signature-controls.json"
AGGREGATE_ARCHIVE = SOURCE / "aggregate-controls.json"
SOURCE_RESULTS = SOURCE / "exact-results.json"
SOURCE_MANIFEST = SOURCE / "package-manifest.sha256"
RESULTS = HERE / "independent-results.json"

SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
FORM_LABELS = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
VECTORS = (
    (1, 2, 2, 2),
    (1, 0, 2, 2),
    (1, 2, 0, 2),
    (1, 2, 2, 0),
    (1, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
)
POSITIONS = tuple((i, j) for i in range(4) for j in range(i, 4))

FROZEN_HASHES = {
    "AGENTS.md": "4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3",
    "attempts/wave209-four-survivor-globalization/protocol.md":
        "3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196",
    "verification/2026-07-31-wave208-integration-audit.md":
        "eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754",
    "logs/2026-07-31-wave208-public-checkpoint.json":
        "af31d56635f47b0a2c8d961fa813a34590d53773c022211b7cdc39731c0cb77b",
    "attempts/wave209-rank4-norm56-proof-b/package-manifest.sha256":
        "2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_inputs() -> dict[str, str]:
    actual = {relative: sha256(ROOT / relative) for relative in FROZEN_HASHES}
    if actual != FROZEN_HASHES:
        raise AssertionError((FROZEN_HASHES, actual))
    return actual


def verify_source_manifest() -> dict[str, str]:
    checked: dict[str, str] = {}
    for raw in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = raw.split("  ", 1)
        path = ROOT / relative
        actual = sha256(path)
        if actual != expected:
            raise AssertionError((relative, expected, actual))
        checked[relative] = actual
    if len(checked) != 12:
        raise AssertionError(f"expected 12 sealed source entries, got {len(checked)}")
    return checked


def inverse_mod3(value: int) -> int:
    value %= Q
    if value == 1:
        return 1
    if value == 2:
        return 2
    raise ZeroDivisionError


def rref_mod3(matrix: Iterable[Iterable[int]]) -> tuple[list[list[int]], list[int]]:
    work = [[entry % Q for entry in row] for row in matrix]
    pivots: list[int] = []
    row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = inverse_mod3(work[row][column])
        work[row] = [(scale * value) % Q for value in work[row]]
        for other in range(len(work)):
            if other == row or not work[other][column]:
                continue
            scale = work[other][column]
            work[other] = [
                (work[other][j] - scale * work[row][j]) % Q
                for j in range(len(work[0]))
            ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return work, pivots


def nullspace_mod3(matrix: Iterable[Iterable[int]]) -> list[list[int]]:
    source = [list(row) for row in matrix]
    reduced, pivots = rref_mod3(source)
    columns = len(source[0])
    basis: list[list[int]] = []
    for free in (column for column in range(columns) if column not in pivots):
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free] % Q
        basis.append(vector)
    return basis


def symmetric_matrix(coordinates: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * 4 for _ in range(4)]
    for value, (i, j) in zip(coordinates, POSITIONS):
        matrix[i][j] = matrix[j][i] = value % Q
    return tuple(tuple(row) for row in matrix)


def bilinear(left: tuple[int, ...], form: tuple[tuple[int, ...], ...], right: tuple[int, ...]) -> int:
    return sum(left[i] * form[i][j] * right[j] for i in range(4) for j in range(4)) % Q


@lru_cache(maxsize=1)
def labelled_grams() -> dict[tuple[int, int, int], tuple[tuple[int, ...], ...]]:
    evaluations = [
        [(vector[i] * vector[j] * (1 if i == j else 2)) % Q for i, j in POSITIONS]
        for vector in VECTORS
    ]
    basis = nullspace_mod3(evaluations)
    if len(basis) != 3:
        raise AssertionError("vanishing symmetric-form space is not three-dimensional")
    output: dict[tuple[int, int, int], tuple[tuple[int, ...], ...]] = {}
    for coefficients in product(range(Q), repeat=3):
        coordinates = [
            sum(coefficients[i] * basis[i][j] for i in range(3)) % Q
            for j in range(10)
        ]
        form = symmetric_matrix(coordinates)
        if any(bilinear(vector, form, vector) for vector in VECTORS):
            raise AssertionError("reconstructed form does not vanish")
        label = (form[1][1], form[2][2], form[3][3])
        output[label] = tuple(
            tuple(bilinear(VECTORS[i], form, VECTORS[j]) for j in range(8))
            for i in range(8)
        )
    if len(output) != 27:
        raise AssertionError("form labels are not unique")
    return output


def grams() -> tuple[tuple[tuple[int, ...], ...], ...]:
    forms = labelled_grams()
    return tuple(forms[label] for label in FORM_LABELS)


def accepted_subsets(D: tuple[tuple[int, ...], ...]) -> tuple[frozenset[tuple[int, int]], ...]:
    product_one = tuple((i, j) for i, j in combinations(range(8), 2) if D[i][j] == 1)
    if len(product_one) != 8:
        raise AssertionError("rank-four product-one graph does not have eight edges")
    accepted: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(product_one)):
        H = frozenset(edge for bit, edge in enumerate(product_one) if mask & (1 << bit))
        if sum(SIGNS[i] * SIGNS[j] for i, j in H) % Q != 1:
            continue
        degrees = [sum(i in edge for edge in H) for i in range(8)]
        if max(degrees) > 3:
            raise AssertionError("invalid selected-triangle degree")
        integer_values = [SIGNS[i] + SIGNS[j] for i, j in H]
        integer_values.extend(SIGNS[i] for i in range(8) for _ in range(3 - degrees[i]))
        residues = [value % Q for value in integer_values]
        weight = sum(value != 0 for value in residues)
        if weight not in {14, 17, 20, 23}:
            continue
        if weight == 14 and (residues.count(1), residues.count(2)) != (7, 7):
            continue
        accepted.append(H)
    return tuple(accepted)


@lru_cache(maxsize=1)
def sign_preserving_permutations() -> tuple[tuple[int, ...], ...]:
    return tuple(
        positive + negative
        for positive in permutations(range(4))
        for negative in permutations(range(4, 8))
    )


def form_maps(source: tuple[tuple[int, ...], ...], target: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in sign_preserving_permutations()
        if all(source[i][j] == target[permutation[i]][permutation[j]] for i in range(8) for j in range(8))
    )


def map_subset(H: frozenset[tuple[int, int]], permutation: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted((permutation[i], permutation[j]))) for i, j in H)


@lru_cache(maxsize=1)
def branch_orbits() -> tuple[tuple[tuple[int, frozenset[tuple[int, int]]], ...], ...]:
    forms = grams()
    subsets = tuple(accepted_subsets(D) for D in forms)
    nodes = {(form, H) for form in range(3) for H in subsets[form]}
    maps = {(i, j): form_maps(forms[i], forms[j]) for i in range(3) for j in range(3)}
    if any(len(rows) != 8 for rows in maps.values()):
        raise AssertionError("expected eight exact label maps for each ordered form pair")
    unseen = set(nodes)
    output = []
    while unseen:
        seed = min(unseen, key=lambda item: (item[0], sorted(item[1])))
        orbit: set[tuple[int, frozenset[tuple[int, int]]]] = set()
        frontier = [seed]
        while frontier:
            form, H = frontier.pop()
            if (form, H) in orbit:
                continue
            orbit.add((form, H))
            for target in range(3):
                for permutation in maps[(form, target)]:
                    image = (target, map_subset(H, permutation))
                    if image in nodes and image not in orbit:
                        frontier.append(image)
        unseen -= orbit
        output.append(tuple(sorted(orbit, key=lambda item: (item[0], sorted(item[1])))))
    flattened = [node for orbit in output for node in orbit]
    if len(flattened) != len(set(flattened)) or set(flattened) != nodes:
        raise AssertionError("orbit partition is not exact")
    return tuple(output)


def mapping_for(source_form: int, source_H: frozenset[tuple[int, int]], target_form: int, target_H: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    return next(
        permutation
        for permutation in form_maps(grams()[source_form], grams()[target_form])
        if map_subset(source_H, permutation) == target_H
    )


@lru_cache(maxsize=1)
def point_signatures() -> tuple[tuple[int, ...], ...]:
    rows = tuple(
        row
        for row in product((-1, 0, 1), repeat=8)
        if sum(SIGNS[i] * row[i] for i in range(8)) % 3 == 0
    )
    if len(rows) != 2187:
        raise AssertionError("integral point-signature count differs")
    return rows


def decode_point_signature(code: int) -> tuple[int, ...]:
    values = []
    for _ in range(8):
        values.append(code % 3 - 1)
        code //= 3
    if code:
        raise AssertionError("point-signature code exceeds eight trits")
    return tuple(values)


def point_pair_table(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]], i: int, j: int) -> dict[tuple[int, int], int]:
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


PointDescriptor = tuple[object, ...]


@lru_cache(maxsize=1)
def point_descriptors() -> tuple[PointDescriptor, ...]:
    rows: list[PointDescriptor] = [("total",)]
    rows.extend(("m", i, value) for i in range(8) for value in (-1, 0, 1))
    rows.extend(
        ("p", i, j, left, right)
        for i, j in combinations(range(8), 2)
        for left in (-1, 0, 1)
        for right in (-1, 0, 1)
    )
    rows.extend((("qsum",), ("q2",)))
    if len(rows) != 279:
        raise AssertionError("point equation count differs")
    return tuple(rows)


def q_value(signature: tuple[int, ...]) -> int:
    numerator = sum(SIGNS[i] * signature[i] for i in range(8))
    if numerator % 3:
        raise AssertionError("nonintegral q signature")
    return numerator // 3


def point_feature(descriptor: PointDescriptor, signature: tuple[int, ...]) -> int:
    kind = descriptor[0]
    if kind == "total":
        return 1
    if kind == "m":
        _, i, value = descriptor
        return int(signature[i] == value)
    if kind == "p":
        _, i, j, left, right = descriptor
        return int(signature[i] == left and signature[j] == right)
    if kind == "qsum":
        return q_value(signature)
    if kind == "q2":
        return q_value(signature) ** 2
    raise AssertionError(descriptor)


def point_targets(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]) -> dict[PointDescriptor, int]:
    output: dict[PointDescriptor, int] = {("total",): 99, ("qsum",): 0, ("q2",): 56}
    for i in range(8):
        output[("m", i, -1)] = 3
        output[("m", i, 0)] = 60
        output[("m", i, 1)] = 36
    for i, j in combinations(range(8), 2):
        table = point_pair_table(D, H, i, j)
        for left in (-1, 0, 1):
            for right in (-1, 0, 1):
                output[("p", i, j, left, right)] = table[(left, right)]
    if set(output) != set(point_descriptors()):
        raise AssertionError("point target descriptors differ")
    return output


def check_point_counts(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]], counts: Counter[tuple[int, ...]]) -> Counter[int]:
    allowed = set(point_signatures())
    if not counts or set(counts) - allowed or any(not isinstance(value, int) or value <= 0 for value in counts.values()):
        raise AssertionError("invalid point control support")
    targets = point_targets(D, H)
    for descriptor in point_descriptors():
        actual = sum(count * point_feature(descriptor, signature) for signature, count in counts.items())
        if actual != targets[descriptor]:
            raise AssertionError((descriptor, targets[descriptor], actual))
    return Counter({value: sum(count for signature, count in counts.items() if q_value(signature) == value) for value in range(-2, 3)})


def transform_point_descriptor(descriptor: PointDescriptor, permutation: tuple[int, ...]) -> PointDescriptor:
    kind = descriptor[0]
    if kind in {"total", "qsum", "q2"}:
        return descriptor
    if kind == "m":
        _, i, value = descriptor
        return ("m", permutation[i], value)
    if kind == "p":
        _, i, j, left, right = descriptor
        a, b = permutation[i], permutation[j]
        return ("p", a, b, left, right) if a < b else ("p", b, a, right, left)
    raise AssertionError(descriptor)


def check_farkas(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]], coefficients: dict[PointDescriptor, int]) -> tuple[int, int]:
    if not coefficients or any(not isinstance(value, int) or not value for value in coefficients.values()):
        raise AssertionError("empty or nonintegral Farkas vector")
    targets = point_targets(D, H)
    rhs = sum(value * targets[descriptor] for descriptor, value in coefficients.items())
    pointwise = [
        sum(value * point_feature(descriptor, signature) for descriptor, value in coefficients.items())
        for signature in point_signatures()
    ]
    if min(pointwise) < 0 or rhs >= 0:
        raise AssertionError((min(pointwise), rhs))
    return min(pointwise), rhs


def verify_point_archive() -> dict[str, object]:
    payload = json.loads(POINT_ARCHIVE.read_text(encoding="utf-8"))
    if payload.get("format") != "wave209-point-signature-controls-v1":
        raise AssertionError("wrong point archive format")
    orbits = branch_orbits()
    if len(payload.get("orbits", [])) != len(orbits):
        raise AssertionError("point archive orbit count differs")
    controls = exclusions = controlled_branches = excluded_branches = 0
    transported_checks = 0
    certificate_extremes: list[dict[str, int]] = []
    for orbit_id, (item, orbit) in enumerate(zip(payload["orbits"], orbits)):
        if item["orbit_id"] != orbit_id:
            raise AssertionError("point archive orbit order differs")
        source_form, source_H = orbit[0]
        source_D = grams()[source_form]
        if item["kind"] == "control":
            counts: Counter[tuple[int, ...]] = Counter()
            for code, count in item["counts"]:
                signature = decode_point_signature(code)
                if signature in counts or not isinstance(count, int) or count <= 0:
                    raise AssertionError("duplicate or invalid point control row")
                counts[signature] = count
            source_q_counts = check_point_counts(source_D, source_H, counts)
            controls += 1
            controlled_branches += len(orbit)
            coefficients = None
        elif item["kind"] == "farkas":
            coefficients = {}
            descriptors = point_descriptors()
            for index, value in item["coefficients"]:
                if not 0 <= index < len(descriptors) or descriptors[index] in coefficients or not isinstance(value, int) or not value:
                    raise AssertionError("invalid sparse Farkas entry")
                coefficients[descriptors[index]] = value
            minimum, rhs = check_farkas(source_D, source_H, coefficients)
            certificate_extremes.append({"orbit_id": orbit_id, "pointwise_minimum": minimum, "rhs": rhs})
            exclusions += 1
            excluded_branches += len(orbit)
            counts = Counter()
            source_q_counts = Counter()
        else:
            raise AssertionError(item["kind"])

        for target_form, target_H in orbit:
            permutation = mapping_for(source_form, source_H, target_form, target_H)
            target_D = grams()[target_form]
            if item["kind"] == "control":
                transported: Counter[tuple[int, ...]] = Counter()
                for signature, count in counts.items():
                    target = [0] * 8
                    for i, value in enumerate(signature):
                        target[permutation[i]] = value
                    transported[tuple(target)] += count
                if check_point_counts(target_D, target_H, transported) != source_q_counts:
                    raise AssertionError("transported q histogram differs")
            else:
                assert coefficients is not None
                transported_coefficients = {
                    transform_point_descriptor(descriptor, permutation): value
                    for descriptor, value in coefficients.items()
                }
                if len(transported_coefficients) != len(coefficients):
                    raise AssertionError("Farkas transport collided")
                check_farkas(target_D, target_H, transported_coefficients)
            transported_checks += 1
    if (controls, exclusions, controlled_branches, excluded_branches, transported_checks) != (7, 17, 51, 198, 249):
        raise AssertionError((controls, exclusions, controlled_branches, excluded_branches, transported_checks))
    return {
        "control_orbits": controls,
        "farkas_orbits": exclusions,
        "controlled_labelled_branches": controlled_branches,
        "excluded_labelled_branches": excluded_branches,
        "explicit_transported_branch_checks": transported_checks,
        "certificate_extremes": certificate_extremes,
    }


def row_space(D: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    rows = {
        tuple(sum(coefficient[k] * D[k][i] for k in range(8)) % 3 for i in range(8))
        for coefficient in product(range(3), repeat=8)
    }
    if len(rows) != 81:
        raise AssertionError("rank-four evaluation code does not have 81 words")
    return tuple(sorted(rows))


AggregateType = tuple[tuple[int, ...], frozenset[int], int]


def aggregate_types(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]) -> tuple[AggregateType, ...]:
    output = []
    for d in row_space(D):
        ones = tuple(i for i, value in enumerate(d) if value == 1)
        for mask in range(1 << len(ones)):
            h = frozenset(ones[bit] for bit in range(len(ones)) if mask & (1 << bit))
            degrees = {i: 0 for i in h}
            h_edges = 0
            allowed = True
            for i, j in combinations(sorted(h), 2):
                if (i, j) in H:
                    degrees[i] += 1
                    degrees[j] += 1
                    h_edges += 1
                    if degrees[i] > 1 or degrees[j] > 1:
                        allowed = False
                        break
                elif D[i][j] == 0:
                    allowed = False
                    break
            if not allowed or len(h) - h_edges > 3:
                continue
            numerator = sum(SIGNS[i] * d[i] for i in range(8))
            if numerator % 3:
                raise AssertionError("residual line sum is nonintegral")
            output.append((d, h, numerator // 3))
    return tuple(output)


AggregateDescriptor = tuple[object, ...]


def aggregate_descriptors() -> tuple[AggregateDescriptor, ...]:
    output: list[AggregateDescriptor] = [("total",)]
    output.extend(("d", i, value) for i in range(8) for value in (0, 1, 2))
    output.extend(("dprod", i, j) for i, j in combinations(range(8), 2))
    output.extend((("tsum",), ("t2",)))
    output.extend(descriptor for i in range(8) for descriptor in (("h", i), ("ht", i)))
    output.extend(("hh", i, j) for i, j in combinations(range(8), 2))
    if len(output) != 99:
        raise AssertionError("aggregate equation count differs")
    return tuple(output)


def residual_pair_count(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]], i: int, j: int) -> int:
    if (i, j) in H:
        return 5
    selected_common = sum(
        tuple(sorted((i, k))) in H and tuple(sorted((j, k))) in H
        for k in range(8) if k not in (i, j)
    )
    return D[i][j] - selected_common


def aggregate_targets(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]]) -> dict[AggregateDescriptor, int]:
    output: dict[AggregateDescriptor, int] = {("total",): 223, ("tsum",): 0, ("t2",): 96}
    for i in range(8):
        for value, full in ((0, 32), (1, 162), (2, 36)):
            output[("d", i, value)] = full - sum(D[k][i] == value for k in range(8) if k != i)
    F = tuple(tuple(-3 if i == j else D[i][j] for j in range(8)) for i in range(8))
    for i, j in combinations(range(8), 2):
        output[("dprod", i, j)] = 252 - 21 * D[i][j] - sum(F[k][i] * F[k][j] for k in range(8))
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    for i in range(8):
        output[("h", i)] = 18 - degrees[i]
        output[("ht", i)] = 3 * sum(SIGNS[j] for j in range(8) if tuple(sorted((i, j))) in H)
    for i, j in combinations(range(8), 2):
        target = residual_pair_count(D, H, i, j)
        if target < 0:
            raise AssertionError("negative residual pair count")
        output[("hh", i, j)] = target
    if set(output) != set(aggregate_descriptors()):
        raise AssertionError("aggregate target descriptors differ")
    return output


def aggregate_feature(descriptor: AggregateDescriptor, row: AggregateType) -> int:
    d, h, t = row
    kind = descriptor[0]
    if kind == "total": return 1
    if kind == "d": return int(d[descriptor[1]] == descriptor[2])
    if kind == "dprod": return d[descriptor[1]] * d[descriptor[2]]
    if kind == "tsum": return t
    if kind == "t2": return t * t
    if kind == "h": return int(descriptor[1] in h)
    if kind == "ht": return t * int(descriptor[1] in h)
    if kind == "hh": return int(descriptor[1] in h and descriptor[2] in h)
    raise AssertionError(descriptor)


def decode_aggregate_type(d_code: int, h_mask: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    d = []
    for _ in range(8):
        d.append(d_code % 3)
        d_code //= 3
    if d_code or h_mask >> 8:
        raise AssertionError("aggregate type code exceeds its width")
    return tuple(d), tuple(i for i in range(8) if h_mask & (1 << i))


def check_aggregate_counts(D: tuple[tuple[int, ...], ...], H: frozenset[tuple[int, int]], counts: Counter[tuple[tuple[int, ...], tuple[int, ...]]]) -> None:
    allowed = {(row[0], tuple(sorted(row[1]))): row for row in aggregate_types(D, H)}
    if not counts or set(counts) - set(allowed) or any(not isinstance(value, int) or value <= 0 for value in counts.values()):
        raise AssertionError("invalid aggregate control support")
    targets = aggregate_targets(D, H)
    for descriptor in aggregate_descriptors():
        actual = sum(count * aggregate_feature(descriptor, allowed[key]) for key, count in counts.items())
        if actual != targets[descriptor]:
            raise AssertionError((descriptor, targets[descriptor], actual))


def verify_aggregate_archive() -> dict[str, int]:
    payload = json.loads(AGGREGATE_ARCHIVE.read_text(encoding="utf-8"))
    if payload.get("format") != "wave209-rank4-aggregate-controls-v2":
        raise AssertionError("wrong aggregate archive format")
    orbits = branch_orbits()
    if len(payload.get("controls", [])) != 24:
        raise AssertionError("aggregate archive orbit count differs")
    checks = 0
    for orbit_id, (item, orbit) in enumerate(zip(payload["controls"], orbits)):
        if item["orbit_id"] != orbit_id or item["branch_count"] != len(orbit):
            raise AssertionError("aggregate orbit metadata differs")
        source_form, source_H = orbit[0]
        if item["form_diagonal"] != list(FORM_LABELS[source_form]) or item["selected_intersections"] != [list(edge) for edge in sorted(source_H)]:
            raise AssertionError("aggregate representative differs")
        counts: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
        for d_code, h_mask, count in item["counts"]:
            key = decode_aggregate_type(d_code, h_mask)
            if key in counts or not isinstance(count, int) or count <= 0:
                raise AssertionError("duplicate or invalid aggregate row")
            counts[key] = count
        check_aggregate_counts(grams()[source_form], source_H, counts)
        for target_form, target_H in orbit:
            permutation = mapping_for(source_form, source_H, target_form, target_H)
            transported: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
            for (d, h), count in counts.items():
                target_d = [0] * 8
                for i, value in enumerate(d):
                    target_d[permutation[i]] = value
                transported[(tuple(target_d), tuple(sorted(permutation[i] for i in h)))] += count
            check_aggregate_counts(grams()[target_form], target_H, transported)
            checks += 1
    if checks != 249:
        raise AssertionError("aggregate transport does not cover 249 branches")
    return {"aggregate_orbits": 24, "explicit_transported_branch_checks": checks}


def rational_rank(matrix: Iterable[Iterable[int | Fraction]]) -> int:
    work = [[Fraction(entry) for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                scale = work[row][column]
                work[row] = [work[row][j] - scale * work[rank][j] for j in range(len(work[0]))]
        rank += 1
    return rank


def verify_projector() -> list[dict[str, object]]:
    summaries = []
    for label, D in zip(FORM_LABELS, grams()):
        F = [[-3 if i == j else D[i][j] for j in range(8)] for i in range(8)]
        M = [[1 - F[i][j] for j in range(8)] for i in range(8)]
        multiplicities = {
            value: 8 - rational_rank([[M[i][j] - (value if i == j else 0) for j in range(8)] for i in range(8)])
            for value in (1, 3, 5, 9)
        }
        if multiplicities != {1: 1, 3: 4, 5: 2, 9: 1}:
            raise AssertionError(multiplicities)
        if [sum(M[i][j] * SIGNS[j] for j in range(8)) for i in range(8)] != [9 * sign for sign in SIGNS]:
            raise AssertionError("alpha is not the 9-eigenvector")
        b = tuple(-3 * sign for sign in SIGNS)
        inverse_image = tuple(-7 * sign for sign in SIGNS)
        if any(sum(Fraction(M[i][j], 21) * inverse_image[j] for j in range(8)) != b[i] for i in range(8)):
            raise AssertionError("projector inverse action differs")
        minimum = sum(b[i] * inverse_image[i] for i in range(8))
        if minimum != 168:
            raise AssertionError("projector minimum differs")
        summaries.append({"form": list(label), "eigenvalue_multiplicities_21P": {str(k): v for k, v in multiplicities.items()}, "minimum_norm": minimum})
    return summaries


@lru_cache(maxsize=None)
def best_private_split(count: int, target: int) -> tuple[int, tuple[int, ...]] | None:
    candidates = [(sum(value * value for value in values), values) for values in product(range(-4, 5), repeat=count) if sum(values) == target]
    return min(candidates) if candidates else None


def selected_union_minimum(H: frozenset[tuple[int, int]]) -> tuple[int, tuple[tuple[tuple[int, ...], int], ...]]:
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    unseen = {i for edge in H for i in edge}
    components = []
    while unseen:
        vertices = {min(unseen)}
        changed = True
        while changed:
            changed = False
            for edge in H:
                if vertices & set(edge):
                    before = len(vertices)
                    vertices.update(edge)
                    changed |= len(vertices) != before
        unseen -= vertices
        components.append((vertices, tuple(sorted(edge for edge in H if set(edge) <= vertices))))
    norm = 0
    witness: list[tuple[tuple[int, ...], int]] = []
    covered = set()
    for vertices, edges in components:
        best = None
        for edge_values in product(range(-4, 5), repeat=len(edges)):
            incident = {i: 0 for i in vertices}
            for edge, value in zip(edges, edge_values):
                incident[edge[0]] += value
                incident[edge[1]] += value
            private = []
            private_norm = 0
            for i in sorted(vertices):
                split = best_private_split(3 - degrees[i], -3 * SIGNS[i] - incident[i])
                if split is None:
                    break
                private_norm += split[0]
                private.extend(((i,), value) for value in split[1])
            else:
                rows = tuple((edge, value) for edge, value in zip(edges, edge_values)) + tuple(private)
                candidate = (sum(value * value for value in edge_values) + private_norm, edge_values, rows)
                if best is None or candidate < best:
                    best = candidate
        if best is None:
            raise AssertionError("selected-union component has no assignment")
        norm += best[0]
        witness.extend(best[2])
        covered |= vertices
    for i in range(8):
        if i not in covered:
            split = best_private_split(3, -3 * SIGNS[i])
            assert split is not None
            norm += split[0]
            witness.extend(((i,), value) for value in split[1])
    return norm, tuple(witness)


def verify_selected_union_controls(source_results: dict[str, object]) -> dict[str, object]:
    examples = source_results["parity"]["selected_union_integer_controls"]["orbit_examples"]
    if len(examples) != 24:
        raise AssertionError("selected-union example count differs")
    norms: Counter[int] = Counter()
    checks = 0
    for orbit_id, (example, orbit) in enumerate(zip(examples, branch_orbits())):
        source_form, source_H = orbit[0]
        minimum, independent_witness = selected_union_minimum(source_H)
        if example["orbit_id"] != orbit_id or example["minimum_selected_union_norm"] != minimum:
            raise AssertionError("selected-union minimum differs")
        archived = tuple((tuple(row["membership"]), row["q"]) for row in example["witness"])
        if sum(value * value for _, value in archived) != minimum:
            raise AssertionError("archived selected-union norm differs")
        if sum(value * value for _, value in independent_witness) != minimum:
            raise AssertionError("independent selected-union norm differs")
        for target_form, target_H in orbit:
            permutation = mapping_for(source_form, source_H, target_form, target_H)
            line_sums = [0] * 8
            for membership, value in archived:
                for i in membership:
                    line_sums[permutation[i]] += value
            if line_sums != [-3 * sign for sign in SIGNS]:
                raise AssertionError("transported selected-union line sums differ")
            checks += 1
        norms[minimum] += len(orbit)
    if checks != 249 or max(norms) > 56:
        raise AssertionError("selected-union coverage or norm cap differs")
    return {"explicit_transported_branch_checks": checks, "minimum_norm_distribution": {str(k): v for k, v in sorted(norms.items())}}


def point_profile_census() -> tuple[int, Counter[int]]:
    values = (-4, -3, -2, -1, 1, 2, 3, 4)
    profile_count = 0
    odd_weights: Counter[int] = Counter()

    def visit(index: int, used: int, total: int, square: int, counts: tuple[int, ...]) -> None:
        nonlocal profile_count
        if index == len(values):
            if total or square != 56 or used > 99:
                return
            profile_count += 1
            odd = sum(count for value, count in zip(values, counts) if value % 2)
            if odd >= 8:
                odd_weights[odd] += 1
            return
        value = values[index]
        for count in range(min(99 - used, (56 - square) // (value * value)) + 1):
            visit(index + 1, used + count, total + value * count, square + value * value * count, counts + (count,))

    visit(0, 0, 0, 0, ())
    return profile_count, odd_weights


def hostile_tests() -> dict[str, bool]:
    payload = json.loads(POINT_ARCHIVE.read_text(encoding="utf-8"))
    first_farkas = next(row for row in payload["orbits"] if row["kind"] == "farkas")
    descriptors = point_descriptors()
    coefficients = {descriptors[index]: value for index, value in first_farkas["coefficients"]}
    orbit = branch_orbits()[first_farkas["orbit_id"]]
    form, H = orbit[0]
    erased_rejected = reversed_rejected = False
    try:
        check_farkas(grams()[form], H, {})
    except AssertionError:
        erased_rejected = True
    try:
        check_farkas(grams()[form], H, {descriptor: -value for descriptor, value in coefficients.items()})
    except AssertionError:
        reversed_rejected = True

    first_control = next(row for row in payload["orbits"] if row["kind"] == "control")
    orbit = branch_orbits()[first_control["orbit_id"]]
    form, H = orbit[0]
    counts = Counter({decode_point_signature(code): count for code, count in first_control["counts"]})
    one_signature = next(iter(counts))
    counts[one_signature] += 1
    mutated_point_rejected = False
    try:
        check_point_counts(grams()[form], H, counts)
    except AssertionError:
        mutated_point_rejected = True

    aggregate_payload = json.loads(AGGREGATE_ARCHIVE.read_text(encoding="utf-8"))
    first = aggregate_payload["controls"][0]
    orbit = branch_orbits()[0]
    form, H = orbit[0]
    aggregate_counts = Counter({decode_aggregate_type(d, h): count for d, h, count in first["counts"]})
    aggregate_counts[next(iter(aggregate_counts))] += 1
    mutated_aggregate_rejected = False
    try:
        check_aggregate_counts(grams()[form], H, aggregate_counts)
    except AssertionError:
        mutated_aggregate_rejected = True

    outcome = {
        "erased_farkas_rejected": erased_rejected,
        "reversed_farkas_orientation_rejected": reversed_rejected,
        "mutated_point_control_rejected": mutated_point_rejected,
        "mutated_aggregate_control_rejected": mutated_aggregate_rejected,
    }
    if not all(outcome.values()):
        raise AssertionError(outcome)
    return outcome


def build_result() -> dict[str, object]:
    frozen = verify_frozen_inputs()
    manifest = verify_source_manifest()
    forms = grams()
    subsets = tuple(accepted_subsets(D) for D in forms)
    orbits = branch_orbits()
    if [len(rows) for rows in subsets] != [83, 83, 83]:
        raise AssertionError("marked subset census differs")
    if len(orbits) != 24 or sum(map(len, orbits)) != 249 or Counter(map(len, orbits)) != Counter({3: 1, 6: 9, 12: 12, 24: 2}):
        raise AssertionError("branch orbit census differs")

    projector = verify_projector()
    point = verify_point_archive()
    aggregate = verify_aggregate_archive()
    source_results = json.loads(SOURCE_RESULTS.read_text(encoding="utf-8"))
    selected_union = verify_selected_union_controls(source_results)
    profiles, odd_weights = point_profile_census()
    if profiles != 872 or sum(odd_weights.values()) != 800:
        raise AssertionError("point coordinate profile census differs")

    source_point = source_results["point_signature_census"]
    if (source_point["feasible_orbits"], source_point["excluded_orbits"], source_point["surviving_labelled_branches"], source_point["excluded_labelled_branches"]) != (7, 17, 51, 198):
        raise AssertionError("source result summary differs from archive")
    if source_results["status"] != "UNKNOWN" or source_results["marked_branch_census"]["target_automorphism_assumed"] is not False:
        raise AssertionError("status wall or automorphism scope differs")

    # First-principles SRG/incidence algebra:
    # A^2=12I-A+2J and BB^T=A+7I imply, for Aq=-4q,
    # ||B^Tq||^2=168, B(B^Tq)=3q, and (B^TB-3I)B^Tq=0.
    algebra = {
        "srg_identity": "A^2=12I-A+2J",
        "incidence_identity": "BB^T=A+7I",
        "triangle_sum_norm": 168,
        "residual_223_norm": 96,
        "residual_223_sum": 0,
        "selected_sums": [-3 * sign for sign in SIGNS],
        "q_even_excluded": all((-3 * sign) % 2 == 1 for sign in SIGNS),
        "point_projector_diagonal": "44/99=4/9",
        "coordinate_bound": "q_x^2<=224/9<25, so integral |q_x|<=4",
        "projector_forms": projector,
    }

    return {
        "role": "verifier",
        "claim_label": "VERIFIED",
        "global_status": "UNKNOWN",
        "frozen_inputs": frozen,
        "source_manifest_entries_checked": len(manifest),
        "source_manifest_entries": manifest,
        "independent_algebra": algebra,
        "marked_branch_census": {
            "forms": [list(label) for label in FORM_LABELS],
            "subsets_per_form": [len(rows) for rows in subsets],
            "total_labelled_branches": 249,
            "orbits": 24,
            "orbit_size_distribution": {str(k): v for k, v in sorted(Counter(map(len, orbits)).items())},
            "maps_per_ordered_form_pair": 8,
            "target_automorphism_assumed": False,
        },
        "point_signature_certificates": point,
        "aggregate_controls": aggregate,
        "selected_union_controls": selected_union,
        "point_coordinate_profiles": {
            "before_odd_support_minimum": profiles,
            "after_odd_support_minimum": sum(odd_weights.values()),
            "odd_support_distribution": {str(k): v for k, v in sorted(odd_weights.items())},
        },
        "hostile_tests": hostile_tests(),
        "verdict": "PASS_NO_VETO",
        "limitations": [
            "All conclusions are conditional on the frozen hypothetical endpoint and one rank-four marked branch.",
            "The 51 surviving point-signature controls are anonymous row-count tables, not named graph points or adjacency.",
            "The aggregate controls do not impose the 223 residual rows of Ct=0 or a 231-block incidence frame.",
            "No 99-vertex graph, counterexample, nonexistence proof, endpoint exclusion, or global resolution is certified.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULTS.write_text(rendered, encoding="utf-8")
    if args.verify:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("independent result archive differs")
        print("PASS: independent Wave209 rank-four verifier")
    elif not args.write:
        print(rendered, end="")


if __name__ == "__main__":
    main()
