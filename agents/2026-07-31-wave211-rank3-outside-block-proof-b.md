# Wave 211 proof B: rank-three outside-block algebra

```yaml
role: proof_b
date_utc: 2026-08-01T04:20:49Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: exact linear, degree, spectral, and parity consequences of the 85x85 outside block for all three Wave 210 rank-three survivor orbits
inputs:
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json sha256 32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256 sha256 d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722
method: exact U/K block reduction, rational and mod-2 ranks, conditional spectrum, and explicit linear-block hostile control
command: .venv\Scripts\python.exe -B attempts\wave211-rank3-outside-block-proof-b\exact_check.py --verify
outputs:
  - attempts/wave211-rank3-outside-block-proof-b/exact-results.json sha256 7064f0b4ad0f1fac2e40121c87500ae32fe8c4b532371921c2a461abf43932de
  - attempts/wave211-rank3-outside-block-proof-b/hostile-linear-control.json sha256 6c2ab54613c38dc9b6942ee08b9c0930957c949edcec0c8821380457d391e98e
limitations: orbit 29 survives only the linear block and fails the quadratic block; orbit 0 and 4 searches are inconclusive; no full D is constructed or excluded; global status UNKNOWN
```

For every one of the three Wave 210 representatives,
`rank_Q(F)=rank_F2(F)=13` and adjoining the all-ones row raises both ranks to
14.  The linear block and degrees force `D` on the 14-dimensional space
`U=im(F^T)+<1>`, leaving the 71-dimensional complement
`K=ker(F) intersect 1^perp`.

The exact characteristic polynomial on `U` is

```text
x^2 (x+2)^2 (x^2-2)^3 (x^4-8x^3-50x^2-40x+32).
```

If the quadratic block held, symmetry would force `D|K` to have eigenvalues
`3^40,-4^31`.  All trace and square-trace checks are consistent, and modulo
two the restriction becomes `D^2+D=0` on `ker(F)`.  No spectral or parity
contradiction results.

For orbit 29, an explicit 520-edge simple graph satisfies all 1,190 entries of
the linear block, all 85 degrees, and all ten selected pair values.  It is a
hostile control for linear exclusion arguments, not a completion: it violates
2,416 of the 3,570 off-diagonal common-neighbor equations.  Orbit 0 and orbit
4 capped searches produced no primal and remain inconclusive.  No target
automorphism was assumed.
