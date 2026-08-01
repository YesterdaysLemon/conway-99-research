# Rank-four point--line coupling

## 1. Frozen conditional branch and reconstruction

Assume the frozen hypothetical prism-free rank-11 endpoint.  Import the
manifest-pinned Wave 209 statement that a surviving rank-four branch has

```text
Aq=-4q,       q.q=56,
t=B^Tq,       Ct=0,       Bt=3q,
t_i=-3 alpha_i  (i=0,...,7),
alpha=(1,1,1,1,-1,-1,-1,-1).
```

The checker does not import the Wave 209 Python module.  It reconstructs the
M7g columns, the three rank-four polar forms, all 83 accepted marked subsets
per form, and the complete 249-node constraint-relabeling partition.  It then
independently replays the manifest-pinned Wave 209 point controls and Farkas
vectors.  The reconstructed survivors are exactly

```text
orbit ids:       0, 2, 4, 11, 12, 14, 23
orbit sizes:     6,12, 6,  6, 12,  3,  6
labelled total: 51.
```

This is a relabeling of the eight selected coordinates by checked
sign-preserving permutations.  It is not an automorphism assumption about an
unknown graph.

## 2. Point signatures

For a point `x` and selected triangle `T_i`, use the Wave 209 signature

```text
s_i(x) = -1  if x is in T_i,
         +1  if x is outside T_i and adjacent to its unique T_i point,
          0  otherwise.
```

The `lambda=1` equation makes the adjacent point unique.  Expansion of
`q=(A-3I)B_S alpha/3` gives

```text
q_x = (1/3) sum_i alpha_i s_i(x).                 (1)
```

There are 2,187 signatures in `{-1,0,+1}^8` for which (1) is integral.  Put

```text
M(s)={i:s_i=-1}.
```

The selected-intersection graph `H` is triangle-free on all seven surviving
orbits.  Hence an actual point has one of the following selected memberships:

```text
M(s)=empty,
M(s)={i},
M(s)={i,j} with ij in H.                          (2)
```

A pair not in `H` is disjoint.  Three selected triangles cannot share a point
because that would create a triangle in `H`.  Filtering by (2) leaves,
respectively for the seven orbit representatives,

```text
444, 576, 532, 532, 488, 510, 444
```

admissible point signatures.  No target automorphism or unnamed point is
chosen in this filtering.

## 3. Exact three-point decomposition of a residual triangle

Let `R` be one of the 223 unselected triangles.  Its Wave 209 aggregate type
is `(d,h,t_R)`, where

* `d_i=F_{Ri}` is its selected polar signature;
* `i in h` means `R` meets `T_i`; and
* `t_R=sum_(x in R)q_x` lies in `{-2,-1,0,1,2}`.

For the three points `x_1,x_2,x_3` of `R`, every coordinate multiset is
forced:

```text
i in h:      {s_i(x_1),s_i(x_2),s_i(x_3)}={-1,+1,+1};
i not in h:  exactly d_i entries are +1 and 3-d_i are 0.   (3)
```

For the first line, the intersection point contributes `-1`; the other two
points of `R` are adjacent to that point and contribute `+1`.  For the second
line, every cross edge has a distinct endpoint on `R`, again by `lambda=1`.

The negative coordinates must also group into actual points.  If `ij` is an
edge of `H` and both `i,j` lie in `h`, then `R` meets `T_i` and `T_j` at their
common point: meeting them at two different points would give an edge two
common neighbors.  Therefore `H[h]` is a matching; each matching edge uses one
point, every unmatched element of `h` uses one point, and

```text
|h|-|E(H[h])| <= 3.                               (4)
```

Conversely, the checker enumerates every unordered triple of integral point
signatures satisfying (3), (4), and

```text
q(x_1)+q(x_2)+q(x_3)=t_R.                         (5)
```

These are local incidence columns, not named triangles in a graph.  Across
the seven representatives there are 507--531 realizable residual types and
11,444--12,110 local three-point columns.

## 4. Global typed incidence equations

For every local column `p=(d,h,t;s_1,s_2,s_3)`, let `W_p` be its multiplicity.
For every admissible signature `s`, let `X_s` be the number of points with
that signature.  An actual graph gives nonnegative integers `W_p,X_s`.

### Triangle-side rows

The `W_p` variables retain all 99 independently verified Wave 209 aggregate
rows.  In particular they include:

* exactly 223 residual triangles;
* every selected polar-coordinate margin;
* every selected polar product moment;
* residual `t` sum zero and squared norm 96;
* exact one- and two-way selected intersection counts; and
* all eight selected rows of `Ct=0`.

Every row is necessary for an actual endpoint.  Some archived duals use only
a subset, but exact replay checks their coefficients in the full row universe.

### Point-side rows

The `X_s` variables retain all 279 independently verified point-signature
rows: 99 points, every one- and two-coordinate table, `sum q=0`, and
`sum q^2=56`.  These include the exact selected-line incidences.  For each
selected `T_i`, precisely three point rows have `s_i=-1`; their pair tables
record whether each other selected triangle intersects `T_i` or contributes
cross-edge endpoints.  Thus the selected triangle point multisets are not
free anonymous choices.

### Point--line incidence rows

Let `m_p(s)` be the multiplicity of `s` among the three rows of local column
`p`.  Every point lies on seven triangles, and exactly `|M(s)|` of them are
selected.  Aggregating over points of the same signature gives the necessary
integer equation

```text
sum_p m_p(s) W_p = (7-|M(s)|) X_s.                (6)
```

This is the missing coupling between the previously separate anonymous
censuses.

### Incident triangle-sum rows

Since `Bt=3q`, the sums of the seven incident triangle values at a point add
to `3q_s`.  Its selected incident triangles contribute

```text
sum_(i in M(s)) t_i = -3 sum_(i in M(s)) alpha_i.
```

Therefore its residual demand is exactly

```text
Delta(s)=3q_s+3 sum_(i in M(s)) alpha_i,
sum_p t_p m_p(s) W_p = Delta(s) X_s.              (7)
```

Equation (7) is an equality, not an interval bound.  The number of equations
in the complete system is `99+279+2N`, where `N` is the representative's
admissible point-signature count; it ranges from 1,266 to 1,530.

## 5. Integer Farkas exclusions

Write all rows from Section 4 as

```text
A z=b,       z=(W,X)>=0.
```

For each of the seven representatives, `coupling-certificates.json` archives
a sparse integer vector `y`.  The standard-library replay evaluates every
integer column directly and proves

```text
A^T y >= 0,       b^T y < 0.                      (8)
```

If `Az=b` and `z>=0` existed, then `(A^Ty)^Tz=b^Ty` would be simultaneously
nonnegative and negative.  Thus (8) excludes even a nonnegative real typed
incidence solution, and therefore excludes an actual graph in that branch.

The exact certificate census is:

| orbit | labelled branches | local columns | nonzero dual entries | `b^Ty` |
|---:|---:|---:|---:|---:|
| 0 | 6 | 12,110 | 71 | -4 |
| 2 | 12 | 11,444 | 102 | -239,020 |
| 4 | 6 | 11,672 | 140 | -18 |
| 11 | 6 | 11,672 | 140 | -18 |
| 12 | 12 | 11,888 | 101 | -239,020 |
| 14 | 3 | 12,003 | 390 | -3,240 |
| 23 | 6 | 12,110 | 72 | -4 |

Both the minimum local-column score and minimum point-column score are zero
for every certificate.  All 51 labelled branches are covered by explicit
sign-preserving constraint transports.  The checker maps every admissible
point row, residual type, and local decomposition and checks the defining
rules after transport, for 601,377 transported local-column checks in total.
This is a finite-system isomorphism, not a graph automorphism assumption.

SciPy/HiGHS was used only to suggest low-L1 floating dual vectors.  Each
candidate was rationalized to integers and then accepted only after (8) was
replayed with Python integers.  Solver status, floating feasibility, and model
confidence were not promoted.

## 6. Failed coarse relaxation and positive controls

There are 35 unordered triples of values in `{-2,-1,0,1,2}`.  Fixing the
selected `q`-triples from each sealed Wave 209 point control and imposing
`|t_R|<=2` leaves 21 residual triple types.  The coarse system also imposes:

* 223 residual triples;
* seven line incidences per point value;
* residual `t` sum zero; and
* residual squared `t` norm 96.

`coarse-q-type-controls.json` contains an exact nonnegative integer control
for every one of the seven orbits.  The default checker replays all counts.
These controls prove that value multiplicities and triangle sums alone cannot
exclude the branches.  They are not 99 named points, 223 named residual
triangles, adjacency, or a graph.

## 7. Exact boundary and status wall

Subject to the frozen Wave 208/209 hypotheses, this proof agent has derived an
exclusion of all 51 rank-four branches.  The package is labelled `DERIVED`,
not `VERIFIED`; a fresh verifier must reconstruct and attack the certificates
before integration can promote them.

This lane says nothing about the surviving rank-three branch.  It supplies no
99-vertex graph and no unconditional nonexistence theorem.  The rank-three
branch and Conway-99 remain `UNKNOWN`.
