#!/usr/bin/env python3
"""Independent Wave 212 rank-three replay; no unknown-graph search."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json"
COMMON = ROOT / "attempts/wave212-rank3-common-neighbor-proof-b"
ALGEBRA = ROOT / "attempts/wave212-rank3-quadratic-algebra-proof-a"
UPSTREAM_SHA256 = "32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd"
ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(directory: Path) -> dict[str, object]:
    manifest = directory / "package-manifest.sha256"
    listed = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        assert sha256(path) == expected
        listed.add(path.resolve())
    actual = {p.resolve() for p in directory.iterdir() if p.is_file() and p != manifest}
    assert listed == actual
    return {"entries": len(listed), "sha256": sha256(manifest), "exact_file_coverage": True}


def support_adjacency() -> list[list[int]]:
    a = [[0] * 14 for _ in range(14)]
    for offset in (0, 7):
        for u, v in ROOTED_EDGES:
            a[u + offset][v + offset] = a[v + offset][u + offset] = 1
    a[0][7] = a[7][0] = 1
    return a


def incidence(control: dict[str, object]) -> list[list[int]]:
    f = [[0] * 85 for _ in range(14)]
    for j, column in enumerate(control["F_columns_support_neighbors"]):
        for s in column:
            f[s][j] = 1
    return f


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def matmul_f2(a, b):
    b_masks = [sum((x & 1) << j for j, x in enumerate(row)) for row in b]
    out = []
    for row in a:
        mask = 0
        for i, x in enumerate(row):
            if x & 1:
                mask ^= b_masks[i]
        out.append([(mask >> j) & 1 for j in range(len(b[0]))])
    return out


def rank_f2(a):
    masks = [sum((x & 1) << j for j, x in enumerate(row)) for row in a]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(rank, len(masks)) if masks[r] >> col & 1), None)
        if pivot is None:
            continue
        masks[rank], masks[pivot] = masks[pivot], masks[rank]
        for r in range(len(masks)):
            if r != rank and masks[r] >> col & 1:
                masks[r] ^= masks[rank]
        rank += 1
    return rank


def rank_q(a):
    m = [[Fraction(x) for x in row] for row in a]
    rank = 0
    for col in range(len(m[0])):
        pivot = next((r for r in range(rank, len(m)) if m[r][col]), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        z = m[rank][col]
        m[rank] = [x / z for x in m[rank]]
        for r in range(len(m)):
            if r != rank and m[r][col]:
                z = m[r][col]
                m[r] = [x - z * y for x, y in zip(m[r], m[rank])]
        rank += 1
    return rank


def inverse(a):
    n = len(a)
    m = [[Fraction(x) for x in a[i]] + [Fraction(i == j) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if m[r][col])
        m[col], m[pivot] = m[pivot], m[col]
        z = m[col][col]
        m[col] = [x / z for x in m[col]]
        for r in range(n):
            if r != col and m[r][col]:
                z = m[r][col]
                m[r] = [x - z * y for x, y in zip(m[r], m[col])]
    return [row[n:] for row in m]


def independent_indices(rows):
    chosen, basis, rank = [], [], 0
    for i, row in enumerate(rows):
        trial = basis + [row]
        new_rank = rank_q(trial)
        if new_rank > rank:
            chosen.append(i)
            basis.append(row)
            rank = new_rank
    return chosen


def solve_f2_basis(basis: list[int], target: int) -> int:
    pivots: list[tuple[int, int, int]] = []
    for index, vector in enumerate(basis):
        x, coefficients = vector, 1 << index
        for pivot, row, combo in pivots:
            if x >> pivot & 1:
                x ^= row
                coefficients ^= combo
        assert x
        pivot = (x & -x).bit_length() - 1
        pivots.append((pivot, x, coefficients))
        pivots.sort()
    x, coefficients = target, 0
    for pivot, row, combo in pivots:
        if x >> pivot & 1:
            x ^= row
            coefficients ^= combo
    assert x == 0
    return coefficients


def fraction_text(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def distribution(values) -> list[dict[str, object]]:
    counts = Counter(values)
    return [{"value": fraction_text(x), "multiplicity": counts[x]} for x in sorted(counts)]


def selected_edges(control):
    selected = sorted(control["selected_outside_column_indices"])
    union = {tuple(sorted(edge)) for edge in control["selected_union_edges"]}
    return selected, {
        (u, v): int((u + 14, v + 14) in union)
        for u, v in combinations(selected, 2)
    }


def conditional_census(upstream):
    columns = [set(row) for row in upstream["F_columns_support_neighbors"]]
    a_s = support_adjacency()
    overlap = Counter(len(columns[i] & columns[j]) for i, j in combinations(range(85), 2))
    assert overlap == {0: 2878, 1: 652, 2: 40}
    metrics = []
    for column in columns:
        t = len(column)
        internal_edges = sum(a_s[u][v] for u, v in combinations(column, 2))
        metrics.append((t, internal_edges, t - 2 * internal_edges, 7 - t + internal_edges))
    q1_edges = sum(row[2] for row in metrics) // 2
    q0_edges = sum(2 * row[3] for row in metrics) // 2
    triangles = sum(row[3] for row in metrics) // 3
    assert (q0_edges, q1_edges, triangles) == (456, 64, 152)
    target_histogram = {
        0: overlap[2] + q1_edges,
        1: overlap[1] - q1_edges + q0_edges,
        2: overlap[0] - q0_edges,
    }
    assert target_histogram == {0: 104, 1: 1044, 2: 2422}
    support_support = Counter()
    for s, t in combinations(range(14), 2):
        if not a_s[s][t]:
            support_support[sum(a_s[s][u] * a_s[u][t] for u in range(14))] += 1
    support_outside = Counter()
    for s in range(14):
        for j, column in enumerate(columns):
            if s not in column:
                support_outside[sum(a_s[s][u] * int(u in column) for u in range(14))] += 1
    assert support_support == {0: 40, 1: 12, 2: 16}
    assert support_outside == {0: 588, 1: 440, 2: 12}
    cycles = {
        "support_0": target_histogram[2] // 2,
        "support_1": overlap[1] - q1_edges,
        "support_2_alternating": overlap[2],
        "support_2_adjacent": support_outside[1] // 2,
        "support_3": support_outside[2],
        "support_4": support_support[2] // 2,
    }
    assert cycles == {
        "support_0": 1211,
        "support_1": 588,
        "support_2_alternating": 40,
        "support_2_adjacent": 220,
        "support_3": 12,
        "support_4": 8,
    }
    assert sum(cycles.values()) == 2079
    return {
        "outside_edges": q0_edges + q1_edges,
        "edge_overlap_split": {"q0": q0_edges, "q1": q1_edges, "q2": 0},
        "outside_pair_overlap_histogram": {str(k): v for k, v in sorted(overlap.items())},
        "common_neighbor_target_histogram": {str(k): v for k, v in sorted(target_histogram.items())},
        "outside_triangles": triangles,
        "outside_four_cycles": cycles["support_0"],
        "four_cycle_support_census": cycles,
        "all_four_cycles": sum(cycles.values()),
    }


def analyze_common_control(upstream, certificate):
    columns = [set(row) for row in upstream["F_columns_support_neighbors"]]
    a_s = support_adjacency()
    metrics = []
    for column in columns:
        t = len(column)
        a = sum(a_s[u][v] for u, v in combinations(column, 2))
        metrics.append((t, a, t - 2 * a, 7 - t + a))
    colored_records = [tuple(map(int, row)) for row in certificate["colored_edges"]]
    assert len(colored_records) == len(set(colored_records)) == 64
    colored = set()
    for color, u, v in colored_records:
        assert u < v and columns[u] & columns[v] == {color}
        colored.add((u, v))
    assert len(colored) == 64
    assert Counter(x for edge in colored for x in edge) == Counter({i: metrics[i][2] for i in range(85) if metrics[i][2]})
    triples = [tuple(map(int, row)) for row in certificate["outside_triangles"]]
    assert len(triples) == len(set(triples)) == 152
    triangle_pairs = Counter()
    triangle_degree = Counter()
    for triple in triples:
        assert len(set(triple)) == 3
        triangle_degree.update(triple)
        for edge in combinations(sorted(triple), 2):
            assert not (columns[edge[0]] & columns[edge[1]])
            triangle_pairs[edge] += 1
    assert set(triangle_pairs.values()) == {1}
    assert Counter({i: triangle_degree[i] for i in range(85) if triangle_degree[i]}) == Counter({i: metrics[i][3] for i in range(85) if metrics[i][3]})
    edges = colored | set(triangle_pairs)
    assert len(edges) == 520 and not (colored & set(triangle_pairs))
    adjacency = [set() for _ in range(85)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    f = incidence(upstream)
    degrees = [14 - sum(f[s][j] for s in range(14)) for j in range(85)]
    assert [len(row) for row in adjacency] == degrees
    selected, selected_values = selected_edges(upstream)
    assert all(int(v in adjacency[u]) == value for (u, v), value in selected_values.items())
    fd_residual, quadratic = Counter(), Counter()
    target_zero = violations = 0
    for s in range(14):
        for j in range(85):
            observed = sum(f[s][i] for i in adjacency[j])
            target = 2 - sum((a_s[s][t] + int(s == t)) * f[t][j] for t in range(14))
            fd_residual[observed - target] += 1
    for i, j in combinations(range(85), 2):
        q = len(columns[i] & columns[j])
        observed_cn = len(adjacency[i] & adjacency[j])
        target_cn = 2 - q - int(j in adjacency[i])
        quadratic[observed_cn - target_cn] += 1
        if target_cn == 0:
            target_zero += 1
            violations += int(observed_cn != 0)
    graph_triangles = {
        (i, j, k) for i in range(85) for j in adjacency[i] if i < j
        for k in adjacency[i] & adjacency[j] if j < k
    }
    assert target_zero == 104 and violations == 0
    return {
        "orbit_index": upstream["orbit_index"],
        "FD_satisfied": fd_residual[0],
        "FD_residual_histogram": {str(k): v for k, v in sorted(fd_residual.items())},
        "quadratic_satisfied": quadratic[0],
        "quadratic_residual_histogram": {str(k): v for k, v in sorted(quadratic.items())},
        "target_zero_pairs": target_zero,
        "target_zero_violations": violations,
        "graph_triangles": len(graph_triangles),
        "spurious_triangles": len(graph_triangles) - 152,
    }


def analyze_algebra(upstream):
    f = incidence(upstream)
    all_rows = f + [[1] * 85]
    assert (rank_q(f), rank_q(all_rows), rank_f2(f), rank_f2(all_rows)) == (13, 14, 13, 14)
    q = [[x & 1 for x in row] for row in matmul(transpose(f), f)]
    q_ranks, power = [], q
    for _ in range(5):
        q_ranks.append(rank_f2(power))
        power = matmul_f2(power, q)
    assert q_ranks == [12, 8, 4, 2, 0]

    a_s = support_adjacency()
    fd = [[2 - sum((a_s[s][t] + int(s == t)) * f[t][j] for t in range(14)) for j in range(85)] for s in range(14)]
    degree = [14 - sum(f[s][j] for s in range(14)) for j in range(85)]
    indices = independent_indices(all_rows)
    assert len(indices) == 14
    b = [all_rows[i] for i in indices]
    bd = [row for row in fd] + [degree]
    bd = [bd[i] for i in indices]
    gram_inverse = inverse(matmul(b, transpose(b)))
    p_u = matmul(matmul(transpose(b), gram_inverse), b)
    l = matmul(matmul(transpose(b), gram_inverse), bd)
    assert p_u == transpose(p_u) and matmul(p_u, p_u) == p_u and l == transpose(l)
    p_k = [[Fraction(i == j) - p_u[i][j] for j in range(85)] for i in range(85)]
    assert sum(p_k[i][i] for i in range(85)) == 71
    assert all(not x for row in matmul(f, p_k) for x in row)
    assert all(not x for x in matmul([[1] * 85], p_k)[0])
    assert sum(l[i][i] for i in range(85)) == 4
    e3_diag = [(-l[i][i] + 4 * p_k[i][i]) / 7 for i in range(85)]
    em4_diag = [(l[i][i] + 3 * p_k[i][i]) / 7 for i in range(85)]
    assert sum(e3_diag) == 40 and sum(em4_diag) == 31
    choices = Counter()
    for i, j in combinations(range(85), 2):
        allowed = []
        for d in (0, 1):
            e3 = (d - l[i][j] - 4 * p_u[i][j]) / 7
            em4 = (-d + l[i][j] - 3 * p_u[i][j]) / 7
            if e3 * e3 <= e3_diag[i] * e3_diag[j] and em4 * em4 <= em4_diag[i] * em4_diag[j]:
                allowed.append(d)
        choices[tuple(allowed)] += 1
    assert choices == {(0, 1): 3570}

    # Reconstruct the forced mod-2 action on U from FD and D1.
    basis_masks = [sum((x & 1) << j for j, x in enumerate(row)) for row in b]
    image_masks = [sum((x & 1) << j for j, x in enumerate(row)) for row in bd]
    coordinate_rows = []
    for image in image_masks:
        combo = solve_f2_basis(basis_masks, image)
        coordinate_rows.append([(combo >> j) & 1 for j in range(14)])
    u_ranks, power = [], coordinate_rows
    for _ in range(4):
        u_ranks.append(rank_f2(power))
        power = matmul_f2(power, coordinate_rows)
    assert u_ranks == [8, 4, 2, 0]

    return {
        "orbit_index": upstream["orbit_index"],
        "q_power_ranks": q_ranks,
        "q_jordan": {"1": 69, "3": 2, "5": 2},
        "u_action_power_ranks": u_ranks,
        "verifier_derived_allocation_pending_independent_promotion": {
            "claim_label": "DERIVED",
            "promotion_status": "PENDING_INDEPENDENT_VERIFICATION",
            "conditional_D_jordan": {
                "eigenvalue_0": {"1": 29, "3": 2, "5": 2},
                "eigenvalue_1": {"1": 40},
            },
            "conditional_D_power_ranks": [52, 48, 44, 42, 40],
        },
        "P_K_diagonal_distribution": distribution([p_k[i][i] for i in range(85)]),
        "E_3_diagonal_distribution": distribution(e3_diag),
        "E_minus4_diagonal_distribution": distribution(em4_diag),
        "projector_traces": {"P_K": 71, "E_3": 40, "E_minus4": 31, "L": 4},
        "two_by_two_choices": {"both_0_and_1_allowed": 3570, "forced_0": 0, "forced_1": 0, "neither_allowed": 0},
    }


def analyze():
    assert sha256(UPSTREAM) == UPSTREAM_SHA256
    upstream_payload = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    upstream = {row["orbit_index"]: row for row in upstream_payload["controls"]}
    assert sorted(upstream) == [0, 4, 29]
    common_submitted = json.loads((COMMON / "exact-results.json").read_text(encoding="utf-8"))
    algebra_submitted = json.loads((ALGEBRA / "exact-results.json").read_text(encoding="utf-8"))
    certificates = {
        row["orbit_index"]: row
        for row in json.loads((COMMON / "hostile-incidence-controls.json").read_text(encoding="utf-8"))["controls"]
    }
    censuses = [conditional_census(upstream[i]) for i in (0, 4, 29)]
    assert censuses[0] == censuses[1] == censuses[2]
    common_rows = [analyze_common_control(upstream[i], certificates[i]) for i in (0, 4, 29)]
    algebra_rows = [analyze_algebra(upstream[i]) for i in (0, 4, 29)]

    expected_common = {row["orbit_index"]: row for row in common_submitted["hostile_incidence_controls"]}
    for row in common_rows:
        submitted = expected_common[row["orbit_index"]]
        assert row["FD_satisfied"] == submitted["FD_equations_satisfied"]
        assert row["FD_residual_histogram"] == submitted["FD_residual_histogram"]
        assert row["quadratic_satisfied"] == submitted["quadratic_pairs_satisfied"]
        assert row["quadratic_residual_histogram"] == submitted["quadratic_residual_histogram"]
        assert row["spurious_triangles"] == submitted["spurious_outside_triangles"]
    expected_algebra = {row["orbit_index"]: row for row in algebra_submitted["orbits"]}
    for row in algebra_rows:
        submitted = expected_algebra[row["orbit_index"]]
        assert row["q_power_ranks"] == submitted["mod_2_artin_schreier"]["rank_F_transpose_F_powers_1_through_5"]
        projectors = submitted["K_projector_local_multiplicities"]
        assert row["P_K_diagonal_distribution"] == projectors["P_K_diagonal_distribution"]
        assert row["E_3_diagonal_distribution"] == projectors["E_3_diagonal_distribution"]
        assert row["E_minus4_diagonal_distribution"] == projectors["E_minus4_diagonal_distribution"]
        assert row["two_by_two_choices"] == projectors["two_by_two_PSD_pair_choices"]

    # Hostile controls are mutated only in memory; both lanes must reject.
    bad_common = copy.deepcopy(certificates[0])
    bad_common["colored_edges"].pop()
    common_mutation_rejected = False
    try:
        analyze_common_control(upstream[0], bad_common)
    except AssertionError:
        common_mutation_rejected = True
    assert common_mutation_rejected
    bad_algebra = copy.deepcopy(upstream[0])
    bad_algebra["F_columns_support_neighbors"][0].pop()
    algebra_mutation_rejected = False
    try:
        analyze_algebra(bad_algebra)
    except AssertionError:
        algebra_mutation_rejected = True
    assert algebra_mutation_rejected

    return {
        "claim_label": "VERIFIED",
        "global_status": "UNKNOWN",
        "manifests": {
            "common_neighbor": verify_manifest(COMMON),
            "quadratic_algebra": verify_manifest(ALGEBRA),
        },
        "common_neighbor": {
            "verdict": "PASS / NO VETO",
            "conditional_census": censuses[0],
            "controls": common_rows,
            "hostile_mutation_rejected": common_mutation_rejected,
        },
        "quadratic_algebra": {
            "core_verdict": "PASS / NO VETO",
            "allocation_statement_verdict": "VETO / REFUTED",
            "reason": (
                "The submitted Q power ranks and projector calculations replay, but the claim that the four nontrivial D blocks may be allocated between roots 0 and 1 omits the forced nilpotent D action on U. Since im(F^T F) is contained in U, every nontrivial Artin-Schreier chain has root 0."
            ),
            "replacement_status": "VERIFIER-DERIVED / PENDING INDEPENDENT PROMOTION",
            "orbits": algebra_rows,
            "hostile_mutation_rejected": algebra_mutation_rejected,
        },
        "limitations": [
            "The common-neighbor controls satisfy all degrees, selected pairs, and 104 zero-target rows, but only partial FD and many quadratic rows; none is a completion.",
            "No 85-by-85 outside block is constructed or excluded.",
            "No target-graph automorphism or unknown-graph search is used.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = analyze()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "exact-results.json").write_text(rendered, encoding="utf-8")
    if args.verify:
        assert (HERE / "exact-results.json").read_text(encoding="utf-8") == rendered
    if not args.write and not args.verify:
        print(rendered, end="")


if __name__ == "__main__":
    main()
