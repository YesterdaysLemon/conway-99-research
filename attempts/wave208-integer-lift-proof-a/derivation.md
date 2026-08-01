# Integral spectral splitting and the balanced weight-fourteen frontier

All statements are conditional on a hypothetical simple
`srg(99,14,1,2)`.  No graph automorphism is assumed.  The exact finite
checks in this package use only integer arithmetic and the seven-point Fano
incidence design; they do not search for a graph on 99 vertices.

Let a nonzero ternary adjacency-kernel word be represented by

```text
x in {0,1,-1}^99,
P={x=1}, N={x=-1}, p=|P|, n=|N|,
w=p+n, p-n=3t,
z=Ax/3 in Z^99.
```

Wave 207 gives the exact lift

```text
Az=4x-z+2t*1.                                      (1)
```

Its category sums are already known to be redundant.  Here we retain the
individual integral vector `z`.

## 1. Exact integral spectral splitting

Since `sum(x)=3t` and the graph is 14-regular,

```text
sum(z)=14t.                                        (2)
```

Define

```text
Q=9(z-x)-t*1,
R=11(4x+3z)-6t*1.                                 (3)
```

Substitution in (1), using `Ax=3z` and `A1=14*1`, gives

```text
AQ=-4Q,       sum(Q)=0,
AR= 3R,       sum(R)=0.                            (4)
```

Thus every residual ternary word produces exact **integral** vectors in the
two restricted real eigenspaces.  Put

```text
h=x.z=(x^T A x)/3.
```

The SRG identity gives

```text
z.z=(4w-h+6t^2)/3.                                (5)
```

Expanding (3) now yields

```text
Q.Q=63[3(w-h)+t^2],
R.R=77[11(4w+3h)-18t^2].                          (6)
```

There is also an exact residue-shell quantization.  Every coordinate of
`Q` is `-t mod 9`; write `Q_i=9m_i-t`.  Equation `sum(Q)=0` says
`sum(m_i)=11t`.  For `0<=t<=8`, the least coordinate norm in this residue
class is obtained from `11t` ones and `99-11t` zeros:

```text
Q.Q >= 99t(9-t).
```

Moreover,

```text
Q.Q-99t(9-t)
 =81 sum_i [m_i(m_i-1)]
 =162L,        L a nonnegative integer.            (7)
```

The machine-readable output lists every `h` allowed by (5)--(7) and the
restricted spectral interval for weights 17, 20, and 23.  These are
necessary arithmetic rows only; none is asserted realizable.

## 2. Balanced weight 14

Wave 207 independently forces `(p,n)=(7,7)` at weight 14, so `t=0`.  The
primitive integral splitting simplifies to

```text
q=z-x,             Aq=-4q,
r=4x+3z,           Ar= 3r,
q.r=0.                                             (8)
```

The edge parity, congruence `h=2 mod 3`, and restricted spectral interval
give exactly

| `h` | `q.q` |
|---:|---:|
| -16 | 70 |
| -10 | 56 |
| -4 | 42 |
| 2 | 28 |
| 8 | 14 |
| 14 | 0 |

This is a six-branch classification, not an exclusion.

## 3. The `q=0` / exact `3`-eigenvector branch

If `q=0`, then `z=x` and `Ax=3x`.  Let `e` be the number of edges in each
seven-point sign class.  Summing the eigenvector equation over either side
gives

```text
e(P,N)=2e-21,
e(P union N)=4e-21.                               (9)
```

The positive restricted-eigenvalue bound on a 14-set is

```text
e(P union N)
 <= floor(3*14/2 + 11*14^2/(2*99))
 =31.
```

Together with nonnegativity in (9), this leaves `e=11,12,13`.

For one sign side, write its internal degrees as `3+c_v`; the cross degree
of that signed vertex is `c_v`, and `sum c_v=2e-21`.  Convexity gives the
minimum wedge counts recorded below.  On the other hand, every adjacent
pair has at most `lambda=1` common neighbor and every nonadjacent pair at
most `mu=2`, so

```text
sum_v C(d_v,2) <= e+2(C(7,2)-e)=42-e.             (10)
```

- For `e=13`, the minimum wedge count is 36 but (10) is 29: impossible.
- For `e=12`, both sides of (10) are 30.  Equality forces every edge to
  lie in a triangle inside the sign class.  Its incident edges are then
  paired by those unique triangles, so every degree is even.  The forced
  minimizing sequence `(4,4,4,3,3,3,3)` contradicts this.
- For `e=11`, the degree sequence is `(4,3,3,3,3,3,3)` and there is exactly
  one cross edge, joining the unique degree-four vertex on each side.
  This branch survives the argument.

Thus `q=0` is sharply reduced but not excluded.

## 4. The `q.q=14` branch and complementary Fano incidence

The independently audited short-eigenvector theorem says that an integral
norm-14 `-4` eigenvector has seven `+1` and seven `-1` entries.  Its two sign
classes are independent and its cross graph is the symmetric
complementary-Fano `2-(7,4,2)` incidence design.  Every outside vertex meets
at most one vertex of each sign class; 70 outside vertices meet exactly one
of each, and the remaining 15 meet neither.

Here `h=8`, so

```text
x.q=h-w=-6.                                       (11)
```

Let `alpha` be the number of common support coordinates on which `x` and
`q` have the same sign, and `beta` the number on which they have opposite
signs.  Equation (11) gives

```text
beta=alpha+6,
0<=alpha<=4,
|supp(x)-supp(q)|=|supp(q)-supp(x)|=8-2alpha.      (12)
```

The entries of `z=x+q` are magnitude two on the `alpha` same-sign
coordinates, zero on the `beta` opposite coordinates, and magnitude one on
the two exclusive parts.

### Complete seven-point capacity census

Label the negative support of `q` by the seven Fano points and the positive
support by the seven complements of Fano lines.  Partition each side into

```text
S     same-sign overlap,
O     opposite-sign overlap,
Qonly q-only coordinates.
```

At an `O` coordinate, the equation `Az=4x-z` prescribes signed outside mass
after the contributions from the opposite Fano side are subtracted.  Every
exclusive `x` coordinate can contribute to at most one vertex on each
Fano side.  `exact_check.py` enumerates **every labelled partition** and
checks this necessary token capacity.  No automorphism quotient is used.

| `alpha` | labelled partitions | token-capacity survivors |
|---:|---:|---:|
| 0 | 3,003 | 651 |
| 1 | 24,010 | 42 |
| 2 | 41,895 | 0 |
| 3 | 13,230 | 0 |
| 4 | 441 | 0 |

Thus `alpha>=2` is impossible already at this exact necessary layer.

The 42 `alpha=1` rows are 21 copies of each of two sign-reversed patterns.
In one orientation there is one positive and five negative exclusive
tokens.  Two negative-demand Fano blocks require total negative outside
surplus four.  A used outside token is one of the 70 vertices meeting one
point on **both** Fano sides, so each such negative token also consumes an
endpoint on the other side.  That other side has total negative surplus
two and only one positive token, hence can host at most three negative
endpoints.  The required four are impossible.  Sign reversal handles the
other 21 rows.

Consequently

```text
alpha=0,
beta=6,
|supp(x) union supp(q)|=22,
z has exactly eight +1 and eight -1 entries.       (13)
```

This is the main strict reduction of the package.

## 5. The three surviving exclusive-sign shapes

Let

```text
k=number of opposite-overlap coordinates with x=+1 and q=-1.
```

Equation (13) gives `7-k` positive and `k+1` negative `x`-only
coordinates.  At an `x`-only coordinate, the contribution from the two
Fano sides is some `c in {-1,0,1}`.  If the coordinate is positive, its
neighbors among the other exclusive coordinates satisfy

```text
d_same-d_opposite=3-c >=2.                        (14)
```

For a negative coordinate the sign-reversed equation is at least two as
well.  Therefore both exclusive sign classes have at least three vertices:

```text
k in {2,3,4}.                                     (15)
```

For `k=2`, the three-point negative side must be a `K3`, has no exclusive
cross edge, and every one of its vertices has Fano contribution `-1`.
The `k=4` statement is the sign reverse.  For `k=3`, both exclusive sides
have four vertices.  A four-vertex graph of minimum degree two satisfying
the adjacent-pair common-neighbor cap `lambda=1` can only be a `C4`.
Equation (14) then forces no cross edges and Fano contributions `+1` on the
positive cycle and `-1` on the negative cycle.

## 6. Exact hostile 22-vertex control

The machine-readable output contains a labelled partial graph on the 14
Fano-support vertices and eight exclusive vertices.  It uses two disjoint
exclusive `C4`s and has the following exact properties on all 22 displayed
vertices:

```text
Ax=3z,
Az=4x-z,
Aq=-4q,
every displayed adjacent pair has <=1 displayed common neighbor,
every displayed nonedge has <=2 displayed common neighbors.
```

It also respects the local triangle upper cap.  This is a hostile boundary,
not a construction: all other 77 vertices, their equations, missing degree
slots, exact common-neighbor lower requirements, and remaining matching
mates are absent.  It proves that the reduction (13)--(15) is not by itself
a contradiction.

## 7. Weights 17, 20, and 23

For these weights, (3)--(7) give exact integral eigenvectors and residue
shell indices for every sign composition up to negation.  The full table is
in `exact-results.json`.  No composition is removed merely because its
arithmetic row exists, and this package does not add a graphical exclusion
for those three weights.

## Status

```text
integral 3/-4 spectral split:              DERIVED
balanced weight-14 six-shell reduction:    DERIVED
q=0 branch reduced to one-cross-edge case: DERIVED
q.q=14 same-sign overlap alpha>0:          REFUTED (discovery)
q.q=14 remaining alpha=0, k=2/3/4:         UNKNOWN
balanced weight 14 excluded:               NO
weights 17,20,23 excluded:                 NO
d(ker_F3 A)>=24:                           UNKNOWN
rank-11 endpoint / Conway-99:              UNKNOWN
```

