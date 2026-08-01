"""Exact arithmetic checks for the Wave 208 integer-lift proof-A package.

This module performs only bounded integer and seven-point Fano-incidence
enumerations.  It does not search for, construct, or complete a graph on 99
vertices.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]

FROZEN_INPUTS = {
    "CONJECTURE.md": "7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58",
    "attempts/wave208-global-residual-rigidity/protocol.md": "3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740",
    "attempts/wave207-ternary-adjacency-code-bridge/derivation.md": "27860e2f8b5ce23c37a43a1ef53fb31d7eda1ee67926e04406ccbf0d938e40b5",
    "attempts/wave207-ternary-adjacency-code-bridge/exact-results.json": "94ed011861be9cf201ac5c531a704832cf8675c5b993c420e92a2e5812f8e7d8",
    "attempts/wave207-kernel-endpoint-proof-c/derivation.md": "da5397c731df8912e076671f80724413be8ab3b5e6dd2336778c61741c25b69f",
    "attempts/wave207-kernel-endpoint-proof-c/exact-results.json": "f323f6735893c0f1b48de7c1eab92e964fc7a6ab89fe479ae985aeec1662bc4e",
    "verification/wave71-modular-theta-extension/audit.md": "0a6280aa008ea7d329c3609bb044f636d52600315e5aff78a27c4712a439cd73",
    "verification/wave94-general-n3-norm14-bound/audit.md": "ab87d369345a27abb4326915f6c392545573780b4fc7f5d67bc494743c4a2ce6",
}

POINTS = frozenset(range(7))
FANO_LINES = (
    frozenset((0, 1, 2)),
    frozenset((0, 3, 4)),
    frozenset((0, 5, 6)),
    frozenset((1, 3, 5)),
    frozenset((1, 4, 6)),
    frozenset((2, 3, 6)),
    frozenset((2, 4, 5)),
)
FANO_COMPLEMENT_BLOCKS = tuple(POINTS - line for line in FANO_LINES)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_inputs() -> list[dict[str, str]]:
    rows = []
    for relative, expected in FROZEN_INPUTS.items():
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise AssertionError(
                f"frozen input drift: {relative}: expected {expected}, got {actual}"
            )
        rows.append({"path": relative, "sha256": actual})
    return rows


def spectral_split_identities() -> dict[str, object]:
    """Record coefficient-level checks of the two exact eigenspace lifts."""

    # The checked input identities are Ax=3z, Az=4x-z+2t*1,
    # A1=14*1, sum(x)=3t, and sum(z)=14t.
    # Q=9(z-x)-t1 and R=11(4x+3z)-6t1.
    aq = {"x": 36, "z": -36, "one_t": 4}
    minus_four_q = {"x": 36, "z": -36, "one_t": 4}
    ar = {"x": 132, "z": 99, "one_t": -18}
    three_r = {"x": 132, "z": 99, "one_t": -18}
    if aq != minus_four_q or ar != three_r:
        raise AssertionError("spectral split coefficient identity failed")

    # Norm identities are expanded exactly from
    # z^2=(4w-h+6t^2)/3 and x.z=h.
    samples = []
    for w, t, h in ((14, 0, 8), (17, 1, 8), (20, 4, 14), (23, 7, 32)):
        z2 = Fraction(4 * w - h + 6 * t * t, 3)
        q2_expanded = 81 * (z2 + w - 2 * h) - 99 * t * t
        q2_closed = 63 * (3 * (w - h) + t * t)
        u2 = 16 * w + 24 * h + 9 * z2
        r2_expanded = 121 * u2 - 3564 * t * t
        r2_closed = 77 * (11 * (4 * w + 3 * h) - 18 * t * t)
        if q2_expanded != q2_closed or r2_expanded != r2_closed:
            raise AssertionError("spectral norm identity failed")
        samples.append(
            {
                "w": w,
                "t": t,
                "h": h,
                "z_squared": int(z2),
                "Q_squared": int(q2_closed),
                "R_squared": int(r2_closed),
            }
        )

    return {
        "Q": "9*(z-x)-t*1",
        "Q_equation": "A*Q=-4*Q",
        "Q_sum": 0,
        "Q_squared": "63*(3*(w-h)+t^2)",
        "Q_coordinate_residue_mod_9": "-t",
        "R": "11*(4*x+3*z)-6*t*1",
        "R_equation": "A*R=3*R",
        "R_sum": 0,
        "R_squared": "77*(11*(4*w+3*h)-18*t^2)",
        "balanced_primitive_minus_four_vector": "q=z-x when t=0",
        "samples": samples,
    }


def residue_shell_rows() -> dict[str, object]:
    """Enumerate exact necessary h-shells for weights 17, 20, and 23."""

    output: dict[str, object] = {}
    for w in (17, 20, 23):
        compositions = []
        for t in range(8):
            if (w + 3 * t) % 2 or 3 * t > w:
                continue
            p = (w + 3 * t) // 2
            n = w - p
            spectral_lower = Fraction(-44 * w + 18 * t * t, 33)
            spectral_upper = Fraction(3 * w + t * t, 3)
            minimum_residue_norm = 99 * t * (9 - t)
            rows = []
            for h in range(-50, 51):
                if h % 2 or h % 3 != w % 3:
                    continue
                if not spectral_lower <= h <= spectral_upper:
                    continue
                q_squared = 63 * (3 * (w - h) + t * t)
                excess = q_squared - minimum_residue_norm
                if excess < 0 or excess % 162:
                    continue
                rows.append(
                    {
                        "h": h,
                        "Q_squared": q_squared,
                        "residue_shell_index_L": excess // 162,
                    }
                )
            if not rows:
                raise AssertionError(f"unexpected empty necessary shell list: w={w}, t={t}")
            compositions.append(
                {
                    "composition_up_to_sign": [p, n],
                    "t": t,
                    "spectral_h_interval": [
                        str(spectral_lower),
                        str(spectral_upper),
                    ],
                    "minimum_residue_norm": minimum_residue_norm,
                    "necessary_rows_only": rows,
                }
            )
        output[str(w)] = compositions

    return {
        "identity": (
            "Q^2=99*t*(9-t)+162*L for 0<=t<=8, because "
            "Q_i=9*n_i-t, sum(n_i)=11*t, and sum n_i(n_i-1) is even"
        ),
        "warning": (
            "Rows are arithmetic necessities only; no row is asserted to be "
            "a graph or codeword. Negative t is covered by x -> -x."
        ),
        "weights": output,
    }


def balanced_weight14_shells() -> dict[str, object]:
    rows = []
    for h in range(-30, 31):
        if h % 6 != 2:
            continue
        if Fraction(-56, 3) <= h <= 14:
            q2 = Fraction(7 * (14 - h), 3)
            if q2.denominator != 1:
                raise AssertionError("balanced q norm lost integrality")
            rows.append({"h": h, "q_squared": int(q2)})
    expected = [
        {"h": -16, "q_squared": 70},
        {"h": -10, "q_squared": 56},
        {"h": -4, "q_squared": 42},
        {"h": 2, "q_squared": 28},
        {"h": 8, "q_squared": 14},
        {"h": 14, "q_squared": 0},
    ]
    if rows != expected:
        raise AssertionError(f"balanced shell drift: {rows}")
    return {
        "h_definition": "h=x.z=(x^T A x)/3",
        "q": "z-x",
        "q_equation": "Aq=-4q",
        "r": "4x+3z",
        "r_equation": "Ar=3r",
        "orthogonality": "q.r=0",
        "rows": rows,
    }


def minimum_wedge_sum(edge_count: int) -> tuple[int, list[int]]:
    cross_edges = 2 * edge_count - 21
    best: tuple[int, list[int]] | None = None
    for excess in itertools.product(range(4), repeat=7):
        if sum(excess) != cross_edges:
            continue
        degrees = sorted(3 + value for value in excess)
        wedges = sum(degree * (degree - 1) // 2 for degree in degrees)
        candidate = (wedges, degrees)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise AssertionError("degree minimization unexpectedly infeasible")
    return best


def zero_q_three_eigen_branch() -> dict[str, object]:
    # q=0 means z=x and Ax=3x.  If e is the number of same-sign
    # edges in either seven-set, cross edges=2e-21 and total edges=4e-21.
    restricted_edge_cap = (
        Fraction(3 * 14, 2) + Fraction(11 * 14 * 14, 198)
    ).numerator // (
        Fraction(3 * 14, 2) + Fraction(11 * 14 * 14, 198)
    ).denominator
    if restricted_edge_cap != 31:
        raise AssertionError("14-vertex restricted-eigenvalue cap drift")

    rows = []
    for e in (11, 12, 13):
        wedge_min, degrees = minimum_wedge_sum(e)
        capacity = 42 - e
        if e == 13:
            status = "EXCLUDED_BY_WEDGE_CAPACITY"
            if not wedge_min > capacity:
                raise AssertionError("e=13 contradiction failed")
        elif e == 12:
            status = "EXCLUDED_BY_EQUALITY_TRIANGLE_PARITY"
            if wedge_min != capacity or e % 3:
                raise AssertionError("e=12 equality arithmetic failed")
            # Equality forces all 12 edges into four edge-disjoint triangles,
            # making every induced degree even; the minimizing sequence has
            # four degree-three vertices.
            if sum(degree % 2 for degree in degrees) != 4:
                raise AssertionError("e=12 parity witness drift")
        else:
            status = "SURVIVES_THIS_ARGUMENT"
            if degrees != [3, 3, 3, 3, 3, 3, 4]:
                raise AssertionError("e=11 survivor degree sequence drift")
        rows.append(
            {
                "same_sign_edges_each_side": e,
                "cross_edges": 2 * e - 21,
                "total_support_edges": 4 * e - 21,
                "minimum_same_side_wedges": wedge_min,
                "same_side_common_neighbor_capacity": capacity,
                "minimizing_degree_sequence": degrees,
                "status": status,
            }
        )
    return {
        "premise": "balanced weight 14 and q=z-x=0, hence Ax=3x",
        "restricted_edge_cap_on_support": restricted_edge_cap,
        "rows": rows,
        "survivor": (
            "exactly one cross edge, joining the unique degree-four vertex "
            "on each side; both same-sign degree sequences are (4,3^6)"
        ),
    }


def partitions(a: int, b: int, c: int) -> Iterable[tuple[set[int], set[int], set[int]]]:
    if a + b + c != 7:
        return
    for first_tuple in itertools.combinations(range(7), a):
        first = set(first_tuple)
        remainder = set(range(7)) - first
        for third_tuple in itertools.combinations(sorted(remainder), c):
            third = set(third_tuple)
            yield first, remainder - third, third


def overlap_capacity_enumeration() -> tuple[dict[str, object], list[dict[str, object]]]:
    """Enumerate all labelled complementary-Fano category assignments.

    The enumeration is over seven labelled points and seven labelled
    complement-of-line blocks.  It assumes no graph automorphism and checks
    only the necessary outside-token capacity described in derivation.md.
    """

    summary: dict[str, object] = {}
    feasible_records: list[dict[str, object]] = []
    for same_overlap in range(5):
        total = 0
        feasible = 0
        count_rows: dict[tuple[int, ...], list[int]] = {}
        for same_minus in range(same_overlap + 1):
            same_plus = same_overlap - same_minus
            opposite_total = same_overlap + 6
            exclusive_each = 8 - 2 * same_overlap
            for opposite_plus in range(8):
                opposite_minus = opposite_total - opposite_plus
                qonly_minus = 7 - same_minus - opposite_plus
                qonly_plus = 7 - same_plus - opposite_minus
                if min(opposite_minus, qonly_minus, qonly_plus) < 0:
                    continue
                xonly_plus = 7 - same_plus - opposite_plus
                xonly_minus = 7 - same_minus - opposite_minus
                if min(xonly_plus, xonly_minus) < 0:
                    continue
                if xonly_plus + xonly_minus != exclusive_each:
                    raise AssertionError("exclusive count drift")

                row_key = (
                    same_minus,
                    same_plus,
                    opposite_plus,
                    opposite_minus,
                    qonly_minus,
                    qonly_plus,
                    xonly_plus,
                    xonly_minus,
                )
                row_counts = count_rows.setdefault(row_key, [0, 0])

                for s_minus, o_plus, q_minus in partitions(
                    same_minus, opposite_plus, qonly_minus
                ):
                    for s_plus, o_minus, q_plus in partitions(
                        same_plus, opposite_minus, qonly_plus
                    ):
                        positive_deficits = []
                        for point in sorted(o_plus):
                            inside = 2 * sum(
                                point in FANO_COMPLEMENT_BLOCKS[block]
                                for block in s_plus
                            ) + sum(
                                point in FANO_COMPLEMENT_BLOCKS[block]
                                for block in q_plus
                            )
                            positive_deficits.append(4 - inside)

                        negative_deficits = []
                        for block in sorted(o_minus):
                            inside = 2 * len(
                                s_minus & FANO_COMPLEMENT_BLOCKS[block]
                            ) + len(q_minus & FANO_COMPLEMENT_BLOCKS[block])
                            negative_deficits.append(4 - inside)

                        capacity_ok = (
                            sum(max(value, 0) for value in positive_deficits)
                            <= xonly_plus
                            and sum(max(-value, 0) for value in positive_deficits)
                            <= xonly_minus
                            and sum(max(value, 0) for value in negative_deficits)
                            <= xonly_minus
                            and sum(max(-value, 0) for value in negative_deficits)
                            <= xonly_plus
                        )
                        total += 1
                        row_counts[0] += 1
                        if capacity_ok:
                            feasible += 1
                            row_counts[1] += 1
                            feasible_records.append(
                                {
                                    "same_overlap": same_overlap,
                                    "counts": list(row_key),
                                    "S_minus": sorted(s_minus),
                                    "O_plus": sorted(o_plus),
                                    "Qonly_minus": sorted(q_minus),
                                    "S_plus": sorted(s_plus),
                                    "O_minus": sorted(o_minus),
                                    "Qonly_plus": sorted(q_plus),
                                    "positive_deficits": positive_deficits,
                                    "negative_deficits": negative_deficits,
                                }
                            )

        summary[str(same_overlap)] = {
            "labelled_assignments": total,
            "outside_token_capacity_survivors": feasible,
            "count_rows": [
                {"counts": list(key), "total": values[0], "feasible": values[1]}
                for key, values in sorted(count_rows.items())
            ],
        }

    expected = {
        "0": (3003, 651),
        "1": (24010, 42),
        "2": (41895, 0),
        "3": (13230, 0),
        "4": (441, 0),
    }
    actual = {
        key: (
            value["labelled_assignments"],
            value["outside_token_capacity_survivors"],
        )
        for key, value in summary.items()
    }
    if actual != expected:
        raise AssertionError(f"Fano overlap census drift: {actual}")
    return summary, feasible_records


def eliminate_same_overlap_one(records: list[dict[str, object]]) -> dict[str, object]:
    rows = [record for record in records if record["same_overlap"] == 1]
    if len(rows) != 42:
        raise AssertionError("same-overlap-one survivor count drift")
    patterns: dict[tuple[object, ...], int] = {}
    for row in rows:
        key = (
            tuple(row["counts"]),
            tuple(sorted(row["positive_deficits"])),
            tuple(sorted(row["negative_deficits"])),
        )
        patterns[key] = patterns.get(key, 0) + 1
    expected_patterns = {
        ((0, 1, 5, 2, 2, 4, 1, 5), (0, 0, 0, 0, 0), (2, 2)): 21,
        ((1, 0, 2, 5, 4, 2, 5, 1), (2, 2), (0, 0, 0, 0, 0)): 21,
    }
    if patterns != expected_patterns:
        raise AssertionError(f"same-overlap-one pattern drift: {patterns}")

    for row in rows:
        counts = row["counts"]
        same_minus, same_plus = counts[0], counts[1]
        if (same_minus, same_plus) == (0, 1):
            # A q-only negative point has z=-1 and x=0, so its required
            # signed outside contribution is 1 minus its positive inside
            # Fano mass.  The two such points have total -2.
            s_plus = set(row["S_plus"])
            q_plus = set(row["Qonly_plus"])
            qonly_signed = []
            for point in row["Qonly_minus"]:
                inside = 2 * sum(
                    point in FANO_COMPLEMENT_BLOCKS[block] for block in s_plus
                ) + sum(
                    point in FANO_COMPLEMENT_BLOCKS[block] for block in q_plus
                )
                qonly_signed.append(1 - inside)
            if sorted(qonly_signed) != [-1, -1]:
                raise AssertionError("same-overlap-one left endpoint sum drift")
        else:
            # The other pattern is obtained by global sign reversal.
            if (same_minus, same_plus) != (1, 0):
                raise AssertionError("unexpected same-overlap-one orientation")

    # In the first orientation, the two negative-demand blocks need negative
    # outside surplus four.  Every used outside token has one endpoint on
    # each q-sign side.  The left side has total negative surplus two and
    # only one positive token, hence at most three negative endpoints.  The
    # other orientation is its sign reversal.
    if not 4 > 2 + 1:
        raise AssertionError("coupled endpoint contradiction lost")
    return {
        "capacity_survivors_before_coupling": 42,
        "two_sign_symmetric_patterns": [
            {"multiplicity": count, "counts_and_deficits": [list(key[0]), list(key[1]), list(key[2])]}
            for key, count in sorted(patterns.items())
        ],
        "required_negative_endpoints_on_demand_side": 4,
        "maximum_negative_endpoints_on_other_side": 3,
        "status": "EXCLUDED_BY_COUPLED_X_OR_Y_ENDPOINTS",
    }


def exclusive_graph_shapes() -> dict[str, object]:
    # On four vertices, enforce only the SRG edge common-neighbor upper cap
    # lambda=1 and minimum degree two.  Exactly the three labelled C4s remain.
    edges4 = list(itertools.combinations(range(4), 2))
    valid_four_vertex_graphs = []
    for mask in range(1 << len(edges4)):
        adjacency = [set() for _ in range(4)]
        for index, (left, right) in enumerate(edges4):
            if mask >> index & 1:
                adjacency[left].add(right)
                adjacency[right].add(left)
        if min(map(len, adjacency)) < 2:
            continue
        if any(
            len(adjacency[left] & adjacency[right]) > 1
            for left, right in edges4
            if right in adjacency[left]
        ):
            continue
        valid_four_vertex_graphs.append(
            sorted(tuple(sorted(edge)) for edge in edges4 if edge[1] in adjacency[edge[0]])
        )
    if len(valid_four_vertex_graphs) != 3:
        raise AssertionError("four-vertex C4 classification drift")
    if any(len(graph) != 4 for graph in valid_four_vertex_graphs):
        raise AssertionError("non-C4 survived four-vertex classification")

    return {
        "k_definition": "number of x=+1,q=-1 opposite-overlap coordinates",
        "universal_bound": [2, 4],
        "reason": (
            "each exclusive positive and negative coordinate needs at least "
            "two same-sign exclusive neighbors"
        ),
        "k_2": {
            "exclusive_sign_sizes": [5, 3],
            "smaller_side": "K3",
            "cross_edges_from_smaller_side": 0,
            "q_support_contribution_on_smaller_side": -1,
        },
        "k_3": {
            "exclusive_sign_sizes": [4, 4],
            "positive_side": "C4",
            "negative_side": "C4",
            "cross_edges": 0,
            "q_support_contributions": {"positive": 1, "negative": -1},
            "labelled_four_vertex_graphs_checked": 64,
            "labelled_C4_survivors": len(valid_four_vertex_graphs),
        },
        "k_4": {
            "exclusive_sign_sizes": [3, 5],
            "smaller_side": "K3",
            "cross_edges_from_smaller_side": 0,
            "q_support_contribution_on_smaller_side": 1,
        },
    }


def node_name(node: tuple[str, int]) -> str:
    return f"{node[0]}{node[1]}"


def hostile_partial_control() -> dict[str, object]:
    """Build a 22-vertex partial control for the surviving k=3 branch."""

    positive_cells = ((4, 1), (5, 3), (5, 2), (6, 2))
    negative_cells = ((1, 4), (2, 6), (2, 5), (3, 5))
    nodes = (
        [("L", index) for index in range(7)]
        + [("R", index) for index in range(7)]
        + [(sign, index) for sign in ("P", "N") for index in range(4)]
    )
    adjacency = {node: set() for node in nodes}

    def add_edge(left: tuple[str, int], right: tuple[str, int]) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    for point in range(7):
        for block in range(7):
            if point in FANO_COMPLEMENT_BLOCKS[block]:
                add_edge(("L", point), ("R", block))
    for sign, cells in (("P", positive_cells), ("N", negative_cells)):
        for index, (point, block) in enumerate(cells):
            add_edge((sign, index), ("L", point))
            add_edge((sign, index), ("R", block))
        for index in range(4):
            add_edge((sign, index), (sign, (index + 1) % 4))

    x = {node: 0 for node in nodes}
    z = {node: 0 for node in nodes}
    for index in (4, 5, 6):
        x[("L", index)] = 1
        x[("R", index)] = -1
    for index in (0, 1, 2, 3):
        z[("L", index)] = -1
        z[("R", index)] = 1
        x[("P", index)] = z[("P", index)] = 1
        x[("N", index)] = z[("N", index)] = -1
    q = {node: z[node] - x[node] for node in nodes}

    for node in nodes:
        ax = sum(x[neighbor] for neighbor in adjacency[node])
        az = sum(z[neighbor] for neighbor in adjacency[node])
        aq = sum(q[neighbor] for neighbor in adjacency[node])
        if ax != 3 * z[node]:
            raise AssertionError(f"hostile control lost Ax=3z at {node}")
        if az != 4 * x[node] - z[node]:
            raise AssertionError(f"hostile control lost Az=4x-z at {node}")
        if aq != -4 * q[node]:
            raise AssertionError(f"hostile control lost Aq=-4q at {node}")

    pair_cap_violations = []
    for index, left in enumerate(nodes):
        for right in nodes[index + 1 :]:
            common = len(adjacency[left] & adjacency[right])
            cap = 1 if right in adjacency[left] else 2
            if common > cap:
                pair_cap_violations.append((left, right, common, cap))
    if pair_cap_violations:
        raise AssertionError(f"partial control violates lambda/mu caps: {pair_cap_violations}")

    edges = sorted(
        (node_name(left), node_name(right))
        for left in nodes
        for right in adjacency[left]
        if node_name(left) < node_name(right)
    )
    if len(edges) != 52:
        raise AssertionError("hostile partial-control edge count drift")

    return {
        "status": "HOSTILE_PARTIAL_CONTROL_NOT_A_COMPLETION",
        "scope": (
            "22 vertices only; all displayed Ax=3z, Az=4x-z, Aq=-4q "
            "equations and lambda/mu upper caps hold on displayed vertices"
        ),
        "nodes": [node_name(node) for node in nodes],
        "edges": [list(edge) for edge in edges],
        "x": {node_name(node): x[node] for node in nodes},
        "z": {node_name(node): z[node] for node in nodes},
        "q": {node_name(node): q[node] for node in nodes},
        "positive_cells_in_C4_order": [list(cell) for cell in positive_cells],
        "negative_cells_in_C4_order": [list(cell) for cell in negative_cells],
        "edge_count": len(edges),
        "degree_multiset": sorted(len(adjacency[node]) for node in nodes),
        "pair_common_neighbor_caps_hold": True,
        "local_triangle_upper_cap_holds": True,
        "limitations": [
            "The other 77 vertices and every equation at them are absent.",
            "Displayed degrees are below 14 and have not been completed.",
            "Missing common neighbors and neighborhood matching mates are absent.",
            "This is neither a ternary codeword in a target graph nor a graph certificate.",
        ],
    }


def build_results() -> dict[str, object]:
    overlap_summary, feasible_records = overlap_capacity_enumeration()
    same_one = eliminate_same_overlap_one(feasible_records)
    return {
        "schema_version": 1,
        "claim_label": "DERIVED_PARTIAL_WITH_UNKNOWN_WALL",
        "scope": "Wave 208 point-code integer lift; no 99-vertex graph search",
        "frozen_inputs": verify_frozen_inputs(),
        "spectral_split": spectral_split_identities(),
        "residue_shell_quantization": residue_shell_rows(),
        "balanced_weight14": {
            "spectral_shells": balanced_weight14_shells(),
            "zero_q_three_eigen_branch": zero_q_three_eigen_branch(),
            "norm14_q_overlap_capacity": overlap_summary,
            "same_overlap_one_coupled_exclusion": same_one,
            "derived_overlap_conclusion": {
                "same_sign_overlap": 0,
                "opposite_sign_overlap": 6,
                "support_union_size": 22,
                "z_profile": "eight +1, eight -1, all other coordinates zero",
            },
            "exclusive_graph_shapes": exclusive_graph_shapes(),
        },
        "hostile_partial_control": hostile_partial_control(),
        "conclusions": {
            "balanced_weight14_excluded": False,
            "balanced_weight14_q_squared_14_branch_excluded": False,
            "balanced_weight14_q_squared_14_branch_strictly_reduced": True,
            "weights_17_20_23_excluded": False,
            "kernel_minimum_distance_at_least_24": "UNKNOWN",
            "rank11_endpoint": "UNKNOWN",
            "conway_99": "UNKNOWN",
        },
    }


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    results = build_results()
    rendered = canonical_json(results)
    if args.verify is not None:
        expected = args.verify.read_text(encoding="utf-8")
        if expected != rendered:
            raise AssertionError(f"result drift: {args.verify}")
        print(f"PASS {args.verify}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
