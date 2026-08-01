# Wave 208 proof B: marked M7g spectral divisibility

```yaml
role: proof_b
date_utc: 2026-08-01T02:32:04Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: >-
  Conditional marked-M7g branch: derive a global spectral divisibility
  obstruction, reduce 23 polar survivors to four, classify the exact marked
  intersection residual, and retain local positive controls.
inputs: attempts/wave208-marked-m7g-proof-b/input-freeze.sha256
method: >-
  Integer incidence lift, exact SRG spectral polynomial, coordinatewise
  ternary divisibility, 27-form symbolic census, complete labelled
  intersection-subset replay, and solver-independent local certificates.
command: >-
  .\.venv\Scripts\python.exe -B
  attempts\wave208-marked-m7g-proof-b\exact_check.py --verify
outputs: attempts/wave208-marked-m7g-proof-b/package-manifest.sha256
limitations:
  - Discovery status is DERIVED pending source-blind verification.
  - Four polar forms and thousands of labelled marked subsets remain.
  - Local controls are not graph completions.
  - Rank 11, the endpoint, and Conway-99 remain UNKNOWN.
```

## Headline theorem

Let `a` be the integer `4+4` lift of a hypothetical tensor-balanced `M7g`
word, put `b~=Ba`, and let

```text
S_D=sum_(i<j) d_ij a_i a_j
```

for the integer restricted polar entries.  The actual selected-intersection
sum cancels from the real spectral deficit, giving

```text
r=(A-3I)b~,
Ar=-4r,
||r||^2=7(24-2S_D).
```

All 99 equations `Ab=0` modulo three make `r` coordinatewise divisible by
three, so its norm is divisible by nine.  Exact reconstruction gives

```text
S_D distribution: -24^3, -12^4, 0^19, 12^1.
```

Only `S_D=-24` and `12` satisfy the divisibility.  Thus 19 of the 23 Wave
207 survivors are removed, leaving three rank-four forms with an integer
minus-four eigenvector of squared norm 56 and one rank-three form satisfying
the exact integer equation `A b~=3b~`.

## Residual boundary

The rank-four product-one graph is `2C4`; complete labelled replay leaves 83
intersection subsets per form.  The rank-three product-one graph is
`K_(4,4)` minus a perfect matching; its point image has either two
intersections and weight 20 or five intersections and balanced weight 14.

Exact 22- and 19-vertex controls realize those two rank-three branches while
satisfying the induced exact eigenvector equation, selected-pair cross
counts, `lambda/mu` caps, and prism-freeness.  They omit the outside graph,
so the global status remains `UNKNOWN`.
