# Wave 210 proof-A protocol: marked/outside coupling

## Frozen conditional input

Assume only the sealed Wave 209 rank-three weight-14 branch: a hypothetical
`srg(99,14,1,2)` has an integer vector `c` with `Ac=3c`, seven `+1`
coordinates, seven `-1` coordinates, and 85 zero coordinates.  The signed
support graph is the unique rooted seven-point type on each sign, joined by
one root cross edge.  The marked eight-line system has five labelled
opposite-sign intersections and is one of the 204 Wave 209 cases.

`input-freeze.sha256` pins `AGENTS.md`, the Wave 209 globalization protocol,
the sealed Wave 209 discovery manifest, and its sealed verifier manifest.
The verifier's later `352 -> 346` weight-20 narrowing is recorded but is not
used: this lane is restricted to weight 14.

## Exact scope

1. Reconstruct all 204 labelled five-edge marked graphs.
2. Reconstruct every ordered support-block packing on both sign sides.
3. Reconstruct all 4,480 capacity-compatible bijections of the two seven-edge
   common-neighbor deficit graphs and the resulting exact 85 support-column
   multiset.
4. Assign each of the five marked zero points to a distinct column copy that
   contains both incident selected-line support blocks.
5. Impose all 28 selected-line polar cross counts, all mandatory triangle
   edges, the induced `lambda<=1` and `mu<=2` caps, and exact column
   multiplicities.
6. Independently test the local one-factor condition in the zero-neighborhood
   of each of the 14 support points.

## Allowed cache and restrictions

No target automorphism is assumed.  Caching is allowed only after the checker
explicitly generates all labelled cases and partitions them under:

- the complete order-48 symmetry group of the frozen labelled polar matrix;
- the independently enumerated order-4 automorphism group of each fixed
  rooted seven-point support graph.

The checker proves closure of all 4,480 deficit bijections under those
relabelings.  A selected-union survivor is only a necessary local control.
There is no 99-vertex graph search, no outside-block `D` search, and no
promotion to `VERIFIED` by this discovery agent.

