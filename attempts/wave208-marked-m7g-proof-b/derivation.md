# Marked M7g spectral divisibility and the four-form residual

## 1. Conditional setting and notation

Assume a hypothetical prism-free rank-11 endpoint and a weight-eight word in
`A_Delta`.  Normalize its unique projective tensor relation on the canonical
`M7g` columns as

```text
a=(+1,+1,+1,+1,-1,-1,-1,-1).                    (1)
```

The labelled projective eight-set has four concurrent-secant perfect
matchings.  Nothing below chooses one of them.  Let `d_ij in {0,1,2}` be the
integer representative of the restricted polar product.  For distinct
selected graph triangles `T_i,T_j`:

- if they intersect, then `d_ij=1`;
- if they are disjoint, `d_ij` is their number of cross edges.

Product one therefore retains both meanings.  Put

```text
S_D=sum_(i<j) d_ij a_i a_j.                       (2)
```

Let `H` be the actual selected-triangle intersection graph and put

```text
h=sum_({i,j} in E(H)) a_i a_j.                    (3)
```

No automorphism is assumed.

## 2. An integer lift visible to the real spectrum

Use the same signs in (1) over the integers and define

```text
b~=B a in Z^99.                                   (4)
```

Each selected triangle has three points and `sum a_i=0`, so

```text
1^T b~=0.                                         (5)
```

Two selected triangles meet in at most one point.  Since
`B^T B` has diagonal three and off-diagonal one precisely on `H`,

```text
||b~||^2=24+2h.                                   (6)
```

The integer matrix `B^T A B` has diagonal six.  Its off-diagonal entry is
four for intersecting triangles: the common point is adjacent to the four
other triangle points, and the unique-common-neighbor law forbids another
cross edge.  For disjoint triangles it is their cross-edge count `d_ij`.
Consequently

```text
b~^T A b~
 =48+2(4h+S_D-h)
 =48+2S_D+6h.                                     (7)
```

The cancellation of `h` below is the key global step.

## 3. A divisible minus-four eigenvector

Define

```text
r=(A-3I)b~.                                       (8)
```

On the zero-sum space, the SRG identity gives

```text
(A-3I)(A+4I)=0.
```

Thus `Ar=-4r`.  Moreover the verified incidence bridge says
`A(Ba)=0` modulo three.  Hence every coordinate of `r` is divisible by
three and

```text
9 divides ||r||^2.                                (9)
```

Using `A^2=12I-A+2J`, (5)--(7) give

```text
||r||^2
 =b~^T(A-3I)^2b~
 =7(3||b~||^2-b~^TAb~)
 =7(24-2S_D).                                     (10)
```

Therefore

```text
S_D=3 mod 9.                                      (11)
```

This uses the real graph spectrum, all 99 modular equations through the
coordinatewise divisibility of (8), and no completion search.

## 4. Twenty-three of 27 forms fail (11)

The canonical `M7g` relation code has four projective weight-eight linear
relations, but only (1) satisfies the quadratic tensor relation.  This
distinction is checked explicitly; the other three linear words are not
substituted for the endpoint word.

For the unique tensor relation, exact reconstruction of the 27 restricted
forms gives

```text
S_D     number of forms       ||r||^2
-24             3               504
-12             4               336
  0            19               168
 12             1                 0.             (12)
```

The middle two rows violate (9).  Thus the divisibility theorem excludes 23
of 27 forms.  Wave 207 had already excluded four no-product-one forms, all
within those 23.  Relative to its 23 survivors, this removes 19 additional
forms and leaves exactly:

```text
diagonal parameters    rank    S_D    consequence
(0,0,1)                  4     -24    q=r/3, Aq=-4q, ||q||^2=56
(0,1,0)                  4     -24    q=r/3, Aq=-4q, ||q||^2=56
(1,0,0)                  4     -24    q=r/3, Aq=-4q, ||q||^2=56
(2,2,2)                  3      12    r=0, hence A b~=3b~.       (13)
```

This is a conditional four-form reduction, not an endpoint exclusion.

## 5. Complete marked-intersection residual

Every product-one graph in (13) is triangle-free.  Consequently an actual
selected intersection uses a pair-specific point; there is no hidden triple
intersection, and every subset census below is label-complete.

For each rank-four form, the product-one graph is `2C4`, with four same-sign
and four opposite-sign edges.  Enumerating all `2^8` labelled subsets and
imposing

```text
h=1 mod 3,
wt_F3(b~) in {14,17,20,23},
weight 14 implies sign composition 7+7
```

leaves 83 subsets per form.  The exact composition-refined profile is stored
in `exact-results.json`; its coarse `(same,opposite,weight,count)` rows are

```text
(1,0,23,4), (0,2,20,6), (2,1,20,24), (1,3,17,16),
(4,0,20,1), (3,2,17,24), (2,4,14,4), (4,3,14,4).
```

For the rank-three form, the product-one graph is
`K_(4,4)` minus a perfect matching and all 12 edges join opposite signs.
If `m` selected pairs actually intersect, then

```text
h=-m,
wt_F3(b~)=||b~||^2=24-2m.
```

The same code restrictions leave exactly

```text
m=2: weight 20, C(12,2)=66 labelled subsets;
m=5: weight 14, C(12,5)=792 labelled subsets.     (14)
```

## 6. Exact local controls and the wall

`local-controls.json` supplies one control for each row of (14).  Direct
checking gives:

```text
                         m=2 control   m=5 control
vertices                      22            19
edges                         53            44
point weight                  20            14
graph triangles               11            11
maximum induced degree         7             6
induced triangular prisms      0             0
```

Both controls realize every prescribed selected-pair cross count, satisfy
the exact induced equations

```text
A_U b~_U=3b~_U,
```

and obey the induced `lambda<=1`, `mu<=2` caps.  They are hostile controls,
not completions: the 77 or 80 outside vertices must still satisfy the missing
coordinates of `Ab~=3b~`, all degrees and common-neighbor equalities, and the
full 231-column endpoint frame.

The rigorous endpoint after this lane is therefore

```text
27 polar forms:             4 survive
rank-four residual:         three norm-56 integer -4 eigenvector branches
rank-three residual:        exact 3-eigenvector branches of weights 14 or 20
weight-eight word excluded: NO
rank-11 endpoint excluded:  NO
Conway-99:                  UNKNOWN
```

