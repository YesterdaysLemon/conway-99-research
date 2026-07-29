# Crossing localizers, star-compression coordinates, and a forced balanced tensor code

## 1. Frozen setting and status

Work over `F_3` on the conditional branch

```text
G is srg(99,14,1,2),
n3=4158, equivalently the induced triangular-prism count is zero,
rank(D)=11.
```

Let `B` be the `99 by 231` point--triangle incidence matrix.  Let `Z`
have the 231 centered triangle columns `z_T`, let `D=Z^*Z`, and put

```text
S_x=diag(B[x,*]),
P_x=-Z S_x Z^*,
M_x=D S_x D.
```

The inherited exact identities include

```text
D^2=0,
rank(Z)=11,
P_x^2=P_x,
rank(P_x)=6,
tr(P_x)=0,
sum_x P_x=0.
```

All claims in this package are `DERIVED` and await an independent Wave 206
verifier.  No automorphism is assumed.

## 2. The crossing feature

Because `D=Z^*Z`,

```text
M_x
 =Z^* Z S_x Z^* Z
 =-Z^*P_xZ.                                      (1)
```

The full row rank of `Z` makes the map

```text
A -> Z^* A Z
```

injective on endomorphisms of the 11-space.  Consequently,

```text
rank(M_x)=6,
dim span{M_x}=dim span{P_x}<=65.                 (2)
```

The upper bound is the dimension of the trace-zero self-adjoint operators
on an 11-space.

The square-zero centered frame gives

```text
D M_x=M_x D=0,
M_x M_y=0 for every x,y,
sum_x M_x=0.                                     (3)
```

For an ordered triangle pair `(T,U)`, define

```text
v_TU=D_T o D_U,
w_TU=B v_TU,
W[(T,U),x]=M_x[T,U].
```

Directly from the definitions,

```text
W[(T,U),x]
 =sum_R B[x,R]D[T,R]D[R,U]
 =w_TU[x].                                       (4)
```

Thus `W` is simultaneously the center-feature matrix of all `M_x` and the
matrix whose ordered-pair rows are the Wave 205 vectors `w_TU`.  Equations
(2)--(3) become

```text
rank(W)=dim span{P_x}<=65,
W 1=0,
W^T W=0.                                         (5)
```

The last identity is exact:

```text
(W^T W)_[x,y]
 =sum_(T,U) M_x[T,U]M_y[T,U]
 =tr(M_xM_y)
 =0.
```

Therefore the mutual-inner-product kernel

```text
L_cross=W W^T
```

is symmetric and square-zero:

```text
L_cross^2=0.                                     (6)
```

If `F[(T,U),R]=v_TU[R]` and `Q=B^TB`, then

```text
L_cross=F Q F^T,
L_cross[(T,U),(R,S)]=w_TU^T w_RS.                (7)
```

Wave 205's norm contraction is the diagonal specialization

```text
(K_D vec(Q))[(T,U)]=w_TU^T w_TU.                 (8)
```

Equations (5)--(7) are new structure on all mutual `w` products.  They do
not classify the restriction of `K_D` to `row(U)` and do not by themselves
exclude an endpoint.

## 3. Fixed-middle-center compression

Fix a graph point `y`, and let `E_y=im(P_y)`, a nondegenerate six-space.
For every center `x`, define the self-adjoint compression

```text
A_x^(y)=P_y P_x P_y restricted to E_y.           (9)
```

Then the Wave 206 three-center tensor is exactly the trace Gram

```text
Tau^(y)[x,z]
 =tau_(xy;z)
 =tr(P_xP_yP_zP_y)
 =tr(A_x^(y)A_z^(y)).                            (10)
```

The basic slice identities are

```text
A_y^(y)=I_(E_y),
sum_x A_x^(y)=0,
tr(A_x^(y))=g_xy,

Tau^(y)[x,x]=h_xy,
Tau^(y)[y,x]=g_xy,
Tau^(y)1=0,
rank(Tau^(y))<=21.                               (11)
```

The rank cap is the dimension

```text
dim self-adjoint End(E_y)=6*7/2=21.              (12)
```

It is only a Gram-rank cap.  Equality between the rank of `Tau^(y)` and the
dimension of the span of the operators `A_x^(y)` requires the restricted
trace form on that span to be nondegenerate; this need not hold.

## 4. The 21 localizer entries are exact compression coordinates

Label the seven triangle columns in the `y`-star by

```text
z_0,...,z_6.
```

They satisfy

```text
sum_i z_i=0,
<z_i,z_i>=0,
<z_i,z_j>=1 for i!=j,
P_y=-sum_i z_i tensor z_i=I_(E_y).               (13)
```

For a self-adjoint operator `A` on `E_y`, put

```text
N_A[i,j]=<z_i,A z_j>,
r_A[i,j]=N_A[i,j] for i<j.
```

Since the star columns sum to zero,

```text
N_A[i,i]=-sum_(j!=i)N_A[i,j].                    (14)
```

Thus the 21 off-diagonal entries `r_A[i,j]`, indexed by the edges of
`K_7`, determine the full symmetric matrix `N_A`.  They determine `A`
itself because the seven columns span `E_y`.  The exact checker constructs
the 21 coordinate operators and obtains coordinate-map rank 21.

Let `C` be the unsigned `7 by 21` vertex--edge incidence matrix of `K_7`.
Using `I=-sum_i(z_i tensor z_i)` twice gives

```text
tr(AB)
 =sum_(i,j) N_A[i,j]N_B[i,j]
 =r_A^T J_star r_B,                              (15)

J_star=C^T C+2I_21.
```

The checker finds

```text
rank(J_star)=21,
det(J_star)=2 in F_3.                             (16)
```

The trace and square are

```text
tr(A)=2 sum_(i<j) r_A[i,j],
tr(A^2)=r_A^T J_star r_A.                        (17)
```

Now return to the target localizer.  For two distinct `y`-star triangles
`T_i,T_j`,

```text
Q[T_i,T_j]=1,
M_x[T_i,T_j]= -<z_i,P_xz_j>.                     (18)
```

The diagonal is masked because `Q[T_i,T_i]=3=0`, and disjoint triangle
pairs are masked because their `Q` entry is zero.  Every distinct
intersecting triangle pair has a unique common point, so the 2,079
unordered supported coordinates of `Q o M_x` split canonically into 99
blocks of 21, one block for each middle point.

Define

```text
m_x^(y)[i,j]=M_x[T_i,T_j], i<j.                  (19)
```

The sign in (18) changes `r` to `-m`, so it cancels in every trace product.
Equations (15)--(17) give the exact graph-local formulas

```text
g_xy=sum_e m_x^(y)[e],

tau_(xy;z)
 =(m_x^(y))^T J_star m_z^(y),

h_xy
 =(m_x^(y))^T J_star m_x^(y).                    (20)
```

This is the main coordinate bridge.  Incidence determines which 21
entries belong to each middle point and the values of the `Q` mask.
Incidence does not yet determine the entries themselves, their
graph-type distributions, or the rank of a 21-row sample of compression
operators.  In particular, the fact that the 21 coordinate functionals
form a basis does not prove that 21 selected center compressions span the
operator space.

## 5. The characteristic-three radical and trace classes

The trace pairing on the full 21-dimensional self-adjoint operator space is
nondegenerate.  Its trace-zero hyperplane is

```text
I_6^perp,
dimension 20.
```

But in characteristic three,

```text
tr(I_6^2)=tr(I_6)=6=0.
```

Therefore

```text
rad(I_6^perp)=<I_6>,
rank(trace form restricted to I_6^perp)=19.       (21)
```

The checker verifies both values exactly and includes the hostile
one-feature example `span{I_6}`: its operator-span rank is one while its
trace Gram has rank zero.

There is nevertheless a safe conditional use of (21).  For fixed `y`,
take `k` centers with the same residue `g_xy`.  After subtracting one base
compression, the other `k-1` operators lie in `I_6^perp`.  Their difference
Gram, obtained by the same row/column differences from `Tau^(y)`, has

```text
rank<=19.                                         (22)
```

Among the 84 nonneighbors of `y`, one of the three `g` residues occurs at
least 28 times.  Its 27-by-27 difference Gram therefore has nullity at
least eight.

These are Gram nullities, not true operator relations.  The radical must
be controlled separately before a null word can be promoted.

## 6. A contracted global three-center matrix

Define

```text
Gamma[x,y]=tr((Q o M_x)M_y).                     (23)
```

Entrywise expansion gives

```text
Gamma=W^T diag(vec(Q)) W.                        (24)
```

Since `Q=sum_z s_zs_z^T`, where `s_z` is the `z`-star selector,

```text
Gamma[x,y]
 =sum_z tr(S_zM_xS_zM_y)
 =sum_z tr(P_xP_zP_yP_z)
 =sum_z Tau^(z)[x,y].                            (25)
```

Consequently,

```text
Gamma is symmetric,
rank(Gamma)<=65,
Gamma 1=0,
diag(Gamma)=H1.                                  (26)
```

Equation (25) is a full 99-by-99 sum-of-localizers identity.  It globalizes
all fixed-middle `tau` slices, but it leaves the diagonal `H1` free; a
square-zero or zero-row-sum theorem for `Gamma` does not force its diagonal
to vanish.

## 7. A forced nonconstant diagonal tensor-relation code

Let

```text
mathcal P:F_3^99 -> Sym_0(V),
mathcal P(c)=sum_x c_xP_x.
```

The target has dimension 65, so

```text
K_P=ker(mathcal P),
dim(K_P)>=34.                                    (27)
```

This is a true operator-relation kernel, not a Gram kernel.

Let

```text
L=ker(B^T).
```

For `c in L`,

```text
mathcal P(c)
 =-sum_T (B^Tc)_T(z_T tensor z_T)
 =0,
```

so `L` is contained in `K_P`.  The inherited simultaneous-star theorem
gives

```text
17<=dim(L)<=33.                                  (28)
```

Equations (27)--(28) force

```text
dim(K_P/L)>=1.                                   (29)
```

Equivalently, there is `c notin L` such that

```text
a=B^Tc !=0,
sum_T a_T(z_T tensor z_T)=0.                     (30)
```

This can be packaged as a finite intersection code.  Define the linear map

```text
Theta(a)=D diag(a)D
```

and

```text
A_Delta=im(B^T) intersect ker(Theta).             (31)
```

Because `rank(Z)=11`,

```text
Theta(a)
 =Z^* (sum_T a_T z_T tensor z_T) Z,
```

and the outer map is injective.  Hence (30) is equivalent to
`Theta(a)=0`.  Moreover,

```text
dim(A_Delta)
 =dim(K_P/L)
 =rank(B)-dim span{P_x}
 >=1.                                            (32)
```

The diagonal entries of `Theta(a)=0` give the weaker necessary condition

```text
(D o D)a=0.                                      (33)
```

The relation in (30) is not the already known constant zero frame.  Indeed,
suppose `B^Tc=lambda*1_231` with `lambda!=0`.  Summing the 231 block
equations and using `B1_231=7*1_99=1_99` gives

```text
sum_x c_x=lambda*231=0.
```

Put `G=BB^T=A+I`.  Then `Gc=lambda*1`, while

```text
G1=0,
G^2=G-J.
```

The first identity gives `G^2c=0`; the second gives

```text
G^2c=lambda*1-(sum c)1=lambda*1,
```

a contradiction.  Therefore

```text
im(B^T) intersect <1_231>={0},                   (34)
```

and every nonzero word in `A_Delta` is nonconstant.

There is also an exact three-class tensor balance.  Put

```text
R_j=sum_(T:a_T=j) z_T tensor z_T, j=0,1,2.
```

Equation (30) and the verified global frame zero give

```text
R_1+2R_2=0,
R_0+R_1+R_2=0.
```

Thus

```text
R_0=R_1=R_2.                                     (35)
```

The 231 triangle columns therefore admit a nonconstant, incidence-induced,
three-symbol partition whose three rank-one tensor sums are identical.
This is a concrete finite target for a complete or marked weight enumerator.

Projective distinctness of the columns implies

```text
wt(a)>=4.                                        (36)
```

The reason is that any one, two, or three distinct quadratic Veronese
columns `z_T tensor z_T` are linearly independent.  The checker exhausts
the universal span-at-most-three case over the 13 points of `PG(2,3)`.

The original centered-code dual-distance-four theorem cannot simply be
imported here: (30) is a relation among quadratic tensors, not necessarily
a linear relation among the original `z_T`.  No stronger weight or complete
composition bound is claimed.

Finally, `K_P` is a common true kernel:

```text
c in K_P
 =>sum_x c_x A_x^(y)=0 for every y
 =>c in ker(Tau^(y)) for every y
 =>c in ker(Gamma).                               (37)
```

At least one dimension of this common true kernel is not generated by the
incidence dependencies `L`.

## 8. Exact controls and what they do not prove

The checker has two separate controls.

First, 24 disjoint local simplexes in the correct nonsquare 11-space form a
full-rank zero frame.  On its 168 columns the checker replays

```text
D^2=0,
M_x=-Z^*P_xZ,
rank(M_x)=6,
W^TW=0,
Gamma=sum_y Tau^(y).
```

This is an algebra control only.  Its columns have incidence degree one,
not three, and it has no graph.

Second, a deterministic hostile construction has

```text
99 labelled rank-six projectors,
96 distinct projector matrices,
sum_x P_x=0,
every local projector generated by a J_7-I_7 singular simplex.
```

It yields

```text
rank(pair-trace Gram)=64,
rank(Tau^(y))=21 for every one of the 99 middle centers,
rank(Gamma)=64,
rank(H)=96,
H-row-sum residues 0^40 1^29 2^30.               (38)
```

Thus even maximal rank in every fixed-middle 21-dimensional slice does not
bound the global fourth-trace matrix by 21.

The control deliberately lacks the shared 231 projectively distinct
columns, degree-three point--triangle incidence, SRG, prism-free crossing
geometry, and endpoint code conditions.  It does not refute an identity
that uses those missing premises.

## 9. Boundary and next exact invariant

Wave 206 Proof B supplies two positive targets:

```text
the 21 supported entries of Q o M_x at a middle point are a complete
coordinate system for P_yP_xP_y;

A_Delta is a nonzero, nonconstant incidence-induced tensor-balance code.
```

The local coordinate theorem can accept graph-side fiber restrictions as
polynomial equations through (20), but a matching pattern alone does not
determine the coordinate values or a 21-by-21 sample determinant.

The remaining loss of information is now explicit.  Fixed-middle `tau`
compares compressions only inside one `E_y`.  The next global object is the
simultaneous compression map

```text
A -> (P_yAP_y restricted to E_y)_(y=1..99),
```

especially its kernel on `span{P_x}`.  A corresponding mixed four-center
tensor is

```text
tr((P_yP_xP_y)(P_vP_zP_v)), y!=v.                (39)
```

It compares compression data across two different middle centers and is
not determined by the individual `Tau^(y)` Gram slices.

No rank-11 exclusion, endpoint exclusion, `n3` improvement, `Q>=7060`,
construction of the target graph, or Conway-99 resolution follows.
