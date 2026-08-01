# Wave 209 verifier: rank-four point signatures

```yaml
role: verifier
date_utc: 2026-08-01T03:25:04Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  The exact conditional rank-four reduction in the sealed Wave209 proof-B
  package, including every labelled exclusion and every positive census
  control; no promotion of a census to a graph or of the branch reduction
  to a global result.
inputs: verification/wave209-rank4-point-signature-verifier/input-freeze.sha256
method: >-
  Clean-room finite-field reconstruction, rational projector audit, exact
  integer dual verification, explicit constraint transport over all 249
  labelled branches, positive-control replay, and hostile mutation tests.
command: >-
  .\.venv\Scripts\python.exe -B
  verification\wave209-rank4-point-signature-verifier\independent_verify.py
  --verify ; .\.venv\Scripts\python.exe -B -m unittest -v
  verification\wave209-rank4-point-signature-verifier\test_independent_verify.py
outputs: verification/wave209-rank4-point-signature-verifier/package-manifest.sha256
limitations:
  - Verification is conditional on the frozen endpoint and rank-four branch.
  - Fifty-one labelled branches survive only as anonymous signature censuses.
  - No adjacency matrix, 231-block frame, complete eigenvector, graph, or nonexistence certificate is supplied.
  - Conway-99 remains UNKNOWN.
```

## Verdict

`PASS_NO_VETO`.

The three rank-four form matrices and their marked subsets were rebuilt from
the vanishing symmetric-form space rather than imported from discovery code.
The reconstruction gives 83 subsets per form and an exact 249-node partition
into 24 constraint-relabeling orbits with size distribution
`3^1, 6^9, 12^12, 24^2`.

For `t=B^Tq`, the incidence algebra gives `Ct=0`, `t.t=168`, and residual
norm 96.  On all three forms the selected projector bound is exactly 168,
so the real extension is the unique saturated interpolant.  Every selected
sum is odd, proving `q` is not even and blocking division to norm 14.

All 17 integer Farkas vectors have `A^Ty>=0` on all 2,187 allowed point
signatures and `b^Ty<0`.  Their constraint names and pair orientations were
transported and recomputed for every one of the 198 excluded labelled
branches.  The seven positive archives were rechecked against all 279
equations on all 51 surviving branches.  All 24 aggregate controls and all
selected-union witnesses were likewise transported and replayed across all
249 labelled branches.  Erased or reversed duals and one-count mutations of
both positive archives are rejected.

The exclusions are exact necessary-condition exclusions.  The surviving
controls are anonymous row-count tables, not graph points, adjacency, or
full `-4` eigenvectors.  The target status is still `UNKNOWN`.
