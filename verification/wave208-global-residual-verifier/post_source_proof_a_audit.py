#!/usr/bin/env python3
"""Manifest-pinned comparison for sealed Wave 208 proof A."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import independent_proof_a as independent_code  # noqa: E402

PACKAGE = ROOT / "attempts" / "wave208-integer-lift-proof-a"
MANIFEST = PACKAGE / "package-manifest.sha256"
INPUT_FREEZE = PACKAGE / "input-freeze.sha256"
SOURCE_RESULT = PACKAGE / "exact-results.json"
SOURCE_CODE = PACKAGE / "exact_check.py"
INDEPENDENT_RESULT = HERE / "proof-a-independent-results.json"
ARCHIVE = HERE / "proof-a-delta-audit.json"
EXPECTED_MANIFEST_SHA256 = "28d69162a8f52bdc325471946efecad890b1edac33f3576bdba8777e32887202"
WAVE94_AUDIT = ROOT / "verification" / "wave94-general-n3-norm14-bound" / "audit.md"
EXPECTED_WAVE94_AUDIT_SHA256 = "ab87d369345a27abb4326915f6c392545573780b4fc7f5d67bc494743c4a2ce6"


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


def validate_source(
    source: dict[str, object], clean: dict[str, object]
) -> dict[str, object]:
    if source["claim_label"] != "DERIVED_PARTIAL_WITH_UNKNOWN_WALL":
        raise AssertionError("source result status changed")
    spectral = source["spectral_split"]
    expected_spectral = {
        "Q": clean["spectral_split"]["Q"],
        "Q_equation": f"A*Q={clean['spectral_split']['AQ']}",
        "Q_sum": clean["spectral_split"]["sum_Q"],
        "Q_squared": clean["spectral_split"]["Q_squared"],
        "Q_coordinate_residue_mod_9": clean["spectral_split"]["Q_coordinate_residue_mod9"],
        "R": clean["spectral_split"]["R"],
        "R_equation": f"A*R={clean['spectral_split']['AR']}",
        "R_sum": clean["spectral_split"]["sum_R"],
        "R_squared": clean["spectral_split"]["R_squared"],
    }
    for key, expected in expected_spectral.items():
        if spectral[key] != expected:
            raise AssertionError(f"spectral identity differs: {key}")

    if source["residue_shell_quantization"]["weights"] != independent_code.residue_shell_table():
        raise AssertionError("full residue-shell table differs")
    balanced = source["balanced_weight14"]
    if balanced["spectral_shells"]["rows"] != clean["balanced_weight14_shells"]:
        raise AssertionError("balanced q-squared shells differ")
    source_zero = balanced["zero_q_three_eigen_branch"]
    if source_zero["restricted_edge_cap_on_support"] != clean["zero_q_branch"]["restricted_edge_cap_on_support"]:
        raise AssertionError("q=0 support edge cap differs")
    if source_zero["rows"] != clean["zero_q_branch"]["rows"]:
        raise AssertionError("q=0 branch rows differ")

    source_capacity = {
        key: {
            "labelled_assignments": value["labelled_assignments"],
            "outside_token_capacity_survivors": value["outside_token_capacity_survivors"],
        }
        for key, value in balanced["norm14_q_overlap_capacity"].items()
    }
    if source_capacity != clean["norm14_overlap"]["capacity"]:
        raise AssertionError("Fano capacity census differs")
    source_patterns = [
        {
            "counts": row["counts_and_deficits"][0],
            "left_deficits": row["counts_and_deficits"][1],
            "right_deficits": row["counts_and_deficits"][2],
            "multiplicity": row["multiplicity"],
        }
        for row in balanced["same_overlap_one_coupled_exclusion"]["two_sign_symmetric_patterns"]
    ]
    if source_patterns != clean["norm14_overlap"]["alpha_one_patterns"]:
        raise AssertionError("alpha=1 patterns differ")
    if balanced["same_overlap_one_coupled_exclusion"]["required_negative_endpoints_on_demand_side"] != 4:
        raise AssertionError("alpha=1 required endpoint count differs")
    if balanced["same_overlap_one_coupled_exclusion"]["maximum_negative_endpoints_on_other_side"] != 3:
        raise AssertionError("alpha=1 endpoint capacity differs")
    derived = balanced["derived_overlap_conclusion"]
    clean_derived = clean["norm14_overlap"]["derived"]
    for key in ("same_sign_overlap", "opposite_sign_overlap", "support_union_size"):
        if derived[key] != clean_derived[key]:
            raise AssertionError(f"derived overlap differs: {key}")
    if derived["z_profile"] != "eight +1, eight -1, all other coordinates zero":
        raise AssertionError("z profile differs")

    shapes = balanced["exclusive_graph_shapes"]
    if shapes["universal_bound"] != [2, 4]:
        raise AssertionError("exclusive k bound differs")
    if shapes["k_2"]["smaller_side"] != clean["exclusive_shapes"]["k2_smaller_side"]:
        raise AssertionError("k=2 shape differs")
    if shapes["k_3"]["positive_side"] != "C4" or shapes["k_3"]["negative_side"] != "C4":
        raise AssertionError("k=3 C4 shape differs")
    if shapes["k_3"]["cross_edges"] != 0 or shapes["k_3"]["labelled_C4_survivors"] != 3:
        raise AssertionError("k=3 exact census differs")
    if shapes["k_4"]["smaller_side"] != clean["exclusive_shapes"]["k4_smaller_side"]:
        raise AssertionError("k=4 shape differs")

    source_control = source["hostile_partial_control"]
    clean_control = clean["hostile_partial_control"]
    if source_control["edge_count"] != clean_control["edges"]:
        raise AssertionError("partial-control edge count differs")
    if source_control["degree_multiset"] != clean_control["degree_multiset"]:
        raise AssertionError("partial-control degrees differ")
    if not source_control["pair_common_neighbor_caps_hold"]:
        raise AssertionError("source control fails its upper caps")
    if clean_control["full_outside_equations_implied"] or clean_control["global_completion_implied"]:
        raise AssertionError("partial control was promoted beyond scope")
    if not clean_control["hostile_extension_preserves_upper_caps"]:
        raise AssertionError("outside hostile witness is absent")
    if clean_control["hostile_outside_Ax_residual"] == 0 or clean_control["hostile_outside_Az_residual"] == 0:
        raise AssertionError("outside hostile witness does not violate the lift")

    conclusions = source["conclusions"]
    if conclusions["balanced_weight14_excluded"] or conclusions["weights_17_20_23_excluded"]:
        raise AssertionError("source claims a weight exclusion")
    if conclusions["rank11_endpoint"] != "UNKNOWN" or conclusions["conway_99"] != "UNKNOWN":
        raise AssertionError("source terminal status inflated")
    if any(clean["weights_excluded"].values()) or clean["global_status"] != "UNKNOWN":
        raise AssertionError("clean-room status inflated")

    code_text = SOURCE_CODE.read_text(encoding="utf-8")
    coefficient_literals = 'aq = {"x": 36, "z": -36, "one_t": 4}' in code_text
    sample_norms = "for w, t, h in ((14, 0, 8)" in code_text
    return {
        "claim_label": "VERIFIED",
        "verified_scope": (
            "conditional proof-A integer lift, residue shells, q=0 reduction, "
            "and norm-14 complementary-Fano alpha=0 reduction"
        ),
        "manifest_sha256": sha256(MANIFEST),
        "manifest_entries_verified": verify_hash_list(MANIFEST),
        "input_freeze_entries_verified": verify_hash_list(INPUT_FREEZE),
        "wave94_import": {
            "audit_sha256": sha256(WAVE94_AUDIT),
            "expected_sha256": EXPECTED_WAVE94_AUDIT_SHA256,
            "complementary_fano_design_reconstructed": True,
            "outside_profile": "70 meet one of each sign; 15 meet neither",
        },
        "spectral_and_shells": {
            "all_identities_verified": True,
            "balanced_q_squared": [row["q_squared"] for row in clean["balanced_weight14_shells"]],
            "full_residue_table_sha256": clean["residue_shell_quantization"]["canonical_table_sha256"],
            "all_weight_17_20_23_compositions_retained": True,
        },
        "q_zero_reduction": {
            "e13_excluded": True,
            "e12_excluded": True,
            "surviving_cross_edges": 1,
            "surviving_degree_sequence_each_side": clean["zero_q_branch"]["surviving_degree_sequence_each_side"],
        },
        "norm14_overlap_reduction": {
            "capacity_counts": clean["norm14_overlap"]["capacity"],
            "alpha_one_rows_before_coupling": 42,
            "required_endpoints": 4,
            "maximum_endpoints": 3,
            **clean["norm14_overlap"]["derived"],
            "k_values": clean["exclusive_shapes"]["k_values"],
        },
        "partial_control_verdict": {
            "vertices": 22,
            "internal_lift_equations_verified": True,
            "outside_row_counterwitnesses": 1,
            "outside_equations_implied": False,
            "global_completion_implied": False,
        },
        "source_coverage_findings": [
            "source spectral checker compares precomputed coefficient literals and tests norm formulas on four samples; clean-room symbolic expansion verifies the general identities"
            if coefficient_literals and sample_norms
            else "none"
        ],
        "weights_excluded": {"14": False, "17": False, "20": False, "23": False},
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "rank11_endpoint": "UNKNOWN",
        "global_status": "UNKNOWN",
    }


def build_result() -> dict[str, object]:
    if sha256(MANIFEST) != EXPECTED_MANIFEST_SHA256:
        raise AssertionError("proof-A manifest changed")
    if sha256(WAVE94_AUDIT) != EXPECTED_WAVE94_AUDIT_SHA256:
        raise AssertionError("imported Wave94 audit changed")
    source = json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))
    clean = json.loads(INDEPENDENT_RESULT.read_text(encoding="utf-8"))
    return validate_source(source, clean)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("proof-A delta audit archive differs")
        print("PASS: post-source Wave208 proof-A audit")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
