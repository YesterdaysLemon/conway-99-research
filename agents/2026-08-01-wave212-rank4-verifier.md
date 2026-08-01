# Wave 212 rank-four full-coupling verifier

```yaml
role: verifier
date_utc: 2026-08-01T05:30:20Z
git_commit: 698f4db2cecd67fb4b9cfa8ff2bf7b375d9d93f3
claim_label: VERIFIED
scope: >-
  Conditional exclusion of all seven Wave209 rank-four survivor orbits and
  all 51 labelled branches; no rank-three or global promotion.
inputs: verification/wave212-rank4-full-coupling-verifier/input-freeze.sha256
method: >-
  Blind full-signature reconstruction and exact integer dual replay, followed
  post-seal by complete canonical source-matrix comparison, exact archived
  dual replay, zero-extension proof, 51-branch constraint transport, and
  hostile coefficient/RHS/column/map mutations.
command: >-
  See verification/wave212-rank4-full-coupling-verifier/run-report.yaml
outputs: verification/wave212-rank4-full-coupling-verifier/package-manifest.sha256
limitations:
  - Conditional on the frozen endpoint and verified Wave208/209 rank-four reduction.
  - Rank three and Conway-99 remain UNKNOWN.
```

## Outcome

`PASS_NO_VETO`.  The previous Wave210 promotion veto is closed.

Before opening Wave210, the verifier reconstructed seven larger systems with
2,187 signatures, 4,752 rows, and 19,348--20,524 W/X columns.  Seven new
integer Farkas vectors replay with strictly positive minimum column values and
negative right-hand sides.  The code, results, and duals are blind-sealed.

Post-seal, the exact membership filter and forced `H[h]` intersection grouping
were reconstructed.  All seven membership-filtered source matrices match the
independent matrices completely after semantic canonicalization.  Every
archived integer dual replays with `A^T y>=0` and `b^T y<0`; the exact right
sides are

```text
-4, -239020, -18, -18, -239020, -3240, -4.
```

The verifier also checked that every filtered column zero-extends into the
larger blind system, transported all seven certificates over all 51 labelled
branches, and checked 601,377 transported local patterns.  No target
automorphism was assumed.  Erased/reversed coefficients and mutated RHS,
column, and map controls are rejected.

This verifies only the conditional rank-four exclusion.  Rank three and the
global Conway-99 claim remain `UNKNOWN`.
