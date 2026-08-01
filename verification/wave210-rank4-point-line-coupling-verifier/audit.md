# Wave 210 rank-four point/line coupling verification audit

## Verdict

`PENDING_VERIFICATION` / **promotion veto**.  I found no mathematical
counterexample to the source derivation, but this run did not independently
reconstruct and replay the source's full matrices and all seven Farkas
certificates.  Consequently the sealed `DERIVED` source package must not be
promoted to `VERIFIED` on this evidence.

The rank-three lane and the global Conway-99 target remain `UNKNOWN`.

## Separation record

Before opening any Wave 210 discovery file, I sealed:

* `protocol.md` and `input-freeze.sha256`;
* an independent standard-library implementation;
* deterministic row/right-hand-side and sparse-column hashes for the seven
  Wave 209 survivor representatives; and
* `blind-seal.sha256` at `2026-08-01T04:23:21Z`.

The blind reconstruction recovered survivor orbit ids
`0,2,4,11,12,14,23`, orbit sizes `6,12,6,6,12,3,6`, hence all 51 labelled
branches.  For each representative it decoded a 99-point census, checked all
eight `(-1,0,+1)=(3,60,36)` margins, `sum(q)=0`, `q.q=56`, decoded aggregate
types totalling 223 residual lines, and checked residual `sum(t)=0`,
`sum(t^2)=96`.  It reconstructed `H[h]` into matching-edge/singleton point
groups and checked the global identity

```text
sum_s (7-|M(s)|) X_s = 669 = 3*223.
```

It also independently derived the residual incident-`t` demand

```text
Delta(s)=3q_s+3 sum_(i in M(s)) alpha_i.
```

No target-graph automorphism was assumed.

## Necessary-equation audit

The following source equations have a valid direct derivation.

1. `M(s)` is empty, a singleton, or an edge of the selected-intersection
   graph `H`: three selected triangles through one point would form a triangle
   in `H`, while nonadjacent selected triangles are disjoint.
2. For a residual triangle of type `(d,h,t)`, a coordinate in `h` has point
   multiset `{-1,+1,+1}`.  A coordinate outside `h` has exactly `d_i` entries
   `+1`; `lambda=1` forbids two cross edges from the same residual point.
3. `H[h]` is a matching.  If intersecting selected triangles met the residual
   triangle at different points, an edge of that residual triangle would have
   two common neighbours.  Two edges of `H[h]` sharing a vertex would force
   the residual and selected triangles to share an edge.
4. The number of point groups is `|h|-|E(H[h])|<=3`.
5. Each point of signature `s` is incident with `7-|M(s)|` residual triangles,
   giving the degree coupling.  Subtracting its selected triangle values
   `-3 alpha_i` from `Bt=3q` gives the displayed `Delta(s)` equality.
6. With variables nonnegative, the claimed dual orientation is the correct
   one: `A^T y>=0` and `b^T y<0` contradict `Az=b`.

These checks support necessity of the construction, but they do not validate
the archived coefficient vectors by themselves.

## Precise independence gap

My blind implementation chose a weaker incidence transportation relaxation:
it fixed the archived nonzero point and residual-type controls and assigned
individual signature/line-role incidences.  After unsealing, the source was
found to do something materially stronger and different:

* it ranges over all 444--576 admissible signatures rather than only the
  40--49 signatures in one archived point control;
* it enumerates exact unordered triples of point signatures for every
  realizable residual type rather than separate point roles;
* it retains all 99 aggregate rows and 279 point-census rows, with two
  coupling rows per admissible signature; and
* it has 11,444--12,110 local columns per orbit, versus 315--460 columns in
  the blind relaxation.

Thus the blind matrix hashes are not hashes of the source matrices and cannot
authenticate the archived duals.  This is a verifier incompleteness finding,
not a refutation of the source claim.

## Source archive and bounded replay

The outer source manifest has the assigned SHA-256
`7eb45280b61e1612f4d70aa95922b7821e16aa3c426832eadb8995809d5cff78`.
All 12 paths in it were present and matched their recorded SHA-256 values.

A bounded command started the source default replay followed by its unittest
suite.  The combined command produced no captured result before the 64-second
tool limit; at timeout the unittest process was still running.  The two exact
processes were stopped and the generated `__pycache__` was removed.  A timeout
is neither a certificate failure nor a pass.  No hostile mutation result was
obtained in this verifier run.

## Required continuation

A fresh verifier should extend the sealed clean-room implementation to:

1. reconstruct all admissible signatures, all 507--531 realizable residual
   types, and all exact local triples without reading discovery code;
2. produce canonical hashes of the complete `99+279+2N` row universe and all
   `W`/`X` columns;
3. compare those complete objects with the source;
4. expand each sparse integer dual and directly compute every column score
   and `b^T y` for all seven representatives;
5. transport and recompute on all 51 labelled branches; and
6. run sign, coefficient, RHS, local-column, and branch-map mutations.

Until that succeeds, the correct verifier label is `UNKNOWN` and the source
package remains `DERIVED`.
