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

## `N3=33` equality exclusion

`n3-33-equality/verify.py` checks the Wave 9 classification-free proof's
finite steps: both active-`q` profiles, the labeled singleton crossing
obstruction, the point-size equations, the forced local `K5`, every residual
`K6`-minus-matching choice, and the strengthened global and branch bounds.

```powershell
python verification/n3-33-equality/verify.py
python -m unittest verification.test_n3_33_equality -v
```

Two optional standard-library programs give a materially different exhaustive
audit. They enumerate all 266 quartic types on eleven vertices and all 610
admissible point-clique families; the second program independently
canonicalizes the graph types, regenerates the family set with a different
recursion, checks every contradiction witness, and rejects certificate
mutations. The connected catalog is an external House of Graphs/Meringer
input, so it is attributed and hashed rather than redistributed.

```powershell
$wave9Catalog = Join-Path ([System.IO.Path]::GetTempPath()) "11_4_3.g6.gz"
$wave9Certificate = Join-Path ([System.IO.Path]::GetTempPath()) "n3-33-audit.json"
$wave9Replay = Join-Path ([System.IO.Path]::GetTempPath()) "n3-33-replay.json"
Invoke-WebRequest `
  -Uri "https://houseofgraphs.org/data/quartics/11_4_3.g6.gz" `
  -OutFile $wave9Catalog
(Get-FileHash $wave9Catalog -Algorithm SHA256).Hash.ToLower()
python verification/n3-33-equality/audit_exhaustive.py `
  --catalog $wave9Catalog --certificate $wave9Certificate `
  --git-commit 19f27d1ede9cdb0b4110540f52eeb3ad9c94cc94
python verification/n3-33-equality/verify_exhaustive.py `
  --catalog $wave9Catalog --certificate $wave9Certificate `
  --output $wave9Replay
```

The expected compressed catalog hash is
`05ee6bb0c2b40d63d5c44efc8e89ed1c0a381a170d81a3d052749c8edf6b14fd`.
Exact deterministic census digests and the external-source boundary are in
`n3-33-equality/n3-33-census-manifest.json`. The resulting `n3>=36` remains a
conditional necessary bound, not a Conway-99 resolution.

## `N3=36` equality exclusion

`n3-36-equality/verify.py` checks the Wave 10 proof's finite steps: all three
active profiles, singleton forcing, local point types and crossings, the
common-point obstructions, all seventy labeled cubic graphs on six vertices,
the rook-graph parameters, the line-graph-twin endpoint configuration, the
three forced triangle-group pairings, and the strengthened bounds.

```powershell
python verification/n3-36-equality/verify.py
python -m unittest verification.test_n3_36_equality -v
```

The committed support certificate is a separate finite audit of the sole
all-size-two `2K6` branch. The primary program decomposes the degree-two
bipartite supports into two permutation matchings. The independent verifier
constructs the complementary matching recursively and imports no code from
the primary implementation. Both recover exactly 216 masks with SHA-256
`6659fe1972cbacc6980a9792557714730572817b43224b5f1fac24bb0c4ca61a`.
Every abstract mask passes the auxiliary-`H` checks and has eighteen decisive
original-SRG rook-saturation violations.

```powershell
python verification/n3-36-equality/verify_support.py `
  --certificate verification/n3-36-equality/n3-36-support.json
python -m unittest verification.test_n3_36_support -v
```

To regenerate a scratch certificate from the technical commit:

```powershell
$wave10Certificate = Join-Path ([System.IO.Path]::GetTempPath()) "n3-36-support.json"
python verification/n3-36-equality/audit_support.py `
  --certificate $wave10Certificate `
  --git-commit 2194c2b68ebd5c34491d64f15d30f1a3597baa74
python verification/n3-36-equality/verify_support.py `
  --certificate $wave10Certificate
```

The reduction from a putative graph to this finite domain is human-checked and
recorded separately. The census is not a standalone Conway-99 certificate.
The resulting `n3>=39` is a conditional necessary bound, and the target remains
`UNKNOWN`.
