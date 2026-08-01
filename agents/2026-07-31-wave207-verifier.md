# Wave 207 fresh verifier report

```yaml
role: verifier
date_utc: 2026-08-01T01:58:54Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Source-blind hostile audit of Wave 207 incidence--tensor rigidity,
  M7g geometry and finite enumerations, mixed-center Gram algebra,
  point-code/polar supplements, ternary distance and weight-fourteen
  composition reductions, and the restricted local incidence certificate.
inputs:
  - verification/wave207-incidence-tensor-rigidity/audited-inputs.sha256: de0c57f64a3bcd2af975e4d733c6dcbb89c8166e5bb7107325a4288825f9e17d
method: >-
  Freeze before discovery inspection; verify manifests; inspect the primary
  geometric source; replay every submitted suite; and independently
  recompute all finite-field, projective, polar, Gram-radical, signed-moment,
  Farkas, and local-certificate claims without importing discovery code.
command: >-
  .\.venv\Scripts\python.exe -B -m unittest -v
  verification\wave207-incidence-tensor-rigidity\test_independent_check.py
outputs:
  - verification/wave207-incidence-tensor-rigidity/run-report.yaml: dee423472dbbcf0cee8cc48c76cd1d63019b91f1eab95889e5faa8a92f7a25ec
  - verification/wave207-incidence-tensor-rigidity/audit.md: 2234c7b6029f0b5f41cac6c93f4208b489e7fc27628dc7dc2b518bd75b718ae4
  - verification/wave207-incidence-tensor-rigidity/independent-results.json: da5d43852a33efda699af210ea13f871c31ca83f3b933a2972a6e79f1fe2250a
limitations: >-
  All endpoint conclusions remain conditional; 23 polar forms and the
  balanced weight-fourteen branch remain; no graph completion, endpoint
  exclusion, counterexample, Q>=7060 proof, strict n3 improvement, or
  Conway-99 resolution follows.
```

## Verdict

The five frozen core claims are verified at their stated scope:

- every incidence word `a in im(B^T)`, hence every `a in A_Delta`, satisfies
  `Da=Za=0` under the rank-eleven nondegenerate factorization;
- a hypothetical weight-eight word has four coefficients of each sign and
  its support is the unique Kaipa--Pradhan M7g projective orbit;
- the canonical relation enumerator is
  `1+24y^4+16y^5+32y^6+8y^8`, and the 27 polar restrictions have zero graphs
  `K8,2K4,4K2,2C4` with affine multiplicities `1,12,8,6`;
- the Gram-radical short exact sequence and transition rank
  `binom(rank(C)+1,2)` are correct, and every true projector relation is
  annihilated by all fixed linear sandwich/mixed-trace features; and
- none of these results proves or excludes the endpoint.

The supplements also verify:

- the point image `b=Ba` is nonzero, lies in `ker_F3(A)`, has `b^Tb=2`, and
  initially has weight in `{2,5,8,11,14,17,20,23}`;
- exactly four of the 27 polar forms are immediately impossible: the
  rank-zero form and three rank-two forms with no product-one pair;
- `d(ker_F3 A)>=12`, narrowing the point image to `{14,17,20,23}`; and
- any weight-fourteen kernel word, if it exists, has sign composition `7+7`.

The restricted rank-four candidate really is a `23`-vertex, `51`-edge local
compatibility model with the archived pair data, local induced adjacency
equations, norm two, `lambda/mu` caps, and no induced triangular prism.  It
does not check the 76 outside coordinates of the global equation or any
99-vertex completion.

## Findings requiring careful wording

1. M7g is the unique projective orbit/closure, but the labelled canonical
   eight-set has four valid concurrent-secant decompositions.  Do not state
   uniqueness of the internal pairing.
2. The local certificate's `Ab_zero` field means the 23 induced-coordinate
   equations only.
3. The frozen M7g `failed-routes.md` says 91 graph vertices are omitted; the
   correct number is `99-23=76`.  This is a documentation error only.

## Validation

```text
source-blind protocol hash: verified
five discovery manifests:  8/8, 9/9, 11/11, 11/11, 11/11 entries
discovery unit tests:       3+5+10+5+8 = 31 passed
clean-room verifier tests:  13/13 passed
clean-room archive replay:  passed
AST/JSON/YAML and diff QA:  passed
global status:              UNKNOWN
```
