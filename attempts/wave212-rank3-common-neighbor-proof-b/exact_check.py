#!/usr/bin/env python3
"""Exact Wave 212 common-neighbor and triangle-incidence audit.

The committed controls are deliberately restricted objects.  They contain a
complete coloured q=1 matching layer and a complete 152-block q=0 triangle
packing, but they are not claimed to be outside blocks of an SRG.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = ROOT / "attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json"
CONTROLS = HERE / "hostile-incidence-controls.json"
RESULTS = HERE / "exact-results.json"

INPUT_HASHES = {
    "AGENTS.md": "4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3",
    "attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json":
        "32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd",
    "attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256":
        "d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722",
    "verification/wave210-rank3-marked-outside-coupling-verifier/package-manifest.sha256":
        "d7f30a8c3e5d89c363f88da64d0a0baf2a2c933694e6bf12efdb94e6cd3132fb",
}

ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)
SUPPORT_EDGES = frozenset(
    {tuple(sorted(edge)) for edge in ROOTED_EDGES}
    | {(u + 7, v + 7) for u, v in ROOTED_EDGES}
    | {(0, 7)}
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def graph(n: int, edges: set[tuple[int, int]] | frozenset[tuple[int, int]]) -> list[set[int]]:
    rows = [set() for _ in range(n)]
    for u, v in edges:
        rows[u].add(v)
        rows[v].add(u)
    return rows


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def verify_inputs() -> dict[str, str]:
    observed = {name: sha256(ROOT / name) for name in INPUT_HASHES}
    assert observed == INPUT_HASHES
    return observed


def support_metrics(column: frozenset[int]) -> tuple[int, int, int, int]:
    t = len(column)
    a = sum({u, v} <= column for u, v in SUPPORT_EDGES)
    return t, a, t - 2 * a, 7 - t + a


def selected_data(control: dict[str, object]) -> tuple[set[int], set[tuple[int, int]]]:
    selected = set(map(int, control["selected_outside_column_indices"]))
    edges = {
        pair(int(u) - 14, int(v) - 14)
        for u, v in control["selected_union_edges"]
        if int(u) >= 14 and int(v) >= 14
    }
    assert len(selected) == 5
    return selected, edges


def cycle_census(columns: list[frozenset[int]]) -> dict[str, object]:
    support_adj = graph(14, SUPPORT_EDGES)
    q_hist = Counter(
        len(columns[u] & columns[v]) for u, v in combinations(range(85), 2)
    )
    assert q_hist == Counter({0: 2878, 1: 652, 2: 40})

    ss_hist = Counter()
    for u, v in combinations(range(14), 2):
        if v not in support_adj[u]:
            ss_hist[len(support_adj[u] & support_adj[v])] += 1
    assert ss_hist == Counter({0: 40, 1: 12, 2: 16})

    so_hist = Counter()
    for support in range(14):
        for column in columns:
            if support not in column:
                so_hist[len(support_adj[support] & column)] += 1
    assert so_hist == Counter({0: 588, 1: 440, 2: 12})

    metrics = [support_metrics(column) for column in columns]
    q1_degree_sum = sum(b for _, _, b, _ in metrics)
    outside_triangle_incidence = sum(c for _, _, _, c in metrics)
    assert q1_degree_sum == 128
    assert outside_triangle_incidence == 456

    # An outside completion has 520 edges.  The q=1 edges are the 64
    # one-support triangles; the remaining 456 edges form 152 outside triples.
    q1_edges = q1_degree_sum // 2
    q0_edges = 520 - q1_edges
    outside_triangles = outside_triangle_incidence // 3
    assert (q1_edges, q0_edges, outside_triangles) == (64, 456, 152)

    # Opposite-pair census.  q=0 outside nonedges are counted twice by an
    # all-outside C4; q=1 outside nonedges are counted once by a 1-support C4.
    cycles = {
        "support_0": (q_hist[0] - q0_edges) // 2,
        "support_1": q_hist[1] - q1_edges,
        "support_2_alternating_supports": ss_hist[0],
        "support_2_adjacent_supports": so_hist[1] // 2,
        "support_3": so_hist[2],
        "support_4": ss_hist[2] // 2,
    }
    assert cycles == {
        "support_0": 1211,
        "support_1": 588,
        "support_2_alternating_supports": 40,
        "support_2_adjacent_supports": 220,
        "support_3": 12,
        "support_4": 8,
    }
    assert sum(cycles.values()) == 2079
    return {
        "outside_pair_support_intersection_histogram": {
            str(key): value for key, value in sorted(q_hist.items())
        },
        "support_support_nonedge_internal_common_histogram": {
            str(key): value for key, value in sorted(ss_hist.items())
        },
        "support_outside_nonedge_internal_common_histogram": {
            str(key): value for key, value in sorted(so_hist.items())
        },
        "forced_outside_edge_split": {"q0": q0_edges, "q1": q1_edges},
        "forced_all_outside_triangles": outside_triangles,
        "forced_four_cycle_support_census": cycles,
        "forced_four_cycles_total": sum(cycles.values()),
    }


def check_control(
    upstream: dict[str, object], certificate: dict[str, object]
) -> dict[str, object]:
    orbit = int(upstream["orbit_index"])
    assert int(certificate["orbit_index"]) == orbit
    columns = [frozenset(map(int, row)) for row in upstream["F_columns_support_neighbors"]]
    assert len(columns) == 85
    support_adj = graph(14, SUPPORT_EDGES)
    metrics = [support_metrics(column) for column in columns]
    selected, selected_edges = selected_data(upstream)
    selected_pairs = set(combinations(sorted(selected), 2))

    coloured = [tuple(map(int, row)) for row in certificate["colored_edges"]]
    assert len(coloured) == 64 and len(set(coloured)) == 64
    e1: set[tuple[int, int]] = set()
    by_colour: dict[int, list[tuple[int, int]]] = {s: [] for s in range(14)}
    for colour, u, v in coloured:
        assert 0 <= colour < 14 and 0 <= u < v < 85
        assert columns[u] & columns[v] == {colour}
        assert pair(u, v) not in e1
        e1.add(pair(u, v))
        by_colour[colour].append(pair(u, v))

    # This proves simultaneous compatibility across the fourteen support
    # colours, rather than checking the colours one at a time.
    for colour, colour_edges in by_colour.items():
        outside = {i for i, column in enumerate(columns) if colour in column}
        unmatched = {
            i for i in outside if not (support_adj[colour] & columns[i])
        }
        endpoints = [vertex for edge in colour_edges for vertex in edge]
        assert len(endpoints) == len(set(endpoints))
        assert set(endpoints) == unmatched
    e1_degrees = Counter(vertex for edge in e1 for vertex in edge)
    assert [e1_degrees[i] for i in range(85)] == [b for _, _, b, _ in metrics]

    for edge in selected_pairs:
        q = len(columns[edge[0]] & columns[edge[1]])
        if q == 1:
            assert (edge in e1) == (edge in selected_edges)

    triples = [tuple(map(int, row)) for row in certificate["outside_triangles"]]
    assert len(triples) == 152 and len(set(triples)) == 152
    triangle_pairs: Counter[tuple[int, int]] = Counter()
    triangle_degrees: Counter[int] = Counter()
    for triple in triples:
        assert len(triple) == 3 and tuple(sorted(triple)) == triple
        assert len(set(triple)) == 3 and all(0 <= v < 85 for v in triple)
        for u, v in combinations(triple, 2):
            assert not (columns[u] & columns[v])
            triangle_pairs[pair(u, v)] += 1
        triangle_degrees.update(triple)
    assert set(triangle_pairs.values()) == {1}
    assert [triangle_degrees[i] for i in range(85)] == [c for _, _, _, c in metrics]

    for edge in selected_pairs:
        if not (columns[edge[0]] & columns[edge[1]]):
            assert (edge in triangle_pairs) == (edge in selected_edges)

    d_edges = e1 | set(triangle_pairs)
    assert len(d_edges) == 520 and not (e1 & set(triangle_pairs))
    d_adj = graph(85, d_edges)
    assert [len(row) for row in d_adj] == [14 - len(column) for column in columns]
    assert all((edge in d_edges) == (edge in selected_edges) for edge in selected_pairs)

    # Count exactly which top-right block equations the restricted control
    # happens to satisfy; these were not imposed by the triangle packing.
    fd_residual = Counter()
    for vertex, column in enumerate(columns):
        for support in range(14):
            lhs = sum(support in columns[neighbor] for neighbor in d_adj[vertex])
            rhs = 2 - int(support in column) - len(support_adj[support] & column)
            fd_residual[lhs - rhs] += 1
    assert sum(fd_residual.values()) == 14 * 85

    quadratic = Counter()
    target_zero_pairs = 0
    target_zero_violations = 0
    for u, v in combinations(range(85), 2):
        q = len(columns[u] & columns[v])
        adjacent = int(v in d_adj[u])
        common = len(d_adj[u] & d_adj[v])
        residual = common + adjacent - (2 - q)
        quadratic[residual] += 1
        if q == 2 or pair(u, v) in e1:
            target_zero_pairs += 1
            target_zero_violations += int(common != 0)
    assert target_zero_pairs == 104 and target_zero_violations == 0
    assert sum(value * count for value, count in quadratic.items()) == 0

    designated = set(triples)
    graph_triangles = {
        triple
        for triple in combinations(range(85), 3)
        if all(pair(u, v) in d_edges for u, v in combinations(triple, 2))
    }
    assert designated <= graph_triangles
    spurious = graph_triangles - designated

    metric_hist = Counter(metrics)
    return {
        "orbit_index": orbit,
        "column_metric_histogram_t_a_q1degree_outsideTriangles": {
            ",".join(map(str, key)): value for key, value in sorted(metric_hist.items())
        },
        "colored_q1_edges": len(e1),
        "all_14_colored_matchings_simultaneously_cover_forced_endpoints": True,
        "outside_triangle_blocks": len(triples),
        "q0_pairs_covered_once": len(triangle_pairs),
        "outside_edges": len(d_edges),
        "degree_equations_satisfied": sum(
            len(d_adj[i]) == 14 - len(columns[i]) for i in range(85)
        ),
        "selected_pair_values_satisfied": sum(
            (edge in d_edges) == (edge in selected_edges) for edge in selected_pairs
        ),
        "FD_residual_histogram": {
            str(key): value for key, value in sorted(fd_residual.items())
        },
        "FD_equations_satisfied": fd_residual[0],
        "FD_equations_total": 1190,
        "target_zero_pairs": target_zero_pairs,
        "target_zero_violations": target_zero_violations,
        "graph_outside_triangles": len(graph_triangles),
        "designated_outside_triangles": len(designated),
        "spurious_outside_triangles": len(spurious),
        "quadratic_residual_histogram": {
            str(key): value for key, value in sorted(quadratic.items())
        },
        "quadratic_pairs_satisfied": quadratic[0],
        "quadratic_pairs_total": 3570,
        "is_full_quadratic_solution": len(quadratic) == 1 and quadratic[0] == 3570,
    }


def build_results() -> dict[str, object]:
    inputs = verify_inputs()
    upstream_payload = json.loads(UPSTREAM.read_text(encoding="utf-8"))
    certificate_payload = json.loads(CONTROLS.read_text(encoding="utf-8"))
    upstream = {int(row["orbit_index"]): row for row in upstream_payload["controls"]}
    certificates = {int(row["orbit_index"]): row for row in certificate_payload["controls"]}
    assert set(upstream) == set(certificates) == {0, 4, 29}

    census = [cycle_census([
        frozenset(map(int, row)) for row in upstream[orbit]["F_columns_support_neighbors"]
    ]) for orbit in (0, 4, 29)]
    assert census[0] == census[1] == census[2]
    controls = [check_control(upstream[orbit], certificates[orbit]) for orbit in (0, 4, 29)]
    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "scope": "common-neighbor, triangle, four-cycle, and coloured-one-factor consequences for the three Wave 210 rank-three representatives",
        "inputs": inputs,
        "conditional_completion_census_common_to_all_three_orbits": census[0],
        "path_budget_identity": {
            "sum_choose_outside_degrees_2": 5888,
            "sum_pair_targets_2_minus_q_minus_D": 5888,
            "consequence": "for any degree-correct binary D, if every off-diagonal common-neighbor value is at most its target, then all 3570 values equal their targets",
        },
        "hostile_incidence_controls": controls,
        "limitations": [
            "the controls are labelled triangle-incidence relaxations, not 85-vertex SRG outside blocks",
            "the controls were required to satisfy all degrees, all ten selected pair values, coloured q=1 compatibility, and all 104 zero-target common-neighbor pairs, but not the 1190 FD entries or the remaining quadratic equalities",
            "their nonzero residuals are explicit failures, not evidence for an SRG construction",
            "no target automorphism is assumed and no unknown 85-vertex graph is enumerated",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payload = build_results()
    if args.verify:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        assert payload == expected
        print("verified", RESULTS.as_posix(), CONTROLS.as_posix())
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
