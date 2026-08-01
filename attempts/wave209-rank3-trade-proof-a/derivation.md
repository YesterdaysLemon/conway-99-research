# Exact reductions for the rank-three M7g signed trade

Claim label: `DERIVED` pending independent replay.

## 1. Point signatures and two exact moments

Let `P`, `N`, and `Z` be the `+1`, `-1`, and zero coordinates of `c`.
Since `Ac=3c` and the graph is 14-regular, `c` is orthogonal to the all-one
vector.  Write

```text
|P|=|N|=k,       k in {7,10},
x=e(P,N).
```

If `v` is positive and has `j_v` negative neighbors, its support signature is
`(j_v+3,j_v)`.  A negative vertex has the reversed signature.  Hence

```text
sum_(v in P) j_v = sum_(v in N) j_v = x,
e(P)=e(N)=(x+3k)/2.                              (1)
```

In particular, `x+3k` is even.  A zero vertex has equally many positive and
negative neighbors; call its signature `(t,t)` and let `z_t` count such
vertices.  Counting `P-Z` edges gives

```text
sum_t t z_t = 11k-2x.                            (2)
```

Now count common neighbors of all ordered-by-sign pairs in `P x N`.
There are `x` adjacent pairs with one common neighbor and `k^2-x`
nonadjacent pairs with two.  A support vertex with opposite degree `j_v`
is a common neighbor of `j_v(j_v+3)` such pairs.  Therefore, with
`J_2=sum_(P union N) j_v^2`,

```text
sum_t t^2 z_t = 2k^2-7x-J_2.                    (3)
```

These are exact `lambda=1`, `mu=2` identities, not inequalities.

Let `f=1_P+1_N`.  Since `f^T A f=4x+6k` and the largest nonprincipal
eigenvalue is three,

```text
4x+6k <= 14(2k)^2/99 + 3(2k-(2k)^2/99),
x <= k^2/9.                                      (4)
```

The checker retains all nondecreasing `j` profiles satisfying (1), the
Erdos--Gallai and Gale--Ryser necessary conditions, and every nonnegative
integer solution of (2)--(3).  This complete aggregate census has five rows
for `k=7` and 425 rows for `k=10`.

There is also an exact selected-line row identity.  Put `R=U^T A U` and
`K=U^T U`.  Multiplying `A(U alpha)=3U alpha` by `U^T` gives

```text
(R-3K) alpha=0.                                  (4a)
```

In one row, the diagonal contributes `-3 alpha_i`; the three same-sign
selected lines contribute `3*2 alpha_i`; and the three unmatched
opposite-sign lines each contribute `-alpha_i`, whether their product-one
pair is disjoint (`R=1,K=0`) or intersecting (`R=4,K=1`).  Everything
cancels except minus the cross count to the unique matched product-zero
opposite line.  Thus all four matched product-zero pairs have cross count
exactly zero.  This independently excludes the residue-zero lift three and
justifies the exact labelled polar counts used below.

## 2. Support 14 collapses to one outside signature

For `k=7`, parity and (4) allow `x=1,3,5`.  The exact aggregate census gives:

```text
x=1: j_P=j_N=(0,0,0,0,0,0,1), four outside rows;
x=3: j_P=j_N=(0,0,0,0,1,1,1), one outside row
     z_0=14, z_1=71;
x=5: no row.
```

The five selected intersections are five labelled edges `ij` of the
product-one `K_(4,4)` minus a perfect matching.  If their intersection
degrees are `d_i,d_j`, their common zero point already sees `3-d_i`
positive and `3-d_j` negative support points on its two selected lines.
Thus its outside signature obeys

```text
t >= max(3-d_i,3-d_j).                           (5)
```

The `x=3` row has `t<=1` everywhere, so every nonisolated selected-line
label would have degree at least two.  A five-edge bipartite graph cannot
have minimum positive degree two: each side has degree sum five and hence at
most two active vertices, allowing at most four edges.  The checker also
tests all 792 labelled five-edge subsets and finds zero compatible subsets.
Therefore `x=1`.

There is one cross edge, and its endpoints are the unique vertices of
opposite degree one.  On either sign, the induced graph consequently has
rooted degree sequence `(4,3,3,3,3,3,3)`.  Ambient common-neighbor counts
give the induced caps

```text
adjacent pair:    at most one internal common neighbor;
nonadjacent pair: at most two internal common neighbors.
```

A complete root-preserving seven-vertex census gives 810 labelled graphs
with the degree sequence, 360 satisfying the adjacent cap, and 180 satisfying
both caps.  Those 180 are one abstract rooted isomorphism type:

```text
01 02 03 04 12 15 26 34 35 46 56.               (6)
```

The other adjacent-cap type has a nonedge with three internal common
neighbors and is rejected.  Relabelling is used only to describe an abstract
seven-vertex type after every labelled graph is checked; no automorphism of
the hypothetical target or of the marked M7g data is assumed.

For (6), subtract internal common neighbors from the required one-or-two
ambient common neighbors of each same-sign pair.  Exactly seven pairs have
deficit one:

```text
14 15 23 26 35 46 56.                            (7)
```

The deficit graph (7) is triangle-free.  The positive-neighbor set of any
zero vertex must be a clique in this deficit graph, so `t<=2`; the same holds
on the negative side.  Equations (2)--(3) now force the unique profile

```text
z_0=17, z_1=61, z_2=7.                            (8)
```

Each of the seven `t=2` vertices consumes one edge of (7) on each sign side,
so it determines a bijection between two seven-edge deficit sets.  The exact
cross-sign common-neighbor capacities retain 4,480 of all 5,040 bijections.
After the seven `2 x 2` rectangles are removed, the 61 `t=1` rows have
incidence degrees `(9,9,9,9,9,8,8)` on each side.  This is still a capacity
table, not an outside graph.

## 3. The marked selected lines leave 204 labelled intersection graphs

On one sign side, a selected line of intersection degree `d_i` contains
`3-d_i` support points.  These support blocks partition the seven vertices.
A block of size three must be a triangle of (6); its only two triangles are
`012` and `034`, both containing the cross-edge root vertex `0`.  A size-two block
comes from a selected line whose third point is an intersection zero, so its
support edge must have no internal support common neighbor.  The five such
external-third edges are

```text
15 26 35 46 56,
```

and have matching number two.  Checking all block packings eliminates the
degree multisets `(3,2,0,0)` and `(2,1,1,1)` and retains exactly

```text
(3,1,1,0) or (2,2,1,0)                           (9)
```

on each sign side.  Both rows of (9) have one isolated selected line; its
three support points form a triangle containing the cross-edge root.  The
two isolated lines therefore contain the unique `P-N` support edge.  Because
they are disjoint and have no zero points, their selected-pair cross count is
exactly one.  In the frozen prism-free endpoint the exact disjoint cross
counts are `0,1,2`, so their labelled pair must be an unused product-one pair.

Among all `C(12,5)=792` labelled intersection subsets, the two degree tests
and this isolated-pair test retain exactly 204:

```text
P (3,1,1,0), N (3,1,1,0):  12
P (3,1,1,0), N (2,2,1,0):  36
P (2,2,1,0), N (3,1,1,0):  36
P (2,2,1,0), N (2,2,1,0): 120.
```

This is the strongest support-14 reduction here; none of the 204 marked
cases is claimed realizable or excluded.

## 4. Support 20: exact moment and selected-zero reductions

For `k=10`, parity and (4) initially allow `x=0,2,4,6,8,10`.  Equations
(1)--(3) plus the graphical degree tests yield no row for `x=10`; the other
values give 425 aggregate rows.

There are two selected intersection zeros.  Summed over all 16 opposite-sign
selected-line pairs, the required restricted cross count is 18.  An edge
between support points of opposite signs contributes one and is counted by
`x`.  Edges incident with either selected intersection zero can cover some
of the 18 counts, but they simultaneously consume the exact same-sign and
opposite-sign entries of the labelled polar matrix.

The checker groups points only by their one- or two-line selected membership
and exhausts every bounded number of zero--support or zero--zero edges.  The
dynamic state records all 28 selected-pair counts; it has at most 256 states
and never searches outside the selected union.  It proves the following
upper bounds on zero-mediated opposite counts, equivalently raw lower bounds
on `x`:

```text
two intersections share a line (24 labelled subsets): max 13, x>=5;
disjoint swapped matching positions (6 subsets):       max 16, x>=2;
other disjoint subsets (36 subsets):                    max 15 or 14,
                                                        x>=3 or 4.
```

Combining parity and the global moment catalog leaves

```text
shared endpoint:   x in {6,8};
swapped disjoint:  x in {2,4,6,8};
other disjoint:    x in {4,6,8}.                        (10)
```

Thus `x=0` is excluded and `x=2` is confined to six labelled selected
intersection pairs.  There remain 352 aggregate degree/outside rows across
`x=2,4,6,8`.  The imported 22-vertex hostile control realizes the internal
selected-union equations at `x=6` with shared intersections, so (10) does
not close the branch.

## 5. The complete 231-line reformulation

Let `B` be the point-by-triangle incidence matrix and let
`C=B^T B-3I` be the 18-regular triangle-intersection graph.  Since
`BB^T=A+7I`, the line-sum vector `tau=B^T c` satisfies

```text
C tau=7 tau,       B tau=10c,
sum tau=0,         ||tau||^2=20k.                 (11)
```

For selected line `i`, if its actual intersection degree is `d_i`,

```text
tau_i=alpha_i(3-d_i).                             (12)
```

The seven incident line sums at every point add to `10c_v`.  The checker
retains (11)--(12) exactly.  In the support-14 branch the selected-line norm
is 30, 32, or 34 and the unselected-line norm is 110, 108, or 106.  In the
support-20 branch the corresponding split is `52+148` for disjoint selected
intersections and `54+146` when they share a line.  All are arithmetically
feasible.

For completeness, if `R_r` counts graph triangles containing `r` support
points and `R_3` is left free, edge and point incidence give

```text
R_2=2x+3k-3R_3,
R_1=8k-4x+3R_3,
R_0=231-11k+2x-R_3.                              (13)
```

`exact-results.json` includes one nonnegative signed line-type census for
each support size.  They are hostile aggregate controls only: they do not
assign the 231 actual lines or their intersections.

## 6. Boundary

The support-14 branch is reduced to a unique signed support type, profile
(8), 204 labelled marked-intersection graphs, and 4,480 cross-deficit
bijections for each fixed rooted support labelling.  The support-20 branch
retains 352 aggregate rows and the exact cases (10).  No 99-vertex adjacency
matrix, global contradiction, or complete outside extension is obtained.
The rank-three survivor, the rank-11 endpoint, and Conway-99 remain
`UNKNOWN`.
