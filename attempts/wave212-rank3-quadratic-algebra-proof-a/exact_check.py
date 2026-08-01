#!/usr/bin/env python3
"""Exact Wave 212 proof-A replay: mod-2 Jordan and K-projector closures.

Only Python's standard library is used.  The script does not search for D.
It derives consequences shared by every hypothetical quadratic completion of
the three frozen Wave 210 representatives and checks that two proposed
symbolic shortcut families close consistently rather than contradicting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json"
RESULTS = HERE / "exact-results.json"
MANIFEST = HERE / "package-manifest.sha256"
UPSTREAM_SHA256 = "32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd"
ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> None:
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, relative = raw.split("  ", 1)
        assert sha256(ROOT / relative) == expected, relative


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def identity(n: int):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    augmented = [
        list(map(Fraction, row)) + identity(n)[i]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [row[n:] for row in augmented]


def matrix_rank_q(rows) -> int:
    matrix = [list(map(Fraction, row)) for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def independent_row_indices(rows):
    chosen = []
    current = []
    rank = 0
    for index, row in enumerate(rows):
        trial = current + [row]
        trial_rank = matrix_rank_q(trial)
        if trial_rank > rank:
            chosen.append(index)
            current.append(row)
            rank = trial_rank
    return chosen


def rank_f2(matrix) -> int:
    masks = [
        sum((value & 1) << column for column, value in enumerate(row))
        for row in matrix
    ]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(masks)) if (masks[row] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        masks[rank], masks[pivot] = masks[pivot], masks[rank]
        for row in range(len(masks)):
            if row != rank and ((masks[row] >> column) & 1):
                masks[row] ^= masks[rank]
        rank += 1
    return rank


def matmul_f2(left, right):
    right_rows = [
        sum((value & 1) << column for column, value in enumerate(row))
        for row in right
    ]
    out = []
    for row in left:
        mask = 0
        for index, value in enumerate(row):
            if value & 1:
                mask ^= right_rows[index]
        out.append([(mask >> column) & 1 for column in range(len(right[0]))])
    return out


def characteristic_polynomial(matrix):
    """Faddeev-LeVerrier coefficients, highest degree first."""
    n = len(matrix)
    ident = [[int(i == j) for j in range(n)] for i in range(n)]
    b = ident
    coefficients = [1]
    for k in range(1, n + 1):
        product = matmul(matrix, b)
        trace = sum(product[i][i] for i in range(n))
        assert trace % k == 0
        coefficient = -trace // k
        coefficients.append(coefficient)
        b = [
            [product[i][j] + coefficient * int(i == j) for j in range(n)]
            for i in range(n)
        ]
    return coefficients


def poly_mul(left, right):
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return output


def poly_pow_mod2(base, exponent):
    result = [1]
    while exponent:
        if exponent & 1:
            result = [value & 1 for value in poly_mul(result, base)]
        base = [value & 1 for value in poly_mul(base, base)]
        exponent //= 2
    return result


def forced_action_polynomial():
    support = support_adjacency()
    operator = [[0] * 15 for _ in range(15)]
    for i in range(14):
        for j in range(14):
            operator[i][j] = -(support[i][j] + int(i == j))
        operator[i][14] = -1
        operator[14][i] = 2
    operator[14][14] = 14
    full = characteristic_polynomial(operator)
    quotient = [full[0]]
    for coefficient in full[1:-1]:
        quotient.append(coefficient - 4 * quotient[-1])
    assert full[-1] == 4 * quotient[-1]
    expected = [1]
    expected = poly_mul(expected, [1, 0, 0])
    expected = poly_mul(expected, [1, 4, 4])
    for _ in range(3):
        expected = poly_mul(expected, [1, 0, -2])
    expected = poly_mul(expected, [1, -8, -50, -40, 32])
    assert quotient == expected
    return quotient


def support_adjacency():
    matrix = [[0] * 14 for _ in range(14)]
    for offset in (0, 7):
        for u, v in ROOTED_EDGES:
            matrix[u + offset][v + offset] = 1
            matrix[v + offset][u + offset] = 1
    matrix[0][7] = matrix[7][0] = 1
    return matrix


def incidence(control):
    matrix = [[0] * 85 for _ in range(14)]
    for column, neighbors in enumerate(control["F_columns_support_neighbors"]):
        for support in neighbors:
            matrix[support][column] = 1
    return matrix


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def distribution(values):
    counts = Counter(values)
    return [
        {"value": fraction_text(value), "multiplicity": counts[value]}
        for value in sorted(counts)
    ]


def jordan_type_from_ranks(ranks):
    # ranks[k] is rank(N^k), including rank(N^0)=85.
    at_least = {
        size: ranks[size - 1] - ranks[size]
        for size in range(1, len(ranks))
    }
    exact = {
        size: at_least[size] - at_least.get(size + 1, 0)
        for size in range(1, len(ranks))
    }
    return {
        "blocks_of_size_at_least": {str(size): count for size, count in at_least.items()},
        "blocks_of_exact_size": {
            str(size): count for size, count in exact.items() if count
        },
        "compact": "J5^2 + J3^2 + J1^69",
    }


def analyze_orbit(control):
    f = incidence(control)
    ftf = [[value & 1 for value in row] for row in matmul(transpose(f), f)]
    powers = []
    power = ftf
    for _ in range(5):
        powers.append(rank_f2(power))
        power = matmul_f2(power, ftf)
    assert powers == [12, 8, 4, 2, 0]
    ranks_with_identity = [85] + powers
    jordan = jordan_type_from_ranks(ranks_with_identity)
    assert jordan["blocks_of_exact_size"] == {"1": 69, "3": 2, "5": 2}

    # Exact orthogonal projector P_U, where U=rowspan(F,1), and the forced
    # action D P_U obtained from FD and the degree row.
    all_rows = f + [[1] * 85]
    indices = independent_row_indices(all_rows)
    assert len(indices) == 14
    b = [all_rows[index] for index in indices]
    gram_inverse = inverse(matmul(b, transpose(b)))
    p_u = matmul(matmul(transpose(b), gram_inverse), b)
    assert p_u == transpose(p_u)
    assert matmul(p_u, p_u) == p_u

    a_s = support_adjacency()
    fd = [[
        2 - sum((a_s[s][t] + int(s == t)) * f[t][j] for t in range(14))
        for j in range(85)
    ] for s in range(14)]
    degrees = [14 - sum(f[s][j] for s in range(14)) for j in range(85)]
    all_bd = fd + [degrees]
    bd = [all_bd[index] for index in indices]
    dp_u = matmul(matmul(transpose(b), gram_inverse), bd)
    assert dp_u == transpose(dp_u)

    e3_diag = []
    em4_diag = []
    pk_diag = []
    for i in range(85):
        pk = 1 - p_u[i][i]
        e3 = (-dp_u[i][i] + 4 * pk) / 7
        em4 = (dp_u[i][i] + 3 * pk) / 7
        assert e3 + em4 == pk
        assert 0 < e3 < 1 and 0 < em4 < 1
        pk_diag.append(pk)
        e3_diag.append(e3)
        em4_diag.append(em4)
    assert sum(pk_diag) == 71
    assert sum(e3_diag) == 40
    assert sum(em4_diag) == 31

    choices = Counter()
    for i in range(85):
        for j in range(i + 1, 85):
            allowed = []
            for d in (0, 1):
                e3ij = (d - dp_u[i][j] - 4 * p_u[i][j]) / 7
                em4ij = (-d + dp_u[i][j] - 3 * p_u[i][j]) / 7
                if (
                    e3ij * e3ij <= e3_diag[i] * e3_diag[j]
                    and em4ij * em4ij <= em4_diag[i] * em4_diag[j]
                ):
                    allowed.append(d)
            choices[tuple(allowed)] += 1
    assert choices == {(0, 1): 3570}

    return {
        "orbit_index": control["orbit_index"],
        "mod_2_artin_schreier": {
            "rank_F_transpose_F_powers_1_through_5": powers,
            "nilpotency_index": 5,
            "jordan_type_of_F_transpose_F": jordan,
            "consequence_for_D": (
                "If D^2+D=F^T F over F2, D has exactly the same four "
                "nontrivial Jordan blocks J5,J5,J3,J3, allocated in an "
                "undetermined way between its 0-primary and 1-primary spaces."
            ),
        },
        "K_projector_local_multiplicities": {
            "trace_P_K": 71,
            "trace_E_3_on_K": 40,
            "trace_E_minus4_on_K": 31,
            "P_K_diagonal_distribution": distribution(pk_diag),
            "E_3_diagonal_distribution": distribution(e3_diag),
            "E_minus4_diagonal_distribution": distribution(em4_diag),
            "E_3_diagonal_min": fraction_text(min(e3_diag)),
            "E_3_diagonal_max": fraction_text(max(e3_diag)),
            "E_minus4_diagonal_min": fraction_text(min(em4_diag)),
            "E_minus4_diagonal_max": fraction_text(max(em4_diag)),
            "two_by_two_PSD_pair_choices": {
                "both_0_and_1_allowed": 3570,
                "forced_0": 0,
                "forced_1": 0,
                "neither_allowed": 0,
            },
        },
    }


def analyze():
    assert sha256(UPSTREAM) == UPSTREAM_SHA256
    payload = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    controls = sorted(payload["controls"], key=lambda row: row["orbit_index"])
    assert [row["orbit_index"] for row in controls] == [0, 4, 29]

    u_polynomial = forced_action_polynomial()
    u_mod2 = [value & 1 for value in u_polynomial]
    full_mod2 = u_mod2
    full_mod2 = [value & 1 for value in poly_mul(full_mod2, poly_pow_mod2([1, 1], 40))]
    full_mod2 = [value & 1 for value in poly_mul(full_mod2, poly_pow_mod2([1, 0], 31))]
    nonzero_degrees = [
        len(full_mod2) - 1 - index
        for index, value in enumerate(full_mod2)
        if value
    ]
    assert nonzero_degrees == [85, 77, 53, 45]
    square_root = [value & 1 for value in poly_mul(poly_pow_mod2([1, 0], 22), poly_pow_mod2([1, 1], 20))]
    alternating_form = [value & 1 for value in poly_mul([1, 0], poly_mul(square_root, square_root))]
    assert full_mod2 == alternating_form

    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "scope": (
            "exact mod-2 Artin-Schreier/Jordan and K-projector local-minor "
            "consequences for Wave 210 rank-three survivor orbits 0, 4, and 29"
        ),
        "input_sha256": {str(UPSTREAM.relative_to(ROOT)).replace("\\", "/"): UPSTREAM_SHA256},
        "conditional_characteristic_polynomial_mod_2": {
            "factorization": "x^45 (x+1)^40",
            "expanded_nonzero_degrees": nonzero_degrees,
            "alternating_odd_order_form": "x * (x^22 (x+1)^20)^2",
            "verdict": "compatible; no alternating-characteristic-polynomial obstruction",
        },
        "orbits": [analyze_orbit(control) for control in controls],
        "limitations": [
            "No 85-by-85 binary matrix D is constructed or excluded.",
            "The allocation of the four nontrivial mod-2 Jordan blocks between the 0- and 1-primary spaces is not forced.",
            "Strict projector diagonals and all 2-by-2 PSD minors close only local spectral-projector shortcuts; larger minors remain equivalent to unresolved quadratic content.",
            "No target automorphism is assumed.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = analyze()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULTS.write_text(rendered, encoding="utf-8")
    if args.verify:
        assert RESULTS.read_text(encoding="utf-8") == rendered
        verify_manifest()
    if not args.write and not args.verify:
        print(rendered, end="")


if __name__ == "__main__":
    main()
