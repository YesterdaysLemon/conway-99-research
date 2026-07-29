# Wave 206 literature and hostile-controls report

```yaml
role: construction
date_utc: 2026-07-29T21:35:14Z
git_commit: 85e705cc6c2a14d123120c93a847e30aaab1789e
claim_label: CANDIDATE
scope: construction/literature/hostile controls, not the Wave 206 verifier
inputs: attempts/wave206-three-center-hostile-controls/input-freeze.sha256
method: exact F_3 reconstruction, mutation tests, and primary-source hypothesis audit
command: python -B attempts\wave206-three-center-hostile-controls\exact_check.py --verify-results attempts\wave206-three-center-hostile-controls\exact-results.json; python -m pytest -q attempts\wave206-three-center-hostile-controls
outputs: attempts/wave206-three-center-hostile-controls/
limitations: relaxed controls only; all target-premise failures listed below and in exact-results.json
```

## Result

The package constructs two exact realizations on the same complete labeled
`99 by 231` linear triple incidence. In both:

- every point star is an exact seven-vector singular simplex for a rank-six
  self-adjoint projector;
- the 231 block vectors span dimension 11;
- the centered Gram has rank 11 and square zero;
- `sum_x P_x=0`; and
- the global column frame is zero.

The checker constructs and compares both complete labeled `99 by 99` matrices,
not merely component summaries:

```text
g_A == g_B
H_A == H_B.
```

Nevertheless, `tau_A` and `tau_B` differ on 209,952 ordered triples. The
difference support consists exactly of triples with one center in each of the
three incidence components.

Claim: the explicitly checked relaxed premise package determines `tau` is
`REFUTED`.

This is not a target counterexample. The incidence point graph has connected
component sizes `27,36,36`, nonuniform edge and nonedge common-neighbor
counts, 1,098 extra graph triangles, and only 19 projective block directions.
Every separated triple is cross-component. Projective distinctness,
`lambda=1`, `mu=2`, endpoint graph types, prism/crossing restrictions,
`t_xy`, code distance, cover, and `Q` premises are missing.

## Fixed-y rank result

For fixed `y`,

```text
tau_y[x,z]=tr((P_y P_x P_y)(P_y P_z P_y))
```

is the trace Gram of self-adjoint operators on the six-space `E_y`, hence has
rank at most 21. Two exact 99-projector zero-sum controls attain rank 21. Their
diagonal distributions are respectively

```text
(0:30,1:33,2:36)
(0:33,1:15,2:51),
```

and their full entry distributions also differ.

Claim: sharpness of the projector-level bound is `DERIVED`.

The controls repeat 33 projector types three times and have no coupled
231-column incidence. A stronger shared-incidence rank-21 control was not
found in the bounded 34-type pool and component ansatz. That nonhit is
`UNKNOWN`, not evidence of nonexistence.

## Literature boundary

The primary-source audit found no theorem whose hypotheses match the frozen
ternary projector tensor:

- finite-field frame theory supplies the square-zero Gram identity, not
  triple projector moments;
- real tight fusion-frame and cubature theorems require positivity and proved
  polynomial exactness;
- complex Grassmannian association-scheme theorems require design,
  angle-class, and annihilator hypotheses;
- cited triple-regularity consequences require stronger design or dual
  conditions; and
- Terwilliger modules require the actual adjacency and basepoint
  subconstituents, not only an SRG parameter tuple.

This is a bounded literature non-discovery with label `UNKNOWN`.

## Boundary and next invariant

The construction shows that complete pair data plus the zero-frame
contraction do not determine `tau` at the checked relaxed
shared-incidence level. The next invariant must couple the family of
fixed-center Gram slices `{tau_y}` through actual graph types, or impose an
equivalent four-center/Terwilliger-localizer constraint.

```text
Conway-99:               UNKNOWN
rank-11 endpoint:        UNKNOWN
n3=4158 endpoint:        UNKNOWN
actual nonedge h:        UNKNOWN
Q>=7060:                 NOT PROVED
automorphism assumption: NONE
```
