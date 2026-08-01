# Wave 207 construction/symbolic incidence report

```yaml
role: construction
date_utc: 2026-08-01T03:20:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: >-
  Conditional prism-free rank-11 endpoint: pull a hypothetical weight-eight
  M7g tensor word through a=B^Tc, classify the immediate polar-form
  exclusions, and test one restricted induced local incidence realization.
inputs: attempts/wave207-m7g-incidence-bridge/input-freeze.sha256
method: >-
  Exact F3 incidence-module algebra, a complete 27-form polar reconstruction,
  internal relation-code enumeration, and an independently checked 23-vertex
  induced local certificate. The discovery scout restricts selected
  intersections to pair-specific vertices; no graph completion is searched.
command: >-
  .\.venv\Scripts\python.exe -B
  attempts\wave207-m7g-incidence-bridge\exact_check.py --verify ;
  .\.venv\Scripts\python.exe -B -m unittest -v
  attempts\wave207-m7g-incidence-bridge\test_exact_check.py
outputs: attempts/wave207-m7g-incidence-bridge/package-manifest.sha256
limitations:
  - Exactly four of 27 polar restrictions are excluded; 23 remain.
  - The rank-four certificate is a 23-vertex induced necessary-condition model, not a 99-vertex SRG.
  - The scout assumes pair-specific selected intersections and a non-hit has no proof status.
  - No internal weight-four or weight-five circuit is assumed to lie in im(B^T).
  - Rank 11, the prism-free endpoint, Conway-99, and external novelty remain UNKNOWN.
```

## Result

If `a=B^Tc` is a hypothetical signed `4+4` weight-eight word and `b=Ba`,
then

```text
Ab=0,
b^Tb=a^Ta=2,
sum_(intersecting selected pairs) a_i a_j=1 in F_3.
```

An intersecting selected pair must have polar product one.  Reconstructing
all 27 forms therefore excludes the unique rank-zero `K8` form and the three
rank-two `2K4` forms with no product-one pair: exactly four forms.

The frozen rank-four `2C4` certificate has 23 vertices and 51 edges.  It
satisfies the exact selected-pair Gram/cross-edge table, `Ab=0`, local
`lambda<=1`, local `mu<=2`, degree at most eight, and contains no induced
triangular prism.  Its twelve weight-four and eight weight-five internal
circuits cross-realize no graph-vertex pair, so existing transversal
multiplicity bounds do not exclude it.

This is a sharp symbolic/local checkpoint, not a global proof or
counterexample.  The surviving obstruction must use outside completion or
the simultaneous 99-star/231-column system.

