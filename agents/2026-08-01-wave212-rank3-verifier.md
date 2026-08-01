# Wave 212 rank-three independent verifier

```yaml
role: verifier
date_utc: 2026-08-01T05:19:08Z
git_commit: 698f4db2cecd67fb4b9cfa8ff2bf7b375d9d93f3
claim_label: VERIFIED
scope: independent replay of Wave 212 common-neighbor and quadratic-algebra rank-three packages, with split verdict on a Jordan-allocation boundary
inputs:
  - attempts/wave212-rank3-common-neighbor-proof-b/package-manifest.sha256 sha256 6fbd4427f701d63e40df2718057dab37b0b7930cc5dc9f0ed7ecf76eab813447
  - attempts/wave212-rank3-quadratic-algebra-proof-a/package-manifest.sha256 sha256 10dbc03ce2ea6e9f5bed46ab5b735fe36d6dddd073a40010c947e59f516496ab
method: sealed preinspection reconstruction, independent exact replay, rational projector arithmetic, F2 power-rank and forced-U audit, and hostile in-memory mutations
command: C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe -B verification\wave212-rank3-symbolic-verifier\independent_verify.py --verify
outputs:
  - verification/wave212-rank3-symbolic-verifier/exact-results.json sha256 9edea84a3a834c4426758d90992f0782140a5681b9976eaf254e4e0ff6493c13
limitations: proof-B controls are restricted non-completions; proof-A Jordan allocation correction is verifier-derived and pending independent promotion; no D is constructed or excluded; global status UNKNOWN
```

Proof B receives `PASS / NO VETO` in its exact restricted scope.  Proof A's
`F^T F` Jordan computation and projector computations receive
`PASS / NO VETO`, but its statement that the nontrivial `D` blocks remain
unallocated receives `VETO / REFUTED`.  The forced action on `U` is nilpotent,
so all nontrivial Artin--Schreier chains are zero-primary.  That correction is
recorded as `DERIVED` by the verifier and awaits independent promotion.

No control is a completion, no orbit is excluded, and Conway-99 remains
`UNKNOWN`.
