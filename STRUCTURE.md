# Checked structural baseline

This file collects consequences of the frozen target. `DERIVED` means the
argument is reproduced in this project; it does not imply novelty.

## Global counts (`DERIVED`)

Any Conway 99-graph has:

- spectrum `14^1, 3^54, (-4)^44`;
- 693 edges;
- 231 triangles, with the edges partitioned among them;
- seven triangles through every vertex;
- 4,158 nonedges;
- 2,079 four-cycles; and
- 84 four-cycles through every vertex.

The clique number is exactly three: triangles exist, while a `K_4` would put
each of its edges in two triangles. Hoffman's ratio bound gives independence
number at most 22 and therefore chromatic number at least five.

The complement would be `srg(99,84,71,72)`. The Laplacian spectrum is
`0^1, 11^54, 18^44`, so the matrix-tree theorem forces

```text
spanning_trees = 11^54 * 18^44 / 99.
```

## Forced `N3` and two-vertex percolation (`CITED` + `DERIVED`)

Every putative Conway graph contains an induced `N3`: two disjoint triangles
joined by exactly two independent cross-edges. Makhnev proved that no target
graph satisfies the condition that two triangles joined by at least two
cross-edges always have exactly three; `lambda=1` makes those cross-edges a
matching, so failure of the condition forces `N3`.

Reimbayev's six-vertex identities then give

```text
n3 = 0 (mod 3),
induced_C6_count = 209,286 + n3.
```

Wave 6 first sharpened the target-specific count to `n3>=24`. Wave 7 excludes
the next two multiples of three, and Wave 8 excludes the remaining equality
case at 30. The currently strongest project bound is

```text
n3 >= 33,
induced_C6_count >= 209,319.
```

For the proof, form a graph `J` on the 693 graph edges, joining two when they
are opposite in a four-cycle. It is 12-regular, so has 4,158 edges. Its
triangles are exactly induced triangular prisms. The subgraph `H` of
nontriangular `J` edges is triangle-free and its edges correspond bijectively
to induced `N3` copies. At every `H` vertex the degree lies in
`{0,4,6,8,10,12}`. Nonemptiness uses the target-specific forced `N3` theorem;
minimum degree, Mantel's bound, and `n3 = 0 (mod 3)` reduce the sub-24 cases
to 18 and 21 edges, and separate local arguments exclude both. The Wave 6
proof and adversarial audit are in
`agents/2026-07-22-wave6-opposite-edge-graph.md` and
`verification/2026-07-22-n3-count-bound-audit.md`.

For the Wave 7 strengthening, form a graph `L` on the 231 graph-triangles,
joining two when they are the sides of an induced `N3`. If `p(T)` is the
number of prism partners of triangle `T` and `q(T)=12-p(T)`, exact cross-edge
counts give

```text
d_L(T)=3q(T),
sum_T q(T)=2n3/3.
```

Lou and Murin's 2014 MIT PRIMES report already gives the equivalent fixed-
triangle partner equations and excludes `q=1` in its variables
`(alpha,beta,gamma)=(a1,a2,a3)`. Wave 7 independently rederived this profile
and combined it with the later opposite-edge graph framework; the project
does not claim novelty for the partner identities or the `q`-gap.

The local two-matching structure makes the `N3`s with fixed side `T` a
2-regular subgraph of triangle-free `H`, so `q(T)` is zero or at least two.
For `n3=24` and 27 this forces respectively eight and nine active triangles,
all with `q=2`. Their `L`-complements are a perfect matching and a 2-regular
graph. For each graph vertex `u`, the active triangles containing `u` form an
independent set `S_u` in `L`, and every actual graph edge satisfies

```text
d_H(uv)=e_L(S_u,S_v).
```

Exact point-incidence enumeration bounds the support of `H` by six when
`n3=24`, and by nine or eight in the only surviving 27-edge cases. These
contradict the required support sizes. Two materially different standard-
library checkers reproduce the finite reduction. The proof and independent
audit are in `agents/2026-07-22-wave7-triangle-side-incidence.md` and
`verification/2026-07-22-n3-side-incidence-audit.md`.

Wave 8 treats `n3=30`. The same arithmetic forces ten active triangles, all
with `q=2`; their `L`-complement `K` is cubic. For an original graph vertex
`u`, a uniform fixed-side count gives

```text
sum_{v: uv in E(G)} d_H(uv) = 4 |S_u|.
```

Point cliques `S_u` consume disjoint `K`-edges. A size-four point is a
saturated `K4` component and forces singleton points, contradicting the fixed-
point identity. Without a size-four point, singletons are again impossible,
and the incidence/edge budget forces fifteen size-two points consuming every
`K`-edge. A cubic graph on ten vertices has a vertex with two nonadjacent
neighbors `j,k`; the corresponding original vertices share an active graph-
triangle but have exactly the one crossing `L`-edge `jk`. The support identity
would give forbidden `H`-degree one. This excludes `n3=30` without classifying
cubic graphs. An independent slow audit also exhausts all 21 cubic types and
674,880 point-clique families. The proof and audit are in
`agents/2026-07-22-wave8-n3-equality.md` and
`verification/2026-07-22-n3-equality-audit.md`.

Each of the two central diagonal nonedges of the four-cycle in any `N3`
2-percolates the whole graph. The seed first infects the other two vertices of
the four-cycle and then the two remaining triangle vertices. The closure classification of
Ibrahim--LaFayette--McCall leaves only a proper `srg(9,4,1,2)` closure, but the
unique `K3 square K3` contains no induced `N3`. Therefore

```text
m(G,2) = 2.
```

For normalized triangles `{x,u,v}`, `{a,b,c}` with cross-edges `xa,ub`, the
only outside two-neighbor profiles, with multiplicity, are

```text
xa:1, ub:1, xc:1, uc:1, va:1, vb:1, vc:2.
```

The singleton profile is `(9,9,8,9,9,8)`, and 33 outside vertices see none of
the six. From seed `{x,b}`, synchronous percolation wave 1 is exactly `{u,a}`
and wave 2 is exactly `{v,c,P_xa,P_ub}`. Later waves may contain additional
vertices beyond the remaining six pair-profile vertices.

Fixing one labeled `N3` is an existentially safe search normalization: a
putative graph has an occurrence that can be globally relabeled. This does not
claim that occurrences form one automorphism orbit. The complete derivation
and source boundaries are in `agents/2026-07-22-wave3-prior-art.md`; the
single-unit implementation and branch-interaction guards are independently
checked in `verification/2026-07-22-n3-normalization-audit.md`.

## Rooted counts (`DERIVED`)

For a root `x`, write `N1=N(x)` and `N2=V-(N1 union {x})`. The induced graph
on `N1` is `7 K_2`, and `N2` is the 12-regular 84-vertex residual graph from
[CONJECTURE.md](CONJECTURE.md). It has:

- 504 internal edges;
- 84 triangles with one vertex in `N1` and two in `N2`;
- 140 triangles entirely inside `N2`; and
- five fully residual triangles through each residual vertex.

For residual labels `p,q`, let `t=|p intersection q|`, which is 0 or 1. Their
required number of common residual neighbors is:

| label relation | residual edge? | common residual neighbors |
|---|---:|---:|
| `t=1` | yes | 0 |
| `t=1` | no | 1 |
| `t=0` | yes | 1 |
| `t=0` | no | 2 |

## Triangle-intersection graph (`DERIVED`, literature-aligned)

Create a graph `T` whose 231 vertices are the triangles of the putative graph,
joining two when they share a vertex. If `N` is the 99-by-231 vertex-triangle
incidence matrix, then

```text
N N^T = A + 7 I,
N^T N = 3 I + adjacency(T).
```

It follows that `T` is 18-regular with forced spectrum

```text
18^1, 7^54, 0^44, (-3)^132.
```

This viewpoint agrees with Petro and Phillips' clique-graph treatment. It is
another exact formulation, not currently a construction.

## Automorphism restrictions (`CITED`, not independently recomputed)

The strongest combined published restrictions in the current audit imply

```text
Aut(G) is one of: trivial, C2, C3.
```

An order-three action would be fixed-point-free. This summary combines results
of Wilbrink, Behbahani--Lam, Crnkovic--Maksimovic, and Cesarz--Woldar; see
[SOURCES.bib](SOURCES.bib) and the dated literature report under `agents/`.

The full project never assumes one of these groups. The automorphism group of
the rooted *uncompleted scaffold* is `C2 wreath S7`; using it to select one
representative from equivalent rooted labelings is safe. Requiring any of it
to survive as an automorphism of the completed graph is not safe.

## Exact residual pair table (`DERIVED`)

The 84 residual labels have 924 intersecting unordered pairs and 2,562
disjoint unordered pairs. The block equations force this complete table:

| labels | residual edge? | common residual neighbors | pair count |
|---|---:|---:|---:|
| intersect | yes | 0 | 84 |
| intersect | no | 1 | 840 |
| disjoint | yes | 1 | 420 |
| disjoint | no | 2 | 2,142 |

Thus each residual vertex has two intersecting-label neighbors, ten
disjoint-label neighbors, 20 intersecting-label nonneighbors, and 51
disjoint-label nonneighbors.

The 84 intersecting-label edges form a 2-regular graph with no triangles. The
420 disjoint-label edges split among 140 edge-disjoint residual triangles. For
every residual vertex `u`, its induced neighborhood is

```text
5 K_2 disjoint-union 2 K_1.
```

The two isolated neighbors are precisely its intersecting-label neighbors.

There are 1,071 four-cycles wholly inside the residual graph, and every
residual vertex lies in 51 of them. This follows because only the 2,142
disjoint-label nonedges have two residual common neighbors; each residual
four-cycle is counted by its two diagonals.

## Seven forced multiple-of-four cycle systems (`DERIVED`)

For a root-neighbor coordinate `a`, let `F_a` be the 12 residual labels that
contain it. For each of the seven matched coordinate pairs `a,mate(a)`, the
partition

```text
F_a, F_mate(a), remaining labels
```

is equitable with quotient matrix

```text
[1 1 10]
[1 1 10]
[2 2  8].
```

Both fiber-induced graphs and the bipartite graph between the two fibers are
perfect matchings. The induced graph on their 24 vertices is a 2-factor. Its
cycles alternate same-side and cross edges, and a closed cycle uses an even
number of cross edges. Every component length is therefore divisible by four.

The possible cycle-length multisets are exactly the 11 partitions of 24 into
multiples of four. This is a pruning condition with no completed-graph symmetry
assumption. Its novelty in the literature has not been established.

These 11 multisets are only coarse cycle types. They are not 11 orbits of the
full 24-vertex configuration under the scaffold stabilizer, so fixing one
24-vertex representative per multiset would be an unsafe symmetry reduction.
The separate 11-branch split in `attempts/2026-07-22-eleven-branch-cover.md`
fixes a matching inside one 12-vertex fiber and is not this rejected shortcut.

## Residual spectrum (`DERIVED`)

Let `B` be the residual adjacency matrix and `C` the fixed endpoint-incidence
matrix. Since

```text
C C^T = 11 I + J - M,
```

`B` acts on `im(C^T)` with eigenvalues `12^1, (-2)^6, 0^7`. On `ker(C)`, the
block equation gives `B^2+B-12I=0`. Dimension and trace then force

```text
spectrum(B) = 12^1, 3^40, 0^7, (-2)^6, (-4)^30.
```

In particular, a putative residual graph is connected.

## Endpoint-fiber incidence (`VERIFIED`)

For a root-neighbor coordinate `a`, let `F_a` be the 12 residual labels
containing `a`, and let `W_a` be the 60 labels containing neither `a` nor its
mate. The map

```text
w -> N_B(w) intersection F_a
```

is a bijection from `W_a` to the 60 nonedges of the perfect matching
`B[F_a]`. Thus `B[F_a,W_a]` is the vertex-edge incidence graph of
`K_12-6K_2`.

Coupling the corresponding bijections for `a` and its mate gives a 12-by-12
nonnegative integer matrix `R` with entry sum 240. Consequently

```text
sum binom(R[u,v],2) >= 96.
```

Each counted pair defines a residual four-cycle separated by that root-matched
coordinate pair. This supplies at least 96 distinct such cycles per root group,
but cycles may be counted for multiple groups, so it is not a contradiction.

Wave 3 sharpens the count. For each root group there is an integer
`0<=z_g<=24` such that the exact number of separated cycles is

```text
S_g = 96 + z_g.
```

Thus the seven groups give at most 840 separation incidences, and at least 231
of the 1,071 residual four-cycles are not separated by any group. The same
block algebra yields a matching-plus-2-regular packaging of selected residual
edges and the exact number of residual four-cycles through each relation type:

```text
(Q,D) = (1,0),(1,1),(0,0),(0,1),(0,2)
cycles =   10,   11,    8,    9,   10.
```

See `agents/2026-07-22-wave2-structural.md` for the endpoint bijection and
`agents/2026-07-22-wave3-fiber-coupling.md` for the independently checked
coupling identities and scope warnings.

## Conditional alpha-22 design reduction (`VERIFIED`)

If a putative graph has an independent set of size 22, its other 77 vertices
define a simple `2-(22,4,2)` design with point-block incidence matrix `N` and
an outside adjacency matrix `D` satisfying

```text
NN^T = 12I+2J,
ND = -N+2J.
```

Writing `G=N^T N` and `X=4D+16I-G`, the remaining SRG equation is exactly

```text
X^2=28X.
```

Equivalently, for symmetric hollow Boolean `D` satisfying the linear
incidence equation, it is enough to impose

```text
D+4I >= 0,
33I-11D+J >= 0.
```

A compatible `X` would be 28 times a rank-33 projector. The design's
intersection-one graph consists of 22 edge-disjoint perfect matchings, while
its disjoint-block edges form 77 triples of pairwise-disjoint blocks, a linear
`77_3` configuration.

The repository includes an exact cyclic `2-(22,4,2)` certificate with block
intersection histogram `1155/1540/231`; this shows the design equations alone
are consistent. No compatible `D` is known, and this one design does not cover
the alpha-22 case. See `agents/2026-07-22-wave3-coclique-design.md`.

## Modular and integral constraints (`VERIFIED`)

Conditional on existence, the full adjacency matrix has

```text
rank_F2(A) = 54,
rank_F3(A) = 45,
SNF(A) = diag(1^45, 3^9, 6, 12^43, 84).
```

The residual adjacency matrix has exact modular Jordan forms

```text
over F2: 1^40 + J_3(0)^6 + 0^26,       rank 52;
over F3: 1^6 + 2^30 + J_2(0)^7 + 0^34, rank 43.
```

Its top nonzero determinantal divisor is

```text
Delta_77(B) = 2^49 * 3^34.
```

This determines 25 nontrivial 2-primary torsion factors with total valuation
49 and 34 factors equal to `Z/3`; it does not determine the individual
2-primary exponents.

Over `F2`, `im(A)` is an even LCD `[99,54]` code and `ker(A)` is its LCD
`[99,45]` dual. Both have minimum weight at least eight. A weight-eight dual
word must support an independent eight-set, with every vertex meeting that set
in zero or two points. Over `F3`, `im(A)` is an LCD `[99,45]` code.

Full derivations and the independently checked boundaries are in
`agents/2026-07-22-wave2-algebra-codes.md` and
`verification/2026-07-22-wave2-audit.md`.
