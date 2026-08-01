# Wave 208 integration audit

```yaml
role: orchestrator
date_utc: 2026-08-01T02:55:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Integrate only the independently reproduced Wave 208 M7g norm
  congruence, four-form reduction, marked-subset census, integer spectral
  lift, and balanced weight-fourteen reductions, while retaining every
  outside-completion, endpoint, and global UNKNOWN wall.
inputs:
  attempts/wave208-global-residual-rigidity/protocol.md: 3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740
  attempts/wave208-m7g-norm-divisibility/package-manifest.sha256: a633dff62e4e1127b8a0c7329928e110d1fef1e78f1f322bbc4e250e277167f3
  attempts/wave208-marked-m7g-proof-b/package-manifest.sha256: f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc
  attempts/wave208-integer-lift-proof-a/package-manifest.sha256: 28d69162a8f52bdc325471946efecad890b1edac33f3576bdba8777e32887202
  verification/wave208-global-residual-verifier/package-manifest.sha256: c9551a7c4d62a57f081b8008f49b9e27fb0372f50a7d114e10136557242fbab4
method: >-
  Keep construction, proof-A, proof-B, and verifier roles separate; replay
  every sealed exact package; require clean-room reconstruction of the
  spectral identities and finite censuses; adopt every verifier scope veto;
  and reject promotion from a local control or arithmetic survivor.
command: >-
  .\.venv\Scripts\python.exe -B -m unittest -v
  verification\wave208-global-residual-verifier\test_independent_baseline.py
  verification\wave208-global-residual-verifier\test_independent_m7g_norm.py
  verification\wave208-global-residual-verifier\test_post_source_m7g_audit.py
  verification\wave208-global-residual-verifier\test_independent_proof_b.py
  verification\wave208-global-residual-verifier\test_independent_proof_a.py
outputs:
  - verification/2026-07-31-wave208-integration-audit.md
  - verification/2026-07-31-wave208-orchestrator.md
  - logs/2026-07-31-wave208-public-checkpoint.json
limitations:
  - Every marked-M7g conclusion is conditional on a hypothetical weight-eight endpoint word.
  - Three rank-four norm-56 branches and rank-three point weights 14 and 20 survive.
  - The general integer lift excludes no weight among 14, 17, 20, and 23.
  - Local controls omit outside equations, binary completion, and the full 231-column frame.
  - No graph, nonexistence proof, endpoint exclusion, Q>=7060 proof, novelty, or priority claim follows.
```

## Verdict

`PASS_VERIFIED_FOUR_FORM_REDUCTION_NO_RESOLUTION`.

Wave 208 replaces the 23 marked polar survivors from Wave 207 by four exact
branches.  It also gives an integral spectral decomposition for every
residual ternary point word and sharply reduces two balanced weight-fourteen
shells.  It does not eliminate a residual word or decide the endpoint.

The verified marked chain is

```text
hypothetical weight-eight a in A_Delta
  -> signed 4+4 M7g triangle configuration
  -> coordinatewise-divisible residual r=(A-3I)B alpha
  -> signed polar congruence S_D=3 (mod 9)
  -> 23 of 27 polar forms excluded
  -> three rank-4 norm-56 branches or one rank-3 branch
  -> rank-3 point weight 20 (66 subsets) or 14 (792 subsets).
```

## Frozen global boundary

```text
Conway-99:                     UNKNOWN
rank-11 endpoint:              UNKNOWN
n3=4158 endpoint:              UNKNOWN
graph construction:            NONE
counterexample/nonexistence:    NONE
rigorous n3 interval:           708<=n3<=4158
conditional Q bound:           Q>=7059
Q>=7060:                       NOT PROVED
automorphism assumption:        NONE
```

## Norm divisibility and the four-form theorem

Let `U` be the eight selected triangle-incidence columns, let `alpha` be the
balanced integer `+/-1` lift, and put

```text
K=U^T U,  R=U^T A U,  H=AU.
```

If `s` is the signed actual-intersection sum and `S_D` is the signed
canonical polar sum, exact expansion gives

```text
alpha^T K alpha = 24+2s,
alpha^T R alpha = 48+2S_D+6s,
||H alpha||^2  = 240+18s-2S_D.
```

Every coordinate of `H alpha` is divisible by three.  The unknown
intersection correction is itself divisible by nine, hence

```text
S_D=3 (mod 9).
```

Proof B independently reaches the same condition spectrally.  With
`b~=B alpha` and `r=(A-3I)b~`, the SRG identity gives

```text
Ar=-4r,
3 divides r coordinatewise,
||r||^2=7(24-2S_D).
```

The complete 27-form census is

```text
S_D=-24: 3 forms
S_D=-12: 4 forms
S_D=  0: 19 forms
S_D= 12: 1 form.
```

Therefore 23 forms fail and precisely four remain:

```text
(0,0,1), (0,1,0), (1,0,0): rank 4, 2C4, ||r/3||^2=56
(2,2,2):                     rank 3, 4K2, r=0.
```

This removes 19 of the 23 Wave 207 survivors; the other four were already
excluded there.  Root construction, proof B, and the clean-room verifier
all reconstruct the same four branches without an automorphism assumption.

## Complete marked-subset census

For each of the three rank-four forms, exact enumeration of all `2^8`
labelled intersection subsets leaves 83 subsets.  Their divided residual is
an integer `-4` eigenvector of squared norm 56.

For the rank-three form, every product-one edge joins opposite signs and
`r=0`, so the integer point image satisfies `A b~=3b~`.  The only compatible
marked profiles are

```text
2 selected intersections: C(12,2)=66 subsets, point weight 20;
5 selected intersections: C(12,5)=792 subsets, point weight 14.
```

No other rank-three point weight survives the frozen marked restrictions.
This is a classification of the marked branch, not an existence theorem.

## General integer spectral lift

For a nonzero `x in ker_F3(A)`, take the signed integer lift, write
`p-n=3t`, `w=||x||^2`, and `z=Ax/3`.  Then

```text
Az=4x-z+2t*1,  sum(z)=14t.
```

The independently verified integral eigensplitting is

```text
Q=9(z-x)-t*1,       AQ=-4Q,
R=11(4x+3z)-6t*1,  AR= 3R,

Q^2=63[3(w-x.z)+t^2],
R^2=77[11(4w+3x.z)-18t^2].
```

Every `Q_i=-t mod 9`, which yields the exact shell quantization

```text
Q^2=99t(9-t)+162L,  L>=0.
```

The complete necessary tables at weights 17, 20, and 23 retain every sign
composition previously under consideration.  They are arithmetic rows, not
constructed codewords.

For balanced weight 14, `q=z-x` is an integral `-4` eigenvector and

```text
q^2 in {0,14,28,42,56,70}.
```

In the `q=0` branch, the row with 13 same-sign edges exceeds exact
common-neighbor wedge capacity.  The row with 12 reaches equality, which
forces every internal edge into its unique internal triangle and hence forces
even internal degrees, contradicting the four forced degree-three vertices.
The row with 11 same-sign edges survives: each sign side has degree sequence
`(4,3,3,3,3,3,3)` and there is exactly one cross edge.

In the `q^2=14` branch, the imported independently audited theorem makes the
two signs of `q` the complementary-Fano `2-(7,4,2)` design.  A complete
labelled capacity census eliminates every same-sign overlap `alpha>=2` and
leaves 42 rows with `alpha=1`.  A separate two-orientation signed-demand and
cross-side endpoint-coupling check eliminates those 42 rows and forces

```text
alpha=0, opposite overlap beta=6,
|supp(x) union supp(q)|=22,
z has eight +1 and eight -1 entries,
k in {2,3,4}.
```

For `k=2` or `4` the smaller exclusive side is `K3`; for `k=3` both
exclusive sides are `C4`.  All three cases remain.  The other five norm
shells also remain, so no weight is excluded.

## Local controls are not completions

The rank-three marked controls replay at exactly

```text
weight 20: 22 vertices, 53 edges, 2 intersections, A_U b_U=3b_U;
weight 14: 19 vertices, 44 edges, 5 intersections, A_U b_U=3b_U.
```

The proof-A hostile control has 22 vertices and satisfies all displayed
`Ax=3z`, `Az=4x-z`, and `Aq=-4q` equations.  All three controls respect the
recorded local degree, triangle, and common-neighbor upper caps.

The verifier then added one zero-coordinate outside vertex to each family.
The internal equations and upper caps still hold, but the new outside row
has nonzero residual.  This is an explicit veto on inferring the missing
outside equations or an SRG completion from any local control.

## Independent verification

Root replay after the final seal obtained

```text
M7g norm source tests:                 8/8 PASS
marked proof-B source tests:           5/5 PASS
integer-lift proof-A source tests:    10/10 PASS
Wave94 imported verifier tests:       12/12 PASS
Wave208 clean-room verifier tests:    33/33 PASS
four package manifests:               PASS (10+11+10+24 entries)
```

Verifier package manifest SHA-256:

```text
c9551a7c4d62a57f081b8008f49b9e27fb0372f50a7d114e10136557242fbab4
```

Recorded coverage and scope findings are retained rather than silently
repaired:

1. proof B hard-coded the count of four concurrent-secant matchings; the
   verifier enumerated all 105 matchings and confirmed it;
2. proof A sampled spectral identities after comparing precomputed
   coefficients; the verifier performed a general symbolic expansion;
3. the original M7g construction prose incorrectly named 91 outside
   vertices; the corrected sealed package says the union size is not fixed;
4. explicit outside-row witnesses refute every local-to-global implication.

No frozen mathematical theorem was refuted.

## Exact next frontier

Two disjoint symbolic branches remain:

1. classify or exclude the rank-three `A b=3b` trades of point weight 14
   and 20 using their full selected-line and outside signatures;
2. classify or exclude the three rank-four integer `-4` eigenvectors of
   squared norm 56 using all 231 triangle sums and the integral incidence
   lattice.

Either route needs the omitted global equations or a checked complete
object.  Aggregate feasibility, a local non-hit, or a positive partial
control cannot change the endpoint status.
