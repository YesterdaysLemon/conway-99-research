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
Conway-99 remains `UNKNOWN`.

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
