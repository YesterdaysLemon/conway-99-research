# Ternary adjacency-code bridge and a parameter-only distance floor

All calculations below are conditional on a hypothetical
`srg(99,14,1,2)`.  No graph is constructed.

## 1. The adjacency algebra over `F_3`

Over the integers,

```text
A^2=12I-A+2J.
```

Put `G=A+I` and `E=A+I-J`.  Reduction modulo three gives

```text
G^2=G-J,
AE=0,
E^2=E.
```

If `x in ker(A)`, then `0=1^T A x=14 sum(x)`, so `Jx=0` and
`Ex=x`.  Conversely `AE=0`.  Hence

```text
ker_F3(A)=im(E).
```

The previously verified rank is `54`, but the distance argument below does
not use the dimension.

## 2. A weight-eight block word has a nonzero point image

Let `a=B^T c` have four coefficients `1`, four coefficients `2`, and all
other coefficients zero.  Define `b=Ba`.  Since every point lies in seven
triangles,

```text
B 1=7*1=1                         over F_3.
```

Therefore

```text
sum(c)=sum(a)=4+2*4=0,
Jc=0.
```

The point--triangle Gram identity is `BB^T=A+I=G`, so

```text
b=Gc=(G-J)c=Ec,
Ab=0.                                             (1)
```

The zero-image caveat can now be removed rather than assumed away.  Indeed,

```text
a.a=c^T B a=c^T b=8=2.                           (2)
```

Thus `b` is nonzero.  Moreover,

```text
b.b=c^T G^2 c
   =c^T(G-J)c
   =c^T Gc
   =2.                                           (3)
```

For a ternary word, `b.b` is its Hamming weight modulo three.  Eight triangle
columns touch at most 24 point coordinates.  Equations (1)--(3) therefore
give the exact bridge

```text
b !=0,
b in ker_F3(A),
wt(b)<=24,
wt(b)=2 mod 3,
wt(b) in {2,5,8,11,14,17,20,23}.                 (4)
```

## 3. Signed neighbor moments

Let `x` be a nonzero word in `ker_F3(A)`, represented by entries in
`{0,1,-1}`.  Write

```text
P={u:x_u=1}, N={u:x_u=-1},
p=|P|, n=|N|, w=p+n.
```

For every vertex `v`, put

```text
i_v=|N(v) intersect P|,
j_v=|N(v) intersect N|.
```

The check equation at `v` says

```text
i_v=j_v mod 3.                                   (5)
```

Also `p-n=0 mod 3`.  Let `e_P,e_N,e_PN` count edges internal to `P`,
internal to `N`, and between the two sign classes.  Regularity and the
common-neighbor parameters give

```text
sum i_v=14p,                    sum j_v=14n,
sum C(i_v,2)=p(p-1)-e_P,
sum C(j_v,2)=n(n-1)-e_N,
sum i_v j_v=2pn-e_PN.                           (6)
```

The last three identities count common neighbors of signed pairs: an
adjacent pair has one and a nonadjacent pair has two.

## 4. Weights at most nine

For nonnegative `i,j` satisfying (5),

```text
F(i,j)=C(i,2)+C(j,2)+2ij-i-j >=0.                (7)
```

If both entries are positive this follows by monotonicity from `F(1,1)=0`.
If one is zero, the other is either zero or at least three by (5), and the
claim is `t(t-3)/2>=0`.

Summing (7) and using (6) gives

```text
0<=sum F
  =w^2+2pn-15w-(e_P+e_N+2e_PN).
```

Consequently

```text
15w<=w^2+2pn<=3w^2/2,
```

so a nonzero word must have `w>=10`.

## 5. Weight ten

The congruences `p+n=10` and `p-n=0 mod 3`, together with the preceding
inequality, leave only `p=n=5`.  Equality holds throughout, so the support is
independent and every local pair `(i_v,j_v)` is one of

```text
(0,0), (1,1), (3,0), (0,3).
```

All ten pairs inside `P` are nonadjacent and have two common neighbors.
Thus

```text
sum_v C(i_v,2)=20.
```

But every displayed local type contributes either zero or three to this
sum, a contradiction modulo three.

## 6. Weight eleven and the exact Farkas inequality

Up to replacing `x` by `-x`, the possible compositions are `(p,n)=(10,1)`
and `(7,4)`.  The first violates the inequality in Section 4.

For `(p,n)=(7,4)`, define for a vertex of membership `M in {P,N,O}`

```text
Phi_P(i,j)=-6i+12j+6i(i-1)-3j(j-1)+4ij,
Phi_N(i,j)=3-12i+5j+6i(i-1)-3j(j-1)+4ij,
Phi_O(i,j)=-12i+8j+6i(i-1)-3j(j-1)+4ij.
```

On the exact ranges

```text
P: 0<=i<=6, 0<=j<=4,
N: 0<=i<=7, 0<=j<=3,
O: 0<=i<=7, 0<=j<=4,
i=j mod 3,
```

each `Phi_M(i,j)` is nonnegative.  This is a finite residue-class check;
the exact checker records every value.  In unsimplified form this is the
following rational Farkas combination of (6) and the support handshakes:

```text
3*1_(v in N) -12i+8j
+12*(C(i,2)+1_(v in P)*i/2)
- 6*(C(j,2)+1_(v in N)*j/2)
+ 4*(ij+1_(v in P)*j).
```

Its sum over all 99 vertices is

```text
3n-12(14p)+8(14n)+12p(p-1)-6n(n-1)+8pn
=-60,
```

contradicting pointwise nonnegativity.  The swapped composition follows by
negating the codeword.  Therefore

```text
d(ker_F3 A)>=12.                                 (8)
```

Combining (4) and (8) leaves exactly

```text
wt(b) in {14,17,20,23}.                          (9)
```

## 7. Why the argument stops

The machine-readable weight-fourteen control satisfies all identities (5),
(6), the support handshakes, and aggregate equations obtained from the fact
that every neighborhood is `7K_2`.  It is nevertheless deliberately not
graphical: each sign class claims internal degree multiset
`[0,0,0,0,0,6,6]`.  A degree-six vertex would be adjacent to every peer, so
the five zero degrees are impossible.

This is useful only as a hostile boundary: the first/second moment and
aggregate local-matching equations do not by themselves prove the desired
distance 24.  It is not evidence for a low-weight codeword.

## 8. Status

```text
weight-eight point image nonzero:       DERIVED
weight-eight point-image choices:       {14,17,20,23}
parameter-only adjacency-code floor:    d>=12 DERIVED
d(ker_F3 A)>=24:                        UNKNOWN
weight-24 equality classification:      UNKNOWN
rank-11 endpoint / Conway-99:            UNKNOWN
```
