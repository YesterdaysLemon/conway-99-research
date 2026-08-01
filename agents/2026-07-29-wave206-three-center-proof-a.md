# Wave 206 proof A report

```yaml
role: proof_a
date_utc: 2026-07-29T21:45:42Z
git_commit: 85e705cc6c2a14d123120c93a847e30aaab1789e
claim_label: DERIVED
scope: conditional prism-free rank-11 three-center graph geometry
inputs: attempts/wave206-three-center-proof-a/input-freeze.sha256
method: exact derivation plus deterministic finite-field enumeration
command: .\.venv\Scripts\python.exe -B attempts\wave206-three-center-proof-a\exact_check.py --verify attempts\wave206-three-center-proof-a\exact-results.json
outputs: attempts/wave206-three-center-proof-a/
limitations: discovery only; shared 231-column completion and all t>=8 modules remain open
```

## Result

For each fixed root `y`, the matrix

```text
T_y[x,z]=tau_(xy;z)
```

is the trace Gram of 99 self-adjoint operators on a six-dimensional space.
It is symmetric, has rank at most 21, and has zero row sums.

The seven root-star blocks give a 21-coordinate model
`r_x^(y)[i,j]`.  The coordinate row determines the operator; its coordinate
sum is `t_xy` modulo three, its linear trace is `g_xy`, and one fixed
quadratic form is `h_xy`.  The 84 nonneighbors split exactly into 21 labelled
four-vertex fibers, one for each coordinate.

Every genuine weighted projector relation `sum_x c_x P_x=0`, including the
nonconstant relation independently established in the crossing-kernel lane,
projects to `sum_x c_x r_x^(y)=0` coordinatewise.  This is not an owner-only
fiber equation: edge centers and all non-owner fibers can contribute to the
same coordinate.

Prism-freeness forces every induced fiber graph to be a subgraph of the two
opposite-corner diagonals.  In the complete normalized low-`t` census,
`t=6` forces marked `r=1,h=1`; for `t=7`, marked `r=1` excludes `h=2`, while
marked `r=0` permits all three `h` values.

Complete edge-module enumeration found 67,950 labelled degree-two incidence
matrices and 130 distinct compressions.  Against each of the four sealed
fixed-pair controls, every relation to `y` and forced root-star placement
still permits all three values of `tau` at the marginal-module level.  Exact
97-entry scalar ledgers satisfy the contraction for all four controls, but
deliberately do not impose the prescribed `x,z` pair module or one shared
operator or column realization.  Thus the full labelled triple-type question
remains open.  Separate abstract operator controls show that rank 21 plus
zero row sums also do not determine `h`.

## Inflection

The scalar three-center route is now sharply localized.  The missing
invariant is the joint law of the four compression operators in each
nonneighbor fiber, coupled across all 21 fibers and the 14 edge centers by
one shared 231-column realization.  The nearer-term triple problem is to add
the missing `x,z` pair module.  These are simultaneous constraints, not
another independently selectable `tau` entry.

Endpoint status remains `UNKNOWN`.
