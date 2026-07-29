"""Source-blind exact checks for the Wave 206 fixed-middle tensor.

This module is intentionally self-contained and imports no discovery code.
All matrix arithmetic is over F_3 and uses Python integers reduced modulo 3.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence

P = 3


def mod(value: int) -> int:
    return value % P


def zeros(rows: int, cols: int) -> list[list[int]]:
    return [[0 for _ in range(cols)] for _ in range(rows)]


def eye(size: int) -> list[list[int]]:
    out = zeros(size, size)
    for i in range(size):
        out[i][i] = 1
    return out


def diagonal(entries: Sequence[int]) -> list[list[int]]:
    out = zeros(len(entries), len(entries))
    for i, value in enumerate(entries):
        out[i][i] = mod(value)
    return out


def transpose(a: Sequence[Sequence[int]]) -> list[list[int]]:
    if not a:
        return []
    return [list(row) for row in zip(*a)]


def add(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> list[list[int]]:
    return [
        [mod(a[i][j] + b[i][j]) for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c: int, a: Sequence[Sequence[int]]) -> list[list[int]]:
    return [[mod(c * value) for value in row] for row in a]


def matmul(
    a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]
) -> list[list[int]]:
    if not a or not b:
        return []
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    assert len(a[0]) == inner
    bt = transpose(b)
    return [
        [mod(sum(a[i][k] * bt[j][k] for k in range(inner))) for j in range(cols)]
        for i in range(rows)
    ]


def matvec(a: Sequence[Sequence[int]], v: Sequence[int]) -> list[int]:
    return [mod(sum(row[j] * v[j] for j in range(len(v)))) for row in a]


def trace(a: Sequence[Sequence[int]]) -> int:
    return mod(sum(a[i][i] for i in range(len(a))))


def trace_product(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> int:
    assert len(a) == len(b[0]) and len(a[0]) == len(b)
    return mod(
        sum(a[i][j] * b[j][i] for i in range(len(a)) for j in range(len(a[0])))
    )


def flatten(a: Sequence[Sequence[int]]) -> tuple[int, ...]:
    return tuple(mod(value) for row in a for value in row)


def is_zero(a: Sequence[Sequence[int]]) -> bool:
    return all(mod(value) == 0 for row in a for value in row)


def matrix_rank(a: Sequence[Sequence[int]]) -> int:
    if not a:
        return 0
    work = [[mod(value) for value in row] for row in a]
    rows = len(work)
    cols = len(work[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, P)
        work[rank] = [mod(inv * value) for value in work[rank]]
        for r in range(rows):
            if r == rank or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                mod(work[r][j] - factor * work[rank][j]) for j in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def inverse(a: Sequence[Sequence[int]]) -> list[list[int]]:
    size = len(a)
    assert all(len(row) == size for row in a)
    work = [
        [mod(value) for value in a[i]] + eye(size)[i]
        for i in range(size)
    ]
    for col in range(size):
        pivot = next((r for r in range(col, size) if work[r][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        work[col], work[pivot] = work[pivot], work[col]
        inv = pow(work[col][col], -1, P)
        work[col] = [mod(inv * value) for value in work[col]]
        for r in range(size):
            if r == col or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                mod(work[r][j] - factor * work[col][j])
                for j in range(2 * size)
            ]
    return [row[size:] for row in work]


def adjoint(a: Sequence[Sequence[int]], form: Sequence[Sequence[int]]) -> list[list[int]]:
    """Adjoint of a square operator for the supplied symmetric Gram matrix."""

    return matmul(matmul(inverse(form), transpose(a)), form)


def rectangular_adjoint(
    a: Sequence[Sequence[int]], codomain_form: Sequence[Sequence[int]]
) -> list[list[int]]:
    """Adjoint to a map from a standard coordinate space into the codomain."""

    return matmul(transpose(a), codomain_form)


def matrix_sum(matrices: Iterable[Sequence[Sequence[int]]]) -> list[list[int]]:
    matrices = list(matrices)
    assert matrices
    out = zeros(len(matrices[0]), len(matrices[0][0]))
    for matrix in matrices:
        out = add(out, matrix)
    return out


def gram_from_vectors(
    vectors: Sequence[Sequence[int]], metric: Sequence[Sequence[int]]
) -> list[list[int]]:
    return [
        [
            mod(
                sum(
                    vectors[i][a] * metric[a][b] * vectors[j][b]
                    for a in range(len(metric))
                    for b in range(len(metric))
                )
            )
            for j in range(len(vectors))
        ]
        for i in range(len(vectors))
    ]


def star_frame() -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    """Return (ambient form, Z, G=Z*Z, P_y=-ZZ*) in dimension 11.

    The first seven ambient coordinates have form -I.  Column i of Z is
    1-e_i in those coordinates and zero in the remaining four coordinates.
    """

    form = diagonal([2] * 7 + [1] * 4)
    z = zeros(11, 7)
    for row in range(7):
        for col in range(7):
            z[row][col] = mod(1 - (1 if row == col else 0))
    z_star = rectangular_adjoint(z, form)
    gram = matmul(z_star, z)
    projector = scale(-1, matmul(z, z_star))
    return form, z, gram, projector


def expected_star_gram() -> list[list[int]]:
    return [
        [0 if i == j else 1 for j in range(7)]
        for i in range(7)
    ]


def coordinate_projector(indices: Sequence[int], size: int = 11) -> list[list[int]]:
    out = zeros(size, size)
    for index in indices:
        out[index][index] = 1
    return out


def deterministic_projectors() -> tuple[
    list[list[int]], list[list[int]], list[list[list[int]]]
]:
    """Build a 99-projector algebraic control with exact zero sum.

    There are 33 rank-six self-adjoint projector types. Each is repeated
    three times, making the total zero over F_3. This is deliberately not a
    graph or projective-column construction.
    """

    form, z, _gram, middle = star_frame()
    types = [middle]
    for indices in itertools.islice(itertools.combinations(range(11), 6), 32):
        types.append(coordinate_projector(indices))
    projectors = [projector for projector in types for _ in range(3)]
    assert len(projectors) == 99
    return form, z, projectors


def check_projector(
    projector: Sequence[Sequence[int]],
    form: Sequence[Sequence[int]],
    expected_rank: int = 6,
) -> bool:
    return (
        matmul(projector, projector) == projector
        and adjoint(projector, form) == projector
        and matrix_rank(projector) == expected_rank
    )


def fixed_middle_tensor(
    projectors: Sequence[Sequence[Sequence[int]]], middle: int
) -> list[list[int]]:
    """Compute tr(P_x P_y P_z P_y) using precomputed P_x P_y."""

    py = projectors[middle]
    right_products = [matmul(px, py) for px in projectors]
    return [
        [trace_product(right_products[x], right_products[z]) for z in range(len(projectors))]
        for x in range(len(projectors))
    ]


def six_space_compressions(
    projectors: Sequence[Sequence[Sequence[int]]], middle: int
) -> list[list[list[int]]]:
    py = projectors[middle]
    return [matmul(matmul(py, px), py) for px in projectors]


def seven_star_matrices(
    projectors: Sequence[Sequence[Sequence[int]]],
    z: Sequence[Sequence[int]],
    form: Sequence[Sequence[int]],
) -> list[list[list[int]]]:
    z_star = rectangular_adjoint(z, form)
    return [matmul(matmul(z_star, px), z) for px in projectors]


COORDINATE_PAIRS = tuple((i, j) for i in range(6) for j in range(i, 6))


def lift_21(coordinates: Sequence[int]) -> list[list[int]]:
    """Lift 21 upper-triangle entries to a symmetric 7x7 K with K*1=0."""

    assert len(coordinates) == 21
    k = zeros(7, 7)
    for value, (i, j) in zip(coordinates, COORDINATE_PAIRS):
        k[i][j] = mod(value)
        k[j][i] = mod(value)
    for i in range(6):
        k[i][6] = mod(-sum(k[i][j] for j in range(6)))
        k[6][i] = k[i][6]
    k[6][6] = mod(-sum(k[6][j] for j in range(6)))
    assert matvec(k, [1] * 7) == [0] * 7
    return k


def coordinates_21(k: Sequence[Sequence[int]]) -> list[int]:
    assert len(k) == 7 and all(len(row) == 7 for row in k)
    assert k == transpose(k)
    assert matvec(k, [1] * 7) == [0] * 7
    coordinates = [mod(k[i][j]) for i, j in COORDINATE_PAIRS]
    assert lift_21(coordinates) == k
    return coordinates


def coordinate_metric_21() -> list[list[int]]:
    basis = [
        lift_21([1 if i == j else 0 for i in range(21)])
        for j in range(21)
    ]
    return [
        [trace_product(basis[i], basis[j]) for j in range(21)]
        for i in range(21)
    ]


def trace_zero_basis_21() -> list[list[int]]:
    """Return 20 coordinate vectors spanning tr(lift_21(q))=0."""

    functional = [
        trace(lift_21([1 if i == j else 0 for i in range(21)]))
        for j in range(21)
    ]
    pivot = next(i for i, value in enumerate(functional) if value)
    pivot_inv = pow(functional[pivot], -1, P)
    basis: list[list[int]] = []
    for free in range(21):
        if free == pivot:
            continue
        vector = [0] * 21
        vector[free] = 1
        vector[pivot] = mod(-functional[free] * pivot_inv)
        assert mod(sum(functional[i] * vector[i] for i in range(21))) == 0
        basis.append(vector)
    return basis


def restrict_metric(
    metric: Sequence[Sequence[int]], basis: Sequence[Sequence[int]]
) -> list[list[int]]:
    return gram_from_vectors(basis, metric)


def columns_matrix(vectors: Sequence[Sequence[int]]) -> list[list[int]]:
    if not vectors:
        return []
    return [[mod(vectors[col][row]) for col in range(len(vectors))] for row in range(len(vectors[0]))]


def analyze() -> dict[str, object]:
    form, z, projectors = deterministic_projectors()
    z_star = rectangular_adjoint(z, form)
    gram = matmul(z_star, z)
    py = projectors[0]
    n = len(projectors)

    tensor = fixed_middle_tensor(projectors, 0)
    compressions = six_space_compressions(projectors, 0)
    star_matrices = seven_star_matrices(projectors, z, form)

    direct_compression_gram = [
        [trace_product(compressions[x], compressions[w]) for w in range(n)]
        for x in range(n)
    ]
    star_coordinate_gram = [
        [trace_product(star_matrices[x], star_matrices[w]) for w in range(n)]
        for x in range(n)
    ]

    right_products = [matmul(px, py) for px in projectors]
    g_values = [trace(product) for product in right_products]
    h_values = [trace_product(product, product) for product in right_products]

    metric = coordinate_metric_21()
    coordinate_vectors = [coordinates_21(k) for k in star_matrices]
    metric_gram = gram_from_vectors(coordinate_vectors, metric)

    identity_k = gram
    identity_coordinates = coordinates_21(identity_k)
    identity_pairings = [
        mod(
            sum(
                identity_coordinates[a] * metric[a][b] * vector[b]
                for a in range(21)
                for b in range(21)
            )
        )
        for vector in (
            [1 if i == j else 0 for i in range(21)]
            for j in range(21)
        )
    ]
    nonzero_identity_witness = next(
        (index for index, value in enumerate(identity_pairings) if value),
        None,
    )

    trace_zero_basis = trace_zero_basis_21()
    trace_zero_metric = restrict_metric(metric, trace_zero_basis)
    identity_pairs_trace_zero = [
        mod(
            sum(
                identity_coordinates[a] * metric[a][b] * vector[b]
                for a in range(21)
                for b in range(21)
            )
        )
        for vector in trace_zero_basis
    ]

    feature_span_rank = matrix_rank(columns_matrix(coordinate_vectors))
    tensor_rank = matrix_rank(tensor)

    reconstructed = [
        matmul(matmul(z, k), z_star)
        for k in star_matrices
    ]

    result: dict[str, object] = {
        "field": "F_3",
        "ambient_dimension": 11,
        "ambient_form_determinant_square_class": 2,
        "center_count": n,
        "projector_types": 33,
        "projector_multiplicity": 3,
        "all_projectors_self_adjoint_idempotent_rank_6": all(
            check_projector(projector, form) for projector in projectors
        ),
        "zero_frame_sum": is_zero(matrix_sum(projectors)),
        "star_columns": 7,
        "star_columns_singular": all(gram[i][i] == 0 for i in range(7)),
        "star_gram_is_E_minus_I": gram == expected_star_gram(),
        "star_gram_rank": matrix_rank(gram),
        "star_relation_Z_one_zero": matvec(z, [1] * 7) == [0] * 11,
        "middle_projector_equals_minus_ZZstar": py == scale(-1, matmul(z, z_star)),
        "middle_projector_rank": matrix_rank(py),
        "tensor_outer_symmetric": tensor == transpose(tensor),
        "tensor_contraction_all_rows_zero": all(mod(sum(row)) == 0 for row in tensor),
        "tensor_diagonal_equals_h": all(tensor[x][x] == h_values[x] for x in range(n)),
        "tensor_middle_column_equals_g": all(tensor[x][0] == g_values[x] for x in range(n)),
        "tensor_equals_six_space_compression_gram": tensor == direct_compression_gram,
        "seven_star_matrices_symmetric": all(k == transpose(k) for k in star_matrices),
        "seven_star_matrices_annihilate_one": all(
            matvec(k, [1] * 7) == [0] * 7 for k in star_matrices
        ),
        "compression_reconstruction_A_equals_ZKZstar": reconstructed == compressions,
        "tensor_equals_seven_star_trace_gram": tensor == star_coordinate_gram,
        "coordinate_dimension": len(COORDINATE_PAIRS),
        "coordinate_roundtrip": all(
            lift_21(coordinates_21(k)) == k for k in star_matrices
        ),
        "coordinate_metric_rank": matrix_rank(metric),
        "tensor_equals_21_coordinate_metric_gram": tensor == metric_gram,
        "identity_coordinate_is_nonzero": any(identity_coordinates),
        "identity_coordinate_is_isotropic": trace_product(identity_k, identity_k) == 0,
        "identity_coordinate_is_not_ambient_radical": nonzero_identity_witness is not None,
        "identity_nonorthogonal_basis_witness_index": nonzero_identity_witness,
        "trace_zero_subspace_dimension": len(trace_zero_basis),
        "trace_zero_restricted_metric_rank": matrix_rank(trace_zero_metric),
        "trace_zero_restricted_radical_dimension": (
            len(trace_zero_basis) - matrix_rank(trace_zero_metric)
        ),
        "identity_lies_in_trace_zero_subspace": trace(identity_k) == 0,
        "identity_is_orthogonal_to_trace_zero_subspace": all(
            value == 0 for value in identity_pairs_trace_zero
        ),
        "single_identity_feature_gram_rank": matrix_rank(
            [[trace_product(identity_k, identity_k)]]
        ),
        "single_identity_feature_span_rank": 1,
        "control_feature_span_rank": feature_span_rank,
        "control_tensor_rank": tensor_rank,
        "control_restricted_radical_dimension": feature_span_rank - tensor_rank,
        "all_ones_is_true_feature_relation": all(
            mod(sum(vector[i] for vector in coordinate_vectors)) == 0
            for i in range(21)
        ),
        "scope": {
            "is_srg_incidence_configuration": False,
            "has_99_distinct_projectors": False,
            "supports_endpoint_tau_classification": False,
            "supports_only_formal_algebra_and_coordinate_caveats": True,
        },
        "status": {
            "Conway_99": "UNKNOWN",
            "rank_11_endpoint": "UNKNOWN",
            "n3_4158_endpoint": "UNKNOWN",
            "actual_nonedge_h": "UNKNOWN",
        },
    }
    return result


def assert_expected(result: dict[str, object]) -> None:
    required_true = [
        "all_projectors_self_adjoint_idempotent_rank_6",
        "zero_frame_sum",
        "star_columns_singular",
        "star_gram_is_E_minus_I",
        "star_relation_Z_one_zero",
        "middle_projector_equals_minus_ZZstar",
        "tensor_outer_symmetric",
        "tensor_contraction_all_rows_zero",
        "tensor_diagonal_equals_h",
        "tensor_middle_column_equals_g",
        "tensor_equals_six_space_compression_gram",
        "seven_star_matrices_symmetric",
        "seven_star_matrices_annihilate_one",
        "compression_reconstruction_A_equals_ZKZstar",
        "tensor_equals_seven_star_trace_gram",
        "coordinate_roundtrip",
        "tensor_equals_21_coordinate_metric_gram",
        "identity_coordinate_is_nonzero",
        "identity_coordinate_is_isotropic",
        "identity_coordinate_is_not_ambient_radical",
        "identity_lies_in_trace_zero_subspace",
        "identity_is_orthogonal_to_trace_zero_subspace",
        "all_ones_is_true_feature_relation",
    ]
    for key in required_true:
        assert result[key] is True, key
    assert result["star_gram_rank"] == 6
    assert result["middle_projector_rank"] == 6
    assert result["coordinate_dimension"] == 21
    assert result["coordinate_metric_rank"] == 21
    assert result["trace_zero_subspace_dimension"] == 20
    assert result["trace_zero_restricted_metric_rank"] == 19
    assert result["trace_zero_restricted_radical_dimension"] == 1
    assert result["single_identity_feature_gram_rank"] == 0
    assert result["single_identity_feature_span_rank"] == 1
    assert result["control_tensor_rank"] <= 21
    assert result["control_restricted_radical_dimension"] >= 0


def main() -> None:
    result = analyze()
    assert_expected(result)
    output = Path(__file__).with_name("blind_result.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
