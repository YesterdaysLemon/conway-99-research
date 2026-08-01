# Exact norm divisibility for the M7g polar net

Claim label: `DERIVED` pending independent replay.

## 1. Integer matrices retain information lost modulo three

Let the columns of `U` be the ordinary zero-one incidence vectors of the
eight selected triangles.  Let `alpha_i=+1` when the corresponding ternary
coefficient is `1`, and `alpha_i=-1` when it is `2`.  The verified M7g
coefficient composition is four plus signs and four minus signs, hence

```text
sum_i alpha_i = 0.
```

Set

```text
K = U^T U,       R = U^T A U,       H = A U.
```

The diagonal entries of `K` and `R` are respectively three and six.  Let
`I` be the set of intersecting pairs among the eight selected triangles and
put

```text
s = sum_{ij in I} alpha_i alpha_j.
```

Distinct triangles meet in at most one point.  Therefore

```text
alpha^T K alpha = 24 + 2s.                         (1)
```

For disjoint triangles, let `q_ij` be their number of cross edges.  At the
prism-free endpoint it lies in `{0,1,2}`.  Intersecting triangles contribute
exactly four to `R_ij`: the shared point is adjacent to the other two points
of either triangle, while a further cross edge would violate uniqueness of
the triangle on an edge.  If `Q=R mod 3` is written with integer entries
`q_ij in {0,1,2}`, an intersecting residue-one entry is changed from its
representative one to the exact value four.  Define

```text
d(Q) = sum_{i<j} alpha_i alpha_j q_ij.
```

Then, without deciding which residue-one pairs intersect,

```text
alpha^T R alpha = 48 + 2d(Q) + 6s.                 (2)
```

## 2. The strongly regular identity gives a mod-nine obstruction

For parameters `(99,14,1,2)`,

```text
A^2 = 12 I - A + 2 J.
```

Every column of `U` has sum three, so `U^T J U=9J_8`.  Using
`sum alpha_i=0`, equations (1) and (2) give

```text
||H alpha||^2
  = alpha^T U^T A^2 U alpha
  = 12 alpha^T K alpha - alpha^T R alpha
  = 240 + 18s - 2d(Q).                             (3)
```

The point-code bridge says `H alpha=A U alpha` is zero modulo three.
It is an integer vector, so every coordinate is divisible by three and its
squared norm is divisible by nine.  The unknown intersection correction
`18s` is already divisible by nine.  Every actual polar form must therefore
satisfy the intersection-independent condition

```text
240 - 2d(Q) = 0 mod 9,                             (4)
```

equivalently `d(Q)=3 mod 9`.

This is the key gain over a purely ternary calculation: the exact entries
one and four are congruent modulo three but contribute the same correction
modulo nine in (3).

## 3. Complete labelled M7g evaluation

The checker starts from the eight published projective representatives

```text
(1,0,0,0), (1,0,0,1), (0,1,0,0), (0,1,0,1),
(0,0,1,0), (0,0,1,1), (1,1,1,1), (1,1,1,2)
```

and the unique quadratic relation

```text
(1,2,1,2,1,2,2,1).
```

It independently recovers all four relative column-sign classes for which
that same word is also linear.  For each class it reconstructs the
three-dimensional space of symmetric forms vanishing on the eight points
and checks all 27 affine forms.  No form is identified with its nonzero
scalar multiple, because the graph fixes the actual residue entries of
`R`, not merely their projective class.

For every one of the four sign classes the distribution of the remainder
`(240-2d(Q)) mod 9` is identical:

| form rank | zero graph | remainder distribution |
|---:|---|---|
| 0 | `K8` | one with remainder 6 |
| 2 | `2K4` | twelve with remainder 6 |
| 3 | `4K2` | six with remainder 6, one with 3, one with 0 |
| 4 | `2C4` | three with remainder 3, three with 0 |

Thus exactly four of 27 labelled forms survive in every orientation class:

* one rank-three `4K2` form with `d(Q)=12` and base norm `216`;
* three rank-four `2C4` forms with `d(Q)=-24` and base norm `288`.

The result eliminates 23 of the 27 polar forms as necessary endpoint data.

## 4. Boundary

The four surviving forms are not asserted realizable.  Equation (3) still
contains the unknown intersection sum `s`, and this package neither chooses
an intersection graph nor supplies the vertices outside the selected-triangle
union, whose size is not fixed here.  Conversely, the congruence alone does
not eliminate the survivors.  Therefore this is a
strict conditional reduction, not a global proof or counterexample, and the
Conway-99 status remains `UNKNOWN`.
