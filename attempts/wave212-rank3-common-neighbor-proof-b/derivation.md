# Common-neighbor, triangle, and four-cycle reduction

Claim label: `DERIVED` pending independent replay.

## 1. The two outside-edge species

For an outside vertex `x`, let `C_x` be its support column, put

```text
t_x = |C_x|,
a_x = e(A_S[C_x]).
```

In a completion, the neighborhood of every vertex is `7K2`.  Inside the
support part of `N(x)`, the `a_x` known edges use `2a_x` support neighbors.
Every remaining support neighbor must be paired with an outside neighbor that
shares exactly that support point.  Hence the number of `q=1` outside edges at
`x` and the number of all-outside triangles through `x` are

```text
b_x = t_x-2a_x,
c_x = 7-t_x+a_x.                                  (1)
```

The remaining outside degree is `2c_x`, and indeed
`b_x+2c_x=14-t_x`.

For orbits 0 and 4, the `(t,a,b,c)` distribution is

```text
(0,0,0,7)^17 (2,0,2,5)^60 (2,1,0,6)^1
(4,1,2,4)^4 (4,2,0,5)^3.
```

For orbit 29, the last line is instead

```text
(4,0,4,3)^1 (4,1,2,4)^2 (4,2,0,5)^4.
```

In all three cases, `sum b_x=128` and `sum c_x=456`.  Thus every completion
has exactly

```text
64 q=1 edges, 456 q=0 edges, 152 all-outside triangles.   (2)
```

Each `q=1` edge belongs to its unique support triangle and has no outside
common neighbor.  Each `q=0` edge belongs to a unique all-outside triangle.

## 2. Simultaneous coloured one-factors

Fix a support point `s`.  The outside vertices containing `s` that are not
already paired to a support neighbor form a labelled set `U_s`.  The required
outside pairs are precisely pairs of columns whose intersection is `{s}`.
Such a pair has a unique colour, so the candidate edge sets for distinct
support points are disjoint.  Consequently, once a perfect matching is chosen
on every `U_s`, their union is automatically a simultaneous coloured graph;
independent choices do not compete for an edge or for a colour slot.

The committed controls give one complete labelled choice for each orbit.
Exact replay proves that the union has 64 edges, covers every forced endpoint
once in each colour, has the degrees `(b_x)`, contains the selected `q=1`
edges, and alone violates no common-neighbor upper bound.  Therefore coloured
one-factor compatibility does not exclude any of the three orbits.

## 3. Four-cycle census

Among the `3570` outside pairs, the support-intersection histogram is

```text
q=0: 2878,  q=1: 652,  q=2: 40.                  (3)
```

An outside nonedge with `q=0,1,2` has respectively `2,1,0` outside common
neighbors.  Opposite-pair counting therefore gives

```text
all-outside C4                 (2878-456)/2 = 1211,
exactly-one-support C4          652-64      =  588,
two supports, alternating                     40.       (4)
```

For support-support nonedges, the number of common vertices already in the
support has histogram `(40,12,16)` at values `(0,1,2)`.  For support-outside
nonedges the corresponding histogram is `(588,440,12)`.  The remaining cycle
classes are consequently

```text
two adjacent supports: 440/2 = 220,
three supports:                 12,
four supports:               16/2 = 8.           (5)
```

Thus the exact support-count census is

```text
0S 1211; 1S 588; 2S 40+220; 3S 12; 4S 8,
total 2079.                                         (6)
```

All integrality and double-counting tests close; this is not a contradiction.

## 4. A sharp upper-bound reformulation

The outside degrees are `14^17,12^61,10^7`, so

```text
sum_x binom(d_x,2)=5888.
```

Using (3) and `|E(D)|=520` also gives

```text
sum_{x<y} (2-q_xy-D_xy)=2*3570-(652+2*40)-520=5888.  (7)
```

Therefore, for any binary `D` with the correct degrees, if every pair obeys

```text
|N_D(x) intersect N_D(y)| + D_xy <= 2-q_xy,        (8)
```

then equality holds for every pair.  The quadratic block can thus be attacked
as a finite forbidden-subconfiguration problem: it is enough to rule out all
common-neighbor excesses.  Deficits cannot remain without a compensating
excess elsewhere.

## 5. Labelled hostile incidence controls

For each orbit, the certificate supplies all 64 coloured edges and 152
pairwise-disjoint-support triples.  The triple family is linear, covers each
vertex `c_x` times, and its 456 pairs together with the coloured edges give a
520-edge graph with every required degree and all ten selected pair values.
It also has zero common neighbors for all 40 `q=2` pairs and all 64 coloured
edges.

This is deliberately only an incidence relaxation.  `FD` was not imposed:
the controls satisfy respectively `499`, `534`, and `532` of its `1190`
entries.  Their quadratic residual histograms are

```text
orbit 0:  -2:300 -1:911 0:1256 1:769 2:268 3:59 4:6 5:1
orbit 4:  -2:340 -1:882 0:1259 1:722 2:278 3:73 4:15 5:1
orbit 29: -2:322 -1:869 0:1299 1:730 2:278 3:61 4:11.
```

They contain `132`, `154`, and `123` spurious outside triangles beyond the
152 designated blocks.  Hence they are not local `7K2` graphs, not solutions
of the quadratic block, and not SRG constructions.

## 6. Boundary

The edge split, triangle count, four-cycle census, coloured matching union,
and upper-bound reformulation are exact.  The first obstruction not resolved
here is simultaneous enforcement of `FD` and the forbidden common-neighbor
configurations on the 152-block incidence layer.  No orbit is excluded and no
outside block is constructed.  The rank-three branch, the rank-11 endpoint,
and Conway-99 remain `UNKNOWN`.
