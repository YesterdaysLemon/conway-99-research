"""Exact Wave 206 proof-B checks over F_3.

This package has three purposes.

1. It makes the fixed-middle-center compression coordinates explicit.
2. It records global crossing/localizer identities and their exact rank bounds.
3. It supplies hostile controls for two invalid inferences:
   ambient nondegeneracy need not survive restriction to a feature span, and
   rank <= 21 for every three-center slice need not bound the fourth-trace
   matrix H by 21.

The controls are not graph or endpoint realizations.  Their missing premises
are emitted in the machine-readable result.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


FIELD = 3
ROOT = Path(__file__).resolve().parents[2]
EXPECTED_INPUTS = {
    "attempts/wave206-three-center-global-extension/protocol.md":
        "66c20334e284a26cc771ee86d97e678cb67b6efb4648b2af2fffe480fb5a9103",
    "verification/2026-07-29-wave205-integration-audit.md":
        "f50b5591cb0e1e3dfdd835a22fd9156dd3a2a039323388889a6fa5e756a0a297",
    "verification/2026-07-29-wave205-orchestrator.md":
        "9b9711ad4b9ac902161833b4a5825404e95ba6f443462ac3d79532df704b2deb",
    "verification/wave205-fourth-trace-globalization-verifier/package-manifest.sha256":
        "b93f65f72db94539c7d42d7eca6debbaf3a5c4a401db3b812a80549bcb9b8325",
    "attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256":
        "2c9976b6cb07a3036df07fd0e7ceb7ffce6a339651d604fcecdcf8c0c3da3d96",
    "attempts/wave205-global-fourth-moment-proof-b/package-manifest.sha256":
        "a91a2a1cdbc129fa66e9d63b34031a774d5af78c458d18d9a1aadd7e4be217e7",
    "attempts/wave205-fourth-trace-globalization/protocol.md":
        "a1d45fc0a82b9944a9e020ded3945e75944e0e00202eacbb20eb05598e30bf4d",
    "agents/2026-07-29-wave191-global-star-module-proof-b.md":
        "afe7d35627ec14a9599b427bcca0751e86a3f32b71fb7baf4d91e9e2e335f75f",
}

Matrix = list[list[int]]


def mod(value: int) -> int:
    return value % FIELD


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs() -> dict[str, str]:
    observed = {
        relative: sha256(ROOT / relative) for relative in EXPECTED_INPUTS
    }
    if observed != EXPECTED_INPUTS:
        raise AssertionError({"expected": EXPECTED_INPUTS, "observed": observed})
    return observed


def identity(size: int) -> Matrix:
    return [[int(row == column) for column in range(size)] for row in range(size)]


def zero(rows: int, columns: int) -> Matrix:
    return [[0] * columns for _ in range(rows)]


def diagonal(entries: Iterable[int]) -> Matrix:
    values = [mod(value) for value in entries]
    return [
        [values[row] if row == column else 0 for column in range(len(values))]
        for row in range(len(values))
    ]


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            mod(left[row][column] + right[row][column])
            for column in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def scalar_matrix(scalar: int, matrix: Matrix) -> Matrix:
    return [[mod(scalar * entry) for entry in row] for row in matrix]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix shape mismatch")
    right_t = transpose(right)
    return [
        [
            mod(sum(a * b for a, b in zip(left_row, right_column)))
            for right_column in right_t
        ]
        for left_row in left
    ]


def matrix_trace(matrix: Matrix) -> int:
    return mod(sum(matrix[index][index] for index in range(len(matrix))))


def flatten(matrix: Matrix) -> list[int]:
    return [entry for row in matrix for entry in row]


def gf3_rref(matrix: Matrix) -> tuple[Matrix, list[int]]:
    if not matrix:
        return [], []
    rows = [[mod(entry) for entry in row] for row in matrix]
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("ragged matrix")
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        source = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column]
            ),
            None,
        )
        if source is None:
            continue
        rows[pivot_row], rows[source] = rows[source], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, FIELD)
        rows[pivot_row] = [mod(inverse * entry) for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                mod(rows[row][index] - multiplier * rows[pivot_row][index])
                for index in range(width)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def gf3_rank(matrix: Matrix) -> int:
    return len(gf3_rref(matrix)[1])


def gf3_nullspace(matrix: Matrix) -> Matrix:
    rref, pivots = gf3_rref(matrix)
    width = len(matrix[0])
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = mod(-rref[row][free_column])
        basis.append(vector)
    return basis


def gf3_determinant(matrix: Matrix) -> int:
    rows = [[mod(entry) for entry in row] for row in matrix]
    size = len(rows)
    if any(len(row) != size for row in rows):
        raise ValueError("determinant needs a square matrix")
    determinant = 1
    for column in range(size):
        source = next(
            (row for row in range(column, size) if rows[row][column]),
            None,
        )
        if source is None:
            return 0
        if source != column:
            rows[column], rows[source] = rows[source], rows[column]
            determinant = mod(-determinant)
        pivot = rows[column][column]
        determinant = mod(determinant * pivot)
        inverse = pow(pivot, -1, FIELD)
        rows[column] = [mod(inverse * value) for value in rows[column]]
        for row in range(column + 1, size):
            multiplier = rows[row][column]
            if multiplier:
                rows[row] = [
                    mod(rows[row][index] - multiplier * rows[column][index])
                    for index in range(size)
                ]
    return determinant


def distribution(values: Iterable[int]) -> dict[str, int]:
    return {
        str(value): count for value, count in sorted(Counter(values).items())
    }


# The canonical six-space for one seven-column star.
STAR_FORM = [
    [0 if row == column else 1 for column in range(6)]
    for row in range(6)
]
STAR_FORM_INVERSE = gf3_rref(
    [
        STAR_FORM[row] + identity(6)[row]
        for row in range(6)
    ]
)[0]
STAR_FORM_INVERSE = [row[6:] for row in STAR_FORM_INVERSE]
STAR_COLUMNS = [
    [int(row == column) for column in range(6)] + [2]
    for row in range(6)
]
STAR_EDGES = [
    (left, right)
    for left in range(7)
    for right in range(left + 1, 7)
]
EDGE_INCIDENCE = [
    [int(vertex in edge) for edge in STAR_EDGES]
    for vertex in range(7)
]
J_STAR = matrix_add(
    matrix_multiply(transpose(EDGE_INCIDENCE), EDGE_INCIDENCE),
    scalar_matrix(2, identity(21)),
)


def star_bilinear_matrix(off_diagonal: list[int]) -> Matrix:
    if len(off_diagonal) != 21:
        raise ValueError("a star operator needs 21 off-diagonal coordinates")
    matrix = zero(7, 7)
    for value, (left, right) in zip(off_diagonal, STAR_EDGES):
        matrix[left][right] = mod(value)
        matrix[right][left] = mod(value)
    for vertex in range(7):
        matrix[vertex][vertex] = mod(-sum(matrix[vertex]))
    return matrix


def star_operator(off_diagonal: list[int]) -> Matrix:
    """Return A with N=Z^* A Z and the requested off-diagonal N entries."""

    bilinear = star_bilinear_matrix(off_diagonal)
    leading = [row[:6] for row in bilinear[:6]]
    return matrix_multiply(STAR_FORM_INVERSE, leading)


def trace_pair(left: Matrix, right: Matrix) -> int:
    return matrix_trace(matrix_multiply(left, right))


def star_coordinate_summary() -> dict[str, Any]:
    expected_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    actual_gram = matrix_multiply(
        matrix_multiply(transpose(STAR_COLUMNS), STAR_FORM),
        STAR_COLUMNS,
    )
    if actual_gram != expected_gram:
        raise AssertionError("canonical star Gram changed")

    coordinate_operators = []
    for coordinate in range(21):
        vector = [0] * 21
        vector[coordinate] = 1
        operator = star_operator(vector)
        if matrix_multiply(transpose(operator), STAR_FORM) != (
            matrix_multiply(STAR_FORM, operator)
        ):
            raise AssertionError("coordinate operator is not self-adjoint")
        coordinate_operators.append(operator)
    if gf3_rank([flatten(operator) for operator in coordinate_operators]) != 21:
        raise AssertionError("star coordinates lost injectivity")

    trace_form = [
        [trace_pair(left, right) for right in coordinate_operators]
        for left in coordinate_operators
    ]
    if trace_form != J_STAR:
        raise AssertionError("J_star formula changed")
    if gf3_rank(J_STAR) != 21 or gf3_determinant(J_STAR) != 2:
        raise AssertionError("J_star is no longer nondegenerate")

    trace_vector = [matrix_trace(operator) for operator in coordinate_operators]
    if trace_vector != [2] * 21:
        raise AssertionError("trace(A)=2 sum r_e formula changed")
    trace_zero_basis = gf3_nullspace([trace_vector])
    if len(trace_zero_basis) != 20:
        raise AssertionError("trace-zero coordinate dimension changed")
    restricted_form = matrix_multiply(
        matrix_multiply(trace_zero_basis, J_STAR),
        transpose(trace_zero_basis),
    )
    if gf3_rank(restricted_form) != 19:
        raise AssertionError("trace-zero radical rank changed")

    identity_coordinates = [1] * 21
    identity_operator = star_operator(identity_coordinates)
    if identity_operator != identity(6):
        raise AssertionError("identity coordinates changed")
    identity_pairing = [
        mod(sum(identity_coordinates[left] * J_STAR[left][right]
                for left in range(21)))
        for right in range(21)
    ]
    if identity_pairing != trace_vector:
        raise AssertionError("<I,A>=tr(A) changed")
    if mod(sum(
        identity_coordinates[left] * J_STAR[left][right]
        * identity_coordinates[right]
        for left in range(21)
        for right in range(21)
    )) != 0:
        raise AssertionError("I should be isotropic in dimension six")

    # Hostile one-feature example: ambient J_star is nondegenerate, but the
    # restricted Gram on span{I} is zero although I is a nonzero operator.
    identity_feature_rank = gf3_rank([identity_coordinates])
    identity_gram_rank = gf3_rank([[trace_pair(identity_operator, identity_operator)]])

    return {
        "star_dimension": 6,
        "star_columns": 7,
        "star_gram": "J_7-I_7",
        "self_adjoint_operator_dimension": 21,
        "coordinate_convention": (
            "r_ij=<z_i,A z_j> for 0<=i<j<=6; "
            "N_ii=-sum_(j!=i) r_ij"
        ),
        "coordinate_map_rank": 21,
        "trace_formula": "tr(A)=2 sum_(i<j) r_ij",
        "trace_square_formula": "tr(A^2)=r^T J_star r",
        "trace_pair_formula": "tr(AB)=r(A)^T J_star r(B)",
        "J_star_formula": "J_star=C^T C+2I_21, C=vertex-edge incidence of K_7",
        "J_star_rank": gf3_rank(J_STAR),
        "J_star_determinant": gf3_determinant(J_STAR),
        "trace_zero_dimension": 20,
        "trace_zero_restricted_rank": gf3_rank(restricted_form),
        "trace_zero_radical": "span{I_6}",
        "hostile_restricted_span": {
            "feature": "span{I_6}",
            "operator_span_rank": identity_feature_rank,
            "restricted_Gram_rank": identity_gram_rank,
            "lesson": (
                "ambient trace-form nondegeneracy does not imply that a "
                "restricted feature span is nondegenerate"
            ),
        },
    }


def veronese_short_relation_audit() -> dict[str, Any]:
    """Exhaust the universal span-at-most-three case for short relations."""

    representatives = []
    for vector in itertools.product(range(FIELD), repeat=3):
        if vector == (0, 0, 0):
            continue
        first_nonzero = next(value for value in vector if value)
        normalized = tuple(
            mod(pow(first_nonzero, -1, FIELD) * value) for value in vector
        )
        if normalized not in representatives:
            representatives.append(normalized)

    def veronese(vector: tuple[int, int, int]) -> list[int]:
        return [
            mod(vector[left] * vector[right])
            for left in range(3)
            for right in range(left, 3)
        ]

    images = [veronese(vector) for vector in representatives]
    minimum_rank_by_size = {}
    for size in (1, 2, 3):
        minimum_rank_by_size[str(size)] = min(
            gf3_rank([images[index] for index in indices])
            for indices in itertools.combinations(range(len(images)), size)
        )
    if minimum_rank_by_size != {"1": 1, "2": 2, "3": 3}:
        raise AssertionError("short Veronese independence changed")
    return {
        "projective_points_checked_in_PG_2_3": len(representatives),
        "minimum_rank_by_distinct_point_count": minimum_rank_by_size,
        "consequence": (
            "a nonzero relation among projectively distinct rank-one "
            "symmetric tensors has support at least four"
        ),
        "scope_note": (
            "any one-, two-, or three-column relation lives in a vector "
            "subspace of dimension at most three, so this exhaustive F_3 "
            "audit covers the ambient 11-space short-relation case"
        ),
    }


def nonconstant_pullback_audit() -> dict[str, Any]:
    """Audit im(B^T) intersect <1_231>=0 from endpoint incidence identities."""

    cases = {}
    for scalar in (1, 2):
        # If B^T c=scalar*1_231, summing all block equations gives
        # sum(c)=scalar*231=0 because B*1_231=7*1_99=1_99.
        sum_c = mod(scalar * 231)
        # Gc=B(B^Tc)=scalar*B1=scalar*1.  Thus G(Gc)=0 since
        # G1=(14+1)1=0.  But G^2=(G-J) gives scalar-sum(c).
        iterated_by_G1 = mod(scalar * (14 + 1))
        iterated_by_G_minus_J = mod(scalar - sum_c)
        if iterated_by_G1 == iterated_by_G_minus_J:
            raise AssertionError("constant pullback contradiction disappeared")
        cases[str(scalar)] = {
            "forced_sum_c": sum_c,
            "G_times_Gc": iterated_by_G1,
            "G_minus_J_times_c": iterated_by_G_minus_J,
            "contradiction": True,
        }
    return {
        "identities": [
            "B 1_231=7 1_99=1_99",
            "G=B B^T=A+I",
            "G^2=G-J",
            "G 1_99=0",
        ],
        "nonzero_constant_cases": cases,
        "conclusion": "im(B^T) intersect span{1_231}={0}",
    }


AMBIENT_DIMENSION = 11
AMBIENT_FORM = diagonal([1] * 10 + [2])
BASE_SUPPORTS = [
    (1, 2, 4, 5, 6, 8),
    (1, 2, 3, 5, 6, 8),
    (1, 2, 5, 7, 8, 9),
    (0, 1, 3, 5, 6, 7),
    (0, 1, 4, 5, 7, 9),
    (0, 1, 3, 4, 5, 9),
]
LOCAL_SIMPLEX = transpose(
    [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 2],
        [0, 0, 1, 2, 2, 0],
        [0, 1, 2, 0, 1, 0],
        [0, 2, 2, 0, 1, 0],
        [1, 0, 2, 1, 0, 0],
        [2, 0, 2, 1, 0, 0],
    ]
)


def coordinate_basis(support: tuple[int, ...]) -> Matrix:
    return [
        [int(row == coordinate) for coordinate in support]
        for row in range(AMBIENT_DIMENSION)
    ]


def orthogonal_reflection(vector: list[int]) -> Matrix:
    covector = [
        mod(sum(vector[index] * AMBIENT_FORM[index][column]
                for index in range(AMBIENT_DIMENSION)))
        for column in range(AMBIENT_DIMENSION)
    ]
    norm = mod(sum(covector[index] * vector[index]
                   for index in range(AMBIENT_DIMENSION)))
    if not norm:
        raise ValueError("reflection vector must be nonisotropic")
    coefficient = pow(norm, -1, FIELD)  # -2/norm = 1/norm in F_3.
    reflection = identity(AMBIENT_DIMENSION)
    return [
        [
            mod(reflection[row][column]
                + coefficient * vector[row] * covector[column])
            for column in range(AMBIENT_DIMENSION)
        ]
        for row in range(AMBIENT_DIMENSION)
    ]


def projector_from_basis(basis: Matrix) -> Matrix:
    return matrix_multiply(
        matrix_multiply(basis, transpose(basis)),
        AMBIENT_FORM,
    )


def local_star_columns(basis: Matrix) -> Matrix:
    return matrix_multiply(basis, LOCAL_SIMPLEX)


def ambient_gram(columns: Matrix) -> Matrix:
    return matrix_multiply(
        matrix_multiply(transpose(columns), AMBIENT_FORM),
        columns,
    )


def pair_trace(left: Matrix, right: Matrix) -> int:
    return matrix_trace(matrix_multiply(left, right))


def fourth_trace(left: Matrix, right: Matrix) -> int:
    product = matrix_multiply(left, right)
    return matrix_trace(matrix_multiply(product, product))


def build_projector_control() -> tuple[list[Matrix], list[Matrix]]:
    first_bases = [coordinate_basis(support) for support in BASE_SUPPORTS]
    reflection_zero = orthogonal_reflection(
        [int(index < 4) for index in range(AMBIENT_DIMENSION)]
    )
    base_bases = first_bases + [
        matrix_multiply(reflection_zero, basis) for basis in first_bases
    ]
    rng = random.Random(206)
    transformations = [identity(AMBIENT_DIMENSION)]
    for group in range(1, 8):
        transformation = identity(AMBIENT_DIMENSION)
        for _ in range(4 + group):
            while True:
                vector = [rng.randrange(FIELD) for _ in range(AMBIENT_DIMENSION)]
                norm = mod(sum(
                    vector[index] * AMBIENT_FORM[index][index] * vector[index]
                    for index in range(AMBIENT_DIMENSION)
                ))
                if norm:
                    break
            transformation = matrix_multiply(
                orthogonal_reflection(vector), transformation
            )
        if matrix_multiply(
            matrix_multiply(transpose(transformation), AMBIENT_FORM),
            transformation,
        ) != AMBIENT_FORM:
            raise AssertionError("deterministic transformation is not orthogonal")
        transformations.append(transformation)

    bases = [
        matrix_multiply(transformation, basis)
        for transformation in transformations
        for basis in base_bases
    ]
    bases += [bases[0]] * 3
    projectors = [projector_from_basis(basis) for basis in bases]
    return bases, projectors


def fixed_middle_rows(
    middle_basis: Matrix, projectors: list[Matrix]
) -> Matrix:
    columns = local_star_columns(middle_basis)
    rows = []
    for projector in projectors:
        bilinear = matrix_multiply(
            matrix_multiply(
                transpose(columns),
                AMBIENT_FORM,
            ),
            matrix_multiply(projector, columns),
        )
        # M_x=-Z^*P_xZ.  These are exactly the distinct-pair entries in
        # Q o M_x for the block pairs owned by the middle point.
        rows.append([
            mod(-bilinear[left][right]) for left, right in STAR_EDGES
        ])
    return rows


def projector_control_summary() -> dict[str, Any]:
    bases, projectors = build_projector_control()
    if len(projectors) != 99:
        raise AssertionError("control label count changed")
    if len({tuple(flatten(projector)) for projector in projectors}) != 96:
        raise AssertionError("control distinctness changed")

    zero_operator = zero(AMBIENT_DIMENSION, AMBIENT_DIMENSION)
    total = zero_operator
    expected_star_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    for basis, projector in zip(bases, projectors):
        if matrix_multiply(
            matrix_multiply(transpose(basis), AMBIENT_FORM), basis
        ) != identity(6):
            raise AssertionError("control basis is not orthonormal")
        if matrix_multiply(projector, projector) != projector:
            raise AssertionError("control projector is not idempotent")
        if matrix_multiply(transpose(projector), AMBIENT_FORM) != (
            matrix_multiply(AMBIENT_FORM, projector)
        ):
            raise AssertionError("control projector is not self-adjoint")
        if gf3_rank(projector) != 6 or matrix_trace(projector) != 0:
            raise AssertionError("control projector rank/trace changed")
        columns = local_star_columns(basis)
        if ambient_gram(columns) != expected_star_gram:
            raise AssertionError("control local simplex Gram changed")
        if [mod(sum(row)) for row in columns] != [0] * AMBIENT_DIMENSION:
            raise AssertionError("control local simplex sum changed")
        frame = zero(AMBIENT_DIMENSION, AMBIENT_DIMENSION)
        for vector in transpose(columns):
            column = [[entry] for entry in vector]
            rank_one = matrix_multiply(
                matrix_multiply(column, [vector]), AMBIENT_FORM
            )
            frame = matrix_add(frame, rank_one)
        if projector != scalar_matrix(2, frame):
            raise AssertionError("control projector frame identity changed")
        total = matrix_add(total, projector)
    if total != zero_operator:
        raise AssertionError("control projector sum changed")

    pair_matrix = [
        [pair_trace(left, right) for right in projectors]
        for left in projectors
    ]
    fourth_matrix = [
        [fourth_trace(left, right) for right in projectors]
        for left in projectors
    ]
    fourth_row_sums = [mod(sum(row)) for row in fourth_matrix]
    if [mod(sum(row)) for row in pair_matrix] != [0] * 99:
        raise AssertionError("pair trace contraction changed")

    feature_ranks = []
    slice_gram_ranks = []
    gamma = zero(99, 99)
    for middle_basis in bases:
        rows = fixed_middle_rows(middle_basis, projectors)
        rref, _ = gf3_rref(rows)
        row_basis = [row for row in rref if any(row)]
        feature_ranks.append(len(row_basis))
        restricted = matrix_multiply(
            matrix_multiply(row_basis, J_STAR),
            transpose(row_basis),
        )
        slice_gram_ranks.append(gf3_rank(restricted))
        tau = matrix_multiply(
            matrix_multiply(rows, J_STAR),
            transpose(rows),
        )
        if [mod(sum(row)) for row in tau] != [0] * 99:
            raise AssertionError("fixed-middle tau row sum changed")
        gamma = matrix_add(gamma, tau)

    if [gamma[index][index] for index in range(99)] != fourth_row_sums:
        raise AssertionError("diag(Gamma)=H*1 changed")
    if [mod(sum(row)) for row in gamma] != [0] * 99:
        raise AssertionError("Gamma row contraction changed")

    return {
        "ambient_form_diagonal": [1] * 10 + [2],
        "ambient_form_discriminant": 2,
        "projector_labels": 99,
        "distinct_projectors": 96,
        "each_projector": {
            "rank": 6,
            "trace": 0,
            "idempotent": True,
            "self_adjoint": True,
            "seven_singular_simplex_columns": True,
            "simplex_gram": "J_7-I_7",
            "simplex_sum_zero": True,
            "projector_identity": "P=-sum_i(z_i tensor z_i)",
        },
        "sum_projectors_zero": True,
        "projector_span_rank": gf3_rank([flatten(item) for item in projectors]),
        "pair_trace_matrix_rank": gf3_rank(pair_matrix),
        "fourth_trace_matrix_rank": gf3_rank(fourth_matrix),
        "fourth_trace_row_sum_distribution": distribution(fourth_row_sums),
        "fixed_middle_feature_rank_distribution": distribution(feature_ranks),
        "fixed_middle_tau_rank_distribution": distribution(slice_gram_ranks),
        "Gamma_rank": gf3_rank(gamma),
        "Gamma_row_sum_distribution": distribution(
            [mod(sum(row)) for row in gamma]
        ),
        "Gamma_diagonal_equals_H_row_sum": True,
        "conclusion": (
            "all 99 fixed-middle tau slices can have rank 21 while the "
            "global fourth-trace matrix H has rank 96"
        ),
        "satisfied_endpoint_shaped_premises": [
            "nondegenerate nonsquare 11-space over F_3",
            "99 rank-six trace-zero self-adjoint idempotents",
            "96 distinct projector labels",
            "every projector has a seven-singular-column J_7-I_7 simplex",
            "sum of all 99 projectors is zero",
        ],
        "failed_target_premises": [
            "three projector labels repeat one projector",
            "the local simplexes are not glued into 231 shared projectively distinct columns",
            "there is no 99-by-231 point-triangle incidence with column degree three",
            "there is no srg(99,14,1,2) graph or prism-free crossing geometry",
            "the rank-11 endpoint code, dual-distance, and circuit-cover conditions are absent",
        ],
    }


def crossing_toy_summary() -> dict[str, Any]:
    """Replay crossing and Gamma identities on a small exact zero frame.

    The 12 local stars are disjoint rather than glued three-at-a-column.
    This checks the algebra but not the target incidence premise.
    """

    bases, all_projectors = build_projector_control()
    # Two complete 12-projector zero-sum orbits are needed here: the first
    # orbit lies in a 10-dimensional coordinate subspace, while the second
    # deterministic orthogonal image raises the synthesis rank to 11.
    bases = bases[:24]
    projectors = all_projectors[:24]
    local_columns = [local_star_columns(basis) for basis in bases]
    columns = [
        [entry for local in local_columns for entry in local[row]]
        for row in range(AMBIENT_DIMENSION)
    ]
    if gf3_rank(columns) != AMBIENT_DIMENSION:
        raise AssertionError("toy synthesis matrix lost full row rank")
    gram = ambient_gram(columns)
    column_count = 7 * len(bases)
    if matrix_multiply(gram, gram) != zero(column_count, column_count):
        raise AssertionError("toy centered Gram is not square-zero")

    selectors = []
    for point in range(len(bases)):
        selector = [0] * column_count
        for column in range(7 * point, 7 * point + 7):
            selector[column] = 1
        selectors.append(selector)
    incidence = selectors
    q_matrix = matrix_multiply(transpose(incidence), incidence)

    moments = []
    for selector, projector in zip(selectors, projectors):
        selected = [
            [
                gram[row][column] * selector[column]
                for column in range(column_count)
            ]
            for row in range(column_count)
        ]
        moment = matrix_multiply(selected, gram)
        expected = scalar_matrix(
            2,
            matrix_multiply(
                matrix_multiply(transpose(columns), AMBIENT_FORM),
                matrix_multiply(projector, columns),
            ),
        )
        if moment != expected:
            raise AssertionError("M_x=-Z^*P_xZ changed")
        if gf3_rank(moment) != 6:
            raise AssertionError("rank M_x changed")
        moments.append(moment)

    moment_sum = zero(column_count, column_count)
    for moment in moments:
        moment_sum = matrix_add(moment_sum, moment)
    if moment_sum != zero(column_count, column_count):
        raise AssertionError("sum M_x changed")

    center_count = len(bases)
    crossing_rows = [
        [moments[point][left][right] for point in range(center_count)]
        for left in range(column_count)
        for right in range(column_count)
    ]
    crossing_rank = gf3_rank(crossing_rows)
    projector_span_rank = gf3_rank([flatten(item) for item in projectors])
    if crossing_rank != projector_span_rank:
        raise AssertionError("injective crossing-feature rank changed")
    if matrix_multiply(
        transpose(crossing_rows), crossing_rows
    ) != zero(center_count, center_count):
        raise AssertionError("W^T W=0 changed")

    gamma = zero(center_count, center_count)
    for left in range(center_count):
        localizer = [
            [
                mod(q_matrix[row][column] * moments[left][row][column])
                for column in range(column_count)
            ]
            for row in range(column_count)
        ]
        for right in range(center_count):
            gamma[left][right] = mod(sum(
                localizer[row][column] * moments[right][row][column]
                for row in range(column_count)
                for column in range(column_count)
            ))

    tau_sum = zero(center_count, center_count)
    for middle in range(center_count):
        rows = fixed_middle_rows(bases[middle], projectors)
        tau = matrix_multiply(
            matrix_multiply(rows, J_STAR), transpose(rows)
        )
        if middle < 3:
            middle_projector = projectors[middle]
            compressions = [
                matrix_multiply(
                    matrix_multiply(middle_projector, projector),
                    middle_projector,
                )
                for projector in projectors
            ]
            direct_tau = [
                [trace_pair(left, right) for right in compressions]
                for left in compressions
            ]
            if tau != direct_tau:
                raise AssertionError("tau coordinate sign or orientation changed")
        tau_sum = matrix_add(tau_sum, tau)
    if gamma != tau_sum:
        raise AssertionError("Gamma=sum_y Tau^(y) changed")

    return {
        "centers": center_count,
        "columns": column_count,
        "synthesis_rank": 11,
        "D_square_zero": True,
        "M_identity": "M_x=D S_x D=-Z^*P_xZ",
        "each_M_rank": 6,
        "D_M_and_M_D_zero": True,
        "all_M_products_zero": True,
        "sum_M_zero": True,
        "W_definition": "W[(T,U),x]=M_x[T,U]=w_TU[x]",
        "W_rank": crossing_rank,
        "projector_span_rank": projector_span_rank,
        "W_transpose_W_zero": True,
        "W_W_transpose_square_zero": True,
        "Gamma_identity": (
            "Gamma_xy=tr((Q o M_x)M_y)="
            "sum_z tr(P_x P_z P_y P_z)"
        ),
        "Gamma_equals_sum_fixed_middle_tau": True,
        "tau_coordinate_formula_directly_checked_middles": 3,
        "Gamma_rank": gf3_rank(gamma),
        "failed_target_premises": [
            "the 168 columns are twenty-four disjoint local stars",
            "each toy column has incidence degree one, not three",
            "the toy has no SRG or prism-free graph",
            "the toy does not claim projective distinctness",
        ],
    }


def theorem_ledger() -> dict[str, Any]:
    return {
        "target_fixed_middle_slice": {
            "operator": "A_x^(y)=P_y P_x P_y restricted to E_y",
            "tau_Gram": (
                "Tau^(y)[x,z]=tau_(xy;z)=tr(A_x^(y) A_z^(y))"
            ),
            "self_adjoint": True,
            "A_y": "I_(E_y)",
            "sum_x_A_x": "0",
            "trace_A_x": "g_xy",
            "diagonal": "Tau^(y)[x,x]=h_xy",
            "row_y": "Tau^(y)[y,x]=g_xy",
            "row_sum": "Tau^(y) 1=0",
            "rank_bound": 21,
            "rank_warning": (
                "rank(Tau^(y)) can be smaller than the operator-span rank "
                "because the restricted trace form can have a radical"
            ),
        },
        "target_localizer_coordinates": {
            "coordinate": (
                "m_x^(y)[i,j]=M_x[T_i,T_j] for the 21 unordered distinct "
                "pairs of the seven y-star triangles"
            ),
            "sign": (
                "m_x^(y)[i,j]= -<z_i,P_x z_j>; the two minus signs cancel "
                "in tau"
            ),
            "inside_Q_o_M": (
                "Q[T_i,T_j]=1 for i!=j; diagonal Q[T_i,T_i]=3=0; "
                "disjoint triangle pairs have Q=0"
            ),
            "reconstruction": (
                "the missing diagonal is N_ii=-sum_(j!=i)N_ij, so the "
                "21 localizer entries determine P_y P_x P_y completely"
            ),
            "g_formula": "g_xy=sum_e m_x^(y)[e]",
            "tau_formula": (
                "tau_(xy;z)=m_x^(y)^T J_star m_z^(y)"
            ),
            "h_formula": (
                "h_xy=m_x^(y)^T J_star m_x^(y)"
            ),
            "known_from_incidence": (
                "which 21 coordinates belong to y and the Q mask values"
            ),
            "still_unknown": (
                "the coordinate values, their graph-type distributions, "
                "and whether any 21 center rows span the 21-space"
            ),
        },
        "target_crossing_feature": {
            "M_properties": [
                "M_x is symmetric of rank six",
                "D M_x=M_x D=0",
                "M_x M_y=0 for every x,y",
                "sum_x M_x=0",
            ],
            "W": "W[(T,U),x]=M_x[T,U]=w_TU[x]",
            "rank_W": (
                "rank(W)=dim span{P_x}<=65 because Z has full row rank 11 "
                "and P maps injectively to -Z^*PZ"
            ),
            "W_relations": ["W 1=0", "W^T W=0"],
            "square_zero_kernel": "(W W^T)^2=0",
        },
        "target_Gamma": {
            "definition": "Gamma_xy=tr((Q o M_x)M_y)",
            "factorization": "Gamma=W^T diag(vec(Q)) W",
            "sum_slices": "Gamma=sum_y Tau^(y)",
            "diagonal": "diag(Gamma)=H 1",
            "row_sum": "Gamma 1=0",
            "rank_bound": 65,
        },
        "common_true_kernel": {
            "map": "mathcal P(c)=sum_x c_x P_x",
            "dimension_lower_bound": 34,
            "incidence_dependency": "L=ker(B^T) is contained in ker(mathcal P)",
            "inherited_incidence_dimension": "17<=dim(L)<=33",
            "new_quotient_lower_bound": "dim(ker(mathcal P)/L)>=1",
            "named_intersection_code": (
                "A_Delta=im(B^T) intersect ker("
                "a -> D diag(a) D)"
            ),
            "intersection_code_dimension": (
                "dim(A_Delta)=dim(ker(mathcal P)/L)="
                "rank(B)-dim span{P_x}>=1"
            ),
            "triangle_coefficient_consequence": (
                "there exists c notin L with a=B^T c nonzero and "
                "sum_T a_T(z_T tensor z_T)=0"
            ),
            "matrix_consequences": [
                "D diag(a) D=0",
                "(D o D) a=0 from the diagonal entries",
            ],
            "nonconstant": (
                "a is outside span{1_231}; im(B^T) intersects the constant "
                "line trivially by G^2=G-J, G1=0, and B1=1 over F_3"
            ),
            "three_class_balance": (
                "if R_j=sum_(T:a_T=j) z_T tensor z_T, then "
                "R_0=R_1=R_2"
            ),
            "support_bound": (
                "wt(a)>=4 by projective distinctness of the Veronese "
                "columns z_T tensor z_T"
            ),
            "support_caveat": (
                "the original centered-code dual-distance theorem does not "
                "directly apply to this quadratic-tensor relation; no "
                "stronger weight or complete-composition bound is proved"
            ),
            "slice_consequence": (
                "ker(mathcal P) is a true operator-relation subspace "
                "contained in every ker(Tau^(y)) and in ker(Gamma)"
            ),
        },
        "trace_class_consequence": {
            "scope": (
                "for any fixed y and any collection of k centers having "
                "the same g_xy residue"
            ),
            "centered_feature_space": "I_6^perp",
            "centered_feature_dimension": 20,
            "centered_trace_form_rank": 19,
            "centered_Gram_rank_bound": 19,
            "nonneighbor_pigeonhole": (
                "among the 84 nonneighbors of y one residue class has "
                "k>=28, so its (k-1)-by-(k-1) difference Gram has nullity>=8"
            ),
            "warning": (
                "these are Gram nullities, not true operator relations, "
                "unless the radical is separately controlled"
            ),
        },
        "next_global_invariant": {
            "simultaneous_compression_map": (
                "A -> (P_y A P_y restricted to E_y)_(y=1..99)"
            ),
            "open_kernel_question": (
                "does its restriction to span{P_x} have kernel exactly zero, "
                "or exactly the known projector-relation kernel after pulling "
                "back to center coefficients?"
            ),
            "mixed_four_center_tensor": (
                "tr((P_y P_x P_y)(P_v P_z P_v)) for y!=v"
            ),
            "reason": (
                "fixed-middle tau slices give within-star Gram data but do "
                "not compare compression coordinates across two middle centers"
            ),
        },
    }


def analyze() -> dict[str, Any]:
    return {
        "claim_label": "DERIVED_PENDING_INDEPENDENT_VERIFICATION",
        "field": 3,
        "scope": (
            "conditional prism-free n3=4158 centered rank-11 endpoint; "
            "crossing kernel, Hadamard localizers, and fixed-middle "
            "three-center compression coordinates"
        ),
        "inputs": verify_inputs(),
        "star_coordinate_theorem": star_coordinate_summary(),
        "veronese_short_relation_audit": veronese_short_relation_audit(),
        "nonconstant_pullback_audit": nonconstant_pullback_audit(),
        "theorem_ledger": theorem_ledger(),
        "crossing_toy": crossing_toy_summary(),
        "strong_hostile_control": projector_control_summary(),
        "conclusions": {
            "new_exact_coordinate_bridge": True,
            "new_nonincidence_projector_relation_forced": True,
            "pair_local_data_sufficient": False,
            "fixed_middle_rank_bound_excludes_endpoint": False,
            "rank11_endpoint_excluded": False,
            "n3_improved": False,
            "Q_7060_proved": False,
            "conway_99_resolved": False,
            "status": "UNKNOWN",
        },
    }


def verify(data: dict[str, Any]) -> None:
    star = data["star_coordinate_theorem"]
    if (
        star["coordinate_map_rank"] != 21
        or star["J_star_rank"] != 21
        or star["J_star_determinant"] != 2
        or star["trace_zero_dimension"] != 20
        or star["trace_zero_restricted_rank"] != 19
    ):
        raise AssertionError("star-coordinate theorem mutated")
    hostile_span = star["hostile_restricted_span"]
    if (
        hostile_span["operator_span_rank"] != 1
        or hostile_span["restricted_Gram_rank"] != 0
    ):
        raise AssertionError("restricted-span hostile control mutated")

    theorem = data["theorem_ledger"]
    if theorem["target_fixed_middle_slice"]["rank_bound"] != 21:
        raise AssertionError("fixed-middle rank bound mutated")
    if theorem["target_Gamma"]["rank_bound"] != 65:
        raise AssertionError("Gamma rank bound mutated")
    if theorem["common_true_kernel"]["dimension_lower_bound"] != 34:
        raise AssertionError("common-kernel bound mutated")
    if (
        theorem["common_true_kernel"]["support_bound"]
        != "wt(a)>=4 by projective distinctness of the Veronese "
           "columns z_T tensor z_T"
    ):
        raise AssertionError("intersection-code support bound mutated")
    if data["veronese_short_relation_audit"][
        "minimum_rank_by_distinct_point_count"
    ] != {"1": 1, "2": 2, "3": 3}:
        raise AssertionError("short Veronese audit mutated")
    if data["nonconstant_pullback_audit"]["conclusion"] != (
        "im(B^T) intersect span{1_231}={0}"
    ):
        raise AssertionError("constant pullback audit mutated")

    toy = data["crossing_toy"]
    if (
        toy["synthesis_rank"] != 11
        or not toy["D_square_zero"]
        or not toy["Gamma_equals_sum_fixed_middle_tau"]
        or toy["W_rank"] != toy["projector_span_rank"]
    ):
        raise AssertionError("crossing toy mutated")

    control = data["strong_hostile_control"]
    if (
        control["projector_labels"] != 99
        or control["distinct_projectors"] != 96
        or not control["sum_projectors_zero"]
        or control["fourth_trace_matrix_rank"] != 96
        or control["fixed_middle_tau_rank_distribution"] != {"21": 99}
    ):
        raise AssertionError("strong hostile control mutated")
    if not any(
        "231 shared projectively distinct" in item
        for item in control["failed_target_premises"]
    ):
        raise AssertionError("strong control limitations were weakened")

    conclusions = data["conclusions"]
    forbidden = [
        "pair_local_data_sufficient",
        "fixed_middle_rank_bound_excludes_endpoint",
        "rank11_endpoint_excluded",
        "n3_improved",
        "Q_7060_proved",
        "conway_99_resolved",
    ]
    if any(conclusions[key] for key in forbidden):
        raise AssertionError("status inflation detected")
    if conclusions["status"] != "UNKNOWN":
        raise AssertionError("target status mutated")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--verify", type=Path)
    arguments = parser.parse_args()
    data = analyze()
    verify(data)
    if arguments.verify:
        expected = json.loads(arguments.verify.read_text(encoding="utf-8"))
        if data != expected:
            raise AssertionError("recomputed analysis differs from sealed JSON")
    if arguments.write:
        arguments.write.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
