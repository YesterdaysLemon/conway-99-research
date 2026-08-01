#!/usr/bin/env python3
"""Source-blind exact necessary point/residual-line coupling reconstruction.

This module deliberately does not import any Wave 209 or Wave 210 code.  It
uses only the two frozen Wave 209 JSON witness tables.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POINT_PATH = ROOT / "attempts/wave209-rank4-norm56-proof-b/point-signature-controls.json"
LINE_PATH = ROOT / "attempts/wave209-rank4-norm56-proof-b/aggregate-controls.json"
ALPHA = (1, 1, 1, 1, -1, -1, -1, -1)
SURVIVORS = (0, 2, 4, 11, 12, 14, 23)


def decode3(code: int, shift: int = 0) -> tuple[int, ...]:
    """Decode the frozen base-three convention: coordinate zero is the LSD."""
    out = []
    for _ in range(8):
        code, digit = divmod(code, 3)
        out.append(digit + shift)
    assert code == 0
    return tuple(out)


def negative_set(signature: tuple[int, ...]) -> frozenset[int]:
    return frozenset(i for i, value in enumerate(signature) if value == -1)


def groups(h: frozenset[int], edges: frozenset[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    induced = [edge for edge in edges if edge[0] in h and edge[1] in h]
    used: set[int] = set()
    result: list[tuple[int, ...]] = []
    for i, j in sorted(induced):
        assert i not in used and j not in used, "H[h] is not a matching"
        used.update((i, j))
        result.append((i, j))
    result.extend((i,) for i in sorted(h - used))
    assert len(result) <= 3, "residual line uses more than three point groups"
    return tuple(sorted(result))


def stable_hash(items: list[object]) -> str:
    digest = hashlib.sha256()
    for item in items:
        digest.update(json.dumps(item, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def build_orbit(point_entry: dict, line_entry: dict) -> dict:
    orbit = int(point_entry["orbit_id"])
    assert orbit == int(line_entry["orbit_id"])
    assert point_entry["kind"] == "control"

    point_counts = {int(code): int(count) for code, count in point_entry["counts"]}
    signatures = {code: decode3(code, -1) for code in point_counts}
    assert sum(point_counts.values()) == 99
    for i in range(8):
        margin = Counter()
        for code, count in point_counts.items():
            margin[signatures[code][i]] += count
        assert margin == {-1: 3, 0: 60, 1: 36}
    q_values = {
        code: sum(a * s for a, s in zip(ALPHA, signature)) // 3
        for code, signature in signatures.items()
    }
    assert all(sum(a * s for a, s in zip(ALPHA, signature)) % 3 == 0 for signature in signatures.values())
    assert sum(point_counts[c] * q_values[c] for c in point_counts) == 0
    assert sum(point_counts[c] * q_values[c] ** 2 for c in point_counts) == 56

    edges = frozenset(tuple(sorted(map(int, edge))) for edge in line_entry["selected_intersections"])
    line_types = []
    for d_code, h_mask, count in line_entry["counts"]:
        d = decode3(int(d_code))
        h = frozenset(i for i in range(8) if (int(h_mask) >> i) & 1)
        assert all(d[i] == 1 for i in h)
        local_groups = groups(h, edges)
        t_numerator = sum(a * value for a, value in zip(ALPHA, d))
        assert t_numerator % 3 == 0
        line_types.append(
            {
                "d_code": int(d_code),
                "h_mask": int(h_mask),
                "count": int(count),
                "d": d,
                "h": h,
                "groups": local_groups,
                "t": t_numerator // 3,
            }
        )
    assert sum(item["count"] for item in line_types) == 223
    assert sum(item["count"] * item["t"] for item in line_types) == 0
    assert sum(item["count"] * item["t"] ** 2 for item in line_types) == 96

    rows: dict[str, int] = {}
    for code, count in sorted(point_counts.items()):
        signature = signatures[code]
        marked = negative_set(signature)
        degree = 7 - len(marked)
        residual_t = 3 * q_values[code] + 3 * sum(ALPHA[i] for i in marked)
        rows[f"point:{code}:degree"] = count * degree
        rows[f"point:{code}:t"] = count * residual_t
        for i in range(8):
            if i in marked:
                demand = degree
            elif signature[i] == 1:
                selected_account = sum(tuple(sorted((i, j))) in edges for j in marked)
                assert selected_account <= 1
                demand = 1 - selected_account
            else:
                demand = 0
            rows[f"point:{code}:selected:{i}"] = count * demand

    columns: list[object] = []
    for line_index, item in enumerate(line_types):
        type_prefix = f"line:{line_index}:{item['d_code']}:{item['h_mask']}"
        role_specs: list[tuple[tuple[int, ...], int]] = [(g, 1) for g in item["groups"]]
        empty_multiplicity = 3 - len(item["groups"])
        if empty_multiplicity:
            role_specs.append(((), empty_multiplicity))
        for role, multiplicity in role_specs:
            role_name = "empty" if not role else ".".join(map(str, role))
            rows[f"{type_prefix}:role:{role_name}"] = item["count"] * multiplicity
        for i, value in enumerate(item["d"]):
            rows[f"{type_prefix}:plus:{i}"] = item["count"] * (2 if i in item["h"] else value)

        for role, _multiplicity in role_specs:
            role_set = frozenset(role)
            role_name = "empty" if not role else ".".join(map(str, role))
            for code, signature in sorted(signatures.items()):
                if negative_set(signature) != role_set:
                    continue
                if any(signature[i] != 1 for i in item["h"] - role_set):
                    continue
                if any(signature[i] != 0 for i, value in enumerate(item["d"]) if i not in item["h"] and value == 0):
                    continue
                entries: dict[str, int] = {
                    f"{type_prefix}:role:{role_name}": 1,
                    f"point:{code}:degree": 1,
                    f"point:{code}:t": item["t"],
                }
                for i, value in enumerate(signature):
                    if value == 1:
                        entries[f"{type_prefix}:plus:{i}"] = 1
                for i in item["h"]:
                    entries[f"point:{code}:selected:{i}"] = 1
                columns.append(
                    [
                        [line_index, role_name, code],
                        sorted((name, value) for name, value in entries.items() if value),
                    ]
                )

    row_items = sorted(rows.items())
    columns.sort(key=lambda value: value[0])
    return {
        "orbit_id": orbit,
        "branch_count": int(line_entry["branch_count"]),
        "selected_intersections": [list(edge) for edge in sorted(edges)],
        "point_signature_support": len(point_counts),
        "residual_line_type_support": len(line_types),
        "residual_lines": sum(item["count"] for item in line_types),
        "row_count": len(row_items),
        "column_count": len(columns),
        "row_rhs_sha256": stable_hash(row_items),
        "sparse_matrix_sha256": stable_hash(columns),
        "point_degree_total": sum(point_counts[c] * (7 - len(negative_set(signatures[c]))) for c in point_counts),
        "line_point_slots": 3 * 223,
    }


def main() -> None:
    point_data = json.loads(POINT_PATH.read_text(encoding="utf-8"))
    line_data = json.loads(LINE_PATH.read_text(encoding="utf-8"))
    point_by_orbit = {int(item["orbit_id"]): item for item in point_data["orbits"]}
    line_by_orbit = {int(item["orbit_id"]): item for item in line_data["controls"]}
    assert tuple(orbit for orbit in sorted(point_by_orbit) if point_by_orbit[orbit]["kind"] == "control") == SURVIVORS
    results = [build_orbit(point_by_orbit[orbit], line_by_orbit[orbit]) for orbit in SURVIVORS]
    assert sum(item["branch_count"] for item in results) == 51
    for item in results:
        assert item["point_degree_total"] == item["line_point_slots"]
    output = {
        "format": "wave210-rank4-cleanroom-coupling-v1",
        "claim_label": "DERIVED",
        "source_blind": True,
        "target_automorphism_assumed": False,
        "survivor_orbits": list(SURVIVORS),
        "labelled_branches": 51,
        "orbits": results,
        "limitations": [
            "This seals an independently derived necessary aggregate incidence system.",
            "No infeasibility dual has yet been supplied or checked at this source-blind stage.",
            "The system couples censuses, not named graph points or named residual lines.",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
