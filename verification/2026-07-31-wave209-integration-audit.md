# Wave 209 integration audit

```yaml
role: orchestrator
date_utc: 2026-08-01T03:48:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Integrate the independently sealed Wave 209 rank-three signed-trade and
  rank-four norm-56 reductions without promoting anonymous point, line, or
  aggregate censuses to a 99-vertex graph or endpoint result.
inputs:
  - path: attempts/wave209-four-survivor-globalization/protocol.md
    sha256: 3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196
  - path: attempts/wave209-four-survivor-globalization/input-freeze.sha256
    sha256: 0eb8033fc5fdc6f7284c96a29ba609eb065a2aa06cd30b125adc24dbacc1bdb3
  - path: attempts/wave209-four-survivor-globalization/post-freeze-inputs.sha256
    sha256: 5a1117778a044ec11a211b34861529e3fbce99e393245338befdd3b33a6a7fbb
  - path: attempts/wave209-four-survivor-globalization/upstream-delta.md
    sha256: 0d6f4d8f3beaf90151eff21c968526c1149892e019eef6d24492504f0cbf5f10
  - path: attempts/wave209-rank3-trade-proof-a/package-manifest.sha256
    sha256: 521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
  - path: verification/wave209-four-survivor-verifier/package-manifest.sha256
    sha256: 7e20ac726cc4823360e49d3fcf08e5c8ff6c7f219c5d1cbbba781d015fe59c91
  - path: attempts/wave209-rank4-norm56-proof-b/package-manifest.sha256
    sha256: 2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b
  - path: verification/wave209-rank4-point-signature-verifier/package-manifest.sha256
    sha256: 62c32cfa278a677053353d5a3c21c01600cadc867d597f5135ab32a6fdb1c07a
method: >-
  Replay all source and verifier tests, validate every manifest entry, compare
  the verifier claim matrices with the sealed source statements, preserve the
  352 aggregate versus 346 combined-cap distinction, and reject every
  local-to-global implication not backed by outside adjacency.
command: >-
  .\.venv\Scripts\python.exe -B -m unittest
  attempts\wave209-rank3-trade-proof-a\test_exact_check.py
  verification\wave209-four-survivor-verifier\test_independent_rank3.py
  verification\wave209-four-survivor-verifier\test_post_source_audit.py
  attempts\wave209-rank4-norm56-proof-b\test_exact_check.py;
  .\.venv\Scripts\python.exe -B -m unittest discover
  -s verification\wave209-rank4-point-signature-verifier -p test*.py
outputs:
  - path: logs/2026-07-31-wave209-public-checkpoint.json
    sha256: a9f231f16f7ca5fbe20327577ba5da43e5fd1c4c49f3396ee7c11c5e74925cbb
limitations:
  - The rank-three marked and deficit objects omit the 85-vertex outside graph.
  - The rank-four survivor controls are anonymous 99-row and 223-line censuses.
  - The new 352-to-346 cap is DERIVED, not independently promoted to VERIFIED.
  - Rank 11, n3=4158, Conway-99, novelty, and priority remain UNKNOWN.
  - AGENTS.md names Orchestrator as a project role but omits it from the
    fenced run-report role enum; this report retains the semantic role and
    records that pre-existing schema gap instead of changing sealed inputs.
```

## Frozen inputs and replay

The historical protocol freeze retains the then-observed Wave 208 verifier
manifest hash.  `upstream-delta.md` records that hash alongside the current
corrected verifier manifest and integration audit; `post-freeze-inputs.sha256`
pins the latter two without rewriting history.  The unavailable earlier
manifest contents are not silently reconstructed or substituted.

The four sealed package manifests reproduce exactly:

```text
rank-three discovery:  521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
rank-three verifier:   7e20ac726cc4823360e49d3fcf08e5c8ff6c7f219c5d1cbbba781d015fe59c91
rank-four discovery:   2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b
rank-four verifier:    62c32cfa278a677053353d5a3c21c01600cadc867d597f5135ab32a6fdb1c07a
```

All 43 manifest entries match.  The submitted and independent suites replay
as `11+15+9+6=41` passing tests.  Both verifiers reconstruct complete labelled
sets rather than checking only headline counts.  The rank-three verifier
preserves its original pre-correction Wave 208 freeze and separately pins the
current integration audit at
`eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754`.

## Rank-three branch

For `c=U alpha`, the exact selected-line identity

```text
(U^T A U-3U^T U) alpha=0
```

forces the cross count of each matched product-zero opposite pair to vanish.
This is a labelled statement; no graph automorphism is assumed.

For point support 14, independent reconstruction verifies:

```text
|P|=|N|=7,
e(P,N)=1,
one rooted sign-side graph type,
outside signatures (z0,z1,z2)=(17,61,7),
4480 of 5040 deficit-edge bijections,
204 of 792 marked five-intersection graphs.
```

The sign-side graph has edges

```text
01 02 03 04 12 15 26 34 35 46 56.
```

Its seven same-sign common-neighbor deficits are triangle-free.  The 4,480
bijections and 204 marked graphs are compatible necessary objects, not outside
adjacency completions; none is excluded here.

For point support 20, the exact selected-zero and aggregate reductions give:

```text
x=0: excluded,
x=2: only six swapped-disjoint marked pairs,
x=4: 42 marked pairs survive the selected-zero lower bound,
x=6,8: all 66 marked pairs survive that lower bound,
x=10: excluded,
aggregate rows at x=2,4,6,8: 109+157+76+10=352.
```

The `352` number is VERIFIED only as a catalog of degree histograms,
bipartite graphicality, and outside first/two-star moments.  The rank-three
verifier then combined that table with the selected-line equation: every
support point lies on one selected line, meets no support point on its matched
opposite line, and can meet at most one support point on each of the other
three opposite lines.  Thus opposite degree is at most three.  Six `x=4`
rows contain a degree-four star and fail, leaving `346` rows under the added
cap.  This additional narrowing remains `DERIVED` pending a separate
independent promotion.  Neither 352 nor 346 counts graphs.

For the 231-line vector `tau=B^T c`, the exact necessary identities are

```text
C tau=7 tau,  B tau=10c,  sum(tau)=0,  ||tau||^2=20k.
```

The archived line histograms satisfy these moments but do not assign the 231
actual triangles or their intersections.

## Rank-four branches

For each of the three rank-four forms, let

```text
q=(A-3I)U alpha/3,  Aq=-4q,  q^2=56,
t=B^Tq,              Ct=0,   t^2=168.
```

The marked entries are `t_i=-3 alpha_i`.  The zero-eigenspace interpolation
bound is exactly 168, so the real extension is projector-saturated.  Reducing
modulo two gives `U^T(q mod 2)=1_8`; hence `q` is not even and division to the
norm-14 complementary-Fano shell is invalid.

Exact sign-preserving constraint relabellings partition all `3*83=249`
labelled marked branches into 24 orbits.  The complete 99-point signature
census uses all 2,187 divisible signatures and 279 exact marginal, pair, sum,
and norm equations.  It proves:

```text
17 orbits / 198 labelled branches: excluded by integer Farkas certificates,
 7 orbits /  51 labelled branches: retain integer census controls,
survivors per rank-four form:       17 of 83.
```

Every Farkas vector is replayed with `A^T y>=0` on all allowed signatures and
`b^T y<0`; solver status is not evidence.  Every survivor control is replayed
against all 279 equations after transport.  All three forms still survive.

The controls do not name the 99 points, couple them to the 223 residual
triangles, realize all residual rows of `Ct=0`, decompose the block graph into
99 point-star `K7` cliques, or construct an adjacency matrix satisfying
`Aq=-4q`.  They are therefore not graph or eigenvector completions.

## Status wall

```text
rank-three weight-14 branch:        NOT EXCLUDED
rank-three weight-20 branch:        NOT EXCLUDED
rank-four forms:                    3/3 STILL SURVIVE
rank-four labelled marked branches: 51 CENSUS SURVIVORS
full 99-vertex adjacency:           NONE
endpoint exclusion:                 NONE
rank-11 endpoint:                   UNKNOWN
n3=4158 endpoint:                   UNKNOWN
rigorous n3 interval:               708<=n3<=4158
conditional Q bound:                Q>=7059
Q>=7060:                            NOT PROVED
Conway-99:                          UNKNOWN
```
