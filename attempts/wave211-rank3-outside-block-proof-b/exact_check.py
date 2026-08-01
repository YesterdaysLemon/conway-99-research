#!/usr/bin/env python3
"""Exact replay for the Wave 211 rank-three outside-block proof-B package.

The committed hostile control is a complete 85-vertex simple graph satisfying
the *linear* outside-block equations for one Wave 210 orbit representative.
It is not claimed to satisfy the quadratic SRG block equation.
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
CONTROL = HERE / "hostile-linear-control.json"
RESULTS = HERE / "exact-results.json"
MANIFEST = HERE / "package-manifest.sha256"
UPSTREAM_SHA256 = "32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd"
ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def verify_manifest() -> None:
    for raw_line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = raw_line.split("  ", 1)
        assert sha256(ROOT / relative) == expected


def support_adjacency() -> list[list[int]]:
    matrix = [[0] * 14 for _ in range(14)]
    for offset in (0, 7):
        for u, v in ROOTED_EDGES:
            matrix[u + offset][v + offset] = 1
            matrix[v + offset][u + offset] = 1
    matrix[0][7] = matrix[7][0] = 1
    return matrix


def matrix_rank_q(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank or not matrix[r][column]:
                continue
            scale = matrix[r][column]
            matrix[r] = [a - scale * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def matrix_rank_f2(rows: list[list[int]]) -> int:
    masks = [sum((value & 1) << column for column, value in enumerate(row)) for row in rows]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next((r for r in range(rank, len(masks)) if (masks[r] >> column) & 1), None)
        if pivot is None:
            continue
        masks[rank], masks[pivot] = masks[pivot], masks[rank]
        for r in range(len(masks)):
            if r != rank and ((masks[r] >> column) & 1):
                masks[r] ^= masks[rank]
        rank += 1
    return rank


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    right_t = list(zip(*right))
    return [[sum(a * b for a, b in zip(row, column)) for column in right_t] for row in left]


def characteristic_polynomial(matrix: list[list[int]]) -> list[int]:
    """Faddeev-LeVerrier coefficients, highest degree first."""
    n = len(matrix)
    identity = [[int(i == j) for j in range(n)] for i in range(n)]
    b = identity
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


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def forced_action_polynomial() -> list[int]:
    a_s = support_adjacency()
    operator = [[0] * 15 for _ in range(15)]
    for i in range(14):
        for j in range(14):
            operator[i][j] = -(a_s[i][j] + int(i == j))
        operator[i][14] = -1
        operator[14][i] = 2
    operator[14][14] = 14
    full = characteristic_polynomial(operator)
    # The redundant signed support vector is a -4 eigenvector.
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


def upstream_control(orbit: int) -> dict[str, object]:
    assert sha256(UPSTREAM) == UPSTREAM_SHA256
    payload = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    return next(row for row in payload["controls"] if row["orbit_index"] == orbit)


def incidence(control: dict[str, object]) -> list[list[int]]:
    f = [[0] * 85 for _ in range(14)]
    for column, neighbors in enumerate(control["F_columns_support_neighbors"]):
        for support in neighbors:
            f[support][column] = 1
    return f


def selected_pair_values(control: dict[str, object]) -> dict[tuple[int, int], int]:
    selected = [vertex - 14 for vertex in control["selected_outside_vertex_ids"]]
    union_edges = {tuple(sorted(edge)) for edge in control["selected_union_edges"]}
    return {
        (u, v): int((u + 14, v + 14) in union_edges)
        for index, u in enumerate(selected)
        for v in selected[index + 1:]
        for u, v in [tuple(sorted((u, v)))]
    }


def graph_from_control(payload: dict[str, object]) -> list[set[int]]:
    adjacency = [set() for _ in range(85)]
    edges = [tuple(edge) for edge in payload["D_edges"]]
    assert len(edges) == len(set(edges)) == 520
    for u, v in edges:
        assert 0 <= u < v < 85
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def analyze() -> dict[str, object]:
    source = upstream_control(29)
    payload = json.loads(CONTROL.read_text(encoding="utf-8"))
    assert payload["orbit_index"] == 29
    assert payload["source_sha256"] == UPSTREAM_SHA256
    f = incidence(source)
    a_s = support_adjacency()
    adjacency = graph_from_control(payload)

    degrees = [14 - sum(f[s][j] for s in range(14)) for j in range(85)]
    assert [len(row) for row in adjacency] == degrees
    for j in range(85):
        for s in range(14):
            observed = sum(i in adjacency[j] for i in range(85) if f[s][i])
            target = 2 - sum((a_s[s][t] + int(s == t)) * f[t][j] for t in range(14))
            assert observed == target
    for pair, value in selected_pair_values(source).items():
        assert int(pair[1] in adjacency[pair[0]]) == value

    # Exact degree-type consequence obtained by summing the 14 equations FD=M.
    degree_type_rows = []
    for j, row in enumerate(adjacency):
        counts = Counter(sum(f[s][i] for s in range(14)) for i in row)
        own_type = sum(f[s][j] for s in range(14))
        roots = f[0][j] + f[7][j]
        assert counts[0] - counts[4] == own_type + roots
        degree_type_rows.append((own_type, roots, counts[0], counts[2], counts[4]))

    residuals = Counter()
    satisfied = 0
    for i in range(85):
        # The diagonal quadratic equations reduce exactly to the degrees.
        assert len(adjacency[i]) == 14 - sum(f[s][i] for s in range(14))
        for j in range(i + 1, 85):
            observed = len(adjacency[i] & adjacency[j]) + int(j in adjacency[i])
            target = 2 - sum(f[s][i] * f[s][j] for s in range(14))
            residual = observed - target
            residuals[residual] += 1
            satisfied += residual == 0

    ranks = []
    for orbit in (0, 4, 29):
        f_orbit = incidence(upstream_control(orbit))
        ranks.append({
            "orbit_index": orbit,
            "rank_F_over_Q": matrix_rank_q(f_orbit),
            "rank_stacked_F_and_ones_over_Q": matrix_rank_q(f_orbit + [[1] * 85]),
            "rank_F_over_F2": matrix_rank_f2(f_orbit),
            "rank_stacked_F_and_ones_over_F2": matrix_rank_f2(f_orbit + [[1] * 85]),
        })
    assert all(row == {
        "orbit_index": row["orbit_index"],
        "rank_F_over_Q": 13,
        "rank_stacked_F_and_ones_over_Q": 14,
            "rank_F_over_F2": 13,
            "rank_stacked_F_and_ones_over_F2": 14,
    } for row in ranks)

    forced_polynomial = forced_action_polynomial()
    assert forced_polynomial == [
        1, -4, -84, -248, 152, 1552, 1152, -3040,
        -4080, 1792, 4160, 256, -1024, 0, 0,
    ]
    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "scope": "outside-block linear and forced spectral consequences for the three Wave 210 orbit representatives",
        "all_three_orbit_rank_data": ranks,
        "forced_rational_subspace": {
            "U_dimension_over_Q": 14,
            "K_dimension_over_Q": 71,
            "U_characteristic_polynomial_coefficients": forced_polynomial,
            "U_characteristic_polynomial_factorization": "x^2 (x+2)^2 (x^2-2)^3 (x^4-8x^3-50x^2-40x+32)",
            "U_trace": 4,
            "U_trace_square": 184,
            "conditional_K_spectrum_if_full_quadratic_block_holds": {"3": 40, "-4": 31},
            "conditional_full_D_characteristic_polynomial": "x^2 (x+2)^2 (x^2-2)^3 (x^4-8x^3-50x^2-40x+32) (x-3)^40 (x+4)^31",
            "mod_2_restriction": "on ker(F), D^2+D=0; rank(F)=13 and rank([F;1^T])=14 over F2",
        },
        "orbit_29_binary_linear_hostile_control": {
            "vertices": 85,
            "edges": 520,
            "degree_distribution": dict(sorted(Counter(degrees).items())),
            "linear_block_equations_checked": 14 * 85,
            "selected_pair_values_checked": 10,
            "degree_type_signature_distribution": {
                ",".join(map(str, key)): value
                for key, value in sorted(Counter(degree_type_rows).items())
            },
            "quadratic_off_diagonal_pairs_satisfied": satisfied,
            "quadratic_off_diagonal_pairs_total": 3570,
            "quadratic_residual_distribution": dict(sorted(residuals.items())),
            "is_full_quadratic_solution": satisfied == 3570,
        },
        "inconclusive_searches": [
            {
                "orbit_index": 0,
                "method": "binary MILP for the linear block, degrees, and ten selected pair values",
                "limit_seconds": 45,
                "result": "time limit with no primal; no evidence",
            },
            {
                "orbit_index": 4,
                "method": "binary MILP for the linear block, degrees, and ten selected pair values",
                "limit_seconds": 45,
                "result": "time limit with no primal; no evidence",
            },
        ],
        "limitations": [
            "the orbit-29 control violates the quadratic common-neighbor block and is not an SRG",
            "no rational or binary linear control was certified for orbit 0 or orbit 4",
            "no target automorphism is assumed",
        ],
    }


def generate() -> None:
    """Generate one binary linear-block witness with SciPy/HiGHS, then seal it."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    source = upstream_control(29)
    f = incidence(source)
    a_s = support_adjacency()
    pairs = [(i, j) for i in range(85) for j in range(i + 1, 85)]
    edge_id = {edge: index for index, edge in enumerate(pairs)}
    rows: list[int] = []
    columns: list[int] = []
    values: list[int] = []
    rhs: list[int] = []
    row = 0
    for s in range(14):
        for j in range(85):
            for i in range(85):
                if i != j and f[s][i]:
                    rows.append(row)
                    columns.append(edge_id[tuple(sorted((i, j)))])
                    values.append(1)
            rhs.append(2 - sum((a_s[s][t] + int(s == t)) * f[t][j] for t in range(14)))
            row += 1
    for j in range(85):
        for i in range(85):
            if i != j:
                rows.append(row)
                columns.append(edge_id[tuple(sorted((i, j)))])
                values.append(1)
        rhs.append(14 - sum(f[s][j] for s in range(14)))
        row += 1
    for pair, target in selected_pair_values(source).items():
        rows.append(row)
        columns.append(edge_id[pair])
        values.append(1)
        rhs.append(target)
        row += 1
    matrix = coo_matrix((values, (rows, columns)), shape=(row, len(pairs))).tocsr()
    rhs_array = np.array(rhs)
    result = milp(
        np.zeros(len(pairs)),
        integrality=np.ones(len(pairs)),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(matrix, rhs_array, rhs_array),
        options={"time_limit": 60, "mip_rel_gap": 0},
    )
    assert result.x is not None, result.message
    solution = np.rint(result.x).astype(int)
    assert np.array_equal(matrix @ solution, rhs_array)
    payload = {
        "claim_label": "CANDIDATE",
        "scope": "orbit-29 binary solution of the linear outside-block equations only",
        "orbit_index": 29,
        "source": "attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json",
        "source_sha256": UPSTREAM_SHA256,
        "D_edges": [list(pair) for pair, flag in zip(pairs, solution) if flag],
        "limitations": [
            "this graph fails the quadratic outside-block equation",
            "it is a hostile control for linear obstruction claims, not an SRG completion",
        ],
    }
    CONTROL.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULTS.write_text(json.dumps(analyze(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.generate:
        generate()
    observed = analyze()
    if args.verify:
        assert json.loads(json.dumps(observed)) == json.loads(RESULTS.read_text(encoding="utf-8"))
        verify_manifest()
    print(json.dumps(observed, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
