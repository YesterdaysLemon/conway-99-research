# Wave 212 rank-three verifier preinspection protocol

Frozen before reading either Wave 212 discovery package.

## Inputs and independence boundary

Only the frozen Wave 210 hostile controls and Wave 211 outside-block equations
may be read before this memo is sealed.  The verifier will then inspect both
Wave 212 packages, replay their manifests/checkers/controls, compare exact
outputs with the expectations below, and apply at least one hostile mutation
to each lane.  It will not enumerate unknown graphs or repair discovery code.

For each orbit `0,4,29`, reconstruct `F`, the fixed support adjacency `A_S`,
and the necessary equations

```text
F D       = 2J - (A_S+I)F,
D 1       = 14 1 - F^T 1,
D^2 + D   = 12I + 2J - F^T F.
```

## Frozen expected invariants

- `rank_Q(F)=rank_F2(F)=13`; adjoining the all-one row gives rank `14`.
- The 85 column sizes are `0^17,2^61,4^7`, hence the outside degree
  multiset is `14^17,12^61,10^7` and there are `520` outside edges.
- For outside pairs, `q_ij=<F_i,F_j>` has distribution
  `q=0:2878, q=1:652, q=2:40`.
- The trace of the linear block against `F^T` forces
  `sum_{D_ij=1} q_ij=64`.  Nonnegative common-neighbor targets force no
  `q=2` edge, so an exact completion has `q=0:456, q=1:64, q=2:0` edges.
- Thus `|N_D(i) intersect N_D(j)|=2-q_ij-D_ij` has target histogram
  `0:104, 1:1044, 2:2422`.  Edge/common-neighbor double counting gives
  exactly `152` all-outside triangles.  Opposite-pair double counting gives
  exactly `1211` all-outside four-cycles.
- Over `F_2`, `Q=F^T F` has power ranks `12,8,4,2,0`, hence Jordan type
  `J_5^2 + J_3^2 + J_1^69`.  The forced action on
  `U=im(F^T)+<1>` has power ranks `8,4,2,0`, hence
  `J_4^2 + J_2^2 + J_1^2` and is nilpotent.  Conditional on the full
  quadratic block, `D` has Jordan type
  `J_5(0)^2 + J_3(0)^2 + J_1(0)^29 + J_1(1)^40`, so
  `rank(D^k)=52,48,44,42,40` for `k=1..5` and
  `rank((D+I)^k)=45` for every positive `k`.
- Over `Q`, with any full-row-rank matrix `R` spanning
  `U`, define `P_U=R^T(RR^T)^-1R` and `P_K=I-P_U`.
  Check exact symmetry/idempotence, `tr(P_K)=rank(P_K)=71`,
  `FP_K=0`, and `1^T P_K=0`.  The forced map `L=DP_U` is computed from
  `DF^T=(FD)^T` and `D1`; it must be symmetric with trace `4`.
  Conditional spectral projectors are
  `E_3=(-L+4P_K+D)/7` and `E_-4=(L+3P_K-D)/7`; their forced diagonal
  sums are `40` and `31`, respectively, and every forced diagonal entry
  must lie in `[0,1]`.

## Verdict rules

A lane receives `PASS / NO VETO` only for exact claims reproduced without
scope inflation.  A control satisfying aggregates, selected pairs, or all
104 zero-target rows is not a completion unless all 1,190 entries of `FD`,
all degrees, and all 3,570 off-diagonal quadratic rows pass.  Timeout and
non-hit data are never infeasibility evidence.  The global status remains
`UNKNOWN` unless a complete independently checked proof or graph certificate
is supplied.
