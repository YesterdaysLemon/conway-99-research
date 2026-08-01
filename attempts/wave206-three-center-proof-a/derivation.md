# Wave 206 proof A: three-center geometry and fixed-root coordinates

## Status

`DERIVED`, pending independent verification.  All statements are conditional
on the frozen branch

```text
G is srg(99,14,1,2), P=0, and rank_F3(D)=11.
```

No automorphism, vertex transitivity, or Gram-kernel-to-vector inference is
used.  Nothing below proves that the endpoint graph exists or does not exist.

## 1. The fixed-root three-center Gram matrix

Fix a vertex `y`, and let `E_y=im(P_y)`, a six-dimensional nondegenerate
space.  Define the self-adjoint operator

```text
A_x^(y)=P_y P_x P_y restricted to E_y.
```

Then

```text
T_y[x,z] = tau_(xy;z) = tr(A_x^(y) A_z^(y)).
```

Consequently:

1. `T_y` is symmetric.
2. `rank(T_y)<=21`, because self-adjoint operators on a six-dimensional
   nondegenerate space form a 21-dimensional vector space.
3. `sum_x A_x^(y)=0`, from `sum_x P_x=0`, so every row sum of `T_y` is zero.
4. `T_y[x,x]=h_yx` and `T_y[y,x]=g_yx`.

For a fixed nonedge `x,y`, the `x`-row therefore gives the exact contraction

```text
sum_(z not in {x,y}) tau_(xy;z) = -h_xy-g_xy.
```

This packages every three-center trace at a fixed root into one rank-at-most
21 Gram matrix, but the rank and row-sum identities alone do not identify its
off-diagonal entries.

## 2. A 21-coordinate model

Write the seven triangles through `y` as root-star blocks and let
`z_0,...,z_6` be their vectors.  Their Gram matrix is

```text
G=J-I
```

over `F_3`, and `sum_i z_i=0`.  Put

```text
R_x = Z_y^* P_x Z_y,
r_x^(y)[i,j] = R_x[i,j]  for i<j.
```

The matrix `R_x` is symmetric and `R_x 1=0`.  Its 21 off-diagonal entries
therefore determine its diagonal:

```text
R_x[i,i] = -sum_(j != i) r_x^(y)[i,j].
```

They also determine the full operator:

```text
A_x^(y)=Z_y R_x Z_y^*.
```

The Wave 205 pair invariants become the first and quadratic moments of this
21-coordinate row:

```text
g_xy = 2 sum_(i<j) r_x^(y)[i,j],
sum_(i<j) r_x^(y)[i,j] = t_xy             (mod 3),
h_xy = tr(R_x G R_x G).
```

Finally, the zero-frame identity becomes 21 coordinate equations

```text
sum_x r_x^(y)[i,j]=0       for every i<j.
```

More generally, every genuine operator relation

```text
sum_x c_x P_x=0
```

projects safely to

```text
sum_x c_x r_x^(y)[i,j]=0   for every fixed y and every i<j.
```

Thus the nonconstant weighted relation independently obtained in the Wave
206 crossing-kernel lane has an immediate fixed-root coordinate image.  For
coordinate `{i,j}`, the four vertices in the owner fiber contribute their
explicit marked bits.  However, the 14 edge centers and all 20 non-owner
fibers may also contribute to the same coordinate.  No equation involving
only the four owner bits follows without additional control of those terms.

These formulas were replayed on all four sealed Wave 205 controls.  They
explain precisely what the earlier `t` and `h` information measures: `t`
fixes one linear moment modulo three, while `h` fixes one quadratic moment.

## 3. Exact graph placement around a nonedge

Fix nonadjacent vertices `x,y`.  Among the other 97 vertices, strong
regularity gives:

| relation of `z` to `x,y` | count |
|---|---:|
| adjacent to both | 2 |
| adjacent only to `y` | 12 |
| adjacent only to `x` | 12 |
| adjacent to neither | 71 |

The neighborhood of `y` is seven disjoint edges, one for each triangle
through `y`.  The two common neighbors of the nonedge `x,y` lie in two
different root-star blocks.  Call these the distinguished blocks.

The 14 neighbors of `y` are distributed as follows:

- the two common neighbors of `x,y` occupy one endpoint in each distinguished
  block;
- the 12 vertices adjacent only to `y` occupy the other endpoint in each
  distinguished block and both endpoints in each of the five ordinary
  blocks.

Thus all edge-third-center common-block placements are fixed exactly.

## 4. The 21 four-vertex nonneighbor fibers

Choose two distinct root-star blocks `i,j`, with endpoints
`a_i^0,a_i^1` and `a_j^0,a_j^1`.  For every choice `(p,q)`, the vertices
`a_i^p,a_j^q` are nonadjacent and have exactly two common neighbors.  One is
`y`; call the other `x_pq`.  It is nonadjacent to `y`.

The four `x_pq` are distinct.  Varying `{i,j}` partitions all 84
nonneighbors of `y` into

```text
21 labelled fibers x_00,x_01,x_10,x_11.
```

### Prism-free matching lemma

If, for example, `x_p0` were adjacent to `x_p1`, then

```text
{a_i^p,x_p0,x_p1}
```

would be a triangle.  Compare it with the disjoint root triangle

```text
{y,a_j^0,a_j^1}.
```

The forced cross edges are exactly

```text
y--a_i^p,  a_j^0--x_p0,  a_j^1--x_p1.
```

There are no extra cross edges: cross-block endpoints in `N(y)` are
nonadjacent, and an extra `a_j`--`x_pq` edge would give the nonedge `y,x_pq`
more than its two allowed common neighbors.  The two triangles would induce
a triangular prism, contradicting `P=0`.

The same argument excludes every fiber edge whose labels share one endpoint.
Hence the induced fiber graph is a subgraph of

```text
{x_00--x_11, x_01--x_10}.
```

There are only four possible induced fiber graphs: neither diagonal, either
single diagonal, or both diagonals.  This is an exact graph-theoretic
restriction with no symmetry assumption.

Each fiber `{i,j}` also owns the marked coordinate `r[i,j]`.  In the
normalized low-`t` modules, that bit is zero when the two special-row extra
positions align and one when they are distinct.  "Owns" does not mean that
other centers have zero in this coordinate.

## 5. Exact finite module censuses

### Edge third centers

For an edge `y,z`, after marking their common root-star block, the cross Gram
has the form

```text
C = [ 0    1^T ]
    [ 1   J_6+N ],
```

where `N` is a binary `6 by 6` matrix with every row and column sum two.
Complete enumeration gives 67,950 labelled matrices and 130 distinct
compressions.  Their exact profile is:

| rank | `g` | `h` | distinct compressions |
|---:|---:|---:|---:|
| 3 | 0 | 0 | 15 |
| 4 | 0 | 0 | 60 |
| 4 | 0 | 1 | 45 |
| 6 | 0 | 0 | 10 |

### Nonedge marked-coordinate census

The complete normalized Wave 205 `t=6,7` census was rerun, retaining only
modules with full two-star Gram rank 11, discriminant two, and true kernel
distance at least four.  Counts by `(h,r_marked)` are:

| `t` | `h` | marked `r` | count |
|---:|---:|---:|---:|
| 6 | 1 | 1 | 18 |
| 7 | 0 | 0 | 288 |
| 7 | 0 | 1 | 9 |
| 7 | 1 | 0 | 144 |
| 7 | 1 | 1 | 180 |
| 7 | 2 | 0 | 144 |

Therefore, within this censused branch:

- `t=6` forces marked `r=1` and `h=1`;
- at `t=7`, marked `r=1` excludes `h=2`;
- at `t=7`, marked `r=0` still permits all three values of `h`.

This is a genuine refinement of the pair-local table, but it does not yet
determine the distribution of marked bits among the four vertices of a
fiber.  Cases `t>=8` remain open.

## 6. Why the scalar contraction does not yet eliminate a module

For each of the four sealed fixed-pair controls (`t6_h1`, `t7_h0`,
`t7_h1`, and `t7_h2`), exact enumeration was performed against:

- all 130 edge compressions at each of the seven possible common blocks; and
- 270 distinct nonedge compressions at each of the 21 marked block pairs,
  obtained from the four sealed controls under all allowed relabellings.

At every tested relation to `y` and every corresponding root-star placement,

```text
tau = tr(A_x^(y) A_z^(y))
```

attains all three residues `0,1,2`.

For each fixed control the checker emits a 97-entry scalar ledger with the
correct `y`-rooted placement multiplicities and total

```text
-h_xy-g_xy.
```

Every ledger entry is individually realized by a local module.  The ledger
does **not** impose the prescribed adjacency of `x` and `z` or an `x,z` pair
module.  It also does not assert that its 97 entries coexist in one graph,
share one operator sum, or arise from one set of 231 columns.  It therefore
shows that the relation to `y` plus root-star placement is insufficient; it
does not decide whether the full labelled graph type of `x,y,z` determines
`tau`.

A separate formal control represents arbitrary self-adjoint operators in the
same 21-dimensional coordinate space.  For every surviving `h`, it produces
99 operators with sum zero and hence a symmetric, row-sum-zero `T_y` of rank
at most 21.  Its residual operator is not asserted to be a graph-derived
compression.

Together these two controls separate the obstruction cleanly:

- relation to `y` plus root-star placement does not fix `tau`;
- the untested `x,z` pair compatibility may still restrict `tau`;
- the rank-21 and zero-sum operator identities alone do not fix `h`;
- the unresolved condition is their **simultaneous** realization by the
  actual shared graph columns.

## 7. Strongest sealed boundary and next invariant

The exact root-relative three-center information checked here does not
eliminate any of the four surviving `t=6,7` controls at the marginal or
abstract-operator levels.  This is not a countermodel to the endpoint,
because neither the third `x,z` pair module nor a simultaneous 99-center
graph-derived completion was built.

The next required invariant is:

> the joint four-operator fiber law for the four compressions owned by each
> root-star block pair, coupled across all 21 fibers and the 14 edge centers
> by one shared 231-column realization.

Equivalently, one needs relations that constrain the four complete
21-coordinate rows in a fiber together, not only the marked bit, their
individual first/quadratic moments, or independently selectable
three-center inner products.  A nearer-term version must first impose all
three pair modules of each labelled triple, especially the missing `x,z`
pair.

The weighted kernel relation supplies 21 additional global linear equations
at every root, but the same non-owner mixing explains why it does not yet
close the four-fiber law.

The endpoint status remains `UNKNOWN`.
