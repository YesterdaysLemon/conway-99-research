# Exact hostile-control derivation

## 1. Projector pool

Work over `F_3` with

```text
M=diag(1,1,1,1,1,1,1,1,1,1,2).
```

Starting from `T=I_11`, the certificate applies its listed 34 nonsingular
orthogonal reflections

```text
R_v=I+(v^T M v)^(-1) v(v^T M),   T <- R_v T.
```

The first six columns `B_j` of each updated `T` are `M`-orthonormal. Therefore

```text
P_j=B_j B_j^T M
```

is an `M`-self-adjoint rank-six idempotent with trace zero. All 34 projectors
are distinct. The seven listed coefficient vectors have Gram `J_7-I_7` and
sum zero in the standard six-space. Their images under every `B_j` form seven
singular vectors `z_(j,c)` satisfying

```text
<z_(j,c),z_(j,d)>=1 for c!=d,
sum_c z_(j,c)=0,
P_j=-sum_c z_(j,c) tensor z_(j,c).
```

All identities are reconstructed from `certificate.json`; no stored matrix is
trusted.

Status: `DERIVED`.

## 2. Shared 99x231 incidence

On cyclic point sets of sizes `27`, `36`, and `36`, use:

```text
{t,t+n/3,t+2n/3}                     for 0<=t<n/3
{t,t+1,t+5}                           for t in Z_n
{t,t+2,t+10}                          for t in Z_n.
```

The short orbit has color 0. The two full orbits have colors
`1+(t mod 3)` and `4+(t mod 3)`. Their disjoint union has 99 points and 231
blocks. Every point sees each color once. The checker obtains:

```text
row degree                         7
column degree                      3
linear triple system               yes
point-graph degree                 14
point-graph edges                  693
connected component sizes          27,36,36
graph triangles                    1329
designated block triangles         231
extra graph triangles              1098
```

The common-neighbor distributions are not the SRG values:

```text
edge lambda:    4:144, 5:243, 6:27, 7:225, 8:27, 9:27
nonedge mu:     0:3240, 2:144, 4:180, 5:27, 6:315, 7:27, 8:225.
```

Thus this is exact shared incidence, but not an `srg(99,14,1,2)`.

## 3. Same full labeled g and H, different tau

Assign one projector type to each component:

```text
realization A:  pool indices (0,2,9)
realization B:  pool indices (0,2,15).
```

Use the matching seven-vector simplex on every colored block. At each point
the seven incident vectors give the assigned projector. The 231 block
vectors span the ambient 11-space, their centered Gram `D` has rank 11, and
`D^2=0`. The component counts are multiples of three, so both realizations
also satisfy

```text
sum_x P_x=0
```

and the global column frame operator is zero. The three selected star spaces
span dimension 11 in each realization.

The pair signatures between distinct component types agree label by label:

```text
component types       g       H
0,1                   2       2
0,2                   2       1
1,2                   0       2.
```

Diagonal entries also agree. Since the projector type is constant on each
labeled component, the checker explicitly constructs and compares the two
complete `99 by 99` matrices:

```text
g_A == g_B
H_A == H_B.
```

This is not an inference from the three-row table; equality of every labeled
matrix entry is tested before the collision is emitted.

The `3 by 3 by 3` type tables for

```text
tau(i,j,k)=tr(P_i P_j P_k P_j)
```

differ precisely on the six permutations of `(0,1,2)`. Consequently the full
labeled tensors differ on

```text
6*27*36*36 = 209952
```

ordered entries. The contraction `sum_z tau_(xy;z)=0` is checked for every
component type pair. Every fixed-center `99 by 99` slice is symmetric, has
zero row sums, has `y` row `g_y*`, and has diagonal `H_y*`; its rank is 3.

This refutes only the following implication:

```text
checked relaxed shared incidence
+ rank-11 square-zero centered Gram
+ exact star projectors and sum_x P_x=0
+ complete labeled g and H
=> tau is determined.
```

Status for that implication: `REFUTED`. Status for the target endpoint:
`UNKNOWN`.

## 4. Why this is not a target construction

The checker emits every material failure:

- the point graph is disconnected;
- `lambda` and `mu` are nonuniform, and cross-component pairs have `mu=0`;
- 1,098 graph triangles are not designated blocks;
- the 231 block labels use only 19 projective directions, with multiplicities
  9, 12, and 21;
- the separated triples have one point in each component and do not realize
  a target SRG three-center type; and
- selected orthogonality, endpoint block profiles, prism and crossing caps,
  `t_xy`, code distance, cover, and `Q` premises are absent.

No graph or coordinate automorphism was assumed.

## 5. The fixed-y rank-21 controls

Fix `y` and write

```text
Q_x=P_y P_x P_y.
```

The restriction of `Q_x` to `E_y` is self-adjoint. A self-adjoint operator on
a nondegenerate six-space has 21 coordinates, and

```text
tau_y[x,z]=tr(Q_x Q_z).
```

Therefore `rank(tau_y)<=21`. The checker also derives

```text
sum_z tau_y[x,z]=0,
tau_y[y,z]=g_yz,
tau_y[x,x]=H_yx.
```

Two exact 99-projector controls attain the bound:

```text
control A: pool types 0,...,32, each repeated three times; y type 0
control B: pool types 1,...,33, each repeated three times; y type 1.
```

For each control, repetition three gives `sum_x P_x=0` in characteristic
three. Both the trace Gram and the span of the compressed operators have rank
21. Their distributions differ:

```text
                         control A             control B
diagonal (0,1,2)         (30,33,36)            (33,15,51)
all entries (0,1,2)      (3078,3195,3528)      (2925,3411,3465).
```

This proves that the 21-dimensional cap is sharp for the stated
projector-level premises and that neither the diagonal nor the full slice
distribution follows from those premises.

These controls are deliberately weaker than the shared-incidence collision:
they repeat projector labels and do not impose 231 columns or star coupling.
The bounded search found no rank-21 control satisfying the stronger shared
incidence package. That nonhit is `UNKNOWN` and is not evidence of
nonexistence.

## 6. Resulting boundary

The shared-incidence construction is a stronger compatibility blueprint than
a pair-local projector collision, because it retains a complete labeled
99x231 incidence and exact star-to-column coupling while fixing full `g` and
`H`. It still misses the graph premises precisely where its `tau` entries
separate.

The next required invariant is a graph-typed joint law coupling the family of
fixed-center Gram slices, or an equivalent four-center
Terwilliger/localizer constraint. Pair data plus the contraction alone do not
provide it.
