# Wave 208 proof A: integral spectral splitting and Fano overlap rigidity

```yaml
role: proof_a
date_utc: 2026-08-01T02:32:25Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: conditional pointwise integer-lift reduction for residual ternary adjacency-kernel weights, with a complete balanced weight-14 complementary-Fano overlap census
inputs:
  - attempts/wave208-global-residual-rigidity/protocol.md: 3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740
  - attempts/wave207-ternary-adjacency-code-bridge/exact-results.json: 94ed011861be9cf201ac5c531a704832cf8675c5b993c420e92a2e5812f8e7d8
  - attempts/wave207-kernel-endpoint-proof-c/exact-results.json: f323f6735893c0f1b48de7c1eab92e964fc7a6ab89fe479ae985aeec1662bc4e
  - verification/wave71-modular-theta-extension/audit.md: 0a6280aa008ea7d329c3609bb044f636d52600315e5aff78a27c4712a439cd73
  - verification/wave94-general-n3-norm14-bound/audit.md: ab87d369345a27abb4326915f6c392545573780b4fc7f5d67bc494743c4a2ce6
method: exact integral eigenspace splitting, residue-shell arithmetic, lambda/mu wedge capacity, complete labelled complementary-Fano partition census, coupled outside-endpoint counting, and a hostile 22-vertex partial control
command: .\.venv\Scripts\python.exe -B attempts\wave208-integer-lift-proof-a\exact_check.py --verify attempts\wave208-integer-lift-proof-a\exact-results.json; .\.venv\Scripts\python.exe -B -m unittest -v attempts\wave208-integer-lift-proof-a\test_exact_check.py
outputs:
  - attempts/wave208-integer-lift-proof-a/derivation.md: 03514a173a24e0fdfd8b1c01038583bc71ba218f8937a1f9fc389a171851765d
  - attempts/wave208-integer-lift-proof-a/exact_check.py: 07eeeb9cb5323e64192bab18e67fada82af2a534c5b8bea71e43c596a158e871
  - attempts/wave208-integer-lift-proof-a/exact-results.json: 8d6656cf476d2c75b05134d307e3694e283a95811b749610ae5daf20e12bc4da
  - attempts/wave208-integer-lift-proof-a/run-report.yaml: 41056092f40a81acd5c14d1576b000afef237f487478c75361008862f1d4cb34
limitations: no residual weight is excluded; the hostile partial control is not a graph completion; weights 17,20,23 receive arithmetic shell data only; Conway-99 and the rank-11 endpoint remain UNKNOWN
```

## Result

For any residual word, the pointwise lift produces exact integral restricted
eigenvectors

```text
Q=9(z-x)-t*1,             AQ=-4Q,
R=11(4x+3z)-6t*1,        AR= 3R.
```

Their exact norms and the coordinate residue of `Q` give

```text
Q.Q=63[3(w-h)+t^2]
    =99t(9-t)+162L,
R.R=77[11(4w+3h)-18t^2].
```

At balanced weight 14, `q=z-x` has squared norm in
`{0,14,28,42,56,70}`.  The zero row is reduced to one surviving exact
`3`-eigenvector shape: a single cross edge and same-sign degree sequence
`(4,3^6)` on each side.

In the norm-14 row, the independently audited complementary-Fano structure
allows a complete seven-point census.  All overlap cases with at least two
same-sign coordinates fail exact outside-token capacity.  The 42 preliminary
one-same-coordinate survivors fail after the two Fano sides are coupled by
the fact that every used outside vertex has one endpoint on both sides.
Therefore the only surviving norm-14 geometry has

```text
six opposite-sign overlaps,
zero same-sign overlaps,
22 vertices in the support union,
z = eight +1 and eight -1,
k in {2,3,4} on the exclusive signs.
```

The exclusive subgraph is forced to contain a `K3` on the smaller side for
`k=2` or `4`; for `k=3` it is two disjoint `C4`s with no cross edge.

This does not exclude weight 14.  The package includes a labelled 22-vertex
partial control satisfying `Ax=3z`, `Az=4x-z`, `Aq=-4q`, and every displayed
`lambda/mu` upper cap.  Its missing 77 vertices are precisely the unresolved
global-extension layer.

## Verification request

Independently reconstruct (3)--(7), the six balanced shells, the `q=0`
wedge/parity reduction, and the labelled Fano census.  In particular, check
the coupling that turns 42 one-same-coordinate capacity rows into zero, and
confirm that the hostile control satisfies only a 22-vertex partial system
and is never promoted to a codeword or graph.

