#!/usr/bin/env python3
"""Post-seal independent audit of the Wave 210 rank-four coupling package.

This file is intentionally separate from ``independent_verify.py`` and its
blind seal.  It reconstructs the membership-filtered source systems using the
sealed first-principles objects, canonicalizes and compares every source row
and column, replays all archived integer duals, and transports them over all
51 labelled branches without assuming a graph automorphism.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BLIND_MODULE_PATH = HERE / "independent_verify.py"
SOURCE_DIR = ROOT / "attempts" / "wave210-rank4-point-line-coupling-proof-b"
SOURCE_MODULE_PATH = SOURCE_DIR / "coupling_check.py"
SOURCE_CERTIFICATES = SOURCE_DIR / "coupling-certificates.json"
SOURCE_RESULTS = SOURCE_DIR / "exact-results.json"
SOURCE_MANIFEST = SOURCE_DIR / "package-manifest.sha256"
RESULTS = HERE / "post-source-results.json"

EXPECTED_SOURCE_MANIFEST_SHA256 = "7eb45280b61e1612f4d70aa95922b7821e16aa3c426832eadb8995809d5cff78"


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


blind = load_module("wave212_blind", BLIND_MODULE_PATH)


Signature = tuple[int, ...]
Edge = tuple[int, int]
ResidualType = tuple[tuple[int, ...], frozenset[int], int]
Decomposition = tuple[Signature, Signature, Signature]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sha256_manifest(path: Path, expected_entries: int | None = None) -> dict[str, str]:
    checked: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        expected, relative = raw.split(maxsplit=1)
        relative = relative.strip().lstrip("*")
        if relative in checked:
            raise AssertionError(f"duplicate manifest path: {relative}")
        actual = sha256(ROOT / relative)
        if actual != expected.lower():
            raise AssertionError((relative, expected, actual))
        checked[relative] = actual
    if expected_entries is not None and len(checked) != expected_entries:
        raise AssertionError((path, expected_entries, len(checked)))
    return checked


def verify_seals() -> dict[str, object]:
    blind_inputs = verify_sha256_manifest(HERE / "blind-input-freeze.sha256", 7)
    blind_outputs = verify_sha256_manifest(HERE / "blind-seal.sha256", 3)
    outer = sha256(SOURCE_MANIFEST)
    if outer != EXPECTED_SOURCE_MANIFEST_SHA256:
        raise AssertionError((EXPECTED_SOURCE_MANIFEST_SHA256, outer))
    source_entries = verify_sha256_manifest(SOURCE_MANIFEST, 12)
    return {
        "blind_input_entries": len(blind_inputs),
        "blind_output_entries": len(blind_outputs),
        "source_manifest_sha256": outer,
        "source_manifest_entries": len(source_entries),
    }


def selected_membership(signature: Signature) -> frozenset[int]:
    return frozenset(i for i, value in enumerate(signature) if value == -1)


@lru_cache(maxsize=None)
def admissible_signatures(H: frozenset[Edge]) -> tuple[Signature, ...]:
    answer = []
    for signature in blind.point_signatures():
        membership = selected_membership(signature)
        if not membership or len(membership) == 1:
            answer.append(signature)
        elif len(membership) == 2 and tuple(sorted(membership)) in H:
            answer.append(signature)
    if any(len(selected_membership(signature)) > 2 for signature in answer):
        raise AssertionError("membership filter retained a triple membership")
    return tuple(answer)


@lru_cache(maxsize=None)
def filtered_decompositions(
    H: frozenset[Edge], triangle_type: ResidualType
) -> tuple[Decomposition, ...]:
    """Reconstruct exact local triples using the forced H[h] grouping."""
    d, h, t = triangle_type
    h_edges = tuple(sorted(edge for edge in H if edge[0] in h and edge[1] in h))
    degrees = Counter(vertex for edge in h_edges for vertex in edge)
    if any(degree > 1 for degree in degrees.values()):
        raise AssertionError("H[h] is not a matching")
    used = set(degrees)
    groups = tuple(frozenset(edge) for edge in h_edges) + tuple(
        frozenset((i,)) for i in sorted(h - used)
    )
    if len(groups) > 3:
        raise AssertionError("residual triangle needs more than three intersection points")
    flexible = tuple(i for i in range(8) if i not in h and d[i] in (1, 2))
    all_integral = ALL_POINT_SIGNATURES
    output: set[Decomposition] = set()
    for slots in itertools.permutations(range(3), len(groups)):
        negative_slot = {
            i: slot
            for group, slot in zip(groups, slots)
            for i in group
        }
        for choices in itertools.product(range(3), repeat=len(flexible)):
            signatures = [[0] * 8 for _ in range(3)]
            for i in h:
                for point in range(3):
                    signatures[point][i] = -1 if point == negative_slot[i] else 1
            for i, distinguished in zip(flexible, choices):
                for point in range(3):
                    signatures[point][i] = int(
                        point == distinguished if d[i] == 1 else point != distinguished
                    )
            triple = tuple(
                sorted((tuple(signature) for signature in signatures), key=blind.encode_signature)
            )
            if all(signature in all_integral for signature in triple):
                if sum(blind.q_value(signature) for signature in triple) != t:
                    raise AssertionError("local q sum differs from residual t")
                output.add(triple)
    return tuple(sorted(output, key=lambda triple: tuple(map(blind.encode_signature, triple))))


ALL_POINT_SIGNATURES = frozenset(blind.point_signatures())


def aggregate_name(descriptor: tuple[object, ...]) -> str:
    kind = descriptor[0]
    if kind == "total":
        return "aggregate/total"
    if kind == "d":
        return f"aggregate/d_{descriptor[1]}_{descriptor[2]}"
    if kind == "dproduct":
        return f"aggregate/dprod_{descriptor[1]}_{descriptor[2]}"
    if kind == "tsum":
        return "aggregate/t_sum"
    if kind == "tnorm":
        return "aggregate/t_square"
    if kind == "hit":
        return f"aggregate/h_{descriptor[1]}"
    if kind == "hit_t":
        return f"aggregate/ht_{descriptor[1]}"
    if kind == "hit_pair":
        return f"aggregate/hh_{descriptor[1]}_{descriptor[2]}"
    raise AssertionError(descriptor)


def point_name(descriptor: tuple[object, ...]) -> str:
    kind = descriptor[0]
    if kind == "total":
        return "point/total"
    if kind == "margin":
        return f"point/m_{descriptor[1]}_{descriptor[2]}"
    if kind == "pair":
        return f"point/p_{descriptor[1]}_{descriptor[2]}_{descriptor[3]}_{descriptor[4]}"
    if kind == "qsum":
        return "point/q_sum"
    if kind == "qnorm":
        return "point/q_square"
    raise AssertionError(descriptor)


@dataclass(frozen=True)
class FilteredSystem:
    orbit_id: int
    form_index: int
    selected_edges: frozenset[Edge]
    row_names: tuple[str, ...]
    rhs: tuple[int, ...]
    columns: tuple[object, ...]
    admissible_signature_count: int
    residual_type_count: int
    realizable_type_count: int
    w_column_count: int
    x_column_count: int


def add_entry(entries: dict[int, int], row: int, value: int) -> None:
    if value:
        entries[row] = entries.get(row, 0) + value
        if entries[row] == 0:
            del entries[row]


def build_filtered_system(
    orbit_id: int,
    branch: tuple[int, frozenset[Edge]] | None = None,
) -> FilteredSystem:
    if branch is None:
        branch = blind.branch_orbits()[orbit_id][0]
    form_index, H = branch
    D = blind.grams()[form_index]
    signatures = admissible_signatures(H)
    signature_index = {signature: index for index, signature in enumerate(signatures)}
    aggregate_descriptors = blind.aggregate_descriptors()
    point_descriptors = blind.point_descriptors()
    aggregate_names = tuple(map(aggregate_name, aggregate_descriptors))
    point_names = tuple(map(point_name, point_descriptors))
    coupling_names = tuple(
        name
        for signature in signatures
        for name in (
            f"incidence/{blind.encode_signature(signature)}",
            f"demand/{blind.encode_signature(signature)}",
        )
    )
    row_names = aggregate_names + point_names + coupling_names
    row_index = {name: index for index, name in enumerate(row_names)}
    if len(row_index) != len(row_names):
        raise AssertionError("duplicate filtered row name")
    aggregate_targets = blind.aggregate_targets(D, H)
    point_targets = blind.point_targets(D, H)
    rhs = tuple(
        [aggregate_targets[descriptor] for descriptor in aggregate_descriptors]
        + [point_targets[descriptor] for descriptor in point_descriptors]
        + [0] * (2 * len(signatures))
    )

    triangle_types = blind.residual_types(D, H)
    columns = []
    realizable_types = 0
    for triangle_type in triangle_types:
        d, h, t = triangle_type
        decompositions = filtered_decompositions(H, triangle_type)
        if decompositions:
            realizable_types += 1
        for decomposition in decompositions:
            entries: dict[int, int] = {}
            for descriptor, name in zip(aggregate_descriptors, aggregate_names):
                add_entry(entries, row_index[name], blind.aggregate_feature(descriptor, triangle_type))
            for signature, multiplicity in Counter(decomposition).items():
                if signature not in signature_index:
                    raise AssertionError("local triple uses a filtered-out point signature")
                code = blind.encode_signature(signature)
                add_entry(entries, row_index[f"incidence/{code}"], multiplicity)
                add_entry(entries, row_index[f"demand/{code}"], t * multiplicity)
            descriptor = (
                "W",
                blind.encode_d(d),
                blind.encode_h(h),
                *(blind.encode_signature(signature) for signature in decomposition),
            )
            columns.append(blind.SparseColumn(descriptor, tuple(sorted(entries.items()))))
    w_column_count = len(columns)

    for signature in signatures:
        entries: dict[int, int] = {}
        for descriptor, name in zip(point_descriptors, point_names):
            add_entry(entries, row_index[name], blind.point_feature(descriptor, signature))
        code = blind.encode_signature(signature)
        add_entry(entries, row_index[f"incidence/{code}"], -blind.star_count_multiplier(signature))
        add_entry(entries, row_index[f"demand/{code}"], -blind.star_t_multiplier(signature))
        columns.append(blind.SparseColumn(("X", code), tuple(sorted(entries.items()))))

    columns.sort(key=lambda column: column.descriptor)
    if len({column.descriptor for column in columns}) != len(columns):
        raise AssertionError("duplicate filtered column descriptor")
    if len(row_names) != 99 + 279 + 2 * len(signatures):
        raise AssertionError("filtered row count formula differs")
    return FilteredSystem(
        orbit_id=orbit_id,
        form_index=form_index,
        selected_edges=H,
        row_names=row_names,
        rhs=rhs,
        columns=tuple(columns),
        admissible_signature_count=len(signatures),
        residual_type_count=len(triangle_types),
        realizable_type_count=realizable_types,
        w_column_count=w_column_count,
        x_column_count=len(signatures),
    )


def filtered_hashes(system: FilteredSystem) -> dict[str, str]:
    row_hasher = hashlib.sha256()
    w_hasher = hashlib.sha256()
    x_hasher = hashlib.sha256()
    full_hasher = hashlib.sha256()
    full_hasher.update(blind.canonical_json(["wave212-membership-filtered-canonical-v1", system.orbit_id]))
    for index, (name, rhs) in enumerate(zip(system.row_names, system.rhs)):
        payload = blind.canonical_json([index, name, rhs])
        row_hasher.update(payload)
        full_hasher.update(b"R" + payload)
    for index, column in enumerate(system.columns):
        payload = blind.canonical_json([index, column.descriptor, column.entries])
        (w_hasher if column.descriptor[0] == "W" else x_hasher).update(payload)
        full_hasher.update(b"C" + payload)
    return {
        "row_universe_sha256": row_hasher.hexdigest(),
        "w_columns_sha256": w_hasher.hexdigest(),
        "x_columns_sha256": x_hasher.hexdigest(),
        "full_system_sha256": full_hasher.hexdigest(),
    }


def source_column_descriptor(source: ModuleType, pattern: object | None, signature: Signature | None) -> tuple[object, ...]:
    if pattern is not None:
        triangle_type, triple = pattern
        d, h, _ = triangle_type
        return (
            "W",
            blind.encode_d(d),
            blind.encode_h(h),
            *sorted(blind.encode_signature(point) for point in triple),
        )
    if signature is None:
        raise AssertionError("source column has no semantic identity")
    return ("X", blind.encode_signature(signature))


def normalize_source_system(source: ModuleType, orbit_id: int, independent: FilteredSystem) -> FilteredSystem:
    row_metadata, patterns, matrix, targets = source.build_sparse_system(orbit_id)
    source_names = [name for name, _ in row_metadata]
    if len(source_names) != len(set(source_names)):
        raise AssertionError("source has duplicate row names")
    if set(source_names) != set(independent.row_names):
        raise AssertionError("source and independent row universes differ")
    independent_index = {name: index for index, name in enumerate(independent.row_names)}
    normalized_rhs = [0] * len(independent.row_names)
    for source_row, ((name, recorded_target), numeric_target) in enumerate(zip(row_metadata, targets)):
        if int(numeric_target) != numeric_target or int(numeric_target) != recorded_target:
            raise AssertionError("source target is not the recorded integer")
        normalized_rhs[independent_index[name]] = recorded_target
    if tuple(normalized_rhs) != independent.rhs:
        raise AssertionError("source and independent right-hand sides differ")

    signatures = source.admissible_point_signatures(independent.selected_edges)
    if len(patterns) + len(signatures) != matrix.shape[1]:
        raise AssertionError("source column metadata length differs")
    csc = matrix.tocsc()
    columns = []
    for source_column in range(matrix.shape[1]):
        pattern = patterns[source_column] if source_column < len(patterns) else None
        signature = None if pattern is not None else signatures[source_column - len(patterns)]
        descriptor = source_column_descriptor(source, pattern, signature)
        entries: dict[int, int] = {}
        start, stop = csc.indptr[source_column], csc.indptr[source_column + 1]
        for source_row, numeric_value in zip(csc.indices[start:stop], csc.data[start:stop]):
            if int(numeric_value) != numeric_value:
                raise AssertionError("source matrix contains a nonintegral entry")
            target_row = independent_index[source_names[source_row]]
            add_entry(entries, target_row, int(numeric_value))
        columns.append(blind.SparseColumn(descriptor, tuple(sorted(entries.items()))))
    columns.sort(key=lambda column: column.descriptor)
    normalized = replace(independent, columns=tuple(columns))
    if normalized.columns != independent.columns:
        independent_columns = {column.descriptor: column.entries for column in independent.columns}
        source_columns = {column.descriptor: column.entries for column in normalized.columns}
        missing = set(independent_columns) - set(source_columns)
        extra = set(source_columns) - set(independent_columns)
        differing = {
            descriptor
            for descriptor in set(independent_columns) & set(source_columns)
            if independent_columns[descriptor] != source_columns[descriptor]
        }
        raise AssertionError({"missing": len(missing), "extra": len(extra), "differing": len(differing)})
    return normalized


def compare_source_matrices(independent_systems: dict[int, FilteredSystem]) -> tuple[dict[str, object], ModuleType]:
    source = load_module("wave210_source_after_seal", SOURCE_MODULE_PATH)
    if tuple(source.SURVIVOR_ORBITS) != tuple(blind.SURVIVING_ORBIT_IDS):
        raise AssertionError("source survivor ids differ")
    if source.branch_orbits() != blind.branch_orbits():
        raise AssertionError("source branch orbit partition differs")
    output = []
    for orbit_id in blind.SURVIVING_ORBIT_IDS:
        independent = independent_systems[orbit_id]
        normalized = normalize_source_system(source, orbit_id, independent)
        independent_hashes = filtered_hashes(independent)
        source_hashes = filtered_hashes(normalized)
        if source_hashes != independent_hashes:
            raise AssertionError("normalized source matrix hash differs")
        output.append({
            "orbit_id": orbit_id,
            "row_count": len(independent.row_names),
            "admissible_point_signature_count": independent.admissible_signature_count,
            "residual_type_count": independent.residual_type_count,
            "realizable_triangle_type_count": independent.realizable_type_count,
            "w_column_count": independent.w_column_count,
            "x_column_count": independent.x_column_count,
            "column_count": len(independent.columns),
            "nonzero_count": sum(len(column.entries) for column in independent.columns),
            **independent_hashes,
            "complete_source_matrix_match": True,
        })
    return {"systems": output, "all_complete_matrix_matches": True}, source


def full_row_name_map(system: object) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for index, descriptor in enumerate(system.row_descriptors):
        if descriptor[0] == "aggregate":
            name = aggregate_name(tuple(descriptor[1:]))
        elif descriptor[0] == "point":
            name = point_name(tuple(descriptor[1:]))
        elif descriptor[0] == "star_count":
            name = f"incidence/{descriptor[1]}"
        elif descriptor[0] == "star_t":
            name = f"demand/{descriptor[1]}"
        else:
            raise AssertionError(descriptor)
        mapping[name] = index
    if len(mapping) != len(system.row_descriptors):
        raise AssertionError("full row-name map collided")
    return mapping


def verify_relaxation_inclusion(independent_systems: dict[int, FilteredSystem]) -> dict[str, object]:
    """Mechanically prove every filtered feasible point zero-extends to full."""
    summaries = []
    for orbit_id in blind.SURVIVING_ORBIT_IDS:
        full = blind.build_exact_system(orbit_id)
        filtered = independent_systems[orbit_id]
        full_rows = full_row_name_map(full)
        filtered_rows = {name: index for index, name in enumerate(filtered.row_names)}
        if not set(filtered_rows) <= set(full_rows):
            raise AssertionError("filtered row is absent from the full system")
        for name, filtered_row in filtered_rows.items():
            if filtered.rhs[filtered_row] != full.rhs[full_rows[name]]:
                raise AssertionError("embedded right-hand side differs")
        extra_full_rows = set(full_rows) - set(filtered_rows)
        if any(full.rhs[full_rows[name]] != 0 for name in extra_full_rows):
            raise AssertionError("an omitted full row has nonzero right-hand side")

        full_columns = {column.descriptor: column.entries for column in full.columns}
        embedded_columns = 0
        for column in filtered.columns:
            if column.descriptor not in full_columns:
                raise AssertionError((orbit_id, "filtered column absent from full relaxation", column.descriptor))
            expected_entries = {
                full_rows[filtered.row_names[row]]: value
                for row, value in column.entries
            }
            if tuple(sorted(expected_entries.items())) != full_columns[column.descriptor]:
                raise AssertionError((orbit_id, "zero-extended column differs", column.descriptor))
            embedded_columns += 1
        summaries.append({
            "orbit_id": orbit_id,
            "filtered_rows": len(filtered.row_names),
            "full_rows": len(full.row_descriptors),
            "filtered_columns": len(filtered.columns),
            "full_columns": len(full.columns),
            "embedded_columns_checked": embedded_columns,
            "zero_extension_is_exact": True,
        })
    return {
        "logic": "every membership-filtered feasible vector extends by zero to the larger full-signature system",
        "systems": summaries,
        "larger_system_is_a_necessary_relaxation": True,
    }


def decode_coefficients(item: dict[str, object], row_names: Sequence[str]) -> dict[str, int]:
    allowed = set(row_names)
    coefficients: dict[str, int] = {}
    for name, value in item["coefficients"]:
        if name not in allowed or name in coefficients or not isinstance(value, int) or value == 0:
            raise AssertionError("malformed archived coefficient")
        coefficients[name] = value
    return coefficients


def replay_named_dual(system: FilteredSystem, coefficients: dict[str, int]) -> dict[str, int]:
    if not coefficients:
        raise AssertionError("empty dual")
    row_index = {name: index for index, name in enumerate(system.row_names)}
    if not set(coefficients) <= set(row_index):
        raise AssertionError("dual names a row outside the system")
    vector = {row_index[name]: value for name, value in coefficients.items()}
    rhs = sum(vector.get(row, 0) * value for row, value in enumerate(system.rhs))
    w_values = []
    x_values = []
    for column in system.columns:
        value = sum(vector.get(row, 0) * entry for row, entry in column.entries)
        (w_values if column.descriptor[0] == "W" else x_values).append(value)
    if rhs >= 0 or min(w_values) < 0 or min(x_values) < 0:
        raise AssertionError((system.orbit_id, rhs, min(w_values), min(x_values)))
    return {
        "rhs": rhs,
        "pattern_minimum": min(w_values),
        "pattern_maximum": max(w_values),
        "point_minimum": min(x_values),
        "point_maximum": max(x_values),
        "nonzero_coefficients": len(coefficients),
    }


def replay_source_duals(independent_systems: dict[int, FilteredSystem]) -> tuple[dict[str, object], dict[int, dict[str, int]]]:
    payload = json.loads(SOURCE_CERTIFICATES.read_text(encoding="utf-8"))
    if payload.get("format") != "wave210-rank4-point-line-farkas-v1":
        raise AssertionError("source dual archive format differs")
    if [item.get("orbit_id") for item in payload.get("orbits", [])] != list(blind.SURVIVING_ORBIT_IDS):
        raise AssertionError("source dual orbit order differs")
    source_results = json.loads(SOURCE_RESULTS.read_text(encoding="utf-8"))
    expected = {
        item["orbit_id"]: item
        for item in source_results["local_coupling"]["certificate_summaries"]
    }
    coefficient_maps: dict[int, dict[str, int]] = {}
    summaries = []
    for item in payload["orbits"]:
        orbit_id = item["orbit_id"]
        system = independent_systems[orbit_id]
        coefficients = decode_coefficients(item, system.row_names)
        metrics = replay_named_dual(system, coefficients)
        recorded = expected[orbit_id]
        for key in ("rhs", "pattern_minimum", "point_minimum", "nonzero_coefficients"):
            if metrics[key] != recorded[key]:
                raise AssertionError((orbit_id, key, metrics[key], recorded[key]))
        coefficient_maps[orbit_id] = coefficients
        summaries.append({
            "orbit_id": orbit_id,
            "labelled_branches": len(blind.branch_orbits()[orbit_id]),
            **metrics,
            "orientation": "A^T y >= 0 and b^T y < 0",
        })
    if sum(item["labelled_branches"] for item in summaries) != 51:
        raise AssertionError("source duals do not cover 51 labelled branches")
    return {"certificates": summaries, "all_exact_integer_replays": True}, coefficient_maps


def rename_signature(signature: Signature, permutation: Sequence[int]) -> Signature:
    answer = [0] * 8
    for i, value in enumerate(signature):
        answer[permutation[i]] = value
    return tuple(answer)


def transform_row_name(name: str, permutation: Sequence[int]) -> str:
    prefix, body = name.split("/", 1)
    if prefix in {"incidence", "demand"}:
        signature = blind.decode_signature(int(body))
        return f"{prefix}/{blind.encode_signature(rename_signature(signature, permutation))}"
    if prefix == "aggregate":
        if body in {"total", "t_sum", "t_square"}:
            return name
        fields = body.split("_")
        if fields[0] == "dprod":
            i, j = sorted((permutation[int(fields[1])], permutation[int(fields[2])]))
            return f"aggregate/dprod_{i}_{j}"
        if fields[0] == "d":
            return f"aggregate/d_{permutation[int(fields[1])]}_{fields[2]}"
        if fields[0] == "hh":
            i, j = sorted((permutation[int(fields[1])], permutation[int(fields[2])]))
            return f"aggregate/hh_{i}_{j}"
        if fields[0] in {"h", "ht"}:
            return f"aggregate/{fields[0]}_{permutation[int(fields[1])]}"
    if prefix == "point":
        if body in {"total", "q_sum", "q_square"}:
            return name
        fields = body.split("_")
        if fields[0] == "m":
            return f"point/m_{permutation[int(fields[1])]}_{fields[2]}"
        if fields[0] == "p":
            source_i, source_j = int(fields[1]), int(fields[2])
            target_i, target_j = permutation[source_i], permutation[source_j]
            left, right = fields[3], fields[4]
            if target_i > target_j:
                target_i, target_j, left, right = target_j, target_i, right, left
            return f"point/p_{target_i}_{target_j}_{left}_{right}"
    raise AssertionError(name)


def map_triangle_type(triangle_type: ResidualType, permutation: Sequence[int]) -> ResidualType:
    d, h, t = triangle_type
    mapped_d = [0] * 8
    for i, value in enumerate(d):
        mapped_d[permutation[i]] = value
    return tuple(mapped_d), frozenset(permutation[i] for i in h), t


def constraint_map(
    source_branch: tuple[int, frozenset[Edge]], target_branch: tuple[int, frozenset[Edge]]
) -> tuple[int, ...]:
    source_form, source_H = source_branch
    target_form, target_H = target_branch
    candidates = [
        permutation
        for permutation in blind.form_maps(blind.grams()[source_form], blind.grams()[target_form])
        if blind.permute_edges(source_H, permutation) == target_H
    ]
    if not candidates:
        raise AssertionError("no checked data relabelling connects orbit nodes")
    permutation = min(candidates)
    if any(blind.ALPHA[i] != blind.ALPHA[permutation[i]] for i in range(8)):
        raise AssertionError("constraint map does not preserve marked signs")
    return permutation


def branch_row_targets(form_index: int, H: frozenset[Edge]) -> dict[str, int]:
    D = blind.grams()[form_index]
    aggregate_targets = blind.aggregate_targets(D, H)
    point_targets = blind.point_targets(D, H)
    output = {
        aggregate_name(descriptor): aggregate_targets[descriptor]
        for descriptor in blind.aggregate_descriptors()
    }
    output.update({
        point_name(descriptor): point_targets[descriptor]
        for descriptor in blind.point_descriptors()
    })
    for signature in admissible_signatures(H):
        code = blind.encode_signature(signature)
        output[f"incidence/{code}"] = 0
        output[f"demand/{code}"] = 0
    return output


def verify_transport(
    representative_systems: dict[int, FilteredSystem],
    coefficient_maps: dict[int, dict[str, int]],
) -> dict[str, object]:
    branch_checks = 0
    pattern_checks = 0
    certificate_checks = 0
    for orbit_id in blind.SURVIVING_ORBIT_IDS:
        orbit = blind.branch_orbits()[orbit_id]
        source_branch = orbit[0]
        source_form, source_H = source_branch
        source_D = blind.grams()[source_form]
        source_types = blind.residual_types(source_D, source_H)
        source_signatures = admissible_signatures(source_H)
        source_targets = branch_row_targets(source_form, source_H)
        source_coefficients = coefficient_maps[orbit_id]
        source_metrics = replay_named_dual(representative_systems[orbit_id], source_coefficients)
        for target_branch in orbit:
            target_form, target_H = target_branch
            target_D = blind.grams()[target_form]
            permutation = constraint_map(source_branch, target_branch)
            if {
                rename_signature(signature, permutation)
                for signature in source_signatures
            } != set(admissible_signatures(target_H)):
                raise AssertionError("point-signature transport is not onto")
            target_targets = branch_row_targets(target_form, target_H)
            if {
                transform_row_name(name, permutation): value
                for name, value in source_targets.items()
            } != target_targets:
                raise AssertionError("row target transport differs")

            aggregate_by_name = {
                aggregate_name(descriptor): descriptor
                for descriptor in blind.aggregate_descriptors()
            }
            point_by_name = {
                point_name(descriptor): descriptor
                for descriptor in blind.point_descriptors()
            }
            target_types = set(blind.residual_types(target_D, target_H))
            mapped_types = {map_triangle_type(row, permutation) for row in source_types}
            if mapped_types != target_types:
                raise AssertionError("residual-type transport is not onto")
            for source_type in source_types:
                target_type = map_triangle_type(source_type, permutation)
                for descriptor in blind.aggregate_descriptors():
                    source_name = aggregate_name(descriptor)
                    target_name = transform_row_name(source_name, permutation)
                    if blind.aggregate_feature(descriptor, source_type) != blind.aggregate_feature(
                        aggregate_by_name[target_name], target_type
                    ):
                        raise AssertionError("aggregate column feature is not covariant")
                source_decompositions = filtered_decompositions(source_H, source_type)
                mapped = {
                    tuple(
                        sorted(
                            (rename_signature(signature, permutation) for signature in triple),
                            key=blind.encode_signature,
                        )
                    )
                    for triple in source_decompositions
                }
                target_decompositions = set(filtered_decompositions(target_H, target_type))
                if mapped != target_decompositions:
                    raise AssertionError("local decomposition transport is not bijective")
                pattern_checks += len(source_decompositions)

            for signature in source_signatures:
                mapped_signature = rename_signature(signature, permutation)
                for descriptor in blind.point_descriptors():
                    source_name = point_name(descriptor)
                    target_name = transform_row_name(source_name, permutation)
                    if blind.point_feature(descriptor, signature) != blind.point_feature(
                        point_by_name[target_name], mapped_signature
                    ):
                        raise AssertionError("point column feature is not covariant")
                if blind.star_count_multiplier(signature) != blind.star_count_multiplier(mapped_signature):
                    raise AssertionError("residual degree is not transport invariant")
                if blind.star_t_multiplier(signature) != blind.star_t_multiplier(mapped_signature):
                    raise AssertionError("incident-t demand is not transport invariant")

            transported: dict[str, int] = {}
            for name, value in source_coefficients.items():
                target_name = transform_row_name(name, permutation)
                if target_name in transported:
                    raise AssertionError("dual transport collided")
                transported[target_name] = value
            target_rhs = sum(transported.get(name, 0) * value for name, value in target_targets.items())
            if target_rhs != source_metrics["rhs"] or target_rhs >= 0:
                raise AssertionError("transported dual right-hand side differs")
            # The complete W/X column bijections and feature covariance above
            # prove that every transported column value equals its already
            # replayed representative value, so this is an exact replay under
            # an explicitly checked matrix isomorphism rather than a solver
            # inference.
            certificate_checks += 1
            branch_checks += 1
    if branch_checks != 51 or certificate_checks != 51 or pattern_checks != 601_377:
        raise AssertionError((branch_checks, certificate_checks, pattern_checks))
    return {
        "transported_branch_checks": branch_checks,
        "transported_dual_replays": certificate_checks,
        "transported_local_pattern_checks": pattern_checks,
        "target_automorphism_assumed": False,
    }


def hostile_tests(
    systems: dict[int, FilteredSystem], coefficient_maps: dict[int, dict[str, int]]
) -> dict[str, bool]:
    system = systems[0]
    coefficients = coefficient_maps[0]
    erased_rejected = False
    try:
        replay_named_dual(system, {})
    except AssertionError:
        erased_rejected = True
    reversed_rejected = False
    try:
        replay_named_dual(system, {name: -value for name, value in coefficients.items()})
    except AssertionError:
        reversed_rejected = True

    mutated_rhs = list(system.rhs)
    mutated_rhs[0] += 1
    rhs_mutation_rejected = filtered_hashes(replace(system, rhs=tuple(mutated_rhs))) != filtered_hashes(system)

    first = system.columns[0]
    entries = dict(first.entries)
    entries[min(entries)] += 1
    mutated_column = blind.SparseColumn(first.descriptor, tuple(sorted(entries.items())))
    columns = (mutated_column,) + system.columns[1:]
    column_mutation_rejected = filtered_hashes(replace(system, columns=columns)) != filtered_hashes(system)

    bad_permutation = (4, 1, 2, 3, 0, 5, 6, 7)
    map_mutation_rejected = any(
        blind.ALPHA[i] != blind.ALPHA[bad_permutation[i]] for i in range(8)
    )
    outcomes = {
        "erased_coefficients_rejected": erased_rejected,
        "reversed_dual_orientation_rejected": reversed_rejected,
        "rhs_mutation_rejected": rhs_mutation_rejected,
        "column_mutation_rejected": column_mutation_rejected,
        "sign_breaking_map_mutation_rejected": map_mutation_rejected,
    }
    if not all(outcomes.values()):
        raise AssertionError(outcomes)
    return outcomes


def build_result() -> dict[str, object]:
    seals = verify_seals()
    blind_duals = blind.replay_blind_duals()
    systems = {
        orbit_id: build_filtered_system(orbit_id)
        for orbit_id in blind.SURVIVING_ORBIT_IDS
    }
    source_comparison, _source = compare_source_matrices(systems)
    del _source
    relaxation = verify_relaxation_inclusion(systems)
    archive_replay, coefficient_maps = replay_source_duals(systems)
    transport = verify_transport(systems, coefficient_maps)
    hostile = hostile_tests(systems, coefficient_maps)
    return {
        "format": "wave212-rank4-full-coupling-post-source-v1",
        "role": "verifier",
        "claim_label": "VERIFIED",
        "verdict": "PASS_NO_VETO",
        "scope": "conditional exclusion of all seven Wave209 rank-four survivor orbits and all 51 labelled branches",
        "seals_and_manifests": seals,
        "independent_full_relaxation": {
            "exact_duals": blind_duals,
            "global_status": "UNKNOWN",
        },
        "membership_filtered_source_comparison": source_comparison,
        "relaxation_inclusion": relaxation,
        "archived_integer_dual_replay": archive_replay,
        "transport": transport,
        "hostile_tests": hostile,
        "target_automorphism_assumed": False,
        "rank_three_status": "UNKNOWN",
        "global_status": "UNKNOWN",
        "limitations": [
            "The verified exclusion is conditional on the frozen hypothetical endpoint and the verified Wave208/209 rank-four reduction.",
            "The rank-three survivor is not addressed by this verifier.",
            "No 99-vertex graph, unrestricted nonexistence proof, counterexample, or global resolution is certified.",
            "Conway-99 remains UNKNOWN.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULTS.write_text(rendered, encoding="utf-8", newline="\n")
    elif args.verify:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("post-source result archive differs")
        print("PASS: Wave212 rank-four full coupling post-source audit")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
