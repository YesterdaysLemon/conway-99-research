"""Exact symbolic checks for the Wave 207 mixed four-center theorem.

The checker uses only linear algebra over F_3.  It does not search for a
graph, a centered 231-column configuration, or an endpoint code.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


FIELD = 3


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix, strict=True)]


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    if not left or not right:
        return []
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            % FIELD
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_from_columns(columns: list[list[int]]) -> list[list[int]]:
    if not columns:
        return []
    return transpose(columns)


def rank_mod(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[entry % FIELD for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, FIELD)
        work[pivot_row] = [
            entry * inverse % FIELD for entry in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][j] - factor * work[pivot_row][j]) % FIELD
                for j in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def determinant_mod(matrix: list[list[int]]) -> int:
    size = len(matrix)
    work = [[entry % FIELD for entry in row] for row in matrix]
    determinant = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % FIELD
        inverse = pow(pivot_value, -1, FIELD)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % FIELD
            for j in range(column, size):
                work[row][j] = (
                    work[row][j] - factor * work[column][j]
                ) % FIELD
    return determinant % FIELD


def inverse_mod(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    work = [
        [entry % FIELD for entry in matrix[row]]
        + [1 if row == column else 0 for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            raise ValueError("matrix is singular")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, FIELD)
        work[column] = [entry * inverse % FIELD for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][j] - factor * work[column][j]) % FIELD
                for j in range(2 * size)
            ]
    return [row[size:] for row in work]


def trace_mod(matrix: list[list[int]]) -> int:
    return sum(matrix[i][i] for i in range(len(matrix))) % FIELD


def zero_matrix(rows: int, columns: int) -> list[list[int]]:
    return [[0 for _ in range(columns)] for _ in range(rows)]


def identity_matrix(size: int) -> list[list[int]]:
    return [
        [1 if row == column else 0 for column in range(size)]
        for row in range(size)
    ]


def star_coordinate_basis() -> tuple[list[tuple[int, int]], list[list[list[int]]]]:
    edges = list(combinations(range(7), 2))
    basis: list[list[list[int]]] = []
    for i, j in edges:
        matrix = zero_matrix(7, 7)
        matrix[i][j] = matrix[j][i] = 1
        matrix[i][i] = matrix[j][j] = 2
        basis.append(matrix)
    return edges, basis


def transition_gram(
    cross: list[list[int]], basis: list[list[list[int]]]
) -> list[list[int]]:
    cross_transpose = transpose(cross)
    return [
        [
            trace_mod(
                matmul(
                    matmul(matmul(left, cross), right),
                    cross_transpose,
                )
            )
            for right in basis
        ]
        for left in basis
    ]


def canonical_cross_matrix(rank: int) -> list[list[int]]:
    # The six columns e_i-e_6 span 1^perp in F_3^7.  Since 1 has norm
    # seven = one, this is a nondegenerate complement to <1>.
    quotient_basis = zero_matrix(7, 6)
    for i in range(6):
        quotient_basis[i][i] = 1
        quotient_basis[6][i] = 2
    quotient_gram = matmul(transpose(quotient_basis), quotient_basis)
    quotient_gram_inverse = inverse_mod(quotient_gram)
    diagonal = [
        [1 if i == j and i < rank else 0 for j in range(6)]
        for i in range(6)
    ]
    return matmul(
        matmul(
            matmul(quotient_basis, diagonal),
            quotient_gram_inverse,
        ),
        transpose(quotient_basis),
    )


def transition_rank_audit() -> dict[str, Any]:
    edges, basis = star_coordinate_basis()
    star_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    same_center = transition_gram(star_gram, basis)
    ranks: dict[str, Any] = {}
    for cross_rank in range(7):
        cross = canonical_cross_matrix(cross_rank)
        transition = transition_gram(cross, basis)
        expected = cross_rank * (cross_rank + 1) // 2
        actual_cross_rank = rank_mod(cross)
        actual_transition_rank = rank_mod(transition)
        if actual_cross_rank != cross_rank or actual_transition_rank != expected:
            raise AssertionError("symmetric-square transition rank changed")
        if any(sum(row) % FIELD for row in cross):
            raise AssertionError("canonical cross matrix lost C*1=0")
        if any(sum(row) % FIELD for row in transpose(cross)):
            raise AssertionError("canonical cross matrix lost C^T*1=0")
        ranks[str(cross_rank)] = {
            "cross_rank": actual_cross_rank,
            "transition_rank": actual_transition_rank,
            "transition_left_radical_dimension": 21
            - actual_transition_rank,
            "formula": f"binom({cross_rank}+1,2)",
        }
    return {
        "coordinate_count": len(edges),
        "coordinate_space": "symmetric 7x7 matrices R with R*1=0",
        "same_center_J_star_rank": rank_mod(same_center),
        "same_center_J_star_determinant": determinant_mod(same_center),
        "cross_rank_table": ranks,
    }


def characteristic_three_radical_audit() -> dict[str, Any]:
    _, basis = star_coordinate_basis()
    star_gram = [
        [0 if row == column else 1 for column in range(7)]
        for row in range(7)
    ]
    j_star = transition_gram(star_gram, basis)

    # In the 21 off-diagonal coordinates, trace(A)=2*sum_e r_e.
    # The vectors e_i-e_20 give a basis of the trace-zero hyperplane.
    trace_zero_basis: list[list[int]] = []
    for i in range(20):
        vector = [0] * 21
        vector[i] = 1
        vector[20] = 2
        trace_zero_basis.append(vector)
    restricted_gram = matmul(
        matmul(trace_zero_basis, j_star),
        transpose(trace_zero_basis),
    )
    identity_coordinate = [1] * 21
    identity_is_in_hyperplane = (
        rank_mod(trace_zero_basis + [identity_coordinate])
        == rank_mod(trace_zero_basis)
    )
    identity_pairings = matmul(
        [identity_coordinate],
        matmul(j_star, transpose(trace_zero_basis)),
    )[0]

    trace_one_feature = [0] * 21
    trace_one_feature[20] = 1
    repaired_features = trace_zero_basis + [trace_one_feature]
    repaired_gram = matmul(
        matmul(repaired_features, j_star),
        transpose(repaired_features),
    )

    if rank_mod(trace_zero_basis) != 20:
        raise AssertionError("trace-zero synthesis rank changed")
    if rank_mod(restricted_gram) != 19:
        raise AssertionError("trace-zero Gram rank changed")
    if not identity_is_in_hyperplane or any(identity_pairings):
        raise AssertionError("identity radical audit changed")
    if rank_mod(repaired_features) != 21 or rank_mod(repaired_gram) != 21:
        raise AssertionError("mixed trace-one repair changed")

    return {
        "full_self_adjoint_dimension": 21,
        "full_trace_pairing_rank": rank_mod(j_star),
        "trace_zero_feature_synthesis_rank": rank_mod(trace_zero_basis),
        "trace_zero_feature_gram_rank": rank_mod(restricted_gram),
        "trace_zero_radical_dimension": 1,
        "trace_zero_radical": "span{I_6}",
        "trace_I6_squared": 6 % FIELD,
        "identity_coordinate": identity_coordinate,
        "identity_is_nonzero_true_feature": True,
        "identity_is_gram_null_against_trace_zero_space": True,
        "gram_nullity_minus_true_relation_nullity": 1,
        "adding_one_trace_nonzero_feature": {
            "feature_synthesis_rank": rank_mod(repaired_features),
            "feature_gram_rank": rank_mod(repaired_gram),
            "identity_radical_is_detected": True,
        },
    }


def polynomial_trim(polynomial: list[int]) -> list[int]:
    result = [coefficient % FIELD for coefficient in polynomial]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_divmod(
    dividend: list[int], divisor: list[int]
) -> tuple[list[int], list[int]]:
    numerator = polynomial_trim(dividend)
    denominator = polynomial_trim(divisor)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    denominator_inverse = pow(denominator[-1], -1, FIELD)
    while len(numerator) >= len(denominator) and numerator != [0]:
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] * denominator_inverse % FIELD
        quotient[degree] = coefficient
        for i, entry in enumerate(denominator):
            numerator[degree + i] = (
                numerator[degree + i] - coefficient * entry
            ) % FIELD
        numerator = polynomial_trim(numerator)
    return polynomial_trim(quotient), polynomial_trim(numerator)


def polynomial_gcd(left: list[int], right: list[int]) -> list[int]:
    a = polynomial_trim(left)
    b = polynomial_trim(right)
    while b != [0]:
        _, remainder = polynomial_divmod(a, b)
        a, b = b, remainder
    inverse = pow(a[-1], -1, FIELD)
    return [coefficient * inverse % FIELD for coefficient in a]


def polynomial_multiply_mod(
    left: list[int], right: list[int], modulus: list[int]
) -> list[int]:
    product = [0] * (len(left) + len(right) - 1)
    for i, left_entry in enumerate(left):
        for j, right_entry in enumerate(right):
            product[i + j] = (
                product[i + j] + left_entry * right_entry
            ) % FIELD
    _, remainder = polynomial_divmod(product, modulus)
    return remainder


def polynomial_power_mod(
    base: list[int], exponent: int, modulus: list[int]
) -> list[int]:
    result = [1]
    power = polynomial_trim(base)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = polynomial_multiply_mod(result, power, modulus)
        power = polynomial_multiply_mod(power, power, modulus)
        remaining //= 2
    return polynomial_trim(result)


def companion_matrix() -> list[list[int]]:
    # Multiplication by t in the basis 1,t,...,t^4 of
    # F_3[t]/(t^5+2t^4+1).  The relation is t^5=t^4+2.
    matrix = zero_matrix(5, 5)
    for column in range(4):
        matrix[column + 1][column] = 1
    matrix[0][4] = 2
    matrix[4][4] = 1
    return matrix


def standard_basis_vector(dimension: int, index: int) -> list[int]:
    return [1 if coordinate == index else 0 for coordinate in range(dimension)]


def add_vectors(left: list[int], right: list[int]) -> list[int]:
    return [(a + b) % FIELD for a, b in zip(left, right, strict=True)]


def symmetric_matrix_coordinates(matrix: list[list[int]]) -> list[int]:
    return [
        matrix[i][j] % FIELD
        for i in range(len(matrix))
        for j in range(i, len(matrix))
    ]


def symmetric_square_columns(subspace_basis: list[list[int]]) -> list[list[int]]:
    dimension = len(subspace_basis[0])
    columns: list[list[int]] = []
    for i in range(len(subspace_basis)):
        for j in range(i, len(subspace_basis)):
            matrix = zero_matrix(dimension, dimension)
            left = subspace_basis[i]
            right = subspace_basis[j]
            for row in range(dimension):
                for column in range(dimension):
                    if i == j:
                        matrix[row][column] = left[row] * left[column] % FIELD
                    else:
                        matrix[row][column] = (
                            left[row] * right[column]
                            + right[row] * left[column]
                        ) % FIELD
            columns.append(symmetric_matrix_coordinates(matrix))
    return columns


def subspace_gram(subspace_basis: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(left[k] * right[k] for k in range(len(left))) % FIELD
            for right in subspace_basis
        ]
        for left in subspace_basis
    ]


def cross_gram_rank(
    left_basis: list[list[int]], right_basis: list[list[int]]
) -> int:
    cross = [
        [
            sum(left[k] * right[k] for k in range(len(left))) % FIELD
            for right in right_basis
        ]
        for left in left_basis
    ]
    return rank_mod(cross)


def graph_restriction_rows(graph_matrix: list[list[int]]) -> list[list[int]]:
    rows: list[list[int]] = []
    graph_transpose = transpose(graph_matrix)
    for i in range(5):
        for j in range(i, 5):
            equation: list[int] = []
            for p in range(5):
                for q in range(5):
                    # Coefficient of K[p,q] in
                    # (K*B+B^T*K^T)[i,j].
                    coefficient = 0
                    if p == i:
                        coefficient += graph_matrix[q][j]
                    if p == j:
                        coefficient += graph_transpose[i][q]
                    equation.append(coefficient % FIELD)
            rows.append(equation)
    return rows


def four_center_certificate_audit() -> dict[str, Any]:
    ambient_dimension = 11
    ell = standard_basis_vector(ambient_dimension, 0)
    u_vectors = [
        standard_basis_vector(ambient_dimension, 1 + i) for i in range(5)
    ]
    w_vectors = [
        standard_basis_vector(ambient_dimension, 6 + i) for i in range(5)
    ]
    companion = companion_matrix()

    first = [ell, *u_vectors]
    second = [ell, *w_vectors]
    third = [
        ell,
        *[add_vectors(u_vectors[i], w_vectors[i]) for i in range(5)],
    ]
    fourth_vectors = [ell]
    for column in range(5):
        vector = u_vectors[column][:]
        for row in range(5):
            vector = add_vectors(
                vector,
                [
                    companion[row][column] * entry % FIELD
                    for entry in w_vectors[row]
                ],
            )
        fourth_vectors.append(vector)
    fourth = fourth_vectors

    spaces = [first, second, third, fourth]
    square_columns = [symmetric_square_columns(space) for space in spaces]
    cumulative_ranks = []
    accumulated: list[list[int]] = []
    for columns in square_columns:
        accumulated.extend(columns)
        cumulative_ranks.append(rank_mod(matrix_from_columns(accumulated)))

    identity5 = identity_matrix(5)
    restriction_rows = graph_restriction_rows(identity5) + graph_restriction_rows(
        companion
    )
    restriction_rank = rank_mod(restriction_rows)

    polynomial = [1, 0, 0, 0, 2, 1]
    x_polynomial = [0, 1]
    x_cubed = polynomial_power_mod(x_polynomial, FIELD, polynomial)
    x_cubed_minus_x = x_cubed[:]
    if len(x_cubed_minus_x) < 2:
        x_cubed_minus_x.extend([0] * (2 - len(x_cubed_minus_x)))
    x_cubed_minus_x[1] = (x_cubed_minus_x[1] - 1) % FIELD
    x_cubed_minus_x = polynomial_trim(x_cubed_minus_x)
    linear_factor_gcd = polynomial_gcd(polynomial, x_cubed_minus_x)
    frobenius_remainder = polynomial_power_mod(
        x_polynomial, FIELD**5, polynomial
    )
    irreducible = linear_factor_gcd == [1] and frobenius_remainder == [0, 1]

    local_gram_ranks = [rank_mod(subspace_gram(space)) for space in spaces]
    local_gram_determinants = [
        determinant_mod(subspace_gram(space)) for space in spaces
    ]
    cross_ranks = [
        [cross_gram_rank(left, right) for right in spaces] for left in spaces
    ]

    if cumulative_ranks != [21, 41, 56, 66]:
        raise AssertionError("four-center symmetric-square ranks changed")
    if restriction_rank != 25:
        raise AssertionError("25-coordinate restriction certificate changed")
    if not irreducible:
        raise AssertionError("degree-five companion polynomial changed")
    if local_gram_ranks != [6, 6, 6, 6]:
        raise AssertionError("four-center control lost nondegeneracy")

    return {
        "ambient_dimension": ambient_dimension,
        "self_adjoint_dimension": ambient_dimension
        * (ambient_dimension + 1)
        // 2,
        "four_subspaces": 4,
        "each_subspace_dimension": 6,
        "cumulative_symmetric_square_span_ranks": cumulative_ranks,
        "first_full_span_pair": {
            "intersection_dimension": 1,
            "symmetric_square_span_rank": cumulative_ranks[1],
            "annihilator_dimension": 66 - cumulative_ranks[1],
            "annihilator_normal_form": (
                "a 5x5 cross matrix K between complements of the common line"
            ),
        },
        "two_additional_center_restriction_rank_on_K": restriction_rank,
        "four_center_symmetric_square_span_is_full": cumulative_ranks[-1] == 66,
        "companion_polynomial": "t^5+2t^4+1",
        "irreducibility_rabin_checks": {
            "gcd_with_t^3_minus_t": linear_factor_gcd,
            "t_to_3_power_5_mod_polynomial": frobenius_remainder,
            "irreducible": irreducible,
        },
        "local_standard_form_gram_ranks": local_gram_ranks,
        "local_standard_form_gram_determinants": local_gram_determinants,
        "pairwise_cross_gram_ranks": cross_ranks,
        "control_scope_failure": [
            "ambient standard form has square discriminant, not the endpoint nonsquare type",
            "there are only four abstract six-spaces, not 99 graph stars",
            "there are no seven-column singular simplexes or shared 231 columns",
            "there is no point-triangle incidence, SRG, or prism-free graph",
        ],
    }


def build_results() -> dict[str, Any]:
    return {
        "format": "wave207-mixed-four-center-proof-b-v1",
        "field": FIELD,
        "claim_label": "DERIVED_PENDING_INDEPENDENT_VERIFICATION",
        "scope": (
            "conditional prism-free n3=4158 rank-11 endpoint; exact kernel, "
            "radical, mixed-transition, and four-center compression algebra"
        ),
        "simultaneous_compression_theorem": {
            "map": "C(A)=(P_y A P_y restricted to E_y)_y",
            "adjoint": "C^*((X_y)_y)=sum_y X_y",
            "normal_operator": "C^*C(A)=Phi(A)=sum_y P_y A P_y",
            "local_operator_span": "J=sum_y Self(E_y)",
            "kernel": "ker C=J^perp",
            "projector_span_kernel": (
                "ker(C restricted to S)=S intersect rad(J), S=span{P_x}"
            ),
            "warning": (
                "ker Phi may strictly contain ker C because im(C) can be "
                "isotropic in characteristic three"
            ),
        },
        "gram_radical_exact_sequence": {
            "general": (
                "for synthesis R with Gram G, 0 -> ker(R) -> ker(G) "
                "-> rad(im R) -> 0 via c |-> R(c)"
            ),
            "fixed_slice": (
                "ker(Tau^(y))/ker(R_y) is isomorphic to rad(F_y)"
            ),
            "global_mixed": "ker(M)/ker(R_all) is isomorphic to rad(F)",
            "rank_defect": "rank(R_all)-rank(M)=dim rad(F)",
            "feature_definitions": {
                "F_yx": "P_y P_x P_y",
                "F_y": "span_x{F_yx}",
                "F": "span_(y,x){F_yx}",
                "M": "M[(y,x),(v,z)]=tr(F_yx F_vz)",
            },
            "center_coefficient_kernel_chain": (
                "K_P subset K_C subset K_mix subset intersection_y ker(Tau^(y))"
            ),
            "nondegenerate_mixed_span_consequence": (
                "rad(F)=0 implies K_P=K_C=K_mix"
            ),
            "rank_66_certificate": (
                "a rank-66 mixed Gram submatrix from four middle-center rows "
                "forces F=Self(V), kills all radical defects, and makes the "
                "four selected compressions jointly injective"
            ),
            "why_four_is_first_possible": "3*dim Self(E_y)=3*21=63<66",
        },
        "transition_rank_audit": transition_rank_audit(),
        "characteristic_three_radical_audit": (
            characteristic_three_radical_audit()
        ),
        "four_center_certificate_audit": four_center_certificate_audit(),
        "A_Delta_functorial_boundary": {
            "linear_relation_correction": (
                "a=B^T c and BD=0 imply D a=0; full-rank nondegenerate "
                "factorization then implies Z a=0"
            ),
            "operator_relation": (
                "Theta(a)=0 and injectivity of A |-> Z^* A Z imply "
                "sum_x c_x P_x=-sum_T a_T(z_T tensor z_T)=0"
            ),
            "sandwich_annihilation": (
                "sum_x c_x F_yx=P_y(sum_x c_xP_x)P_y=0 for every y"
            ),
            "mixed_annihilation": (
                "sum_x c_x M[(y,x),(v,z)]=0 for every y,v,z"
            ),
            "consequence": (
                "linear sandwich and mixed trace-Gram constructions cannot "
                "classify or exclude an already true A_Delta relation; "
                "nonlinear or graph-typed data are required"
            ),
        },
        "conclusions": {
            "new_exact_mixed_center_compatibility_theorem": True,
            "new_exact_transition_rank_formula": "rank=binom(rank(C_yv)+1,2)",
            "new_four_center_25_coordinate_certificate": True,
            "rank_66_certificate_established_for_endpoint": False,
            "rank_11_endpoint_excluded": False,
            "n3_improved": False,
            "Q_7060_proved": False,
            "conway_99_resolved": False,
            "status": "UNKNOWN",
        },
    }


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", type=Path)
    action.add_argument("--verify", type=Path)
    args = parser.parse_args()
    data = build_results()
    rendered = canonical_json(data)
    if args.write is not None:
        args.write.write_text(rendered, encoding="utf-8", newline="\n")
        return
    expected = args.verify.read_text(encoding="utf-8")
    if expected != rendered:
        raise SystemExit("exact results do not match deterministic replay")
    print(f"PASS: {args.verify}")


if __name__ == "__main__":
    main()
