#!/usr/bin/env python3
"""Clean-room verifier for the sealed Wave 208 integer-lift proof-A package.

The source checker is never imported.  Its archived 22-vertex partial model
is treated only as a candidate certificate and replayed from raw data.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_RESULT = ROOT / "attempts" / "wave208-integer-lift-proof-a" / "exact-results.json"
ARCHIVE = HERE / "proof-a-independent-results.json"
ALLOWED_WEIGHTS = (17, 20, 23)


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def apply_a(coefficients: tuple[int, int, int]) -> tuple[int, int, int]:
    """Apply A to a*x+b*z+c*t*1 in the frozen symbolic basis."""
    a, b, c = coefficients
    return (4 * b, 3 * a - b, 2 * b + 14 * c)


def spectral_identities() -> dict[str, object]:
    q = (-9, 9, -1)
    r = (44, 33, -6)
    if apply_a(q) != tuple(-4 * value for value in q):
        raise AssertionError("Q is not a symbolic -4 eigenvector")
    if apply_a(r) != tuple(3 * value for value in r):
        raise AssertionError("R is not a symbolic 3 eigenvector")

    # z^2=(4w-h+6t^2)/3.  Expanding each norm gives these
    # coefficient triples in (w,h,t^2).
    q_norm = (189, -189, 63)
    r_norm = (3388, 2541, -1386)
    if q_norm != (63 * 3, -63 * 3, 63):
        raise AssertionError("Q norm coefficients differ")
    if r_norm != (77 * 44, 77 * 33, -77 * 18):
        raise AssertionError("R norm coefficients differ")
    return {
        "Q": "9*(z-x)-t*1",
        "AQ": "-4*Q",
        "sum_Q": 0,
        "Q_squared": "63*(3*(w-h)+t^2)",
        "Q_coordinate_residue_mod9": "-t",
        "R": "11*(4*x+3*z)-6*t*1",
        "AR": "3*R",
        "sum_R": 0,
        "R_squared": "77*(11*(4*w+3*h)-18*t^2)",
        "z_squared": "(4*w-h+6*t^2)/3",
    }


def residue_shell_table() -> dict[str, list[dict[str, object]]]:
    output: dict[str, list[dict[str, object]]] = {}
    for weight in ALLOWED_WEIGHTS:
        compositions = []
        for t in range(9):
            if 3 * t > weight or (weight + 3 * t) % 2:
                continue
            positive = (weight + 3 * t) // 2
            negative = weight - positive
            lower = Fraction(-44 * weight + 18 * t * t, 33)
            upper = Fraction(3 * weight + t * t, 3)
            minimum = 99 * t * (9 - t)
            rows = []
            for h_value in range(-100, 101):
                if h_value % 2 or h_value % 3 != weight % 3:
                    continue
                if not lower <= h_value <= upper:
                    continue
                q_squared = 63 * (3 * (weight - h_value) + t * t)
                excess = q_squared - minimum
                if excess < 0 or excess % 162:
                    continue
                rows.append(
                    {
                        "h": h_value,
                        "Q_squared": q_squared,
                        "residue_shell_index_L": excess // 162,
                    }
                )
            if not rows:
                raise AssertionError("composition lost every arithmetic row")
            compositions.append(
                {
                    "composition_up_to_sign": [positive, negative],
                    "t": t,
                    "spectral_h_interval": [str(lower), str(upper)],
                    "minimum_residue_norm": minimum,
                    "necessary_rows_only": rows,
                }
            )
        output[str(weight)] = compositions
    return output


def residue_shell_summary() -> dict[str, object]:
    table = residue_shell_table()
    return {
        "identity": "Q^2=99*t*(9-t)+162*L",
        "canonical_table_sha256": canonical_hash(table),
        "compositions_per_weight": {key: len(rows) for key, rows in table.items()},
        "rows_per_composition": {
            key: [len(row["necessary_rows_only"]) for row in rows]
            for key, rows in table.items()
        },
        "all_compositions_retained": True,
        "rows_are_graphs": False,
    }


def balanced_shells() -> list[dict[str, int]]:
    rows = []
    for h_value in range(-100, 101):
        if h_value % 2 or h_value % 3 != 14 % 3:
            continue
        if not Fraction(-56, 3) <= h_value <= 14:
            continue
        q_squared = Fraction(7 * (14 - h_value), 3)
        if q_squared.denominator == 1:
            rows.append({"h": h_value, "q_squared": int(q_squared)})
    expected = [70, 56, 42, 28, 14, 0]
    if [row["q_squared"] for row in rows] != expected:
        raise AssertionError("balanced shell list differs")
    return rows


def zero_q_branch() -> dict[str, object]:
    edge_cap = int(Fraction(3 * 14, 2) + Fraction(11 * 14 * 14, 2 * 99))
    rows = []
    for same_edges in (11, 12, 13):
        cross_edges = 2 * same_edges - 21
        quotient, remainder = divmod(cross_edges, 7)
        degrees = sorted([3 + quotient] * (7 - remainder) + [4 + quotient] * remainder)
        wedge_minimum = sum(value * (value - 1) // 2 for value in degrees)
        capacity = 42 - same_edges
        if same_edges == 13:
            if wedge_minimum <= capacity:
                raise AssertionError("e=13 wedge contradiction fails")
            status = "EXCLUDED_BY_WEDGE_CAPACITY"
        elif same_edges == 12:
            if wedge_minimum != capacity or sum(value % 2 for value in degrees) != 4:
                raise AssertionError("e=12 equality/parity contradiction fails")
            status = "EXCLUDED_BY_EQUALITY_TRIANGLE_PARITY"
        else:
            if degrees != [3, 3, 3, 3, 3, 3, 4] or cross_edges != 1:
                raise AssertionError("e=11 survivor differs")
            status = "SURVIVES_THIS_ARGUMENT"
        rows.append(
            {
                "same_sign_edges_each_side": same_edges,
                "cross_edges": cross_edges,
                "total_support_edges": 4 * same_edges - 21,
                "minimum_same_side_wedges": wedge_minimum,
                "same_side_common_neighbor_capacity": capacity,
                "minimizing_degree_sequence": degrees,
                "status": status,
            }
        )
    return {
        "restricted_edge_cap_on_support": edge_cap,
        "rows": rows,
        "surviving_cross_edges": 1,
        "surviving_degree_sequence_each_side": [4, 3, 3, 3, 3, 3, 3],
    }


def complementary_fano_blocks() -> tuple[frozenset[int], ...]:
    points = frozenset(range(1, 8))
    lines = {
        frozenset((left, right, left ^ right))
        for left, right in itertools.combinations(points, 2)
    }
    blocks = tuple(sorted((points - line for line in lines), key=lambda row: tuple(sorted(row))))
    if len(blocks) != 7:
        raise AssertionError("Fano complement does not have seven blocks")
    return blocks


FANO_BLOCKS = complementary_fano_blocks()


def fano_import_check() -> dict[str, object]:
    point_degrees = Counter(point for block in FANO_BLOCKS for point in block)
    pair_degrees = Counter(
        pair for block in FANO_BLOCKS for pair in itertools.combinations(sorted(block), 2)
    )
    if set(point_degrees.values()) != {4} or set(pair_degrees.values()) != {2}:
        raise AssertionError("complementary-Fano incidence parameters differ")
    support_edge_cap = int(Fraction(3 * 14, 2) + Fraction(11 * 14 * 14, 2 * 99))
    if 28 + 4 > support_edge_cap:
        same_sign_edges = 0
    else:
        raise AssertionError("norm-14 same-sign independence was not forced")
    cross_degree = 4
    outside_incidence_each_sign = 7 * (14 - cross_degree)
    if outside_incidence_each_sign != 70:
        raise AssertionError("outside incidence count differs")
    return {
        "unit_sign_class_sizes": [7, 7],
        "support_edge_cap": support_edge_cap,
        "same_sign_edges": same_sign_edges,
        "cross_degree": cross_degree,
        "design": "2-(7,4,2)",
        "outside_vertices_meeting_one_of_each_sign": 70,
        "outside_vertices_meeting_neither_sign": 15,
        "outside_vertex_meets_at_most_one_per_sign": True,
        "import_scope": "verified norm-14 integral -4 eigenvector theorem",
    }


def assignments(same: int, opposite: int) -> list[tuple[frozenset[int], frozenset[int], frozenset[int]]]:
    points = frozenset(range(1, 8))
    rows = []
    for same_tuple in itertools.combinations(sorted(points), same):
        same_set = frozenset(same_tuple)
        remainder = points - same_set
        for opposite_tuple in itertools.combinations(sorted(remainder), opposite):
            opposite_set = frozenset(opposite_tuple)
            rows.append((same_set, opposite_set, remainder - opposite_set))
    return rows


def overlap_census() -> dict[str, object]:
    cache: dict[tuple[int, int], list[tuple[frozenset[int], frozenset[int], frozenset[int]]]] = {}

    def rows(same: int, opposite: int):
        cache.setdefault((same, opposite), assignments(same, opposite))
        return cache[(same, opposite)]

    summary: dict[str, dict[str, int]] = {}
    alpha_one_patterns: Counter[tuple[object, ...]] = Counter()
    coupling_checks = []
    for alpha in range(5):
        total = 0
        feasible = 0
        for same_minus in range(alpha + 1):
            same_plus = alpha - same_minus
            opposite_total = alpha + 6
            for opposite_plus in range(8):
                opposite_minus = opposite_total - opposite_plus
                qonly_minus = 7 - same_minus - opposite_plus
                qonly_plus = 7 - same_plus - opposite_minus
                xonly_plus = 7 - same_plus - opposite_plus
                xonly_minus = 7 - same_minus - opposite_minus
                if min(opposite_minus, qonly_minus, qonly_plus, xonly_plus, xonly_minus) < 0:
                    continue
                left_rows = rows(same_minus, opposite_plus)
                right_rows = rows(same_plus, opposite_minus)
                for s_left, o_left, q_left in left_rows:
                    for s_right_idx, o_right_idx, q_right_idx in right_rows:
                        # Right-side labels index the seven complement blocks.
                        s_right = {FANO_BLOCKS[index - 1] for index in s_right_idx}
                        o_right = {index - 1 for index in o_right_idx}
                        q_right = {FANO_BLOCKS[index - 1] for index in q_right_idx}
                        left_deficits = [
                            4
                            - 2 * sum(point in block for block in s_right)
                            - sum(point in block for block in q_right)
                            for point in sorted(o_left)
                        ]
                        right_deficits = [
                            4
                            - 2 * len(s_left & FANO_BLOCKS[index])
                            - len(q_left & FANO_BLOCKS[index])
                            for index in sorted(o_right)
                        ]
                        capacity_ok = (
                            sum(max(value, 0) for value in left_deficits) <= xonly_plus
                            and sum(max(-value, 0) for value in left_deficits) <= xonly_minus
                            and sum(max(value, 0) for value in right_deficits) <= xonly_minus
                            and sum(max(-value, 0) for value in right_deficits) <= xonly_plus
                        )
                        total += 1
                        if not capacity_ok:
                            continue
                        feasible += 1
                        if alpha == 1:
                            counts = (
                                same_minus,
                                same_plus,
                                opposite_plus,
                                opposite_minus,
                                qonly_minus,
                                qonly_plus,
                                xonly_plus,
                                xonly_minus,
                            )
                            key = (counts, tuple(sorted(left_deficits)), tuple(sorted(right_deficits)))
                            alpha_one_patterns[key] += 1
                            if (same_minus, same_plus) == (0, 1):
                                qonly_residuals = [
                                    1
                                    - 2 * sum(point in block for block in s_right)
                                    - sum(point in block for block in q_right)
                                    for point in sorted(q_left)
                                ]
                                required = sum(max(value, 0) for value in right_deficits)
                                maximum = sum(max(-value, 0) for value in qonly_residuals) + xonly_plus
                            elif (same_minus, same_plus) == (1, 0):
                                qonly_residuals = [
                                    -1
                                    + 2 * len(s_left & FANO_BLOCKS[index - 1])
                                    + len(q_left & FANO_BLOCKS[index - 1])
                                    for index in sorted(q_right_idx)
                                ]
                                required = sum(max(value, 0) for value in left_deficits)
                                maximum = sum(max(value, 0) for value in qonly_residuals) + xonly_minus
                            else:
                                raise AssertionError("unexpected alpha-one orientation")
                            if required != 4 or maximum != 3:
                                raise AssertionError(
                                    "alpha-one coupled endpoint counts differ: "
                                    f"orientation={(same_minus, same_plus)}, "
                                    f"required={required}, maximum={maximum}, "
                                    f"qonly={qonly_residuals}"
                                )
                            coupling_checks.append((required, maximum))
        summary[str(alpha)] = {
            "labelled_assignments": total,
            "outside_token_capacity_survivors": feasible,
        }
    expected = {
        "0": {"labelled_assignments": 3003, "outside_token_capacity_survivors": 651},
        "1": {"labelled_assignments": 24010, "outside_token_capacity_survivors": 42},
        "2": {"labelled_assignments": 41895, "outside_token_capacity_survivors": 0},
        "3": {"labelled_assignments": 13230, "outside_token_capacity_survivors": 0},
        "4": {"labelled_assignments": 441, "outside_token_capacity_survivors": 0},
    }
    if summary != expected or len(coupling_checks) != 42:
        raise AssertionError("independent Fano overlap census differs")
    patterns = [
        {
            "counts": list(key[0]),
            "left_deficits": list(key[1]),
            "right_deficits": list(key[2]),
            "multiplicity": count,
        }
        for key, count in sorted(alpha_one_patterns.items())
    ]
    if sorted(row["multiplicity"] for row in patterns) != [21, 21]:
        raise AssertionError("alpha-one pattern multiplicities differ")
    return {
        "capacity": summary,
        "alpha_one_patterns": patterns,
        "alpha_one_required_endpoints": 4,
        "alpha_one_maximum_other_side_endpoints": 3,
        "alpha_one_excluded": True,
        "derived": {
            "same_sign_overlap": 0,
            "opposite_sign_overlap": 6,
            "support_union_size": 22,
            "z_positive_coordinates": 8,
            "z_negative_coordinates": 8,
        },
    }


def exclusive_shapes() -> dict[str, object]:
    edges = list(itertools.combinations(range(4), 2))
    survivors = []
    for mask in range(1 << len(edges)):
        adjacency = [set() for _ in range(4)]
        for index, (left, right) in enumerate(edges):
            if mask >> index & 1:
                adjacency[left].add(right)
                adjacency[right].add(left)
        if min(map(len, adjacency)) < 2:
            continue
        if any(
            len(adjacency[left] & adjacency[right]) > 1
            for left, right in edges
            if right in adjacency[left]
        ):
            continue
        survivors.append(mask)
    if len(survivors) != 3 or any(mask.bit_count() != 4 for mask in survivors):
        raise AssertionError("four-vertex C4 classification differs")
    return {
        "k_values": [2, 3, 4],
        "k2_smaller_side": "K3",
        "k3_sides": ["C4", "C4"],
        "k3_cross_edges": 0,
        "k4_smaller_side": "K3",
        "labelled_four_vertex_graphs_checked": 64,
        "labelled_C4_survivors": 3,
    }


def graph_caps(nodes: list[str], edges: set[tuple[str, str]]) -> dict[str, object]:
    adjacency = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    for left, right in itertools.combinations(nodes, 2):
        common = len(adjacency[left] & adjacency[right])
        if common > (1 if right in adjacency[left] else 2):
            raise AssertionError("partial common-neighbor upper cap fails")
    triangles = [
        triple
        for triple in itertools.combinations(nodes, 3)
        if all(tuple(sorted(edge)) in edges for edge in itertools.combinations(triple, 2))
    ]
    incident = Counter(vertex for triple in triangles for vertex in triple)
    return {
        "degrees": sorted(len(adjacency[node]) for node in nodes),
        "triangles": len(triangles),
        "maximum_incident_triangles": max(incident.values(), default=0),
    }


def replay_partial_control() -> dict[str, object]:
    payload = json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))["hostile_partial_control"]
    nodes = list(payload["nodes"])
    edges = {tuple(sorted(edge)) for edge in payload["edges"]}
    x = payload["x"]
    z = payload["z"]
    q = payload["q"]
    if len(nodes) != 22 or len(edges) != 52 or set(x) != set(nodes) or set(z) != set(nodes):
        raise AssertionError("partial-control dimensions differ")
    if any(q[node] != z[node] - x[node] for node in nodes):
        raise AssertionError("partial q is not z-x")
    adjacency = {node: set() for node in nodes}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    for node in nodes:
        ax = sum(x[neighbor] for neighbor in adjacency[node])
        az = sum(z[neighbor] for neighbor in adjacency[node])
        aq = sum(q[neighbor] for neighbor in adjacency[node])
        if (ax, az, aq) != (3 * z[node], 4 * x[node] - z[node], -4 * q[node]):
            raise AssertionError(f"partial lift equation fails at {node}")
    metrics = graph_caps(nodes, edges)
    if metrics["degrees"] != payload["degree_multiset"] or metrics["maximum_incident_triangles"] > 7:
        raise AssertionError("partial-control graph metrics differ")

    q_negative = [node for node in nodes if q[node] == -1]
    q_positive = [node for node in nodes if q[node] == 1]
    if len(q_negative) != 7 or len(q_positive) != 7:
        raise AssertionError("partial q support is not 7+7")
    if any(tuple(sorted(pair)) in edges for pair in itertools.combinations(q_negative, 2)):
        raise AssertionError("negative q support is not independent")
    if any(tuple(sorted(pair)) in edges for pair in itertools.combinations(q_positive, 2)):
        raise AssertionError("positive q support is not independent")
    cross_degrees = [
        sum(tuple(sorted((left, right))) in edges for right in q_positive)
        for left in q_negative
    ]
    if cross_degrees != [4] * 7:
        raise AssertionError("partial q support is not complementary-Fano regular")

    # Add a new zero-coordinate vertex with one neighbor P0.  Every displayed
    # equation remains unchanged and all upper caps remain valid, while the
    # omitted outside Ax and Az equations both have residual one.
    witness_neighbor = "P0"
    extended_nodes = nodes + ["O0"]
    extended_edges = set(edges)
    extended_edges.add(tuple(sorted((witness_neighbor, "O0"))))
    extended_metrics = graph_caps(extended_nodes, extended_edges)
    if max(extended_metrics["degrees"]) > 14:
        raise AssertionError("hostile outside extension exceeds the degree cap")
    outside_ax = x[witness_neighbor]
    outside_az = z[witness_neighbor]
    if outside_ax == 0 or outside_az == 0:
        raise AssertionError("hostile outside witness does not violate omitted equations")
    return {
        "vertices": len(nodes),
        "outside_vertices_missing": 77,
        "edges": len(edges),
        "degree_multiset": metrics["degrees"],
        "all_displayed_Ax_equals_3z": True,
        "all_displayed_Az_equals_4x_minus_z": True,
        "all_displayed_Aq_equals_minus4q": True,
        "pair_common_neighbor_caps": True,
        "local_triangle_upper_cap": True,
        "hostile_extension_preserves_upper_caps": True,
        "hostile_outside_Ax_residual": outside_ax,
        "hostile_outside_Az_residual": outside_az,
        "full_outside_equations_implied": False,
        "global_completion_implied": False,
    }


def build_result() -> dict[str, object]:
    overlap = overlap_census()
    result = {
        "source_code_imported": False,
        "spectral_split": spectral_identities(),
        "residue_shell_quantization": residue_shell_summary(),
        "balanced_weight14_shells": balanced_shells(),
        "zero_q_branch": zero_q_branch(),
        "complementary_fano_import": fano_import_check(),
        "norm14_overlap": overlap,
        "exclusive_shapes": exclusive_shapes(),
        "hostile_partial_control": replay_partial_control(),
        "weights_excluded": {"14": False, "17": False, "20": False, "23": False},
        "balanced_weight14_q_squared14_branch_excluded": False,
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "rank11_endpoint": "UNKNOWN",
        "global_status": "UNKNOWN",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("independent proof-A archive differs")
        print("PASS: independent Wave208 proof-A reconstruction")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
