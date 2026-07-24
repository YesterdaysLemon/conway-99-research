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

Replay the Wave 16 structural proof companion and independent verifier:

```powershell
.venv\Scripts\python -B `
  attempts\wave16-n3-51-structural\exact_check.py `
  --verify attempts\wave16-n3-51-structural\exact-checks.json
.venv\Scripts\python -B -m unittest -v `
  attempts\wave16-n3-51-structural\test_exact_check.py
.venv\Scripts\python -B `
  verification\n3-51-structural\independent_check.py

$wave16Python = (Resolve-Path '.venv\Scripts\python.exe').Path
Push-Location verification\n3-51-structural
& $wave16Python -B -m unittest -v test_independent_check.py
Pop-Location
```

The submitted suite passes 8 tests and the independent suite passes 24. The
checker pins repaired discovery report hash
`95d04a774397332417c9613718fe6699a5392ef5222fef1cfa00b12e2860af3f`
and final Wave 15 audit hash
`edda3785d080db464028f10c22bcae5c0bf17f1e61432a8641bfa6ffdccab036`,
while retaining the failed baseline and intermediate hashes as historical
provenance. These checks verify the conditional `n3=51` exclusion and the
bounds `n3>=54`, `induced_C6_count>=209340`.

Replay the separate Wave 16 active-local computational archive:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.venv\Scripts\python -B code\wave16_n3_51_profiles.py `
  --output verification\n3-51-computation\regenerated-profile-census.json
.venv\Scripts\python -B code\wave16_n3_51_verify.py `
  --output verification\n3-51-computation\submitted-validation-replay.json
.venv\Scripts\python -B code\wave16_n3_51_test.py -v
.venv\Scripts\python -B `
  verification\n3-51-computation\independent_check.py `
  --output verification\n3-51-computation\independent-audit.json
.venv\Scripts\python -B `
  verification\n3-51-computation\test_independent_check.py -v
```

The independent audit rebuilds all seven DIMACS streams, fixes the raw
24-point/69-edge candidate into its rebuilt positive CNF, rejects 38 hostile
mutations, and passes 4 tests; the submitted suite passes 8. Regenerated
profile and validation artifacts are byte-identical. The archive status is
exactly `1 SAT_CANDIDATE`, `5 TIMEOUT_UNKNOWN`, `1 UNSAT_UNVERIFIED`, plus
one historical `BUDGET_UNKNOWN`. No negative row has a checked proof trace,
and none is used in the human exclusion.

The non-computational literature record is preserved in
`agents/2026-07-23-wave16-status-search.md` and independently checked in
`verification/2026-07-23-wave16-status-audit.md`. These reports record their
exact query families, source URLs, page locations, source-file hashes where
available, access failures, and the 2026-07-23 cutoff. Their search nonhits do
not reproduce a mathematical conclusion or establish novelty. The complete
detached replay is recorded in
`verification/2026-07-23-wave16-clean-clone.md`.

Replay the Wave 17 `n3=54` structural reduction and independent audit:

```powershell
.venv\Scripts\python.exe -B `
  attempts\wave17-n3-54-structural\exact_check.py
.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave17-n3-54-structural\test_exact_check.py
.venv\Scripts\python.exe -B `
  verification\n3-54-structural\independent_check.py
.venv\Scripts\python.exe -B -m unittest -v `
  verification\n3-54-structural\test_independent_check.py
```

The submitted suite passes 7 tests and the independent suite passes 21. They
verify the six-profile reduction, equality/equitable cut, exact `F/R`
representation, `3K3,3` parity exclusion, and the two remaining catalog
families. The restricted SAT controls may also return raw `UNSAT`, but they
emit no checked proof trace and are not evidence.

Replay the exact 457-case census and its separately written verifier without
overwriting committed artifacts:

```powershell
$wave17ReplayStem = [guid]::NewGuid().ToString('N')
$wave17ReplayRoot = [System.IO.Path]::GetTempPath()
$wave17Raw = Join-Path $wave17ReplayRoot "$wave17ReplayStem-raw.json"
$wave17Certificate = Join-Path $wave17ReplayRoot "$wave17ReplayStem-certificate.json"
$wave17Independent = Join-Path $wave17ReplayRoot "$wave17ReplayStem-independent.json"

.venv\Scripts\python.exe -B `
  attempts\wave17-n3-54-census\census.py `
  --model-limit 100000 --output $wave17Raw
.venv\Scripts\python.exe -B `
  attempts\wave17-n3-54-census\build_certificate.py `
  --output $wave17Certificate
.venv\Scripts\python.exe -B `
  attempts\wave17-n3-54-census\verify_certificate.py `
  attempts\wave17-n3-54-census\exact-certificate.json
.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave17-n3-54-census\test_certificate.py
.venv\Scripts\python.exe -B `
  verification\n3-54-census\independent_verifier.py `
  --output $wave17Independent
.venv\Scripts\python.exe -B -m unittest -v `
  verification\n3-54-census\test_independent_verifier.py

Get-FileHash -Algorithm SHA256 $wave17Raw,$wave17Certificate,$wave17Independent
```

The expected SHA-256 values are:

```text
raw census:            f81158e9dacbb4b83bdbc3f19724c304b9dc10a550297661f68272f0d83cdeb2
exact certificate:     f5c66a2ba6ee0c8b0d4ea4a15411366000faf03fdcb431e19f26747d117ced12
independent result:    159903af624a2df1975dd490ea5c267e453b5a96fe9744a9aa7a7be28390b056
```

Both implementations fetch the official House of Graphs catalogs into
memory, validate compressed and decompressed hashes, decode every record, and
reconstruct all 457 cases. The discovery tests pass 6/6 and the independent
hostile tests pass 17/17. The exact proof uses parity-kernel exhaustion and a
mixed-component degree count, not the archived proofless SAT statuses. The
audited consequence is the conditional necessary bound `n3>=57`, hence
`induced_C6_count>=209343`; Conway-99 and novelty remain `UNKNOWN`. The
separate literature reports are
`agents/2026-07-23-wave17-status-search.md` and
`verification/2026-07-23-wave17-status-audit.md`.

Replay the Wave 18 direct exclusion of conditional `n3=57` and its separately
written verifier without overwriting the committed discovery artifact:

```powershell
$wave18ReplayStem = [guid]::NewGuid().ToString('N')
$wave18ReplayRoot = [System.IO.Path]::GetTempPath()
$wave18Exact = Join-Path $wave18ReplayRoot "$wave18ReplayStem-exact.json"

.venv\Scripts\python.exe -B `
  attempts\wave18-n3-57-structural\exact_check.py `
  --output $wave18Exact
.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave18-n3-57-structural\test_exact_check.py
.venv\Scripts\python.exe -B `
  attempts\wave18-n3-57-structural\exact_check.py `
  --verify attempts\wave18-n3-57-structural\exact-checks.json
.venv\Scripts\python.exe -B `
  verification\n3-57-structural\independent_checker.py
.venv\Scripts\python.exe -B -m unittest -v `
  verification\n3-57-structural\test_independent_checker.py

Get-FileHash -Algorithm SHA256 $wave18Exact
Get-FileHash -Algorithm SHA256 `
  verification\n3-57-structural\checker-results.json, `
  verification\n3-57-structural\mutation-results.json
```

The expected SHA-256 values are:

```text
regenerated exact checks: 76decce7f0af8e3bf2db483096a10a86321a9d7143e6123ad2081ec17d28604c
independent results:      1e640f9e3a0d754f60f66638c481f01ce878ef6ccdc140c2ad79aada903aaf1d
mutation results:         eb5f4204e625bfa07f1a4f1e3c99940adacde68d73a0ae07bec1429ea7c40f59
```

The submitted suite passes 10/10 tests and the independent suite passes 14/14.
The independent checker detects all 24 frozen mutations and reconstructs all
nine `sum q=38` profiles, the endpoint crossing tables, the `r=18` equality
branches, both `r=19` active-set sizes, and exact rational spectral caps.
Wave 18 excludes `n3=57` without importing Wave 17; combining the two audited
waves gives the conditional necessary bound `n3>=60`, hence
`induced_C6_count>=209346`. Conway-99 and novelty remain `UNKNOWN`.
The source-first literature record and its independent audit are
`agents/2026-07-23-wave18-status-search.md` and
`verification/2026-07-23-wave18-status-audit.md`. They also preserve the
exact `1^20,2^51` correction to Ishihara's equation (88), while keeping both
target outcomes and Wave 18 novelty `UNKNOWN`.
The detached end-to-end release replay is recorded in
`verification/2026-07-23-wave18-clean-clone.md`.

Replay the canonical Wave 19 `n3=60` release and its separately written
verifier without overwriting committed artifacts:

```powershell
.venv\Scripts\python.exe -B -m unittest -v `
  attempts.wave19-alternate-frontier.test_exact_frontier
.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\n3-60-closure `
  -p test_independent_baseline.py -v
.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\n3-60-closure `
  -p test_independent_closure_verifier.py -v

$wave19ReplayStem = [guid]::NewGuid().ToString('N')
$wave19ReplayRoot = [System.IO.Path]::GetTempPath()
$wave19Independent = Join-Path $wave19ReplayRoot `
  "$wave19ReplayStem-independent-full.json"
.venv\Scripts\python.exe -B `
  verification\n3-60-closure\independent_closure_verifier.py `
  --phase all --output $wave19Independent
Get-FileHash -Algorithm SHA256 $wave19Independent
```

The expected independent JSON SHA-256 is
`c8fb3af52d5a929d7d88b59ef53b8825a3b2d922fdb3fad1ac4208078a27a2a2`.
The submitted suite passes 7/7 tests, the independent baseline passes 27/27,
and the focused independent verifier passes 10/10. The full verifier downloads
and validates the six pinned official cubic catalogs, reproduces all 510,489
connected and 177 disconnected dispositions, reconstructs the two-Petersen
orbit, exhausts every allowed `Z` through three edges, and replays the exact
Gram/Farkas obstruction. The official catalog completeness assertion remains
an external premise. The audited consequence is the conditional bound
`n3>=63`, hence `induced_C6_count>=209349`; Conway-99 and novelty remain
`UNKNOWN`. The detached end-to-end replay is recorded in
`verification/2026-07-23-wave19-clean-clone.md`.

Replay the Wave 20 global Schur-projector arithmetic and the separately
written independent implementation from the repository root:

```powershell
.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave20-global-obstruction `
  -p test_exact_check.py -v
.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave20-global-obstruction\independent-verifier `
  -p test_independent_check.py -v

$wave20ReplayStem = [guid]::NewGuid().ToString('N')
$wave20ReplayRoot = [System.IO.Path]::GetTempPath()
$wave20Submitted = Join-Path $wave20ReplayRoot `
  "$wave20ReplayStem-submitted.json"
$wave20Independent = Join-Path $wave20ReplayRoot `
  "$wave20ReplayStem-independent.json"

.venv\Scripts\python.exe -B `
  attempts\wave20-global-obstruction\exact_check.py `
  --output $wave20Submitted
.venv\Scripts\python.exe -B `
  attempts\wave20-global-obstruction\independent-verifier\independent_check.py `
  --output $wave20Independent
Get-FileHash -Algorithm SHA256 $wave20Submitted,$wave20Independent
```

The expected submitted and independent SHA-256 values are, respectively,

```text
6aea5c4688880a33d358ccc8992ef3aa63d40be70b5c450a8a39bf83b4878dc2
575939f9abe19e5578a2efd1155495877c2080944c75cc0db6702c21a9ce2637
```

The submitted suite passes 18/18 and the independent suite passes 16/16.
They reconstruct the triangle-incidence spectrum, all 13 fixed-triangle
profiles, the rank-44 projector, the Schur trace, the mod-two nonzero-row
condition, the alternating mod-two lemma, the mod-four diagonal floor, and
the final divisibility endpoint. The audited conditional consequence is
`n3>=705`, hence `induced_C6_count>=209991`. No automorphism, graph catalog,
solver-negative, or floating-point premise is used. The source-first status
record is
`verification/global-schur/2026-07-23T170612Z-status-literature-audit.md`;
its exact-search nonhits leave novelty and Conway-99 `UNKNOWN`. The detached
end-to-end release replay is
`verification/2026-07-23-wave20-clean-clone.md`.

Replay the Wave 21 six-/seven-vertex affine-count audit from the repository
root. The submitted checker is standard-library-only:

```powershell
.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave21-six-vertex-lp\test_exact_check.py

$wave21Stem = [guid]::NewGuid().ToString('N')
$wave21Root = Join-Path ([System.IO.Path]::GetTempPath()) "wave21-$wave21Stem"
New-Item -ItemType Directory -Path $wave21Root | Out-Null
$wave21Submitted = Join-Path $wave21Root "submitted.json"

.venv\Scripts\python.exe -B `
  attempts\wave21-six-vertex-lp\exact_check.py `
  --output $wave21Submitted
Get-FileHash -Algorithm SHA256 $wave21Submitted
```

The submitted suite passes 16/16 and the expected JSON SHA-256 is
`5e7b6f526985fb719754145944579aacb0e8f38e9e14a54d2075552a3756ff2b`.

The independent verifier parses fresh copies of the exact primary-source TeX.
Download, inspect, and extract the two pinned arXiv archives:

```powershell
$wave21SixArchive = Join-Path $wave21Root "six-v2.tar"
$wave21SevenArchive = Join-Path $wave21Root "seven-v1.tar"
$wave21SixRoot = Join-Path $wave21Root "six"
$wave21SevenRoot = Join-Path $wave21Root "seven"
New-Item -ItemType Directory -Path $wave21SixRoot,$wave21SevenRoot | Out-Null

Invoke-WebRequest -UseBasicParsing `
  https://export.arxiv.org/e-print/2508.03377v2 `
  -OutFile $wave21SixArchive
Invoke-WebRequest -UseBasicParsing `
  https://export.arxiv.org/e-print/2511.06572v1 `
  -OutFile $wave21SevenArchive

Get-FileHash -Algorithm SHA256 $wave21SixArchive,$wave21SevenArchive

foreach ($wave21Archive in @($wave21SixArchive,$wave21SevenArchive)) {
  $wave21Members = @(& tar -tf $wave21Archive)
  if ($LASTEXITCODE -ne 0) { throw "Could not list $wave21Archive" }
  foreach ($wave21Member in $wave21Members) {
    $wave21Normalized = $wave21Member.Replace('\','/')
    if ([System.IO.Path]::IsPathRooted($wave21Member) -or
        $wave21Normalized -match '(^|/)\.\.(/|$)' -or
        $wave21Normalized -match '^[A-Za-z]:') {
      throw "Unsafe archive path: $wave21Member"
    }
  }
}

& tar -xf $wave21SixArchive -C $wave21SixRoot
if ($LASTEXITCODE -ne 0) { throw "Six-vertex extraction failed" }
& tar -xf $wave21SevenArchive -C $wave21SevenRoot
if ($LASTEXITCODE -ne 0) { throw "Seven-vertex extraction failed" }

$wave21SixTex = Join-Path $wave21SixRoot "The_Subgraphs_of_Order_Six.tex"
$wave21SevenTex = Join-Path $wave21SevenRoot `
  "Hamiltonian_Subgraphs_of_Order_Seven.tex"
Get-FileHash -Algorithm SHA256 $wave21SixTex,$wave21SevenTex
```

Expected archive hashes, in order, are
`f8429d2f839267e2aaf98b04451cb2f0252c0353f75bee6ec6e6947eab0d5834`
and
`10f8d9ea09dc72f4ca6bce4e9427ff1df32718d2978bb35a16db1af3c27cc39a`.
Expected TeX hashes are
`823bcaf636a99f6655af453b2a910b9953338db980480572bca81730cfa1b44f`
and
`0b06fdc1c2951a344592c6af23abd133c4a8a68d717f199e7a0e2d7ceb909d0a`.

Preserve the raw source failure, then run only the explicit correction:

```powershell
$wave21Raw = Join-Path $wave21Root "raw.json"
$wave21Corrected = Join-Path $wave21Root "corrected.json"

.venv\Scripts\python.exe -B `
  verification\wave21-six-vertex-lp\independent_check.py `
  --six-tex $wave21SixTex --seven-tex $wave21SevenTex `
  --mode raw --output $wave21Raw
$wave21RawExit = $LASTEXITCODE
if ($wave21RawExit -ne 1) {
  throw "Expected raw printed equation to exit 1; got $wave21RawExit"
}

.venv\Scripts\python.exe -B `
  verification\wave21-six-vertex-lp\independent_check.py `
  --six-tex $wave21SixTex --seven-tex $wave21SevenTex `
  --mode corrected --output $wave21Corrected
if ($LASTEXITCODE -ne 0) { throw "Corrected replay failed" }

$env:WAVE21_SIX_TEX = $wave21SixTex
$env:WAVE21_SEVEN_TEX = $wave21SevenTex
.venv\Scripts\python.exe -B -m unittest -v `
  verification\wave21-six-vertex-lp\test_independent_check.py
Get-FileHash -Algorithm SHA256 $wave21Raw,$wave21Corrected
```

The independent suite passes 19/19. The expected raw and corrected result
hashes are, respectively,

```text
50129e12b180c4f7ad7655cb4febe229588a855042a04b28817eeb52a3b27fb6
1c0cc560206ce388308573f2174a0a6189ae909f83a4acb86093063b5adfeacd
```

The raw process exit 1 is the expected `FAIL_AS_PRINTED`: the `m7(n-5)`
equation has residual exactly `n23`. The corrected process changes only the
named missing `+n23` deletion card. The verified exhaustion leaves
`n3=705,708,...,4158`, so it supplies neither a stronger bound nor a graph
construction. The public replay record is
`verification/wave21-six-vertex-lp/2026-07-23T175223Z-orchestrator-replay.md`.
The bounded current-version and correction search is recorded separately in
`verification/wave21-six-vertex-lp/status/2026-07-23T182843Z-source-status-audit.md`;
its companion manifest pins the official arXiv records, v1/v2 TeX and PDFs,
and later author sources.

Replay the two Wave 21 endpoint-refinement packages from the repository root:

```powershell
$wave21EndpointStem = [guid]::NewGuid().ToString('N')
$wave21EndpointRoot = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave21-endpoint-$wave21EndpointStem"
New-Item -ItemType Directory -Path $wave21EndpointRoot | Out-Null

.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave21-local-diagonal\test_exact_check.py
.venv\Scripts\python.exe -B -m unittest -v `
  verification\wave21-local-diagonal\test_independent_check.py

$wave21LocalSubmitted = Join-Path $wave21EndpointRoot "local-submitted.json"
.venv\Scripts\python.exe -B `
  attempts\wave21-local-diagonal\exact_check.py `
  --output $wave21LocalSubmitted

# The independent local checker writes beside its own script, so copy only
# that checker into the temporary replay directory.
$wave21LocalIndependentRoot = Join-Path $wave21EndpointRoot "local-independent"
New-Item -ItemType Directory -Path $wave21LocalIndependentRoot | Out-Null
Copy-Item -LiteralPath `
  verification\wave21-local-diagonal\independent_check.py `
  -Destination $wave21LocalIndependentRoot
.venv\Scripts\python.exe -B `
  (Join-Path $wave21LocalIndependentRoot "independent_check.py")

.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave21-lattice-extension\test_exact_check.py
.venv\Scripts\python.exe -B -m unittest -v `
  verification\wave21-lattice-extension\test_independent_check.py

$wave21LatticeSubmitted = Join-Path $wave21EndpointRoot `
  "lattice-submitted.json"
$wave21LatticeIndependent = Join-Path $wave21EndpointRoot `
  "lattice-independent.json"
.venv\Scripts\python.exe -B `
  attempts\wave21-lattice-extension\exact_check.py `
  --output $wave21LatticeSubmitted
.venv\Scripts\python.exe -B `
  verification\wave21-lattice-extension\independent_check.py `
  --output $wave21LatticeIndependent

Get-FileHash -Algorithm SHA256 `
  $wave21LocalSubmitted,`
  (Join-Path $wave21LocalIndependentRoot "independent-checks.json"),`
  $wave21LatticeSubmitted,`
  $wave21LatticeIndependent
```

The submitted/independent suites pass respectively 15/18 and 12/16 tests.
The four expected replay hashes, in command order, are

```text
2d51c827f822183c7c3cfea60e429ae550c2d95270c76f2a5f469371e71b4ce8
5150e0047e09cca5b09c15eb7d5a740ff6e0f1bf4291a7a4de0db61120da25af
18235cf32229bcdf1616a7560aa2389c830e7e23fa25f0a0fc02377c174dc53b
735ff677e7837f14ec2a52cbccd827d30abc5eee68ee5e4f8e2bd6a9e5bd21b1
```

The local package verifies `q(T)<=8` and
`tr(A4^2)>=26460` at `n3=705`; its scalar and spectral survivors are
relaxations only. The lattice package verifies the necessary endpoint
condition `h in {1,9}` while leaving `h` undetermined. Neither package
changes the unconditional project bound or target status.

Replay the Wave 22 complete order-seven aggregate deck witness:

```powershell
$wave22ReplayStem = [guid]::NewGuid().ToString('N')
$wave22ReplayRoot = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave22-seven-deck-$wave22ReplayStem"
New-Item -ItemType Directory -Path $wave22ReplayRoot | Out-Null

.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave22-full-seven-deck -p test_exact_check.py -v
.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\wave22-full-seven-deck `
  -p test_independent_verify.py -v

$wave22Submitted = Join-Path $wave22ReplayRoot "submitted.json"
$wave22Independent = Join-Path $wave22ReplayRoot "independent.json"
.venv\Scripts\python.exe -B `
  attempts\wave22-full-seven-deck\exact_check.py `
  --output $wave22Submitted
.venv\Scripts\python.exe -B `
  verification\wave22-full-seven-deck\independent_verify.py `
  --output $wave22Independent

Get-FileHash -Algorithm SHA256 $wave22Submitted,$wave22Independent
```

The submitted and independent suites pass 15/15 and 26/26. Expected result
hashes are:

```text
ca5d9d116f6a9d6e355600429652e2bf4474b73dcf281bbcb564420d820acbd2
54a02ffda9fe13293d6732fc6bf51f47e28a876a92ebdece10dea187ae0d020c
```

Both programs reconstruct the 62-by-208 deletion system and verify all 62
rows and all 19 pinned Hamiltonian counts at `n3=705,h11=2820`. The
nonnegative integer vector is only an aggregate count-system witness; it is
not a graph.

Replay the primary Wave 23 endpoint exclusion:

```powershell
$wave23ReplayStem = [guid]::NewGuid().ToString('N')
$wave23ReplayRoot = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave23-index-$wave23ReplayStem"
New-Item -ItemType Directory -Path $wave23ReplayRoot | Out-Null

.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave23-index-pranks -p test_exact_check.py -v
.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\wave23-index-pranks `
  -p test_independent_check.py -v

$wave23Submitted = Join-Path $wave23ReplayRoot "submitted.json"
$wave23Independent = Join-Path $wave23ReplayRoot "independent.json"
.venv\Scripts\python.exe -B `
  attempts\wave23-index-pranks\exact_check.py `
  --output $wave23Submitted
.venv\Scripts\python.exe -B `
  verification\wave23-index-pranks\independent_check.py `
  --output $wave23Independent

Get-FileHash -Algorithm SHA256 $wave23Submitted,$wave23Independent
```

The submitted and independent suites pass 15/15 and 14/14. Expected result
hashes are:

```text
64bf8192018376961ec88562d64928f73514697000c73cbf79a4a2a2def923b5
5ddcc8f5dec1b9923e4c28d60fb998858f33a99e659b451632641f6cea62701b
```

The independent verifier also checks all 20 entries in
`verification/wave23-index-pranks/artifact-manifest.sha256`. The verified
scope is the conditional exclusion `n3!=705`, hence `n3>=708` and
`induced_C6_count>=209994`; target existence remains `UNKNOWN`.

The separately developed shorter Wave 23 cross-check can be replayed with:

```powershell
$wave23CrossStem = [guid]::NewGuid().ToString('N')
$wave23CrossResult = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave23-cross-$wave23CrossStem.json"
$wave23CrossIndependent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave23-cross-independent-$wave23CrossStem.json"

.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave23-endpoint-crosscheck -p test_exact_check.py -v
.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\wave23-endpoint-crosscheck `
  -p test_independent_check.py -v
.venv\Scripts\python.exe -B `
  attempts\wave23-endpoint-crosscheck\exact_check.py `
  --output $wave23CrossResult
.venv\Scripts\python.exe -B `
  verification\wave23-endpoint-crosscheck\independent_check.py `
  --output $wave23CrossIndependent
Get-FileHash -Algorithm SHA256 `
  $wave23CrossResult,$wave23CrossIndependent
```

The corrected candidate and independent suites pass 25/25 and 17/17. Expected
result hashes are:

```text
1b31074d0fe4872c14caf1e25842377e4ddab9860f241d87d2814a350ac100a4
69fc4ee307e45f2f4a4ccf1d41817636d38c92d5094080e938ecad66d7d24693
```

The cross-check reaches the same endpoint exclusion using the exact
Maclaurin bound `det(B)<43`. The first verifier audit preserves the original
candidate snapshot and records a nonblocking invalid hostile control; the
separate correction addendum verifies the corrected control and confirms that
the mathematical result is unchanged.

The current-head correction manifest has SHA-256

```text
43bcb9fe593e1c16fbeb0a130d7a064ed7d019d688624ea99302a586abbfc6cf
```

and all 13 entries in
`verification/wave23-endpoint-crosscheck/correction-artifact-manifest.sha256`
must match. The original `artifact-manifest.sha256` is intentionally frozen
to the pre-correction candidate bytes; do not use its candidate-file entries
as a current-head integrity check.

Replay the Wave 23 orbit-refined weighted-extension result:

```powershell
$wave23WeightedStem = [guid]::NewGuid().ToString('N')
$wave23WeightedSubmitted = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave23-weighted-submitted-$wave23WeightedStem.json"
$wave23WeightedIndependent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave23-weighted-independent-$wave23WeightedStem.json"

python -B -m unittest discover `
  -s attempts\wave23-weighted-extensions `
  -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave23-weighted-extensions `
  -p test_independent_verifier.py -v
python -B attempts\wave23-weighted-extensions\exact_check.py `
  --output $wave23WeightedSubmitted
python -B verification\wave23-weighted-extensions\independent_verifier.py `
  --output $wave23WeightedIndependent
Get-FileHash -Algorithm SHA256 `
  $wave23WeightedSubmitted,$wave23WeightedIndependent
```

The discovery and independent suites pass 18/18 and 20/20. Expected result
hashes are:

```text
83a41b78eac02d845650ccdcb5b9782aba80caff9bdb7be983ec3f9e91c65b4c
fecd813402ddb3aabd2434833f020edaf11e82c4392fc6ecc7d1f300b7d97eb4
```

All nine entries in
`verification/wave23-weighted-extensions/artifact-manifest.sha256` must
match; the manifest itself has SHA-256
`0de03a8000cdb83aa6c1c7dfbd5162c37459f3da5e033c0f63ff98f08bdd4cd6`.
The verified statement is exact feasibility of the encoded 712-by-208
necessary count relaxation for every allowed historical-endpoint parameter,
not overlap consistency, a graph construction, or a bound change.

Replay the Wave 24 `n3=708` index-boundary result:

```powershell
$wave24Stem = [guid]::NewGuid().ToString('N')
$wave24Submitted = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave24-submitted-$wave24Stem.json"
$wave24Independent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave24-independent-$wave24Stem.json"
$wave24Survivor = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave24-survivor-$wave24Stem.json"

python -B -m unittest discover `
  -s attempts\wave24-n3-708-index -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave24-n3-708-index `
  -p test_independent_check.py -v
python -B attempts\wave24-n3-708-index\exact_check.py `
  --output $wave24Submitted
python -B verification\wave24-n3-708-index\independent_check.py `
  --output $wave24Independent `
  --matrix-certificate $wave24Survivor
Get-FileHash -Algorithm SHA256 `
  $wave24Submitted,$wave24Independent,$wave24Survivor
```

The submitted and independent suites pass 15/15 and 17/17. Expected hashes
are:

```text
a4241cdeea64a8f6073037d564e72fb7ef545287d45aca4759cec6c31d26a463
726807402388c02909171a689f3a7fe2d8d1b74307c24e322ae013d0a9cd486a
a217ec7211128f51e684030a7fe8d3c60ac80935f356ba5193dc34d36d4077a2
```

All ten entries in
`verification/wave24-n3-708-index/artifact-manifest.sha256` must match; the
manifest itself has SHA-256
`36b3a3b39264e502346960acf00e2b1e054bda88b21ec1559c9076dd340edb84`.
The verified result restricts the endpoint to eight arithmetic index values
and verifies an abstract `h=9` lattice survivor. It does not exclude
`n3=708` or construct the projector or graph.

Replay the Wave 25 strict endpoint refinement:

```powershell
$wave25Stem = [guid]::NewGuid().ToString('N')
$wave25Submitted = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave25-submitted-$wave25Stem.json"
$wave25Independent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave25-independent-$wave25Stem.json"

python -B -m unittest discover `
  -s attempts\wave25-n3-708-strictness -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave25-n3-708-strictness `
  -p test_independent_check.py -v
python -B attempts\wave25-n3-708-strictness\exact_check.py `
  --output $wave25Submitted
python -B verification\wave25-n3-708-strictness\independent_check.py `
  --output $wave25Independent
Get-FileHash -Algorithm SHA256 $wave25Submitted,$wave25Independent
```

The submitted and independent suites pass 21/21 and 18/18. Expected hashes
are:

```text
6da9200adf19a5305913178c271ac584e9825aa4f3594fad20717f9418d2b40e
8c147d7b9da422c9d9b3d646015d95d737efc57d81964fabb3b33574a1d69f77
```

All six entries in
`verification/wave25-n3-708-strictness/artifact-manifest.sha256` must match;
the manifest itself has SHA-256
`473601e70d6c873e1b691d8fcf7c769d907ae2a9eadff198d72e0936e9fcc1ce`.
All four entries in
`verification/wave25-literature-audit/publication-hashes.sha256` must match;
that manifest has SHA-256
`df3621eefa727aac0a75e8562b31dcfda0c4eec313dcdb0bd5e2f3704941d395`.

The verifier reproduces `tr(C^2)>=10`, `tr(B^2)>=116`, and the combined
necessary cap `det(B)<=6525`, while preserving the exact abstract
`h=9`, `det(B)=81` survivor. The result does not exclude `n3=708`, construct
a projector or graph, improve the headline `n3>=708` bound, or resolve
Conway-99.

The detached incremental replay is recorded in
`verification/2026-07-23-wave25-clean-clone.md`. At integration commit
`156756d4ef98dc7233e29a7f8c9feeb143548197`, it passes all 39 Wave 25 tests,
regenerates both exact JSON files byte-identically, checks both manifests and
all 129 status path/hash pairs, scans the release tree and all four commits
after the prior public checkpoint for credential-shaped or private-path
payloads, and finishes with a clean tracked tree and
`git fsck --full --strict`.

Replay the two Wave 26 `A2` obstructions and their independent verifiers:

```powershell
$wave26Stem = [guid]::NewGuid().ToString('N')
$wave26FrameSubmitted = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave26-frame-submitted-$wave26Stem.json"
$wave26FrameIndependent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave26-frame-independent-$wave26Stem.json"
$wave26CubicSubmitted = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave26-cubic-submitted-$wave26Stem.json"
$wave26CubicIndependent = Join-Path ([System.IO.Path]::GetTempPath()) `
  "wave26-cubic-independent-$wave26Stem.json"

python -B -m unittest discover `
  -s attempts\wave26-a2-frame-obstruction -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave26-a2-frame-obstruction `
  -p test_independent_check.py -v
python -B -m unittest discover `
  -s attempts\wave26-a2-cubic-obstruction -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave26-a2-cubic-obstruction `
  -p test_independent_check.py -v

python -B attempts\wave26-a2-frame-obstruction\exact_check.py `
  --output $wave26FrameSubmitted
python -B verification\wave26-a2-frame-obstruction\independent_check.py `
  --output $wave26FrameIndependent
python -B attempts\wave26-a2-cubic-obstruction\exact_check.py `
  --output $wave26CubicSubmitted
python -B verification\wave26-a2-cubic-obstruction\independent_check.py `
  --output $wave26CubicIndependent

Get-FileHash -Algorithm SHA256 `
  $wave26FrameSubmitted,$wave26FrameIndependent,`
  $wave26CubicSubmitted,$wave26CubicIndependent
```

The four suites pass 15/15, 14/14, 19/19, and 17/17. Expected generated
hashes, in the same order, are:

```text
bb2b2ffe33d0ca6a0a1f18be8b36c48060d40aef2fc6e0857fd1d23c18e84bb9
b664844d65ab553cfd2277e925f5596193c586378d880dc1a29242cb9ac8f03b
acc3ce7298c164bdee1fe32766bf18437fe79770ee69090b759d3dc774640f33
658b7eb7eec64a4560d20e9c7b272c428168876c43910d9af6e44035dde12352
```

All eight entries in
`verification/wave26-a2-frame-obstruction/artifact-manifest.sha256` must
match; the manifest SHA-256 is
`dc12aeacd906d5b7f54fca3de796ca95d829385ac3a901dbf9760ee4aed3550c`.
All nine entries in
`verification/wave26-a2-cubic-obstruction/artifact-manifest.sha256` must
match; the manifest SHA-256 is
`75572e7f356312e2f4aee94ecaa5032f7d2bfdfd530f989a9e36fd39da63f842`.
All nine entries in
`verification/wave26-literature-audit/manifest.sha256` must match; the
manifest SHA-256 is
`0d9381d47a33fa376c53510cae2a57dfd419a41bb96658b56ce7cb624d953816`.

The frame route proves the exact `21>18` root-fibre contradiction. The cubic
route independently proves `tr(A2 Q_AA)>=18`, while each explicit survivor
block has trace ten. Together they exclude the required projector-frame and
full Schur-square origins of the one `E8^5 orthogonal-sum A2^2` hostile
control. They do not classify all `h=9` forms, exclude `n3=708`, improve the
headline `n3>=708` bound, or resolve Conway-99.

The detached incremental replay is recorded in
`verification/2026-07-23-wave26-clean-clone.md`. At integration commit
`4f1f3be35e712789dcba10fda5ec8d2bc569bc17`, it passes all 65 Wave 26 tests,
regenerates four exact JSON files byte-identically, checks all three
manifests, 60 claims, 54 obligations, 151 status hashes, 172 local links, 47
BibTeX keys, and 50 LF-only Wave 26/central files. Exact-blob scans of the
integration tree and all three commits after public baseline `930cb99` find
zero credential-shaped or private-path payloads. The detached clone finishes
with a clean tracked tree and `git fsck --full --strict`.

Replay the seven Wave 27 discovery and independent-verification suites:

```powershell
$wave27Stem = [guid]::NewGuid().ToString('N')
$wave27Temp = [System.IO.Path]::GetTempPath()
$wave27A2FreeSubmitted = Join-Path $wave27Temp `
  "wave27-a2free-submitted-$wave27Stem.json"
$wave27A2FreeIndependent = Join-Path $wave27Temp `
  "wave27-a2free-independent-$wave27Stem.json"
$wave27E6TraceSubmitted = Join-Path $wave27Temp `
  "wave27-e6-trace-submitted-$wave27Stem.json"
$wave27E6TraceIndependent = Join-Path $wave27Temp `
  "wave27-e6-trace-independent-$wave27Stem.json"
$wave27TensorSubmitted = Join-Path $wave27Temp `
  "wave27-tensor-submitted-$wave27Stem.json"
$wave27A20Submitted = Join-Path $wave27Temp `
  "wave27-a20-submitted-$wave27Stem.json"
$wave27TensorIndependent = Join-Path $wave27Temp `
  "wave27-tensor-independent-$wave27Stem.json"
$wave27Generated = @(
  $wave27A2FreeSubmitted,
  $wave27A2FreeIndependent,
  $wave27E6TraceSubmitted,
  $wave27E6TraceIndependent,
  $wave27TensorSubmitted,
  $wave27A20Submitted,
  $wave27TensorIndependent
)

function Assert-Wave27ByteEqual {
  param(
    [Parameter(Mandatory = $true)][string]$Expected,
    [Parameter(Mandatory = $true)][string]$Actual
  )
  $expectedBytes = [Convert]::ToBase64String(
    [System.IO.File]::ReadAllBytes((Resolve-Path $Expected))
  )
  $actualBytes = [Convert]::ToBase64String(
    [System.IO.File]::ReadAllBytes($Actual)
  )
  if ($expectedBytes -cne $actualBytes) {
    throw "Byte mismatch: $Expected versus $Actual"
  }
}

try {
  python -B -m unittest discover `
    -s attempts\wave27-a2free-construction -p test_exact_check.py -v
  python -B -m unittest discover `
    -s verification\wave27-a2free-construction `
    -p test_independent_check.py -v
  python -B -m unittest discover `
    -s attempts\wave27-h9-classification -p test_exact_check.py -v
  python -B -m unittest discover `
    -s verification\wave27-h9-classification `
    -p test_independent_check.py -v
  python -B -m unittest discover `
    -s attempts\wave27-general-root-tensor -p test_exact_check.py -v
  python -B -m unittest discover `
    -s attempts\wave27-a20-trace-addendum -p test_exact_check.py -v
  python -B -m unittest discover `
    -s verification\wave27-general-root-tensor `
    -p test_independent_check.py -v

  python -B attempts\wave27-a2free-construction\exact_check.py `
    --output $wave27A2FreeSubmitted
  python -B verification\wave27-a2free-construction\independent_check.py `
    --output $wave27A2FreeIndependent
  python -B attempts\wave27-h9-classification\exact_check.py `
    --output $wave27E6TraceSubmitted
  python -B verification\wave27-h9-classification\independent_check.py `
    --output $wave27E6TraceIndependent
  python -B attempts\wave27-general-root-tensor\exact_check.py `
    --output $wave27TensorSubmitted
  python -B attempts\wave27-a20-trace-addendum\exact_check.py `
    --output $wave27A20Submitted
  python -B verification\wave27-general-root-tensor\independent_check.py `
    --output $wave27TensorIndependent

  Assert-Wave27ByteEqual `
    attempts\wave27-a2free-construction\exact-results.json `
    $wave27A2FreeSubmitted
  Assert-Wave27ByteEqual `
    verification\wave27-a2free-construction\independent-results.json `
    $wave27A2FreeIndependent
  Assert-Wave27ByteEqual `
    attempts\wave27-h9-classification\exact-results.json `
    $wave27E6TraceSubmitted
  Assert-Wave27ByteEqual `
    verification\wave27-h9-classification\independent-results.json `
    $wave27E6TraceIndependent
  Assert-Wave27ByteEqual `
    attempts\wave27-general-root-tensor\exact-results.json `
    $wave27TensorSubmitted
  Assert-Wave27ByteEqual `
    attempts\wave27-a20-trace-addendum\exact-results.json `
    $wave27A20Submitted
  Assert-Wave27ByteEqual `
    verification\wave27-general-root-tensor\independent-results.json `
    $wave27TensorIndependent

  Get-FileHash -Algorithm SHA256 $wave27Generated
}
finally {
  Remove-Item -LiteralPath $wave27Generated -Force -ErrorAction SilentlyContinue
}
```

The suites pass, in command order, 15/15, 16/16, 16/16, 21/21, 17/17,
8/8, and 23/23: 116 tests total. The generated files are byte-identical to
their seven stored JSON counterparts. Their expected SHA-256 values, in the
same order, are:

```text
3b1d30b6110d937f1bd4bb9ff570419625063afc5c0915382baa2466d349946d
ee0b100806de66252a9795622881adb5651e5b46f8ae0b5757fc15874257e31f
377b4edc9498ad71cb655f084970aed234ea809c8413643cb5e9cfd03b75fde2
4b0532842e506cb5de4e8d131c48da6d078be7d69b459af50b3207a8900d788a
98aba5a30b2f3a83b9f6ce6fd6a20458505b668249d97b0810907de50cae678d
dc5716cbf2537cd214906f1bf2eae96d4886e4bd88008cd7508c6a64d78f089c
7e87796980a43df199713865fed920bc094778f1828431a673938484c026e6fd
```

The six Wave 27 manifests below must validate from their containing
directories:

| package | entries | manifest SHA-256 |
|---|---:|---|
| `attempts/wave27-general-root-tensor` | 7 | `3ba7ee4683dfac361b6f2d1b09a90d485210e2debd87cbe9d4ecb62f607ebf32` |
| `attempts/wave27-a20-trace-addendum` | 7 | `8f8ef9538a4070d569cfd4415296206214af3d3b2d8fe136ec7536257ead9949` |
| `verification/wave27-a2free-construction` | 8 | `a4ab58cf5f2e1f7cd635b4ec7d7dca801d878b4ce596e85d161c2a2b7c2c1023` |
| `verification/wave27-h9-classification` | 8 | `7b9584b72e59bfeff8430cfe13b2eac8b08e02481eac7c89219cfb454332686f` |
| `verification/wave27-general-root-tensor` | 11 | `e72b134623d95ea054b348b641ca23a57ee7d29b5edd8033527cca1f8c68914c` |
| `verification/wave27-literature-audit` | 10 | `f439b850eeecbb519208200aa908434a3d7908faff9021694c6fcd3f2aeadfe1` |

The replays verify an abstract `E8^4 orthogonal-sum E6^2` arithmetic
survivor, the unrestricted local `E6` trace minimum 14, the stronger
frame/Schur cubic exclusions for orthogonal `E6` and `A6` summands, and the
separate `A20` trace addendum. Combined with the Wave 26 `A2` result, they
exclude a full orthogonal ADE endpoint form under the stated projector/Schur
premises. They do not classify general even rank-44 forms, exclude `n3=708`,
improve the headline `n3>=708` bound, resolve Conway-99, or establish novelty.

The detached Wave 27 publication replay is
`verification/2026-07-24-wave27-clean-clone.md`. At integration commit
`4a2f65d20f8fa403a3a245815799070cf126173f`, it passes all 116 tests,
regenerates seven JSON files byte-identically, validates all 51 entries in
six manifests, checks 65 claims, 59 obligations, 211 status path/hash pairs,
205 scoped local links, 52 unique BibTeX keys, and 81 LF-only Wave 27/central
files. Exact-blob scans cover 761 release-tree files and all 77 new blobs
across the seven-commit unpublished range with zero credential-shaped or
private-path findings. The detached clone finishes clean, and
`git fsck --full --strict` returns success.

## Wave 28 unrestricted-lattice controls

Replay the five Wave 28 discovery and independent-verification suites:

```powershell
python -B -m unittest discover `
  -s attempts\wave28-glue-discriminant -p test_exact_check.py -v
python -B -m unittest discover `
  -s attempts\wave28-theta-modular -p test_exact_check.py -v
python -B -m unittest discover `
  -s verification\wave28-glue-discriminant `
  -p test_independent_check.py -v
python -B -m unittest discover `
  -s verification\wave28-theta-modular `
  -p test_independent_check.py -v
python -B -m unittest discover `
  -s verification\wave28-simultaneous-neighbor `
  -p test_independent_check.py -v
```

The suites pass `13`, `14`, `16`, `20`, and `25` tests respectively: 88
tests total. The theta unit tests validate the stored complete shell
certificate without repeating the 15-million-node enumeration.

Regenerate all five mathematical JSON files outside the checkout:

```powershell
$wave28Generated = Join-Path `
  ([IO.Path]::GetTempPath()) `
  ("conway-wave28-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $wave28Generated | Out-Null

function Assert-Wave28ByteEqual {
  param([string]$Expected, [string]$Actual)
  $left = [IO.File]::ReadAllBytes((Resolve-Path $Expected))
  $right = [IO.File]::ReadAllBytes((Resolve-Path $Actual))
  if (-not [System.Linq.Enumerable]::SequenceEqual($left, $right)) {
    throw "byte mismatch: $Expected versus $Actual"
  }
}

try {
  $glueSubmitted = Join-Path $wave28Generated "glue-submitted.json"
  $thetaSubmitted = Join-Path $wave28Generated "theta-submitted.json"
  $glueIndependent = Join-Path $wave28Generated "glue-independent.json"
  $thetaIndependent = Join-Path $wave28Generated "theta-independent.json"
  $neighborIndependent = Join-Path $wave28Generated "neighbor-independent.json"

  python -B attempts\wave28-glue-discriminant\exact_check.py `
    --output $glueSubmitted
  python -B attempts\wave28-theta-modular\exact_check.py `
    --output $thetaSubmitted
  python -B verification\wave28-glue-discriminant\independent_check.py `
    --output $glueIndependent
  python -B verification\wave28-theta-modular\independent_check.py `
    --output $thetaIndependent
  python -B verification\wave28-simultaneous-neighbor\independent_check.py `
    --output $neighborIndependent

  Assert-Wave28ByteEqual `
    attempts\wave28-glue-discriminant\exact-results.json `
    $glueSubmitted
  Assert-Wave28ByteEqual `
    attempts\wave28-theta-modular\exact-results.json `
    $thetaSubmitted
  Assert-Wave28ByteEqual `
    verification\wave28-glue-discriminant\independent-results.json `
    $glueIndependent
  Assert-Wave28ByteEqual `
    verification\wave28-theta-modular\independent-results.json `
    $thetaIndependent
  Assert-Wave28ByteEqual `
    verification\wave28-simultaneous-neighbor\independent-results.json `
    $neighborIndependent
}
finally {
  Remove-Item -LiteralPath $wave28Generated -Recurse -Force `
    -ErrorAction SilentlyContinue
}
```

The expected SHA-256 values, in the same order, are:

```text
13a3bb8f83c56ff899991362736089b772114cff840a2cb20d68845e231b3cf1
9d7b1ffcc0cef2441aa6dd381228abaa1018f721594e930cdd7227c0647470d6
0d15724c772300072c565030e88080c05333af8f75241b633d5801e5c4ac83fe
24298ae282c7baa252a39ffe96fc37b7c696cb51f14b9ddea2318a59b4335b7f
d9f6829dc967fb3777f541b4fd16cd27acb3478d96479b8ad9c3e9fbad2afedd
```

The six Wave 28 manifests validate 46 entries:

| package | entries | manifest SHA-256 |
|---|---:|---|
| `attempts/wave28-glue-discriminant` | 7 | `5ac509e960c3b2e5e8b949aa88958f9bce6ae7b5b34a7baad140d20d3487bcbb` |
| `attempts/wave28-theta-modular` | 8 | `1a7a68019241b5f83b4f9154a1361d1ebcf8da72d287175a13e8400b83b07692` |
| `verification/wave28-glue-discriminant` | 4 | `d25e446673fcb80cb21afc87cd1f271c4c5e4d6d36f6ec6a564e7d6fbb2296a7` |
| `verification/wave28-theta-modular` | 10 | `50a5e3d4b5bb066b4b281c80d6d2caa0906afc21b9de99e12731177f661c6fed` |
| `verification/wave28-simultaneous-neighbor` | 7 | `068d9270a83b0d99a39bbc8cda8a18773c62d5899fcba202c42755f79145e985` |
| `verification/wave28-literature-audit` | 10 | `102bb4e5200a1a62dee8b8094b2b32b594d18067deef61508eae377d4db2898f` |

The exact theta replay is offline by default and uses the attributed,
hash-bound numeric matrices in `catalogue-data.json`. The optional live
source refresh rewrites `source-manifest.json` with the new access timestamp,
so run it only in a disposable clone. To refetch the two catalogue pages,
verify their frozen response hashes, parse the matrix data, and discard the
HTML, run there:

```powershell
$wave28RefreshOutput = Join-Path `
  ([IO.Path]::GetTempPath()) `
  ("conway-wave28-refresh-" + [guid]::NewGuid().ToString("N") + ".json")
python -B verification\wave28-theta-modular\independent_check.py `
  --refresh-sources `
  --output $wave28RefreshOutput
Remove-Item -LiteralPath $wave28RefreshOutput -Force
```

This optional command requires network access and deliberately fails closed
on source drift. Its refreshed `source-manifest.json` should be treated as
new evidence and reviewed before retention. The public package contains no
copied HTML or paper.

The verified Wave 28 scope is limited to corrected necessary
discriminant/glue and theta restrictions, a rootless bare `S/G` control, and
two abstract simultaneous-neighbor controls. It does not classify general
rank-44 forms, construct `X,M,W,Q,B`, exclude `n3=708`, improve the
`n3>=708` bound, resolve Conway-99, or establish novelty.

The combined detached clean-source replay for Waves 21-24 is recorded in
`verification/2026-07-23-wave24-clean-clone.md`. It runs 278 submitted and
independent tests, regenerates 15 exact files from 14 commands, checks seven
publication manifests and the 108 status path/hash pairs present at the
replayed commit, scans both the release tree and all unpublished Git history
for credential-shaped or private-path payloads, and finishes with a clean
tracked tree and `git fsck --full --strict`.

The separate `attempts/wave20-n3-63-structural` package is archival. Its
14/14 tests and exact JSON replay pass, but its proof remains
`DERIVED_PENDING_INDEPENDENT_AUDIT`; the first false two-profile census is
retained as `REJECTED`, and the repaired census contains 18 profiles. The
verified global theorem numerically supersedes that lane without certifying
its derivation.

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
