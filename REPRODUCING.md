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
