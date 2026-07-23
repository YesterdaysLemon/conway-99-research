# Conway 99 Research

An open, reproducible research project on the existence of a strongly regular
graph with parameters `srg(99,14,1,2)`.

> **Research disclaimer:** This repository contains exploratory research and
> internally checked candidates, not peer-reviewed mathematical results.

## Frozen target

Determine whether there is a finite simple undirected graph on 99 vertices in
which every vertex has degree 14, every adjacent pair has exactly one common
neighbor, and every nonadjacent pair has exactly two common neighbors.

For a symmetric binary adjacency matrix `A` with zero diagonal, the target is
equivalently

```text
A^2 = 12 I - A + 2 J.
```

John H. Conway phrased the question as asking for a 99-vertex graph in which
every edge belongs to a unique triangle and every nonedge belongs to a unique
quadrilateral. See [CONJECTURE.md](CONJECTURE.md) for conventions, equivalences,
and the normalized search problem.

## Current status

- **Literature status:** no resolution found in the sources searched through
  2026-07-23; this is not a proof of openness.
- **Project status:** `EXPLORATORY`.
- **Resolution claim:** none.
- **Strongest internally verified conditional bound:** `n3>=708`, hence at
  least `209,994` induced six-cycles; this does not resolve existence.
- **Symmetry policy:** no nontrivial automorphism, transitivity, Cayley, or
  circulant assumption is imposed on the full search.

A peer-reviewed 2025 paper calls existence an open problem. Two independent
freshness searches through 2026-07-23 found no credible construction or
nonexistence proof. Current 2026 SAT work reports an unsuccessful computation,
and a June 2026 lecture notice discusses only a possible similar approach.
Those searches are evidence about the literature, not a mathematical proof of
openness or novelty.

A 2022 technical-report paper does state a nonexistence theorem, but two
independent project audits find that its decisive equation (88) assumes a false
uniform residual degree. Exact reconstruction gives residual-cut degrees
`1^20,2^51` and corrected count `122=2(71)-20`, rather than the asserted 142.
This refutes the displayed proof step, not the nonexistence statement itself;
both existence outcomes remain `UNKNOWN`.

Wave 3 added three advances, with independently checked structural and
proof-pipeline components, without changing the target status. First, cited
results force an induced six-vertex `N3` configuration in every putative graph;
a project derivation shows that each of its two central diagonal nonedges
2-percolates the whole graph. Second, exact mate-fiber coupling identities and
a conditional alpha-22 projector formulation sharpen the structural search.
Third, the native-cardinality model now has a source-built
Exact-to-VeriPB-to-CakePB certificate path. Its small positive and negative
controls pass. A 10-second full target log is itself verified to have
`NO CONCLUSION`, so it is explicitly non-evidentiary. See the
[Wave 3 audit](verification/2026-07-22-wave3-audit.md) and
[proof-pipeline calibration](verification/2026-07-22-veripb-calibration.md).

Wave 4 turns the derived universal `N3` consequence into a separately verified
target normalization: after safe global relabeling it is the single residual
unit `+24`. The unbranched `--n3` formula is equisatisfiable conditional on the
derived occurrence claim and assumes no completed-graph automorphism. Wave 4
deliberately rejected the legacy 11 representatives because their interaction
with the smaller stabilizer had not yet been proved. See the
[N3 audit](verification/2026-07-22-n3-normalization-audit.md).

Wave 5 supplies that missing joint analysis on the invariant shared fiber
`S_2`. The normalized stabilizer has order 768, and its action partitions the
945 compatible fiber matchings into exactly 12 verified orbits. A strict
standalone checker independently reconstructs the full stabilizer, cover,
Burnside checksum, representatives, and SAT literals. All 12 proof-producing
five-second scouts ended in checked `NO CONCLUSION`, so the target remains
`UNKNOWN`. See the
[joint-cover audit](verification/2026-07-22-n3-joint-cover-audit.md),
[certificate](verification/n3-joint-cover/n3-joint-cover.json), and
[clean-clone replay](verification/2026-07-22-wave5-clean-clone.md).

Wave 6 adds a verified 78-case second-stage refinement and a new conditional
structural bound. The oriented stabilizer has order 384 and partitions the
`945 * 11 = 10,395` matching/common-neighbor states into 78 exact orbits; its
standalone checker reproduces the parent and refined covers, literal mapping,
orbit-stabilizer data, and Burnside sum 29,952. Separately, an auxiliary graph
on the 693 graph edges gives the project derivation

```text
n3 >= 24,
induced_C6_count >= 209,310.
```

The bound uses the cited-and-derived theorem forcing an `N3` in the Conway
target and has passed an independent adversarial audit. Bounded runs on all
12 parent branches and an incremental scout of all 78 refined cases still
ended `UNKNOWN`; checked partial proof traces say only `NO CONCLUSION`. See the
[refined-cover audit](verification/2026-07-22-n3-refined-cover-audit.md),
[N3-count audit](verification/2026-07-22-n3-count-bound-audit.md), and
[Wave 6 clean replay](verification/2026-07-22-wave6-clean-clone.md).

Wave 7 strengthens the conditional structural bound by studying an auxiliary
graph on the 231 graph-triangles and its incidence with the support of the
Wave 6 graph `H`. Two independent exact enumerators exclude the extremal
values 24 and 27, giving

```text
n3 >= 30,
induced_C6_count >= 209,316.
```

The finite reduction, crossing multiplicities, and clean-source replay all
passed independent audits. This is a necessary condition, not a construction
or nonexistence proof; Conway-99 remains `UNKNOWN`. See the
[Wave 7 derivation](agents/2026-07-22-wave7-triangle-side-incidence.md),
[side-incidence audit](verification/2026-07-22-n3-side-incidence-audit.md),
[precise-status search](agents/2026-07-22-wave7-status-search.md), and
[clean replay](verification/2026-07-22-wave7-clean-clone.md).

Wave 8 excludes the remaining equality case `n3=30` without assuming a
completed-graph automorphism or classifying cubic graphs. A fixed-original-
vertex incidence identity and point-clique edge budget reduce the case to a
forbidden `H`-degree one, giving

```text
n3 >= 33,
induced_C6_count >= 209,319.
```

An adversarial proof reconstruction returned `PUBLISH`; a separate slow
standard-library audit generated all 21 cubic complement types and all
674,880 point-clique families, with zero surviving exact-two covers. Lou and
Murin's 2014 report is now explicitly credited for the upstream fixed-
triangle partner equations and `q!=1` gap; no novelty is claimed for those
facts. See the [Wave 8 derivation](agents/2026-07-22-wave8-n3-equality.md),
[equality audit](verification/2026-07-22-n3-equality-audit.md),
[status/prior-art audit](agents/2026-07-22-wave8-status-search.md), and
[clean replay](verification/2026-07-22-wave8-clean-clone.md). Conway-99 itself
remains `UNKNOWN`.

Wave 9 excludes the next equality case `n3=33`. The active-triangle arithmetic
has two profiles. A labeled crossing-graph lemma rules out active singleton
points and eliminates the mixed profile; in the all-`q=2` profile,
point-clique resources force either three saturated `K5` components or one
`K5` plus `K6` minus a perfect matching, and both alternatives contradict the
allowed `H`-degrees. This gives

```text
n3 >= 36,
induced_C6_count >= 209,322.
```

The overlap, actual-edge, disconnected, and residual-matching steps passed an
independent adversarial reconstruction. A compact standard-library checker
replays every finite case split. A separate two-implementation census rejects
all 610 admissible point-clique families across 266 quartic types, and a
detached no-local clone passes all tests and both census programs at the
frozen commits. See the
[Wave 9 derivation](agents/2026-07-22-wave9-n3-33-equality.md),
[equality audit](verification/2026-07-22-n3-33-equality-audit.md), and
[clean replay](verification/2026-07-22-wave9-clean-clone.md). A focused
[status search](agents/2026-07-22-wave9-status-search.md) found no checked
exact hit but explicitly leaves novelty `UNKNOWN`. The result is a conditional
necessary bound, not a resolution; Conway-99 remains `UNKNOWN`.

Wave 10 excludes `n3=36`. After singleton points eliminate both mixed active
profiles, the all-`q=2` complement `K` is 5-regular on twelve triangles. Local
crossing constraints leave point types `222`, `223`, `224`, and `233`. A
common-point rule, an open-twin obstruction in a cubic line graph, and exact
SRG common-neighbor saturation eliminate all points of sizes three and four.
The remaining size-two incidence forces `K=2K6`; each component then induces
the rook graph `L(K3,3)=srg(9,4,1,2)`, whose `lambda` and `mu` counts are
already saturated. This gives

```text
n3 >= 39,
induced_C6_count >= 209,325.
```

The first draft's unjustified closed-`K5` shortcut is retained and repaired in
the proof report. A compact checker covers every finite local step. Two
independent support enumerators recover the same 216 abstract survivors and
show that each violates rook saturation in eighteen places, leaving zero.
See the [Wave 10 derivation](agents/2026-07-22-wave10-n3-36-equality.md),
[equality audit](verification/2026-07-22-n3-36-equality-audit.md), and
[clean replay](verification/2026-07-22-wave10-clean-clone.md). The result is
again only a conditional necessary bound; Conway-99 remains `UNKNOWN`.

Wave 11 excludes `n3=39`. Singleton forcing removes the three mixed active
profiles, leaving thirteen active triangles, all with `q=2`, and a 6-regular
complement `K`. Point-hypergraph linearity and the common-point rule give an
expansion bound of four on every active point set. Exact singleton-side
crossing witnesses then eliminate sizes four and three; if every point has
size two, the total incidence 39 has impossible parity. Thus

```text
n3 >= 42,
induced_C6_count >= 209,328.
```

The first proof exposition failed audit because it did not explicitly carry
the premise `K=overline(L)` into the singleton-crossing step. The first compact
checker also hid a six-profile overlap and had weak semantic mutation tests.
Both failures and their repairs are public. Two independent implementations
now replay 8,907 premise-bound records with combined SHA-256
`452850018ad13362694f5bfff2e4beac03288a113a0391c3456a47cd6fbfe9a1`.
See the [Wave 11 derivation](agents/2026-07-22-wave11-n3-39-equality.md),
[adversarial audit](verification/2026-07-22-n3-39-equality-audit.md), and
[local replay audit](agents/2026-07-22-wave11-local-replay-audit.md). A
[clean-source replay](verification/2026-07-22-wave11-clean-clone.md) records
the initial LF/CRLF portability failure and the byte-stable repair. No
checked source was found for the exact exclusion, but novelty remains
`UNKNOWN`; the Conway-99 target itself also remains `UNKNOWN`.

Wave 12 excludes `n3=42`. Exact active-profile arithmetic leaves an all-`q=2`
case on fourteen triangles after a new degree-three point-clique obstruction.
Expansion and fixed-point arguments eliminate active points of sizes four and
three. In the remaining all-size-two case, the 21 point objects are the edges
of a cubic triangle-free graph `F` on fourteen labels. An independent GENREG
catalog plus a direct disconnected census matches all 112 types in the nauty
catalog; a mandatory-`K` filter leaves four, and independently generated and
replayed support-factor rejection trees leave zero.
Consequently,

```text
n3 >= 45,
induced_C6_count >= 209,331.
```

This remains a conditional necessary bound, not a Conway-99 resolution. The
official GENREG archive used for the cross-catalog audit has no stated
redistribution license, so it is fetched from its official URL and checked by
SHA-256 rather than committed. See the [Wave 12 proof reduction](agents/2026-07-22-wave12-n3-42-proof-a.md),
[support audit](verification/2026-07-22-n3-42-support-audit.md), and
[final integration audit](verification/2026-07-22-wave12-integration-audit.md).
No checked source was found for the exact exclusion; novelty and Conway-99 both
remain `UNKNOWN`.

Wave 13 conditionally excludes `n3=45`. Exact partitioning of
`sum q(T)=30` gives nine raw active profiles. The inherited degree and
point-clique obstructions leave a mixed order-fourteen profile and an
all-`q=2` order-fifteen profile. The mixed case is eliminated by its local
crossings and a cubic `K3,3`/open-twin obstruction. In the order-fifteen
case, flower arguments reduce every active point to size two or three; the
four possible size-three modes are then reduced to modes `122` and `222`.
Every vertex of the auxiliary graph `H` consequently has degree zero or four,
contradicting `|E(H)|=45` by the handshake lemma. Thus

```text
n3 >= 48,
induced_C6_count >= 209,334.
```

Two independent semantic verifiers reconstruct the human proof, including a
blind verdict frozen before comparison. The discovery SAT scan is not used in
that proof: its 17 negative rows remain `UNSAT_UNVERIFIED`. The first
computational bundle failed audit because its census and validator were not
self-sufficient; that failure remains public, followed by a separate repair
and fresh 17/17 formula, 31-mutation, and clause-by-clause audit. See the
[Wave 13 proof](agents/2026-07-22-wave13-n3-45-proof-a.md),
[first proof audit](verification/2026-07-22-wave13-n3-45-audit.md),
[blind proof audit](verification/2026-07-22-wave13-n3-45-audit-b.md), and
[computation-repair audit](verification/2026-07-22-wave13-computation-repair-audit.md).
This is a conditional necessary bound, not a Conway-99 resolution. No checked
source was found for the exact strengthening; novelty and the target remain
`UNKNOWN`.

Wave 14 analyzes the remaining equality frontier `n3=48` but does not exclude
it. Exact partitioning of `sum q(T)=32` gives twelve active profiles; inherited
degree and point-clique obstructions leave three. Human reductions eliminate
the mixed order-fourteen and order-fifteen profiles. The surviving case has
sixteen active triangles, `q=2` everywhere, a 9-regular complement `K`, and
active point sizes two or three. Eight aligned size-three modes remain, every
edge-auxiliary `H`-degree is zero or four, and a support graph `R` has degree
equal to point size with exact twofold rectangle coverage of `L`.

Those conditions are a sharp residual, not a contradiction. A checked
all-size-two object satisfies the stated active/local/support relaxation, and
a separate active-local SAT lane retains the exact raw status split
`1 SAT_CANDIDATE / 7 UNSAT_UNVERIFIED / 1 BUDGET_UNKNOWN / 2 TIMEOUT_UNKNOWN`.
The negative solver rows have no checked proof traces and are not evidence.
See the [Wave 14 reduction](agents/2026-07-22-wave14-n3-48-proof-a.md),
[proof audit](verification/2026-07-22-wave14-n3-48-proof-audit.md),
[computation audit](verification/2026-07-22-wave14-n3-48-computation-audit.md),
and [status audit](verification/2026-07-22-wave14-status-audit.md). The strongest
verified project bound therefore remains `n3>=48` and
`induced_C6_count>=209334`; exclusion of equality, Conway-99, and novelty are
all `UNKNOWN` at this checkpoint.

Wave 15 closes that residual by bringing back a global SRG constraint. Let
`X` be the original vertices whose active point `S_u` is nonempty. The Wave 14
incidence count gives `|X|<=24`. A point of size `s` supplies `2s` distinct
active-triangle neighbors inside `X`. Size-three points therefore already
have six; a size-two point has four such neighbors plus two distinct support
neighbors that cannot meet it in an active triangle. Hence
`delta(G[X])>=6`.

For every `m`-vertex induced subgraph of an `srg(99,14,1,2)`, the largest
nontrivial eigenvalue gives

```text
2e(X) <= 3m + m^2/9.
```

Minimum degree six would require `2e(X)>=6m`, forcing `m>=27`, contrary to
`m<=24`. An independent outside-common-neighbor second-moment calculation
gives the same contradiction. Two discovery lanes reached the obstruction
independently, and two adversarial verifiers reconstructed the delicate
point-to-original-vertex and meeting/support bridges. Therefore

```text
n3 >= 51,
induced_C6_count >= 209,337.
```

See the [global-lift proof](agents/2026-07-23-wave15-global-lift.md),
[global-lift audit](verification/2026-07-23-wave15-global-lift-audit.md),
[independent algebraic proof](agents/2026-07-23-wave15-algebraic.md), and
[algebraic audit](verification/2026-07-23-wave15-algebraic-audit.md). The
initial global certificate had a Windows CRLF/public-LF hash mismatch; failed
baseline `522260a` and repair `874af27` preserve that provenance. The Wave 14
active relaxation object remains valid in its narrow scope, while every lift
of the audited residual to a full target graph is excluded. This is still a
conditional necessary bound, not a resolution: Conway-99 and novelty remain
`UNKNOWN`.

Wave 16 excludes the next equality `n3=51` without assuming the Wave 14
point-size classification. Exact `sum q=34` partitioning and the audited
`d_K>=4` obstruction leave four profiles with `14<=r<=17` and only
`q=2,3`. If `X={u:S_u is nonempty}`, indexed incidence gives

```text
|X| <= floor(3r/2) <= 25.
```

A point of size at least three has six distinct active-triangle neighbors.
At a size-two point, the two-sided crossing law makes every meeting crossing
zero and every positive disjoint crossing a four-edge `K_(2,2)`. The fixed
sum `2(q(i)+q(j))` therefore supplies two positive nonmeeting neighbors for
type `(2,2)`, excludes mixed type `(2,3)`, and supplies three for `(3,3)`.
Thus every vertex of `G[X]` has at least six neighbors in `X`.

The same exact spectral bound used in Wave 15 requires `|X|>=27`, a
contradiction. Since `3|n3`, the new internally verified necessary bounds are

```text
n3 >= 54,
induced_C6_count >= 209,340.
```

The [structural proof](agents/2026-07-23-wave16-n3-51-structural.md) and
[independent audit](verification/2026-07-23-wave16-n3-51-structural-audit.md)
explicitly rule out hidden point-size, global `H`-degree, and support-graph
assumptions. The separate [computational audit](verification/2026-07-23-wave16-n3-51-computation-audit.md)
rebuilds seven active-local CNFs and one positive relaxation candidate, but
its `1 UNSAT_UNVERIFIED`, `5 TIMEOUT_UNKNOWN`, and historical
`1 BUDGET_UNKNOWN` are not evidence for the proof. Baseline `09c20e6` and
repair `7530cae` preserve a transient Wave 15 input-hash failure and its
public-provenance correction. Conway-99 and novelty remain `UNKNOWN`.

The [Wave 16 status search](agents/2026-07-23-wave16-status-search.md) and
[independent status audit](verification/2026-07-23-wave16-status-audit.md)
checked exact numbers, alternate terminology, recent citations, corrections,
maintained tables, current preprints, and the June 2026 Shpectorov lecture
notice. They independently recover the published identity
`induced_C6_count=209286+n3` and find no source for `n3>=54` or `209340`.
That nonhit is not a novelty certificate: the target and novelty both remain
`UNKNOWN`.

Wave 17 excludes the sharp equality `n3=54`. Exact `sum q=36` profile
filtering first removes every profile with at most 17 active labels. Equality
forces 18 active labels, 27 active original vertices, and a 6-regular induced
subgraph giving the equitable partition

```text
[[6,8],
 [3,11]].
```

The 27 active vertices become the edges of a simple cubic triangle-free graph
`F` on 18 labels. Their two remaining neighbors form a 2-factor `R` on
`E(F)`, with exact rectangle identity

```text
N A_R N^T = 2 A_L.
```

An independently audited parity argument excludes `F=3K3,3`. The remaining
finite universe is 455 connected order-18 cubic graphs of girth at least five
and two graphs `K3,3` plus a connected order-12 component, using the official
House of Graphs catalogs. For the 455 connected cases, a binary parity kernel
is trivial in 443 cases; all vectors in the other 12 kernels are exhaustively
checked, with none giving point-degree two. In the two mixed cases, degree
counting forces nine internal order-12 support edges although only one or zero
compatible candidates exist. A separately written verifier reconstructed all
457 cases, fetched and hash-validated the official catalog bytes, and passed
17 hostile tests. The earlier 457 raw SAT `UNSAT` statuses have no proof
traces and are not used.

Consequently the internally verified conditional necessary bounds are

```text
n3 >= 57,
induced_C6_count >= 209,343.
```

See the [structural reduction](agents/2026-07-23-wave17-n3-54-structural.md),
[structural audit](verification/2026-07-23-wave17-n3-54-structural-audit.md),
[exact census](agents/2026-07-23-wave17-n3-54-census.md),
[independent census audit](verification/2026-07-23-wave17-n3-54-census-audit.md),
[status search](agents/2026-07-23-wave17-status-search.md), and
[status audit](verification/2026-07-23-wave17-status-audit.md). Catalog
completeness and one representative per isomorphism class remain official
external premises; no local generator proof is claimed. Current sources still
describe Conway-99 as unresolved, and exact prior-art searches found no
`n3>=57`, `n3=54` exclusion, or `209343` threshold. Those nonhits do not
establish novelty. Conway-99 and novelty remain `UNKNOWN`.

Wave 18 independently excludes the next equality `n3=57`, without importing
the Wave 17 census. The exact `sum q=38` filter leaves nine active-label
profiles. Profiles with at most 17 active labels have at most 25 active
original vertices, contradicting the spectral minimum of 27. At `r=18`,
incidence and spectral equality force 27 size-two points and a 6-regular
induced subgraph; the two surviving label profiles are excluded by parity and
the endpoint-local `(2,4)` degree bound. At `r=19`, the only label profile is
`q=2^19`. Exact point-size excess leaves three cases at 27 active vertices and
one case at 28; the former contradict 6-regularity or the fixed-point sum, and
the latter forces degree sum at least 172 against the spectral upper cap 170.

The discovery suite passes 10 focused tests. A separately written checker
reconstructs the nine profiles, crossing tables, point-size partitions, and
exact rational spectral bounds; it passes 14 hostile tests and detects all 24
frozen mutations. Combining this independently verified exclusion with Wave
17 gives

```text
n3 >= 60,
induced_C6_count >= 209,346.
```

See the [Wave 18 structural report](agents/2026-07-23-wave18-n3-57-structural.md)
and [independent structural audit](verification/2026-07-23-wave18-n3-57-structural-audit.md).
This remains a conditional necessary bound over the audited active-triangle
framework, not a raw 99-by-99 certificate, formal proof, target resolution, or
novelty determination. Conway-99 and novelty remain `UNKNOWN`.

The [Wave 18 status search](agents/2026-07-23-wave18-status-search.md) and
[independent source audit](verification/2026-07-23-wave18-status-audit.md)
checked current maintained tables, primary papers, exact numerical searches,
the 2022 purported proof, and Ben Baker's May 2026 conference abstract. They
found no exact published `n3=57` exclusion, `n3>=60`, or `209346` bound. The
generic spectral subset-edge inequality is standard Rayleigh/Alon--Chung prior
art; no exact prior match to the active-set endpoint argument was located.
Those focused nonhits are not a novelty certificate.

Wave 19 excludes the next equality `n3=60`. The equality reduction first
eliminates the remaining `m=27` prism and `K3,3` point profiles by exact
witness multiplicity. At `m=30`, it reduces the residual to a triangle-free
cubic graph `F` on 20 labels, a symmetric family of local six-cycles, a
2-factor `R`, and at most three extra point edges `Z`. The released census
checks all 510,489 connected cubic catalog records and all 177 disconnected
types. Only the two-Petersen residual reaches the final Gram stage.

For that residual, all 120 `L/R` models form one orbit. The exact search covers
all 748,825 nonempty labeled `Z` placements through three edges, leaving 8,935
entrywise survivors, 66 symmetry orbits, and 16 PSD Gram systems. Fifteen are
exactly inconsistent. The last has an integer Farkas separator of target
value `-6` whose 232 support scores are all nonnegative. A separately written
verifier reproduces every catalog disposition, orbit, Gram system, and hostile
mutation, then replays the submitted checker in an isolated canonical-path
sandbox. Its verdict is the conditional bound

```text
n3 >= 63,
induced_C6_count >= 209,349.
```

See the [Wave 19 discovery report](agents/2026-07-23-wave19-alternate-frontier.md)
and [independent closure audit](verification/n3-60-closure/2026-07-23T161951Z-final-audit.md).
The official House of Graphs completeness/nonisomorphism assertion is an
explicit external premise; the pinned bytes and every derived case were
independently checked. This is not a target nonexistence proof, formal-kernel
proof, or novelty claim. Conway-99 and novelty remain `UNKNOWN`.

Wave 20 replaces the equality-by-equality frontier with a global
Schur-projector inequality. Let `Gamma` be the intersection graph on the 231
target triangles and let `M=21E` be the integral scaling of its rank-44
orthogonal projector onto the zero eigenspace. Exact incidence arithmetic
gives

```text
M^2 = 21M,
diag(M) = 4,
offdiag(M) in {0,1,-1,-2}.
```

For `W=M∘M`, the matrix `A4=MWM` is positive semidefinite and integral. Every
row is nonzero modulo two, while an alternating-form argument makes every
diagonal entry a positive multiple of four. The exact trace identity is

```text
tr(A4) = 84(n3-693).
```

The 231 positive diagonals force `n3-693>=11`; because `3|n3`, this sharpens
to the independently reconstructed conditional bound

```text
n3 >= 705,
induced_C6_count >= 209,991.
```

The submitted and independent suites pass 18/18 and 16/16 tests and regenerate
their exact JSON outputs byte-identically. See the
[Wave 20 discovery report](agents/2026-07-23-wave20-global-schur.md) and
[adversarial audit](verification/2026-07-23-wave20-global-schur-audit.md).
The proof uses no automorphism, catalog, solver-negative, or floating-point
premise. One frozen failed-routes sentence still names the intermediate 699
endpoint; the operative proof, code, results, audit, and public correction all
use 705.

A separately frozen [Wave 20 source audit](verification/global-schur/2026-07-23T170612Z-status-literature-audit.md)
did not inspect the proof. It verified Reimbayev's six-cycle identity and
Petro--Phillips's triangle-graph spectrum, and found no accepted target
resolution or exact published `705/209991` endpoint through 2026-07-23.
Generic Schur/Krein positivity is established prior art; search non-discovery
does not establish novelty. Conway-99 and exact-specialization novelty remain
`UNKNOWN`.

Wave 21 exhausts a different, published necessary-condition lane without
improving the bound. Exact arithmetic and independent graph-deck
reconstruction align all 62 six-vertex types in arXiv:2508.03377v2 and all 19
Hamiltonian seven-vertex types in arXiv:2511.06572v1. They also expose a narrow
source defect: the printed `m7(n-5)` deletion equation has residual exactly
`n23` because its right-hand side omits `+n23`. An independent verifier tried
every possible missing one-card row and found that this is the unique repair
matching an actual six-vertex deletion deck.

After applying only that named correction, complete integrality and
nonnegativity are exactly

```text
n3 in {0,3,6,...,4158},
h11 = 0 (mod 4),
ceil_to_multiple_of_4(2*n3) <= h11 <= 4*n3.
```

Intersecting with `n3>=705` leaves all 1,152 values
`705,708,...,4158`; at `n3=705`, 353 values of `h11` remain. Thus the
published encoded count systems are internally verified but inconclusive:
feasible count vectors are not graph constructions, and the seven-vertex
source covers Hamiltonian types only. See the
[Wave 21 discovery report](agents/2026-07-23-wave21-six-vertex-lp.md),
[independent audit](verification/wave21-six-vertex-lp/2026-07-23T174137Z-audit.md),
and [orchestrator replay](verification/wave21-six-vertex-lp/2026-07-23T175223Z-orchestrator-replay.md).
The separate [source-status audit](verification/wave21-six-vertex-lp/status/2026-07-23T182843Z-source-status-audit.md)
confirms that the current official arXiv version is still v2 and that both v1
and v2 omit the term; it found no formal correction or corrected
journal/author version in its bounded search. Those nonhits do not establish
novelty.
At the end of Wave 21 the strongest bound was still `n3>=705`; Conway-99 and
novelty remained `UNKNOWN`.

Two independent Wave 21 endpoint audits then refine what a surviving
`n3=705` case would have to look like. For the integral Schur lift
`A4=M(M o M)M`, every triangle satisfies

```text
A4[T,T] >= (99/43)*(q(T)-2)^2,
q(T) <= 8,
tr(A4^2) >= 26460.
```

The exact scalar relaxation still has 22,113 profiles and a simple survivor,
so these are restrictions rather than a contradiction. The parallel
projector-lattice lane defines
`L=im(M) intersect Z^231` and `h=[L:21L*]`. Its determinant factorization,
combined with an independently supplied even-Gram congruence, gives the
sharper necessary endpoint condition

```text
n3=705  ==>  h in {1,9}.
```

At the Wave 21 checkpoint, these lanes did not determine `h`. See the
[local-diagonal audit](verification/wave21-local-diagonal/2026-07-23T185252Z-audit.md)
and [lattice audit](verification/wave21-lattice-extension/2026-07-23T184926Z-audit.md).
Neither lane then changed the bound or target status; Wave 23 later excludes
the entire `n3=705` endpoint by a stronger argument.

Wave 22 tests the complete aggregate order-seven vertex-deletion relaxation at
that historical endpoint. It independently enumerates 394,020 locally
admissible labeled order-seven graphs, forming 208 isomorphism classes, and
builds the complete `62 x 208` deletion matrix. At
`n3=705,h11=2820`, an exact nonnegative integer witness satisfies all 62
deletion rows and all 19 pinned Hamiltonian-type formulas:

```text
sum of all class counts = binom(99,7) = 14,887,031,544
positive support size   = 105
```

This is deliberately a negative result about the strength of the relaxation:
the witness does not consistently assign types to overlapping subsets and is
not a graph. Wave 23 later excludes the same endpoint using stronger lattice
information, so the Wave 22 witness is not evidence for target existence. See
the [Wave 22 report](agents/2026-07-23-wave22-full-seven-deck.md) and
[independent audit](verification/wave22-full-seven-deck/2026-07-23T191133Z-audit.md).

Wave 23 combines the verified global Schur lift with the projector lattice.
At `n3=705`, the positive integral rank-44 endomorphism has
`B=I+2C`, `tr(B)=48`, and `tr(C)=2`. Integral trace parity and
positive-form self-adjointness force

```text
tr(B^2) >= 60.
```

A complete compactness and two-moment determinant audit then proves
`det(B)<13` using exact rational radical brackets for every KKT multiplicity.
The determinant factorization `det(B)=h det(Q)`, the even-Gram congruence, and
the rank-44 even-unimodular signature obstruction eliminate every remaining
index. Thus

```text
n3 != 705,
n3 >= 708,
induced_C6_count >= 209,994.
```

The [Wave 23 discovery report](agents/2026-07-23-wave23-index-pranks.md) and
[blind independent audit](verification/wave23-index-pranks/2026-07-23T192952Z-audit.md)
include separate implementations, 29 exact tests in total, exact
regeneration, and the imported-theorem applicability check. This is a
conditional necessary bound, not a construction or nonexistence proof.
Conway-99 and literature novelty remain `UNKNOWN`.

A structurally independent, shorter proof reaches the same endpoint without
the KKT determinant maximization. Newton's identity and AM--GM on all 946 pair
products give

```text
det(B)^(1/22) <= 51/43,
51^22 < 43^23,
det(B) <= 42.
```

The scaled-dual factorization and congruences then leave no lattice index. Its
[separate audit](verification/wave23-endpoint-crosscheck/2026-07-23T195158Z-audit.md)
passes the proof and 17 independent tests. That audit also caught one
nonblocking discovery-side hostile-control error: `(9,3,27)` violates a
retained determinant residue. The public ledgers preserve and refute the bad
control, replace it with the valid `(9,1,9)` single-relaxation witness, and a
[correction addendum](verification/wave23-endpoint-crosscheck/2026-07-23T200645Z-correction-audit.md)
confirms that the main proof is unchanged.

Another Wave 23 lane strengthens the small-subgraph relaxation rather than
the lattice proof. It independently rebuilds all 208 locally admissible
seven-vertex classes and the complete orbit-refined extension matrix

```text
712 rows x 208 columns
row split: 62 deletion + 207 vertex + 180 edge-pair + 263 nonedge-pair
```

At the now-excluded historical endpoint `n3=705`, this entire encoded system
is exactly feasible for every allowed `h11=4z`, `z=353,...,705`, through a
frozen affine nonnegative integer family. The
[independent weighted-extension audit](verification/wave23-weighted-extensions/2026-07-23T202156Z-audit.md)
reconstructs the census, coefficients, ranks, lower-order gate, all 353
parameter values, and 20 hostile tests without importing discovery code. This
closes that obstruction route negatively: aggregate class counts are not a
graph, and the result neither constructs the target nor changes the current
`n3>=708` bound.

The proof-separated
[Wave 23 literature audit](verification/wave23-literature-audit/2026-07-23-wave23-literature-audit.md)
finds that its inspected current sources still treat the target as open and
locates neither the exact `708/209994` endpoint nor the complete Wave 23
method in 24 frozen query and citation searches. This is bounded
non-discovery, not proof of openness or novelty.

Wave 24 attacks the first surviving endpoint `n3=708`. Here
`B=I+2C` has `tr(C)=8`. The nonzero eigenvalue product of the integral,
real-diagonalizable matrix `C` is a nonzero integer, and an exact pointwise
logarithmic inequality gives

```text
det(B) <= 3^8 = 6561.
```

Combining this with `det(B)=h det(Q)`, `det(Q)>=5`, and the scaled-dual
congruences leaves exactly

```text
h in {9,21,49,81,189,441,729,1029}.
```

The local harmonic argument also gives `q(T)<=11` with at most one
`q(T)=11`. This is not an endpoint exclusion: a complete exact
`E8^5 direct-sum A2^2` coordinate-lattice package survives the current
abstract identities at `h=9`. The
[blind Wave 24 audit](verification/wave24-n3-708-index/2026-07-23T204222Z-audit.md)
reconstructs the proof, verifies every 44-by-44 matrix entry, passes 17
independent tests, and preserves the crucial scope wall. No primitive
`Z^231` embedding, projector/Hadamard origin, Schur-square origin, or graph
is known. The lower bound remains `n3>=708`, and Conway-99 remains `UNKNOWN`.

The proof-separated
[Wave 24 literature audit](verification/wave24-literature-audit/2026-07-23-wave24-literature-audit.md)
finds no exact endpoint, determinant-cap, eight-index-list, or logarithmic
method match in its frozen searches. It records older conceptual prior art
for pseudodeterminants and lattices from rational idempotents, and again
records the concrete layer-counting gap in a 2022 report claiming
nonexistence. Exact-match non-discovery is bounded; novelty and priority
remain `UNKNOWN`.

Wave 2's 10,000-conflict pass over all 11 complete matching branches likewise
returned `UNKNOWN` everywhere. Bounded runs are used only for engineering and
branch ranking. See the [Wave 2 audit](verification/2026-07-22-wave2-audit.md)
and [run manifest](logs/2026-07-22-wave2.json).

## Why the search has 84 vertices

Fix a root `x`. Its 14 neighbors induce seven disjoint edges. Each of the other
84 vertices is canonically labeled by one of the 84 nonedges among those 14
neighbors. The unknown part is therefore a 12-regular graph on those 84 labels,
subject to exact common-neighbor constraints. This normalization removes
labeling redundancy without assuming that a solution has any automorphisms.

## Research lanes

1. **Statement and literature:** freeze definitions, reproduce known
   restrictions, and audit current status.
2. **Structural proof attacks:** derive constraints from the 84-vertex
   residual graph, its incidence matrix, spectra, codes, and local subgraphs.
3. **Construction/counterexample search:** exact-cover, SAT/PB, constraint
   programming, and heuristic candidate generation.
4. **Adversarial verification:** independent checkers, proof certificates,
   small-instance calibration, and explicit attempts to falsify every claim.

The orchestrator keeps discovery and verification separate. Agent prose is not
evidence by itself; only cited mathematics, checked derivations, reproducible
computations, or independently verifiable certificates may raise a claim's
status.

## Evidence labels

| Label | Meaning |
|---|---|
| `CITED` | A precise source is given; the project has not independently proved it. |
| `DERIVED` | A complete human-checkable derivation is recorded. |
| `VERIFIED` | Independent code or formal checking reproduced the claim. |
| `CANDIDATE` | Worth testing; not established. |
| `REFUTED` | A recorded check found a concrete defect or counterexample. |
| `UNKNOWN` | Neither proved nor refuted here. |

## Repository map

- [CONJECTURE.md](CONJECTURE.md): exact target and normalized formulation.
- [STRUCTURE.md](STRUCTURE.md): checked global and rooted consequences.
- [STATUS.yaml](STATUS.yaml): machine-readable project status.
- [CLAIMS.yaml](CLAIMS.yaml): claim and resolution-candidate ledger.
- [OBLIGATIONS.yaml](OBLIGATIONS.yaml): proof and verification obligations.
- [SOURCES.bib](SOURCES.bib): bibliography and provenance.
- [REPRODUCING.md](REPRODUCING.md): reproducibility and certificate policy.
- [PROMPT.md](PROMPT.md): reusable orchestrator/parallel-agent/verifier prompt.
- [First-wave audit](verification/2026-07-22-first-wave-audit.md): adversarial
  verifier verdict.
- [Wave 2 audit](verification/2026-07-22-wave2-audit.md): independent review of
  the structural, algebraic, and native-encoding claims.
- [Wave 3 audit](verification/2026-07-22-wave3-audit.md): independent review of
  the coclique/design, fiber-coupling, and OPB claims.
- [LRAT calibration](verification/2026-07-22-lrat-calibration.md): pinned small
  negative-control proof replay.
- [VeriPB calibration](verification/2026-07-22-veripb-calibration.md): canonical
  OPB fixtures and Exact/VeriPB/CakePB replay.
- [N3 normalization audit](verification/2026-07-22-n3-normalization-audit.md):
  independent orbit, implementation, and safety review.
- [N3 joint-cover audit](verification/2026-07-22-n3-joint-cover-audit.md):
  independent proof of the conditional 12-branch split and strict certificate
  review.
- [N3 refined-cover audit](verification/2026-07-22-n3-refined-cover-audit.md):
  independent proof of the conditional 78-case second-stage split.
- [N3-count audit](verification/2026-07-22-n3-count-bound-audit.md):
  adversarial reconstruction of the auxiliary-edge graph and `n3 >= 24`.
- [N3 side-incidence audit](verification/2026-07-22-n3-side-incidence-audit.md):
  two independent reconstructions and finite checks proving the conditional
  strengthening `n3 >= 30`.
- [N3 equality audit](verification/2026-07-22-n3-equality-audit.md):
  adversarial proof reconstruction and exhaustive secondary audit proving the
  conditional strengthening `n3 >= 33`.
- [N3=33 equality audit](verification/2026-07-22-n3-33-equality-audit.md):
  adversarial reconstruction and exact finite checks proving the conditional
  strengthening `n3 >= 36`.
- [N3=36 equality audit](verification/2026-07-22-n3-36-equality-audit.md):
  repaired adversarial reconstruction and independent support census proving
  the conditional strengthening `n3 >= 39`.
- [N3=39 equality audit](verification/2026-07-22-n3-39-equality-audit.md):
  repaired adversarial reconstruction and two-implementation rooted-flower
  replay proving the conditional strengthening `n3 >= 42`.
- [N3=42 support audit](verification/2026-07-22-n3-42-support-audit.md):
  independent GENREG/nauty cross-catalog check and proof-tree replay excluding
  the final all-size-two support branch.
- [Wave 12 integration audit](verification/2026-07-22-wave12-integration-audit.md):
  adversarial reconstruction of the full conditional reduction and the
  strengthening `n3 >= 45`.
- [Wave 13 `n3=45` audit](verification/2026-07-22-wave13-n3-45-audit.md):
  independent proof reconstruction and finite checks proving the conditional
  strengthening `n3 >= 48`.
- [Wave 13 blind semantic audit](verification/2026-07-22-wave13-n3-45-audit-b.md):
  a separately frozen semantic reconstruction of the same conditional
  exclusion.
- [Wave 13 computation audit](verification/2026-07-22-wave13-computation-audit.md):
  preserved FAIL verdict for the original self-validation bundle, while
  retaining the independently checked formula semantics and positive control.
- [Wave 13 computation-repair audit](verification/2026-07-22-wave13-computation-repair-audit.md):
  fresh 17-formula reconstruction, clause-by-clause positive replay, direct
  provenance, and 31 hostile mutations; solver negatives remain uncertified.
- [Wave 14 `n3=48` proof audit](verification/2026-07-22-wave14-n3-48-proof-audit.md):
  independent reconstruction of the twelve-to-three profile reduction, both
  mixed-profile exclusions, and the exact surviving support residual.
- [Wave 14 computation audit](verification/2026-07-22-wave14-n3-48-computation-audit.md):
  independent reconstruction of all thirteen formula streams, three positive
  relaxation objects, 29 hostile mutations, and the non-evidentiary scan
  status boundary.
- [Wave 14 literature/status audit](verification/2026-07-22-wave14-status-audit.md):
  source-frozen audit of the `N3` notation, hexagon identity, unresolved target
  status, and nonexhaustive novelty search.
- [Wave 15 global-lift audit](verification/2026-07-23-wave15-global-lift-audit.md):
  independent reconstruction of the active-set minimum-degree bridge, spectral
  bound, outside second moment, and conditional exclusion of `n3=48`.
- [Wave 15 algebraic audit](verification/2026-07-23-wave15-algebraic-audit.md):
  blind second audit of the same exclusion plus exact triangle-intersection
  moments and the repaired weighted-moment metadata.
- [Wave 16 structural audit](verification/2026-07-23-wave16-n3-51-structural-audit.md):
  independent reconstruction of the 16-to-4 profile filter, endpoint-local
  crossing bridge, spectral contradiction, and conditional exclusion of
  `n3=51`.
- [Wave 16 computation audit](verification/2026-07-23-wave16-n3-51-computation-audit.md):
  independent seven-CNF reconstruction, positive active-local replay, 38
  hostile mutations, and strict preservation of unknown solver outcomes.
- [Wave 16 literature/status audit](verification/2026-07-23-wave16-status-audit.md):
  independent source-page verification of the current target status, induced
  hexagon identity, exact-number nonhits, and conservative `UNKNOWN` novelty
  label.
- [Wave 17 structural audit](verification/2026-07-23-wave17-n3-54-structural-audit.md):
  independent reconstruction of the equality/equitable-cut reduction, cubic
  point graph, 2-factor identity, component classification, and `3K3,3`
  parity exclusion.
- [Wave 17 exact-census audit](verification/2026-07-23-wave17-n3-54-census-audit.md):
  separate 457-case catalog replay, parity-kernel exhaustion, mixed-component
  degree obstruction, and 17 hostile tests excluding conditional `n3=54`.
- [Wave 17 literature/status audit](verification/2026-07-23-wave17-status-audit.md):
  source-frozen audit of positive intriguing-set terminology, near-match
  exclusions, official cubic-catalog provenance, current status, and
  conservative novelty nonhits.
- [Wave 18 structural audit](verification/2026-07-23-wave18-n3-57-structural-audit.md):
  independent reconstruction of all nine `sum q=38` profiles, the `r=18` and
  `r=19` endpoint cases, exact spectral arithmetic, 14 hostile tests, and 24
  detected mutations excluding conditional `n3=57`.
- [Wave 18 literature/status audit](verification/2026-07-23-wave18-status-audit.md):
  independent primary-source and exact-query audit of current status, the
  Reimbayev identity, focused prior-art nonhits, Baker's abstract, generic
  Rayleigh attribution, and the exact defect in Ishihara's equation (88).
- [Wave 19 independent closure audit](verification/n3-60-closure/2026-07-23T161951Z-final-audit.md):
  independent authentication and reconstruction of the repaired `m=27`
  proof, all 510,489 connected and 177 disconnected cubic cases, the complete
  two-Petersen `Z` census, exact Gram systems, and the final Farkas separator.
- [Wave 20 global-Schur audit](verification/2026-07-23-wave20-global-schur-audit.md):
  blind reconstruction of the triangle-incidence projector, Schur trace,
  integral mod-four lift, 16 hostile tests, and byte-identical replay of all
  18 submitted tests excluding every `n3<705`.
- [Wave 20 literature/status audit](verification/global-schur/2026-07-23T170612Z-status-literature-audit.md):
  proof-separated source/query ledger covering the exact endpoint, equivalent
  projector terminology, current status, 13 pinned sources, and three retained
  access failures without promoting search nonhits to novelty.
- [Wave 20 clean-source replay](verification/2026-07-23-wave20-clean-clone.md):
  detached 18/16/14-test replay, three byte-identical regenerations, exact
  ledger/manifest/hash checks, public-hygiene scans, clean status, and
  `git fsck`.
- [Wave 21 six-/seven-vertex count audit](verification/wave21-six-vertex-lp/2026-07-23T174137Z-audit.md):
  independent 9/21/62/19 local-class reconstruction, explicit source-equation
  correction, exact affine feasibility exhaustion, and 19 hostile tests.
- [Wave 21 orchestrator replay](verification/wave21-six-vertex-lp/2026-07-23T175223Z-orchestrator-replay.md):
  fresh pinned-source downloads, guarded archive extraction, expected raw
  failure, corrected replay, 24 manifest checks, and byte-identical outputs.
- [Wave 21 source-status audit](verification/wave21-six-vertex-lp/status/2026-07-23T182843Z-source-status-audit.md):
  current-version, v1/v2 equation, later-author-source, correction, and
  publication-status checks with pinned bytes and bounded nonhit language.
- [Wave 21 local-diagonal audit](verification/wave21-local-diagonal/2026-07-23T185252Z-audit.md):
  independent tensor, harmonic, trace-square, profile, and spectral-boundary
  reconstruction with 18 hostile tests and byte-identical replays.
- [Wave 21 lattice audit](verification/wave21-lattice-extension/2026-07-23T184926Z-audit.md):
  independent dual/index and determinant reconstruction, theorem audit,
  16 hostile tests, and the exact endpoint strengthening `h in {1,9}`.
- [Wave 22 full seven-deck audit](verification/wave22-full-seven-deck/2026-07-23T191133Z-audit.md):
  independent 62-by-208 deletion system, Hamiltonian alignment, 26 hostile
  tests, and strict replay of the aggregate integer witness.
- [Wave 23 projector-index audit](verification/wave23-index-pranks/2026-07-23T192952Z-audit.md):
  blind reconstruction of the trace-square floor, complete exact determinant
  cap, lattice-index obstruction, 14 hostile tests, and the conditional
  strengthening `n3>=708`.
- [Wave 23 endpoint cross-check audit](verification/wave23-endpoint-crosscheck/2026-07-23T195158Z-audit.md):
  independent pair-product AM--GM proof, exact determinant/index exhaustion,
  17 hostile tests, and transparent identification of one ancillary
  discovery-ledger defect.
- [Wave 23 cross-check correction addendum](verification/wave23-endpoint-crosscheck/2026-07-23T200645Z-correction-audit.md):
  seven-file freeze, corrected hostile witness, byte-identical replay, and
  confirmation that the endpoint proof is unchanged.
- [Wave 23 weighted-extension audit](verification/wave23-weighted-extensions/2026-07-23T202156Z-audit.md):
  independent complete census, 712-row orbit reconstruction, exact affine
  feasibility for all 353 allowed values, and 20 hostile tests.
- [Wave 23 literature/status audit](verification/wave23-literature-audit/2026-07-23-wave23-literature-audit.md):
  current-source status, exact-value and method searches, source/query ledger,
  and bounded non-discovery with novelty left `UNKNOWN`.
- [Wave 24 `n3=708` index-boundary audit](verification/wave24-n3-708-index/2026-07-23T204222Z-audit.md):
  independent pseudodeterminant/log-bound proof, eight-value index
  exhaustion, full abstract lattice certificate, 17 hostile tests, and
  fail-closed separation from a projector or graph realization.
- [Wave 24 literature/status audit](verification/wave24-literature-audit/2026-07-23-wave24-literature-audit.md):
  exact endpoint and method queries, 40 individual index templates,
  conceptual ingredient prior art, and bounded non-discovery.
- [Wave 3/N3 clean-clone replay](verification/2026-07-22-wave3-clean-clone.md):
  frozen-commit tests and byte-identical proof regeneration.
- [Wave 5 clean-clone replay](verification/2026-07-22-wave5-clean-clone.md):
  frozen-commit tests and byte-identical regeneration of all 12 branch OPBs.
- [Wave 6 clean-source replay](verification/2026-07-22-wave6-clean-clone.md):
  frozen-commit tests and byte-identical refined-certificate regeneration.
- [Wave 7 clean-source replay](verification/2026-07-22-wave7-clean-clone.md):
  frozen-commit tests and replay of two independent incidence checkers.
- [Wave 8 clean-source replay](verification/2026-07-22-wave8-clean-clone.md):
  frozen-commit tests and replay of the equality-exclusion arithmetic checker.
- [Wave 9 clean-source replay](verification/2026-07-22-wave9-clean-clone.md):
  frozen-commit tests and replay of the `n3=33` equality-exclusion checker.
- [Wave 10 clean-source replay](verification/2026-07-22-wave10-clean-clone.md):
  frozen-commit tests, certificate replay, and independent regeneration of all
  216 abstract support masks.
- [Wave 11 clean-source replay](verification/2026-07-22-wave11-clean-clone.md):
  frozen-commit tests and byte-identical canonical certificate regeneration,
  including the retained newline-portability failure and repair.
- [Wave 12 clean-source replay](verification/2026-07-22-wave12-clean-clone.md):
  detached full-suite replay, fresh official-catalog download, and
  byte-identical support-certificate regeneration.
- [Wave 13 clean-source replay](verification/2026-07-22-wave13-clean-clone.md):
  detached 52/12/104-test replay and byte-identical census and positive-v2
  diagnostic regeneration.
- [Wave 14 clean-source replay](verification/2026-07-23-wave14-clean-clone.md):
  detached 52/12/104/10/7-test replay, byte-identical regeneration of four
  Wave 14 artifacts, and the preserved pre-release determinism repair.
- [Wave 15 clean-source replay](verification/2026-07-23-wave15-clean-clone.md):
  detached 52/12/104/10/7/5/11/7-test replay, 18 frozen hash checks, and
  byte-identical canonical-LF certificate regeneration.
- [Wave 16 clean-source replay](verification/2026-07-23-wave16-clean-clone.md):
  detached 252-test replay, six semantic checkers, five byte-identical
  regenerations, seven status hashes, public-hygiene scans, clean status, and
  `git fsck`.
- [Wave 17 clean-source replay](verification/2026-07-23-wave17-clean-clone.md):
  detached 318-test replay, 13 semantic computations/checkers, 11
  byte-identical regenerations, nine status hashes, public-hygiene scans,
  clean status, and `git fsck`.
- [Wave 18 clean-source replay](verification/2026-07-23-wave18-clean-clone.md):
  detached 343-test replay, 22 semantic/reproduction commands, 13
  byte-identical regenerations, seven Wave 18 status hashes, public-hygiene
  scans, clean status, and `git fsck`.
- [Wave 19 clean-source replay](verification/2026-07-23-wave19-clean-clone.md):
  detached 7/27/10-test replay, complete independent 510,489-record census,
  byte-identical final certificate, frozen hash checks, clean tracked diff,
  and `git fsck`.
- `agents/`: role prompts and immutable run reports.
- `attempts/`: proof and search attempts, including failed ones.
- `candidates/`: machine-readable candidate objects and quarantined artifacts.
- `verification/`: independent validators and verification reports.
- `code/`: discovery/search code, kept separate from verification code.
- `formal/`: proof-assistant or proof-certificate work.
- `logs/`: run manifests and summarized logs; bulky raw output stays in releases
  or external archives with checksums.

## Primary starting points

- [Conway, *Five $1,000 Problems* (2017 update)](https://oeis.org/A248380/a248380.pdf)
- [Lou and Murin, *On the Strongly Regular Graph of Parameters (99, 14, 1, 2)* (2014)](https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf)
- [Cesarz and Woldar, *Algebraic Combinatorics* 8 (2025)](https://doi.org/10.5802/alco.418)
- [Keramatipour, *Approaching the Conway-99 problem using SAT solvers*](https://arxiv.org/abs/2604.23037)
- [Petro and Phillips, *On clique graphs and clique regular graphs*](https://doi.org/10.1016/j.disc.2025.114862)
- [Reimbayev, *The lower bound for number of hexagons in strongly regular graphs with parameters lambda=1 and mu=2*](https://doi.org/10.62780/ejaam/2024-001)

An older public code repository is tracked only as prior art because no license
was found during the initial audit. Its source must not be copied here.

## Licensing

Original software in this repository is MIT-licensed; see [LICENSE](LICENSE).
Original prose and data are offered under CC BY 4.0; see
[LICENSE-CONTENT.md](LICENSE-CONTENT.md). Third-party sources retain their own
licenses and are linked, not vendored, unless their terms are explicitly
compatible.
