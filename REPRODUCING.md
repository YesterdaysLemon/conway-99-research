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

Validate a future Conway-format certificate using the frozen defaults:

```powershell
python verification/check_srg.py candidates/conway-99.srg.json
```

No such target certificate is currently claimed. `STATUS.yaml` remains the
authoritative machine-readable status.

`requirements-search.txt` pins the prototyping API version, but it is not an
archival proof lockfile. Before a proof-producing run, also pin the Python ABI,
wheel hashes, native solver binary, and independent checker binary, then record
their cryptographic hashes in the run manifest.

## Artifact retention

Small certificates and verification reports belong in Git. Large CNF, LRAT,
solver logs, and checkpoints should be stored in a content-addressed release or
archive. Commit a manifest containing cryptographic hashes and retrieval URLs.
Never treat an unavailable artifact as verified evidence.
