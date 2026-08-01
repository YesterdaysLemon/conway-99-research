# Wave 207 integration audit

```yaml
role: orchestrator
date_utc: 2026-08-01T02:01:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Integrate only the independently verified Wave 207 incidence-linear,
  M7g, mixed-center, ternary-code, weight-fourteen, and restricted local
  consequences while preserving the endpoint and global UNKNOWN walls.
inputs:
  agents/2026-07-31-wave207-statement-literature.md: d53c453f41b4671d3904fdba7d303fa68d01ddfd4b49f0ac4ffa5a5181b29f25
  attempts/wave207-incidence-tensor-code-proof-a/package-manifest.sha256: 544e9d469dc0666ff3463f5c7f3b41a4ad3acfde857100c422dd3acea4c6d8ab
  attempts/wave207-mixed-four-center-proof-b/package-manifest.sha256: 87158d7931f6f2440bb176670368b112055b84a0e358a1b6b8ea18cb630e756d
  attempts/wave207-ternary-adjacency-code-bridge/package-manifest.sha256: 31e3abf3a7e16bf80eb8de4721c683f41d4d20d55f90564398e4d638b3414f99
  attempts/wave207-kernel-endpoint-proof-c/package-manifest.sha256: bb0a3e8b4821f7533330fcdd9b0fb58085eaefcb2281f387b7356784efacd2e6
  attempts/wave207-m7g-incidence-bridge/package-manifest.sha256: 3fa21f164fd7a7afb13c546447e3a42f9ae870d2d1b8cd5030d254ee61a5c561
  verification/wave207-incidence-tensor-rigidity/SOURCE_BLIND_PROTOCOL.sha256: 603f27ff164658883c0df5646910ba56254772497c4bc5c6c632bfee87a9c008
  verification/wave207-incidence-tensor-rigidity/package-manifest.sha256: 63aa632350e7191075203de6a7568ca0a3e387925d99f824a073eed12db00023
method: >-
  Freeze the global status; keep literature, proof, construction, and
  verifier roles separate; replay every exact package; accept verifier scope
  corrections; and promote only claims reproduced by the clean-room checker.
command: >-
  .\.venv\Scripts\python.exe -B -m unittest -v
  verification\wave207-incidence-tensor-rigidity\test_independent_check.py
outputs:
  - verification/2026-07-31-wave207-integration-audit.md
  - verification/2026-07-31-wave207-orchestrator.md
  - logs/2026-07-31-wave207-public-checkpoint.json
limitations:
  - Every M7g conclusion is conditional on a hypothetical weight-eight word at the prism-free rank-11 endpoint.
  - The ternary distance theorem is d>=12, not d>=24.
  - The rank-four local control checks only 23 induced coordinates and is not a completion.
  - No graph, nonexistence proof, endpoint exclusion, strict n3 improvement, Q>=7060 proof, novelty, or priority claim follows.
```

## Verdict

`PASS_VERIFIED_SYMBOLIC_REDUCTION_NO_RESOLUTION`.

Wave 207 materially narrows the first unresolved support case in the
conditional prism-free rank-11 tensor-balance code.  It does not close that
case and does not decide Conway-99.

The verified chain is:

```text
hypothetical weight-eight a in A_Delta
  -> incidence-linear and quadratic M7g relation with composition 4+4
  -> nonzero b=Ba in ker_F3(A)
  -> wt(b) in {14,17,20,23}
  -> if wt(b)=14, its signs are 7+7
  -> exactly 4 of 27 restricted polar forms are impossible.
```

The remaining branches are real proof obligations, not search failures.

## Frozen global boundary

```text
Conway-99:                    UNKNOWN
rank-11 endpoint:             UNKNOWN
n3=4158 endpoint:             UNKNOWN
graph construction:           NONE
counterexample/nonexistence:   NONE
rigorous n3 interval:          708<=n3<=4158
conditional Q bound:          Q>=7059
Q>=7060:                      NOT PROVED
automorphism assumption:       NONE
```

## Incidence membership corrects the linear-relation boundary

Let `B` be the `99 by 231` point--triangle incidence matrix, `G=BB^T=A+I`,
and `D=Z^*Z`.  Over `F_3`,

```text
D B^T=B^T A B B^T=B^T A G=2B^T J=0.
```

Thus every `a in im(B^T)` satisfies `Da=0`.  At the rank-eleven endpoint,
`Z` has full row rank into a nondegenerate space, so `Z^*` is injective and

```text
Da=Z^*(Za)=0  =>  Za=0.
```

Tensor-kernel membership is not needed for this linear implication.  This
is the precise correction to the older generic caveat: a generic quadratic
relation need not be linear, but an incidence word is.

Since `D1=0` also gives `Z1=0`, a tensor-balanced incidence word has equal
linear and quadratic coefficient-class sums:

```text
S0=S1=S2,
R0=R1=R2.
```

## Weight-eight support is M7g with composition 4+4

The sealed Wave 206 equality premises give vector rank four and an
eight-cap.  The quadratic relation has Veronese rank seven: rank at most six
would yield a second relation and hence a forbidden support-at-most-seven
relation.  Kaipa--Pradhan's maximal rank-seven classification then leaves
only the eight-point `M7g` closure.

The first and second moment relations force exactly four coefficients of
each nonzero ternary value.  The canonical linear kernel has dimension four
and enumerator

```text
1 + 24 y^4 + 16 y^5 + 32 y^6 + 8 y^8.
```

The restricted three-dimensional symmetric-form space has 27 affine forms:

```text
rank 0:  1 form,  zero graph K8
rank 2: 12 forms, zero graph 2K4
rank 3:  8 forms, zero graph 4K2
rank 4:  6 forms, zero graph 2C4.
```

The projective M7g orbit/closure is unique.  A labelled canonical eight-set
has four valid concurrent-secant perfect matchings, not a unique internal
pairing.  Every matching has one external concurrency point and no three of
its secants are coplanar.

## Ternary point-code bridge and distance floor

Write `a=B^Tc`, `b=Ba`, and use the `4+4` relation.  Since `B1=1` and
`sum a=0`, one has `sum c=0`.  The adjacency algebra gives

```text
b=(A+I)c,
Ab=0,
c^T b=a^T a=2,
b^T b=c^T((A+I)-J)c=2.
```

Hence `b` is nonzero, is supported on the union of eight triangles, and has
weight congruent to two modulo three.  Its weight is at most 24.

For an arbitrary nonzero `x in ker_F3(A)`, signed neighbor counts obey exact
first and second common-neighbor moments.  A pointwise nonnegative inequality
excludes weights one through nine; equality arithmetic excludes weight ten;
and a separate exact membership-dependent Farkas certificate excludes weight
eleven.  Therefore

```text
d(ker_F3(A))>=12,
wt(b) in {14,17,20,23}.
```

No weight-24 lower bound or equality classification is proved.

## Weight-fourteen sign reduction

At weight 14, `p-n=0 mod 3` permits five sign compositions.  Two independent
pointwise Farkas polynomials are nonnegative on every exact local
membership/range/residue type but have forced global sums

```text
(p,n)=(1,13):  -35,
(p,n)=(4,10):  -12.
```

Sign reversal handles `(13,1)` and `(10,4)`.  Thus any weight-fourteen
kernel word must have composition `(7,7)`.  The balanced case survives.

The integer lift

```text
z=Ax/3,
Az=4x-z+2t*1,  p-n=3t,
```

is exact, but its category sums collapse to the existing moment equations.
The archived balanced aggregate control is deliberately nongraphical; it is
neither a graph nor a codeword and proves no low-weight existence.

## Four polar forms excluded, with a restricted local survivor

Let `B_S` be the eight selected incidence columns.  The norm identity is

```text
b^T b
 =a^T(B_S^T B_S)a
 =2 sum_(i<j, T_i intersects T_j) a_i a_j
 =2.
```

An intersection can occur only at restricted polar product one.  Exact
enumeration in each relative sign class therefore excludes the rank-zero
form and exactly three rank-two forms having no off-diagonal one: four of 27
normalized forms.  The other 23 remain.

The rank-four `2C4` certificate has 23 vertices, 51 edges, one selected
triangle intersection, 11 induced graph triangles, maximum induced degree
eight, and no induced triangular prism.  It realizes the selected-pair
product table and satisfies

```text
A_U b_U=0
```

on the 23 induced coordinates.  It also respects the necessary induced
`lambda<=1` and `mu<=2` caps.  This is not the full equation `Ab=0`: the 76
outside coordinates are untested.  Eighteen internal edges still need their
unique common neighbor outside, and the object omits 223 triangle blocks and
the full rank-eleven frame.

All twelve weight-four and eight weight-five internal projective circuits
cross-realize zero vertex pairs in this restricted model.  Existing
cross-realization multiplicity bounds therefore do not remove it locally.

## Mixed four-center theorem and method boundary

For synthesis into a nondegenerate bilinear space, the verifier confirms

```text
0 -> ker(R) -> ker(Gram(R)) -> rad(im R) -> 0.
```

A cross matrix of rank `d` induces rank `d(d+1)/2` on symmetric squares.  An
abstract four-center control reaches cumulative ranks `21,41,56,66` and the
displayed 25-coordinate restriction is injective.  These are sharp algebraic
controls, not endpoint measurements.

More importantly, if `sum_x c_xP_x=0`, then every fixed center satisfies

```text
sum_x c_x P_yP_xP_y=0.
```

All mixed traces and sandwiches that factor linearly through these features
annihilate true projector relations functorially.  More linear combinations
of the same data cannot exclude an `A_Delta` relation.  A continuation must
use nonlinear, relation-dependent, or explicitly graph-typed information.

## Literature boundary

The current-through-2026-07-31 audit found primary prior art for the M7g
classification and the triangle clique-graph language, but no proof,
counterexample, applicable `d>=24` theorem, or full marked-incidence theorem.
The revised SAT preprint remains a computational nonresolution.  This is a
bounded source result and cannot prove openness, novelty, or priority.

## Independent verification

The verifier froze its protocol before opening any Wave 207 discovery
artifact:

```text
protocol-freeze.md SHA256
e381877375f1f5f270e7ad064db570494a7df12dc0bbf01a0df0d24b67884444
```

Root and verifier replay obtained:

```text
Proof A submitted tests:             3/3 PASS
Proof B submitted tests:             5/5 PASS
ternary bridge submitted tests:    10/10 PASS
kernel endpoint submitted tests:     8/8 PASS
M7g bridge submitted tests:          5/5 PASS
clean-room verifier tests:          13/13 PASS
all five discovery manifests:        PASS (50 entries)
verifier package manifest:           PASS (11 entries)
```

Verifier package manifest SHA256:

```text
63aa632350e7191075203de6a7568ca0a3e387925d99f824a073eed12db00023
```

Recorded findings, not silent repairs:

1. the labelled M7g representative has four internal secant pairings;
2. the local `Ab=0` claim is only the 23-coordinate equation `A_Ub_U=0`;
3. one frozen `failed-routes.md` line says 91 omitted graph vertices, while
   the correct count is 76 and the derivation uses 76.

No frozen mathematical claim is refuted.

## Exact next frontier

Two symbolic targets remain:

1. use neighbor-to-neighbor correlations in the integer lift, or an exact
   code theorem, to exclude/classify balanced weight 14 and weights 17, 20,
   and 23;
2. impose the other 76 point-code equations, outside common-neighbor
   completion, and all 231 triangle columns on the 23 remaining marked M7g
   polar forms.

Either route must remain independent of automorphism assumptions and must
produce a checked contradiction or a complete target-compatible object
before any endpoint status promotion.
