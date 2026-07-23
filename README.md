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
