# Wave 210 proof B: rank-four point--line coupling

```yaml
role: proof_b
date_utc: 2026-08-01T04:09:47Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: >-
  Conditional exclusion of all seven Wave209 rank-four survivor orbits and
  their 51 labelled branches through exact typed point--line incidence
  equations; no rank-three or global promotion.
inputs: attempts/wave210-rank4-point-line-coupling-proof-b/input-freeze.sha256
method: >-
  Clean reconstruction of the rank-four branch cover, exact enumeration of
  three-point decompositions for every residual triangle type, global point
  incidence and incident-t demand coupling, sparse integer Farkas replay, and
  explicit transport under checked sign-preserving constraint relabelings.
command: >-
  .\.venv\Scripts\python.exe -B
  attempts\wave210-rank4-point-line-coupling-proof-b\coupling_check.py
  --verify ; .\.venv\Scripts\python.exe -B -m unittest -v
  attempts\wave210-rank4-point-line-coupling-proof-b\test_coupling_check.py
outputs: attempts/wave210-rank4-point-line-coupling-proof-b/package-manifest.sha256
limitations:
  - Conditional on the frozen endpoint and independently verified Wave208/209 rank-four reduction.
  - Proof-agent result is DERIVED pending a fresh verifier.
  - The rank-three branch and Conway-99 remain UNKNOWN.
```

## Result

The M7g forms, 83 marked subsets per form, 249 labelled branches, and 24
constraint-relabeling orbits were reconstructed without importing the Wave209
discovery module.  Independent replay of the pinned point-census archive
recovered exactly the seven survivor orbit ids

```text
0, 2, 4, 11, 12, 14, 23
```

with orbit sizes `6,12,6,6,12,3,6`, totalling 51 labelled branches.

For every residual triangle `(d,h,t)`, the checker enumerates its exact three
point signatures.  A selected intersection coordinate contributes
`(-1,+1,+1)`; a disjoint coordinate contributes `d_i` copies of `+1`; and the
negative memberships are grouped by the matching `H[h]` into at most three
points.  Each point-signature count is then coupled to residual triangles by

```text
residual incidences = (7-|M|) times the point count,
residual t sum      = (3q+3 sum_(i in M) alpha_i) times the point count.
```

These equalities are necessary consequences of seven triangles through every
point and `Bt=3q`.  The system also retains all 223 residual triangle counts,
the selected-line point incidences, all verified point/polar marginals, and
the exact residual sum and norm rows.

Seven archived integer Farkas vectors prove `A^Ty>=0` on every admissible
point and local-triangle column while giving the respective negative right
sides

```text
-4, -239020, -18, -18, -239020, -3240, -4.
```

The constraint transports were replayed over every labelled target.  No graph
automorphism was assumed.  The default path uses only standard-library exact
integer arithmetic; SciPy/HiGHS is confined to optional candidate generation,
and solver status is not promoted.

The coarser relaxation on the 35 unordered point-`q` triples still has an
explicit integer control in every survivor orbit after fixing the selected
types and residual `|t|<=2`.  Those controls are retained as evidence that
scalar value marginals alone do not give the exclusion.

## Status wall

The 51 rank-four branches are `DERIVED`-excluded by this proof agent.  They are
not `VERIFIED` until a fresh verifier independently reconstructs and attacks
the sealed certificates.  The rank-three branch is untouched; Conway-99
remains `UNKNOWN`.
