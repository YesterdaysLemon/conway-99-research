# Wave 206 Proof B addendum: tensor-balance weight at least eight

```yaml
role: proof_b
date_utc: 2026-07-29T22:10:12Z
git_commit: 85e705cc6c2a14d123120c93a847e30aaab1789e
claim_label: DERIVED
scope: >-
  Conditional Wave 206 tensor-balance code: prove that every nonzero word
  has support at least eight and audit sharpness of the local argument.
inputs:
  attempts/wave206-crossing-kernel-proof-b/package-manifest.sha256: 6c7718de1c5f2c7d4203d1727d6b74214e51fa069608f318c8583b07b0325f0a
  verification/wave174-no-weight3-dual/package-manifest.sha256: ac34c8a3b045bec70e3a2080cb4365c0ea43cc732b313ecb3cec355a28f23450
method: >-
  Coefficient-space Witt bound, exact small projective caps, and an exact
  singular weight-eight control in a nonsquare 11-space.
command: >-
  .\.venv\Scripts\python.exe -B
  attempts\wave206-tensor-balance-weight-proof-b\exact_check.py --verify
  attempts\wave206-tensor-balance-weight-proof-b\exact-results.json ;
  .\.venv\Scripts\python.exe -B -m unittest -v
  attempts\wave206-tensor-balance-weight-proof-b\test_exact_check.py
outputs:
  attempts/wave206-tensor-balance-weight-proof-b/exact-results.json: e1dd9c788b54016dc63284ad7a8602723ee714b8e703e224fc9e39e1fbbf5d47
  attempts/wave206-tensor-balance-weight-proof-b/derivation.md: 7d13a1834819e952c4d4eff033fac033e23699ab643d9852318a67d19bcb6cf2
limitations:
  - The existence of A_Delta remains a Wave 206 discovery claim pending verification.
  - The weight-eight control lacks the target global incidence.
  - Endpoint and Conway-99 status remain UNKNOWN.
```

## Result

Let a nonzero tensor-balance word have support size `k`, and write

```text
sum_i a_i(z_i tensor z_i)=0,
Lambda=diag(a_i).
```

After removing the invertible ambient form and restricting to the support
span,

```text
V Lambda V^T=0.
```

The row space of `V` is therefore totally isotropic in the nondegenerate
coefficient form `Lambda`, giving

```text
rank(V)<=WittIndex(Lambda)<=floor(k/2).
```

Verified dual distance at least four makes the support points a projective
cap.  Exact cap maxima in vector ranks one, two, and three are

```text
1,2,4.
```

For every `k<=7`, the Witt bound puts the support in rank at most three,
where the relevant cap maximum is smaller than `k`.  Hence

```text
wt(a)>=8.
```

If equality holds, the support span has rank four, `Lambda` is split, and
the number of coefficient-two entries is even.

## Sharp local boundary

An exact eight-column control has:

```text
rank(V)=4,
every three columns independent,
V Lambda V^T=0,
all columns singular,
ambient form nonsquare and nondegenerate of dimension 11.
```

Thus the audited local ingredients cannot prove weight at least nine.  The
control does not provide the target 231-column frame, incidence, graph, or
membership in `im(B^T)`.

No endpoint exclusion or status change follows.
