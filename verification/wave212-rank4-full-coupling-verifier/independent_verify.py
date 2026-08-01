#!/usr/bin/env python3
"""Clean-room exact verifier for the Wave 210 rank-four coupling claim.

The blind phase of this module depends only on the sealed Wave 209 verifier
inputs.  In particular, it does not import any discovery module.  It rebuilds
the seven surviving rank-four constraint orbits, all point signatures,
residual triangle types, and exact unordered three-point decompositions.

For a residual triangle R with line sum t_R and point-signature multiset
{s(x): x in R}, two point-star identities are imposed for every signature s:

  sum_R multiplicity_R(s) = (7 - number_of_minus_entries(s)) n_s,

  sum_R t_R multiplicity_R(s)
      = (3 q(s) + 3 sum_{i:s_i=-1} alpha_i) n_s.

The second identity is the signature-class sum of B t = 3 q after removing
the eight marked triangles, whose line sums are -3 alpha_i.  Both identities
are necessary conditions only.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "blind-results.json"
DUALS = HERE / "blind-duals.json"

Q = 3
ALPHA = (1, 1, 1, 1, -1, -1, -1, -1)
FORM_LABELS = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
M7G_COLUMNS = (
    (1, 2, 2, 2),
    (1, 0, 2, 2),
    (1, 2, 0, 2),
    (1, 2, 2, 0),
    (1, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
)
SYMMETRIC_POSITIONS = tuple((i, j) for i in range(4) for j in range(i, 4))
SURVIVING_ORBIT_IDS = (0, 2, 4, 11, 12, 14, 23)

Signature = tuple[int, ...]
Edge = tuple[int, int]
Branch = tuple[int, frozenset[Edge]]
ResidualType = tuple[tuple[int, ...], frozenset[int], int]
Decomposition = tuple[Signature, Signature, Signature]
Descriptor = tuple[object, ...]


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("ascii")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse_mod3(value: int) -> int:
    if value % 3 == 1:
        return 1
    if value % 3 == 2:
        return 2
    raise ZeroDivisionError("zero has no inverse modulo three")


def nullspace_mod3(rows: Iterable[Iterable[int]]) -> tuple[tuple[int, ...], ...]:
    matrix = [[entry % 3 for entry in row] for row in rows]
    if not matrix:
        return ()
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inverse_mod3(matrix[pivot_row][column])
        matrix[pivot_row] = [(scale * entry) % 3 for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (matrix[row][j] - scale * matrix[pivot_row][j]) % 3
                for j in range(len(matrix[0]))
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    basis: list[tuple[int, ...]] = []
    for free in (column for column in range(len(matrix[0])) if column not in pivot_columns):
        vector = [0] * len(matrix[0])
        vector[free] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free] % 3
        basis.append(tuple(vector))
    return tuple(basis)


def symmetric_form(coordinates: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    matrix = [[0] * 4 for _ in range(4)]
    for value, (i, j) in zip(coordinates, SYMMETRIC_POSITIONS):
        matrix[i][j] = matrix[j][i] = value % 3
    return tuple(tuple(row) for row in matrix)


def pairing(left: Sequence[int], form: Sequence[Sequence[int]], right: Sequence[int]) -> int:
    return sum(left[i] * form[i][j] * right[j] for i in range(4) for j in range(4)) % 3


@lru_cache(maxsize=1)
def grams() -> tuple[tuple[tuple[int, ...], ...], ...]:
    evaluation_rows = []
    for vector in M7G_COLUMNS:
        evaluation_rows.append(tuple(
            vector[i] * vector[j] * (1 if i == j else 2) % 3
            for i, j in SYMMETRIC_POSITIONS
        ))
    basis = nullspace_mod3(evaluation_rows)
    if len(basis) != 3:
        raise AssertionError("M7g vanishing-form space is not three-dimensional")
    labelled: dict[tuple[int, int, int], tuple[tuple[int, ...], ...]] = {}
    for weights in itertools.product(range(3), repeat=3):
        coordinates = tuple(
            sum(weights[k] * basis[k][j] for k in range(3)) % 3
            for j in range(10)
        )
        form = symmetric_form(coordinates)
        if any(pairing(vector, form, vector) for vector in M7G_COLUMNS):
            raise AssertionError("reconstructed form fails a vanishing equation")
        label = (form[1][1], form[2][2], form[3][3])
        labelled[label] = tuple(
            tuple(pairing(left, form, right) for right in M7G_COLUMNS)
            for left in M7G_COLUMNS
        )
    if len(labelled) != 27:
        raise AssertionError("form diagonal labels are not unique")
    return tuple(labelled[label] for label in FORM_LABELS)


def accepted_marked_intersections(D: Sequence[Sequence[int]]) -> tuple[frozenset[Edge], ...]:
    eligible = tuple((i, j) for i, j in itertools.combinations(range(8), 2) if D[i][j] == 1)
    if len(eligible) != 8:
        raise AssertionError("expected eight product-one pairs")
    accepted: list[frozenset[Edge]] = []
    for mask in range(1 << 8):
        selected = frozenset(edge for bit, edge in enumerate(eligible) if mask & (1 << bit))
        if sum(ALPHA[i] * ALPHA[j] for i, j in selected) % 3 != 1:
            continue
        degrees = [sum(i in edge for edge in selected) for i in range(8)]
        if max(degrees) > 3:
            raise AssertionError("marked triangle degree exceeds three")
        residues = [
            value % 3
            for value in (
                [ALPHA[i] + ALPHA[j] for i, j in selected]
                + [ALPHA[i] for i in range(8) for _ in range(3 - degrees[i])]
            )
        ]
        weight = sum(value != 0 for value in residues)
        if weight not in {14, 17, 20, 23}:
            continue
        if weight == 14 and (residues.count(1), residues.count(2)) != (7, 7):
            continue
        accepted.append(selected)
    return tuple(accepted)


@lru_cache(maxsize=1)
def sign_preserving_permutations() -> tuple[tuple[int, ...], ...]:
    return tuple(
        positive + negative
        for positive in itertools.permutations(range(4))
        for negative in itertools.permutations(range(4, 8))
    )


def form_maps(source: Sequence[Sequence[int]], target: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in sign_preserving_permutations()
        if all(source[i][j] == target[permutation[i]][permutation[j]] for i in range(8) for j in range(8))
    )


def permute_edges(edges: frozenset[Edge], permutation: Sequence[int]) -> frozenset[Edge]:
    return frozenset(tuple(sorted((permutation[i], permutation[j]))) for i, j in edges)


@lru_cache(maxsize=1)
def branch_orbits() -> tuple[tuple[Branch, ...], ...]:
    forms = grams()
    accepted = tuple(accepted_marked_intersections(form) for form in forms)
    nodes = {(form_index, edges) for form_index in range(3) for edges in accepted[form_index]}
    maps = {
        (source, target): form_maps(forms[source], forms[target])
        for source in range(3)
        for target in range(3)
    }
    if any(len(permutations) != 8 for permutations in maps.values()):
        raise AssertionError("ordered form pair does not have eight data isomorphisms")
    unseen = set(nodes)
    output: list[tuple[Branch, ...]] = []
    while unseen:
        seed = min(unseen, key=lambda node: (node[0], tuple(sorted(node[1]))))
        orbit: set[Branch] = set()
        frontier = [seed]
        while frontier:
            form_index, edges = frontier.pop()
            if (form_index, edges) in orbit:
                continue
            orbit.add((form_index, edges))
            for target in range(3):
                for permutation in maps[(form_index, target)]:
                    image = (target, permute_edges(edges, permutation))
                    if image in nodes and image not in orbit:
                        frontier.append(image)
        unseen -= orbit
        output.append(tuple(sorted(orbit, key=lambda node: (node[0], tuple(sorted(node[1]))))))
    flattened = [branch for orbit in output for branch in orbit]
    if len(flattened) != 249 or len(set(flattened)) != 249 or len(output) != 24:
        raise AssertionError("rank-four branch partition differs from Wave 209 seal")
    return tuple(output)


def decode_signature(code: int) -> Signature:
    if not 0 <= code < 3**8:
        raise ValueError("signature code is outside eight trits")
    values = []
    for _ in range(8):
        values.append(code % 3 - 1)
        code //= 3
    return tuple(values)


def encode_signature(signature: Sequence[int]) -> int:
    if len(signature) != 8 or any(value not in {-1, 0, 1} for value in signature):
        raise ValueError("not an eight-coordinate point signature")
    return sum((value + 1) * 3**i for i, value in enumerate(signature))


@lru_cache(maxsize=1)
def point_signatures() -> tuple[Signature, ...]:
    output = tuple(
        signature
        for code in range(3**8)
        for signature in (decode_signature(code),)
        if sum(ALPHA[i] * signature[i] for i in range(8)) % 3 == 0
    )
    if len(output) != 2187 or len(set(output)) != 2187:
        raise AssertionError("admissible point-signature census differs")
    return output


def q_value(signature: Signature) -> int:
    numerator = sum(ALPHA[i] * signature[i] for i in range(8))
    if numerator % 3:
        raise AssertionError("nonintegral q value")
    return numerator // 3


def point_pair_table(D: Sequence[Sequence[int]], H: frozenset[Edge], i: int, j: int) -> dict[tuple[int, int], int]:
    if (i, j) in H:
        return {
            (-1, -1): 1, (-1, 0): 0, (-1, 1): 2,
            (0, -1): 0, (0, 0): 40, (0, 1): 20,
            (1, -1): 2, (1, 0): 20, (1, 1): 14,
        }
    value = D[i][j]
    return {
        (-1, -1): 0, (-1, 0): 3 - value, (-1, 1): value,
        (0, -1): 3 - value, (0, 0): 39 - 3 * value, (0, 1): 18 + 4 * value,
        (1, -1): value, (1, 0): 18 + 4 * value, (1, 1): 18 - 5 * value,
    }


@lru_cache(maxsize=1)
def point_descriptors() -> tuple[Descriptor, ...]:
    output: list[Descriptor] = [("total",)]
    output.extend(("margin", i, value) for i in range(8) for value in (-1, 0, 1))
    output.extend(
        ("pair", i, j, left, right)
        for i, j in itertools.combinations(range(8), 2)
        for left in (-1, 0, 1)
        for right in (-1, 0, 1)
    )
    output.extend((("qsum",), ("qnorm",)))
    if len(output) != 279:
        raise AssertionError("point equation universe does not have 279 rows")
    return tuple(output)


def point_feature(descriptor: Descriptor, signature: Signature) -> int:
    kind = descriptor[0]
    if kind == "total":
        return 1
    if kind == "margin":
        return int(signature[descriptor[1]] == descriptor[2])
    if kind == "pair":
        return int(signature[descriptor[1]] == descriptor[3] and signature[descriptor[2]] == descriptor[4])
    if kind == "qsum":
        return q_value(signature)
    if kind == "qnorm":
        return q_value(signature) ** 2
    raise AssertionError(descriptor)


def point_targets(D: Sequence[Sequence[int]], H: frozenset[Edge]) -> dict[Descriptor, int]:
    output: dict[Descriptor, int] = {("total",): 99, ("qsum",): 0, ("qnorm",): 56}
    for i in range(8):
        output[("margin", i, -1)] = 3
        output[("margin", i, 0)] = 60
        output[("margin", i, 1)] = 36
    for i, j in itertools.combinations(range(8), 2):
        table = point_pair_table(D, H, i, j)
        for left in (-1, 0, 1):
            for right in (-1, 0, 1):
                output[("pair", i, j, left, right)] = table[(left, right)]
    if set(output) != set(point_descriptors()):
        raise AssertionError("point target universe differs")
    return output


def row_space(D: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    output = {
        tuple(sum(coefficients[k] * D[k][i] for k in range(8)) % 3 for i in range(8))
        for coefficients in itertools.product(range(3), repeat=8)
    }
    if len(output) != 81:
        raise AssertionError("rank-four residual evaluation code does not have 81 words")
    return tuple(sorted(output))


def residual_types(D: Sequence[Sequence[int]], H: frozenset[Edge]) -> tuple[ResidualType, ...]:
    output: list[ResidualType] = []
    for d in row_space(D):
        ones = tuple(i for i, value in enumerate(d) if value == 1)
        for mask in range(1 << len(ones)):
            h = frozenset(ones[bit] for bit in range(len(ones)) if mask & (1 << bit))
            h_degrees = {i: 0 for i in h}
            selected_edges = 0
            allowed = True
            for i, j in itertools.combinations(sorted(h), 2):
                if (i, j) in H:
                    h_degrees[i] += 1
                    h_degrees[j] += 1
                    selected_edges += 1
                    if h_degrees[i] > 1 or h_degrees[j] > 1:
                        allowed = False
                        break
                elif D[i][j] == 0:
                    allowed = False
                    break
            if not allowed or len(h) - selected_edges > 3:
                continue
            numerator = sum(ALPHA[i] * d[i] for i in range(8))
            if numerator % 3:
                raise AssertionError("residual line sum is nonintegral")
            output.append((d, h, numerator // 3))
    if len(output) != len(set(output)):
        raise AssertionError("duplicate residual triangle type")
    return tuple(output)


@lru_cache(maxsize=1)
def aggregate_descriptors() -> tuple[Descriptor, ...]:
    output: list[Descriptor] = [("total",)]
    output.extend(("d", i, value) for i in range(8) for value in (0, 1, 2))
    output.extend(("dproduct", i, j) for i, j in itertools.combinations(range(8), 2))
    output.extend((("tsum",), ("tnorm",)))
    output.extend(descriptor for i in range(8) for descriptor in (("hit", i), ("hit_t", i)))
    output.extend(("hit_pair", i, j) for i, j in itertools.combinations(range(8), 2))
    if len(output) != 99:
        raise AssertionError("aggregate equation universe does not have 99 rows")
    return tuple(output)


def residual_pair_count(D: Sequence[Sequence[int]], H: frozenset[Edge], i: int, j: int) -> int:
    if (i, j) in H:
        return 5
    selected_common = sum(
        tuple(sorted((i, k))) in H and tuple(sorted((j, k))) in H
        for k in range(8)
        if k not in (i, j)
    )
    return D[i][j] - selected_common


def aggregate_targets(D: Sequence[Sequence[int]], H: frozenset[Edge]) -> dict[Descriptor, int]:
    output: dict[Descriptor, int] = {("total",): 223, ("tsum",): 0, ("tnorm",): 96}
    for i in range(8):
        for value, full_count in ((0, 32), (1, 162), (2, 36)):
            output[("d", i, value)] = full_count - sum(D[k][i] == value for k in range(8) if k != i)
    F = tuple(tuple(-3 if i == j else D[i][j] for j in range(8)) for i in range(8))
    for i, j in itertools.combinations(range(8), 2):
        output[("dproduct", i, j)] = 252 - 21 * D[i][j] - sum(F[k][i] * F[k][j] for k in range(8))
    degrees = [sum(i in edge for edge in H) for i in range(8)]
    for i in range(8):
        output[("hit", i)] = 18 - degrees[i]
        output[("hit_t", i)] = 3 * sum(ALPHA[j] for j in range(8) if tuple(sorted((i, j))) in H)
    for i, j in itertools.combinations(range(8), 2):
        count = residual_pair_count(D, H, i, j)
        if count < 0:
            raise AssertionError("negative residual selected-intersection pair count")
        output[("hit_pair", i, j)] = count
    if set(output) != set(aggregate_descriptors()):
        raise AssertionError("aggregate target universe differs")
    return output


def aggregate_feature(descriptor: Descriptor, triangle_type: ResidualType) -> int:
    d, h, t = triangle_type
    kind = descriptor[0]
    if kind == "total":
        return 1
    if kind == "d":
        return int(d[descriptor[1]] == descriptor[2])
    if kind == "dproduct":
        return d[descriptor[1]] * d[descriptor[2]]
    if kind == "tsum":
        return t
    if kind == "tnorm":
        return t * t
    if kind == "hit":
        return int(descriptor[1] in h)
    if kind == "hit_t":
        return t * int(descriptor[1] in h)
    if kind == "hit_pair":
        return int(descriptor[1] in h and descriptor[2] in h)
    raise AssertionError(descriptor)


@lru_cache(maxsize=None)
def exact_decompositions(d: tuple[int, ...], h_tuple: tuple[int, ...]) -> tuple[Decomposition, ...]:
    """Return every unordered three-signature decomposition of one type."""
    h = frozenset(h_tuple)
    coordinate_options: list[tuple[tuple[int, int, int], ...]] = []
    for i, value in enumerate(d):
        if i in h:
            labelled = (-1, 1, 1)
        elif value == 0:
            labelled = (0, 0, 0)
        elif value == 1:
            labelled = (1, 0, 0)
        elif value == 2:
            labelled = (1, 1, 0)
        else:
            raise AssertionError("residual polar coordinate outside F3 representatives")
        coordinate_options.append(tuple(sorted(set(itertools.permutations(labelled)))))
    admissible = set(point_signatures())
    output: set[Decomposition] = set()
    for assignments in itertools.product(*coordinate_options):
        labelled_signatures = tuple(
            tuple(assignments[i][point] for i in range(8))
            for point in range(3)
        )
        if all(signature in admissible for signature in labelled_signatures):
            output.add(tuple(sorted(labelled_signatures, key=encode_signature)))
    return tuple(sorted(output, key=lambda triple: tuple(map(encode_signature, triple))))


def star_count_multiplier(signature: Signature) -> int:
    return 7 - signature.count(-1)


def star_t_multiplier(signature: Signature) -> int:
    return 3 * q_value(signature) + 3 * sum(ALPHA[i] for i, value in enumerate(signature) if value == -1)


def encode_d(d: Sequence[int]) -> int:
    return sum(value * 3**i for i, value in enumerate(d))


def encode_h(h: Iterable[int]) -> int:
    return sum(1 << i for i in h)


@dataclass(frozen=True)
class SparseColumn:
    descriptor: tuple[object, ...]
    entries: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ExactSystem:
    orbit_id: int
    form_index: int
    selected_edges: frozenset[Edge]
    row_descriptors: tuple[tuple[object, ...], ...]
    rhs: tuple[int, ...]
    columns: tuple[SparseColumn, ...]
    residual_type_count: int
    decomposition_count: int
    w_column_count: int
    x_column_count: int


def add_entry(entries: dict[int, int], row: int, value: int) -> None:
    if value:
        entries[row] = entries.get(row, 0) + value
        if entries[row] == 0:
            del entries[row]


def build_exact_system(orbit_id: int) -> ExactSystem:
    if orbit_id not in SURVIVING_ORBIT_IDS:
        raise ValueError("not one of the seven sealed Wave 209 survivor orbits")
    form_index, H = branch_orbits()[orbit_id][0]
    D = grams()[form_index]
    signatures = point_signatures()
    signature_index = {signature: index for index, signature in enumerate(signatures)}
    aggregate_rows = aggregate_descriptors()
    point_rows = point_descriptors()
    aggregate_offset = 0
    point_offset = len(aggregate_rows)
    star_offset = point_offset + len(point_rows)
    star_t_offset = star_offset + len(signatures)
    row_descriptors = tuple(
        [("aggregate", *descriptor) for descriptor in aggregate_rows]
        + [("point", *descriptor) for descriptor in point_rows]
        + [("star_count", encode_signature(signature)) for signature in signatures]
        + [("star_t", encode_signature(signature)) for signature in signatures]
    )
    aggregate_rhs = aggregate_targets(D, H)
    point_rhs = point_targets(D, H)
    rhs = tuple(
        [aggregate_rhs[descriptor] for descriptor in aggregate_rows]
        + [point_rhs[descriptor] for descriptor in point_rows]
        + [0] * (2 * len(signatures))
    )

    triangle_types = residual_types(D, H)
    columns: list[SparseColumn] = []
    decomposition_count = 0
    for triangle_type in triangle_types:
        d, h, t = triangle_type
        decompositions = exact_decompositions(d, tuple(sorted(h)))
        decomposition_count += len(decompositions)
        for decomposition in decompositions:
            entries: dict[int, int] = {}
            for row, descriptor in enumerate(aggregate_rows, start=aggregate_offset):
                add_entry(entries, row, aggregate_feature(descriptor, triangle_type))
            for signature, multiplicity in Counter(decomposition).items():
                index = signature_index[signature]
                add_entry(entries, star_offset + index, multiplicity)
                add_entry(entries, star_t_offset + index, t * multiplicity)
            descriptor = (
                "W",
                encode_d(d),
                encode_h(h),
                *(encode_signature(signature) for signature in decomposition),
            )
            columns.append(SparseColumn(descriptor, tuple(sorted(entries.items()))))

    w_column_count = len(columns)
    for index, signature in enumerate(signatures):
        entries: dict[int, int] = {}
        for row_delta, descriptor in enumerate(point_rows):
            add_entry(entries, point_offset + row_delta, point_feature(descriptor, signature))
        add_entry(entries, star_offset + index, -star_count_multiplier(signature))
        add_entry(entries, star_t_offset + index, -star_t_multiplier(signature))
        columns.append(SparseColumn(("X", encode_signature(signature)), tuple(sorted(entries.items()))))

    if len(row_descriptors) != 99 + 279 + 2 * 2187:
        raise AssertionError("full row universe size differs")
    if len(set(row_descriptors)) != len(row_descriptors):
        raise AssertionError("duplicate canonical row descriptor")
    if len({column.descriptor for column in columns}) != len(columns):
        raise AssertionError("duplicate canonical column descriptor")
    if decomposition_count != w_column_count:
        raise AssertionError("one W column was not emitted per decomposition")
    return ExactSystem(
        orbit_id=orbit_id,
        form_index=form_index,
        selected_edges=H,
        row_descriptors=row_descriptors,
        rhs=rhs,
        columns=tuple(columns),
        residual_type_count=len(triangle_types),
        decomposition_count=decomposition_count,
        w_column_count=w_column_count,
        x_column_count=len(signatures),
    )


def system_hashes(system: ExactSystem) -> dict[str, str]:
    row_hasher = hashlib.sha256()
    w_hasher = hashlib.sha256()
    x_hasher = hashlib.sha256()
    full_hasher = hashlib.sha256()
    header = ["wave212-rank4-coupling-canonical-v1", system.orbit_id]
    full_hasher.update(canonical_json(header))
    for index, (descriptor, rhs) in enumerate(zip(system.row_descriptors, system.rhs)):
        record = [index, descriptor, rhs]
        payload = canonical_json(record)
        row_hasher.update(payload)
        full_hasher.update(b"R")
        full_hasher.update(payload)
    for index, column in enumerate(system.columns):
        record = [index, column.descriptor, column.entries]
        payload = canonical_json(record)
        (w_hasher if column.descriptor[0] == "W" else x_hasher).update(payload)
        full_hasher.update(b"C")
        full_hasher.update(payload)
    return {
        "row_universe_sha256": row_hasher.hexdigest(),
        "w_columns_sha256": w_hasher.hexdigest(),
        "x_columns_sha256": x_hasher.hexdigest(),
        "full_system_sha256": full_hasher.hexdigest(),
    }


def to_scipy_csc(system: ExactSystem):
    import numpy as np
    from scipy.sparse import csc_matrix

    rows: list[int] = []
    columns: list[int] = []
    values: list[int] = []
    for column_index, column in enumerate(system.columns):
        for row, value in column.entries:
            rows.append(row)
            columns.append(column_index)
            values.append(value)
    return csc_matrix(
        (np.asarray(values, dtype=np.float64), (rows, columns)),
        shape=(len(system.row_descriptors), len(system.columns)),
    )


def primal_status(system: ExactSystem) -> dict[str, object]:
    """Use a floating solver only as a discovery oracle, never as evidence."""
    import numpy as np
    from scipy.optimize import linprog

    matrix = to_scipy_csc(system)
    result = linprog(
        np.zeros(matrix.shape[1]),
        A_eq=matrix,
        b_eq=np.asarray(system.rhs, dtype=np.float64),
        bounds=(0, None),
        method="highs",
    )
    return {"status": int(result.status), "message": str(result.message)}


def exact_dual_extremes(system: ExactSystem, coefficients: dict[int, int]) -> tuple[int, int, int]:
    if not coefficients or any(
        not isinstance(row, int)
        or not 0 <= row < len(system.row_descriptors)
        or not isinstance(value, int)
        or value == 0
        for row, value in coefficients.items()
    ):
        raise AssertionError("dual coefficients are empty, malformed, or nonintegral")
    rhs = sum(coefficients.get(row, 0) * value for row, value in enumerate(system.rhs))
    column_values = [
        sum(coefficients.get(row, 0) * value for row, value in column.entries)
        for column in system.columns
    ]
    minimum = min(column_values)
    maximum = max(column_values)
    if minimum < 0 or rhs >= 0:
        raise AssertionError((system.orbit_id, minimum, rhs))
    return minimum, maximum, rhs


def discover_integer_dual(system: ExactSystem) -> dict[str, object]:
    """Find a floating ray, pad it into the cone interior, then check integers.

    The floating solve is only a discovery device.  Row 0 is the aggregate
    total and row 99 is the point total.  Their sum evaluates to exactly one
    on every W and every X column.  Adding 1/1000 of that vector therefore
    gives a strict column margin while changing the normalized right-hand
    side from -1 to -1 + (223+99)/1000 = -339/500.  Rounding after scaling by
    10,000 is accepted only if a fresh all-integer replay proves every column
    inequality and the strict right-hand-side sign.
    """
    import numpy as np
    from scipy.optimize import linprog

    if system.row_descriptors[0] != ("aggregate", "total"):
        raise AssertionError("aggregate total row moved")
    if system.row_descriptors[99] != ("point", "total"):
        raise AssertionError("point total row moved")
    for column in system.columns:
        values = dict(column.entries)
        padding_value = values.get(0, 0) + values.get(99, 0)
        if padding_value != 1:
            raise AssertionError((column.descriptor, padding_value))

    matrix = to_scipy_csc(system)
    rhs = np.asarray(system.rhs, dtype=np.float64)
    result = linprog(
        np.zeros(matrix.shape[0]),
        A_ub=-matrix.T,
        b_ub=np.zeros(matrix.shape[1]),
        A_eq=rhs.reshape(1, -1),
        b_eq=np.asarray([-1.0]),
        bounds=(None, None),
        method="highs",
    )
    if result.status != 0 or result.x is None:
        raise RuntimeError(f"dual discovery oracle failed: {result.message}")
    padded = result.x.copy()
    padded[0] += 1 / 1000
    padded[99] += 1 / 1000
    integral = np.rint(10_000 * padded)
    if not np.all(np.isfinite(integral)):
        raise AssertionError("nonfinite rounded dual")
    coefficients = {
        int(row): int(value)
        for row, value in enumerate(integral.tolist())
        if int(value)
    }
    common = 0
    for value in coefficients.values():
        common = math.gcd(common, abs(value))
    if common > 1:
        coefficients = {row: value // common for row, value in coefficients.items()}
    minimum, maximum, exact_rhs = exact_dual_extremes(system, coefficients)
    return {
        "orbit_id": system.orbit_id,
        "full_system_sha256": system_hashes(system)["full_system_sha256"],
        "coefficients": [[row, coefficients[row]] for row in sorted(coefficients)],
        "support_size": len(coefficients),
        "pointwise_minimum": minimum,
        "pointwise_maximum": maximum,
        "rhs": exact_rhs,
        "discovery_note": "floating normalized ray plus exact all-column interior padding; only integer replay is evidence",
    }


def write_blind_duals() -> dict[str, object]:
    payload = {
        "format": "wave212-rank4-full-coupling-blind-duals-v1",
        "orientation": "A^T y >= 0 and b^T y < 0",
        "padding_identity": "aggregate_total + point_total evaluates to 1 on every W/X column",
        "certificates": [
            discover_integer_dual(build_exact_system(orbit_id))
            for orbit_id in SURVIVING_ORBIT_IDS
        ],
    }
    DUALS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return payload


def replay_blind_duals() -> dict[str, object]:
    payload = json.loads(DUALS.read_text(encoding="utf-8"))
    if payload.get("format") != "wave212-rank4-full-coupling-blind-duals-v1":
        raise AssertionError("blind dual archive format differs")
    if [item.get("orbit_id") for item in payload.get("certificates", [])] != list(SURVIVING_ORBIT_IDS):
        raise AssertionError("blind dual orbit order differs")
    summaries = []
    for item in payload["certificates"]:
        system = build_exact_system(item["orbit_id"])
        if item["full_system_sha256"] != system_hashes(system)["full_system_sha256"]:
            raise AssertionError("dual is pinned to a different system")
        coefficients: dict[int, int] = {}
        for row, value in item["coefficients"]:
            if row in coefficients:
                raise AssertionError("duplicate dual row")
            coefficients[row] = value
        minimum, maximum, rhs = exact_dual_extremes(system, coefficients)
        expected = (item["pointwise_minimum"], item["pointwise_maximum"], item["rhs"])
        if (minimum, maximum, rhs) != expected or len(coefficients) != item["support_size"]:
            raise AssertionError("blind dual summary differs")
        summaries.append({
            "orbit_id": system.orbit_id,
            "support_size": len(coefficients),
            "pointwise_minimum": minimum,
            "pointwise_maximum": maximum,
            "rhs": rhs,
        })
    return {"certificates": summaries, "all_exact": True}


def build_blind_summary(include_solver_status: bool = False) -> dict[str, object]:
    orbit_partition = branch_orbits()
    if [len(accepted_marked_intersections(form)) for form in grams()] != [83, 83, 83]:
        raise AssertionError("marked branch count differs")
    summary: dict[str, object] = {
        "format": "wave212-rank4-full-coupling-blind-v1",
        "role": "verifier",
        "claim_label": "CANDIDATE",
        "global_status": "UNKNOWN",
        "target_automorphism_assumed": False,
        "point_signature_count": len(point_signatures()),
        "row_count": 99 + 279 + 2 * len(point_signatures()),
        "branch_orbits": len(orbit_partition),
        "labelled_branches": sum(map(len, orbit_partition)),
        "surviving_orbit_ids": list(SURVIVING_ORBIT_IDS),
        "surviving_labelled_branches": sum(len(orbit_partition[index]) for index in SURVIVING_ORBIT_IDS),
        "systems": [],
    }
    for orbit_id in SURVIVING_ORBIT_IDS:
        system = build_exact_system(orbit_id)
        item: dict[str, object] = {
            "orbit_id": orbit_id,
            "branch_count": len(orbit_partition[orbit_id]),
            "form_index": system.form_index,
            "form_diagonal": list(FORM_LABELS[system.form_index]),
            "selected_intersections": [list(edge) for edge in sorted(system.selected_edges)],
            "residual_type_count": system.residual_type_count,
            "decomposition_count": system.decomposition_count,
            "row_count": len(system.row_descriptors),
            "w_column_count": system.w_column_count,
            "x_column_count": system.x_column_count,
            "column_count": len(system.columns),
            "nonzero_count": sum(len(column.entries) for column in system.columns),
            **system_hashes(system),
        }
        if include_solver_status:
            item["discovery_solver_status_not_evidence"] = primal_status(system)
        summary["systems"].append(item)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-blind", action="store_true")
    parser.add_argument("--verify-blind", action="store_true")
    parser.add_argument("--write-duals", action="store_true")
    parser.add_argument("--verify-duals", action="store_true")
    parser.add_argument("--solver-status", action="store_true")
    args = parser.parse_args()
    if args.write_duals:
        payload = write_blind_duals()
        print(json.dumps({"written": str(DUALS), "certificates": len(payload["certificates"])}, sort_keys=True))
        return
    if args.verify_duals:
        print(json.dumps(replay_blind_duals(), indent=2, sort_keys=True))
        return
    result = build_blind_summary(include_solver_status=args.solver_status)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_blind:
        RESULTS.write_text(rendered, encoding="utf-8", newline="\n")
    elif args.verify_blind:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("blind result archive differs")
        print("PASS: Wave212 blind reconstruction matches archive")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
