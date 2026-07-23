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

## Mature LRAT calibration

The external proof path is calibrated separately with pinned CaDiCaL 3.0.1,
`drat-trim`, and `lrat-check` source commits. Both complete `pair_count=3`
branch-unit CNFs were accepted after DRAT-to-LRAT conversion. Exact versions,
commands, artifact hashes, and the target-scope warning are recorded in
`2026-07-22-lrat-calibration.md`.

This calibration does not make an embedded-solver `UNSAT` result evidentiary.
A target claim still requires retained proofs for a proved complete cover and
independent replay of every artifact.

## Conditional `N3` joint-cover checker

`n3-joint-cover/verify.py` is a standard-library verifier for the strict JSON
certificate describing the 12 matching orbits after canonical `N3`
normalization. It independently enumerates the full rooted scaffold
stabilizer, all 945 compatible matchings, orbit-stabilizer products, a Burnside
checksum, the legacy-fiber diagnostic, and SAT literal numbering.

```powershell
python verification/n3-joint-cover/verify.py
python verification/n3-joint-cover/verify.py `
  verification/n3-joint-cover/n3-joint-cover.json
```

The parser rejects duplicate keys, booleans masquerading as integers, unknown
fields, and non-standard JSON constants. This certificate proves only the
conditional finite branch cover. It neither establishes the upstream `N3`
occurrence theorem nor solves a target branch.

## Conditional refined `N3` checker

`n3-refined-cover/verify.py` independently reconstructs the order-768 parent
stabilizer, its twelve matching orbits, the order-384 oriented subgroup, and
all 78 orbits on the `945 * 11 = 10,395` refined states. It also derives the
forced coordinate profile, rebuilds SAT literal numbering, checks every
orbit-stabilizer product and a Burnside sum of 29,952, and enforces a strict
JSON schema.

```powershell
python verification/n3-refined-cover/verify.py
python verification/n3-refined-cover/verify.py `
  verification/n3-refined-cover/n3-refined-cover.json
```

The checker uses only the Python standard library and does not import search
code. Its `PASS` establishes the conditional symmetry case split only; it is
not a SAT/UNSAT result for any branch.

## `N3` count-bound checker

`n3-count-bound/verify.py` checks the exact arithmetic behind the auxiliary
opposite-edge graph consequence. It exhausts the sub-24 degree-sequence cases,
enumerates every forced local model for the remaining 18-edge case, rebuilds
the twelve branch degree/signature table from the verified joint certificate,
enumerates all 10,395 perfect matchings, and independently derives the
normalized six-vertex boundary profile.

```powershell
python verification/n3-count-bound/verify.py
```

The accompanying human proof establishes why the auxiliary graph has the
properties checked by the script. The resulting `n3 >= 24` is conditional on
the target-specific theorem forcing an `N3`; it is a necessary bound, not a
resolution of Conway-99.

## `N3` side-incidence checkers

`n3-side-incidence/verify.py` checks the Wave 7 active-triangle reduction and
explicitly enumerates the complement-component point patterns forced by
`n3=24` and `n3=27`. `n3-side-incidence/audit_generic.py` is a separate
implementation that generates every clique family, permits unused complement
edges, enforces disjoint intersection resources, and adds singleton fillers.

```powershell
python verification/n3-side-incidence/verify.py
python verification/n3-side-incidence/audit_generic.py
```

Both reproduce support maxima `6`, `9`, and `8`, giving the conditional
necessary bound `n3>=30`. The human proof supplies the upstream graph-theoretic
reduction; neither finite checker is a Conway-99 existence or nonexistence
certificate.

## `N3=30` equality exclusion

`n3-equality/verify.py` checks the exact arithmetic accompanying the Wave 8
classification-free proof: the unique ten-triangle `q=2` equality profile,
the fixed-endpoint count four, the point-size equations, the cubic component
orders, the forbidden internal crossing, and the strengthened global and
branch-local bounds.

```powershell
python verification/n3-equality/verify.py
python -m unittest verification.test_n3_equality -v
```

`n3-equality/audit_exhaustive.py` is an optional slow, solver-free secondary
audit archived verbatim from an independent lane. It generates every
normalized labeled cubic graph on ten vertices, recovers all 21 isomorphism
types, enumerates 674,880 point-clique families, and checks the committed JSON
certificate byte-for-byte. A replay takes about five minutes under the pinned
environment.

```powershell
python verification/n3-equality/audit_exhaustive.py `
  --check verification/n3-equality/n3-30-audit.json
```

The human derivation and adversarial audit establish why these finite
conditions follow from the Wave 6/7 framework. The resulting `n3>=33` is a
conditional necessary bound; it does not resolve Conway-99.
