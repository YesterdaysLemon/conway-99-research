# Wave 207 proof C: ternary adjacency-code bridge

```yaml
role: proof_a
date_utc: 2026-08-01T01:39:53Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: conditional ternary adjacency-code bridge and parameter-only distance floor
inputs:
  - CONJECTURE.md: 7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58
  - attempts/wave176-star-projector-circuits/derivation.md: b5ba53c9d93d3c8169f7d7bbf179c3d355b01df36f3feb9fec797c7274a568c8
  - attempts/wave206-crossing-kernel-proof-b/derivation.md: 9bdc0a296f704a5bd73ffa3a726694b74454b011dac486da9afa599f868aab13
  - attempts/wave206-tensor-balance-weight-proof-b/derivation.md: 7d13a1834819e952c4d4eff033fac033e23699ab643d9852318a67d19bcb6cf2
method: signed neighbor moments plus an exact weight-eleven Farkas certificate
command: .\.venv\Scripts\python.exe -B -m unittest -v attempts/wave207-ternary-adjacency-code-bridge/test_exact_check.py
outputs:
  - attempts/wave207-ternary-adjacency-code-bridge/derivation.md: 27860e2f8b5ce23c37a43a1ef53fb31d7eda1ee67926e04406ccbf0d938e40b5
  - attempts/wave207-ternary-adjacency-code-bridge/exact-results.json: 94ed011861be9cf201ac5c531a704832cf8675c5b993c420e92a2e5812f8e7d8
  - attempts/wave207-ternary-adjacency-code-bridge/formal-control.json: 97ef89ff784dd1a42b0c4608bb22c7b6babe4b9b657872bf411e52f1c20c455e
limitations: d>=24, equality at 24, endpoint exclusion, and Conway-99 remain UNKNOWN
```

## Result

Let `a=B^T c` be a hypothetical weight-eight `A_Delta` word with four
coefficients of each nonzero ternary value, and put `b=Ba`.  The incidence
identities give

```text
sum c=sum a=0,
b=(A+I)c=(A+I-J)c in ker_F3(A).
```

The image cannot vanish:

```text
c^T b=a^T a=8=2 in F_3.
```

Also `G=A+I` satisfies `G^2=G-J`, so

```text
b^T b=c^T(G-J)c=c^T Gc=2.
```

The union of eight triangle supports has size at most 24.  Hence

```text
b!=0,
wt(b)<=24,
wt(b)=2 mod 3.
```

The signed-neighbor argument in the derivation proves the new
parameter-only theorem

```text
d(ker_F3 A)>=12.
```

The only possible point-image weights are therefore

```text
wt(b) in {14,17,20,23}.
```

## Proof boundary

Weights at most nine are excluded by the pointwise inequality

```text
C(i,2)+C(j,2)+2ij-i-j>=0
```

summed against the SRG common-neighbor moments.  Weight ten collapses to a
balanced independent support and fails modulo three.  Weight eleven is
excluded by a separately recorded nonnegative Farkas function whose global
sum would be `-60`.

An exact weight-fourteen aggregate control survives all recorded first and
second moments and aggregate `7K_2` matching sums.  It is deliberately
nongraphical: the internal degree multiset in each sign class is
`[0,0,0,0,0,6,6]`.  It is not a graph and not a codeword, but it marks the
stopping point of this moment method.

## Validation

```text
exact unit tests: 10/10 passed
exact result replay: passed
Python bytecode compilation: passed
git diff --check on package: passed
Ruff: unavailable in .venv
```

The desired `d>=24`, classification of weight-24 words, exclusion of the
rank-eleven endpoint, and global construction/nonexistence result all remain
`UNKNOWN`.
