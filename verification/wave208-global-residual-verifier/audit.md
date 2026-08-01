# Wave 208 source-blind verifier audit

Date (UTC): `2026-08-01T02:28:31Z`  
Frozen git commit: `c58fd917ea8f9622e1388f10b0e0e3c709ba4854`

## Verdict

`VERIFIED`, with deliberately narrow scope: conditional on the frozen
prism-free M7g branch, the exact integer norm identity forces

```text
d(Q) = 3 mod 9,
```

and this excludes exactly 23 of the 27 labelled polar forms in each of all
four relative column orientations.  Four forms per orientation survive.

This is not an endpoint exclusion.  It supplies neither an intersection
graph, the outside incidence block, full row-space membership, a 99-vertex
graph, nor a nonexistence certificate.  Therefore

```text
Conway-99:                    UNKNOWN
rank-11 prism-free endpoint:  UNKNOWN
```

## Source barrier and blind freeze

Before opening either named Wave 208 discovery lane, the verifier froze
`protocol-freeze.md`, `independent_baseline.py`, `baseline-results.json`, and
`test_independent_baseline.py`.  Their four hashes are recorded in
`blind-freeze.sha256`; all four still replay exactly.

The blind derivation independently recovered

```text
Az = 4x-z+2t*1
sum(z) = 14t
3||z||^2 = 4w-x.z+6t^2
u_3  = (3x.z+4w-18t^2/11)/7
u_-4 = (3w-3x.z+t^2)/7
```

and retained all arithmetically possible sign compositions at weights 17,
20, and 23.  At weight 14 it imported only the already-verified `7+7`
composition.  The hostile baseline also preserves both product-one models,
requires the omitted equation `M b_U=0`, distinguishes a binary graphical
completion from an aggregate Gram matrix, refuses to zero unknown enumerator
coefficients, and rejects terminal status inflation.

## Supplemental sealed M7g norm package

The construction package was first sealed by manifest SHA-256

```text
8d7088cf4bee7792ae22f75c4babbd114fe3aee7c1ca64a25fe33c04dac40373
```

The verifier did not import its checker.  Starting from the eight published
labelled representatives and the fixed ternary relation, the clean-room
checker independently:

1. recovered all four relative orientations (by exhausting the 128 sign
   choices modulo global sign);
2. reconstructed the three-dimensional vanishing symmetric-form space;
3. retained all 27 forms rather than quotienting by nonzero scalar;
4. used the literal balanced integer lift
   `(1,-1,1,-1,1,-1,-1,1)`; and
5. reproduced the exact rank, zero-graph, residue, and survivor counts.

For triangle-incidence matrix `U`, put `K=U^T U`, `R=U^T A U`, and
`H=AU`.  If `s` is the signed sum over intersecting pairs and `d(Q)` is the
signed canonical-residue sum, then

```text
alpha^T K alpha = 24+2s
alpha^T R alpha = 48+2d(Q)+6s
||H alpha||^2   = 240+18s-2d(Q).
```

The bridge makes every coordinate of `H alpha` divisible by three, so the
last norm is divisible by nine.  The unknown `18s` correction vanishes
modulo nine without resolving whether a product-one pair intersects.  This
gives `d(Q)=3 mod 9`.

The independent survivor totals across the four orientations are

```text
4  rank-3 4K2 forms with d=12 and base norm 216
12 rank-4 2C4 forms with d=-24 and base norm 288
```

The source checker replayed (`8/8` tests), the initial post-source hostile
audit replayed (`5/5` tests), and the independent baseline plus norm suites
replayed (`12/12` tests).

## Recorded correction, not erased

The initial sealed derivation incorrectly said that the package did not
supply the "other 91 vertices."  Eight triangle columns are not eight graph
vertices, and the package fixes no selected-union size.  The verifier vetoed
that count while accepting the unaffected norm calculation.

The source corrected the sentence to say that the vertices outside the
selected-triangle union are absent and that the union size is not fixed.  A
new manifest was sealed:

```text
a633dff62e4e1127b8a0c7329928e110d1fef1e78f1f322bbc4e250e277167f3
```

The delta audit verified all ten manifest entries and all five frozen-input
entries.  Only these documentation records received new hashes:

```text
derivation.md
run-report.yaml
agents/2026-07-31-wave208-m7g-norm-divisibility.md
```

`exact_check.py`, `exact-results.json`, and `test_exact_check.py` retained
their original hashes.  The original finding and both manifest hashes remain
machine-readable in `m7g-norm-post-source-audit.json` and
`m7g-norm-post-correction-audit.json`.

## Named discovery lanes at this seal

At the time of this verifier seal, neither of the following directories had
been opened because no sealed manifest had been delivered:

```text
attempts/wave208-integer-lift-proof-a/
attempts/wave208-marked-m7g-proof-b/
```

Their communicated work-in-progress statements are not promoted or audited
here.  Any later claim from either lane requires a manifest-pinned delta
audit; it cannot inherit this package's `VERIFIED` label.

## Reproduction

From the repository root:

```powershell
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\independent_baseline.py --verify
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\independent_m7g_norm.py --verify
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\post_source_m7g_audit.py --verify
.venv\Scripts\python.exe -B -m unittest verification\wave208-global-residual-verifier\test_independent_baseline.py verification\wave208-global-residual-verifier\test_independent_m7g_norm.py verification\wave208-global-residual-verifier\test_post_source_m7g_audit.py -v
.venv\Scripts\python.exe -B attempts\wave208-m7g-norm-divisibility\exact_check.py --verify
.venv\Scripts\python.exe -B -m unittest attempts\wave208-m7g-norm-divisibility\test_exact_check.py -v
```

No solver exit code, local non-hit, or aggregate feasibility statement was
used as a certificate.

## Manifest-pinned proof-B delta audit

This section was appended after the initial verifier seal.  Proof B was
opened only after receipt of the sealed manifest

```text
f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc
```

All 11 package entries and all four frozen-input entries match the seal.  The
submitted checker and its `5/5` tests replay.

### Spectral identity

For the balanced integer point image `b~=B alpha`, independently applying

```text
A^2=12I-A+2J
```

on the zero-sum space gives

```text
(A+4I)(A-3I)b~=0.
```

Thus `r=(A-3I)b~` is a `-4` eigenvector.  The verified modular bridge gives
`Ab~=0 mod 3`, so `r` is coordinatewise divisible by three.  If `S_D` is the
signed canonical polar sum and `h` the actual signed intersection sum, then

```text
||b~||^2      =24+2h
b~^T A b~     =48+2S_D+6h
||r||^2       =7(3||b~||^2-b~^T A b~)
              =7(24-2S_D).
```

Therefore `9 | ||r||^2` forces `S_D=3 mod 9`.  The actual intersection term
cancels without interpreting every product-one pair as an intersection.

### Exact form and marked-subset census

The clean-room form reconstruction reproduces

```text
S_D=-24: 3 forms
S_D=-12: 4 forms
S_D=  0: 19 forms
S_D= 12: 1 form
```

The norm condition excludes 23 forms.  Four of those were already excluded
by Wave 207, so the new reduction removes 19 of the previous 23 survivors
and leaves exactly the same four forms:

```text
(0,0,1), (0,1,0), (1,0,0): rank 4, S_D=-24, ||r/3||^2=56
(2,2,2):                     rank 3, S_D= 12, r=0
```

All `2^8` labelled intersection subsets were replayed for each rank-four
form, including the full composition-refined profile: 83 subsets survive per
form.  In the rank-three branch, every product-one edge joins opposite
signs; exactly `C(12,2)=66` subsets have point weight 20 and
`C(12,5)=792` have balanced point weight 14.  No other rank-three support
weight survives the frozen point-code restrictions.

The clean-room verifier separately enumerated all four projective
weight-eight linear words, checked that exactly one is tensor-balanced, and
enumerated all 105 perfect matchings to recover exactly four concurrent-
secant matchings.  These are three different notions.  The source checker
hard-codes the secant-matching count as four rather than deriving it; the
independent enumeration fills that coverage gap and confirms the claim.

### Local-control veto boundary

Both positive controls replay exactly:

```text
weight 20: 22 vertices, 53 edges, 2 intersections, A_U b_U=3b_U
weight 14: 19 vertices, 44 edges, 5 intersections, A_U b_U=3b_U
```

Their selected-pair cross counts, point images, induced `lambda<=1` and
`mu<=2` caps, degree caps, triangle counts, and absence of induced triangular
prisms were independently recomputed.

They enforce internal necessary equations only.  For each control the
verifier added one new zero-coordinate vertex adjacent to a single
nonzero-`b` vertex.  This preserves `A_U b_U=3b_U`, degree bounds, and all
local common-neighbor upper caps, but the new outside row has dot product
`1` with `b_U`.  Hence the displayed local constraints do not imply the
missing equation `M b_U=0`, much less an outside SRG completion.

The scoped proof-B reduction is `VERIFIED`.  The three rank-four branches,
the rank-three weight-14 and weight-20 branches, all outside equations, and
the full 231-column frame survive.  Consequently the weight-eight word,
rank-11 endpoint, and Conway-99 remain `UNKNOWN`.

Proof-B delta reproduction:

```powershell
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\independent_proof_b.py --verify
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\post_source_proof_b_audit.py --verify
.venv\Scripts\python.exe -B -m unittest -v verification\wave208-global-residual-verifier\test_independent_proof_b.py
.venv\Scripts\python.exe -B attempts\wave208-marked-m7g-proof-b\exact_check.py --verify
.venv\Scripts\python.exe -B -m unittest -v attempts\wave208-marked-m7g-proof-b\test_exact_check.py
```

## Separately pinned proof-A delta audit

Proof A was audited only after the proof-B delta had been sealed.  Its
independent seal is

```text
28d69162a8f52bdc325471946efecad890b1edac33f3576bdba8777e32887202
```

All ten package entries and all eight frozen-input entries match.  The
submitted checker and `10/10` tests replay.  The older Wave94 verifier that
supplies the norm-14 complementary-Fano theorem also replayed with `12/12`
tests under its frozen audit hash.

### Exact integral lift and residue shells

Starting only from `Ax=3z`, `Az=4x-z+2t*1`, and `A1=14*1`, the verifier
symbolically recomputed

```text
Q=9(z-x)-t*1,       AQ=-4Q,  sum(Q)=0,
R=11(4x+3z)-6t*1,  AR= 3R,  sum(R)=0,

z.z=(4w-h+6t^2)/3,
Q.Q=63[3(w-h)+t^2],
R.R=77[11(4w+3h)-18t^2].
```

Since every `Q_i=-t mod 9`, writing `Q_i=9m_i-t` and using
`sum(m_i)=11t` yields the exact shell identity

```text
Q.Q=99t(9-t)+162L,  L>=0.
```

The full arithmetic tables for every sign composition up to global sign at
weights 17, 20, and 23 agree entry-for-entry.  They contain respectively
`3`, `4`, and `4` compositions and eliminate none.

At balanced weight 14 the complete shell list is

```text
(h,q.q)=(-16,70),(-10,56),(-4,42),(2,28),(8,14),(14,0).
```

These are six branches, not six constructions and not an exclusion.

### The q=0 branch

For `q=0`, the verifier independently reproduced the same-sign edge cases
`e=11,12,13`.  The `e=13` row exceeds the exact common-neighbor wedge
capacity.  The `e=12` equality row forces every internal edge into its unique
internal triangle and hence even internal degrees, contradicting the forced
four degree-three vertices.  The `e=11` row survives with exactly one cross
edge and degree sequence `(4,3,3,3,3,3,3)` on each sign side.

### Complementary-Fano import and overlap census

The imported theorem is valid in precisely the scope used here.  A norm-14
integral `-4` eigenvector has independent `7+7` sign classes whose cross
graph is the symmetric complementary-Fano `2-(7,4,2)` design.  The
clean-room verifier reconstructed its seven blocks, degree four, pair degree
two, and the support edge bound forcing same-sign independence.  The
outside eigenvector equations then give exactly 70 vertices meeting one
coordinate of each sign and 15 meeting neither; no automorphism is used.

Using an independently generated Fano labelling, the verifier enumerated all
labelled three-way partitions on both sign sides.  The exact necessary
token-capacity census is

```text
alpha  labelled rows  capacity survivors
0          3003              651
1         24010               42
2         41895                0
3         13230                0
4           441                0
```

The 42 `alpha=1` rows split into two sign-reversed classes of 21.  In each
orientation, four same-sign outside endpoints are required on one Fano side.
The other side has signed demand two and only one opposite token available,
so it can host at most three.  Both orientations were checked directly.
Thus `alpha=1` also fails, and the norm-14 branch is reduced to

```text
same-sign overlap alpha=0,
opposite-sign overlap beta=6,
|supp(x) union supp(q)|=22,
z has eight +1 and eight -1 coordinates.
```

The exclusive sign sizes force `k in {2,3,4}`.  The smaller side for `k=2`
or `4` is a `K3`; at `k=3`, exhaustive checking of all 64 labelled graphs on
four vertices leaves exactly the three labelled `C4`s on each side and no
exclusive cross edge.  These structures survive.

### Partial-control boundary and coverage finding

The 22-vertex certificate independently satisfies all displayed

```text
Ax=3z,  Az=4x-z,  Aq=-4q
```

equations, has 52 edges, respects the displayed common-neighbor and triangle
upper caps, and contains the complementary-Fano support with two exclusive
`C4`s.  It is only a partial control.  Adding one new zero-coordinate vertex
adjacent to `P0` preserves every displayed equation and all local upper caps,
but its omitted outside `Ax` and `Az` residuals are both one.  Hence the
partial system implies neither the missing 77 equations nor a completion.

The source spectral checker compares precomputed coefficient dictionaries
and checks its norm formulas on four samples.  That is a checker-coverage
gap, not a theorem error: the clean-room verifier performs general symbolic
expansion and confirms every identity.  No silent repair was made to the
source package.

The proof-A reductions are `VERIFIED` only in their stated conditional
scope.  No residual weight among 14, 17, 20, and 23 is excluded.  The
`q^2=14` branch still contains `alpha=0,k=2,3,4`; the other five balanced
shells remain.  Rank 11, the endpoint, and Conway-99 remain `UNKNOWN`.

Proof-A delta reproduction:

```powershell
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\independent_proof_a.py --verify
.venv\Scripts\python.exe -B verification\wave208-global-residual-verifier\post_source_proof_a_audit.py --verify
.venv\Scripts\python.exe -B -m unittest -v verification\wave208-global-residual-verifier\test_independent_proof_a.py
.venv\Scripts\python.exe -B attempts\wave208-integer-lift-proof-a\exact_check.py --verify attempts\wave208-integer-lift-proof-a\exact-results.json
.venv\Scripts\python.exe -B -m unittest -v attempts\wave208-integer-lift-proof-a\test_exact_check.py
```
