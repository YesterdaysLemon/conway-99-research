# Tensor-balance words have weight at least eight

## 1. Frozen input and exact claim

Work over `F_3`.  The sealed Wave 206 Proof-B package conditionally forces a
nonzero word

```text
a in A_Delta,
sum_T a_T(z_T tensor z_T)=0,                     (1)
```

where the 231 centered columns are projectively distinct.  Wave 174
independently verifies that their true column code has dual distance at
least four.

This addendum audits only:

```text
wt(a)>=8.                                        (2)
```

It does not independently verify the existence theorem (1); that remains
a Wave 206 discovery claim pending the fresh integration verifier.

## 2. Removing the ambient form

Let the support of `a` have size `k`, enumerate it by `1,...,k`, and write

```text
a_i in {1,2},
Lambda=diag(a_1,...,a_k).
```

Let `V` be the matrix whose columns are the supported vectors `z_i`.
If the nondegenerate ambient form has matrix `F`, then the rank-one
self-adjoint operator `z_i tensor z_i` has matrix

```text
z_i z_i^T F.
```

Thus (1) is

```text
V Lambda V^T F=0.
```

The ambient form is invertible, so

```text
V Lambda V^T=0.                                  (3)
```

No assumption on the restriction of `F` to the span of the support is
used.  If `V=EX`, where the columns of `E` are any basis of that span, a
left inverse of `E` applied on both sides of (3) gives

```text
X Lambda X^T=0.                                  (4)
```

Hence degenerate support spans in the ambient orthogonal geometry do not
create an exception.

## 3. The coefficient-space Witt bound

All diagonal entries of `Lambda` are nonzero, so `Lambda` defines a
nondegenerate symmetric bilinear form on `F_3^k`.  Equation (4) says that
the row space of `X` is totally isotropic for this coefficient-space form.
Writing

```text
r=rank(V)=rank(X),
```

gives

```text
r<=WittIndex(Lambda).                             (5)
```

For any totally isotropic subspace `U` of a nondegenerate `k`-space,

```text
U subset U^perp,
dim(U)+dim(U^perp)=k.
```

Therefore

```text
2 dim(U)<=k,
WittIndex(Lambda)<=floor(k/2).                   (6)
```

Combining (5)--(6),

```text
r<=floor(k/2).                                   (7)
```

This is a coefficient-space argument.  It does not confuse the ambient
orthogonal form on the 11-space with `Lambda`.

## 4. Dual distance becomes a cap condition

The verified dual distance at least four says that every set of at most
three original centered columns is linearly independent.  In particular,
among the supported projective points:

```text
no three are collinear.                          (8)
```

Thus the `k` support points form a projective cap in their `r`-dimensional
vector span, namely in `PG(r-1,3)`.

The exact small cap maxima are

```text
vector rank r     projective space    maximum cap
1                 PG(0,3)                  1
2                 PG(1,3)                  2
3                 PG(2,3)                  4.     (9)
```

The checker exhausts all projective points:

```text
1 point in PG(0,3),
4 points in PG(1,3),
13 points in PG(2,3).
```

It independently obtains cap maxima `1,2,4`; there are 234 labelled
four-point caps in `PG(2,3)`.

## 5. Excluding every support through seven

For `k<=7`, equation (7) gives `r<=3`, so (9) applies.  Case by case:

```text
k     maximum r from (7)     cap maximum at that r
1              0                         0
2,3            1                         1
4,5            2                         2
6,7            3                         4.
```

In every row the cap maximum is strictly smaller than `k`.  Therefore no
nonzero tensor relation satisfying the inherited dual-distance condition
can have support at most seven.  This proves (2).

This use of dual distance is valid because it is applied to linear
dependence among the original `z_i`, not directly to the quadratic tensor
relation.  The earlier weight-four bound did not exploit the new
coefficient-space rank collapse (7).

## 6. Exact weight-eight boundary

If equality `k=8` occurs, then an eight-point cap cannot lie in vector rank
at most three by (9), while (7) gives rank at most four.  Hence

```text
r=4,
WittIndex(Lambda)=4.                              (10)
```

The coefficient form must be the split eight-dimensional form.  Over
`F_3`, with diagonal entries in `{1,2}`, this is equivalent to

```text
the number of coefficient-2 entries is even.     (11)
```

Thus a possible weight-eight word has coefficient-2 count

```text
0,2,4,6, or 8.
```

This parity condition is necessary, not sufficient for membership in
`A_Delta`.

## 7. Weight eight is sharp for the audited local ingredients

The checker constructs eight columns in `F_3^4`:

```text
e_1,e_2,e_3,e_4,
(0,1,1,1),
(1,0,1,1),
(1,1,0,1),
(1,1,1,2),
```

with coefficient vector

```text
(1,1,1,2,2,2,2,1).                              (12)
```

It verifies exactly:

```text
rank(V)=4,
every three columns are independent,
V diag(a)V^T=0,
WittIndex(diag(a))=4.
```

The same eight projective columns are singular for the nondegenerate
four-form

```text
[0 1 0 1]
[1 0 0 1]
[0 0 0 2]
[1 1 2 0],
```

whose determinant is one.  Appending a seven-dimensional complement of
determinant two embeds the control into a nondegenerate nonsquare
11-space.  The checker then verifies the rank-one self-adjoint operator
sum directly in that 11-space.

Therefore weight eight is attainable under all of the local ingredients:

```text
projective distinctness,
dual distance at least four,
singular columns,
nonsquare nondegenerate ambient 11-space,
the quadratic tensor relation.
```

The control is not a target endpoint realization.  It supplies only eight
columns, not the shared 231-column frame; it has no point--triangle
incidence or graph; and it does not show that its coefficient vector lies
in `im(B^T)`.  Consequently it blocks only an attempted proof of
`wt(a)>=9` from the audited local ingredients alone.

## 8. Status boundary

The safe strengthened conditional conclusion is:

```text
A_Delta !=0,
every nonzero a in A_Delta has wt(a)>=8,
and a weight-eight word, if present, spans dimension four and has an even
number of coefficient-2 entries.
```

Independent verification is still required.  No endpoint exclusion,
`n3` improvement, `Q>=7060`, graph construction, or Conway-99 resolution
follows.
