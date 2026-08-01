# Wave 207 proof B: simultaneous compression and the mixed four-center radical

## 1. Status and frozen setting

Claim label: `DERIVED`, pending independent verification.

Work over `F_3` on the conditional branch

```text
G is srg(99,14,1,2),
n3=4158, equivalently the induced triangular-prism count is zero,
rank_F3(D)=11.
```

Let `V` be the nondegenerate 11-space, let `P_x` be the verified rank-six
self-adjoint star projectors, and put `E_x=im(P_x)`.  The inherited identities
include

```text
P_x^2=P_x,
tr(P_x)=0,
sum_x P_x=0.
```

No automorphism, transitivity, or unverified constancy by graph type is used.
This package does **not** exclude the endpoint.  It proves an exact mixed-center
compatibility theorem, identifies the radical that separates mixed trace-Gram
nullity from true operator relations, and gives a 25-coordinate four-center
certificate that a future endpoint realization could satisfy or violate.

## 2. The simultaneous compression map and its adjoint

Let `Self(V)` be the 66-dimensional space of self-adjoint endomorphisms of
`V`, with trace pairing

```text
<A,B> = tr(AB).
```

The pairing is nondegenerate because the ambient form is nondegenerate and
the characteristic is not two.  Likewise, `Self(E_y)` has dimension 21 and
a nondegenerate full trace pairing.

Define

```text
C:Self(V) -> direct_sum_y Self(E_y),
C(A)_y=P_y A P_y restricted to E_y.               (1)
```

Embed `Self(E_y)` back into `Self(V)` by extending an operator by zero on
`E_y^perp`.  For `X_y` supported on `E_y`, cyclicity and `P_yX_yP_y=X_y`
give

```text
<P_yAP_y,X_y> = <A,X_y>.
```

Therefore

```text
C^*((X_y)_y)=sum_y X_y.                           (2)
```

Put

```text
J=sum_y Self(E_y) inside Self(V).
```

Equation (2) gives the exact kernel theorem

```text
ker C = J^perp.                                   (3)
```

Let `S=span{P_x}`.  Since `P_x` is the identity of `E_x`, extended by zero,
one has `S subset J`.  Hence

```text
ker(C restricted to S)
 =S intersect J^perp
 =S intersect rad(J).                             (4)
```

Thus a nonzero projector combination can be invisible to every compression
only by lying in the characteristic-three radical of the **true local
operator span** `J`.  This is stronger and more precise than a rank bound on
any trace Gram.

The normal operator is the Wave 205 sandwich map:

```text
C^*C(A)=Phi(A)=sum_y P_y A P_y.                   (5)
```

There is no positive-definite argument over `F_3`.  From `Phi(A)=0` one may
only infer that `C(A)` is orthogonal to `im(C)`.  It need not follow that
`C(A)=0`; the difference is exactly `rad(im(C))`.  Consequently `ker Phi`
must not be substituted for the true simultaneous-compression kernel.

If

```text
pi:F_3^99 -> S,  pi(c)=sum_x c_xP_x,
K_P=ker(pi),
K_C=ker(C pi),
```

then (4) gives the short exact sequence

```text
0 -> K_P -> K_C -> S intersect rad(J) -> 0,       (6)
```

where the last map is `c |-> pi(c)`.  Thus `K_C=K_P` precisely when no
nonzero element of `S` lies in `rad(J)`.

## 3. Every trace Gram has one exact radical defect

The following elementary lemma is the bookkeeping device needed throughout.

### Gram-radical exact sequence

Let `R:F_3^m -> W` be any synthesis map into a space with a nondegenerate
bilinear form, let `F=im(R)`, and let

```text
G_ij=<R(e_i),R(e_j)>.
```

Then

```text
0 -> ker(R) -> ker(G) -> rad(F) -> 0,             (7)
```

where the last map sends `c` to `R(c)`.

Indeed, `Gc=0` says exactly that `R(c)` is orthogonal to every element of
`F`.  Since `R(c)` is already in `F`, it lies in `rad(F)`.  Every radical
element has a preimage, and the kernel of the last map is `ker(R)`.  In
particular,

```text
rank(R)-rank(G)=dim rad(F).                       (8)
```

This proves, rather than merely warns, how many Gram-null directions fail to
be true operator relations.

## 4. Fixed slices, the mixed tensor, and the kernel ladder

Define the sandwich features

```text
F_yx=P_yP_xP_y,
F_y=span_x{F_yx},
F=span_(y,x){F_yx}.                               (9)
```

The fixed-middle tensor is the Gram of the `y`-slice synthesis

```text
R_y(c)=sum_x c_xF_yx=P_y pi(c) P_y,
Tau^(y)[x,z]=tr(F_yxF_yz).                        (10)
```

Applying (7) gives the exact identity

```text
ker(Tau^(y))/ker(R_y) isomorphic to rad(F_y).     (11)
```

Thus the difference between the true coordinate rank of the `y`-slice and
the rank of `Tau^(y)` is not evidence for more operator relations; it is the
dimension of the restricted trace radical.

Now define the mixed four-center tensor

```text
M[(y,x),(v,z)]
 =tr((P_yP_xP_y)(P_vP_zP_v))
 =tr(F_yxF_vz).                                   (12)
```

It is the complete trace Gram of the global sandwich synthesis

```text
R_all(e_(y,x))=F_yx.
```

Hence (7) gives

```text
ker(M)/ker(R_all) isomorphic to rad(F),
rank(R_all)-rank(M)=dim rad(F).                   (13)
```

This is the first exact cross-middle-center compatibility law: the mixed
tensor removes every slice-local false kernel except the directions that
remain radical in the **global** sandwich span.

For center coefficients, define

```text
K_mix={c:
  sum_x c_x M[(y,x),(v,z)]=0 for every y,v,z},

K_tau=intersection_y ker(Tau^(y)).                (14)
```

Equations (10)--(14) give

```text
K_P subset K_C subset K_mix subset K_tau.         (15)
```

More precisely:

- `c in K_tau` iff every `R_y(c)` lies in `rad(F_y)`;
- `c in K_mix` iff every `R_y(c)` lies in `rad(F)`;
- `c in K_C` iff every `R_y(c)` is the zero operator.

Because `P_x=F_xx`, one has `S subset F subset J`.  If `rad(F)=0`, then
`K_mix=K_C`.  Moreover an element of `S intersect rad(J)` lies in `F` and
is orthogonal to `F`, so it lies in `rad(F)`; equations (6) and (15) then
give the stronger conclusion

```text
rad(F)=0  =>  K_P=K_C=K_mix.                     (16)
```

The condition in (16) must be checked by comparing a true operator-coordinate
rank with the mixed Gram rank.  Mere nullity of `M` is expected, because
there are `99^2` labelled features in a 66-dimensional space.

## 5. Exact star-coordinate bridge across different centers

Let `Z_y` be the seven-column singular simplex of the `y`-star and put

```text
C_yv=Z_y^* Z_v,
R_x^(y)=Z_y^* P_x Z_y.                            (17)
```

The inherited simplex identities give

```text
Z_y 1=0,
C_yv 1=C_yv^T 1=0,
R_x^(y)=R_x^(y)^T,
R_x^(y)1=0.
```

Also

```text
F_yx=Z_y R_x^(y) Z_y^*.                           (18)
```

Substituting (18) into (12) gives the promised cross-center coordinate law

```text
M[(y,x),(v,z)]
 =tr(R_x^(y) C_yv R_z^(v) C_vy).                 (19)
```

For `y=v`, `C_yy=J_7-I_7`, and (19) reduces to the verified fixed-middle
`J_star` formula.

The 21 off-diagonal entries of a symmetric `7 by 7` matrix `R` satisfying
`R1=0` determine its diagonal.  Hence

```text
R_space={R=R^T:R1=0}
```

is a 21-dimensional model of `Self(E_y)`.  For any cross matrix `C` with
`C1=C^T1=0`, define

```text
B_C(R,S)=tr(R C S C^T).                           (20)
```

Let `d=rank(C)`.  The congruence map

```text
S |-> C S C^T
```

has image equal to the symmetric square of the `d`-dimensional image of
`C`.  Characteristic three is odd, so its rank is

```text
rank(B_C)=binom(d+1,2).                           (21)
```

Equivalently, if `d_yv=rank(C_yv)=rank(P_y restricted to E_v)`, then the
full `21 by 21` transition pairing between `Self(E_y)` and `Self(E_v)` has

```text
d_yv     0  1  2  3   4   5   6
rank     0  1  3  6  10  15  21.                 (22)
```

The exact checker constructs canonical matrices of every rank and replays
(21).  At `d=6`, the transition is a perfect pairing; at `d<6`, its left
and right radicals are genuine transition losses of dimensions
`21-binom(d+1,2)`.

Equation (21) is useful only with the true slice span.  A full-rank transition
to a center whose features span a proper or degenerate subspace does not
detect all 21 coordinates.

## 6. Why four middle centers are the first possible full certificate

Each middle-center row of sandwich features lies in the 21-dimensional
space `Self(E_y)`.  Therefore three middle centers contribute at most

```text
3*21=63<66=dim Self(V).                            (23)
```

Four are the first number that can span every self-adjoint operator.  If a
mixed Gram submatrix using features from four middle-center rows has rank
66, then its feature span has dimension at least 66 and hence equals
`Self(V)`.  Its trace restriction is automatically nondegenerate.  It follows
that

```text
rank_ F3(M on four middle rows)=66
 => the four compressions are jointly injective
 => rad(F)=0
 => K_P=K_C=K_mix.                               (24)
```

This is an exact, finite certificate: one nonsingular `66 by 66` mixed
minor suffices.  No endpoint artifact currently supplies such a minor.

## 7. A 25-coordinate normal form for a four-center certificate

There is a smaller equivalent certificate when two star spaces already
span `V`.  Let

```text
U=E_y, W=E_v,
U+W=V,
L=U intersect W, dim(L)=1.
```

Choose complements

```text
U=L direct_sum U_0,
W=L direct_sum W_0,
dim(U_0)=dim(W_0)=5.
```

A symmetric bilinear form `b` that vanishes on both `U` and `W` has `L` in
its radical and only a cross block between `U_0` and `W_0`.  It is therefore
determined by one matrix

```text
K in Mat_(5 by 5)(F_3).                           (25)
```

This proves

```text
dim(Self(U)+Self(W))=41,
dim(Self(U)+Self(W))^perp=25.                    (26)
```

Write the six basis columns of another star space `E_s` relative to
`L direct_sum U_0 direct_sum W_0` as

```text
[ell_s]
[ X_s ]
[ Y_s ],
```

where `X_s,Y_s` are `5 by 6`.  The condition that the form (25) vanish on
`E_s` is exactly

```text
X_s^T K Y_s + Y_s^T K^T X_s=0.                  (27)
```

For two more centers `s,t`, stack their two systems (27).  The resulting
linear map

```text
Lambda_(s,t):Mat_5(F_3) -> Sym_6(F_3)^2          (28)
```

has rank 25 iff the four local symmetric squares span `Self(V)`, iff the
four-center compression map is injective.  Thus (28) is a compact
25-coordinate version of the rank-66 certificate (24).

### Exact sharpness control

The checker shows that rank 25 is algebraically attainable without a search.
Take

```text
E_y=L direct_sum U_0,
E_v=L direct_sum W_0,
E_s=L direct_sum graph(I_5),
E_t=L direct_sum graph(B),
```

where `B` is the companion of the irreducible polynomial

```text
p(t)=t^5+2t^4+1.
```

The `E_s` equation makes `K` alternating.  The `E_t` equation then becomes

```text
K B=B^T K.                                       (29)
```

If a nonzero `K` satisfied (29), its kernel would be `B`-invariant.
Irreducibility forces `K` to be invertible.  But every alternating `5 by 5`
matrix in odd characteristic is singular, a contradiction.  Hence `K=0`.

The checker independently verifies the Rabin irreducibility identities,
the restriction rank 25, and cumulative symmetric-square ranks

```text
21, 41, 56, 66.
```

All four abstract six-spaces are nondegenerate for the standard form.  This
is an algebra control only: the ambient form has the wrong discriminant, and
there are no 99 stars, seven-column singular simplexes, shared 231 columns,
incidence matrix, SRG, or prism-free graph.  It proves the certificate is
not dimensionally impossible; it does not establish it at the endpoint.

## 8. Characteristic-three radical audit

The full trace form on `Self(E_y)` is nondegenerate.  Nevertheless

```text
tr(I_6^2)=tr(I_6)=6=0 in F_3.                    (30)
```

The trace-zero hyperplane is `I_6^perp`, contains `I_6`, and has

```text
dimension 20,
radical <I_6>,
trace-Gram rank 19.                              (31)
```

The checker realizes all 20 true independent trace-zero features.  Their
Gram has rank 19, so it has one null word although the synthesis has no
relation.  Adding one trace-nonzero feature raises both synthesis and Gram
rank to 21 and detects `I_6`.  This is an exact hostile control against
promoting trace-Gram nullity to an operator kernel.

By contrast, on the 11-dimensional ambient space,

```text
tr(I_11^2)=11=2 !=0 in F_3.
```

Therefore the 65-dimensional ambient trace-zero self-adjoint space is
nondegenerate.  The projector span `S` lies in a nondegenerate ambient
space, but its own restriction, the slice spans `F_y`, the global sandwich
span `F`, and `J` may still have radicals.  Equations (6), (11), and (13)
keep these four notions separate.

## 9. The `A_Delta` functorial obstruction

There is an important correction to the Wave 206 scope wall.  If

```text
a=B^T c,
```

then the verified star relation `BD=0` gives

```text
D a=D B^T c=0.                                   (32)
```

Because `D=Z^*Z`, `Z` has full row rank 11, and the ambient form is
nondegenerate, `ker(D)=ker(Z)`.  Thus

```text
Z a=0.                                           (33)
```

So every `A_Delta` word is also a true relation among the original centered
columns; the earlier warning that this need not hold was too weak.

For `a in A_Delta`, the quadratic equation `Theta(a)=0` and injectivity of
`A |-> Z^*AZ` give

```text
pi(c)=sum_x c_xP_x
     =-sum_T a_T(z_T tensor z_T)
     =0.                                         (34)
```

Equations (10) and (12) now imply, functorially,

```text
sum_x c_xF_yx=P_y pi(c)P_y=0,                    (35)

sum_x c_xM[(y,x),(v,z)]
 =tr(P_y pi(c)P_y F_vz)=0                        (36)
```

for every `y,v,z`.

Therefore linear sandwich maps and every mixed trace Gram obtained from
them **cannot classify or exclude an already true `A_Delta` relation**.
Such a relation lies in the true synthesis kernel, not in the radical defect
that mixed centers repair.  Any exclusion must use information nonlinear in
the relation, or graph-typed restrictions on its coefficient coloring,
support, star incidences, or individual compression coordinates.

This package deliberately does not repeat the separate weight-eight
enumeration route.

## 10. Boundary and next exact invariant

The positive result is the exact compatibility package

```text
mixed trace-Gram defect = global sandwich-span radical,
rank transition(y,v)=binom(rank(C_yv)+1,2),
four centers are the first possible full certificate,
and a full-span pair reduces that certificate to 25 exact coordinates.
```

The endpoint would advance if actual shared-incidence data proved either

```text
a rank-66 mixed Gram minor from four middle centers,
```

or, on a full-span star pair, a rank-25 system (28) for two further actual
stars.  Neither rank is presently established.  The abstract sharpness
control is not an endpoint model.

No rank-11 exclusion, endpoint exclusion, strict `n3` improvement,
`Q>=7060`, graph construction, or Conway-99 resolution follows.  The status
remains `UNKNOWN`.
