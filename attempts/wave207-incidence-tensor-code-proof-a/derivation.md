# Incidence-linear weight-eight rigidity for the tensor code

## 1. Frozen setting and claim boundary

Work over `F_3`, conditionally on the prism-free rank-11 endpoint.  Let
`B` be the `99 by 231` point--triangle incidence matrix, let

```text
D=Z^* Z=B^T A B
```

be the centered Gram matrix of the 231 singular projective columns `z_T`,
and let

```text
A_Delta=im(B^T) intersect ker(a |-> D diag(a) D).
```

Wave 206 verified that `A_Delta` is nonzero, every nonzero word has weight
at least eight, and equality has support rank four with a split coefficient
form.  Everything below is `DERIVED`, not verifier-promoted.  No
automorphism is assumed.

The new point is that the `im(B^T)` hypothesis supplies a linear moment
which was not used in the Wave 206 relaxed weight-eight control.

## 2. Incidence membership kills the first centered moment

The strongly regular identity gives, over `F_3`,

```text
G=BB^T=A+I,
A G=A(A+I)=2J.
```

Every triangle has three points, so `B^T 1=0`.  Consequently

```text
D B^T
 =B^T A B B^T
 =B^T A G
 =2B^T J
 =0.                                                   (1)
```

Factor `D=Z^*Z` with `Z` of full row rank eleven.  The adjoint `Z^*` is
injective, so (1) implies

```text
Z B^T=0.                                               (2)
```

Thus every `a in im(B^T)`, and in particular every `a in A_Delta`, obeys

```text
sum_T a_T z_T=0.                                      (3)
```

This does not say that a quadratic tensor relation by itself is a linear
relation.  It says that the additional incidence membership in the
definition of `A_Delta` forces (3).

There is also a global linear zero frame.  Since `B 1_231=7*1_99=1_99`,

```text
D 1_231=B^T A 1_99=2B^T1_99=0,
```

and injectivity of `Z^*` gives

```text
sum_T z_T=0.                                          (4)
```

For `j in F_3`, put

```text
S_j=sum_(T:a_T=j) z_T,
R_j=sum_(T:a_T=j) z_T tensor z_T.
```

Equations (3)--(4), the tensor equation, and the global quadratic zero
frame give the two simultaneous three-class balances

```text
S_0=S_1=S_2,
R_0=R_1=R_2.                                         (5)
```

The second line is the verified Wave 206 balance.  The first line is the
new incidence-linear companion.

## 3. Equality forces exactly four coefficients of each sign

Suppose `a in A_Delta` has weight eight.  Let `V` be a `4 by 8` coordinate
matrix for its supported columns and let

```text
Lambda=diag(a_i).
```

Wave 206 gives `rank(V)=4`, while the tensor and linear relations give

```text
V Lambda V^T=0,
V Lambda 1=0.                                        (6)
```

The row space `U` of `V` is a four-dimensional totally isotropic subspace
of the nondegenerate coefficient space `(F_3^8,Lambda)`.  It is maximal,
so

```text
U=U^(perp_Lambda).
```

The second equation in (6) therefore puts `1` in `U`.  Since `U` is
isotropic,

```text
0=<1,1>_Lambda=sum_i a_i.                           (7)
```

Maximal isotropy also says that `Lambda` is split.  For a diagonal
eight-form over `F_3`, this means that the number `m` of entries equal to
`2=-1` is even.  Equation (7) says

```text
8+m=0 mod 3.
```

The only even `m` in `0..8` satisfying this is

```text
m=4.                                                (8)
```

Thus every target weight-eight word has composition

```text
(n_0,n_1,n_2)=(223,4,4).                            (9)
```

## 4. Affine moment formulation

Choose a row basis of `U` whose first row is `1`.  The eight projective
columns then have unique affine representatives

```text
v_i=(1,p_i),  p_i in AG(3,3).
```

Let `P` be the four `p_i` with coefficient one and `N` the four with
coefficient two.  Equation (6) becomes equality of all affine moments of
degree at most two:

```text
|P|=|N|=4,
sum_(p in P) p=sum_(n in N) n,
sum_(p in P) pp^T=sum_(n in N) nn^T.              (10)
```

The verified dual distance at least four says that no three supported
projective columns are dependent.  In this affine chart, no three of the
eight points are collinear.

Neither `P` nor `N` can be planar.  Suppose, for example, that an affine
linear form `ell` vanishes on `P`.  Applying (10) to `ell` and `ell^2`
shows

```text
sum_(n in N) ell(n)=sum_(n in N) ell(n)^2=0.
```

The second equality says that the number of points of `N` outside the
plane is `0 mod 3`, hence zero or three.  Zero would put all eight points
in one affine plane, contradicting `rank(V)=4`.  If it were three, the
first equality makes their three nonzero `ell`-values equal.  Applying
(10) to `ell*m` for every affine linear `m` says that those three points
have affine vector sum zero.  Three distinct points of `AG(3,3)` with sum
zero are collinear, again a contradiction.  Hence both signed four-sets
are affine bases.

## 5. The two tetrahedra are central reflections

The common affine centroid in (10) is well-defined because `4=1` in
`F_3`.  Translate it to zero and write the centered signed tetrahedra as
the columns of `3 by 4` matrices `X,Y`.  Then

```text
X1=Y1=0,
ker(X)=ker(Y)=<1>,
XX^T=YY^T=M.                                      (11)
```

The form `M` is nondegenerate: the row space of either matrix is
`1^perp` in `F_3^4`, and `1` has norm `4=1`, so the standard form is
nondegenerate on that hyperplane.

After ordering the second tetrahedron, (11) gives a unique
`H in O(M)` with `Y=HX`.  Permuting the four columns of `X` embeds the
tetrahedral group `S_4` in `O(M)`.  Its order is 24, while

```text
|O(3,3)|=2*3*(3^2-1)=48.
```

The central element `-I` is not in this `S_4`: otherwise the four-point
affine basis would be stable under negation and would be contained in the
span of at most two opposite pairs.  Hence

```text
O(M)=S_4 disjoint_union (-I)S_4.
```

If `H` lay in the first coset, the two signed point sets would be equal,
contrary to their disjoint supports.  Therefore `H` lies in the second
coset and

```text
N=-P                                                   (12)
```

as centered sets.

Undoing the translation, there is an affine point `m` and a pairing
`p_i <-> n_i` such that

```text
n_i-m=-(p_i-m).
```

For homogeneous representatives,

```text
(1,p_i)+(1,n_i)=2(1,m).
```

Thus the four projective secants `overline(z_(p_i),z_(n_i))` concur at the
same external point

```text
q=[(1,m)].                                           (13)
```

The point `q` is not one of the 231 selected columns, since otherwise a
secant would contain three selected projective points.  No three of the
four secant lines lie in a plane, because any three centered tetrahedron
directions are linearly independent.

This is the finite-geometric class called `M_7g` in Kaipa--Pradhan's
classification of rank-seven configurations on the ternary quadratic
Veronese three-fold.  Their classification is prior art for the support
orbit.  Equations (2), (8), and the applicability to the incidence
intersection code are derived here independently.

## 6. Forced short-circuit portfolio inside the support

The canonical representative is

```text
P={0,e_1,e_2,e_3},
N={(2,2,2),(1,2,2),(2,1,2),(2,2,1)},
```

with signs `+` on `P` and `-` on `N`.  The small exact checker evaluates
the 81 linear relations on these eight homogeneous columns.  Their weight
enumerator is

```text
1+24 y^4+16 y^5+32 y^6+8 y^8.                   (14)
```

In particular, the support contains

```text
12 projective weight-four circuits,
8 projective weight-five circuits.               (15)
```

Six of the weight-four circuits are the unions of two of the four paired
secants through `q`.  The eight quadratic Veronese columns have rank seven,
and their unique relation is the signed `4+4` word.

Equations (14)--(15) are a 81-word canonical calculation, not a search for
a graph.  They show in particular that a target weight-eight word is never
a matroid circuit; it carries a rigid portfolio of smaller circuits.

## 7. Restricting the endpoint polar form

Translate the concurrency point to `(1,0)` and write the restriction of
the ambient symmetric form to the support span as

```text
H=[[alpha,beta^T],[beta,C]].
```

Both `(1,p)` and `(1,-p)` are singular for each tetrahedron point `p`.
Subtracting their quadratic equations gives `beta*p=0` for four spanning
directions, hence `beta=0`.  The restriction is therefore block diagonal.

In the canonical tetrahedron, all such restrictions form a three-dimensional
space.  The exact checker evaluates its 27 elements.  Their ranks and the
orthogonality graph on the eight support points are

```text
rank(H)   number of forms   support orthogonality graph
0                1         K8
2               12         2 K4
3                8         4 K2
4                6         2 C4.                 (16)
```

At the prism-free endpoint, distinct triangle blocks have centered inner
product zero exactly when they are disjoint and have no cross edge.  Thus
(16) has the following graph-incidence translation:

```text
rank 0: all eight support triangles are mutually anticomplete;
rank 2: two four-sets are each mutually anticomplete;
rank 3: four anticomplete pairs are forced;
rank 4: the anticompleteness graph is two four-cycles.       (17)
```

The four concurrency-pair inner products are all equal.  They vanish
exactly when the concurrency point `q` is singular.

## 8. Sharp conditional conclusion

The present proof does not exclude all four patterns in (17).  Its exact
conclusion is the implication

```text
wt(a)=8 in A_Delta
 => composition (223,4,4)
 => an M_7g support of four concurrent external secants
 => the circuit portfolio (14)--(15)
 => one of the four anticompleteness patterns (17).          (18)
```

Consequently, proving that no signed `M_7g` configuration satisfying
(17) lies in `im(B^T)` for the actual 99-by-231 triangle incidence would
raise the verified minimum distance of `A_Delta` from eight to nine.

No such final incidence exclusion is proved here.  Rank 11, the
prism-free endpoint, `n3=4158`, `Q>=7060`, graph existence, and Conway-99
all remain unresolved.

## Prior-art note

Krishna Kaipa and Puspendu Pradhan, *Higher weight spectra of ternary codes
associated to the quadratic Veronese 3-fold*, arXiv:2405.12011 (2024),
later *Journal of Algebra and Its Applications* 24 (2025), article 2541007,
DOI `10.1142/S0219498825410075`.  Their rank-seven class `M_7g` is the
eight-point configuration whose four paired secants meet at an external
point and no three of the four lines are coplanar.
