#!/usr/bin/env python3
"""Post-source delta audit for the sealed Wave 209 proof-A package.

This file is intentionally separate from ``independent_rank3.py``.  It may
load the discovery checker only after the independent archive has been built.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_DIR = ROOT / "attempts" / "wave209-rank3-trade-proof-a"
SOURCE_MODULE = SOURCE_DIR / "exact_check.py"
SOURCE_MANIFEST = SOURCE_DIR / "package-manifest.sha256"
ARCHIVE = HERE / "post-source-audit.json"

sys.path.insert(0, str(HERE))
import independent_rank3 as clean  # noqa: E402


def load_source():
    spec = importlib.util.spec_from_file_location("wave209_rank3_discovery_post_source", SOURCE_MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load sealed source module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source_manifest() -> dict[str, object]:
    outer = file_sha256(SOURCE_MANIFEST)
    expected_outer = "521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1"
    if outer != expected_outer:
        raise AssertionError("outer source seal differs")
    entries = []
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        actual = file_sha256(ROOT / relative)
        if actual != expected:
            raise AssertionError(f"manifest entry differs: {relative}")
        entries.append({"path": relative, "sha256": actual})
    return {"outer_sha256": outer, "entries_checked": len(entries), "entries": entries}


def erdos_gallai(sequence: Sequence[int]) -> bool:
    degrees = sorted(sequence, reverse=True)
    return sum(degrees) % 2 == 0 and all(
        sum(degrees[:size])
        <= size * (size - 1) + sum(min(degree, size) for degree in degrees[size:])
        for size in range(1, len(degrees) + 1)
    )


def shell_key(
    k: int,
    x: int,
    plus: Sequence[int],
    minus: Sequence[int],
    outside: Sequence[int],
) -> tuple[object, ...]:
    return (k, x, tuple(sorted(plus)), tuple(sorted(minus)), tuple(outside))


def independent_shell_catalog(k: int) -> set[tuple[object, ...]]:
    rows: set[tuple[object, ...]] = set()
    maximum = min(5, k - 4)
    for x in range(k * k // 9 + 1):
        if (x + 3 * k) % 2:
            continue
        histograms = clean.degree_histograms(k, x, maximum)
        for plus_histogram in histograms:
            plus = clean.expanded_degrees(plus_histogram)
            if not erdos_gallai(tuple(value + 3 for value in plus)):
                continue
            for minus_histogram in histograms:
                minus = clean.expanded_degrees(minus_histogram)
                if not erdos_gallai(tuple(value + 3 for value in minus)):
                    continue
                if not clean.gale_ryser(plus_histogram, minus_histogram):
                    continue
                first = 11 * k - 2 * x
                squares = sum(value * value for value in plus + minus)
                second = 2 * k * k - 7 * x - squares
                if (second - first) % 2:
                    continue
                factorial_second = (second - first) // 2
                for outside in clean.outside_histograms(99 - 2 * k, first, factorial_second):
                    rows.add(shell_key(k, x, plus, minus, outside))
    return rows


def source_shell_catalog(source, k: int) -> set[tuple[object, ...]]:
    return {
        shell_key(
            int(row["k"]),
            int(row["x"]),
            row["positive_opposite_degrees"],
            row["negative_opposite_degrees"],
            row["outside_signatures_z0_to_z7"],
        )
        for row in source.shell_catalog(k)
    }


def aggregate_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        int(row["x"]),
        tuple(int(value) for value in row["plus_cross_degree_histogram"]),
        tuple(int(value) for value in row["minus_cross_degree_histogram"]),
        tuple(int(value) for value in row["outside_balanced_degree_histogram"]),
    )


def shell_to_aggregate(key: tuple[object, ...]) -> tuple[object, ...]:
    _, x, plus, minus, outside = key
    plus_histogram = tuple(Counter(plus)[degree] for degree in range(6))
    minus_histogram = tuple(Counter(minus)[degree] for degree in range(6))
    return (x, plus_histogram, minus_histogram, outside)


def source_marked_m5_set(source) -> set[tuple[tuple[int, int], ...]]:
    allowed = {(3, 1, 1, 0), (2, 2, 1, 0)}
    rows = set()
    for chosen in combinations(source.PRODUCT_ONE_EDGES, 5):
        degrees = [0] * 8
        for left, right in chosen:
            degrees[left] += 1
            degrees[right] += 1
        positive = tuple(sorted(degrees[:4], reverse=True))
        negative = tuple(sorted(degrees[4:], reverse=True))
        if positive not in allowed or negative not in allowed:
            continue
        positive_isolated = degrees[:4].index(0)
        negative_isolated = 4 + degrees[4:].index(0)
        if (positive_isolated, negative_isolated) not in source.PRODUCT_ONE_EDGES:
            continue
        rows.add(tuple(sorted((left, right - 4) for left, right in chosen)))
    return rows


def clean_marked_m5_set(result: dict[str, object]) -> set[tuple[tuple[int, int], ...]]:
    return {
        tuple(sorted(tuple(edge) for edge in marked))
        for marked in result["weight14_m5"]["marked_lines"]["accepted_subsets"]
    }


def m2_bound_map(source) -> tuple[dict[tuple[tuple[int, int], ...], int], dict[tuple[tuple[int, int], ...], int]]:
    source_rows = {}
    clean_rows = {}
    for chosen in combinations(source.PRODUCT_ONE_EDGES, 2):
        local = tuple(sorted((left, right - 4) for left, right in chosen))
        maximum_zero, _ = source.zero_edge_capacity(chosen)
        source_rows[local] = 18 - maximum_zero
        clean_rows[local] = len(clean.protected_q1_pairs(local))
    return source_rows, clean_rows


def cross_deficit_profile() -> dict[str, int]:
    graph = clean.adjacency(7, clean.ROOTED_GRAPH)
    deficits = clean.deficit_edges(clean.ROOTED_GRAPH)
    required = [[2 for _ in range(7)] for _ in range(7)]
    required[0][0] = 1
    for vertex in graph[0]:
        required[vertex][0] -= 1
        required[0][vertex] -= 1
    profiles: Counter[tuple[int, int, int]] = Counter()
    valid = 0
    for ordering in permutations(deficits):
        residual = [row[:] for row in required]
        for plus_edge, minus_edge in zip(deficits, ordering):
            for plus in plus_edge:
                for minus in minus_edge:
                    residual[plus][minus] -= 1
        if min(min(row) for row in residual) < 0:
            continue
        valid += 1
        flat = [value for row in residual for value in row]
        profiles[(flat.count(0), flat.count(1), flat.count(2))] += 1
    if valid != 4480:
        raise AssertionError("post-source independent deficit profile count differs")
    return {
        f"zeros_{zero}_ones_{one}_twos_{two}": count
        for (zero, one, two), count in sorted(profiles.items())
    }


def source_line_type_to_clean(row: dict[str, object]) -> dict[tuple[int, int], int]:
    source_types = row["types"]
    mapping = {
        "000": (0, 0),
        "P00": (1, 0),
        "N00": (0, 1),
        "PP0": (2, 0),
        "PN0": (1, 1),
        "NN0": (0, 2),
        "PPP": (3, 0),
        "PPN": (2, 1),
        "PNN": (1, 2),
        "NNN": (0, 3),
    }
    return {mapping[name]: int(value) for name, value in source_types.items()}


def build_post_source_result() -> dict[str, object]:
    manifest = verify_source_manifest()
    source = load_source()
    source_result = source.build_results()
    clean_result = clean.build_result()

    shell_comparisons = {}
    source_shells_by_k = {}
    for k in (7, 10):
        source_rows = source_shell_catalog(source, k)
        clean_rows = independent_shell_catalog(k)
        if source_rows != clean_rows:
            raise AssertionError(f"full aggregate shell differs at k={k}")
        source_shells_by_k[k] = source_rows
        shell_comparisons[str(k)] = {
            "rows": len(source_rows),
            "full_set_equal": True,
            "set_sha256": clean.canonical_json_hash(sorted(source_rows)),
        }

    clean_aggregate = {aggregate_key(row) for row in clean_result["weight20_m2"]["aggregate_rows"]}
    source_aggregate = {
        shell_to_aggregate(key)
        for key in source_shells_by_k[10]
        if key[1] in (2, 4, 6, 8)
    }
    if clean_aggregate != source_aggregate or len(clean_aggregate) != 352:
        raise AssertionError("352-row aggregate result sets differ")

    source_marked = source_marked_m5_set(source)
    independent_marked = clean_marked_m5_set(clean_result)
    if source_marked != independent_marked or len(source_marked) != 204:
        raise AssertionError("204 marked subsets differ")

    source_m2, independent_m2 = m2_bound_map(source)
    if source_m2 != independent_m2:
        raise AssertionError("per-labelled-m2 lower bounds differ")

    source_deficit_profiles = source_result["weight14_final_reduction"]["cross_deficit_bijections"][
        "residual_value_profile_counts"
    ]
    independent_deficit_profiles = cross_deficit_profile()
    if source_deficit_profiles != independent_deficit_profiles:
        raise AssertionError("deficit residual profiles differ")

    for name, row in source.LINE_WITNESSES.items():
        counts = source_line_type_to_clean(row)
        if not clean.line_type_table_valid(counts, int(row["k"]), int(row["x"])):
            raise AssertionError(f"source line witness fails independent replay: {name}")

    removed = sorted(
        key
        for key in clean_aggregate
        if key[2][4] or key[2][5] or key[1][4] or key[1][5]
    )
    # key order is (x, plus histogram, minus histogram, outside histogram).
    if len(removed) != 6 or any(key[0] != 4 for key in removed):
        raise AssertionError("degree-four selected-line delta differs")

    return {
        "schema_version": 1,
        "source_manifest": manifest,
        "source_claim_label": source_result["claim_label"],
        "source_global_status": source_result["global_status"],
        "comparisons": {
            "selected_row_identity": {
                "source_matched_counts": source_result["selected_line_row_identity"][
                    "all_four_matched_q0_cross_counts"
                ],
                "independent_coordinate_cases": clean_result["r_minus_3k"][
                    "marked_and_mask_cases_checked"
                ],
                "equal_conclusion": True,
            },
            "aggregate_shells": shell_comparisons,
            "weight20_aggregate_352": {
                "full_set_equal": True,
                "rows": len(clean_aggregate),
                "set_sha256": clean.canonical_json_hash(sorted(clean_aggregate)),
            },
            "weight14_rooted_graph": {
                "canonical_edges_equal": source_result["weight14_final_reduction"][
                    "rooted_support_census"
                ]["canonical_edges"]
                == clean_result["weight14_m5"]["rooted_sign_graph"]["representative_edges"],
                "valid_labelled_graphs": 180,
                "rooted_types": 1,
            },
            "weight14_deficit_bijections": {
                "count_equal": True,
                "valid": 4480,
                "residual_profiles_equal": True,
            },
            "weight14_marked_subsets": {
                "full_set_equal": True,
                "rows": len(source_marked),
                "set_sha256": clean.canonical_json_hash(sorted(source_marked)),
            },
            "weight20_m2_lower_bounds": {
                "all_66_labelled_bounds_equal": True,
                "distribution": {
                    str(bound): count
                    for bound, count in sorted(Counter(source_m2.values()).items())
                },
                "x2_swapped_cases": 6,
            },
            "line_type_witnesses": {
                "all_source_witnesses_independently_replayed": True,
                "line_vector_identity_independently_derived": "C*tau=7*tau, B*tau=10*c, ||tau||^2=20*k",
            },
        },
        "findings": {
            "aggregate_352_scope": "VERIFIED as an aggregate-only necessary catalog",
            "post_aggregate_selected_line_degree_cap": {
                "claim_label": "DERIVED",
                "reason": "matched q0 contributes zero and each of the three other opposite selected-line pairs has at most one support-support edge",
                "maximum_opposite_degree_per_support_point": 3,
                "aggregate_rows_removed": len(removed),
                "removed_rows": [
                    {
                        "x": key[0],
                        "plus_cross_degree_histogram": list(key[1]),
                        "minus_cross_degree_histogram": list(key[2]),
                        "outside_balanced_degree_histogram": list(key[3]),
                    }
                    for key in removed
                ],
                "removed_rows_sha256": clean.canonical_json_hash(removed),
                "combined_remaining_rows": 352 - len(removed),
                "promotion_status": "requires another independent verifier",
            },
            "source_test_undercoverage": [
                "source tests assert headline aggregate counts but not full result-set equality",
                "source selected-row test does not inject nonzero matched q0 crosses coordinatewise",
                "source tests do not combine the 352 aggregate rows with the selected-line degree cap",
            ],
            "source_claims_refuted": False,
            "source_claims_narrowed": True,
        },
        "scope_walls": {
            "aggregate_or_combined_rows_are_graphs": False,
            "complete_99_vertex_object": False,
            "complete_nonexistence_certificate": False,
            "rank_four_branches_excluded": False,
            "conway_99_status": "UNKNOWN",
            "rank11_endpoint_status": "UNKNOWN",
            "n3_4158_endpoint_status": "UNKNOWN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build_post_source_result()
    if args.write:
        ARCHIVE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"WROTE {ARCHIVE}")
    elif args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("post-source audit archive differs")
        print("PASS: Wave 209 post-source delta audit")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
