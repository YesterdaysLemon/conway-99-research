# Wave 210 proof-B protocol: rank-four point--line coupling

## Frozen scope

Assume the hypothetical prism-free rank-11 endpoint and import only the
manifest-pinned, independently verified Wave 209 rank-four reduction.  The
input consists of the seven constraint-relabeling orbits, containing 51
labelled branches, which survived the anonymous 99-point signature census.
The source and verifier manifests, the Wave 209 protocol, and `AGENTS.md` are
pinned in `input-freeze.sha256`.

## Exact target

Couple the anonymous point and residual-triangle censuses without searching
for a 99-vertex graph.  Every retained constraint must be necessary for an
actual endpoint:

1. each residual triangle has three point signatures whose coordinate
   multisets realize its exact `(d,h,t)` type;
2. each point lies on seven triangles;
3. the incident triangle sums at a point add to `3q`;
4. intersections with the selected union are grouped at no more than three
   points, with `H[h]` a matching; and
5. all imported point and triangle marginal equations retain their exact
   integer right-hand sides.

The proof object for an exclusion is an integer Farkas vector checked on every
allowed point column and every allowed local triangle column.  A numerical LP
status or floating dual ray is not evidence.

## Required controls and status wall

Retain an explicit integer positive control for the coarser 35 unordered
triangle-`q`-type relaxation, including the selected triangle types and the
residual `|t|<=2` restriction.  This documents why separate value marginals do
not suffice.

This lane may report `DERIVED` or `CANDIDATE` only.  It must not promote its
own certificates to `VERIFIED`.  It does not touch the rank-three branch, and
Conway-99 remains `UNKNOWN` unless an independently verified integration
closes every branch.
