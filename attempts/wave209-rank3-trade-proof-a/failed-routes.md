# Failed or incomplete routes

## Point moments alone

The exact first and second outside moments leave five support-14 rows and
425 support-20 rows.  They are useful reductions, not nonexistence proofs.

## Support-14 local closure

The `lambda/mu` deficit calculation forces one seven-point support type and
one outside signature.  It still leaves 4,480 capacity-compatible pairings
of the seven positive and seven negative deficit edges and 204 labelled
selected-intersection graphs.  A capacity-compatible pairing is not an
outside graph.

## Selected-zero dynamic program

The support-20 dynamic program maximizes only the selected-pair counts that
the two intersection zeros can mediate.  It is a complete exact calculation
for that relaxation, but it does not impose outside degrees, outside-outside
common neighbors, or the remaining 223 line coordinates.  Its surviving
rows cannot be promoted to candidates.

## Line-graph eigenvector

The full line reformulation produces integral `7`-eigenvector norms and
point-sum equations, but every retained branch has nonnegative residual norm.
No dual inequality excluding those norms was found.

## Aggregate line types

Both branches admit nonnegative 231-line type censuses.  These counts ignore
which lines meet, so they do not realize the partial quadrangle.

## Local positive controls

The imported 19- and 22-vertex controls satisfy the induced `Ac=3c` rows and
the induced `lambda<=1`, `mu<=2` caps.  They lack 80 or 77 vertices and all
missing equalities; they are deliberately retained as hostile controls.

