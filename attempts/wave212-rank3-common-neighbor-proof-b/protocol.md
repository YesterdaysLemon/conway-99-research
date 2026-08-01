# Protocol

## Frozen scope

Use only the three labelled `F` multisets in the Wave 210 hostile controls.
No automorphism of a target 85- or 99-vertex graph is assumed.  Vertex labels
`0..84` in this package are the upstream outside-column labels.

## Permitted reduction

Derive consequences of

```text
FD       = 2J-(A_S+I)F,
D^2 + D = 12I+2J-F^T F,
D1       = 14*1-F^T1,
```

using common-neighbor counts, triangle blocks, four-cycle incidence, and the
local `7K2` neighborhood condition.  Small labelled incidence feasibility is
allowed, but no search over complete unknown 85-vertex graphs is in scope.

## Certificate wall

`hostile-incidence-controls.json` is a restricted certificate.  Exact replay
must check every listed coloured edge and triangle, every degree, every
selected pair, the 104 zero-target pairs, every `FD` residual, and every
quadratic residual.  A solver exit status is not evidence.  Nonzero residuals
must remain visible and prevent construction language.

## Promotion rule

The package may be labelled only `DERIVED` until an independent verifier
reconstructs the identities and replays the labelled certificates.  Nothing
here changes the global status from `UNKNOWN`.
