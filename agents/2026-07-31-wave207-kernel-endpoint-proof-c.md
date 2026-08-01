# Wave 207 proof D: kernel endpoint sign balance

```yaml
role: proof_b
date_utc: 2026-08-01T01:53:36Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: conditional weight-fourteen sign-composition reduction in ker_F3(A)
inputs:
  - CONJECTURE.md: 7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58
  - attempts/wave207-ternary-adjacency-code-bridge/derivation.md: 27860e2f8b5ce23c37a43a1ef53fb31d7eda1ee67926e04406ccbf0d938e40b5
  - attempts/wave207-ternary-adjacency-code-bridge/exact-results.json: 94ed011861be9cf201ac5c531a704832cf8675c5b993c420e92a2e5812f8e7d8
method: exact signed common-neighbor moments and two pointwise Farkas inequalities
command: .\.venv\Scripts\python.exe -B -m unittest -v attempts\wave207-kernel-endpoint-proof-c\test_exact_check.py
outputs:
  - attempts/wave207-kernel-endpoint-proof-c/derivation.md: da5397c731df8912e076671f80724413be8ab3b5e6dd2336778c61741c25b69f
  - attempts/wave207-kernel-endpoint-proof-c/exact_check.py: 56e2f34d3775665e6bbe2e865c3f377b2b9784e947d55d327f976733bef62437
  - attempts/wave207-kernel-endpoint-proof-c/exact-results.json: f323f6735893c0f1b48de7c1eab92e964fc7a6ab89fe479ae985aeec1662bc4e
  - attempts/wave207-kernel-endpoint-proof-c/balanced-aggregate-control.json: b8304be81f5ff504a4afe234e8e07c5c84fd5e6a82c9153a6e69971b7fc4b445
limitations: weight fourteen is not excluded; its balanced 7+7 branch and weights 17, 20, and 23 remain UNKNOWN; the hostile aggregate control is deliberately nongraphical; no graph, codeword, endpoint, global proof, or counterexample is constructed
```

## Result

For a ternary adjacency-kernel word of weight fourteen, the congruence
`p-n=0 mod 3` permits five sign compositions.  Exact pointwise nonnegative
polynomials have global sums `-35` for `(p,n)=(1,13)` and `-12` for
`(4,10)`.  Negating the word handles `(13,1)` and `(10,4)`.  Therefore any
such word must have exactly seven positive and seven negative coordinates.

This is a strict reduction, not a weight-fourteen exclusion.  The balanced
branch survives the submitted equations, and the upstream endpoint remains
unresolved.

## Verification request

Independently reconstruct equations (2), enumerate the exact membership
ranges for both polynomials, confirm pointwise nonnegativity and global sums,
and check that no conclusion in the package promotes the hostile aggregate
control to a graph or codeword.

