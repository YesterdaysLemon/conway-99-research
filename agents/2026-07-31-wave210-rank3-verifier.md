# Wave 210 rank-three marked/outside coupling verifier

```yaml
role: verifier
date_utc: 2026-08-01T04:19:50Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: sealed conditional weight-14 selected-union coupling; no D completion
inputs:
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256 sha256 d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722
  - verification/wave210-rank3-marked-outside-coupling-verifier/input-freeze.sha256 sha256 717b36cfbfec5d6c22cc968518e08a72e0a9764d1b5ca662dc99f31bd190c11d
  - verification/wave210-rank3-marked-outside-coupling-verifier/pre-source-comparison-seal.sha256 sha256 8fac8f07e3c3ca2605e30e7e08387586d5ef028881d0fcb865b73c0676f34067
method: independent labelled reconstruction, complete symmetry/orbit audit, exact rank and local-matching checks, full set comparison, hostile controls
command: .venv\Scripts\python.exe -B verification\wave210-rank3-marked-outside-coupling-verifier\verify_sealed.py
outputs:
  - verification/wave210-rank3-marked-outside-coupling-verifier/independent-results.json sha256 350134f2e5593d3d83e3463b1a536622db294a127c5fccab05a7b42858ce42bd
  - verification/wave210-rank3-marked-outside-coupling-verifier/post-source-audit.json sha256 52c3e04799cc25547f8caad057b7cf224a37bbdb275a6844f806657b0fab76bb
limitations: conditional local reduction only; no D; no 99-vertex graph or exclusion; global status UNKNOWN
```

Verdict: **PASS / NO VETO**.

The source-blind verifier independently reproduced the complete reductions
`204 -> 96` labelled `H`, `20,928 -> 1,536` labelled packing cases, and
`93,757,440 -> 55,296` labelled case/deficit triples.  The exact surviving set
has three of 33 proved case orbits: 0, 4, and 29.

All 4,480 capacity-compatible `F` configurations satisfy the common Gram
identity and therefore have rational rank 13.  All 62,720 support-neighborhood
one-factor instances are feasible, with the submitted matching-count
distribution reproduced exactly.

The complete order-48 polar group and order-4 rooted-support group were found by
brute-force permutation enumeration.  The coupled order-768 action is closed,
faithful, and has Burnside fixed-point sum 25,344, giving 33 case orbits.  No
target-graph automorphism enters the reduction.

Complete labelled sets, orbit memberships, matching-index sets, all `F`
columns/residuals, and all local matching vectors agree with the sealed source.
All manifests validate.  The three hostile controls independently replay and
are confirmed to be 19-point partial controls, not completions.  All hostile
mutations fail closed.

One verifier-interface issue is recorded: the pre-source-sealed script's direct
`--verify` comparison reaches the end of the recomputation but compares JSON
lists to Python tuples.  The additive `verify_sealed.py` wrapper canonicalizes
that representation.  This does not affect the mathematical comparison.

No `85 x 85` block `D` is constructed or excluded.  Conway-99 remains
`UNKNOWN`.
