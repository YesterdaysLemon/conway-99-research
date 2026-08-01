#!/usr/bin/env python3
"""Exact checks for the Wave 207 ternary adjacency-code bridge.

The script uses only the Python standard library.  It does not construct or
search for a graph.  Its finite loops verify pointwise inequalities and the
submitted aggregate hostile control.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
P = 3
V = 99
K = 14
LAM = 1
MU = 2

FROZEN_INPUTS = {
    "CONJECTURE.md":
        "7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58",
    "attempts/wave176-star-projector-circuits/derivation.md":
        "b5ba53c9d93d3c8169f7d7bbf179c3d355b01df36f3feb9fec797c7274a568c8",
    "attempts/wave206-crossing-kernel-proof-b/derivation.md":
        "9bdc0a296f704a5bd73ffa3a726694b74454b011dac486da9afa599f868aab13",
    "attempts/wave206-tensor-balance-weight-proof-b/derivation.md":
        "7d13a1834819e952c4d4eff033fac033e23699ab643d9852318a67d19bcb6cf2",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_frozen_inputs() -> dict[str, str]:
    actual = {name: sha256(ROOT / name) for name in FROZEN_INPUTS}
    require(actual == FROZEN_INPUTS, "frozen input hash mismatch")
    return actual


# Elements of the adjacency algebra are coefficient triples for I,A,J.
Alg = tuple[int, int, int]


def alg_add(left: Alg, right: Alg) -> Alg:
    return tuple((a + b) % P for a, b in zip(left, right))  # type: ignore[return-value]


def alg_scale(scalar: int, value: Alg) -> Alg:
    return tuple((scalar * a) % P for a in value)  # type: ignore[return-value]


def alg_mul(left: Alg, right: Alg) -> Alg:
    """Multiply using A^2=(k-mu)I+(lambda-mu)A+mu J."""
    li, la, lj = left
    ri, ra, rj = right
    out_i = li * ri + la * ra * (K - MU)
    out_a = li * ra + la * ri + la * ra * (LAM - MU)
    out_j = (
        li * rj + lj * ri
        + la * ra * MU
        + la * rj * K + lj * ra * K
        + lj * rj * V
    )
    return out_i % P, out_a % P, out_j % P


def adjacency_algebra_checks() -> dict[str, object]:
    identity = (1, 0, 0)
    adjacency = (0, 1, 0)
    all_ones = (0, 0, 1)
    gram = alg_add(adjacency, identity)
    projector = alg_add(gram, alg_scale(-1, all_ones))
    expected_a2 = ((K - MU) % P, (LAM - MU) % P, MU % P)
    require(alg_mul(adjacency, adjacency) == expected_a2, "A^2 changed")
    require(
        alg_mul(gram, gram) == alg_add(gram, alg_scale(-1, all_ones)),
        "G^2 != G-J",
    )
    require(alg_mul(adjacency, projector) == (0, 0, 0), "AE != 0")
    require(alg_mul(projector, projector) == projector, "E is not idempotent")
    return {
        "basis": ["I", "A", "J"],
        "A_squared_mod_3": list(expected_a2),
        "G": list(gram),
        "E": list(projector),
        "G_squared_equals_G_minus_J": True,
        "A_E_equals_zero": True,
        "E_squared_equals_E": True,
    }


def bridge_checks() -> dict[str, object]:
    composition = [1] * 4 + [2] * 4
    a_sum = sum(composition) % P
    a_norm = sum(value * value for value in composition) % P
    require(a_sum == 0, "4+4 word is not centered")
    require(a_norm == 2, "weight-eight norm changed")
    possible = [w for w in range(1, 25) if w % P == a_norm]
    require(possible == [2, 5, 8, 11, 14, 17, 20, 23], "weight list changed")
    return {
        "composition": {"coefficient_1": 4, "coefficient_2": 4},
        "sum_a_mod_3": a_sum,
        "a_dot_a_mod_3": a_norm,
        "B_one_mod_3": 7 % P,
        "sum_c_mod_3": 0,
        "point_image": "b=Ba=BB^T c=Gc=Ec",
        "kernel_identity": "Ab=0",
        "nonzero_witness": "c^T b=a^T a=2",
        "b_dot_b_mod_3": 2,
        "support_union_bound": 24,
        "possible_weights_before_distance_floor": possible,
        "possible_weights_after_distance_floor": [14, 17, 20, 23],
    }


def f_value(i: int, j: int) -> int:
    return i * (i - 1) // 2 + j * (j - 1) // 2 + 2 * i * j - i - j


def phi_value(membership: str, i: int, j: int) -> int:
    common = 6 * i * (i - 1) - 3 * j * (j - 1) + 4 * i * j
    if membership == "P":
        return common - 6 * i + 12 * j
    if membership == "N":
        return common + 3 - 12 * i + 5 * j
    if membership == "O":
        return common - 12 * i + 8 * j
    raise ValueError(membership)


def admissible_pairs(max_i: int, max_j: int) -> Iterable[tuple[int, int]]:
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            if i + j <= K and (i - j) % P == 0:
                yield i, j


def signed_distance_checks() -> dict[str, object]:
    base_table = [
        {"i": i, "j": j, "F": f_value(i, j)}
        for i, j in admissible_pairs(K, K)
    ]
    require(all(row["F"] >= 0 for row in base_table), "F has a negative value")

    low_weight_bounds = []
    for w in range(1, 10):
        maximum = 3 * w * w // 2 if w % 2 == 0 else (3 * w * w - 1) // 2
        low_weight_bounds.append(
            {"weight": w, "upper_w2_plus_2pn": maximum, "required": 15 * w}
        )
        require(maximum < 15 * w, f"base inequality no longer excludes weight {w}")

    w10_compositions = []
    for p_count in range(11):
        n_count = 10 - p_count
        if (p_count - n_count) % P:
            continue
        lhs = 10 * 10 + 2 * p_count * n_count
        w10_compositions.append([p_count, n_count, lhs])
    require(w10_compositions == [[2, 8, 132], [5, 5, 150], [8, 2, 132]],
            "weight-ten composition list changed")
    require(20 % P != 0, "weight-ten same-sign contradiction disappeared")

    ranges = {"P": (6, 4), "N": (7, 3), "O": (7, 4)}
    phi_tables: dict[str, list[dict[str, int]]] = {}
    for membership, (max_i, max_j) in ranges.items():
        table = [
            {"i": i, "j": j, "Phi": phi_value(membership, i, j)}
            for i, j in admissible_pairs(max_i, max_j)
        ]
        require(all(row["Phi"] >= 0 for row in table), f"negative Phi_{membership}")
        phi_tables[membership] = table

    p_count, n_count = 7, 4
    farkas_sum = (
        3 * n_count
        - 12 * K * p_count
        + 8 * K * n_count
        + 12 * p_count * (p_count - 1)
        - 6 * n_count * (n_count - 1)
        + 8 * p_count * n_count
    )
    require(farkas_sum == -60, "weight-eleven Farkas sum changed")

    return {
        "pointwise_F_nonnegative": True,
        "pointwise_F_table": base_table,
        "weights_1_through_9": low_weight_bounds,
        "weight_10": {
            "admissible_compositions_and_bounds": w10_compositions,
            "only_survivor": [5, 5],
            "forced_same_sign_common_neighbor_sum": 20,
            "local_contribution_divisor": 3,
            "contradiction": True,
        },
        "weight_11": {
            "hard_composition": [7, 4],
            "phi_tables": phi_tables,
            "all_phi_nonnegative": True,
            "global_farkas_sum": farkas_sum,
            "contradiction": True,
        },
        "derived_minimum_distance_lower_bound": 12,
    }


def local_matching_feasible(record: dict[str, object]) -> bool:
    i = int(record["i"])
    j = int(record["j"])
    h_pp = int(record["h_pp"])
    h_nn = int(record["h_nn"])
    h_pn = int(record["h_pn"])
    p_singles = i - 2 * h_pp - h_pn
    n_singles = j - 2 * h_nn - h_pn
    occupied_pairs = h_pp + h_nn + h_pn + p_singles + n_singles
    return (
        min(h_pp, h_nn, h_pn, p_singles, n_singles) >= 0
        and occupied_pairs <= 7
    )


def formal_control_checks() -> dict[str, object]:
    path = HERE / "formal-control.json"
    control = json.loads(path.read_text(encoding="utf-8"))
    records = control["records"]
    require(all(local_matching_feasible(row) for row in records),
            "a local matching record is impossible")
    require(all((int(row["i"]) - int(row["j"])) % P == 0 for row in records),
            "a formal record violates the ternary check")

    def total(expression) -> int:
        return sum(int(row["count"]) * expression(row) for row in records)

    category_counts = {
        membership: total(lambda row, m=membership: int(row["membership"] == m))
        for membership in ("P", "N", "O")
    }
    require(category_counts == {"P": 7, "N": 7, "O": 85}, "category counts changed")
    sum_i = total(lambda row: int(row["i"]))
    sum_j = total(lambda row: int(row["j"]))
    e_p_twice = total(
        lambda row: int(row["i"]) if row["membership"] == "P" else 0
    )
    e_n_twice = total(
        lambda row: int(row["j"]) if row["membership"] == "N" else 0
    )
    e_pn_from_p = total(
        lambda row: int(row["j"]) if row["membership"] == "P" else 0
    )
    e_pn_from_n = total(
        lambda row: int(row["i"]) if row["membership"] == "N" else 0
    )
    require(e_p_twice % 2 == e_n_twice % 2 == 0, "nonintegral edge count")
    e_p, e_n = e_p_twice // 2, e_n_twice // 2
    require(e_pn_from_p == e_pn_from_n, "cross handshakes disagree")
    e_pn = e_pn_from_p

    choose_i = total(lambda row: int(row["i"]) * (int(row["i"]) - 1) // 2)
    choose_j = total(lambda row: int(row["j"]) * (int(row["j"]) - 1) // 2)
    cross_pairs = total(lambda row: int(row["i"]) * int(row["j"]))
    matching_totals = {
        "h_pp": total(lambda row: int(row["h_pp"])),
        "h_nn": total(lambda row: int(row["h_nn"])),
        "h_pn": total(lambda row: int(row["h_pn"])),
    }
    require(sum_i == sum_j == K * 7, "regularity moment failed")
    require(choose_i == 7 * 6 - e_p, "positive pair moment failed")
    require(choose_j == 7 * 6 - e_n, "negative pair moment failed")
    require(cross_pairs == 2 * 7 * 7 - e_pn, "cross pair moment failed")
    require(matching_totals == {"h_pp": e_p, "h_nn": e_n, "h_pn": e_pn},
            "aggregate 7K2 matching sums failed")

    positive_degrees = sorted(
        int(row["i"])
        for row in records
        for _ in range(int(row["count"]))
        if row["membership"] == "P"
    )
    negative_degrees = sorted(
        int(row["j"])
        for row in records
        for _ in range(int(row["count"]))
        if row["membership"] == "N"
    )
    require(positive_degrees == [0, 0, 0, 0, 0, 6, 6], "positive control changed")
    require(negative_degrees == positive_degrees, "negative control changed")
    nongraphical = positive_degrees[-1] == 6 and positive_degrees.count(0) == 5
    require(nongraphical, "hostile control accidentally lost its declared failure")

    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(path),
        "category_counts": category_counts,
        "sum_i": sum_i,
        "sum_j": sum_j,
        "edge_counts": {"e_P": e_p, "e_N": e_n, "e_PN": e_pn},
        "pair_moments": {
            "sum_choose_i_2": choose_i,
            "sum_choose_j_2": choose_j,
            "sum_i_j": cross_pairs,
        },
        "matching_totals": matching_totals,
        "all_local_matching_records_feasible": True,
        "declared_nongraphical": nongraphical,
        "is_graph": False,
        "is_codeword": False,
    }


def build_result() -> dict[str, object]:
    return {
        "schema_version": 1,
        "claim_label": "DERIVED_CONDITIONAL_WITH_UNKNOWN_WALL",
        "scope": "parameter-only ternary adjacency-code bridge for a hypothetical srg(99,14,1,2)",
        "frozen_inputs": check_frozen_inputs(),
        "adjacency_algebra": adjacency_algebra_checks(),
        "weight_eight_bridge": bridge_checks(),
        "signed_neighbor_distance": signed_distance_checks(),
        "aggregate_hostile_control": formal_control_checks(),
        "conclusions": {
            "kernel_minimum_distance_lower_bound": 12,
            "endpoint_point_image_nonzero": True,
            "endpoint_point_image_possible_weights": [14, 17, 20, 23],
            "kernel_minimum_distance_at_least_24": "UNKNOWN",
            "weight_24_classification": "UNKNOWN",
            "rank_11_endpoint": "UNKNOWN",
            "conway_99": "UNKNOWN",
        },
    }


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        submitted = json.loads(args.verify.read_text(encoding="utf-8"))
        require(submitted == result, "submitted result does not match exact recomputation")
    if args.output:
        args.output.write_text(canonical(result), encoding="utf-8")
    if not args.output:
        print(canonical(result), end="")


if __name__ == "__main__":
    main()
