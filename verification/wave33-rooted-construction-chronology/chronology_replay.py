#!/usr/bin/env python3
"""Replay the frozen Wave 33 construction packages in their historical inputs.

The discovery and verifier packages were correctly frozen before the central
``STRUCTURE.md`` received its Wave 33 integration section.  Their original
input ledgers therefore must not be interpreted as assertions about mutable
central-document bytes in the later publication tree.

This module authenticates an immutable content-addressed snapshot of all eight
historical inputs, materializes a temporary synthetic repository, copies only
hash-accepted candidate/verifier/solver-provenance bytes into it, and runs the
unchanged 14 discovery and 37 verifier tests there.  Nothing is imported from
the discovery package into this module.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ARCHIVE = HERE / "historical-inputs.json"

HISTORICAL_STRUCTURE_SHA256 = (
    "45640fecaa5834b24063c682c7edd0898f2746253a7708a2c70c3610e4bcb99a"
)
EXPECTED_ARCHIVE_SHA256 = (
    "d62fc4311577d56cbf34f8bd4e63aefb3b796457b3d020f4322324073d82f7dd"
)

CANDIDATE_FREEZE = (
    REPO / "verification" / "wave33-rooted-construction-candidate-freeze.sha256"
)
CANDIDATE_FREEZE_SHA256 = (
    "441465c157f28e658afde31e6ca0cff49ccb5841a001150bd3e3af616c5bf63a"
)
CANDIDATE_ARTIFACT = (
    REPO / "attempts" / "wave33-rooted-construction" / "artifact-manifest.sha256"
)
CANDIDATE_ARTIFACT_SHA256 = (
    "0cd192c0182506b3c901806cc96abb9fe53f04dc906b0b5cd73bc9b602558ff4"
)
VERIFIER_DIR = REPO / "verification" / "wave33-rooted-construction"
VERIFIER_ARTIFACT = VERIFIER_DIR / "artifact-manifest.sha256"
VERIFIER_ARTIFACT_SHA256 = (
    "20c27560bdf9720cd1cf043b11c218130cd2891a2d3c874f9dbc9bce2f27fbbf"
)
PRECOMPARISON_MANIFEST_SHA256 = (
    "4ccbbad9c01eab764d9aa6fb207114e43f8c5a36bec3ec5bf0d161708ce0360d"
)

EXPECTED_EXACT_RESULTS_SHA256 = (
    "ba6640eacd041bc8349024a1d3f13e3d74bd67cdad64d2d78c9a94927319c496"
)
EXPECTED_COMPARISON_RESULTS_SHA256 = (
    "c0476fb877e0e7d6a6fc63b1a4c72bda0d7804a18a4e4b2b6d5a1bcbc4b6b459"
)
EXPECTED_COMPARISON_CLI_STDOUT_SHA256 = (
    "7025cc30551e219c224fe068d641a202db9f1c7a39e480908933e9a93fe597c5"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "340e5df716ad63bceba25c745ab04c22ea1a3dca01e939072f09775a5fc5f634"
)

HISTORICAL_INPUTS = {
    "AGENTS.md":
        "4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3",
    "CONJECTURE.md":
        "7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58",
    "STRUCTURE.md": HISTORICAL_STRUCTURE_SHA256,
    "agents/2026-07-24-wave32-rooted-proof.md":
        "04990231e3b42cded363e39ffea771556e52ec66fe03a97164ae99f40ddbefe0",
    "verification/wave32-rooted-vector/audit.md":
        "36d83232d82e30205e0aefa30aedff0a517de1edb0adbaa54575ea68d04ce1a5",
    "verification/wave32-rooted-vector/independent-results.json":
        "4ed239e997e4485abdab4e26a2e28e2a981b6fff069c4d926ccff3d2241dbe6f",
    "verification/wave32-rooted-vector/artifact-manifest.sha256":
        "2607c3000944e6d31ab5491a7d959ae4f97f05ac3e0d754baaf2830efcd085df",
    "verification/wave33-continuation-protocol.md":
        "b98b6bb8228b54b67cd949ee1bf6eb05ebd6ebe74f1cbc9e49b041a55e2d2fe6",
}

SOLVER_PROVENANCE = {
    ".venv/Lib/site-packages/pysat/card.py":
        "adabf7fedfe60b36cbc3c48075770e87e3cd6c5b5a013552009ce96f282a890e",
    ".venv/Lib/site-packages/pysat/solvers.py":
        "253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e",
    ".venv/Lib/site-packages/pysolvers.cp313-win_amd64.pyd":
        "1019bacdbb9400cc54fa89aa39294fefe1c63d5a67fdab35f473364529ec72dd",
    ".venv/Lib/site-packages/scipy/optimize/_milp.py":
        "803785ebcc365d1c04967a267650953da01ed285ee8be1c7a66a9fe3dbf75c3c",
    ".venv/Lib/site-packages/scipy/optimize/_highspy/_core.cp313-win_amd64.pyd":
        "92d47727b06333f871f57427a6d9800481e3e9feeabd59d31320ded8028c5357",
    ".venv/Lib/site-packages/scipy/optimize/_highspy/"
    "_highs_options.cp313-win_amd64.pyd":
        "df51a5cdf24f3ff1f06f36ef25c88b0ea41c496f8f7e12bfd40ca840f56d30a5",
}

MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")
WAVE33_STRUCTURE_START = (
    b"## Wave 33 finite rooted extension and rootless contraction wall\n"
)
POST_WAVE33_STRUCTURE_MARKER = b"Each of the two central diagonal nonedges"


class ChronologyError(RuntimeError):
    """Raised when a frozen chronology or isolated replay gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ChronologyError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True)
        .encode("utf-8")
        + b"\n"
    )


def reject_duplicate_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def safe_repo_relative(raw: str) -> PurePosixPath:
    require("\\" not in raw, f"manifest path must use forward slashes: {raw}")
    relative = PurePosixPath(raw)
    require(not relative.is_absolute(), f"absolute manifest path: {raw}")
    require(
        relative.parts
        and all(part not in ("", ".", "..") for part in relative.parts),
        f"escaping or empty manifest path: {raw}",
    )
    return relative


def parse_manifest_bytes(
    data: bytes,
    *,
    label: str,
    expected_sha256: str | None = None,
) -> dict[str, str]:
    if expected_sha256 is not None:
        require(
            sha256_bytes(data) == expected_sha256,
            f"{label}: manifest byte hash mismatch",
        )
    require(data.endswith(b"\n"), f"{label}: missing terminal LF")
    require(b"\r" not in data and b"\0" not in data, f"{label}: invalid bytes")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChronologyError(f"{label}: invalid UTF-8") from exc
    entries: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = MANIFEST_LINE.fullmatch(line)
        require(match is not None, f"{label}: malformed line {line_number}")
        expected, raw = match.groups()
        safe_repo_relative(raw)
        require(raw not in entries, f"{label}: duplicate path: {raw}")
        entries[raw] = expected
    require(entries, f"{label}: empty manifest")
    return entries


def require_regular_source(path: Path, *, label: str) -> None:
    require(path.exists(), f"{label}: missing file")
    require(path.is_file(), f"{label}: not a regular file")
    require(not path.is_symlink(), f"{label}: symlink is forbidden")


def validate_manifest(
    path: Path,
    *,
    base: Path,
    expected_sha256: str,
) -> dict[str, str]:
    require_regular_source(path, label=str(path))
    entries = parse_manifest_bytes(
        path.read_bytes(), label=str(path), expected_sha256=expected_sha256
    )
    base_resolved = base.resolve()
    for raw, expected in entries.items():
        relative = safe_repo_relative(raw)
        target = base.joinpath(*relative.parts)
        require_regular_source(target, label=f"{path}:{raw}")
        resolved = target.resolve()
        require(
            resolved == base_resolved or base_resolved in resolved.parents,
            f"{path}: resolved path escapes base: {raw}",
        )
        require(
            sha256_path(target) == expected,
            f"{path}: entry hash mismatch: {raw}",
        )
    return entries


def historical_structure_bytes(current: bytes) -> bytes:
    if sha256_bytes(current) == HISTORICAL_STRUCTURE_SHA256:
        return current
    require(
        WAVE33_STRUCTURE_START in current,
        "integrated STRUCTURE.md lacks the Wave 33 insertion marker",
    )
    start = current.index(WAVE33_STRUCTURE_START)
    require(
        POST_WAVE33_STRUCTURE_MARKER in current[start:],
        "integrated STRUCTURE.md lacks the post-insertion marker",
    )
    end = current.index(POST_WAVE33_STRUCTURE_MARKER, start)
    recovered = current[:start] + current[end:]
    require(
        sha256_bytes(recovered) == HISTORICAL_STRUCTURE_SHA256,
        "recovered historical STRUCTURE.md hash mismatch",
    )
    return recovered


def build_archive_payload(source_root: Path = REPO) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for relative, expected in sorted(HISTORICAL_INPUTS.items()):
        source = source_root / relative
        require_regular_source(source, label=f"archive source {relative}")
        data = source.read_bytes()
        if relative == "STRUCTURE.md":
            data = historical_structure_bytes(data)
        require(
            sha256_bytes(data) == expected,
            f"archive source hash mismatch: {relative}",
        )
        compressed = zlib.compress(data, level=9)
        entries.append(
            {
                "path": relative,
                "sha256": expected,
                "size": len(data),
                "encoding": "zlib+base85",
                "payload": base64.b85encode(compressed).decode("ascii"),
            }
        )
    return {
        "schema_version": 1,
        "evidence_kind": "IMMUTABLE_HISTORICAL_INPUT_SNAPSHOT",
        "scope": (
            "The eight exact inputs named by the frozen construction input "
            "ledger and continuation addendum; no current central bytes."
        ),
        "entries": entries,
    }


def decode_archive_bytes(
    raw: bytes,
    *,
    expected_archive_sha256: str | None = EXPECTED_ARCHIVE_SHA256,
) -> dict[str, bytes]:
    if expected_archive_sha256 is not None:
        require(
            sha256_bytes(raw) == expected_archive_sha256,
            "historical archive byte hash mismatch",
        )
    try:
        value = json.loads(raw, object_pairs_hook=reject_duplicate_json_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ChronologyError("historical archive is not strict JSON") from exc
    require(isinstance(value, dict), "archive must be an object")
    require(
        set(value) == {"schema_version", "evidence_kind", "scope", "entries"},
        "archive top-level schema drift",
    )
    require(value["schema_version"] == 1, "archive schema_version drift")
    require(
        value["evidence_kind"] == "IMMUTABLE_HISTORICAL_INPUT_SNAPSHOT",
        "archive evidence_kind drift",
    )
    rows = value["entries"]
    require(isinstance(rows, list), "archive entries must be a list")
    decoded: dict[str, bytes] = {}
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"archive entry {index} must be an object")
        require(
            set(row) == {"path", "sha256", "size", "encoding", "payload"},
            f"archive entry {index} schema drift",
        )
        path = row["path"]
        require(isinstance(path, str), f"archive entry {index} path type")
        safe_repo_relative(path)
        require(path not in decoded, f"archive duplicate path: {path}")
        require(row["encoding"] == "zlib+base85", f"archive codec drift: {path}")
        require(
            isinstance(row["sha256"], str)
            and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
            f"archive hash syntax: {path}",
        )
        require(
            isinstance(row["size"], int)
            and not isinstance(row["size"], bool)
            and row["size"] >= 0,
            f"archive size type: {path}",
        )
        require(isinstance(row["payload"], str), f"archive payload type: {path}")
        try:
            data = zlib.decompress(base64.b85decode(row["payload"].encode("ascii")))
        except (UnicodeEncodeError, ValueError, zlib.error) as exc:
            raise ChronologyError(f"archive payload decode failed: {path}") from exc
        require(len(data) == row["size"], f"archive size mismatch: {path}")
        require(
            sha256_bytes(data) == row["sha256"],
            f"archive entry hash mismatch: {path}",
        )
        decoded[path] = data
    require(
        {path: sha256_bytes(data) for path, data in decoded.items()}
        == HISTORICAL_INPUTS,
        "archive path/hash map differs from frozen input ledgers",
    )
    return decoded


def write_exact(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def copy_hash_accepted(
    source: Path,
    destination: Path,
    *,
    expected_sha256: str,
    label: str,
) -> None:
    require_regular_source(source, label=label)
    require(sha256_path(source) == expected_sha256, f"{label}: hash mismatch")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination, follow_symlinks=False)
    require(
        sha256_path(destination) == expected_sha256,
        f"{label}: copied-byte hash mismatch",
    )


def validate_frozen_packages(source_root: Path = REPO) -> dict[str, Any]:
    candidate_freeze = (
        source_root
        / "verification"
        / "wave33-rooted-construction-candidate-freeze.sha256"
    )
    candidate_artifact = (
        source_root
        / "attempts"
        / "wave33-rooted-construction"
        / "artifact-manifest.sha256"
    )
    verifier_dir = (
        source_root / "verification" / "wave33-rooted-construction"
    )
    verifier_artifact = verifier_dir / "artifact-manifest.sha256"

    candidate_entries = validate_manifest(
        candidate_freeze,
        base=source_root,
        expected_sha256=CANDIDATE_FREEZE_SHA256,
    )
    require(len(candidate_entries) == 17, "candidate freeze entry count drift")
    candidate_artifact_entries = validate_manifest(
        candidate_artifact,
        base=source_root,
        expected_sha256=CANDIDATE_ARTIFACT_SHA256,
    )
    require(
        len(candidate_artifact_entries) == 16,
        "candidate artifact entry count drift",
    )
    nested = dict(candidate_entries)
    nested_manifest_hash = nested.pop(
        "attempts/wave33-rooted-construction/artifact-manifest.sha256",
        None,
    )
    require(
        nested_manifest_hash == CANDIDATE_ARTIFACT_SHA256,
        "candidate freeze does not bind the nested artifact manifest",
    )
    require(
        nested == candidate_artifact_entries,
        "candidate freeze and artifact entries disagree",
    )

    verifier_entries = validate_manifest(
        verifier_artifact,
        base=verifier_dir,
        expected_sha256=VERIFIER_ARTIFACT_SHA256,
    )
    require(len(verifier_entries) == 14, "verifier artifact entry count drift")
    precomparison = verifier_dir / "precomparison-freeze.sha256"
    precomparison_entries = validate_manifest(
        precomparison,
        base=verifier_dir,
        expected_sha256=PRECOMPARISON_MANIFEST_SHA256,
    )
    require(
        len(precomparison_entries) == 5,
        "precomparison manifest entry count drift",
    )
    return {
        "candidate_entries": candidate_entries,
        "candidate_artifact_entries": candidate_artifact_entries,
        "verifier_entries": verifier_entries,
        "precomparison_entries": precomparison_entries,
    }


def materialize_historical_root(
    destination: Path,
    *,
    source_root: Path = REPO,
    archive_path: Path = ARCHIVE,
) -> dict[str, Any]:
    require(not destination.exists(), "synthetic root must not already exist")
    destination.mkdir(parents=True)
    archive_bytes = archive_path.read_bytes()
    historical = decode_archive_bytes(archive_bytes)
    frozen = validate_frozen_packages(source_root)

    for relative, data in historical.items():
        write_exact(destination.joinpath(*PurePosixPath(relative).parts), data)

    for relative, expected in frozen["candidate_entries"].items():
        source = source_root.joinpath(*PurePosixPath(relative).parts)
        target = destination.joinpath(*PurePosixPath(relative).parts)
        copy_hash_accepted(
            source, target, expected_sha256=expected, label=f"candidate {relative}"
        )

    verifier_source = (
        source_root / "verification" / "wave33-rooted-construction"
    )
    verifier_destination = (
        destination / "verification" / "wave33-rooted-construction"
    )
    for relative, expected in frozen["verifier_entries"].items():
        copy_hash_accepted(
            verifier_source.joinpath(*PurePosixPath(relative).parts),
            verifier_destination.joinpath(*PurePosixPath(relative).parts),
            expected_sha256=expected,
            label=f"verifier {relative}",
        )

    copy_hash_accepted(
        source_root
        / "verification"
        / "wave33-rooted-construction-candidate-freeze.sha256",
        destination
        / "verification"
        / "wave33-rooted-construction-candidate-freeze.sha256",
        expected_sha256=CANDIDATE_FREEZE_SHA256,
        label="candidate freeze",
    )

    for relative, expected in SOLVER_PROVENANCE.items():
        copy_hash_accepted(
            source_root.joinpath(*PurePosixPath(relative).parts),
            destination.joinpath(*PurePosixPath(relative).parts),
            expected_sha256=expected,
            label=f"solver provenance {relative}",
        )

    require(
        sha256_path(destination / "STRUCTURE.md")
        == HISTORICAL_STRUCTURE_SHA256,
        "synthetic root did not receive historical STRUCTURE.md",
    )
    return {
        "historical_input_count": len(historical),
        "candidate_freeze_entries": len(frozen["candidate_entries"]),
        "candidate_artifact_entries": len(frozen["candidate_artifact_entries"]),
        "verifier_artifact_entries": len(frozen["verifier_entries"]),
        "precomparison_entries": len(frozen["precomparison_entries"]),
        "solver_provenance_files": len(SOLVER_PROVENANCE),
    }


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            snapshot[relative] = sha256_path(path)
    return snapshot


def run_process(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
) -> subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stdout = completed.stdout.decode("utf-8", errors="replace")[-2000:]
        stderr = completed.stderr.decode("utf-8", errors="replace")[-4000:]
        raise ChronologyError(
            f"subprocess failed ({completed.returncode}): {command}\n"
            f"stdout tail:\n{stdout}\nstderr tail:\n{stderr}"
        )
    return completed


def unittest_count(completed: subprocess.CompletedProcess[bytes]) -> int:
    combined = completed.stdout + b"\n" + completed.stderr
    matches = re.findall(rb"Ran ([0-9]+) tests?", combined)
    require(len(matches) == 1, "could not determine exact unittest count")
    return int(matches[0])


def assert_status_wall(payload: Any) -> None:
    require(isinstance(payload, dict), "comparison result must be an object")
    wall = payload.get("status_wall")
    require(isinstance(wall, dict), "comparison status wall missing")
    expected = {
        "complete_graph_extension": "UNKNOWN",
        "complete_domain_UNSAT_certificate": "NONE",
        "full_rooted_endpoint": "UNKNOWN",
        "n3_708": "UNKNOWN",
        "Conway_99": "UNKNOWN",
        "novelty": "UNKNOWN",
        "timeout_negative_evidence": False,
    }
    require(wall == expected, "comparison status wall drift or promotion")


def run_full_replay(*, source_root: Path = REPO) -> dict[str, Any]:
    source_before = {
        "candidate_freeze": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction-candidate-freeze.sha256"
        ),
        "candidate_artifact": sha256_path(
            source_root
            / "attempts"
            / "wave33-rooted-construction"
            / "artifact-manifest.sha256"
        ),
        "verifier_artifact": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction"
            / "artifact-manifest.sha256"
        ),
        "precomparison": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction"
            / "precomparison-freeze.sha256"
        ),
    }
    require(
        source_before
        == {
            "candidate_freeze": CANDIDATE_FREEZE_SHA256,
            "candidate_artifact": CANDIDATE_ARTIFACT_SHA256,
            "verifier_artifact": VERIFIER_ARTIFACT_SHA256,
            "precomparison": PRECOMPARISON_MANIFEST_SHA256,
        },
        "source freeze anchors drifted before replay",
    )

    with tempfile.TemporaryDirectory(prefix="wave33-chronology-") as directory:
        scratch = Path(directory)
        synthetic = scratch / "historical-root"
        outputs = scratch / "outputs"
        outputs.mkdir()
        materialized = materialize_historical_root(
            synthetic, source_root=source_root
        )
        before = tree_snapshot(synthetic)
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"

        discovery_test = run_process(
            [
                sys.executable,
                "-B",
                "-m",
                "unittest",
                "discover",
                "-s",
                "attempts/wave33-rooted-construction",
                "-p",
                "test_*.py",
                "-q",
            ],
            cwd=synthetic,
            environment=environment,
        )
        verifier_test = run_process(
            [
                sys.executable,
                "-B",
                "-m",
                "unittest",
                "discover",
                "-s",
                "verification/wave33-rooted-construction",
                "-p",
                "test_*.py",
                "-q",
            ],
            cwd=synthetic,
            environment=environment,
        )
        discovery_count = unittest_count(discovery_test)
        verifier_count = unittest_count(verifier_test)
        require(discovery_count == 14, "historical discovery test count drift")
        require(verifier_count == 37, "historical verifier test count drift")

        exact_output = outputs / "exact-results.json"
        run_process(
            [
                sys.executable,
                "-B",
                "attempts/wave33-rooted-construction/exact_check.py",
                "--partial-certificate",
                "attempts/wave33-rooted-construction/"
                "partial-design-certificate.json",
                "--output",
                str(exact_output),
            ],
            cwd=synthetic,
            environment=environment,
        )
        require(
            sha256_path(exact_output) == EXPECTED_EXACT_RESULTS_SHA256,
            "historical exact replay output hash drift",
        )
        accepted_exact = (
            synthetic
            / "attempts"
            / "wave33-rooted-construction"
            / "exact-results.json"
        )
        require(
            exact_output.read_bytes() == accepted_exact.read_bytes(),
            "historical exact replay is not byte-identical",
        )

        comparison_process = run_process(
            [
                sys.executable,
                "-B",
                "verification/wave33-rooted-construction/"
                "candidate_comparison.py",
                "--reproduce-search",
            ],
            cwd=synthetic,
            environment=environment,
        )
        try:
            comparison_value = json.loads(comparison_process.stdout)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ChronologyError("comparison CLI did not emit JSON") from exc
        accepted_comparison_path = (
            synthetic
            / "verification"
            / "wave33-rooted-construction"
            / "candidate-comparison-results.json"
        )
        accepted_comparison = json.loads(
            accepted_comparison_path.read_text(encoding="utf-8")
        )
        require(
            sha256_bytes(comparison_process.stdout)
            == EXPECTED_COMPARISON_CLI_STDOUT_SHA256,
            "comparison CLI stdout hash drift",
        )
        require(
            sha256_path(accepted_comparison_path)
            == EXPECTED_COMPARISON_RESULTS_SHA256,
            "accepted comparison result hash drift",
        )
        assert_status_wall(comparison_value)
        assert_status_wall(accepted_comparison)
        require(
            comparison_value["claim_label"]
            == accepted_comparison["claim_label"]
            == "VERIFIED",
            "comparison claim label drift",
        )
        require(
            comparison_value["assignment_encoding"]["row_system_sha256"]
            == accepted_comparison["assignment_encoding"]["row_system_sha256"],
            "comparison assignment-row digest drift",
        )
        for actual_key, accepted_key in (
            ("violation_count", "BF_violation_count"),
            ("squared_defect", "BF_squared_defect"),
            ("exact_support_group_count", "BF_exact_support_group_count"),
        ):
            require(
                comparison_value["hostile_partial"]["BF"][actual_key]
                == accepted_comparison["hostile_partial"][accepted_key],
                f"comparison hostile BF summary drift: {actual_key}",
            )
        require(
            comparison_value["deterministic_hostile_search_reproduction"][
                "certificate_sha256"
            ]
            == EXPECTED_CERTIFICATE_SHA256,
            "comparison search replay certificate hash drift",
        )
        require(
            comparison_value["deterministic_hostile_search_reproduction"][
                "byte_identical"
            ]
            is True,
            "comparison search replay is not byte-identical",
        )

        after = tree_snapshot(synthetic)
        require(before == after, "historical synthetic tree was modified")
        require(
            not any("__pycache__" in path.parts for path in synthetic.rglob("*")),
            "historical replay created __pycache__",
        )

    source_after = {
        "candidate_freeze": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction-candidate-freeze.sha256"
        ),
        "candidate_artifact": sha256_path(
            source_root
            / "attempts"
            / "wave33-rooted-construction"
            / "artifact-manifest.sha256"
        ),
        "verifier_artifact": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction"
            / "artifact-manifest.sha256"
        ),
        "precomparison": sha256_path(
            source_root
            / "verification"
            / "wave33-rooted-construction"
            / "precomparison-freeze.sha256"
        ),
    }
    require(source_before == source_after, "source freeze anchors changed in replay")

    return {
        "schema_version": 1,
        "role": "verifier",
        "claim_label": "VERIFIED",
        "scope": (
            "Historical-byte replay of the unchanged Wave 33 rooted "
            "construction discovery and verifier packages only."
        ),
        "chronology": {
            "live_structure_is_not_historical_input": (
                sha256_path(source_root / "STRUCTURE.md")
                != HISTORICAL_STRUCTURE_SHA256
            ),
            "historical_structure_sha256": HISTORICAL_STRUCTURE_SHA256,
            "historical_input_count": 8,
            "archive_sha256": sha256_path(ARCHIVE),
            "archive_status": "PASS",
        },
        "freeze_anchors": {
            "candidate_freeze_sha256": CANDIDATE_FREEZE_SHA256,
            "candidate_artifact_manifest_sha256": CANDIDATE_ARTIFACT_SHA256,
            "precomparison_manifest_sha256": PRECOMPARISON_MANIFEST_SHA256,
            "verifier_artifact_manifest_sha256": VERIFIER_ARTIFACT_SHA256,
            "status": "UNCHANGED",
        },
        "materialized": materialized,
        "replay": {
            "unchanged_discovery_tests_passed": discovery_count,
            "unchanged_verifier_tests_passed": verifier_count,
            "historical_package_tests_passed": discovery_count + verifier_count,
            "exact_results_sha256": EXPECTED_EXACT_RESULTS_SHA256,
            "exact_results_byte_identical": True,
            "comparison_results_sha256": EXPECTED_COMPARISON_RESULTS_SHA256,
            "comparison_cli_stdout_sha256":
                EXPECTED_COMPARISON_CLI_STDOUT_SHA256,
            "comparison_accepted_summary_core_bound": True,
            "hostile_search_certificate_sha256": EXPECTED_CERTIFICATE_SHA256,
            "hostile_search_certificate_byte_identical": True,
            "synthetic_tree_unchanged": True,
            "checkout_outputs_written": 0,
            "pycache_created": False,
            "status": "PASS",
        },
        "status_wall": {
            "complete_graph_extension": "UNKNOWN",
            "complete_domain_UNSAT_certificate": "NONE",
            "full_rooted_endpoint": "UNKNOWN",
            "n3_708": "UNKNOWN",
            "Conway_99": "UNKNOWN",
            "novelty": "UNKNOWN",
            "timeout_negative_evidence": False,
        },
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--build-archive", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.build_archive:
            require(args.output is not None, "--build-archive requires --output")
            payload = build_archive_payload()
            args.output.write_bytes(canonical_json_bytes(payload))
            print(
                json.dumps(
                    {
                        "archive": str(args.output),
                        "sha256": sha256_path(args.output),
                        "status": "BUILT_AND_HASH_CHECKED",
                    },
                    sort_keys=True,
                )
            )
            return 0
        result = run_full_replay()
        encoded = canonical_json_bytes(result)
        if args.output is None:
            sys.stdout.buffer.write(encoded)
        else:
            args.output.write_bytes(encoded)
            print(
                json.dumps(
                    {
                        "output": str(args.output),
                        "sha256": sha256_path(args.output),
                        "status": "PASS",
                    },
                    sort_keys=True,
                )
            )
        return 0
    except (OSError, ChronologyError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
