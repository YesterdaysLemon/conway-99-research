# M7g incidence bridge: a signed-intersection obstruction and a local survivor

## 1. Frozen conditional setting

Work over `F_3` at the hypothetical prism-free rank-11 endpoint.  Let the
eight selected triangle blocks support

```text
a=(1,1,1,1,2,2,2,2) in im(B^T),
sum_i a_i z_i=0,
sum_i a_i z_i tensor z_i=0.
```

Their projective columns form the `M_7g` eight-set.  The following argument
uses the eight-set and the full three-dimensional space of symmetric forms
vanishing on it.  It does not choose or assume a unique labelled concurrent
secant matching.

## 2. The incidence norm identity

Choose `c in F_3^99` with

```text
a=B^T c
```

and put

```text
b=Ba.
```

Write `G=BB^T=A+I`.  Since every graph point belongs to seven triangle
blocks,

```text
B 1_231=7 1_99=1_99.
```

The signed support has sum zero, so

```text
0=1^T a=(B1)^T c=1^T c,
Jc=0.                                                (1)
```

The strongly regular identities over `F_3` are

```text
G^2=G-J,
AG=2J.
```

Consequently

```text
b=Gc,
Ab=AGc=2Jc=0,                                      (2)
```

and

```text
b^T b
 =c^T G^2 c
 =c^T(G-J)c
 =c^T Gc
 =a^T a
 =8
 =2 in F_3.                                        (3)
```

This is stronger than the automatic equation `B^TAb=Da=0`: (2) is a
coordinatewise equation on all 99 graph points.  Because `a` has support
eight, `b` is supported on the vertices occurring in those eight triangle
blocks, and its coordinate at a selected-union vertex is the signed sum of
the selected blocks containing that vertex.

Let `K=B_S^T B_S` be the point-incidence Gram restricted to the eight
selected blocks.  Its diagonal is three, hence zero in `F_3`, and its
off-diagonal entry is one exactly when the two selected triangles intersect.
Equation (3) becomes

```text
2 sum_(i<j, T_i intersects T_j) a_i a_j =2,

sum_(i<j, T_i intersects T_j) a_i a_j =1 in F_3.   (4)
```

In particular at least one selected pair intersects.

## 3. Four of the 27 polar restrictions are impossible

At the prism-free endpoint:

- an intersecting pair of distinct triangle blocks has centered product one;
- a disjoint pair has centered product equal to its cross-edge count in
  `{0,1,2}`.

Thus product zero or two forces disjointness, while product one remains
ambiguous.  Combining this one-way implication with (4) proves:

```text
if the restricted 8 by 8 polar Gram has no entry one,
then the incidence word cannot exist.             (5)
```

An exact reconstruction of all 27 forms gives:

```text
rank  zero graph  #ones among pairs  number of forms
 0       K8                0                 1
 2      2K4                0                 3
 2      2K4                8                 6
 2      2K4               16                 3
 3      4K2                8                 3
 3      4K2               12                 2
 3      4K2               16                 3
 4      2C4                8                 3
 4      2C4               12                 3.
```

Therefore (5) excludes exactly

```text
1 rank-zero K8 form + 3 rank-two 2K4 forms = 4 of 27 forms.   (6)
```

The qualification in (6) matters: it excludes only the three `2K4` forms
whose nonzero products are all two, not the whole rank-two zero-graph type.
The other 23 forms retain at least one possible intersection edge.

## 4. Graph-typed internal relations

For each selected index `i`, apply the tensor relation to `z_i`.  The word

```text
r^(i)_j=a_j D_ij                                  (7)
```

is a true relation among the eight original centered columns.  Its support
is the complement of the polar zero-neighborhood of `i`.  Hence every row
has the following weight:

```text
polar zero graph   weight of r^(i)
K8                         0
2K4                        4
4K2                        6
2C4                        5.                    (8)
```

The canonical eight-column relation code has exact enumerator

```text
1+24y^4+16y^5+32y^6+8y^8
```

and exactly twelve projective weight-four circuits and eight projective
weight-five circuits.  Thus the rank-two polar rows are weight-four circuits,
the rank-four rows are weight-five circuits, and the rank-three rows are
nonminimal weight-six relations.  These are true centered-column relations;
none is promoted to `im(B^T)` merely because the parent eight-word lies
there.

## 5. A rank-four induced local survivor

The machine-readable certificate `local-rank4-certificate.json` uses the
rank-four form with diagonal parameter `(0,0,1)`.  It deliberately lies in
the scout restriction that intersections use pair-specific vertices: only
selected triangles 0 and 3 meet, at one vertex, and no vertex belongs to
three selected triangles.  Its induced selected-union graph has:

```text
23 vertices,
51 edges,
11 graph triangles,
maximum local degree 8.
```

The independent checker proves exactly:

1. each selected triangle is a graph triangle and distinct selected blocks
   meet in at most one point;
2. the unique selected intersection occurs at a polar-product-one pair;
3. every disjoint selected pair has exactly its prescribed `0`, `1`, or `2`
   cross edges;
4. its signed incidence vector is the archived `b` and satisfies `Ab=0` on
   every one of the 23 vertices;
5. `b^Tb=2`, matching (3);
6. every local edge has at most one common neighbor and every local nonedge
   has at most two;
7. no induced triangular prism occurs in the 23-vertex graph; and
8. all twelve internal weight-four circuits and all eight internal
   weight-five circuits cross-realize zero graph-vertex pairs in this model.

Item 8 explains why the existing exact-transversal multiplicity bounds do
not eliminate this support: those bounds apply to circuits that
cross-realize a vertex pair, while the entire internal circuit portfolio of
this local model avoids that sector.

The certificate is not a graph completion.  Eighteen of its edges have no
common neighbor inside the 23-vertex union and would need their unique third
vertices outside.  The model omits the other 76 graph points, the other 223
triangle blocks, all outside degree and common-neighbor equalities, and the
full rank-11 231-column frame.  It proves only that the named local equations
do not exclude the rank-four branch.

## 6. Boundary

The rigorous advance is the incidence equation (4) and the exact exclusion
of four polar forms in (6).  The rank-four certificate shows that the
remaining bridge is genuinely global: even `Ab=0`, exact selected-pair
products, local `lambda/mu` caps, and local prism-freeness coexist.

```text
weight-eight word excluded: NO (4/27 polar forms excluded)
rank-11 endpoint excluded:  NO
Conway-99 resolved:          NO
global status:               UNKNOWN
```

