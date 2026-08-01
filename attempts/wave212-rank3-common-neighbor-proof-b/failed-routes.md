# Failed and nonclosing routes

## Global triangle and four-cycle totals

The forced totals `64+456`, 152 outside triangles, and 2079 four-cycles all
have the required divisibility.  Their exact support-count refinement also
closes without contradiction.

## Treating support colours independently as an obstruction

This fails structurally: an outside edge with support intersection one has a
unique colour.  Matchings for distinct support points therefore use disjoint
candidate edge sets.  The committed labelled unions show simultaneous
compatibility in all three orbits.

## Triangle packing as a graph completion

A linear 152-block packing supplies designated local pairs but does not forbid
additional graph triangles assembled from edges of different blocks.  The
three controls have 123--154 such spurious triangles and must not be called
`7K2` neighborhoods or SRG candidates.

## Target-zero constraints alone

Forbidding common neighbors across all 40 `q=2` pairs and all 64 coloured
edges is feasible in every orbit.  It leaves 2271--2314 quadratic pair
failures and hundreds of `FD` failures.

## Solver interpretation

The incidence controls were discovered in a bounded labelled triple
relaxation.  Only their complete committed lists and exact replay are
evidence.  A solver success, timeout, or non-hit is not a proof, and no search
over complete unknown 85-vertex graphs was performed.
