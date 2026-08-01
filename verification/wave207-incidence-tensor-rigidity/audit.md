# Wave 207 incidence--tensor rigidity: hostile verifier audit

## Scope and verdicts

This audit was performed from the source-blind protocol whose SHA256 is
`e381877375f1f5f270e7ad064db570494a7df12dc0bbf01a0df0d24b67884444`.
No Wave 207 discovery artifact was opened before that protocol was written
and hashed.  The verifier then inspected the discovery packages, replayed
their exact checks, inspected the primary geometric source, and implemented
a separate standard-library-only finite-field checker that imports no Wave
207 discovery module.

| Claim | Verdict | Scope |
|---|---|---|
| C1: `a in A_Delta` implies `Da=Za=0` | `VERIFIED` | Conditional endpoint identities; in fact tensor-kernel membership is unnecessary |
| C2: weight eight is `4+4` and has M7g support | `VERIFIED` | Conditional on the sealed rank-four/cap premises |
| C3: relation enumerator and four polar graph types | `VERIFIED` | Complete canonical M7g enumeration |
| C4: Gram-radical sequence, transition rank, and linear-feature boundary | `VERIFIED` | Abstract finite-field theorem plus conditional projector application |
| C5: no endpoint/global conclusion | `VERIFIED` | Global status remains `UNKNOWN` |
| Point-code image and rank-zero/no-one exclusions | `VERIFIED` | Conditional on a hypothetical weight-eight `A_Delta` word |
| Parameter-only `d(ker_F3 A)>=12` | `VERIFIED` | Any hypothetical `srg(99,14,1,2)` |
| Weight-14 sign composition is necessarily `7+7` | `VERIFIED` | Conditional existence; weight 14 itself remains open |
| Rank-four 23-vertex certificate | `VERIFIED` as restricted data | Necessary-condition model only; not a graph completion |

No frozen mathematical claim is refuted.  Two precision findings and one
documentation count error are recorded below rather than silently repaired.

## C1. Incidence membership supplies the missing linear relation

The matrix orientations are:

```text
B: 99 x 231,       G=BB^T=A+I: 99 x 99,
D=B^T A B=Z^*Z: 231 x 231,     Z: F_3^231 -> V, dim(V)=11.
```

The strongly regular identity gives `AG=2J` over `F_3`, and every triangle
has three points, so `B^T 1=0`.  Therefore

```text
D B^T = B^T A B B^T = B^T A G = 2 B^T J = 0.
```

Thus `Da=0` for every `a in im(B^T)`, not merely for the intersection with
the tensor kernel.  At the endpoint, `Z` has full row rank and the form on
`V` is nondegenerate.  Hence the adjoint `Z^*:V->F_3^231` is injective.
From

```text
0=Da=Z^*(Za)
```

one obtains `Za=0`.  This exactly corrects the Wave 206 caveat: a generic
quadratic tensor relation still need not be a linear centered-column
relation, but incidence membership forces one.

The hypotheses are essential.  With a degenerate one-dimensional ambient
form, `Z=[1]` gives `Z^*Z=0`, so `Da=0` does not imply `Za=0`.  Even with a
nondegenerate hyperbolic plane, a nonsurjective synthesis whose image is an
isotropic line gives the same failure.  Full row rank and ambient
nondegeneracy rule out precisely these cases.

Separately, `B1_231=7*1_99=1_99`, so
`D1_231=B^TA1_99=2B^T1_99=0`; adjoint injectivity then gives `Z1=0`.
Together with `Za=0` and the quadratic relations, this yields both class
balances `S_0=S_1=S_2` and `R_0=R_1=R_2`.

## C2. Weight-eight composition and M7g applicability

Let `V` be a `4 x 8` coordinate matrix for the supported centered columns
and `Lambda=diag(a_i)`.  The sealed Wave 206 result gives `rank(V)=4` and a
split coefficient form; C1 and the tensor equation give

```text
V Lambda 1=0,       V Lambda V^T=0.
```

The row space `U` is a four-dimensional maximal totally isotropic subspace
of the nondegenerate eight-dimensional coefficient form.  Hence
`U=U^(perp_Lambda)`.  The first equation puts `1` in `U`, and isotropy gives
`sum_i a_i=0`.  If `m` coefficients equal `2`, splitness says `m` is even,
while

```text
sum_i a_i = (8-m)+2m = 8+m = 0 mod 3.
```

The unique even solution in `0..8` is `m=4`.  The composition is therefore
exactly four `1`s and four `2`s; this is invariant under global sign swap.

For the geometric classification:

1. Wave 206 gives vector rank four, and the sealed Wave 174 dual-distance
   result makes every three support columns independent.  The support is an
   eight-cap in `PG(3,3)`.
2. The tensor relation gives Veronese rank at most seven.  Rank at most six
   would give two independent tensor relations; eliminating one coordinate
   would produce a nonzero relation of support at most seven, contrary to the
   sealed universal Witt-plus-cap bound.  The Veronese rank is exactly seven.
3. Kaipa--Pradhan Lemma 3.3 supplies the unique maximal rank-seven closure,
   and their Lemma 6.1 lists `M7a,...,M7g`.  The cap maxima of the first six
   closures are at most `5,6,6,6,6,7`; only the eight-point `M7g` closure can
   contain the support.

The primary-source line mapping and retrieval hashes are recorded in
`literature-source-audit.md`.  No automorphism assumption enters.

The clean-room checker examined all `105` labelled perfect matchings and all
`40` points of `PG(3,3)`.  It found four valid concurrent-secant
decompositions of the labelled representative.  Each decomposition has one
common external point and every triple of its four lines spans the whole
four-dimensional vector space.  This is a precision finding: the published
uniqueness is the unique projective M7g class/closure, not a unique internal
pairing of a labelled eight-set.  The frozen claim, phrased as a unique M7g
orbit with existence of four paired secants, remains verified.

## C3. Complete canonical enumerations

The verifier-owned `independent_check.py` records an explicit published M7g
representative, verifies column rank four, independence of every triple,
Veronese rank seven, and one-dimensional quadratic-relation space, and finds
the signed `4+4` relation.

The linear kernel has dimension four.  Exhausting all `3^4=81` words gives

```text
weight 0: 1,   weight 4: 24,   weight 5: 16,
weight 6: 32,  weight 8: 8,
```

which is exactly

```text
1 + 24 y^4 + 16 y^5 + 32 y^6 + 8 y^8.
```

The three-dimensional space of symmetric forms vanishing on the eight
points has `27` affine elements.  Direct row reduction and simple-graph
invariants give:

| Form rank | Affine forms | Projective nonzero forms | Polar zero graph |
|---:|---:|---:|---|
| 0 | 1 | -- | `K8` |
| 2 | 12 | 6 | `2K4` |
| 3 | 8 | 4 | `4K2` |
| 4 | 6 | 3 | `2C4` |

Every graph was checked by edge count, degree sequence, component sizes, and
connectivity, not only by a name.  Column rescaling and point reordering
preserve the relation weight enumerator and polar zero graphs.  There are
four relative column-sign classes (modulo global sign) for which the
quadratic `4+4` relation is also linear; all four were enumerated.

## C4. Gram radicals, transitions, and the obstruction boundary

For a synthesis map `R:F_3^m->W` into a nondegenerate bilinear space, put
`F=im(R)` and let `G` be the coordinate Gram matrix.  The proposed sequence
is

```text
0 -> ker(R) -> ker(G) --R--> rad(F) -> 0.
```

It is exact: `Gc=0` is equivalent to `R(c)` being orthogonal to every vector
of `F`, while `R(c)` already lies in `F`; every radical vector has a
preimage; and the kernel of the displayed restriction of `R` is exactly
`ker(R)`.  Consequently

```text
rank(R)-rank(G)=dim(rad(F)).
```

The clean-room checker exhausted all `3^6=729` synthesis matrices
`F_3^3->F_3^2` against the nondegenerate form `diag(1,2)`, including
nontrivial radical examples, and verified the sequence by exact set images
and kernel cardinalities.

For Proof B's simultaneous compression

```text
C:Self(V)->direct_sum_y Self(E_y),
C(A)_y=P_y A P_y|E_y,
```

the adjoint extends local operators by zero and sums them.  If
`J=sum_y Self(E_y)`, then `ker C=J^perp`.  With
`pi(c)=sum_x c_xP_x`, `S=im(pi) subset J`,
`K_P=ker(pi)`, and `K_C=ker(C pi)`, the map `c |-> pi(c)` gives the fully
specified exact sequence

```text
0 -> K_P -> K_C -> S intersect rad(J) -> 0.
```

For a transition matrix of rank `d`, invertible row and column changes
reduce it to `diag(I_d,0)`.  The congruence map on symmetric matrices then
has image `Sym_d`, of dimension `d(d+1)/2`.  The argument is valid in odd
characteristic; the clean-room calculation gives ranks

```text
d:       0  1  2  3   4   5   6
rank:    0  1  3  6  10  15  21
```

and also passes rectangular `4x6`, `6x4`, and `3x7` edge cases.  The
independent abstract four-center control reproduces cumulative symmetric
square ranks `21,41,56,66`, the `25`-coordinate restriction rank, and four
nondegenerate local six-spaces.  These are algebraic sharpness controls, not
endpoint data.

Finally, if `pi(c)=0`, then for every fixed center `y`

```text
sum_x c_x P_y P_x P_y = P_y pi(c) P_y = 0,
```

and tracing against any fixed mixed feature also gives zero.  Therefore all
features that factor linearly through these sandwiches annihilate every true
projector relation.  Nonlinear or relation-dependent features are outside
this statement.  The result is a verified method boundary: these linear
features cannot themselves exclude an `A_Delta` relation.

## Supplemental incidence and point-code consequences

For a hypothetical weight-eight word write `a=B^Tc`, `b=Ba`, and
`G=A+I`.  Since `B1=7*1=1` and `sum a=0`, one has `sum c=0`.  Also

```text
a.a=8=2,
b=Gc,
Ab=AGc=2Jc=0,
b.b=c^T G^2 c=c^T(G-J)c=c^TGc=2.
```

Thus `b` is nonzero and its ternary Hamming weight is `2 mod 3`.  It is
supported on the union of eight triangles, of size at most `24`, so

```text
wt(b) in {2,5,8,11,14,17,20,23}.
```

The rank-zero polar form has `D_ij=0` for every distinct support pair.
At the prism-free endpoint this forces eight pairwise disjoint triangles
with no cross edges.  Their union has 24 vertices and every coordinate of
`b` there is nonzero, so `b.b=24=0`, contradicting `b.b=2`.  The rank-zero
`K8` case is excluded.

More generally, with `B_S` the eight selected incidence columns,

```text
b.b=a^T(B_S^T B_S)a
   =2 sum_(i<j, T_i intersects T_j) a_i a_j
   =2.
```

An intersection can occur only at a restricted Gram entry equal to one.
Hence a restricted form whose off-diagonal entries contain only `0` and `2`
is impossible.  For each of the four relative sign classes, exact
enumeration finds the zero form and exactly three of the twelve rank-two
affine forms with no entry one.  Thus exactly `4/27` forms are excluded per
normalization: the rank-zero form and three rank-two forms.  This does not
exclude every rank-two zero graph; scalar partners and the other forms can
contain product-one pairs.

## Parameter-only adjacency-code floor

For any nonzero `x in ker_F3(A)`, write its signs as positive set `P` and
negative set `N`, with sizes `p,n`, and let `i_v,j_v` count positive and
negative neighbors.  Since `14` is nonzero in `F_3`,
`0=1^TAx=14 sum(x)` also gives `p-n=0 mod 3`.  The SRG equations give

```text
i_v=j_v mod 3,
sum i_v=14p,                    sum j_v=14n,
sum C(i_v,2)=p(p-1)-e_P,
sum C(j_v,2)=n(n-1)-e_N,
sum i_v j_v=2pn-e_PN.
```

The pointwise function

```text
F(i,j)=C(i,2)+C(j,2)+2ij-i-j
```

is nonnegative whenever `i,j>=0` and `i=j mod 3`.  Summing it gives

```text
15w <= w^2+2pn <= 3w^2/2,
```

excluding weights at most nine.  At weight ten the only composition that
can attain equality is `(5,5)`; equality forces an independent support and
local types `(0,0),(1,1),(3,0),(0,3)`.  The positive-pair common-neighbor
sum would be `20`, but every contributing local type contributes a multiple
of three, a contradiction.

At weight eleven the only remaining composition up to sign is `(7,4)`.
The verifier independently enumerated the three membership-dependent Farkas
polynomials on the exact ranges

```text
P: 0<=i<=6, 0<=j<=4;
N: 0<=i<=7, 0<=j<=3;
O: 0<=i<=7, 0<=j<=4;
i=j mod 3.
```

Every value is nonnegative, while the exact sum forced by the moment and
support-handshake identities is `-60`.  Therefore

```text
d(ker_F3 A)>=12.
```

The hypothetical endpoint image is narrowed to
`wt(b) in {14,17,20,23}`.  No bound `d>=24` or equality classification is
proved.

The submitted weight-fourteen aggregate control was separately recomputed.
It satisfies all recorded first/second moments and aggregate `7K2`
neighborhood-matching totals, but its internal degree multiset in each sign
class is `[0,0,0,0,0,6,6]`.  A degree-six vertex must meet every peer, so
the five declared degree-zero peers make the data nongraphical.  The control
is a legitimate stopping witness for those aggregate equations and is
neither a graph nor a codeword.  Weight twelve is simply not excluded by the
`d>=12` theorem; the frozen package supplies no separate weight-twelve
candidate certificate.

## Weight-fourteen sign-composition refinement

At weight fourteen, `p-n=0 mod 3` permits exactly

```text
(p,n)=(1,13),(4,10),(7,7),(10,4),(13,1).
```

Besides the moment equations above, the support handshakes give the
edge-free forms

```text
sum [i(i-1)+1_P i] = 2p(p-1),
sum [j(j-1)+1_N j] = 2n(n-1),
sum [ij+1_P j]     = 2pn,
sum [1_P j-1_N i]  = 0.
```

For `(p,n)=(1,13)`, the verifier independently enumerated every membership,
range, degree-14, and residue-compatible local type for

```text
Phi_13 = 1_N+4i-2j+j(j-1)+1_N j-2ij-2*1_N i.
```

There are `24` types.  According to membership and `i=0,1`, the polynomial
factors as `j(j-3)`, `(j-1)(j-4)`, `(j-1)^2`, or
`(j-1)(j-3)`.  The congruence `i=j mod 3` makes every value nonnegative,
but its exact sum from the displayed identities is

```text
13+4(14)-2(14)(13)+2(13)(12)-4(13) = -35,
```

a contradiction.

For `(p,n)=(4,10)`, the second polynomial is

```text
Phi_10 = 3i-2j+j(j-1)-ij+1_N(j-i).
```

All `51` admissible local types were checked.  It factors as
`(j-3)(j-i)` off `N` and `(j-2)(j-i)` on `N`; the exact ranges
`i<=4`, `i+j<=14`, and `i=j mod 3` make both products nonnegative.  Its
global sum is nevertheless

```text
3(14)(4)-2(14)(10)+2(10)(9)-2(4)(10) = -12.
```

Negating a codeword excludes `(13,1)` and `(10,4)`.  Therefore every
weight-fourteen word, if one exists, has exactly seven entries of each sign.
This is a `VERIFIED` composition theorem, not a weight exclusion.

For completeness, the integer lift is valid: if `p-n=3t` and `z=Ax/3`
over the integers, then the integral SRG identity gives

```text
Az=4x-z+2t*1.
```

Summing this only over the positive or negative categories reduces to
`2p(p-n)-6tp=0` and `2n(p-n)-6tn=0`; it adds no equation beyond
`p-n=3t`.  Neighbor-to-neighbor lift correlations remain unexploited.
The balanced `7+7` branch, weights `17,20,23`, `d>=24`, and the endpoint all
remain `UNKNOWN`.

## Restricted rank-four local certificate

The verifier parsed the candidate data independently, without importing its
checker, and recomputed:

```text
23 vertices, 51 edges, one selected intersection (triangles 0 and 3),
rank-four polar form, zero graph 2C4, maximum induced degree 8,
11 induced graph triangles, and no induced triangular prism.
```

Every disjoint selected pair has exactly the prescribed `0`, `1`, or `2`
cross edges; the intersecting pair has polar product one.  The signed
incidence vector has norm two and satisfies the **23 induced-coordinate**
equations `A_U b_U=0`.  All local edge/nonedge common-neighbor counts obey
the necessary caps `lambda<=1`, `mu<=2`.  The twelve weight-four and eight
weight-five internal projective circuits have zero cross-realizing vertex
pairs in this induced model.

The certificate is deliberately restricted to pair-specific intersections
and no triple membership.  It does not test the other `76` coordinates of
the global equation `Ab=0`; it omits the outside degree/common-neighbor
equalities, the other `223` triangle blocks, and the full rank-eleven frame.
Eighteen internal edges still need their unique common neighbor outside the
23-set.  It is a local compatibility certificate, not a 99-vertex SRG,
completion, counterexample, or existence result.

## Recorded discrepancies and precision findings

1. **M7g pairing language:** the projective M7g orbit/closure is unique, but
   the labelled canonical eight-set has four valid concurrent-secant
   decompositions.  Statements should not claim a unique internal pairing.
2. **Local `Ab=0` scope:** the certificate checks `A_Ub_U=0` on its 23
   induced coordinates.  The 76 outside equations are absent.  The package's
   limitations make this clear, although the short JSON key `Ab_zero` is
   scope-ambiguous in isolation.
3. **Documentation count:**
   `attempts/wave207-m7g-incidence-bridge/failed-routes.md` says the local
   model omits 91 graph vertices.  The correct count is `99-23=76`, as the
   package derivation itself states.  This does not affect any computation.

## C5. Status wall

The verified consequences are conditional/local or abstract.  None embeds
an M7g support into all endpoint constraints, produces an actual rank-66
mixed minor, completes the 23-vertex model, or excludes every survivor.
The final status is therefore exactly:

```text
Conway-99:                    UNKNOWN
rank-11 endpoint:             UNKNOWN
n3=4158 endpoint:             UNKNOWN
graph construction:           NONE
counterexample/nonexistence:   NONE
Q>=7060:                      NOT PROVED
strict n3 improvement:         NONE
```
