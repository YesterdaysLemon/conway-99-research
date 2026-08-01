# Wave 211 rank-three outside-block proof B

This package tests exact linear, degree, spectral, and parity consequences of
the unknown symmetric `85 x 85` outside adjacency block `D` for all three
Wave 210 surviving case-orbit representatives.  Wave 210 is treated as
`DERIVED` pending its independent verifier.

The substantive result is a stopping-wall result, not an exclusion:

- all three representatives have the same exact 14-dimensional forced
  rational action and 71-dimensional unresolved complement;
- the conditional spectrum required by the full quadratic block is
  arithmetically consistent;
- orbit 29 has an explicit 520-edge binary graph satisfying all 1,190 linear
  block equations, all 85 degrees, and all ten selected-zero pair values;
- that hostile control fails 2,416 of 3,570 off-diagonal quadratic equations,
  so it is not an SRG completion;
- 45-second binary-linear searches for orbits 0 and 4 produced no primal and
  are recorded only as inconclusive.

No target automorphism is assumed.  Reproduce the sealed result with:

```powershell
.venv\Scripts\python.exe -B attempts\wave211-rank3-outside-block-proof-b\exact_check.py --verify
.venv\Scripts\python.exe -B -m unittest discover -s attempts\wave211-rank3-outside-block-proof-b -p test_exact_check.py -v
```

`--generate` reruns the orbit-29 MILP discovery and replaces the hostile
control; ordinary verification uses only the committed explicit edge list and
does not trust a solver status.

Claim label: `DERIVED`.  Global Conway-99 status: `UNKNOWN`.
