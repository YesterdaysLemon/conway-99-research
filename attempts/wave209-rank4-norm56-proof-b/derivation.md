# Rank-four norm-56 triangle reduction

## 1. Frozen conditional branch

Assume the frozen hypothetical prism-free rank-11 endpoint and one of the
three Wave 208 rank-four M7g forms.  Let `U=B_S` be the incidence matrix of
the eight selected triangles and let

```text
alpha=(+1,+1,+1,+1,-1,-1,-1,-1),
c=U alpha,
q=(A-3I)c/3.
```

The sealed input gives

```text
Aq=-4q,       q.q=56,       U^Tq=-3 alpha.          (1)
```

All statements below remain conditional on this branch.  The orchestrator
independently supplied the same triangle-variable reformulation after it had
been derived in this lane; every identity is reproduced here and checked
from (1).

## 2. The complete triangle-sum vector

Put

```text
t=B^Tq,       C=B^TB-3I.
```

Using `BB^T=A+7I` and (1),

```text
t.t=q^T(A+7I)q=168,
Bt=(A+7I)q=3q,
B^TBt=3t,
Ct=0.                                             (2)
```

The `-4` eigenspace is orthogonal to constants, so `sum(t)=7sum(q)=0`.
The eight marked entries are `-3alpha_i`; they have sum zero and squared norm
72.  Therefore the other 223 entries satisfy

```text
sum_(R outside S) t_R=0,
sum_(R outside S) t_R^2=96.                       (3)
```

Define the integral 231 by 231 matrix

```text
F=B^T(A-3I)B.
```

Its diagonal is `-3`.  For distinct blocks its entry is `0,1,2`: it is one
for intersecting blocks and otherwise equals the number of cross edges.  At
the prism-free endpoint every row has off-diagonal distribution
`0^32,1^162,2^36`.  A residual block with selected polar signature
`d=(F_Ri)_i` has

```text
t_R=(1/3) sum_i alpha_i d_i.                      (4)
```

The signature belongs to the 81-word rank-four evaluation code and its dot
product with `alpha` is divisible by three.  Thus (4) gives the exact alphabet

```text
t_R in {-2,-1,0,1,2}.                             (5)
```

The spectral action of `F` gives the exact moment identity

```text
F^2=-21F+252J.                                    (6)
```

Equation (6) supplies every selected-pair polar-product moment used in the
aggregate controls.

## 3. Projector saturation

On the triangle intersection graph, the zero-eigenspace projector is

```text
P_0=(J-F)/21.                                     (7)
```

For each of the three forms, the exact eigenvalue multiset of
`21 P_0[S,S]` is

```text
1, 3,3,3,3, 5,5, 9,
```

and `alpha` is a 9-eigenvector.  If a zero-eigenvector has marked values
`b=-3alpha`, the projector interpolation bound is

```text
||t||^2 >= b^T P_0[S,S]^{-1} b=168.               (8)
```

Equality holds in (2).  Hence the extension is the unique minimum-norm real
zero-eigenvector with those marked coordinates, and

```text
P_0[S,S]^{-1}b=-7alpha.
```

This recovers (4).  It also proves that the norm-168 test is sharp, so the
scalar line-sum moment cannot exclude any of the three forms.

The point-space `-4` projector has constant diagonal `44/99=4/9`.  Therefore

```text
q_x^2 <= (4/9)||q||^2=224/9<25,
q_x in {-4,-3,...,4}.                              (9)
```

## 4. Parity closes the norm-14 fork

Let `p=q mod 2`.  Reducing (1) gives

```text
Ap=0,             U^Tp=1_8.                       (10)
```

In particular `q` is not even: every marked triangle has odd sum.  Thus
`q/2` is not integral and the norm-14 complementary-Fano classification is
unavailable.  If `s=B^Tp=t mod 2`, then (2) gives

```text
Cs=0,             s_S=1_8.                        (11)
```

The pinned Wave 66 result gives `wt(p)>=8`.  Combining this import with (9),
`sum(q)=0`, and `q.q=56` leaves 800 integer value-count profiles, with odd
support weights `8,12,...,56`.  This is deliberately an arithmetic census,
not an eigenvector construction.

For a more relevant positive control, the checker solves the eight marked
line sums on the exact selected-union incidence pattern.  Every one of the
249 labelled branches has an explicit integer assignment with entries in
`[-4,4]`; the minimum selected-union norm ranges from 20 to 34, safely below
56.  These witnesses refute any parity-only or marked-line-only exclusion,
but they do not satisfy `Aq=-4q` outside the selected union.

## 5. The complete 99-point signature census

For a graph point `x` and selected triangle `T_i`, define

```text
s_i(x) = -1,  x in T_i,
          +1,  x outside T_i and adjacent to its unique T_i point,
           0,  otherwise.
```

The uniqueness in the second row follows from `lambda=1`.  Expanding the
definition of `q` gives the pointwise identity

```text
q_x=(1/3) sum_i alpha_i s_i(x).                   (12)
```

For each coordinate `i`, the 99 rows have exact counts

```text
s_i=-1: 3,       s_i=+1: 36,       s_i=0: 60.    (13)
```

The full pair table is also forced.  If `T_i,T_j` intersect, with rows and
columns ordered `-1,0,+1`, it is

```text
[ 1   0   2 ]
[ 0  40  20 ]
[ 2  20  14 ].                                    (14)
```

If they are disjoint and `d=D_ij` is their cross-edge count, it is

```text
[   0       3-d       d   ]
[ 3-d     39-3d    18+4d ]
[   d     18+4d    18-5d ].                       (15)
```

Indeed the `(-1,*)` and `(*,-1)` entries count triangle membership and cross
edges.  The remaining `(+1,+1)` entry follows from

```text
sum_x s_i(x)s_j(x)=18-7F_ij,
```

which is the off-diagonal entry of
`U^T(A-3I)^2U=18J-7F_S`; the margins then determine the rest.

There are exactly 2,187 signatures in `{-1,0,+1}^8` for which the numerator
in (12) is divisible by three.  For each of the 24 relabeling orbits, the
checker asks for nonnegative row counts satisfying (13)--(15), total 99,
`sum(q_x)=0`, and `sum(q_x^2)=56`.

The exact result is:

```text
17 orbits / 198 labelled branches: excluded,
 7 orbits /  51 labelled branches: integer census controls retained.   (16)
```

Every exclusion has an archived integer Farkas vector `y`.  The default
replay verifies over all 2,187 allowed signatures that

```text
A^T y >= 0,       b^T y < 0,                      (17)
```

so no nonnegative real census can satisfy the equations.  Numerical solver
status is not used as evidence.  For each survivor the archive instead gives
99 explicit integer signature rows and the checker replays every equation.

## 6. Exact 249-to-24 relabeling proof

Each form has exactly 83 accepted labelled intersection subsets.  The checker
enumerates the sign-preserving label permutations `S4 x S4` and retains a map
from a source form to a target form only when it preserves every polar entry:

```text
D_source[i,j]=D_target[pi(i),pi(j)].               (18)
```

There are exactly eight maps for each ordered pair of forms.  Acting with
these checked maps on all `3*83=249` branches gives 24 disjoint orbits, with
size distribution

```text
3^1, 6^9, 12^12, 24^2.                            (19)
```

This is not an automorphism assumption about the unknown graph.  It is only
an exact renaming of the eight marked triangle labels and their polar data.
The verifier reconstructs the full node set, proves disjoint coverage, and
transports and rechecks every witness on every labelled branch.

## 7. Residual aggregate equations and controls

For a residual triangle `R`, archive the pair `(d,h)`, where `d` is its
eight-coordinate polar signature and `h` is the set of selected triangles it
actually intersects.  Necessarily `h_i=1` only when `d_i=1`.  Because `R` has
three points, the graph induced by `H` on `h` is a matching and
`|h|-|E(H[h])|<=3`.

For every selected triangle `i`, the residual rows obey:

```text
# {R:i in h_R}=18-deg_H(i),
sum_(R:i in h_R) t_R=3 sum_(j:ij in H) alpha_j.    (20)
```

The second equation is the selected row of `Ct=0`.  For a selected pair:

```text
# {R:i,j in h_R} = 5,                              if ij in H,
# {R:i,j in h_R} = D_ij-|N_H(i) intersect N_H(j)|, otherwise.   (21)
```

The first case counts the five other blocks through a selected intersection
point.  The second uses the unique triangle on each cross edge and subtracts
selected common-neighbor triangles.  Equations (3)--(6), (20), and (21) form
99 exact integer aggregate equations.

`aggregate-controls.json` supplies a nonnegative integer census of 223
residual types for every orbit.  The default checker ignores solver status,
recomputes every allowed type and equation, transports each control through
(18), and verifies all 249 labelled branches exactly.

## 8. Unresolved boundary

The 198 exclusions in (16) are exact, but the 51 surviving branches are not
graphs.  Their controls do not couple the 99 point signatures to named points,
adjacency, or to 223 named residual blocks and their mutual intersection
graph.  In particular they do not impose:

1. the remaining 223 rows of `Ct=0`;
2. the decomposition of the 18-regular block-intersection graph into 99
   point-star `K7` cliques;
3. a 99-coordinate vector satisfying every row of `Aq=-4q`; or
4. all adjacency, `lambda=1`, `mu=2`, and prism-free equations.

The next exact problem is to couple the surviving point and triangle
signature controls to those graph equations or derive a contradiction.
Until then the branch and Conway-99 are `UNKNOWN`.
