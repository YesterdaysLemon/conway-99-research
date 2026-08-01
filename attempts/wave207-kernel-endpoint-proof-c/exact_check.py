#!/usr/bin/env python3
"""Exact arithmetic checks for the Wave 207 kernel-endpoint checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K = 14
FIELD = 3

FROZEN_INPUTS = {
    "CONJECTURE.md": "7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58",
    "attempts/wave207-ternary-adjacency-code-bridge/derivation.md":
        "27860e2f8b5ce23c37a43a1ef53fb31d7eda1ee67926e04406ccbf0d938e40b5",
    "attempts/wave207-ternary-adjacency-code-bridge/exact-results.json":
        "94ed011861be9cf201ac5c531a704832cf8675c5b993c420e92a2e5812f8e7d8",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_frozen_inputs() -> list[dict[str, str]]:
    rows = []
    for relative, expected in FROZEN_INPUTS.items():
        path = ROOT / relative
        actual = sha256(path)
        require(actual == expected, f"frozen input drifted: {relative}")
        rows.append({"path": relative, "sha256": actual})
    return rows


def admissible_types(p: int, n: int) -> Iterable[tuple[str, int, int]]:
    ranges = {
        "P": (p - 1, n),
        "N": (p, n - 1),
        "O": (p, n),
    }
    for membership, (max_i, max_j) in ranges.items():
        for i in range(min(K, max_i) + 1):
            for j in range(min(K - i, max_j) + 1):
                if (i - j) % FIELD == 0:
                    yield membership, i, j


def phi_1_13(membership: str, i: int, j: int) -> int:
    indicator_n = int(membership == "N")
    return (
        indicator_n
        + 4 * i
        - 2 * j
        + j * (j - 1)
        + indicator_n * j
        - 2 * i * j
        - 2 * indicator_n * i
    )


def phi_4_10(membership: str, i: int, j: int) -> int:
    indicator_n = int(membership == "N")
    return 3 * i - 2 * j + j * (j - 1) - i * j + indicator_n * (j - i)


def certificate_check(p: int, n: int) -> dict[str, object]:
    if (p, n) == (1, 13):
        phi = phi_1_13
        global_sum = (
            n + 4 * K * p - 2 * K * n
            + 2 * n * (n - 1) - 4 * p * n
        )
        expected = -35
        scale = 35
        factorization = {
            "P_i=0": "j*(j-3)",
            "O_i=0": "j*(j-3)",
            "O_i=1": "(j-1)*(j-4)",
            "N_i=0": "(j-1)^2",
            "N_i=1": "(j-1)*(j-3)",
        }
    elif (p, n) == (4, 10):
        phi = phi_4_10
        global_sum = (
            3 * K * p - 2 * K * n
            + 2 * n * (n - 1) - 2 * p * n
        )
        expected = -12
        scale = 12
        factorization = {
            "P_or_O": "(j-3)*(j-i)",
            "N": "(j-2)*(j-i)",
        }
    else:
        raise ValueError((p, n))

    table = [
        {"membership": membership, "i": i, "j": j,
         "phi": phi(membership, i, j)}
        for membership, i, j in admissible_types(p, n)
    ]
    require(table, "empty pointwise table")
    require(all(int(row["phi"]) >= 0 for row in table),
            f"negative pointwise value for {(p, n)}")
    require(global_sum == expected, f"global sum changed for {(p, n)}")
    return {
        "composition": [p, n],
        "dual_scale": scale,
        "admissible_type_count": len(table),
        "minimum_pointwise_value": min(int(row["phi"]) for row in table),
        "zero_type_count": sum(int(row["phi"]) == 0 for row in table),
        "maximum_pointwise_value": max(int(row["phi"]) for row in table),
        "all_pointwise_values_nonnegative": True,
        "global_sum": global_sum,
        "contradiction": True,
        "factorization_by_case": factorization,
    }


def weight_compositions(weight: int) -> list[list[int]]:
    return [
        [p, weight - p]
        for p in range(weight + 1)
        if (p - (weight - p)) % FIELD == 0
    ]


def composition_reduction() -> dict[str, object]:
    all_14 = weight_compositions(14)
    require(all_14 == [[1, 13], [4, 10], [7, 7], [10, 4], [13, 1]],
            "weight-fourteen composition list changed")
    certs = [certificate_check(1, 13), certificate_check(4, 10)]
    return {
        "weight_14_admissible_before_farkas": all_14,
        "certificates": certs,
        "negation_covers": [[13, 1], [10, 4]],
        "surviving_composition": [7, 7],
        "weight_14_excluded": False,
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


def hostile_control_check() -> dict[str, object]:
    path = HERE / "balanced-aggregate-control.json"
    control = json.loads(path.read_text(encoding="utf-8"))
    records = control["records"]
    require(all(local_matching_feasible(row) for row in records),
            "locally impossible 7K2 record")
    require(all((int(row["i"]) - int(row["j"])) % FIELD == 0 for row in records),
            "ternary residue failure")

    def total(expression) -> int:
        return sum(int(row["count"]) * expression(row) for row in records)

    category_counts = {
        membership: total(lambda row, m=membership: int(row["membership"] == m))
        for membership in ("P", "N", "O")
    }
    require(category_counts == {"P": 7, "N": 7, "O": 85},
            "category counts changed")
    sum_i = total(lambda row: int(row["i"]))
    sum_j = total(lambda row: int(row["j"]))
    e_p_twice = total(lambda row: int(row["i"]) if row["membership"] == "P" else 0)
    e_n_twice = total(lambda row: int(row["j"]) if row["membership"] == "N" else 0)
    e_pn_p = total(lambda row: int(row["j"]) if row["membership"] == "P" else 0)
    e_pn_n = total(lambda row: int(row["i"]) if row["membership"] == "N" else 0)
    require(e_p_twice % 2 == e_n_twice % 2 == 0, "half-integral edge count")
    require(e_pn_p == e_pn_n, "cross handshakes disagree")
    e_p, e_n, e_pn = e_p_twice // 2, e_n_twice // 2, e_pn_p
    choose_i = total(lambda row: int(row["i"]) * (int(row["i"]) - 1) // 2)
    choose_j = total(lambda row: int(row["j"]) * (int(row["j"]) - 1) // 2)
    cross = total(lambda row: int(row["i"]) * int(row["j"]))
    matching = {
        key: total(lambda row, k=key: int(row[k]))
        for key in ("h_pp", "h_nn", "h_pn")
    }
    require(sum_i == sum_j == 98, "first moments failed")
    require(choose_i == 42 - e_p, "positive pair moment failed")
    require(choose_j == 42 - e_n, "negative pair moment failed")
    require(cross == 98 - e_pn, "cross pair moment failed")
    require(matching == {"h_pp": e_p, "h_nn": e_n, "h_pn": e_pn},
            "local matching totals failed")

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
    declared_failure = (
        positive_degrees == [0, 0, 0, 0, 0, 6, 6]
        and negative_degrees == positive_degrees
    )
    require(declared_failure, "hostile control lost its graphical failure")
    return {
        "path": "attempts/wave207-kernel-endpoint-proof-c/balanced-aggregate-control.json",
        "sha256": sha256(path),
        "category_counts": category_counts,
        "edge_counts": {"e_P": e_p, "e_N": e_n, "e_PN": e_pn},
        "pair_moments": {
            "sum_choose_i_2": choose_i,
            "sum_choose_j_2": choose_j,
            "sum_i_j": cross,
        },
        "matching_totals": matching,
        "all_recorded_aggregate_equations_hold": True,
        "declared_nongraphical": True,
        "is_graph": False,
        "is_codeword": False,
    }


def lift_collapse_check() -> dict[str, object]:
    checks = []
    for p, n in ((1, 13), (4, 10), (7, 7), (10, 7), (13, 4)):
        require((p - n) % 3 == 0, "nonintegral t")
        t = (p - n) // 3
        # The P-category sum of Az=4x-z+2t1 differs from the signed
        # pair-moment evaluation by 2p(p-n)-6tp.
        p_residual = 2 * p * (p - n) - 6 * t * p
        # The N-category residual is 2n(p-n)-6tn.
        n_residual = 2 * n * (p - n) - 6 * t * n
        require(p_residual == n_residual == 0, "lift aggregate did not collapse")
        checks.append({"composition": [p, n], "t": t,
                       "P_residual": p_residual, "N_residual": n_residual})
    return {
        "integer_lift": "z=Ax/3; Az=4x-z+2t*1",
        "category_summed_lift_adds_no_equation": True,
        "sample_symbolic_residuals": checks,
    }


def build_result() -> dict[str, object]:
    return {
        "schema_version": 1,
        "claim_label": "DERIVED_PARTIAL_WITH_UNKNOWN_WALL",
        "scope": "parameter-only signed-support reduction for endpoint kernel weights",
        "frozen_inputs": check_frozen_inputs(),
        "weight_14_reduction": composition_reduction(),
        "balanced_hostile_control": hostile_control_check(),
        "integer_lift_boundary": lift_collapse_check(),
        "conclusions": {
            "weight_14_unbalanced_compositions": "REFUTED",
            "weight_14_balanced_7_plus_7": "UNKNOWN",
            "weight_14_excluded": False,
            "weight_17_excluded": False,
            "weight_20_excluded": False,
            "weight_23_excluded": False,
            "endpoint_excluded": False,
            "kernel_minimum_distance_at_least_24": "UNKNOWN",
            "conway_99": "UNKNOWN",
        },
    }


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = canonical(result)
    if args.verify is not None:
        require(json.loads(args.verify.read_text(encoding="utf-8")) == result,
                f"result mismatch: {args.verify}")
    print(rendered, end="")


if __name__ == "__main__":
    main()
