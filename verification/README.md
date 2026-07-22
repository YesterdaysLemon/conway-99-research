# Independent verification

Verification code must be small, deterministic, exact, and independent of the
search implementation where practical. Reports should include commands,
versions, hashes, expected failures on mutated fixtures, and a clear verdict.

## Baseline validator

`check_srg.py` accepts a strict `srg-edge-list-v1` JSON certificate. It uses
only the Python standard library and validates the graph twice: first with
adjacency-set intersections, then by evaluating the integer adjacency-matrix
identity entry by entry. The parser rejects duplicate object keys, unknown or
case-varied keys, Boolean endpoints, loops, and duplicate undirected edges.

Calibrate it on the 3-by-3 rook graph, an `srg(9,4,1,2)`:

```powershell
python verification/check_srg.py `
  verification/fixtures/rook-3x3.srg.json `
  --vertices 9 --degree 4 --lambda 1 --mu 2
python -m unittest discover -s verification -p "test_*.py" -v
```

The Conway defaults are `(99,14,1,2)`, so a future target certificate needs no
parameter flags.

`Check-Srg.ps1` is a second implementation. It independently parses the JSON
and checks the graph through .NET hash sets under Windows PowerShell 5.1 or
newer:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File verification/Check-Srg.ps1 `
  -Certificate verification/fixtures/rook-3x3.srg.json `
  -Vertices 9 -Degree 4 -AdjacentCommon 1 -NonadjacentCommon 2
```

## Small DRUP checker

`check_drup.py` is an independent, clarity-first checker for textual DRUP
proofs. It checks every addition by reverse unit propagation and requires a
verified empty clause. It is suitable for calibration and auditing encoder/
solver integration. A target-scale nonexistence claim should also use a mature,
pinned proof checker and preferably an LRAT conversion/check.

```powershell
python verification/check_drup.py path/to/instance.cnf path/to/proof.drup
```
