# Wave 210 proof A: rank-three marked/outside coupling

```yaml
role: proof_a
date_utc: 2026-08-01T03:53:37Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: complete labelled selected-union coupling for the weight-14 Ac=3c branch
inputs:
  - attempts/wave209-rank3-trade-proof-a/package-manifest.sha256 sha256 521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
  - verification/wave209-four-survivor-verifier/package-manifest.sha256 sha256 7e20ac726cc4823360e49d3fcf08e5c8ff6c7f219c5d1cbbba781d015fe59c91
method: exact 85-column reconstruction, complete labelled small censuses, and proved orbit caching
command: .venv\Scripts\python.exe -B attempts\wave210-rank3-marked-outside-coupling-proof-a\exact_check.py --verify
outputs:
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/exact-results.json sha256 f4b40b0d6e0ab45a2389c218abeba9e473658351090607fbd86faf0a9089e09c
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json sha256 32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd
limitations: no D block, no 99-vertex graph, no exclusion; global status UNKNOWN
```

## Result

The exact support/outside incidence matrix has 17 empty columns, 61 columns
of type `(1,1)`, and seven columns of type `(2,2)`.  All 4,480 retained
deficit-edge bijections satisfy the full `F F^T` block identity and have
rank 13.

The 204 labelled marked graphs expand to 20,928 ordered support-block
packings.  Containment alone leaves every one of the 232 distinct requirement
patterns.  After all 28 selected-line polar counts, mandatory triangle edges,
exact column multiplicities, and induced common-neighbor caps are imposed,
only three of 33 proved case orbits remain.  Label expansion leaves 1,536
`H`/packing cases and 55,296 of 93,757,440 `H`/packing/deficit branches.

Exactly 96 labelled marked graphs survive: all 36 cases of each asymmetric
degree orientation, 24 of the 120 `(2,2,1,0)`/`(2,2,1,0)` cases, and none of
the 12 `(3,1,1,0)`/`(3,1,1,0)` cases.  Every surviving marked graph has 16
ordered support packings.

The local 1-factor condition was reconstructed independently.  All 4,480
exact `F` configurations admit a perfect matching in each of the 14 support
zero-neighborhoods; the matching is highly nonunique.  Every selected-union
survivor extends those local matchings, so this test gives no additional cut.

Three explicit orbit-representative hostile controls are sealed.  They are
19-point partial controls with complete 85-column `F` data, not global graph
constructions.  The unknown 85-by-85 outside adjacency block remains the
exact boundary, and Conway-99 stays `UNKNOWN`.

