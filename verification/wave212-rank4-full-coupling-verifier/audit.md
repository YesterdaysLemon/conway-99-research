# Wave 212 independent audit: rank-four full point-line coupling

## Verdict

`PASS_NO_VETO` for the conditional Wave210 rank-four exclusion.  The seven
Wave209 survivor orbits and all 51 labelled branches are promoted from the
proof agent's `DERIVED` status to `VERIFIED` as exact necessary-condition
exclusions.

This does **not** exclude the rank-three survivor, produce a graph or
counterexample, or resolve Conway-99.  Rank three and the global target remain
`UNKNOWN`.

## Separation and blind reconstruction

The verifier reconstructed the M7g forms, all `3*83=249` marked branches, the
24 constraint-relabeling orbits, and the seven survivor ids

```text
0, 2, 4, 11, 12, 14, 23
```

from the sealed Wave209 verifier inputs.  Before opening a Wave210 artifact it
enumerated all 2,187 integral point signatures, 513--537 residual types per
representative, every coordinatewise unordered three-signature decomposition,
and the full `99+279+2*2187=4752` row universe.  The seven larger systems have
19,348--20,524 W/X columns.  Their complete row and column streams were
canonical-hashed.

Seven independently generated integer Farkas vectors replay exactly on every
column of those larger systems.  Their minimum column values and right-hand
sides are

```text
orbit:  0       2       4        11       12      14       23
min:    1       1       3         6        1       6        1
rhs: -678    -678   -6735     -6746     -678   -5113     -678
```

The blind seal pins the reconstruction code, complete-system hashes, and
176-kilobyte sparse integer dual archive.  `source-contact-log.md` records a
dimension-only scope message received after the complete matrices and hashes
were generated but before the dual archive was written.  No Wave210 matrix,
column, coefficient, mapping, or certificate entry was inspected before the
seal; the narrower source universe was audited separately after sealing.

## Exact geometric membership filter

For a point signature `s`, let `M(s)={i:s_i=-1}`.  The selected-triangle
intersection data force

```text
M(s) = empty, {i}, or {i,j} with ij in H.
```

Every accepted `H` is triangle-free.  For a residual triangle with selected
intersection set `h`, the induced graph `H[h]` is a matching.  Endpoints of an
edge of this matching are the same intersection point and therefore must
receive their `-1` entries in the same member of the unordered point triple.
The remaining vertices of `h` are singleton intersection groups.  This
independently recovers the source's exact local columns, not merely a
coordinatewise relaxation.

The seven filtered systems have the following dimensions:

```text
orbit       0      2      4     11     12     14     23
points    444    576    532    532    488    510    444
rows     1266   1530   1442   1442   1354   1398   1266
W cols  12110  11444  11672  11672  11888  12003  12110
```

For each representative, the verifier normalized the source matrix by
semantic row and column descriptors.  Every right-hand side, W column, X
column, and integer entry matched the independent reconstruction exactly.
The normalized complete-matrix hashes are archived in
`post-source-results.json`.

## Why the larger blind system is relevant

The post-seal verifier mechanically checked that every filtered row appears in
the larger blind system with the same right-hand side, every omitted coupling
row has right-hand side zero, and every filtered W/X column is literally a
column of the larger system after row-name embedding.  Hence any feasible
filtered vector would extend by zero to a feasible vector of the larger
system.  The blind contradiction is therefore a valid independent stronger
cross-check, not a comparison of unrelated dimensions.

## Archived dual replay and transport

All seven archived Wave210 vectors were decoded as sparse integer row maps and
replayed against the independently built filtered columns.  In orientation

```text
A^T y >= 0,        b^T y < 0,
```

both W- and X-column minima are zero, while the exact right-hand sides are

```text
-4, -239020, -18, -18, -239020, -3240, -4.
```

The verifier then enumerated the checked sign-preserving data relabellings
from each representative to every labelled orbit member.  It proved exact
point-signature, residual-type, and local-decomposition bijections; checked
row targets and every aggregate/point/coupling feature under transport; and
transported every coefficient map without collision.  This gives 51 exact
dual replays and 601,377 local-pattern checks.  No automorphism of a
hypothetical target graph is assumed.

## Hostile controls

The audit rejects all of the following:

* erasing a dual;
* reversing all dual coefficients and the required inequality orientation;
* changing an exact right-hand side;
* changing a sparse column entry; and
* using a coordinate map that breaks the four-positive/four-negative marked
  sign partition.

The RHS and column mutations are detected by complete canonical hashes, not by
sampling.  Solver exit status is absent from the proof path.

## Execution note

One accidental duplicate post-source process and one slower pre-optimization
process were terminated after their exact command lines and process ids were
checked.  They produced no accepted output and are not evidence.  A single
optimized fail-closed replay subsequently completed and wrote
`post-source-results.json`; the bounded archive and manifest test suite then
passed `5/5`.

## Exact boundary

The verified theorem is conditional on the frozen endpoint and the verified
Wave208/209 rank-four reduction.  It removes the rank-four case only.  The
rank-three case, unrestricted endpoint exclusion, construction of an
`srg(99,14,1,2)`, and the global Conway-99 target remain `UNKNOWN`.
