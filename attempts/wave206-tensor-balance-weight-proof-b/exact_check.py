"""Exact checks for the Wave 206 tensor-balance weight addendum."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable


FIELD = 3
ROOT = Path(__file__).resolve().parents[2]
EXPECTED_INPUTS = {
    "attempts/wave206-tensor-balance-weight-proof-b/protocol.md":
        "96d7e061a5df7aee9cf675198535788be11a0f0f2491536d0a18d51ab767319e",
    "attempts/wave206-crossing-kernel-proof-b/package-manifest.sha256":
        "6c7718de1c5f2c7d4203d1727d6b74214e51fa069608f318c8583b07b0325f0a",
    "verification/wave174-no-weight3-dual/package-manifest.sha256":
        "ac34c8a3b045bec70e3a2080cb4365c0ea43cc732b313ecb3cec355a28f23450",
    "verification/wave174-no-weight3-dual/verification-report.md":
        "59bc0e470a7d007aa2ddaec262a2f3046c8df7da56192bdab90327962feb9b0a",
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


def block_diagonal(*blocks: Matrix) -> Matrix:
    size = sum(len(block) for block in blocks)
    result = zero(size, size)
    offset = 0
    for block in blocks:
        for row in range(len(block)):
            for column in range(len(block)):
                result[offset + row][offset + column] = mod(block[row][column])
        offset += len(block)
    return result


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


def gf3_rref(matrix: Matrix) -> tuple[Matrix, list[int]]:
    if not matrix:
        return [], []
    rows = [[mod(entry) for entry in row] for row in matrix]
    width = len(rows[0])
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


def gf3_determinant(matrix: Matrix) -> int:
    rows = [[mod(entry) for entry in row] for row in matrix]
    size = len(rows)
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
        for row in range(column + 1, size):
            multiplier = mod(rows[row][column] * inverse)
            rows[row] = [
                mod(rows[row][index] - multiplier * rows[column][index])
                for index in range(size)
            ]
    return determinant


def canonical_projective(vector: tuple[int, ...]) -> tuple[int, ...]:
    first = next(value for value in vector if value)
    inverse = pow(first, -1, FIELD)
    return tuple(mod(inverse * value) for value in vector)


def projective_points(vector_dimension: int) -> list[tuple[int, ...]]:
    points = []
    for vector in itertools.product(range(FIELD), repeat=vector_dimension):
        if not any(vector):
            continue
        canonical = canonical_projective(vector)
        if canonical not in points:
            points.append(canonical)
    return points


def is_cap(points: list[tuple[int, ...]]) -> bool:
    return all(
        gf3_rank([
            list(points[first]),
            list(points[second]),
            list(points[third]),
        ]) == 3
        for first, second, third in itertools.combinations(range(len(points)), 3)
    )


def exact_cap_maximum(vector_dimension: int) -> tuple[int, int]:
    points = projective_points(vector_dimension)
    maximum = 0
    maximum_count = 0
    for mask in range(1 << len(points)):
        size = mask.bit_count()
        if size < maximum:
            continue
        selected = [
            point for index, point in enumerate(points) if (mask >> index) & 1
        ]
        if not is_cap(selected):
            continue
        if size > maximum:
            maximum = size
            maximum_count = 1
        else:
            maximum_count += 1
    return maximum, maximum_count


def cap_summary() -> dict[str, Any]:
    results = {}
    expected = {1: 1, 2: 2, 3: 4}
    for dimension in (1, 2, 3):
        maximum, count = exact_cap_maximum(dimension)
        if maximum != expected[dimension]:
            raise AssertionError("small projective cap maximum changed")
        results[str(dimension)] = {
            "projective_space": f"PG({dimension - 1},3)",
            "projective_points": len(projective_points(dimension)),
            "maximum_no_three_collinear": maximum,
            "number_of_maximum_labelled_subsets": count,
        }
    return {
        "exact_exhaustion": results,
        "cap_transfer": (
            "dual distance at least four means every three selected original "
            "columns are linearly independent, hence the support points form "
            "a projective cap in their span"
        ),
    }


def witt_index_diagonal(dimension: int, number_of_twos: int) -> int:
    if dimension % 2:
        return dimension // 2
    half = dimension // 2
    determinant_square_class = number_of_twos % 2
    hyperbolic_square_class = half % 2
    return half if determinant_square_class == hyperbolic_square_class else half - 1


def witt_summary() -> dict[str, Any]:
    table = {}
    for dimension in range(1, 9):
        rows = []
        for number_of_twos in range(dimension + 1):
            index = witt_index_diagonal(dimension, number_of_twos)
            if index > dimension // 2:
                raise AssertionError("Witt index exceeded the dimension bound")
            rows.append({
                "number_of_coefficient_2_entries": number_of_twos,
                "determinant": pow(2, number_of_twos, FIELD),
                "witt_index": index,
            })
        table[str(dimension)] = rows
    return {
        "coefficient_form": "Lambda=diag(a_i), every a_i in {1,2}",
        "nondegenerate": True,
        "row_space_consequence": (
            "V Lambda V^T=0 makes row(V) totally isotropic, so "
            "rank(V)<=WittIndex(Lambda)<=floor(k/2)"
        ),
        "dimension_bound_proof": (
            "U subset U^perp and nondegeneracy gives "
            "dim(U)+dim(U^perp)=k, hence 2 dim(U)<=k"
        ),
        "exact_diagonal_form_table": table,
    }


def exclusion_summary(caps: dict[str, Any]) -> dict[str, Any]:
    cap_maxima = {
        dimension: caps["exact_exhaustion"][str(dimension)][
            "maximum_no_three_collinear"
        ]
        for dimension in (1, 2, 3)
    }
    rows = []
    for support in range(1, 8):
        maximum_rank = support // 2
        if maximum_rank == 0:
            maximum_cap = 0
        else:
            maximum_cap = cap_maxima[maximum_rank]
        excluded = maximum_cap < support
        if not excluded:
            raise AssertionError("a support at most seven survived")
        rows.append({
            "support_size": support,
            "maximum_span_rank_from_Witt": maximum_rank,
            "maximum_cap_in_that_rank": maximum_cap,
            "excluded": excluded,
        })
    return {
        "cases": rows,
        "conclusion": "every nonzero tensor-balance word has weight at least eight",
    }


def weight_eight_boundary() -> dict[str, Any]:
    split_compositions = [
        number_of_twos
        for number_of_twos in range(9)
        if witt_index_diagonal(8, number_of_twos) == 4
    ]
    if split_compositions != [0, 2, 4, 6, 8]:
        raise AssertionError("weight-eight split-form compositions changed")
    return {
        "forced_span_rank": 4,
        "reason": (
            "an eight-point cap cannot lie in projective dimension at most "
            "two, while the Witt bound gives rank at most four"
        ),
        "coefficient_form": "Lambda must be the split 8-dimensional form",
        "allowed_number_of_coefficient_2_entries": split_compositions,
        "composition_consequence": (
            "the number of coefficient-2 support entries is even"
        ),
    }


WEIGHT_EIGHT_COLUMNS = [
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (0, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 2),
]
WEIGHT_EIGHT_COEFFICIENTS = [1, 1, 1, 2, 2, 2, 2, 1]
SUPPORT_FORM = [
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 2],
    [1, 1, 2, 0],
]


def tensor_matrix(
    columns: list[tuple[int, ...]], coefficients: list[int]
) -> Matrix:
    dimension = len(columns[0])
    result = zero(dimension, dimension)
    for vector, coefficient in zip(columns, coefficients):
        for row in range(dimension):
            for column in range(dimension):
                result[row][column] = mod(
                    result[row][column]
                    + coefficient * vector[row] * vector[column]
                )
    return result


def bilinear_norm(vector: tuple[int, ...], form: Matrix) -> int:
    return mod(sum(
        vector[row] * form[row][column] * vector[column]
        for row in range(len(vector))
        for column in range(len(vector))
    ))


def weight_eight_control() -> dict[str, Any]:
    columns = WEIGHT_EIGHT_COLUMNS
    coefficients = WEIGHT_EIGHT_COEFFICIENTS
    synthesis = transpose([list(vector) for vector in columns])
    coefficient_form = diagonal(coefficients)
    isotropic_rows = matrix_multiply(
        matrix_multiply(synthesis, coefficient_form),
        transpose(synthesis),
    )
    if isotropic_rows != zero(4, 4):
        raise AssertionError("weight-eight tensor relation changed")
    if gf3_rank(synthesis) != 4:
        raise AssertionError("weight-eight span rank changed")
    if not is_cap(columns):
        raise AssertionError("weight-eight support lost dual distance four")
    if gf3_rank(SUPPORT_FORM) != 4 or gf3_determinant(SUPPORT_FORM) != 1:
        raise AssertionError("support singular form changed")
    if any(bilinear_norm(vector, SUPPORT_FORM) for vector in columns):
        raise AssertionError("a support column became nonsingular")

    complement = diagonal([1] * 6 + [2])
    ambient_form = block_diagonal(SUPPORT_FORM, complement)
    if gf3_rank(ambient_form) != 11 or gf3_determinant(ambient_form) != 2:
        raise AssertionError("ambient nonsquare 11-form changed")
    embedded = [
        tuple(vector) + (0,) * 7 for vector in columns
    ]
    if any(bilinear_norm(vector, ambient_form) for vector in embedded):
        raise AssertionError("embedded support column became nonsingular")

    operator_sum = tensor_matrix(embedded, coefficients)
    if operator_sum != zero(11, 11):
        raise AssertionError("embedded tensor relation changed")

    return {
        "support_size": 8,
        "span_rank": gf3_rank(synthesis),
        "all_coefficients_nonzero": True,
        "coefficient_composition": {"1": 4, "2": 4},
        "coefficient_form_witt_index": witt_index_diagonal(8, 4),
        "every_three_columns_independent": True,
        "projectively_distinct": True,
        "tensor_sum_zero": True,
        "support_form_rank": gf3_rank(SUPPORT_FORM),
        "support_form_determinant": gf3_determinant(SUPPORT_FORM),
        "all_support_columns_singular": True,
        "ambient_dimension": 11,
        "ambient_form_determinant": gf3_determinant(ambient_form),
        "ambient_form_nonsquare": True,
        "conclusion": (
            "weight eight is attainable under the tensor relation, "
            "projectivity, dual-distance-four, singular-column, and "
            "nonsquare-11-space premises"
        ),
        "failed_endpoint_premises": [
            "only eight support columns are supplied, not a shared 231-column frame",
            "there is no 99-by-231 point-triangle incidence",
            "there is no endpoint centered code or zero global frame",
            "there is no srg(99,14,1,2) or prism-free graph",
            "the control does not assert that its coefficient word lies in im(B^T)",
        ],
    }


def analyze() -> dict[str, Any]:
    caps = cap_summary()
    return {
        "claim_label": "DERIVED_PENDING_INDEPENDENT_VERIFICATION",
        "field": 3,
        "scope": (
            "support bound for the nonzero nonconstant Wave 206 "
            "tensor-balance intersection-code word"
        ),
        "inputs": verify_inputs(),
        "operator_to_coefficient_form": {
            "rank_one_operator_equation": (
                "sum_i a_i(z_i tensor z_i)=0"
            ),
            "ordinary_tensor_equation": "V Lambda V^T=0",
            "ambient_form_step": (
                "the operator matrix is V Lambda V^T F; multiply by "
                "the invertible ambient form F^{-1}"
            ),
            "support_span_step": (
                "factoring V=E X with E full column rank and applying a "
                "left inverse gives X Lambda X^T=0; the ambient support "
                "span need not be nondegenerate"
            ),
        },
        "witt_audit": witt_summary(),
        "cap_audit": caps,
        "small_support_exclusion": exclusion_summary(caps),
        "weight_eight_boundary": weight_eight_boundary(),
        "weight_eight_control": weight_eight_control(),
        "conclusions": {
            "tensor_balance_weight_lower_bound": 8,
            "weight_nine_lower_bound_proved": False,
            "crossing_package_promoted_to_verified": False,
            "rank11_endpoint_excluded": False,
            "n3_improved": False,
            "Q_7060_proved": False,
            "conway_99_resolved": False,
            "status": "UNKNOWN",
        },
    }


def verify(data: dict[str, Any]) -> None:
    if data["small_support_exclusion"]["conclusion"] != (
        "every nonzero tensor-balance word has weight at least eight"
    ):
        raise AssertionError("weight conclusion mutated")
    if any(
        not row["excluded"]
        for row in data["small_support_exclusion"]["cases"]
    ):
        raise AssertionError("a small support was un-excluded")
    caps = data["cap_audit"]["exact_exhaustion"]
    if [caps[str(rank)]["maximum_no_three_collinear"] for rank in (1, 2, 3)] != [
        1, 2, 4
    ]:
        raise AssertionError("cap maxima mutated")
    control = data["weight_eight_control"]
    if (
        control["support_size"] != 8
        or control["span_rank"] != 4
        or control["coefficient_form_witt_index"] != 4
        or not control["tensor_sum_zero"]
        or not control["every_three_columns_independent"]
        or not control["all_support_columns_singular"]
        or control["ambient_form_determinant"] != 2
    ):
        raise AssertionError("weight-eight control mutated")
    if data["weight_eight_boundary"][
        "allowed_number_of_coefficient_2_entries"
    ] != [0, 2, 4, 6, 8]:
        raise AssertionError("weight-eight coefficient parity mutated")
    if not any(
        "im(B^T)" in item for item in control["failed_endpoint_premises"]
    ):
        raise AssertionError("weight-eight control scope was weakened")

    conclusions = data["conclusions"]
    if conclusions["tensor_balance_weight_lower_bound"] != 8:
        raise AssertionError("weight lower bound mutated")
    forbidden = [
        "weight_nine_lower_bound_proved",
        "crossing_package_promoted_to_verified",
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
