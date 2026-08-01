# Wave 207 M7g incidence bridge: frozen protocol

## Scope

Work conditionally over `F_3` at the putative prism-free rank-11 endpoint.
The input is a hypothetical weight-eight word

```text
a in im(B^T),
a=(1,1,1,1,2,2,2,2) on its support,
sum_i a_i z_i=0,
sum_i a_i z_i tensor z_i=0,
```

whose eight projective support columns form the `M_7g` orbit.  The four
positive and four negative points are paired on four concurrent external
secants, with no three secants coplanar.  The restricted polar form has one
of the four zero graphs `K8`, `2K4`, `4K2`, or `2C4`.

The task is to pull this support through eight actual triangle blocks and
the point--triangle incidence map.  No automorphism is assumed.

## Accepted input identities

1. `B` is the `99 x 231` point--triangle incidence matrix of a hypothetical
   `srg(99,14,1,2)`; every point is on seven triangle blocks and every graph
   edge lies in its unique graph triangle.
2. `G=BB^T=A+I`, `G^2=G-J`, and `AG=2J` over `F_3`.
3. At the prism-free endpoint, two disjoint triangle blocks have at most two
   cross edges.  Their centered product is that cross-edge count; two
   distinct intersecting blocks have centered product one.
4. The eight-column `M_7g` normal form and its three-dimensional space of
   polar restrictions may be reconstructed directly, but no result is to be
   promoted from an existing Wave 207 discovery package.

## Questions and proof gates

1. Derive every consequence of `a=B^T c` that is visible on the selected
   triangle union, especially for `b=Ba`.
2. Classify which pairs of selected triangles may intersect.  Retain the
   ambiguity that a polar product one can mean either intersection or one
   cross edge; products zero and two force disjointness.
3. Test whether the four polar types survive the exact local conditions
   `Ab=0`, `lambda<=1`, `mu<=2`, unique selected-triangle edges, and the
   prescribed pairwise cross-edge counts.
4. Any finite case analysis must state all restrictions.  A SAT local model
   is only a local compatibility certificate.  An UNSAT solver exit is not a
   proof without an independently checkable complete certificate or analytic
   derivation.
5. Internal weight-four and weight-five relations may be used as true
   centered-column relations, but they must not be assumed to lie in
   `im(B^T)`.

## Status wall

Unless an exact contradiction is independently established for every local
and global possibility, retain:

```text
weight-eight exclusion: UNKNOWN
rank-11 endpoint:        UNKNOWN
Conway-99:               UNKNOWN
```

