#!/usr/bin/env python3
"""Post-seal comparison for the Wave 208 M7g norm-divisibility package.

This checker reads archived JSON only.  It does not import discovery code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = ROOT / "attempts" / "wave208-m7g-norm-divisibility"
SOURCE_RESULT = PACKAGE / "exact-results.json"
INDEPENDENT_RESULT = HERE / "m7g-norm-independent-results.json"
ORIGINAL_AUDIT = HERE / "m7g-norm-post-source-audit.json"
ARCHIVE = HERE / "m7g-norm-post-correction-audit.json"
MANIFEST = PACKAGE / "package-manifest.sha256"
INPUT_FREEZE = PACKAGE / "input-freeze.sha256"
ORIGINAL_MANIFEST_SHA256 = "8d7088cf4bee7792ae22f75c4babbd114fe3aee7c1ca64a25fe33c04dac40373"
EXPECTED_MANIFEST_SHA256 = "a633dff62e4e1127b8a0c7329928e110d1fef1e78f1f322bbc4e250e277167f3"


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
            raise AssertionError(f"malformed hash line in {path.name}: {line!r}")
        expected, relative = match.groups()
        target = ROOT / Path(relative)
        if sha256(target) != expected:
            raise AssertionError(f"hash mismatch: {relative}")
        count += 1
    return count


def survivor_counter(rows: list[dict[str, object]]) -> Counter[tuple[object, ...]]:
    return Counter(
        (row["rank"], row["zero_graph"], row["d"], row["base_norm"])
        for row in rows
    )


def validate_source(
    source: dict[str, object], independent: dict[str, object]
) -> dict[str, object]:
    if source["global_status"] != "UNKNOWN":
        raise AssertionError("source inflated the global status")
    if source["claim_label"] != "DERIVED":
        raise AssertionError("source package must remain DERIVED before audit")
    m7g = source["m7g"]
    if m7g["integer_lift"] != independent["integer_lift"]:
        raise AssertionError("integer lifts differ")
    if m7g["integer_lift_sum"] != 0:
        raise AssertionError("integer lift is not balanced")
    if m7g["relative_sign_classes"] != independent["relative_orientation_count"]:
        raise AssertionError("orientation count differs")
    if m7g["affine_polar_forms_per_class"] != independent["affine_forms_per_orientation"]:
        raise AssertionError("affine-form count differs")
    if source["summary"]["eliminated_per_orientation"] != 23:
        raise AssertionError("source did not exclude exactly 23 forms")
    if source["summary"]["survivors_per_orientation"] != 4:
        raise AssertionError("source did not retain exactly four forms")

    source_classes = source["classes"]
    independent_classes = independent["orientation_classes"]
    if len(source_classes) != len(independent_classes):
        raise AssertionError("orientation class list differs")
    expected_survivors = Counter({(3, "4K2", 12, 216): 1, (4, "2C4", -24, 288): 3})
    for source_class, independent_class in zip(source_classes, independent_classes):
        if source_class["signs"] != independent_class["signs"]:
            raise AssertionError("orientation signs differ")
        normalized = {
            key.replace("_rem", "_remainder"): value
            for key, value in source_class["distribution"].items()
        }
        if normalized != independent_class["distribution"]:
            raise AssertionError("rank/remainder distribution differs")
        if survivor_counter(source_class["surviving_forms"]) != expected_survivors:
            raise AssertionError("source survivor types differ")
        if survivor_counter(independent_class["survivors"]) != expected_survivors:
            raise AssertionError("independent survivor types differ")

    if independent["forms_excluded_per_orientation"] != 23:
        raise AssertionError("clean-room exclusion count differs")
    if independent["forms_surviving_per_orientation"] != 4:
        raise AssertionError("clean-room survivor count differs")
    if independent["product_one_interpretation_fixed"]:
        raise AssertionError("product-one ambiguity was silently resolved")
    if independent["complete_graph_certificate"] or independent["complete_nonexistence_certificate"]:
        raise AssertionError("unsupported terminal certificate")

    return {
        "claim_label": "VERIFIED",
        "verified_scope": (
            "conditional prism-free M7g branch: the exact mod-nine norm condition "
            "excludes 23 of 27 labelled polar forms in each of four orientations"
        ),
        "manifest_sha256": sha256(MANIFEST),
        "manifest_entries_verified": verify_hash_list(MANIFEST),
        "input_freeze_entries_verified": verify_hash_list(INPUT_FREEZE),
        "clean_room_agreement": {
            "relative_orientations": 4,
            "affine_forms_per_orientation": 27,
            "excluded_per_orientation": 23,
            "survivors_per_orientation": 4,
            "rank3_4K2_survivors_total": independent["survivor_type_totals"]["rank3_4K2_d12_base216"],
            "rank4_2C4_survivors_total": independent["survivor_type_totals"]["rank4_2C4_d-24_base288"],
        },
        "hostile_boundaries": {
            "literal_plus_minus_one_lift_required": True,
            "product_one_interpretation_fixed": False,
            "intersection_sum_reconstructed": False,
            "outside_completion_supplied": False,
            "complete_graph_certificate": False,
            "complete_nonexistence_certificate": False,
        },
        "documentation_finding": (
            "derivation.md says 'other 91 vertices', but eight triangle columns are not "
            "eight graph vertices and no union size is fixed; the outside count is unsupported"
        ),
        "global_status": "UNKNOWN",
    }


def build_result() -> dict[str, object]:
    if sha256(MANIFEST) != EXPECTED_MANIFEST_SHA256:
        raise AssertionError("sealed package-manifest hash changed")
    source = json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))
    independent = json.loads(INDEPENDENT_RESULT.read_text(encoding="utf-8"))
    result = validate_source(source, independent)
    original = json.loads(ORIGINAL_AUDIT.read_text(encoding="utf-8"))
    if original["manifest_sha256"] != ORIGINAL_MANIFEST_SHA256:
        raise AssertionError("original documentation finding is not preserved")
    derivation = (PACKAGE / "derivation.md").read_text(encoding="utf-8")
    if "other 91 vertices" in derivation:
        raise AssertionError("original outside-count error remains")
    corrected = "vertices outside the selected-triangle\nunion, whose size is not fixed here"
    if corrected not in derivation:
        raise AssertionError("outside-scope correction is absent")
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    unchanged_hashes = {
        "attempts/wave208-m7g-norm-divisibility/exact_check.py": "4e34ec62a575aba41a2c5f276e1eb6d9186caba055336e3f39523270503be7af",
        "attempts/wave208-m7g-norm-divisibility/exact-results.json": "ea3481c805a88d233f9e35f1c9e9c61e8546e7f6ddb56add2e552b9a80ec3703",
        "attempts/wave208-m7g-norm-divisibility/test_exact_check.py": "2d6f63a8d3eefb37c7d4dc174536ec669d9a252185a22720e60c4396fb865c9f",
    }
    for relative, digest in unchanged_hashes.items():
        if f"{digest}  {relative}" not in manifest_text:
            raise AssertionError(f"computational artifact changed: {relative}")
    result.pop("documentation_finding")
    result["documentation_history"] = {
        "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
        "original_finding": original["documentation_finding"],
        "corrected_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "correction_verified": (
            "derivation now states that the selected-triangle union size is not fixed"
        ),
        "changed_document_hashes": {
            "derivation.md": {
                "old": "a56c075c1e0fd4c5129dfbf3fabc11b3264f62abb4fe144039fda3a13a16532c",
                "new": "2c480d92d0c9f47d2425b3a0aef0e02d2dd89be27404877f46910395699b46f7",
            },
            "run-report.yaml": {
                "old": "12a3d6c553ad770b4671e756c2791f7a56b00e8cd20f80cdef39d8cecced4ab6",
                "new": "77d8ea6954e5cb262d4df830dc1216cb6fa3795c9b45a06ec81cb911674e18bc",
            },
            "agents/2026-07-31-wave208-m7g-norm-divisibility.md": {
                "old": "00a44e05201c040cb537cfb0b28d5d314b0fa2bc5046ff5b0c53aac934b8ad9b",
                "new": "92680a0fd429e1e257dd60c6aeb5780f5aa3c0bbb7e36b7307f095da885c0c4f",
            },
        },
        "computational_artifacts_unchanged": True,
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
            raise AssertionError("post-source M7g audit archive differs")
        print("PASS: post-source Wave208 M7g audit")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
