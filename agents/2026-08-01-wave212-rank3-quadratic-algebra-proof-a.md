# Wave 212 proof A: rank-three quadratic K-block algebra

```yaml
role: proof_a
date_utc: 2026-08-01T05:02:51Z
git_commit: 698f4db2cecd67fb4b9cfa8ff2bf7b375d9d93f3
claim_label: DERIVED
scope: exact mod-2 Jordan and conditional K-projector local-minor closure for survivor orbits 0, 4, and 29
inputs:
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json sha256 32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd
  - attempts/wave211-rank3-outside-block-proof-b/package-manifest.sha256 sha256 c8066f81ad607d598755442994c7804ebc375f9d637ed33e5cbd8335aae47a10
method: exact F2 power ranks and Jordan reconstruction plus exact rational K-projector local-minor tests
command: python attempts\wave212-rank3-quadratic-algebra-proof-a\exact_check.py --verify
outputs:
  - attempts/wave212-rank3-quadratic-algebra-proof-a/exact-results.json sha256 782a89c9ff134b73427bc9235548e830038ebefacb61efdf21602eb54f0f7df9
limitations: no D, graph, or exclusion; projector tests stop at 2-by-2 minors; global status UNKNOWN
```

For all three Wave 210 survivor representatives, exact reduction over
`F_2` gives

```text
rank((F^T F)^k), k=1,...,5: 12,8,4,2,0.
```

Thus `F^T F` has Jordan type

```text
J_5(0)^2 direct-sum J_3(0)^2 direct-sum J_1(0)^69.
```

If the quadratic block holds, `D^2+D=F^T F` modulo two.  On each primary
space, `D=lambda I+T` gives `D^2+D=T(I+T)`, whose powers have the same ranks
as those of `T`.  Therefore any completion has exactly the four nontrivial
blocks `J_5,J_5,J_3,J_3`, with their allocation between primary roots `0`
and `1` still undetermined.  The conditional characteristic polynomial is

```text
x^45(x+1)^40 = x * (x^22(x+1)^20)^2,
```

so the odd-order alternating-matrix parity test is exactly compatible.

The exact orthogonal projector onto
`U=im(F^T)+<1>` and the forced operator `D P_U` determine all diagonal local
multiplicities of the conditional `3`- and `-4`-projectors on `K`.  Every
diagonal lies strictly in `(0,1)`, with traces `40` and `31`.  More strongly,
for every one of the 3,570 off-diagonal positions in every orbit, both
`D_ij=0` and `D_ij=1` satisfy both exact `2 x 2` PSD inequalities.  Hence
neither projector diagonals nor pairwise Cauchy--Schwarz forces an entry.

This is a stopping-wall result, not a construction or exclusion.  Larger
projector minors retain the unresolved quadratic correlations.  Orbits
`0`, `4`, and `29`, the rank-three branch, and Conway-99 remain `UNKNOWN`.

