# Wave 212 rank-three symbolic audit

## Verdicts

### Proof B: common-neighbor/triangle/four-cycle lane

**PASS / NO VETO** for the submitted `DERIVED` scope.

Independent reconstruction gives the same 520-edge split
`q=0:456, q=1:64, q=2:0`, common-neighbor target histogram
`0:104, 1:1044, 2:2422`, 152 all-outside triangles, 1,211 all-outside
four-cycles, and 2,079 total four-cycles.  All three labelled incidence
controls replay exactly and their package manifest has exact file coverage.

The controls are deliberately restricted.  They satisfy all 85 degree rows,
all ten selected pair values, and all 104 zero-target common-neighbor rows,
but only `499/1190`, `534/1190`, and `532/1190` entries of `FD`, and only
`1256/3570`, `1259/3570`, and `1299/3570` quadratic pair rows.  They have
132, 154, and 123 additional graph triangles beyond the 152 designated
blocks.  None is an outside-block completion or an SRG construction.

### Proof A: mod-2 and projector lane

**PASS / NO VETO** for the exact `F^T F` power ranks/Jordan type, conditional
characteristic-polynomial compatibility, rational `K`-projector diagonals,
and all 3,570 two-by-two projector-minor tests in each orbit.  The submitted
manifest has exact file coverage and every exact distribution replays.

**VETO / REFUTED** specifically for the stated boundary that the four
nontrivial mod-2 Jordan blocks of `D` have an undetermined allocation between
the zero- and one-primary spaces.

The correction was not made silently.  It is recorded only as
**VERIFIER-DERIVED / PENDING INDEPENDENT PROMOTION**:

1. The frozen linear equations reconstruct `D|U` over `F_2` with power ranks
   `8,4,2,0`; hence the forced action on `U=im(F^T)+<1>` is nilpotent.
2. Put `Q=D^2+D=F^T F`.  On a nontrivial primary block
   `D=lambda I+T`, one has `Q=T(I+T)`.  Its image is `im(T)`, and the
   restriction of `D` to that nonzero image has primary root `lambda`.
3. Since `im(Q)` is contained in `im(F^T)`, it lies in `U`.  Nilpotence of
   `D|U` therefore forces `lambda=0` for every nontrivial block.
4. Together with `chi_D=x^45(x+1)^40`, the conditional Jordan type is
   `J5(0)^2 + J3(0)^2 + J1(0)^29 + J1(1)^40`, and the resulting power ranks
   are `rank(D^k)=52,48,44,42,40` for `k=1,...,5`.

This sharper allocation is a verifier discovery, so AGENTS.md prevents this
audit from promoting it to `VERIFIED` without another independent check.

## Replay and hostile tests

The verifier was source-blind through the preinspection seal, then replayed
both submitted `--verify` commands and all seven submitted unit tests.  Its
own standard-library checker independently reconstructed the incidence
residual histograms, mod-2 ranks, forced `U` action, exact rational projectors,
and pairwise PSD choices.  It also rejected an in-memory deleted coloured
edge in proof B and a deleted support-incidence entry in proof A.  No
discovery artifact was repaired or edited.

## Boundary

No `85 x 85` binary outside block is constructed or excluded.  No unknown
graph search or target-graph automorphism is used.  The three rank-three
orbits, rank-11 endpoint, and unrestricted Conway-99 target remain `UNKNOWN`.
