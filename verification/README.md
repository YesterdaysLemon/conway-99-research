# Independent verification

Verification code must be small, deterministic, exact, and independent of the
search implementation where practical. Reports should include commands,
versions, hashes, expected failures on mutated fixtures, and a clear verdict.
This file is a selected orientation index, not a chronologically complete
catalog of every verification artifact; the repository map and dated
subdirectories remain authoritative for omitted waves.

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

## `N3=39` equality exclusion

`n3-39-equality/verify.py` checks the Wave 11 proof's finite steps and exact
semantic witnesses: the four active profiles, singleton forcing, point-size
expansion, all `3^8` rooted size-four petal words, all `2^6` rooted
size-three words, literal forced `K`/`U` edge sets, forbidden point owners,
final parity, and the strengthened global and branch bounds.

```powershell
python verification/n3-39-equality/verify.py
python -m unittest -v verification/test_n3_39_equality.py
```

The committed local replay is a second layer. The primary generator explicitly
constructs canonical point sets, point-clique edges, singleton-forced
complement edges, and owner-intersection witnesses. The independent verifier
imports no primary code, uses integer-coded enumeration and a closed crossing
table, freezes nine stream hashes, and attacks the result with eight mutations.

```powershell
python verification/n3-39-equality/verify_local.py `
  --certificate verification/n3-39-equality/n3-39-local.json
python -m unittest -v verification/test_n3_39_local.py
```

The certificate contains 8,907 records and has combined stream SHA-256
`452850018ad13362694f5bfff2e4beac03288a113a0391c3456a47cd6fbfe9a1`.
Its canonical-LF outer JSON has SHA-256
`4cd23939cfb8ec5080b57fb0626e9579b68250a219ea17876a8e1f4066ad2261`;
the exact detached-clone replay is recorded in
`2026-07-22-wave11-clean-clone.md`.
Its premise stream explicitly binds `K=overline(L)`, 6-regularity, point-clique
membership, linearity, the common-point rule, and the degree-zero-or-two
crossing law. This remains a conditional replay companion to the human proof,
not a standalone Conway-99 nonexistence certificate. The resulting `n3>=42`
is a necessary bound and the target remains `UNKNOWN`.

## `N3=42` equality exclusion

`n3-42-equality/verify_reduction.py` independently checks the proof-side finite
steps: all six active profiles, the degree-three obstruction, both size-four
flower counts, the size-three `t` inequalities, the `(2,3,3)` fixed-point
contradiction, the cubic `K3,3`/open-twin obstruction, and the strengthened
global and branch bounds. Its bound output is guarded by an explicit external
support-exclusion premise.

```powershell
python verification/n3-42-equality/verify_reduction.py
python -m unittest -v verification/test_n3_42_reduction.py
```

The remaining all-size-two branch is checked by a separate proof-producing
support search and a set-based certificate replayer that imports neither the
builder nor the discovery code. The replay requires Meringer's official
`14_3_4.scd` archive, expected SHA-256
`6f3e9cf2b7e0d85c5df59c1638ab9d2fddbfc9905c49b35da01cc892f847e9a0`.
The archive has no stated redistribution license and is intentionally ignored;
download it from the official URL recorded in `REPRODUCING.md`.

```powershell
python verification/n3-42-equality/verify_support_certificate.py `
  --certificate verification/n3-42-equality/n3-42-support-certificate.json `
  --scd verification/n3-42-equality/14_3_4.scd `
  --graph6 attempts/wave12-computation/n3-42-cubic-trianglefree-14.g6 `
  --mutations
```

The certificate has SHA-256
`8115b5f34568a463952afc399bc22db927121f3f1aa28cfc33ae191ea93dc68a`.
The independent catalog bridge checks 110 connected and two disconnected cubic
triangle-free types; four survive the mandatory-degree filter, and all four
support rejection trees replay with zero survivors. The combined adversarial
audit records the conditional strengthening `n3>=45` and
`induced_C6_count>=209331`. It does not resolve Conway-99, and novelty remains
`UNKNOWN`. The detached full-suite replay and byte-identical regeneration are
recorded in `2026-07-22-wave12-clean-clone.md`.

## `N3=45` equality exclusion

`n3-45-equality/verify.py` independently reconstructs the nine active
profiles, mixed order-fourteen reductions, order-fifteen flower census, four
rooted modes, type-`223` parity obstruction, type-`111` saturation
obstruction, and final degree-zero-or-four handshake contradiction. Its
mutation mode attacks the imported premise boundary.

```powershell
python verification/n3-45-equality/verify.py --mutations
python -m unittest -v verification/test_n3_45_audit.py
```

`n3-45-equality-b/audit_semantics.py` is a second semantic reconstruction. It
froze `precomparison-verdict.md` before reading the first audit and then found
no disagreement. Both audits pass only the conditional equality exclusion:

```text
n3 >= 48,
induced_C6_count >= 209334,
Conway-99 = UNKNOWN,
novelty = UNKNOWN.
```

The companion SAT bundle is audited separately. The original bundle retains a
public FAIL report under `2026-07-22-wave13-computation-audit.md`. Its repaired
v2 artifacts pass `n3-45-computation-repair/independent_repair_audit.py` and
six focused regressions:

```powershell
python verification/n3-45-computation-repair/independent_repair_audit.py
python -m unittest discover `
  -s verification/n3-45-computation-repair -p 'test_*.py' -v
```

The repair audit independently reproduces all 17 formula hashes, checks the
1,141,796-clause positive diagnostic, certifies its 18 deliberately omitted
common-point violations, verifies direct artifact provenance, and rejects 31
hostile mutations. The historical 15-test suite now loads the failed baseline
directly from commit `066d9c7fcf593c3b9d35cfef1031dbd9daab4145`, while
the repaired 12-test suite exercises the current files. No negative proof
trace was emitted or checked, so every solver-negative branch remains
`UNSAT_UNVERIFIED`; none is used in the human proof. The detached clean-source
replay at `2026-07-22-wave13-clean-clone.md` records 52 code tests, 12 focused
Wave 13 tests, 104 verification tests, and byte-identical census and positive
diagnostic regeneration.

## `N3=48` frontier reduction

`n3-48-proof/independent_reconstruction.py` independently rebuilds the twelve
active profiles, inherited three-profile filter, order-fourteen and
order-fifteen mixed-profile contradictions, and order-sixteen local-mode
arithmetic. `n3-48-proof/audit_countermodel.py` separately reconstructs the
explicit all-size-two active/local/support object and attacks it with five
semantic mutations.

```powershell
python -B verification/n3-48-proof/independent_reconstruction.py
python -B verification/n3-48-proof/audit_countermodel.py `
  attempts/wave14-proof-a/all2-active-countermodel.json
```

The proof audit passes the scoped reduction to an `r=16`, all-`q=2` residual
with point sizes two or three, eight surviving size-three modes, `H`-degrees
zero or four, and exact twofold support coverage. The positive object shows
that the listed active constraints alone are not contradictory; it is not a
partial or complete Conway graph. Exclusion of `n3=48` remains `UNKNOWN` at
this checkpoint.

The computation lane is audited independently by
`n3-48-computation/independent_audit.py`. It reconstructs all thirteen formula
streams, checks the full positive candidate and two weakened controls, binds
file and semantic provenance, and rejects 29 hostile mutations.

```powershell
python -B verification/n3-48-computation/independent_audit.py
python -B code/wave14_n3_48_test.py -v
```

The archived JSON output is deterministic under replay. The scan status is
`1 SAT_CANDIDATE`, `7 UNSAT_UNVERIFIED`, `1 BUDGET_UNKNOWN`, and
`2 TIMEOUT_UNKNOWN`; negative solver exits are explicitly non-evidentiary.
The literature/status audit also keeps the target and novelty `UNKNOWN`.
The detached clean-source replay, four byte-identical regenerations, and the
pre-release timestamp-determinism repair are recorded in
`2026-07-23-wave14-clean-clone.md`.

## `N3=48` global exclusion

Wave 15 brings the full SRG equations back into the Wave 14 residual. The
active original-vertex set has order at most 24 and induced minimum degree at
least six. The target spectrum gives

```text
2e(X) <= 3|X| + |X|^2/9,
```

so minimum degree six forces `|X|>=27`, a contradiction. An independent
outside-degree second-moment argument reaches the same obstruction.

```powershell
python -B attempts/wave15-global-lift/verify_subset_moment_certificate.py `
  attempts/wave15-global-lift/subset-moment-certificate.json
python -B -m unittest -v `
  attempts/wave15-global-lift/test_subset_moment.py
python -B verification/n3-48-global-lift/independent_check.py

$wave15Python = (Resolve-Path '.venv\Scripts\python.exe').Path
Push-Location verification/n3-48-global-lift
& $wave15Python -B -m unittest -v test_independent_check.py
Pop-Location

python -B attempts/wave15-algebraic/exact_checks.py `
  --output attempts/wave15-algebraic/exact-checks.json
python -B verification/n3-48-algebraic/independent_check.py `
  --artifact attempts/wave15-algebraic/exact-checks.json
python -B -m unittest -v `
  verification/n3-48-algebraic/test_independent_check.py
```

The two discovery lanes and their separate adversarial audits pass 5, 11,
and 7 focused tests. The global certificate and independent regeneration are
byte-identical canonical-LF files. The first CRLF/public-LF mismatch is kept
at baseline commit `522260a` and repaired at `874af27`; the algebraic lane's
ambiguous weighted-moment key is also preserved and re-audited. The verified
conditional consequence is

```text
n3 >= 51,
induced_C6_count >= 209337,
Conway-99 = UNKNOWN,
novelty = UNKNOWN.
```

The detached clean-source replay at
`2026-07-23-wave15-clean-clone.md` records the full historical suites, all 23
focused Wave 15 tests, all 18 frozen file hashes, byte-identical canonical-LF
certificate regeneration, clean detached status, and `git fsck`.

## `N3=51` equality exclusion and active-local archive

Wave 16 independently verifies a shorter global obstruction. Sixteen raw
`sum q=34` profiles reduce to four. Their indexed active original-vertex set
has order at most 25, while exact size-two endpoint crossings and distinct
triangle neighbors force induced minimum degree at least six. The target
spectrum requires order at least 27.

```powershell
python -B attempts/wave16-n3-51-structural/exact_check.py `
  --verify attempts/wave16-n3-51-structural/exact-checks.json
python -B verification/n3-51-structural/independent_check.py
$wave16Python = (Resolve-Path '.venv\Scripts\python.exe').Path
Push-Location verification/n3-51-structural
& $wave16Python -B -m unittest -v test_independent_check.py
Pop-Location
```

The 24-test adversarial suite verifies the endpoint-local scope and contains
countercontrols against a global `H`-degree law, a point-size cap, the old
support-graph identity, reused support indices, and weakened spectral inputs.
It also pins the final Wave 15 public hash while preserving two transient
historical hashes. The verified conditional consequence is

```text
n3 >= 54,
induced_C6_count >= 209340,
Conway-99 = UNKNOWN,
novelty = UNKNOWN.
```

The computational lane is deliberately separate:

```powershell
python -B verification/n3-51-computation/independent_check.py `
  --output verification/n3-51-computation/independent-audit.json
python -B verification/n3-51-computation/test_independent_check.py -v
python -B code/wave16_n3_51_test.py -v
```

It independently rebuilds seven exact DIMACS streams, validates one positive
active-local relaxation candidate, rejects 38 hostile mutations, and passes
4 independent plus 8 submitted tests. Its final bounded status remains
`1 SAT_CANDIDATE / 5 TIMEOUT_UNKNOWN / 1 UNSAT_UNVERIFIED`, with one earlier
`BUDGET_UNKNOWN` retained separately. No solver-negative outcome is used as
mathematical evidence.

The independent literature/status audit is
`2026-07-23-wave16-status-audit.md`. It checks the exact source pages behind
`induced_C6_count=209286+n3`, current target-specific sources, exact-number
searches, corrections, citations, and the June 2026 Shpectorov lecture scope.
It found no target resolution or exact prior Wave 16 bound through 2026-07-23,
but correctly leaves both target status and novelty `UNKNOWN`.

The detached release replay is `2026-07-23-wave16-clean-clone.md`. It records
252 passing tests, six semantic checker entry points, five byte-identical
regenerations, all seven Wave 16 status hashes, every ledger evidence path,
public-hygiene scans, clean detached status, and `git fsck`.

## Wave 27 endpoint lattice and orthogonal-root audits

The Wave 27 verification package has three deliberately separated
mathematical layers.

First, the
[A2-summand-free construction audit](wave27-a2free-construction/2026-07-24T001657Z-audit.md)
independently reconstructs the abstract coupled package

```text
S=E8^4 orthogonal_sum E6^2
```

and passes 16 independent tests plus the submitted 15-test replay. Complete
root enumeration proves that `S` has no orthogonal `A2` direct summand.
Embedded `A2` root subsystems do occur inside its `E6` blocks; the audit
explicitly preserves that distinction. The verified object is still only a
candidate for the arithmetic/lattice relaxation, with no frame, projector,
Schur-square, or graph origin. The submitted account is the
[construction report](../agents/2026-07-23-wave27-a2free-construction.md).

Second, the
[unrestricted E6 trace audit](wave27-h9-classification/2026-07-24T002029Z-audit.md)
proves

```text
E6 Q=I (mod 2), Q symmetric even integral positive definite
  implies tr(E6 Q)>=14,
```

with equality attained by the displayed `Q6`. Its independent suite passes
21 tests and its submitted suite passes 16. The report retains one nonfatal
exposition correction, the missing parity bridge
`tr(C^2)=tr(C) (mod 2)`. This algebraic trace floor is not the later
projector-frame cubic floor: the trace-14 block is a valid hostile control for
the weaker algebraic problem. See the
[trace report](../agents/2026-07-23-wave27-h9-classification.md).

Third, the
[general-root tensor audit](wave27-general-root-tensor/2026-07-24T010548Z-audit.md)
uses an independent affine-CVP enumerator to verify cubic-energy floors 24
for an orthogonal `E6` summand and 66 for an orthogonal `A6` summand. The
`E6` floor contradicts its complement-imposed compression cap 22; the `A6`
floor exceeds the global trace 60. Arbitrary cross-block `Q` entries are
allowed, but every conclusion requires an orthogonal integral summand.

The frozen [core tensor report](../agents/2026-07-23-wave27-general-root-tensor.md)
leaves exactly `A20 orthogonal_sum E8^3` at `h=21` among 17 full rank-44 ADE
decompositions. A later, separately frozen
[A20 addendum](../agents/2026-07-24-wave27-a20-trace-addendum.md) proves a
local trace floor 42; the rank-24 complement raises the total floor to 66 and
excludes that core survivor. The audit verifies the core and addendum
separately, passing 23 independent, 17 submitted-core, and 8
submitted-addendum tests with byte-identical regenerations.

The combined conclusion is conditional on `n3=708`, the full projector/Schur
endpoint identities, and the additional hypothesis that the scaled-dual form
is a full orthogonal sum of irreducible ADE root lattices:

```text
full orthogonal ADE rank-44 endpoint form: impossible
general even rank-44 scaled-dual form: UNKNOWN
n3=708 / Conway-99 / novelty: UNKNOWN
```

Glued, non-root, and otherwise nonorthogonal general lattices are not
classified or excluded. The headline conditional bound therefore remains
`n3>=708`.

The
[Wave 27 correction ledger](2026-07-24-wave27-orchestrator-corrections.md)
preserves the E6 exposition bridge, the corrected literature-protocol
interpretation, and the later A20-addendum chronology.

The proof-separated
[Wave 27 literature audit](wave27-literature-audit/audit.md) covers 56 frozen
or separately frozen service-query pairs and 303 inspected records through
2026-07-24. It records conceptual component and Cartan-matrix prior art, a
retained protocol correction, and failed-service results without treating
them as nonexistence evidence. No direct match was found within the bounded
search, but novelty and priority remain `UNKNOWN`.
