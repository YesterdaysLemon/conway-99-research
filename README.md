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

- **Literature status:** open as of the audit dated 2026-07-22.
- **Project status:** `EXPLORATORY`.
- **Resolution claim:** none.
- **Symmetry policy:** no nontrivial automorphism, transitivity, Cayley, or
  circulant assumption is imposed on the full search.

A peer-reviewed 2025 paper calls existence an open problem. A targeted
freshness search through 2026-07-22 found no credible construction or
nonexistence proof. That search is evidence about the literature, not a
mathematical proof of openness.

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

An older public code repository is tracked only as prior art because no license
was found during the initial audit. Its source must not be copied here.

## Licensing

Original software in this repository is MIT-licensed; see [LICENSE](LICENSE).
Original prose and data are offered under CC BY 4.0; see
[LICENSE-CONTENT.md](LICENSE-CONTENT.md). Third-party sources retain their own
licenses and are linked, not vendored, unless their terms are explicitly
compatible.
