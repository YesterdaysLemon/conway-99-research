# Wave 209 verifier: rank-three signed trade

```yaml
role: verifier
date_utc: 2026-08-01T03:40:53Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: sealed Wave 209 rank-three proof-A package under its explicit conditional and aggregate walls
inputs:
  - attempts/wave209-rank3-trade-proof-a/package-manifest.sha256 sha256 521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
  - verification/wave209-four-survivor-verifier/input-freeze.sha256
method: source-blind symbolic reconstruction, label-complete finite censuses, hostile mutations, then full-set post-source comparison
outputs:
  - verification/wave209-four-survivor-verifier/audit.md
  - verification/wave209-four-survivor-verifier/exact-results.json
  - verification/wave209-four-survivor-verifier/post-source-audit.json
limitations: no 99-vertex certificate; six-row tightening is new DERIVED work; all global endpoints remain UNKNOWN
```

## Verdict

`PASS_VERIFIED_SCOPED_WITH_DERIVED_352_TO_346_NARROWING_NO_RESOLUTION`.

The source seal and all ten entries match.  Discovery replay passed 11/11
tests; the clean-room and post-source suites passed 9/9 and 6/6.  Complete
result sets agree for the five weight-14 aggregate rows, all 425 weight-20
aggregate rows, the 204 marked weight-14 subsets, all 66 marked weight-20
lower bounds, and the retained 352-row aggregate table.

The verifier additionally derives that the exact selected-line cross counts
force opposite degree at most three for every support point.  Six `x=4`
aggregate rows have a degree-four star and are removed, leaving 346 rows under
this extra necessary cap.  That narrowing is `DERIVED` pending a second
verifier and is not a graph construction or exclusion.

The rank-three branch, rank-11 endpoint, `n3=4158`, and Conway-99 remain
`UNKNOWN`.
