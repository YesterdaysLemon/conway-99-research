# Wave 206 integration audit

## Verdict

`PASS_VERIFIED_TENSOR_BALANCE_INFLECTION`.

Wave 206 reaches a new independently verified necessary condition on the
conditional prism-free rank-11 endpoint.  The actual 99-star projector system
would force a nonzero, nonconstant ternary relation in

```text
A_Delta
 = im(B^T) intersect ker(a |-> D diag(a) D).
```

Every nonzero word in this intersection has support at least eight, partitions
the 231 triangle tensors into three coefficient classes with equal tensor
sums, and pulls back to a genuine projector relation lying in every
fixed-middle three-center trace kernel and in the global `Gamma` kernel.

This is a true operator relation, not a null vector promoted from a degenerate
trace Gram matrix.  It is a useful global obstruction target, but it is not
yet a contradiction.  Rank 11, `n3=4158`, the actual nonedge fourth traces,
`Q>=7060`, and Conway 99 remain unresolved.

## Frozen boundary

```text
Conway-99:                 UNKNOWN
rank-11 endpoint:          UNKNOWN
n3=4158 endpoint:          UNKNOWN
actual nonedge h:          UNKNOWN
rigorous n3 interval:      708<=n3<=4158
conditional Q bound:       Q>=7059
Q>=7060:                   NOT PROVED
automorphism assumption:   NONE
```

The Wave 206 protocol was frozen at
`attempts/wave206-three-center-global-extension/protocol.md`, with SHA-256
`66c20334e284a26cc771ee86d97e678cb67b6ef4648b2af2fffe480fb5a9103`.

## Fixed-middle geometry

For a fixed center `y`, let

```text
A_x^(y)=P_y P_x P_y restricted to E_y,
Tau^(y)[x,z]=tr(A_x^(y) A_z^(y)).
```

The verified matrix `Tau^(y)` is symmetric, has zero row sums, has diagonal
`h_xy`, contains `g_xy` in its marked row, and has rank at most 21.  Its
compression is determined by the 21 off-diagonal coordinates

```text
m_x^(y)[i,j]=M_x[T_i,T_j],  1<=i<j<=7,
```

with nondegenerate trace metric

```text
J_star=C^T C+2I_21,
rank(J_star)=21,
det(J_star)=2.
```

The trace-zero self-adjoint subspace has dimension 20 and restricted trace
rank 19, with radical spanned by the identity.  This is why trace-Gram
nullity alone is not evidence of an operator relation.

The 84 nonneighbors of `y` split into 21 exact four-vertex fibres indexed by
the two chosen triangles in the seven-block star.  Prism-freeness allows only
the two opposite-corner matching edges inside each fibre.  Proof A also
reproduces 67,950 labelled degree-two edge modules, 130 distinct
compressions, and the complete marked low-count censuses:

```text
t=6: 18 admissible placements, all (h,r)=(1,1)
t=7: (h,r) counts
     (0,0)=288, (0,1)=9, (1,0)=144, (1,1)=180, (2,0)=144.
```

These are marginal, root-relative modules.  They do not impose the `x-z`
pair module, a shared 231-column completion, or the complete labelled
three-center graph type.

## Crossing tensors and the true-kernel code

With

```text
M_x=D S_x D=-Z^*P_xZ,
W[(T,U),x]=M_x[T,U],
Gamma=sum_y Tau^(y),
```

the independently checked relations include

```text
rank(W)=dim span{P_x}<=65,
W 1=0,
W^T W=0,
(W W^T)^2=0,
Gamma 1=0,
diag(Gamma)=H 1,
rank(Gamma)<=65.
```

Let `L=ker(B^T)` and let `K_P` be the kernel of the map
`c |-> sum_x c_x P_x`.  Since the projectors lie in the 65-dimensional
trace-zero self-adjoint space,

```text
dim(K_P)>=34.
```

The previously verified incidence bound gives `dim(L)<=33`, so `K_P/L` is
nonzero.  The outer map `A |-> Z^* A Z` is injective because `Z` has full row
rank.  Therefore

```text
K_P/L is isomorphic to A_Delta,
dim(A_Delta)=rank(B)-dim span{P_x}>=1.
```

Moreover `im(B^T)` meets the constant line only in zero.  Thus every nonzero
word in `A_Delta` is nonconstant.

For coefficient classes `j=0,1,2`, define

```text
R_j=sum_(a_T=j) z_T tensor z_T.
```

The tensor relation and the verified zero global frame give

```text
R_1+2R_2=0,
R_0+R_1+R_2=0,
therefore R_0=R_1=R_2.
```

This is equality of tensor sums, not equality of class sizes.  Pulling the
relation back through `B^T` proves that the corresponding nonzero vector is
in every true `ker(Tau^(y))` and hence in `ker(Gamma)`.

## Minimum support and sharp local boundary

For a nonzero relation supported on `k` columns, write the supported columns
as `V` and their nonzero coefficients as a diagonal matrix `Lambda`.  The
operator equation implies

```text
V Lambda V^T=0,
rank(V)<=floor(k/2).
```

The independently verified Wave 174 dual-distance theorem says that no three
centered columns are dependent.  Exact cap maxima in vector dimensions one,
two, and three are respectively `1,2,4`.  Combining these facts excludes
every `k<=7`, so

```text
every nonzero a in A_Delta has wt(a)>=8.
```

At equality the eight columns span dimension four, the coefficient form is
split, and the number of coefficient-two entries is even.

An exact relaxed eight-column control attains all local ingredients used in
this bound.  It has no 231-column frame, target incidence, graph, or
membership in `im(B^T)`.  It proves that those local ingredients alone cannot
raise the bound to nine; it does not prove that the target has a weight-eight
word.

## Hostile-control boundary

Two exact relaxed `99 by 231` systems share:

- the complete labelled pair-trace matrix `g`;
- the complete labelled fourth-trace matrix `H`;
- rank-11 square-zero centered Grams;
- exact star-projector coupling; and
- the zero global frame.

Their three-center tensors differ on 209,952 ordered triples.  Their point
graphs are disconnected, fail the target `lambda/mu` laws, contain extra
triangles, and use repeated projective directions.  They refute only the
claim that the listed relaxed pair and frame data determine `tau`.

Separate projector-only controls attain fixed-middle rank 21, and a stronger
relaxed 99-projector control has every fixed-middle slice of rank 21 while
`rank(H)=96`.  None is an endpoint construction.

## Literature boundary

The bounded Wave 206 audit checked finite-field frame spanning assumptions,
real and complex Grassmannian design hypotheses, triply regular association
schemes, and actual-graph Terwilliger algebra hypotheses.  No theorem with all
needed hypotheses was located.  This is a scoped non-discovery statement, not
evidence of novelty, priority, or openness beyond the search cutoff.

## Independent verification

The verifier froze its protocol and source-blind implementation before
opening any Wave 206 discovery package:

```text
verification/wave206-three-center-global-extension-verifier/SOURCE_BLIND_FREEZE.sha256
sha256 f878441cf73e9087596f82b1600cbffb9f22659ee10f438825161ac28246adac
```

The verifier independently reconstructed the fixed-middle algebra, hostile
controls, Proof A censuses, Proof B crossing identities, the true-kernel
quotient, the weight-eight strengthening, and a fresh relaxed boundary
control.  Root replay obtained:

```text
source-blind verifier:          10/10 PASS
post-source hostile audit:        8/8 PASS
post-source Proof-A audit:         8/8 PASS
post-source Proof-B audit:       11/11 PASS
submitted hostile suite:           7/7 PASS
submitted Proof-A suite:          12/12 PASS
submitted Proof-B suite:          14/14 PASS
submitted weight addendum:        11/11 PASS
mathematical or scope vetoes:       NONE
verifier strengthening:             wt>=8
```

Verifier package:

```text
verification/wave206-three-center-global-extension-verifier/package-manifest.sha256
sha256 3368b0b1995e40f294530cefb596cd2722a859d22aaa672190c55dbd23107ecf
```

## Inflection and next exact theorem

Wave 206 moves the route from unconstrained pair moments to a concrete
global relation code.  The next exact target is to classify
`A_Delta`, especially its possible weight-eight words, using membership in
`im(B^T)`, all 231 incidence columns, and simultaneous compatibility across
different middle centers.

Equivalent next targets include:

```text
determine the complete or marked weight enumerator of A_Delta;
exclude or classify the rank-four, even-composition weight-eight case;
impose all three pair modules on a labelled triple simultaneously;
derive a mixed four-center law for
tr((P_yP_xP_y)(P_vP_zP_v)) with y!=v.
```

If no tensor-balanced word can satisfy the incidence and mixed-center laws,
the conditional rank-11 endpoint is excluded.  If compatible words survive,
they provide a substantially more concrete blueprint for the remaining
endpoint search.
