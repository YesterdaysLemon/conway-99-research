#!/usr/bin/env python3
"""Manifest-pinned comparison for the sealed Wave 208 proof-B package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = ROOT / "attempts" / "wave208-marked-m7g-proof-b"
MANIFEST = PACKAGE / "package-manifest.sha256"
INPUT_FREEZE = PACKAGE / "input-freeze.sha256"
SOURCE_RESULT = PACKAGE / "exact-results.json"
SOURCE_CODE = PACKAGE / "exact_check.py"
INDEPENDENT_RESULT = HERE / "proof-b-independent-results.json"
ARCHIVE = HERE / "proof-b-delta-audit.json"
EXPECTED_MANIFEST_SHA256 = "f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_hash_list(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})\s{2}(.+)", line)
        if match is None:
            raise AssertionError(f"malformed hash line: {line!r}")
        expected, relative = match.groups()
        if sha256(ROOT / relative) != expected:
            raise AssertionError(f"hash mismatch: {relative}")
        count += 1
    return count


def comparable_survivor(row: dict[str, object]) -> dict[str, object]:
    keys = (
        "diagonal",
        "rank",
        "signed_polar_sum",
        "residual_squared_norm",
        "divided_residual_squared_norm",
        "product_one_edges",
        "same_sign_product_one_edges",
        "accepted_labelled_intersection_subsets",
    )
    return {key: row[key] for key in keys}


def validate_source(
    source: dict[str, object], independent: dict[str, object]
) -> dict[str, object]:
    if source["claim_label"] != "DERIVED":
        raise AssertionError("discovery status is not DERIVED")
    exact_equalities = (
        "projective_linear_weight_eight_relation_classes",
        "projective_tensor_weight_eight_relation_classes",
        "wave207_no_product_one_forms",
        "additional_wave207_survivors_excluded",
        "signed_polar_sum_distribution",
        "minus24_intersection_profiles",
        "plus12_intersection_profiles",
    )
    for key in exact_equalities:
        if source[key] != independent[key]:
            raise AssertionError(f"source/independent mismatch: {key}")
    if source["restricted_polar_forms"] != 27:
        raise AssertionError("source omitted polar forms")
    if source["surviving_forms"] != len(independent["surviving_forms"]):
        raise AssertionError("surviving form count differs")
    if source["concurrent_secant_matchings_retained_without_choice"] != independent["concurrent_secant_matching_count"]:
        raise AssertionError("concurrent-secant count differs")
    if independent["relation_matching_objects_identified"]:
        raise AssertionError("linear words and secant matchings were conflated")
    source_relation = source["survivor_classes"][0]["relation"]
    if [source_relation] != independent["projective_tensor_weight_eight_relations"]:
        raise AssertionError("source used a non-tensor linear relation")

    source_survivors = sorted(
        (comparable_survivor(row) for row in source["survivor_classes"][0]["surviving_forms"]),
        key=lambda row: tuple(row["diagonal"]),
    )
    independent_survivors = [comparable_survivor(row) for row in independent["surviving_forms"]]
    if source_survivors != independent_survivors:
        raise AssertionError("survivor records differ")

    source_controls = {row["name"]: row for row in source["local_controls"]}
    independent_controls = {row["name"]: row for row in independent["local_controls"]}
    if source_controls.keys() != independent_controls.keys():
        raise AssertionError("local control list differs")
    control_keys = (
        "vertices",
        "edges",
        "selected_intersections",
        "point_weight",
        "integer_b_norm",
        "graph_triangles",
        "induced_triangular_prisms",
        "maximum_induced_degree",
        "exact_AUb_equals_3b",
        "lambda_mu_caps",
    )
    for name in source_controls:
        for key in control_keys:
            if source_controls[name][key] != independent_controls[name][key]:
                raise AssertionError(f"local control mismatch: {name}/{key}")
        if independent_controls[name]["full_outside_equation_implied"]:
            raise AssertionError("local control was promoted to a full equation")
        if independent_controls[name]["global_completion_implied"]:
            raise AssertionError("local control was promoted to a completion")
        if not independent_controls[name]["hostile_extension_preserves_upper_caps"]:
            raise AssertionError("outside hostile witness is absent")
        if independent_controls[name]["hostile_outside_row_dot_b"] == 0:
            raise AssertionError("outside hostile row does not violate M b=0")

    limitations = " ".join(source["limitations"])
    for phrase in ("outside completion", "no target graph", "Conway-99"):
        if phrase not in limitations:
            raise AssertionError(f"source status wall omits {phrase!r}")
    if independent["global_status"] != "UNKNOWN":
        raise AssertionError("independent global status inflated")

    code_text = SOURCE_CODE.read_text(encoding="utf-8")
    hardcoded = '"concurrent_secant_matchings_retained_without_choice": 4' in code_text
    return {
        "claim_label": "VERIFIED",
        "verified_scope": (
            "conditional marked-M7g proof-B reduction: exact spectral divisibility "
            "removes 19 of the 23 Wave207 survivors and leaves the same four forms"
        ),
        "manifest_sha256": sha256(MANIFEST),
        "manifest_entries_verified": verify_hash_list(MANIFEST),
        "input_freeze_entries_verified": verify_hash_list(INPUT_FREEZE),
        "spectral_verification": {
            "residual_eigenvalue": -4,
            "coordinate_divisor": 3,
            "norm": "7*(24-2*S_D)",
            "necessary_congruence": "S_D=3 mod 9",
        },
        "form_census": {
            "all_forms": 27,
            "wave207_survivors_before": 23,
            "newly_excluded": 19,
            "survivors": 4,
            "survivor_diagonals": [row["diagonal"] for row in independent["surviving_forms"]],
        },
        "marked_subset_census": {
            "rank4_subsets_per_form": 83,
            "rank3_weight20_subsets": independent["plus12_intersection_profiles"]["m2_same0_opposite2_w20_p10_n10_norm20"],
            "rank3_weight14_subsets": independent["plus12_intersection_profiles"]["m5_same0_opposite5_w14_p7_n7_norm14"],
            "rank3_support_weights": [14, 20],
        },
        "relation_matching_distinction": {
            "projective_linear_words": 4,
            "tensor_words": 1,
            "concurrent_secant_matchings": 4,
            "objects_identified": False,
            "all_105_perfect_matchings_independently_enumerated": True,
        },
        "source_coverage_finding": (
            "source exact_check.py hard-codes the concurrent-secant count; the "
            "clean-room verifier independently enumerates and verifies the four matchings"
            if hardcoded
            else "none"
        ),
        "local_control_verdict": {
            "controls_replayed": 2,
            "internal_necessary_equations_verified": True,
            "outside_row_counterwitnesses": 2,
            "outside_equations_implied": False,
            "global_completion_implied": False,
        },
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "global_status": "UNKNOWN",
    }


def build_result() -> dict[str, object]:
    if sha256(MANIFEST) != EXPECTED_MANIFEST_SHA256:
        raise AssertionError("proof-B manifest changed")
    source = json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))
    independent = json.loads(INDEPENDENT_RESULT.read_text(encoding="utf-8"))
    return validate_source(source, independent)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("proof-B delta audit archive differs")
        print("PASS: post-source Wave208 proof-B audit")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
