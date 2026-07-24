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
the next two multiples of three, Waves 8--13 exclude equality at 30, 33, 36,
39, 42, and 45, Wave 15 excludes equality at 48, Wave 16 excludes equality at
51, Wave 17 excludes equality at 54, Wave 18 independently excludes equality
at 57, and Wave 19 excludes equality at 60. Wave 20 then replaces the
equality frontier with a global Schur-projector argument, and Wave 23 excludes
its first surviving endpoint. The currently strongest internally verified
project bound is

```text
n3 >= 708,
induced_C6_count >= 209,994.
```

Wave 21 independently exhausts the published six-vertex and Hamiltonian
seven-vertex affine count systems. Relative to the then-current Wave 20
bound, those necessary conditions retained every multiple of three from 705
through 4,158 and therefore supplied no improvement.

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

Wave 9 treats `n3=33`. The active-`q` arithmetic leaves only a mixed profile
`(2^8,3^2)` on ten triangles and an all-`q=2` profile on eleven. A labeled
crossing graph between possibly overlapping point sets shows that an active
singleton point would give incident `H`-degree zero or two; the global allowed
degree set eliminates two, while the fixed-point identity eliminates zero.
This immediately rules out the mixed profile.

In the eleven-triangle case the complement `K` is 4-regular. Disjoint
point-clique edge consumption leaves only size profiles
`(x2,x3)=(12,3),(15,1)`. Every size-three point forces a saturated `K5`
component. Three such points need fifteen vertices; one leaves
`K6` minus a perfect matching, where the three consumed neighbors of any
vertex would have to be a clique but never can be. This excludes `n3=33`
without assuming connectedness or a completed-graph automorphism. The proof,
compact checker, and adversarial audit are in
`agents/2026-07-22-wave9-n3-33-equality.md`,
`verification/n3-33-equality/verify.py`, and
`verification/2026-07-22-n3-33-equality-audit.md`.

Wave 10 treats `n3=36`. The active arithmetic gives `(2^12)`, `(2^9,3^2)`,
and `(2^6,3^4)`. The singleton lemma eliminates both mixed profiles because
their `q=3` triangles have `K`-degree one or zero. In the all-`q=2` case,
`K` is 5-regular on twelve active triangles and the only local point types are
`222`, `223`, `224`, and `233`.

Three point sets cannot pairwise meet at three distinct active triangles:
their original vertices would form a second graph-triangle on each edge. This
common-point rule, together with the local crossing alternatives, eliminates
size-four points and both possible modes of size-three incidence. In the
all-size-two branch, the consumed edges form a cubic graph `F`, while
`K-E(F)` is forced to be `4C3`; symmetry gives `F=2K3,3` and `K=2K6`.
Within either component the nine original point objects induce
`L(K3,3)=srg(9,4,1,2)`. Every internal pair has already saturated its required
`lambda=1` or `mu=2` common-neighbor count, whereas the fixed-point identity
forces each opposite point to be adjacent to two of them. This contradiction
excludes `n3=36` without a completed-graph automorphism assumption.

The proof, compact checker, independent 216-support census, and adversarial
audit are in `agents/2026-07-22-wave10-n3-36-equality.md`,
`verification/n3-36-equality/verify.py`,
`verification/n3-36-equality/n3-36-support.json`, and
`verification/2026-07-22-n3-36-equality-audit.md`. An initially proposed
closed-`K5` shortcut failed review and is not used in the repaired proof.

Wave 11 treats `n3=39`. The active arithmetic leaves four profiles. Singleton
forcing eliminates the three mixed profiles, while the all-`q=2` profile has
thirteen active triangles and a 6-regular complement `K`. Every active point
set is a clique in `K`; linearity and the common-point rule show that a point
of size `s` needs `2s` distinct representatives outside itself, so `s<=4`.

A size-four point has eight external petals in nine available places. At
least three occurrences are `224`; two such occurrences provide four distinct
endpoints adjacent in `K` to all four root vertices, forcing root degree at
least seven. With only sizes two and three left, let `F` be the point-clique
edges and `U=K-E(F)`. If `t_i` size-three points pass through active triangle
`i`, then

```text
d_F(i)=3+t_i and d_U(i)=3-t_i.
```

At a `233` occurrence, the size-two endpoint has four singleton-crossing
neighbors. The common-point rule prevents any of their edges from lying in
`F`, contradicting `d_U<=3`. A size-three point cannot be all `333` by the
same external-capacity argument; hence it has a `223` occurrence. Its five
forced `U`-edges propagate `223` to the other two root occurrences, whose four
distinct endpoints then force `U`-degree four at the original root, although
its available degree is two. Finally, an all-size-two point family would have
even total incidence, contradicting `13*3=39`.

The derivation and all checkers explicitly require that `K` is the simple
complement of `L` on distinct active triangles. An earlier exposition omitted
that bridge and failed audit. The repaired compact checker, independent
8,907-record replay, and public audit are in
`agents/2026-07-22-wave11-n3-39-equality.md`,
`verification/n3-39-equality/`, and
`verification/2026-07-22-n3-39-equality-audit.md`.

Wave 12 treats `n3=42`. Exact partitioning of `sum q(T)=28` gives six raw
active profiles. The inherited no-singleton premise first leaves
`(2^14)` and `(2^11,3^2)`. A triangle of forced point sets around any active
`K`-vertex of degree three excludes the mixed profile, so the sole case has
fourteen active triangles, `q=2` everywhere, and a 7-regular `K`.

Expansion again bounds active point size by four. Eight petals around a
size-four point occupy ten external labels, forcing at least six singleton
external sides and hence `K`-degree at least nine at every root label. With
sizes two and three left, put `t_i` for the number of size-three points through
label `i`, let `F` be the point-clique edges, and set `U=K-E(F)`. Then

```text
d_F(i)=3+t_i,  d_U(i)=4-t_i.
```

For a size-three point `{i,j,k}`, singleton petals and capacity leave only
`(t_i,t_j,t_k)=(2,2,2)` or a permutation of `(2,3,3)`. The latter forces five
distinct full `2`-by-`2` crossings, contributing 20 to a fixed-point sum equal
to 12. If a size-three point remained in the former mode, the intersection
graph of size-three points would be cubic and triangle-free. Incidence bounds
reduce it to `K3,3`; its nine edge labels would inject into only five `t=0`
labels because `L(K3,3)` has no open twins. Thus every active point has size
two.

The 42 point incidences are therefore the 21 edges of a simple cubic
triangle-free graph `F` on fourteen labels. Every valid `K` contains `F` and
every pair of `F`-neighbors of one label. The fixed-point identity makes the
positive-support graph on `E(F)` a 2-factor. Testing support rectangles only
against those mandatory `K`-edges is a relaxation, while the forced active
adjacency graph must obey the SRG common-neighbor upper caps one and two.

An independently decoded GENREG catalog supplies the 110 connected types;
direct order-six and order-eight censuses supply the two disconnected types.
They match the independent 112-record graph6 catalog bijectively. Only four
types survive the mandatory-degree filter, and independently generated and
replayed rejection trees find no support factor satisfying the caps. This
conditionally excludes `n3=42`; it assumes no completed-graph automorphism and
does not resolve Conway-99. The proof, support certificate, and final audit are
in `agents/2026-07-22-wave12-n3-42-proof-a.md`,
`verification/n3-42-equality/`, and
`verification/2026-07-22-wave12-integration-audit.md`.

Wave 13 treats `n3=45`. Exact partitioning of `sum q(T)=30` gives nine raw
active profiles. The inherited no-singleton and degree-three obstructions
leave only

```text
r=14: q-profile (2^12,3^2),
r=15: q-profile (2^15).
```

In the mixed case, active points have size at most three. A size-three point
containing a `q=3` label has no admissible local mode. An ordinary size-three
point can have only mode `222` or `233`; fixed-crossing capacity removes
`233`, while `222` would make the intersection graph cubic and triangle-free.
It reduces to `K3,3`, whose line graph has distinct open neighborhoods, forcing
an impossible injection of nine labels into three. If all points instead have
size two, either special label needs at least five `K`-neighbors although its
capacity is four. Thus the mixed profile is impossible.

For the all-`q=2` order-fifteen profile, flower enumeration removes point sizes
five and four. Let `t_i` count size-three points through label `i`. Exact
crossing and fixed-point capacities leave four local types:

```text
111, 122, 222, 223.
```

Type `223` would induce a one-regular graph on three labels and is impossible.
For type `111`, the six co-point endpoints saturate every root label in `K`;
the remaining labels cannot supply the required fixed support. Hence only
types `122` and `222` remain. A size-two point then has positive crossing
degree four, while a size-three point already consumes eight or twelve units,
so every vertex of the edge-auxiliary graph `H` has degree zero or four. But
`|E(H)|=n3=45`, and the handshake sum `90` is not divisible by four. This
conditionally excludes `n3=45`, forcing `n3>=48` and
`induced_C6_count>=209334`.

Two independent semantic audits reconstruct this argument without assuming a
completed-graph automorphism, connectedness, or transitivity. The separate
active-local SAT scan is not part of the proof and its 17 negative rows remain
`UNSAT_UNVERIFIED`; its initial self-validation bundle failed audit and was
repaired and re-audited without erasing the failure. See
`agents/2026-07-22-wave13-n3-45-proof-a.md`,
`verification/2026-07-22-wave13-n3-45-audit.md`,
`verification/2026-07-22-wave13-n3-45-audit-b.md`, and
`verification/2026-07-22-wave13-computation-repair-audit.md`. The result is a
conditional necessary bound only. Conway-99 and novelty remain `UNKNOWN`.

Wave 14 treats the unresolved equality case `n3=48`. Partitioning
`sum q(T)=32` gives twelve raw active profiles; the inherited minimum
point-clique degree and degree-three obstruction leave

```text
r=14: q-profile (2^10,3^4),
r=15: q-profile (2^13,3^2),
r=16: q-profile (2^16).
```

In the order-fourteen case, local crossing capacity reduces size-three points
to two modes; their intersection graph and incidence budget conflict, and the
all-size-two alternative overfills a special label. In the order-fifteen
case, size-three points cannot meet either special label, while a remaining
special--ordinary size-two point has fixed support sum ten although every
term is divisible by four. Both mixed profiles are therefore excluded.

For `r=16`, expansion and flower obstructions leave only point sizes two and
three. Exact local enumeration gives ten aligned size-three modes; fixed
support eliminates the two modes with no full meeting crossing. A six-edge
crossing is then impossible, so every graph-edge vertex of `H` has degree
zero or four. If `mathcal P` is the active point family and `R` joins point
objects whose actual graph edge has `H`-degree four, then

```text
d_R(P)=|P| in {2,3},
sum_(P in mathcal P)|P|=48,
|E(R)|=24,
```

and every one of the 48 edges of the 6-regular graph `L` has exact twofold
coverage by the full `K2,2` rectangles carried by `R`.

This finite residual is consistent at the active/local/support level. The
archived all-size-two object has point graph `2Q3`, support `6C4`, a simple
4-regular triangle-free `H`, and passes the declared common-neighbor upper
caps. It omits the other 75 original vertices, inactive triangles, degree-14
completion, and the missing SRG equalities, so it is a countermodel only to an
overstrong relaxation claim. A separate computation has raw status
`1 SAT_CANDIDATE`, `7 UNSAT_UNVERIFIED`, `1 BUDGET_UNKNOWN`, and
`2 TIMEOUT_UNKNOWN`; none of its negative rows is proof evidence. The
reduction and independent audits are in
`agents/2026-07-22-wave14-n3-48-proof-a.md`,
`verification/2026-07-22-wave14-n3-48-proof-audit.md`, and
`verification/2026-07-22-wave14-n3-48-computation-audit.md`. Thus Wave 14
does not improve the verified `n3>=48` bound. The equality exclusion, target,
and novelty remain `UNKNOWN` at this checkpoint.

Wave 15 excludes the Wave 14 `n3=48` residual with a global induced-subgraph
obstruction. Let

```text
X = {u in V(G) : S_u is nonempty}.
```

The sixteen active triangle labels have point degree three, so
`sum_u |S_u|=48`. Every nonempty point has size at least two; hence
`|X|<=24`. Each active triangle through `u` supplies its other two vertices as
distinct neighbors of `u` in `X`. Distinct triangles through `u` cannot share
another vertex because every graph edge lies in exactly one triangle. Thus a
point of size at least three already gives six induced neighbors.

If `|S_u|=2`, the Wave 14 support graph has two distinct actual graph-edge
neighbors at `S_u`. Neither is one of the four triangle neighbors. If such a
support edge met `S_u` in an active label, deleting the shared label would
leave one crossing row and at most two columns. The audited two-sided `0/2`
crossing law makes its `H`-degree zero (and in any event below four), whereas
a support edge has `H`-degree four. Therefore the two support neighbors are
new, and every vertex of `G[X]` has induced degree at least six.

The target spectrum is `14^1,3^54,(-4)^44`. For `m=|X|`, decomposing the
characteristic vector of `X` into its all-ones and orthogonal parts gives

```text
2e(X) <= 14m^2/99 + 3(m-m^2/99)
       = 3m + m^2/9.
```

But minimum degree six gives `2e(X)>=6m`, so `m>=27`, contradicting
`m<=24`. A separate exact count of the first two moments of outside degrees
reaches the same contradiction by Cauchy--Schwarz. Consequently `n3=48` is
impossible; the divisibility `3|n3` and Reimbayev identity give

```text
n3 >= 51,
induced_C6_count >= 209337.
```

Two discovery lanes and two independent audits reproduce the result. The
explicit Wave 14 all-size-two object remains a valid countermodel to its
stated active/local/support relaxation, but its lift to the full SRG equations
is refuted. See `agents/2026-07-23-wave15-global-lift.md`,
`agents/2026-07-23-wave15-algebraic.md`,
`verification/2026-07-23-wave15-global-lift-audit.md`, and
`verification/2026-07-23-wave15-algebraic-audit.md`. This is a conditional
necessary bound only; Conway-99 and novelty remain `UNKNOWN`.

Wave 16 applies the same global obstruction directly at `n3=51`, without a
Wave 14 point-size classification. Here

```text
sum_T q(T)=34,
q(T)>=2,
d_K(T)=r-1-3q(T).
```

Exact partitioning gives sixteen raw active profiles. Every active label lies
in three non-singleton linear points, so `d_K>=3`; the independently audited
degree-three obstruction strengthens this to `d_K>=4`. Exactly four profiles
remain:

```text
r=14: q=2^8 3^6,
r=15: q=2^11 3^4,
r=16: q=2^14 3^2,
r=17: q=2^17.
```

For the indexed active original-vertex set

```text
X={u:S_u is nonempty},
sum_{u in X}|S_u|=3r.
```

No active point is a singleton, so `|X|<=floor(3r/2)<=25`. A point of size
at least three already supplies six distinct active-triangle neighbors. For a
size-two point `P={i,j}`, the complete two-sided crossing classification is
endpoint-local:

```text
P and Q meet:                  d_H(uv)=0,
P and Q are disjoint:          d_H(uv) is 0 or 4.
```

The fixed-point sum is `2(q(i)+q(j))`. Thus a `(2,2)` point has exactly two
positive nonmeeting neighbors, a mixed `(2,3)` point is impossible modulo
four, and a `(3,3)` point has exactly three positive nonmeeting neighbors.
All positive terms are distinct actual graph neighbors in `X`, not support
multiplicities. Consequently every vertex of `G[X]` has induced degree at
least six.

The Wave 15 spectral inequality requires every nonempty induced set of
minimum degree six to have order at least 27, contradicting `|X|<=25`.
Therefore `n3=51` is impossible. Divisibility by three and the exact cycle
identity give

```text
n3 >= 54,
induced_C6_count >= 209340.
```

The independent audit explicitly tests that the proof does not assume a
point-size-at-most-three bound, a global `H`-degree `{0,4}` law, or the Wave 14
support-graph identity. A separate computation verifies a seven-branch
active-local archive and one positive relaxation object but is not used in
the exclusion; its one raw UNSAT return has no proof trace. See
`agents/2026-07-23-wave16-n3-51-structural.md` and
`verification/2026-07-23-wave16-n3-51-structural-audit.md`. This remains a
conditional necessary bound; Conway-99 and novelty are `UNKNOWN`.

Wave 17 applies the same framework at `n3=54`, where

```text
sum_T q(T)=36.
```

The exact `d_K>=4` filter leaves six profiles. Five have `r<=17`, hence
`|X|<=25`, while the endpoint-local crossing arithmetic still gives
`delta(G[X])>=6`; the spectral subset bound excludes them. The last profile is

```text
r=18, q=2^18, |X|=27.
```

Equality forces every active point to have size two, `G[X]` to be 6-regular,
and the cut to be equitable with quotient `[[6,8],[3,11]]`. Let `F` be the
simple cubic triangle-free graph on the 18 active labels whose 27 edges are
the active points. The remaining two neighbors of each point form a simple
2-factor `R` on `E(F)`. If `N` is the vertex-edge incidence matrix of `F`,
then

```text
G[X] = line(F) union R,
N A_R N^T = 2 A_L.
```

No nonadjacent pair of `F` has codegree exactly two. Hence each component is
`K3,3` or has girth at least five. Component sizes reduce to `(18)`, `(6,12)`,
or `(6,6,6)`; an exact binary parity argument excludes `3K3,3`. The two
remaining families contain exactly 455 connected cubic girth-at-least-five
graphs of order 18 and two disjoint unions of `K3,3` with a connected such
graph of order 12, according to the official House of Graphs catalogs.

For a fixed `F`, a compatible support variable joins two disjoint `F`-edges
whose endpoint rectangle avoids every forced `K`-pair. Reducing point-degree
two and rectangle-coverage zero-or-two modulo two gives a `180`-row binary
system. Among the 455 connected cases, 443 kernels are trivial. The remaining
12 have nullities `1^4,2^5,4^2,18`; exhaustive enumeration of all 262,204
vectors in those nontrivial kernels finds no vector with integer degree two at
all 27 points. In each mixed case, the nine `K3,3` point-edges force 18 cross
edges and therefore nine internal order-12 edges, but only one or zero such
candidates exist.

An independent implementation fetched and hash-validated both official
catalogs, reconstructed all 457 cases, reproduced every certificate field,
and passed 17 hostile tests. This exact obstruction excludes `n3=54`.
Divisibility by three and the induced-cycle identity give

```text
n3 >= 57,
induced_C6_count >= 209343.
```

The raw SAT scout also returned `UNSAT` on all 457 fixed-`F` cases, but it
produced no checked proof traces and is non-evidentiary. Catalog completeness
and one representative per isomorphism class remain external official
premises. See `agents/2026-07-23-wave17-n3-54-structural.md`,
`verification/2026-07-23-wave17-n3-54-structural-audit.md`,
`agents/2026-07-23-wave17-n3-54-census.md`, and
`verification/2026-07-23-wave17-n3-54-census-audit.md`. This is a conditional
necessary bound, not a target resolution or novelty determination; both
Conway-99 and novelty remain `UNKNOWN`.

Wave 18 analyzes `n3=57` directly, without importing the Wave 17 exclusion.
Here

```text
sum_T q(T)=38.
```

The exact `d_K>=4` filter gives nine profiles with `14<=r<=19`. Endpoint-local
crossing arithmetic again yields `delta(G[X])>=6`, while non-singleton indexed
points give `|X|<=floor(3r/2)`. The spectral subset bound requires `|X|>=27`,
so every profile with `r<=17` is impossible.

For `r=18`, equality forces 27 size-two points and exact 6-regularity of
`G[X]`. The surviving profiles are `q=2^16 3^2` and `q=2^17 4`. The former
would separate the two odd labels from the sixteen even labels in a simple
cubic point graph, which cannot give either odd label degree three. In the
latter, every point incident with the unique `q=4` label is of type `(2,4)`
and has induced degree at least seven, contradicting 6-regularity.

For `r=19`, the only profile is `q=2^19` and `27<=|X|<=28`. At 27 vertices,
the exact point-size profiles are `2^26 5`, `2^25 3 4`, and `2^24 3^3`;
meeting-neighbor counts or the fixed-point sum exclude all three. At 28
vertices, the sole profile `2^27 3` forces the size-three point to have at
least nine active neighbors. The even degree sum is therefore at least 172,
whereas

```text
2e(G[X]) <= 3(28)+28^2/9 = 1540/9
```

permits at most 170. Thus conditional `n3=57` is impossible. A materially
independent checker reconstructs the profiles, overlap-deleted crossings,
point-size partitions, and exact rational bounds, passing 14 tests and
detecting 24 hostile mutations. Combining this exclusion with Wave 17 yields

```text
n3 >= 60,
induced_C6_count >= 209346.
```

See `agents/2026-07-23-wave18-n3-57-structural.md` and
`verification/2026-07-23-wave18-n3-57-structural-audit.md`. This is a
conditional necessary bound over authenticated audited framework premises,
not a target resolution, formal-kernel proof, or novelty determination;
Conway-99 and novelty remain `UNKNOWN`.

The Wave 18 literature lanes independently checked the exact endpoint numbers,
the standard Rayleigh ingredient, current sources, and two close 2022/2026
status leads. No exact published `n3=57` exclusion, `n3>=60`, or `209346`
endpoint was found; those focused nonhits do not establish novelty. Baker's May
2026 conference abstract describes a related induced-subgraph paradigm but
states no exact theorem or proof. Ishihara's 2022 Theorem 28 claims
nonexistence, but its equation (88) assumes every second-layer residual vertex
has two first-layer residual neighbors. Root-label reconstruction instead gives
degrees `1^20,2^51` and the corrected double count

```text
10(10)+11(2)=122=2(71)-20,
```

not 142. Thus that displayed proof is `REFUTED`, while both target outcomes
remain `UNKNOWN`. See `agents/2026-07-23-wave18-status-search.md` and
`verification/2026-07-23-wave18-status-audit.md`.

Wave 19 treats `n3=60`, so `sum_T q(T)=40`. The `m=27` equality profile
forces 21 size-two and six size-three indexed points. The positive-meeting
graph on the six size-three points is either a triangular prism or `K3,3`;
exact twofold witness multiplicity excludes both after making the grid-label
injectivity step explicit.

At `m=30`, every active point has size two. Writing the 30 points as the edges
of a triangle-free cubic graph `F` on 20 active labels gives

```text
D = L(F) union R union Z,
N A_R N^T = 2 A_L,
|Z| <= 3,
B = 12I - D - D^2 + 2J = C C^T.
```

Here each local `L` row is a remote induced six-cycle, the choices are
symmetric, `R` is the resulting point 2-factor, and `Z` contains the remaining
allowed point edges. Exact enumeration of all official connected cubic
order-20 records and all disconnected component types leaves only two Petersen
components. Its 120 `L/R` models form one orbit with stabilizer 240. Exhausting
all `1+165+C(165,2)+C(165,3)=748826` labeled `Z` placements leaves 16 PSD Gram
orbits. Fifteen coefficient systems are inconsistent. For the sole residual

```text
Z = {(0,23),(1,22),(2,17)},
```

an integer Farkas functional has target `-6` and nonnegative score on every one
of the 232 possible nonzero binary outside columns. Hence no nonnegative column
multiplicities can realize `B`, excluding conditional `n3=60` and yielding

```text
n3 >= 63,
induced_C6_count >= 209349.
```

A materially independent verifier authenticates the canonical-LF release,
reconstructs every connected and disconnected disposition, re-enumerates all
`Z` placements and Gram systems, checks hostile mutations, and replays the
submitted checker. See `agents/2026-07-23-wave19-alternate-frontier.md` and
`verification/n3-60-closure/2026-07-23T161951Z-final-audit.md`. Official House
of Graphs catalog completeness and nonisomorphism are explicit external
premises. This remains a conditional necessary bound; Conway-99 and novelty
remain `UNKNOWN`.

Wave 20 uses only the target parameters and the full set of 231 graph
triangles. Let `N` be the `99`-by-`231` vertex-triangle incidence matrix and
let `Gamma` join intersecting triangles. Then

```text
N N^T = A + 7I,
N^T N = 3I + Gamma,
spec(Gamma) = 18^1, 7^54, 0^44, (-3)^132.
```

For

```text
C = Gamma^2 - 5Gamma - 18I,
```

the diagonal and intersecting entries vanish, while a disjoint pair entry is
its number `r` of cross-edges, in `{0,1,2,3}`. If `a_r(T)` counts disjoint
triangles with `r` cross-edges to a fixed triangle and
`q(T)=12-a_3(T)`, exact zeroth, first, and second moments give

```text
(a0,a1,a2,a3) = (20+q, 180-3q, 3q, 12-q),
2n3 = 3 sum_T q(T),
3 divides n3.
```

The orthogonal projector onto the 44-dimensional zero eigenspace of `Gamma`
is

```text
E = (3I + J - Gamma - C)/21.
```

Thus the integral matrix `M=21E` is positive semidefinite, has rank 44,
satisfies `M^2=21M`, has diagonal 4, and has off-diagonal entries
`0,1,-1,-2`. Put

```text
W = M o M,
A4 = M W M.
```

Schur positivity makes `W` and `A4` positive semidefinite. Since
`W=M (mod 2)`, one has `A4=M (mod 2)`, and every row is nonzero. Writing
`D=(W-M)/2`, the matrix `D mod 2` is symmetric with zero diagonal, so its
quadratic form is alternating. It follows that every diagonal of `A4` is
divisible by four. A zero diagonal in a positive-semidefinite matrix would
force the corresponding row to vanish, so all 231 diagonals are at least
four. Finally,

```text
tr(A4) = 84(n3-693) >= 4*231 = 924.
```

Hence `n3-693>=11`; divisibility by three forces

```text
n3 >= 705,
induced_C6_count >= 209991.
```

A blind verifier independently reconstructed the combinatorial entries,
projector scaling, Schur trace, mod-two and mod-four arguments, and endpoint;
its 16 tests and the submitted 18 tests pass with byte-identical regenerated
JSON. See `agents/2026-07-23-wave20-global-schur.md` and
`verification/2026-07-23-wave20-global-schur-audit.md`. The frozen
`failed-routes.md` introduction retains the intermediate endpoint 699, while
the later section and every operative artifact use 705; the correction and
failed harness invocations are retained in `orchestrator-notes.md`.

An independent status auditor froze the claim without opening the proof,
verified the cited triangle-graph spectrum and induced-six-cycle identity, and
found no accepted target resolution or exact published `705/209991` endpoint
through 2026-07-23. Generic Schur/Krein positivity is prior art, and
non-discovery cannot certify novelty. The argument is a conditional necessary
bound rather than a construction, nonexistence proof, or formal-kernel proof;
Conway-99 and novelty remain `UNKNOWN`.

## First surviving endpoint refinements (`VERIFIED_INCONCLUSIVE`)

At the first surviving value `n3=705`, the integral Schur lift from Wave 20

```text
W = M o M,
A4 = M W M
```

has trace 1,008. Representing `M` as the Gram matrix of norm-four vectors in
dimension 44 and contracting the associated quadratic tensors gives, for
every triangle `T`,

```text
A4[T,T] >= (99/43)*(q(T)-2)^2.
```

Every diagonal is already known to be a positive multiple of four. Since the
other 230 diagonals contribute at least 920, a selected diagonal is at most
88, and therefore

```text
q(T) <= 8.
```

The exact trace-square arithmetic also yields

```text
tr(A4^2) = 441*t,
t = 4 (mod 8),
t >= 60,
tr(A4^2) >= 26,460.
```

These restrictions do not close the endpoint. Keeping `q=1`, the exact scalar
relaxation has 22,113 aggregate profiles; one survivor has 223 rows with
`q=2` and eight with `q=3`. A separate rank-44 two-moment spectrum also
survives. Neither object is asserted to be a compatible matrix or graph.

The parallel lattice reduction puts

```text
U = im(M),
L = U intersect Z^231,
h = [L : 21L*].
```

The independently audited identities include

```text
E Z^231 = L*,
M Z^231 = 21L*,
h = 21^44/det(L).
```

The lattice `L` is even with minimum at least four. On `L`, the operator
`B=A4/21` is integral, self-adjoint, positive definite, and congruent to the
identity modulo two. For an integral basis matrix `X` of `L`, the even
positive-definite Gram matrix `Q=X^T W X` satisfies

```text
det(B) = h*det(Q).
```

At `n3=705`, `tr(B)=48` and exact AM--GM gives `det(B)<=45`. The discovery
submission obtained the weaker necessary list `{1,3,7,9}`. The verifier
separately proved that an even integral Gram matrix of rank 44 and odd
determinant has determinant one modulo four. Together with the standard
rank-44 even-unimodular signature obstruction, this sharpens the full endpoint
condition to

```text
n3=705  ==>  h in {1,9}.
```

At the Wave 21 checkpoint the index `h` was not determined, so those lanes
gave no improvement over `n3>=705`. Wave 23 later excludes the whole endpoint
by a stronger argument. Full derivations and exact replays are in
`agents/2026-07-23-wave21-local-diagonal.md`,
`verification/wave21-local-diagonal/2026-07-23T185252Z-audit.md`,
`agents/2026-07-23-wave21-lattice-extension.md`, and
`verification/wave21-lattice-extension/2026-07-23T184926Z-audit.md`.

## Six-/seven-vertex affine count envelope (`VERIFIED_INCONCLUSIVE`)

The Wave 21 lane independently enumerates every locally admissible graph under
the pairwise conditions inherited from `srg(n,k,1,2)`. Canonicalization under
all vertex permutations gives exactly

```text
order 4:                  9 classes
order 5:                 21 classes
order 6:                 62 classes
order 7, Hamiltonian:    19 classes
```

Reconstructing every vertex-deletion deck uniquely aligns these classes with
the indices in Reimbayev's six-vertex and Hamiltonian seven-vertex tables.
The aligned `N3` is exactly two vertex-disjoint triangles joined by two
independent cross-edges, so the source parameter `n3` is the project parameter.
No automorphism of a putative target is assumed.

The printed five-to-six deletion equations in arXiv:2508.03377v2 have one
defect. Sixty-one `N_j` columns have coefficient sum six, but the `N23` column
has sum five. Substitution of the source's own affine formulas gives

```text
20 equations:                 residual 0
printed m7(n-5) equation:     residual n23
n23 at the Conway parameters: 1,496,880 + 4*n3
```

Trying the missing deletion card in each of the 21 possible `M_i` rows shows
that only `M7` yields an actual locally admissible six-vertex deck. The narrow
correction is therefore

```text
printed m7(n-5) right-hand side + n23.
```

The raw equation is retained as `REFUTED_AS_PRINTED`; the correction is a
separately named and independently checked path. After that correction all 62
deletion columns sum to six, all source indices align bijectively, and all 21
deck identities have zero residual.

At `n=99,k=14`, exact rational specialization of all 62 six-vertex formulas
gives simultaneous integrality and nonnegativity exactly when

```text
n3 = 0 (mod 3),
0 <= n3 <= 4158.
```

Writing the free Hamiltonian seven-vertex count as `h11`, all 19 displayed
counts are simultaneously integral and nonnegative exactly when

```text
h11 = 0 (mod 4),
ceil_to_multiple_of_4(2*n3) <= h11 <= 4*n3.
```

The universal choice `h11=4*n3` works for every six-vertex-feasible value.
Consequently, the then-current Wave 20 bound left

```text
n3 = 705,708,...,4158:        1,152 values
n3=705, h11=1412,1416,...,2820: 353 values
```

This is a complete exhaustion of the encoded formulas, not of global graphs.
The seven-vertex source enumerates Hamiltonian types rather than all induced
seven-vertex types, and a feasible count vector is not an adjacency matrix.
The discovery suite passes 16 tests, the separately written verifier passes
19, and all three exact JSON outputs replay byte-identically. See
`agents/2026-07-23-wave21-six-vertex-lp.md`,
`verification/wave21-six-vertex-lp/2026-07-23T174137Z-audit.md`, and
`verification/wave21-six-vertex-lp/2026-07-23T175223Z-orchestrator-replay.md`.
The source-first status record
`verification/wave21-six-vertex-lp/status/2026-07-23T182843Z-source-status-audit.md`
confirms that official v1 and the still-current v2 both omit the term and
records that no formal or corrected publication was located. That bounded
non-discovery is not a novelty certificate. The count result supplies no
stronger bound or target resolution.

## Complete aggregate order-seven deck (`VERIFIED_INCONCLUSIVE`)

Wave 22 enumerates all `2^21` labeled graphs on seven vertices, retains the
394,020 that satisfy the inherited local common-neighbor upper bounds, and
canonicalizes them into 208 isomorphism classes. Deleting every possible
vertex produces the complete integer matrix

```text
D: 62 six-vertex types x 208 seven-vertex types.
```

Its exact row ranks over `F_2,F_3,F_5,F_7,F_11` are respectively
`48,57,61,61,62`. At the historical endpoint
`n3=705,h11=2820`, a frozen nonnegative integer vector has total
`binom(99,7)`, support size 105, satisfies all 62 equations

```text
D*x = 93*(n1,...,n62),
```

and assigns all 19 pinned Hamiltonian classes their displayed published
counts. The discovery and independent implementations separately reconstruct
the complete order-six/order-seven censuses, deletion cards, Hamiltonian
classes, source alignment, and exact arithmetic.

This witness is not a graph: it does not impose consistency between
overlapping seven-subsets and supplies no adjacency matrix. Its role is to
show that the complete aggregate deletion relaxation alone does not exclude
the old endpoint. See
`agents/2026-07-23-wave22-full-seven-deck.md` and
`verification/wave22-full-seven-deck/2026-07-23T191133Z-audit.md`.

## Projector-index endpoint exclusion (`VERIFIED`)

Wave 23 returns to the rank-44 projector lattice. At `n3=705`, write the
integral positive self-adjoint endomorphism as

```text
B = I+2C,
rank(B)=44,
tr(B)=48,
tr(C)=2.
```

For an integral matrix, `tr(C^2)=tr(C) (mod 2)`. Positive-form
self-adjointness makes the eigenvalues of `C` real, so `tr(C^2)` is a
positive even integer. Hence

```text
tr(B^2) >= 60.
```

The 44 positive eigenvalues of `B` therefore have sum 48 and square sum at
least 60. A complete compactness/KKT argument puts any determinant maximizer
on square sum 60 with exactly two eigenvalue values. The independent checker
uses exact dyadic radical intervals for all 38 positive multiplicities and
proves

```text
det(B) < 13.
```

Since `det(B)` is a positive integer congruent to one modulo four,
`det(B)` is in `{1,5,9}`. The verified factorization
`det(B)=h det(Q)`, the rank-44 even-Gram congruence, and the
even-unimodular signature obstruction leave only `h=1`; but
`h=1` would make `G/21` an even positive-definite unimodular form of
signature 44, which is impossible. Thus the endpoint is excluded:

```text
n3 != 705,
n3 >= 708,
induced_C6_count >= 209994.
```

A second proof lane, isolated from this derivation, obtains the looser but
sufficient exact cap `det(B)<43` directly from Newton and Maclaurin:

```text
e2 <= 1122,
det(B)^(1/22) <= 1122/binom(44,2) = 51/43,
51^22 < 43^23.
```

Together with the scaled-dual determinant congruence this also leaves no
index. A separately written verifier reconstructs the proof and passes 17
hostile tests. Its first audit also caught an ancillary discovery-ledger
error: `(9,3,27)` violates the retained `det(B)=1 (mod 4)` condition. The bad
control is preserved and refuted, `(9,1,9)` is the corrected
single-relaxation witness, and a second frozen addendum verifies that the
mathematical result is unchanged.

The primary proof and blind audit are
`agents/2026-07-23-wave23-index-pranks.md` and
`verification/wave23-index-pranks/2026-07-23T192952Z-audit.md`; the isolated
cross-check, audit, and correction record are
`agents/2026-07-23-wave23-endpoint-crosscheck.md`,
`verification/wave23-endpoint-crosscheck/2026-07-23T195158Z-audit.md`, and
`verification/wave23-endpoint-crosscheck/2026-07-23T200645Z-correction-audit.md`.

Both arguments are conditional necessary bounds. Neither constructs a graph
or proves that no target graph exists. A source-separated audit of 24 frozen
query and citation paths found that its inspected current sources still treat
the target as open and located neither the exact `708/209994` endpoint nor
the complete method. This is bounded non-discovery, not proof of openness or
novelty; both target existence and novelty remain `UNKNOWN`. See
`verification/wave23-literature-audit/2026-07-23-wave23-literature-audit.md`.

## Orbit-refined order-seven extensions (`VERIFIED_INCONCLUSIVE`)

A parallel Wave 23 lane strengthens the aggregate seven-vertex deck by
distinguishing every vertex and pair orbit inside each six-vertex card. Over
all 208 locally admissible seven-vertex classes, the exact integer system has

```text
deletion rows:               62
vertex-orbit rows:          207
edge-pair-orbit rows:       180
nonedge-pair-orbit rows:    263
total:                      712
```

The independent verifier checks every canonicalizing isomorphism and confirms
that these coefficients merely partition distinguished vertices and pairs;
they impose no automorphism on the putative 99-vertex target. A separately
rebuilt lower-order gate forces the counts through order five, and the source
order-six vector passes all 171 orbit-refined `5->6` rows.

At the now-excluded historical endpoint `n3=705`, the matrix `A` has rational
rank 207. A frozen nonzero integer vector `delta` spans its checked kernel,
and adjoining only the pinned `H11` coordinate raises the rank to 208. The
exact family

```text
x(z) = base + (z-353) delta,
z = 353,...,705,
h11 = 4z
```

satisfies every row. Its endpoint minimum counts are two and zero, so every
coordinate remains nonnegative throughout the interval. The other 18
Hamiltonian formulas are post-hoc comparisons, not solver inputs, and all
match.

Thus this complete encoded necessary relaxation is feasible for all 353
allowed values. It does not impose overlap consistency, provide an adjacency
matrix, or contradict the stronger lattice exclusion. The current bound
remains `n3>=708`, and target existence remains `UNKNOWN`. See
`agents/2026-07-23-wave23-weighted-extensions.md` and
`verification/wave23-weighted-extensions/2026-07-23T202156Z-audit.md`.

## Next-endpoint lattice boundary (`VERIFIED_INCONCLUSIVE`)

At the first surviving endpoint `n3=708`, the same rank-44 endomorphism has

```text
B = I+2C,
tr(B)=60,
tr(C)=8.
```

Because `C` is integral and self-adjoint for a positive Gram form, its
nonzero eigenvalues are real and their product is a nonzero integer. If their
number is `r`, AM--GM and Cauchy give

```text
tr(C^2) >= r,
tr(C^2) >= 64/r,
tr(C^2) >= 8,
tr(B^2) >= 108.
```

For every real `x>-1/2`, `x!=0`, an exact calculus argument proves

```text
log(1+2x)
  <= x log(3) - (log(3)-2/3) log|x|.
```

Summing over the nonzero eigenvalues and using their integral
pseudodeterminant yields

```text
det(B) <= 3^8 = 6561.
```

The factorization `det(B)=h det(Q)`, the floor `det(Q)>=5`, and the
scaled-dual conditions reduce the endpoint to exactly

```text
h in {9,21,49,81,189,441,729,1029}.
```

The harmonic local identities separately imply `q(T)<=11` and permit at most
one triangle with `q(T)=11`. A scalar profile with 221 values equal to two
and ten equal to three still survives.

Most importantly, the remaining abstract lattice conditions are genuinely
feasible. With `E8` the even unimodular rank-eight Gram matrix and
`A2=[[2,-1],[-1,2]]`, define

```text
S = E8^5 direct_sum A2^2,
Q = (E8^-1)^5 direct_sum A2^2,
G = 21 S^-1,
B = S Q.
```

Exact 44-by-44 arithmetic gives

```text
det(S)=h=9,
det(Q)=9,
det(B)=81,
tr(B)=60,
S G=21I,
G B=21Q,
B=I (mod 2),
minimum(G)>=14.
```

This is a hostile control against overclaiming the lattice route. It is not a
primitive sublattice of `Z^231`, a 231-row projector-frame realization, a
matrix with proved `W=M o M` origin, or a graph. Thus `n3=708` remains open
inside the project, and a further contradiction must use one of those omitted
structural bridges. See
`agents/2026-07-23-wave24-n3-708-index-boundary.md` and
`verification/wave24-n3-708-index/2026-07-23T204222Z-audit.md`.

A proof-separated source audit found no exact match for `n3=708`,
`det(B)<=3^8`, the ordered eight-value index list, or the complete logarithmic
argument in its frozen searches. It records Knill's general
pseudodeterminant work and Bacher--Venkov's rational-idempotent lattice
construction as conceptual prior art, not exact target matches. This is
bounded non-discovery; novelty and priority remain `UNKNOWN`. See
`verification/wave24-literature-audit/2026-07-23-wave24-literature-audit.md`.

The combined detached Waves 21-24 publication replay is
`verification/2026-07-23-wave24-clean-clone.md`. It records 278 passing tests,
15 byte-identical regenerated files, seven exact manifests, metadata and
unpublished-history privacy checks, a clean tracked tree, and Git object
integrity at integration commit
`4111abeea284d218af31cfb7d37ec8a697400998`.

## Strict first-endpoint arithmetic (`VERIFIED_INCONCLUSIVE`)

Wave 25 excludes the only equality case in the Wave 24 trace-square bound.
If `tr(C^2)=8`, equality in the rank and Cauchy estimates gives

```text
C^2=C,
spectrum(C)={1^8,0^36}.
```

Because `C` is integral, its image and kernel split `Z^44` in a unimodular
adapted basis. Self-adjointness for the positive Gram matrix `G` makes that
split orthogonal. On the hypothetical equality case's rank-36 kernel block,

```text
Q0=G0/21,
S0=21G0^(-1)=Q0^(-1).
```

Both `Q0` and `S0` are even integral positive-definite forms, so `Q0` would
be even unimodular of rank 36. This contradicts the standard theorem that
the signature of an even unimodular lattice is divisible by eight. The
restriction to this equality-case kernel block is essential: globally
`SQ=B`, not `I`, and the identity `S=Q^(-1)` is false.

Trace parity and the excluded equality case now give

```text
tr(C^2) >= 10,
tr(B^2) >= 116,
det(B) < 6561.
```

The congruence `det(B)=1 (mod 4)` first gives `det(B)<=6557`. Exhausting the
323 exact factor pairs allowed by `det(B)=h det(Q)`, the scaled-dual index
conditions, and `det(Q)=1 (mod 4)` sharpens the combined necessary cap to

```text
det(B) <= 6525,
```

uniquely maximized at `(h,det(Q))=(9,725)`. The surviving index set remains

```text
{9,21,49,81,189,441,729,1029}.
```

This stricter arithmetic still does not exclude the endpoint. The exact
Wave 24 `E8^5 direct_sum A2^2` package has `h=9`, `det(B)=81`, and
`tr(C^2)=32`, so it survives all Wave 25 arithmetic. Wave 26 below later
excludes its required projector-frame and Schur-square origins while
preserving the abstract matrices. Thus the project bound remains `n3>=708`,
while Conway-99 existence remains `UNKNOWN`. See
`agents/2026-07-23-wave25-n3-708-strictness.md` and
`verification/wave25-n3-708-strictness/2026-07-23T215549Z-audit.md`.

The proof-separated Wave 25 source audit froze 30 queries before proof
inspection and inspected ten primary or authoritative sources. It found no
exact match for this Conway-99 synthesis, while recording established prior
art for rational-idempotent lattices, rational orthogonal graph lattices, and
the even-unimodular rank theorem. This is bounded non-discovery only; novelty
and priority remain `UNKNOWN`. See
`verification/wave25-literature-audit/2026-07-23-wave25-literature-audit.md`.

The detached Wave 25 publication replay is
`verification/2026-07-23-wave25-clean-clone.md`. It records 39 passing tests,
two byte-identical regenerated JSON files, two exact manifests, 129 verified
status path/hash pairs, scoped link and line-ending checks, zero exact-blob
privacy findings in the release tree and the four-commit unpublished range,
a clean tracked tree, and Git object integrity at integration commit
`156756d4ef98dc7233e29a7f8c9feeb143548197`.

## Explicit `A2` survivor-origin obstruction (`VERIFIED_INCONCLUSIVE`)

Wave 26 uses the realization data omitted by the Wave 24 hostile control.
Suppose the scaled-dual form `S` of an actual 231-row projector frame has an
orthogonal `A2` summand. In a basis displaying that summand,

```text
M=Y S Y^T,
Y^T Y=21 S^(-1),
M_ii=4,
M_ij in {0,1,-1,-2}.
```

The `A2` block of the second identity has energy 42. Since `A2` has six
oriented roots of norm two and no vector of norm four, exactly 21 rows meet
that block in a root. Rows sharing one oriented root have norm-two residuals;
the off-diagonal alphabet and positivity give a fibre cap of three. The total
capacity is therefore only

```text
6*3=18<21.
```

The independent frame verifier reconstructs the contragredient basis change,
the exact root enumeration, the opposite-root edge case, and active `+2` and
missing-frame hostile controls. See
`agents/2026-07-23-wave26-a2-frame-obstruction.md` and
`verification/wave26-a2-frame-obstruction/2026-07-23T225015Z-audit.md`.

A separate cubic/Schur argument does not use the off-diagonal fibre cap. The
same frame block places seven rows on each of the three unoriented root lines,
so their three signed imbalances are odd. The exact cubic Gram form has
eigenvalues `6,9,9`, giving

```text
tr(A2 Q_AA)>=18.
```

Ordered-tensor orthogonality shows that complement and mixed blocks cannot
decrease this compression. For either displayed `A2` block of the explicit
Wave 24 package,

```text
Q_AA=A2,
tr(A2 Q_AA)=tr(A2^2)=10,
```

which is impossible. The independent verifier checks ordered and normalized
symmetric-tensor conventions, cross blocks, basis covariance, row
orientation, and a dropped-frame control. It also proves that `M1=0` is
unnecessary for the numeric floor. See
`agents/2026-07-23-wave26-a2-cubic-obstruction.md` and
`verification/wave26-a2-cubic-obstruction/2026-07-23T231001Z-audit.md`.

These arguments refute the projector-frame and full Schur-square origins of
one explicit abstract survivor. They do not refute its coordinate-lattice
identities, classify all even `h=9` forms, exclude `n3=708`, or resolve
Conway-99. The proposed global cap `det(B)<=3645` remains `UNKNOWN`.

The proof-separated Wave 26 source audit attempted 28 frozen queries and
inspected 15 primary or authoritative sources. General tight-frame,
lattice-eutaxy, spherical-design, SRG-embedding, and Hadamard-Gram machinery
is established prior art, while generic `A2` root data is compatible with
tightness and strong eutaxy. No direct or near-direct match for the
parameter-specific 231-row exclusion was found. This is bounded
non-discovery only; novelty and priority remain `UNKNOWN`. See
`verification/wave26-literature-audit/audit-report.md`.

The detached Wave 26 publication replay is
`verification/2026-07-23-wave26-clean-clone.md`. It records 65 passing tests,
four byte-identical regenerated JSON files, three exact manifests, 151
verified status path/hash pairs, link and line-ending checks, zero exact-blob
privacy findings in the integration tree and three-commit unpublished range,
a clean tracked tree, and Git object integrity at integration commit
`4f1f3be35e712789dcba10fda5ec8d2bc569bc17`.

## A2-summand-free control and orthogonal ADE screen (`VERIFIED_INCONCLUSIVE`)

Wave 27 first supplies a different exact hostile control after Wave 26
excluded the old Wave 24 package's required projector/Schur origins:

```text
S = E8^4 orthogonal_sum E6^2,
Q = (E8^(-1))^4 orthogonal_sum Q6^2,
G = 21 S^(-1),
B = S Q,
C = (B-I)/2.
```

The full integral package satisfies

```text
rank(S)=44,
det(S)=det(Q)=9,
det(B)=81,
tr(B)=60,
tr(C)=8,
tr(C^2)=32,
B=I (mod 2),
G B=21Q.
```

Complete exact root enumeration gives component sizes

```text
240,240,240,240,72,72.
```

An orthogonal `A2` direct summand would contribute a complete connected
six-root component, so none is present, even after an integral basis change.
This is a direct-summand statement only. Each `E6` component contains
embedded `A2` root subsystems, and the positive control deliberately retains
one so the two notions cannot be conflated. The package remains an abstract
arithmetic/lattice candidate: it supplies no 231-row frame, projector,
Schur-square tensor, or graph. See the
[construction report](agents/2026-07-23-wave27-a2free-construction.md) and
[independent audit](verification/wave27-a2free-construction/2026-07-24T001657Z-audit.md).

A separate local optimization is unrestricted within its stated algebraic
class. For the frozen `E6` Cartan form,

```text
Q symmetric, even integral, positive definite
E6 Q=I (mod 2)
  implies
tr(E6 Q)>=14.
```

The displayed `Q6` attains 14. This algebraic minimum is not the
projector-frame cubic minimum. Its verifier records one nonfatal prose
omission: the discovery report needs
`tr(C^2)=tr(C) (mod 2)` when passing from the excluded value two to the next
admissible trace-square value. The theorem and equality witness are
unchanged. See the
[trace report](agents/2026-07-23-wave27-h9-classification.md) and
[independent audit](verification/wave27-h9-classification/2026-07-24T002029Z-audit.md).

The full frame/Schur origin supplies more structure. For an orthogonal
integral summand `R`, the projected rows obey

```text
sum_i z_i z_i^T=21R^(-1),
sum_i z_i=0.
```

Repeated coordinates of the symmetric cubic tensor consequently lie in an
explicit affine parity lattice. Exact rational affine-CVP enumeration gives
empty closed balls through energy 18 for `E6` and through energy 60 for
`A6`. The zero-sum identity makes the actual cubic energy divisible by six,
so the safe floors are

```text
orthogonal E6 cubic energy >=24,
orthogonal A6 cubic energy >=66.
```

The complementary positive compression has trace at least its rank. Hence a
rank-six component has local trace at most `60-38=22`, contradicting the
`E6` floor, while the `A6` floor already exceeds the full trace 60. Arbitrary
cross-block entries in `Q` are allowed. These theorems require an orthogonal
summand; an embedded nonorthogonal root subsystem is outside their scope.
In particular, the algebraic trace-14 `E6` block is a valid hostile control
for the weaker arithmetic problem and is rejected only after the cubic
origin is imposed.

The frozen core ADE census first tests the necessary integrality of
`21R^(-1)`. Among all irreducible simply-laced Cartan forms through rank 44,
only

```text
A2, A6, A20, E6, E8
```

pass. The Wave 26 `A2` theorem and the Wave 27 `A6`/`E6` tensor theorems
leave exactly

```text
h=21, A20 orthogonal_sum E8^3
```

among the 17 full rank-44 ADE decompositions. This was the sole survivor of
the frozen **core** screen, not a claimed realization.

A later, separately frozen orchestrator addendum factors the path Cartan
matrix as

```text
A_n=e_1e_1^T+e_ne_n^T
    +sum_(i=1)^(n-1)(e_i-e_(i+1))(e_i-e_(i+1))^T.
```

For every even integral positive-definite `Q`,

```text
tr(A_n Q)>=2(n+1).
```

At `n=20`, the local floor 42 plus the rank-24 complement floor 24 gives
`66>60`, excluding an orthogonal `A20` summand. Thus the core
`A20 orthogonal_sum E8^3` survivor is removed only by this later addendum.
The independent audit preserves that chronology and verifies both packages
separately. See the
[core tensor report](agents/2026-07-23-wave27-general-root-tensor.md),
[later A20 addendum](agents/2026-07-24-wave27-a20-trace-addendum.md), and
[independent combined audit](verification/wave27-general-root-tensor/2026-07-24T010548Z-audit.md).

Combining the component results gives the conditional statement

```text
full n3=708 projector/Schur endpoint identities
and S is a full orthogonal ADE root lattice
  implies
no n3=708 endpoint package.
```

This does not classify general even rank-44 scaled-dual lattices. Such a
lattice may be glued, non-root, or otherwise not an orthogonal ADE sum, so
the endpoint and all unrestricted `h` rows remain `UNKNOWN`. The project
bound is still `n3>=708`; Conway-99 existence remains `UNKNOWN`.

The proof-separated Wave 27 literature audit executed 56 frozen or separately
frozen service-query pairs and inspected 303 records through 2026-07-24. It
found standard component tables and `A_n` Cartan data as conceptual precedent,
but no direct match for the trace-14 optimization, scale-21 cubic
obstructions, A20 use, or exact rank-44 comparison. One frozen interpretation
defect was corrected in a separately retained protocol correction, and failed
zbMATH requests remain failures rather than zero-result evidence. Novelty and
priority remain `UNKNOWN`. See the
[Wave 27 literature audit](verification/wave27-literature-audit/audit.md).
The
[Wave 27 correction ledger](verification/2026-07-24-wave27-orchestrator-corrections.md)
preserves the E6 exposition bridge, the literature-protocol correction, and
the later A20-addendum chronology without rewriting their frozen inputs.

The detached
[Wave 27 clean-source replay](verification/2026-07-24-wave27-clean-clone.md)
records 116 passing tests, seven byte-identical JSON regenerations, all 51
entries of six manifests, 211 status path/hash pairs, scoped link and
line-ending gates, exact-blob privacy checks of the release tree and
seven-commit unpublished range, clean status, and strict Git object
verification at integration commit
`4a2f65d20f8fa403a3a245815799070cf126173f`.

## Wave 28 general-lattice controls

At `n3=708`, write

```text
G=X^T X,
S=21G^(-1),
M=XSX^T,
W=M o M,
Q=X^T W X,
B=SQ=I+2C.
```

Wave 28 keeps this full endpoint package frozen while dropping every
root-lattice, orthogonal-decomposition, strong-modularity, and automorphism
assumption from its generic reductions.

For

```text
h=det(S) in {9,21,49,81,189,441,729,1029},
```

the discriminant group has elementary 3- and 7-primary parts and exact level
`3`, `7`, or `21`. The exact Milgram calculation leaves twelve formal finite
quadratic modules. A primitive root has divisibility one but need not split:
its orthogonal complement has determinant `2h`, and the primitive
root-closure is governed by root-preserving isotropic glue against a rootless
complement. The exact projector moments leave 46 one-root coordinate
patterns, reduced to 32 by the cubic-energy bound. These are necessary count
patterns, not frame realizations.

The frozen discovery sentence excluding cyclic order-21 invariant factors is
false. The correct statement is:

```text
no p-primary cyclic factor has order p^2 or higher;
invariant factors divide 21 and may have order 21.
```

The independent
[glue audit](verification/wave28-glue-discriminant/audit.md) verifies the
corrected primary decomposition and every downstream finite calculation. It
excludes no determinant row.

The theta lane proves the exact generic level, character, Poisson/Weil, Sturm,
and modularity-veto statements and constructs the bare control

```text
S0=K12 orthogonal_sum LAMBDA(F),
det(S0)=729,
min(S0)=4,
r_S0(2)=0,
r_S0(4)=147636,
min(21S0^(-1))=28.
```

The rooted lattice `E6^6 orthogonal_sum E8` has the same finite discriminant
quadratic module and Weil representation but 672 roots. Hence these bare
lattice/theta data do not determine the root coefficient. The complete
fraction-free enumeration of the 32-dimensional component visits 15,053,011
closed-ellipsoid nodes. See the
[theta audit](verification/wave28-theta-modular/audit.md). Neither comparison
object includes the marked 231-vector frame.

Finally, a simultaneous two-neighbor transformation of the Wave 27 paired
forms produces two exact abstract controls. The preferred control has 568
roots of rank 43 and components

```text
A1^4 orthogonal_sum A5 orthogonal_sum D5 orthogonal_sum D8
  orthogonal_sum E7^3,
```

while the retained initial control has 568 roots of full rank 44. Their
complete matrices, roots, closures, and glue indices pass independent exact
reconstruction. See the
[neighbor audit](verification/wave28-simultaneous-neighbor/2026-07-24-wave28-simultaneous-neighbor-audit.md).

These controls establish sharp boundary information:

```text
bare scaled-dual lattice data do not force roots;
general neighbors need not retain an orthogonal ADE decomposition;
full projector/Schur endpoint compatibility remains UNKNOWN.
```

No Wave 28 object supplies all of `X,M,W,Q,B`. Thus no `h` row, `n3=708`,
or Conway-99 outcome is excluded. The bound remains `n3>=708`, with at least
209,994 induced six-cycles. Corrections and failed routes are collected in
the
[Wave 28 correction ledger](verification/2026-07-24-wave28-orchestrator-corrections.md).
The detached
[clean-clone replay](verification/2026-07-24-wave28-clean-clone.md) verifies
all 88 tests, five byte-identical regenerations, 46 manifest entries, central
metadata, links, exact Git-blob privacy, clean status, and strict object
integrity at integration commit
`4c4d2cb8dec14c7834984d47a7e5b29991891e60`.

## Wave 29 exclusion of the rootless `S0` endpoint origin

Wave 29 tests whether the Wave 28 bare control

```text
S0=K12 orthogonal_sum LAMBDA(F)
```

can carry the full frozen `n3=708` projector/Schur package. Because both
integral summands have minimum four, every norm-four frame row lies wholly in
one summand. The tight-frame trace gives the exact split

```text
K12 rows:       63
LAMBDA(F) rows: 168.
```

After permuting rows, `X`, `M`, `W`, `Q`, and `B` split into matching blocks.
The endpoint determinant bound gives `det(Q)=5`. Evenness rules out a
rank-12 unimodular `Q_K`, so

```text
det(Q_K)=5, det(Q_L)=1,
det(B_K)=3645, det(B_L)=1.
```

The projector row alphabet and cubic trace identity make both block traces
positive multiples of six. Exact AM--GM leaves only

```text
tr(B_K)=24, tr(B_L)=36.
```

Thus the integral, `G_K`-self-adjoint matrix
`C_K=(B_K-I_12)/2` has trace six. It is not assumed positive semidefinite;
only `B_K=I+2C_K` is positive, so each `C_K` eigenvalue is greater than
`-1/2`. Integral characteristic coefficients make the nonzero
characteristic pseudodeterminant an integer of absolute value at least one.
The full-domain logarithmic inequality then gives

```text
det(B_K)<=3^6=729,
```

contradicting `det(B_K)=3645`.

The
[independent audit](verification/wave29-s0-frame-exclusion/audit.md)
reconstructs the proof with 27 hostile tests and a byte-identical result. The
[source audit](verification/wave29-s0-literature-audit/audit.md) logs 81
queries and finds no exact combined precedent, without asserting novelty.
Corrections and packaging chronology are retained in the
[Wave 29 correction ledger](verification/2026-07-24-wave29-orchestrator-corrections.md).

The detached
[clean-clone replay](verification/2026-07-24-wave29-clean-clone.md) verifies
all 45 tests, two byte-identical regenerations, 19 manifest entries, central
metadata, repository-wide links, exact Git-blob privacy, clean status, and
strict object integrity at integration commit
`ae8fd70baaeb35302f957653e20ad710e5e77281`.

This excludes one exact `S0` endpoint origin only. Other determinant-729
lattices, the full `h=729` row, `n3=708`, Conway-99, and novelty remain
`UNKNOWN`.

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
