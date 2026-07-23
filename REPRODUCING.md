# Reproducing results

## Trust model

Discovery code may be complicated, optimized, randomized, or wrong. A result
is promoted only when a small independent checker validates a complete
certificate using exact arithmetic.

The minimum positive certificate is a 99-vertex edge list or adjacency matrix.
The canonical validator checks, from scratch:

1. input syntax and vertex count;
2. simplicity, symmetry, and zero diagonal;
3. degree 14 at every vertex;
4. exactly one common neighbor for every edge;
5. exactly two common neighbors for every nonedge; and
6. the integer matrix identity `A^2 = 12 I - A + 2 J`.

Checks 3--5 and check 6 are deliberately redundant implementations of the
same mathematics. A second validator should use a different representation or
language.

## Environment policy

- Pin interpreter, solver, and package versions in every run manifest.
- Record operating system, CPU, wall time, command, random seed, input hashes,
  output hashes, and Git commit.
- Keep exact integer/rational artifacts; floating-point output can guide a
  search but cannot certify a claim.
- Calibrate encodings on known strongly regular graphs and known infeasible
  parameter sets before running the target instance.
- Verify SAT/UNSAT results independently. For UNSAT, retain a checkable proof
  artifact such as LRAT when technically feasible.

Create the optional search environment without changing the global Python
installation:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --requirement requirements-search.txt
```

The independent validators do not import this environment or trust its solver
bindings.

## Baseline commands

Run the test suite and the known-positive `srg(9,4,1,2)` calibration fixture:

```powershell
python -m unittest discover -s verification -p "test_*.py" -v
python verification/check_srg.py `
  verification/fixtures/rook-3x3.srg.json `
  --vertices 9 --degree 4 --lambda 1 --mu 2
powershell -NoProfile -ExecutionPolicy Bypass -File verification/Check-Srg.ps1 `
  -Certificate verification/fixtures/rook-3x3.srg.json `
  -Vertices 9 -Degree 4 -AdjacentCommon 1 -NonadjacentCommon 2
```

Check the deterministic rooted scaffold and its constraint counts:

```powershell
python code/root_model.py
python code/matching_orbits.py
```

Run the SAT encoding's positive and negative calibration cases:

```powershell
.venv\Scripts\python -m unittest discover -s code -p "test_*.py" -v
.venv\Scripts\python code/sat_model.py --pair-count 2 --solve `
  --candidate candidates/calibration-srg-9.srg.json
python verification/check_srg.py candidates/calibration-srg-9.srg.json `
  --vertices 9 --degree 4 --lambda 1 --mu 2
```

Run the native-cardinality discovery backend on the same positive control, or
make a bounded non-evidentiary pass over all complete target branches:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 2 `
  --cardinality native --solve
.venv\Scripts\python code/scout_branches.py --cardinality native `
  --fresh-solvers --conflict-budget 100000 `
  --output logs/local/native-100000.json
```

The embedded MiniCard solve is discovery-only, but the native formula now has
an exact archival export. Generate the canonical LF OPB positive and negative
controls with:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 2 `
  --cardinality native --opb formal/opb-calibration/pair2.opb
.venv\Scripts\python code/sat_model.py --pair-count 3 `
  --cardinality native --opb formal/opb-calibration/pair3.opb
```

The committed formulas, raw VeriPB proofs, and elaborated CakePB-compatible
proofs replay as documented in
`verification/2026-07-22-veripb-calibration.md`. The same exporter can produce
the target formula:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 7 `
  --cardinality native --opb logs/local/conway99-native-lf.opb
```

The independently audited theorem-forced normalization is available only for
the target:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 7 --n3 `
  --cardinality native --opb logs/local/conway99-n3-native-lf.opb
```

Fixing the N3 witness changes the stabilizer, so the old 11 representatives
remain incompatible and the CLI rejects that combination. Use the separately
verified 12-branch cover instead:

```powershell
.venv\Scripts\python code/matching_orbits.py --n3-joint
.venv\Scripts\python verification/n3-joint-cover/verify.py
1..12 | ForEach-Object {
  $branch = '{0:D2}' -f $_
  .venv\Scripts\python code/sat_model.py --pair-count 7 `
    --cardinality native --n3 --n3-branch $_ `
    --opb "logs/local/conway99-n3-branch-$branch.opb"
}
```

All 12 branches together cover the normalized search. They act on the
invariant shared fiber `S_2`; the legacy `S_0` fiber is moved by part of the
stabilizer and has 78 orbits under its preserving subgroup. The exact
derivation, public certificate, and independent audit are in
`agents/2026-07-22-wave5-n3-joint-cover.md` and
`verification/2026-07-22-n3-joint-cover-audit.md`.

Reproduce the verified second-stage refinement with:

```powershell
.venv\Scripts\python code\matching_orbits.py --n3-refined
.venv\Scripts\python verification\n3-refined-cover\verify.py
1..78 | ForEach-Object {
  $branch = '{0:D3}' -f $_
  .venv\Scripts\python code\sat_model.py --pair-count 7 `
    --cardinality native --n3 --n3-refined-branch $_ `
    --opb "logs/local/conway99-n3-refined-$branch.opb"
}
```

The 78 cases cover the same normalized search more finely. They combine one
of the twelve shared-fiber matchings with the forced choice of an additional
coordinate-4 neighbor. The standalone checker verifies the full finite cover;
generating or briefly solving the OPBs does not establish a target result.

Replay the exact arithmetic for the conditional `n3 >= 24` structural bound
and its twelve branch-local refinements with:

```powershell
.venv\Scripts\python verification\n3-count-bound\verify.py
```

The corresponding human derivation and its source boundary are recorded in
`agents/2026-07-22-wave6-opposite-edge-graph.md` and
`verification/2026-07-22-n3-count-bound-audit.md`.

Replay the Wave 7 strengthening from `n3>=24` to `n3>=30` with two
independent standard-library implementations:

```powershell
.venv\Scripts\python verification\n3-side-incidence\verify.py
.venv\Scripts\python verification\n3-side-incidence\audit_generic.py
```

The first checker follows the complement-component analysis directly. The
second generates all admissible point-clique families, permits unused
complement edges, and adds singleton fillers. Their scope and clean-source
replay are recorded in
`verification/2026-07-22-n3-side-incidence-audit.md` and
`verification/2026-07-22-wave7-clean-clone.md`.

Replay the Wave 8 exclusion of the remaining equality case `n3=30` with:

```powershell
.venv\Scripts\python verification\n3-equality\verify.py
.venv\Scripts\python -m unittest verification.test_n3_equality -v
```

The compact checker is an arithmetic regression companion to the human
proof. An optional independent census audit regenerates all 21 cubic types,
674,880 point-clique families, and the committed exact JSON certificate. It
uses only the standard library but takes about five minutes:

```powershell
.venv\Scripts\python verification\n3-equality\audit_exhaustive.py `
  --check verification\n3-equality\n3-30-audit.json
```

The derivation, adversarial audit, and frozen-commit replay are recorded in
`agents/2026-07-22-wave8-n3-equality.md`,
`verification/2026-07-22-n3-equality-audit.md`, and
`verification/2026-07-22-wave8-clean-clone.md`. They establish the conditional
necessary bound `n3>=33`, not a target construction or nonexistence proof.

Replay the Wave 9 exclusion of `n3=33` with:

```powershell
.venv\Scripts\python verification\n3-33-equality\verify.py
.venv\Scripts\python -m unittest verification.test_n3_33_equality -v
```

The optional exhaustive secondary audit uses the complete connected quartic
order-11 catalog from House of Graphs, attributed there to Meringer's
`genreg`. The catalog is hashed but not vendored. Download and verify it, then
regenerate the scratch certificate and replay it independently:

```powershell
$wave9Catalog = Join-Path ([System.IO.Path]::GetTempPath()) "11_4_3.g6.gz"
$wave9Certificate = Join-Path ([System.IO.Path]::GetTempPath()) "n3-33-audit.json"
$wave9Replay = Join-Path ([System.IO.Path]::GetTempPath()) "n3-33-replay.json"
Invoke-WebRequest `
  -Uri "https://houseofgraphs.org/data/quartics/11_4_3.g6.gz" `
  -OutFile $wave9Catalog
$wave9CatalogHash = (Get-FileHash $wave9Catalog -Algorithm SHA256).Hash.ToLower()
if ($wave9CatalogHash -ne "05ee6bb0c2b40d63d5c44efc8e89ed1c0a381a170d81a3d052749c8edf6b14fd") {
  throw "unexpected Wave 9 catalog hash: $wave9CatalogHash"
}
.venv\Scripts\python verification\n3-33-equality\audit_exhaustive.py `
  --catalog $wave9Catalog --certificate $wave9Certificate `
  --git-commit 19f27d1ede9cdb0b4110540f52eeb3ad9c94cc94
.venv\Scripts\python verification\n3-33-equality\verify_exhaustive.py `
  --catalog $wave9Catalog --certificate $wave9Certificate `
  --output $wave9Replay
```

The expected census is 266 quartic types, 610 admissible point-clique
families, and zero survivors. The derivation, precise-status search,
adversarial audit, deterministic manifest, and clean replay are recorded in
`agents/2026-07-22-wave9-n3-33-equality.md`,
`agents/2026-07-22-wave9-status-search.md`,
`verification/2026-07-22-n3-33-equality-audit.md`,
`verification/n3-33-equality/n3-33-census-manifest.json`, and
`verification/2026-07-22-wave9-clean-clone.md`. They establish the conditional
necessary bound `n3>=36`; Conway-99 remains `UNKNOWN`.

Replay the Wave 10 exclusion of `n3=36` with:

```powershell
.venv\Scripts\python verification\n3-36-equality\verify.py
.venv\Scripts\python -m unittest verification.test_n3_36_equality -v
.venv\Scripts\python verification\n3-36-equality\verify_support.py `
  --certificate verification\n3-36-equality\n3-36-support.json
.venv\Scripts\python -m unittest verification.test_n3_36_support -v
```

The primary and independent support implementations use different enumeration
strategies. To regenerate the certificate in a scratch path from the technical
commit and replay it independently:

```powershell
$wave10Certificate = Join-Path ([System.IO.Path]::GetTempPath()) "n3-36-support.json"
.venv\Scripts\python verification\n3-36-equality\audit_support.py `
  --certificate $wave10Certificate `
  --git-commit 2194c2b68ebd5c34491d64f15d30f1a3597baa74
.venv\Scripts\python verification\n3-36-equality\verify_support.py `
  --certificate $wave10Certificate
```

The expected domain has 14 integer resource profiles before local pruning,
100 labeled point families in the forced `2K6` case, one point-family orbit,
216 abstract support masks, and zero survivors after the original-SRG
`lambda`/`mu` saturation check. The mask digest is
`6659fe1972cbacc6980a9792557714730572817b43224b5f1fac24bb0c4ca61a`.
The derivation, status search, adversarial audit, and clean replay are recorded
in `agents/2026-07-22-wave10-n3-36-equality.md`,
`agents/2026-07-22-wave10-status-search.md`,
`verification/2026-07-22-n3-36-equality-audit.md`, and
`verification/2026-07-22-wave10-clean-clone.md`. They establish only the
conditional necessary bound `n3>=39`; Conway-99 remains `UNKNOWN`.

Replay the Wave 11 exclusion of `n3=39` with:

```powershell
.venv\Scripts\python verification\n3-39-equality\verify.py
.venv\Scripts\python verification\n3-39-equality\verify_local.py `
  --certificate verification\n3-39-equality\n3-39-local.json
.venv\Scripts\python -m unittest -v `
  verification/test_n3_39_equality.py verification/test_n3_39_local.py
```

The committed certificate is bound to replay-code commit
`c299b88fbd956c813ff3379ff236b3123a90d242`. To regenerate it in a scratch
path and replay it independently:

```powershell
$wave11Certificate = Join-Path ([System.IO.Path]::GetTempPath()) "n3-39-local.json"
.venv\Scripts\python verification\n3-39-equality\audit_local.py `
  --certificate $wave11Certificate `
  --git-commit c299b88fbd956c813ff3379ff236b3123a90d242
.venv\Scripts\python verification\n3-39-equality\verify_local.py `
  --certificate $wave11Certificate
```

The expected replay has 8,907 records, 1,730,729 canonical JSONL bytes, and
combined SHA-256
`452850018ad13362694f5bfff2e4beac03288a113a0391c3456a47cd6fbfe9a1`.
The outer JSON certificate is emitted with canonical LF bytes and has
SHA-256 `4cd23939cfb8ec5080b57fb0626e9579b68250a219ea17876a8e1f4066ad2261`.
The two implementations use different enumeration mechanisms, freeze all nine
stream hashes, and reject eight premise, digest, conclusion, and status
mutations. The result is only the conditional necessary bound `n3>=42`;
Conway-99 remains `UNKNOWN`. The detached-clone procedure, first failed
newline-portability gate, canonical-LF repair, and exact byte comparison are
recorded in `verification/2026-07-22-wave11-clean-clone.md`.

Replay the Wave 12 exclusion of `n3=42` with:

```powershell
.venv\Scripts\python code\wave12_n3_42_active.py `
  --certificate attempts\wave12-computation\n3-42-size2-active-local-candidate.json
.venv\Scripts\python code\wave12_n3_42_size2_scout.py `
  --compare attempts\wave12-computation\n3-42-size2-active-local-candidate.json
.venv\Scripts\python code\wave12_n3_42_size2_caps.py `
  --catalog attempts\wave12-computation\n3-42-cubic-trianglefree-14.g6
.venv\Scripts\python code\test_wave12_n3_42.py -v
.venv\Scripts\python verification\n3-42-equality\verify_reduction.py
.venv\Scripts\python -m unittest verification.test_n3_42_reduction -v
```

The independent catalog replay uses Meringer's official 871-byte GENREG
shortcode archive. It is not redistributed because its source page states no
license. Download it from the official host and verify its exact digest:

```powershell
$wave12Scd = 'verification\n3-42-equality\14_3_4.scd'
$wave12ScdSha = '6f3e9cf2b7e0d85c5df59c1638ab9d2fddbfc9905c49b35da01cc892f847e9a0'
Invoke-WebRequest `
  -Uri 'https://www.mathe2.uni-bayreuth.de/markus/REGGRAPHS/SCD/14_3_4.scd' `
  -OutFile $wave12Scd
if ((Get-FileHash $wave12Scd -Algorithm SHA256).Hash.ToLower() -ne $wave12ScdSha) {
  throw 'Wave 12 GENREG archive hash mismatch'
}

$wave12Certificate = Join-Path ([System.IO.Path]::GetTempPath()) `
  'n3-42-support-certificate.json'
.venv\Scripts\python verification\n3-42-equality\build_support_certificate.py `
  --scd $wave12Scd `
  --graph6 attempts\wave12-computation\n3-42-cubic-trianglefree-14.g6 `
  --output $wave12Certificate
$wave12Expected = '8115b5f34568a463952afc399bc22db927121f3f1aa28cfc33ae191ea93dc68a'
if ((Get-FileHash $wave12Certificate -Algorithm SHA256).Hash.ToLower() -ne $wave12Expected) {
  throw 'Wave 12 regenerated certificate hash mismatch'
}
.venv\Scripts\python verification\n3-42-equality\verify_support_certificate.py `
  --certificate verification\n3-42-equality\n3-42-support-certificate.json `
  --scd $wave12Scd `
  --graph6 attempts\wave12-computation\n3-42-cubic-trianglefree-14.g6 `
  --mutations
```

The catalog audit decodes 110 connected GENREG types, independently classifies
two disconnected types, and matches all 112 graph6 records. Four types survive
the mandatory-degree filter and zero support factors survive the exact replay.
Combined with the separately checked proof reduction, this establishes only the
conditional necessary bound `n3>=45` and
`induced_C6_count>=209331`. Conway-99 and novelty remain `UNKNOWN`. See
`verification/2026-07-22-n3-42-support-audit.md` and
`verification/2026-07-22-wave12-integration-audit.md`. The complete detached
replay is recorded in `verification/2026-07-22-wave12-clean-clone.md`.

Replay the Wave 13 conditional exclusion of `n3=45` with two independent
semantic checkers:

```powershell
.venv\Scripts\python verification\n3-45-equality\verify.py --mutations
.venv\Scripts\python -m unittest verification.test_n3_45_audit -v
.venv\Scripts\python verification\n3-45-equality-b\audit_semantics.py
```

The frozen proof report has SHA-256
`e721614256f003d7266d0b3d1bb2f884febbdec33893f92ed18bf8961c6958e8`.
Both semantic audits return the conditional bounds `n3>=48` and
`induced_C6_count>=209334`, with target and novelty `UNKNOWN`. The second
verdict was frozen before it read the first audit. Neither checker assumes a
completed-graph automorphism, connectedness, or transitivity.

Replay the repaired Wave 13 computation bundle separately:

```powershell
$env:PYTHONPATH='code'
.venv\Scripts\python code\wave13_n3_45_test.py -v
.venv\Scripts\python verification\n3-45-computation-repair\independent_repair_audit.py
.venv\Scripts\python -m unittest discover `
  -s verification\n3-45-computation-repair -p 'test_*.py' -v
.venv\Scripts\python -m unittest discover `
  -s verification\n3-45-computation -p 'test_*.py' -v
```

The last command is the historical FAIL-audit suite. At the current tip it
loads the defective validator and artifact directly from frozen commit
`066d9c7fcf593c3b9d35cfef1031dbd9daab4145`, so its 15 tests continue to
exercise the original defects rather than the repaired v2 files. The current
repair suite has 12 tests and the independent repair suite has six.

For direct provenance replay, regenerate the census and positive diagnostic:

```powershell
$wave13Census = Join-Path ([System.IO.Path]::GetTempPath()) `
  'n3-45-local-census.json'
$wave13Candidate = Join-Path ([System.IO.Path]::GetTempPath()) `
  'n3-45-no-common-point-m5-111.json'
.venv\Scripts\python code\wave13_n3_45_profiles.py `
  --output $wave13Census --json
.venv\Scripts\python code\wave13_n3_45_active_sat.py `
  --size3 5 --root-mode 111 --variant no_common_point `
  --solver cadical195 --conflict-budget 300000 `
  --candidate $wave13Candidate --json
.venv\Scripts\python code\wave13_n3_45_active_sat.py `
  --validate $wave13Candidate
```

The expected census SHA-256 is
`6546819c11dbecbf21a4cfaff00b71d338629c045c7bf156493426391b25ac55`;
the expected positive artifact SHA-256 is
`629cf0dd9f67b71072e94037161d99891f16c90c330b7d5746ed8a86ac8ba1e8`.
The independent audit rebuilds all 17 formula streams, checks all 1,141,796
positive clauses, certifies exactly 18 violations of the deliberately omitted
common-point premise, and rejects 31 hostile mutations. The original bundle's
FAIL audit and its later repair are both retained. No checked proof trace
exists for any solver-negative row, so every such row remains
`UNSAT_UNVERIFIED` and is not evidence for the `n3=45` exclusion. The detached
52-code-test, 12-focused-test, and 104-verification-test replay is recorded in
`verification/2026-07-22-wave13-clean-clone.md`.

Replay the Wave 14 `n3=48` structural frontier and its explicit
all-size-two relaxation object:

```powershell
.venv\Scripts\python -B attempts\wave14-proof-a\profile_modes.py
.venv\Scripts\python -B attempts\wave14-proof-a\verify_all2_countermodel.py `
  attempts\wave14-proof-a\all2-active-countermodel.json
.venv\Scripts\python -B -m unittest -v `
  attempts\wave14-proof-a\test_wave14_proof_a.py
.venv\Scripts\python -B verification\n3-48-proof\independent_reconstruction.py
.venv\Scripts\python -B verification\n3-48-proof\audit_countermodel.py `
  attempts\wave14-proof-a\all2-active-countermodel.json
```

Replay the separate active-local computation and its independent audit:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.venv\Scripts\python code\wave14_n3_48_verify.py `
  --output attempts\wave14-computation\n3-48-independent-validation.json
.venv\Scripts\python code\wave14_n3_48_test.py -v
.venv\Scripts\python verification\n3-48-computation\independent_audit.py
```

The proof audit reproduces twelve raw profiles, three inherited survivors,
both mixed-profile exclusions, and the exact unresolved `r=16` support
residual. The computation audit independently rebuilds thirteen formulas,
checks one full positive object and two weakened controls, and rejects 29
hostile mutations. Its raw scan remains exactly `1 SAT_CANDIDATE`,
`7 UNSAT_UNVERIFIED`, `1 BUDGET_UNKNOWN`, and `2 TIMEOUT_UNKNOWN`. None of
the seven negative rows has a checked proof trace. Wave 14 therefore leaves
the verified bound at `n3>=48` and `induced_C6_count>=209334`; equality,
Conway-99, and novelty remain `UNKNOWN`.

Replay the Wave 15 global-lift certificate, submitted checks, and independent
audit from the repository root:

```powershell
.venv\Scripts\python -B `
  attempts\wave15-global-lift\build_subset_moment_certificate.py `
  --countermodel attempts\wave14-proof-a\all2-active-countermodel.json `
  --output verification\n3-48-global-lift\regenerated-certificate.json
.venv\Scripts\python -B `
  attempts\wave15-global-lift\verify_subset_moment_certificate.py `
  attempts\wave15-global-lift\subset-moment-certificate.json
.venv\Scripts\python -B -m unittest -v `
  attempts\wave15-global-lift\test_subset_moment.py
.venv\Scripts\python -B `
  verification\n3-48-global-lift\independent_check.py

$wave15Python = (Resolve-Path '.venv\Scripts\python.exe').Path
Push-Location verification\n3-48-global-lift
& $wave15Python -B -m unittest -v test_independent_check.py
Pop-Location
```

The submitted certificate and independently regenerated certificate must be
byte-identical LF files with SHA-256
`cb02ab80f92d7d2c8ec5140e3be2916354976442aa2e1869524aa728c73bd386`.
The verifier-directory change is intentional: that focused suite imports its
sibling checker. The first repository-root invocation of that suite failed
before collecting tests; the corrected working directory and failure are
both recorded in the audit trail.

Replay the independent algebraic lane and its adversarial checker from the
repository root:

```powershell
.venv\Scripts\python -B attempts\wave15-algebraic\exact_checks.py `
  --output attempts\wave15-algebraic\exact-checks.json
.venv\Scripts\python -B `
  verification\n3-48-algebraic\independent_check.py `
  --artifact attempts\wave15-algebraic\exact-checks.json
.venv\Scripts\python -B -m unittest -v `
  verification\n3-48-algebraic\test_independent_check.py
```

The algebraic JSON must have SHA-256
`a6c9109e4fcfcdd2f5a8f5d4299ac1b4cf4037b8f1e4c468b4ecd75aba762512`.
These commands pass 5 submitted global tests, 11 independent global tests,
and 7 independent algebraic tests. They verify the conditional exclusion
`n3!=48`, hence `n3>=51` and `induced_C6_count>=209337`; they do not resolve
Conway-99 or establish novelty.

An archival UNSAT claim would require the complete public OPB formula, a
complete proof from a pinned producer, and successful independent checking.
The alternative sequential-counter CNF/LRAT route remains available. No
target proof currently exists in either format.

Validate a future Conway-format certificate using the frozen defaults:

```powershell
python verification/check_srg.py candidates/conway-99.srg.json
```

No such target certificate is currently claimed. `STATUS.yaml` remains the
authoritative machine-readable status.

`requirements-search.txt` pins the prototyping API version, but it is not an
archival proof lockfile. Before a proof-producing run, also pin the Python ABI,
wheel hashes, proof-producing solver binary, and independent checker binaries,
then record their cryptographic hashes in the run manifest. The current Exact,
VeriPB, and CakePB identities and hashes are in the calibration report.

## Artifact retention

Small certificates and verification reports belong in Git. Large CNF, LRAT,
solver logs, and checkpoints should be stored in a content-addressed release or
archive. Commit a manifest containing cryptographic hashes and retrieval URLs.
Never treat an unavailable artifact as verified evidence.
