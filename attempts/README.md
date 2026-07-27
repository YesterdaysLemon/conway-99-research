# Attempt ledger

Record proof and search attempts here, including failures. Each entry should
state its scope, assumptions, result, evidence label, and the smallest known
obstruction. Do not overwrite failed attempts when a method evolves.

## Wave 15: global lift of the `n3=48` residual

- Scope: the independently audited Wave 14 active-point residual, conditional
  on a putative `srg(99,14,1,2)` with `n3=48`.
- Result: `VERIFIED` conditional equality exclusion, so `n3>=51` and
  `induced_C6_count>=209337`.
- Smallest obstruction: the nonempty active original vertices form an induced
  set of order at most 24 and minimum degree at least six, while the target
  spectrum requires every such set to have order at least 27.
- Independent evidence: `wave15-global-lift/` gives spectral and outside-degree
  moment certificates; `wave15-algebraic/` independently reconstructs the
  spectral route and retained triangle moments.
- Retained failures: active common-neighbor caps and the first two
  triangle-intersection moments do not obstruct the residual; an ambiguous
  algebraic JSON key and a CRLF/public-LF certificate mismatch were repaired
  transparently and re-audited.
- Boundary: this is a necessary count bound, not a proof or counterexample for
  Conway-99; target and novelty remain `UNKNOWN`.

## Wave 16: conditional `n3=51`

- Structural scope: all sixteen `sum q=34` profiles under the audited
  active-triangle framework.
- Structural result: `VERIFIED` conditional equality exclusion, hence
  `n3>=54` and `induced_C6_count>=209340`.
- Smallest obstruction: the four surviving profiles give at most 25 active
  original vertices, endpoint-local crossing arithmetic forces minimum
  induced degree six, and the target spectrum requires at least 27 vertices.
- Computational scope: a separate seven-branch active-local relaxation with
  exact CNF hashes and one raw positive candidate.
- Computational result: `PASS_FOR_CONDITIONAL_ACTIVE_LOCAL_ARCHIVE_ONLY`;
  one proofless UNSAT, five timeouts, and one historical budget stop are
  explicitly non-evidentiary.
- Retained failure: discovery baseline `09c20e6` pinned a transient Wave 15
  audit hash; repair `7530cae` pins the final public input and an independent
  re-audit preserves all historical hashes.
- Boundary: neither lane resolves Conway-99 or establishes novelty.

## Wave 33: rooted extension and rootless motif boundary

- `wave33-rooted-extension/` derives the forced `14+70+15` quotient,
  simple `2-(15,3,2)` O-Q design, exact induced-70 spectrum, and the full
  six-block binary graph-extension criterion. Its 15-test discovery suite
  supplies no satisfying pair and no infeasibility certificate.
- `wave33-rootless-motif/` gives two formal local third-triangle tables
  invisible to the checked fused algebra while changing the common-R3 count,
  plus the actual eight-vertex R2 board with four transversal candidates.
  Its 14-test suite does not prove global realization, motif forcing, or
  motif avoidance. The independent audit narrows the headline to the formal
  `q=2` R2 and bilinear `Q[Gamma]` / `N^T p(A)N` scope.
- `wave33-rooted-construction/` retains an exact hostile O-Q certificate,
  a deterministic search replay, and a bounded MILP record for all `70!`
  assignments of one fixed simple design. The certificate fails ten
  central-notation `F B=2J` entries with squared defect ten and supplies no
  O-O layer. The
  status-1 timeout, heuristic nonhits, and every missing layer are explicitly
  non-evidentiary. Because its input freeze predates the mutable central
  Wave 33 exposition, replay the unchanged 14-test package through
  `verification/wave33-rooted-construction-chronology/`, not directly
  against the integrated root. That clone-independent chronology replays 36
  of 37 verifier cases, separately passes the portable half of the sole
  omitted composite test, and labels the solver-environment half, which
  depends on ignored local files, `NOT_REPLAYED_NONBLOCKING`; it opens zero
  such files and observes zero environment hashes.
- The full correction and nonpromotion chronology is in
  `verification/2026-07-24-wave33-orchestrator-corrections.md`.

## Wave 34: exact rooted formula and rootless actual-incidence continuation

- `wave34-rooted-structural/` records the discovery-side support/SNF,
  projector, and Pb-only 2-factor census candidate. Its five-file manifest
  is frozen; independent verification and a structurally different
  pair-census crosscheck live under `verification/`.
- `wave34-rooted-encoding/` contains the complete labeled CNF publication
  package. The tracked deterministic gzip expands to an 89,546,779-byte raw
  formula with 1,233,001 variables and 4,323,943 clauses. The raw CNF is
  ignored locally; no solver result or proof is claimed.
- `wave34-rootless-global/` contains the candidate local-fibre model,
  restricted factor scan, and partial 45-vertex control. It is not a target
  graph and supplies no global motif-forcing or avoidance result.
- `wave34-current-literature/` freezes the bounded search and six source
  records. No exact unrestricted Wave 34 prior result was found in the
  searched windows, which is not a novelty or openness claim.
- Corrections, failed routes, and the unchanged target wall are collected in
  `verification/2026-07-24-wave34-orchestrator-corrections.md`.

## Wave 35: prism-free upper endpoint

- `wave35-n3-upper-spectral/` records exact endpoint signed-projector, Smith,
  Schur, compression, incidence-scalar, and local-PSD routes. The submitted
  14-test suite and an independent 10-test suite pass, but every tested
  obstruction survives and `n3<=4158` is unchanged.
- `wave35-n3-4158-combinatorial/` records the exact one-triangle
  `3+36+60` incidence reduction, finite restricted block census, one
  pairwise positive control, and failed parity/heuristic/proofless-solver
  routes. It does not construct or exclude a simultaneous block system.
- `wave35-n3-upper-triple-overlap/` records the 84 rooted prism-forbidding
  units, exact reduction from twelve normalized `N3` branches to five,
  deterministic OPB files for four local seed partitions, and every bounded
  solver stop. All timeouts and conflict-budget stops are `UNKNOWN`.

## Wave 36: modular, ternary-polar, and mixed-block restrictions

- `wave36-modular-reflection/` derives reciprocal Smith factors, modular-rank
  constraints, and the characteristic-seven pure-cube ceiling. Its submitted
  11-test suite does not construct a surviving endpoint matrix.
- `wave36-ternary-polar-bound/` converts the endpoint rows into a regular
  induced set of ternary norm-two projective points and checks the exact
  finite orthogonal parameter table. Its submitted 10-test suite leaves the
  square rank-twelve class and all larger allowed ranks alive.
- `wave36-block-compatibility/` derives the mixed block equations, restricted
  individual-column and fixed-pair censuses, component balance, and spectral
  transfer to `H`. Its 10-test suite supplies no simultaneous 60-column
  design.
- `wave36-literature-audit/` freezes the bounded source/query metadata and
  exact Evans substitutions. No search nonhit is treated as novelty evidence.

## Wave 37: endpoint clause catalogs, polar strengthening, and OPB handoff

- `wave36-rooted-branches/` is the delayed publication of the exact
  fixed-triangle `P=0` clause construction. Each surviving parent branch has
  282,774 deduplicated active clauses. The retained branch-4 MiniCard result
  is `BUDGET_UNKNOWN`; the nonterminal 33-case sweep is ignored locally and
  excluded from every claim.
- `wave37-polar-strengthen/` records the projective self-orthogonal ternary
  code consequences, the corrected balanced-degenerate-triple count, and an
  exact characteristic-seven rank-eleven association-scheme test. The
  tempting collinearity shortcut is retained as refuted, and every tested
  rank boundary survives.
- `wave37-proof-producing-endpoint/` publishes a deterministic compressed OPB
  formula for refined branch 15, its metadata, stream audit, parser record,
  test suite, and correction ledger. Parser acceptance is syntax-only. Even
  a future checked `UNSAT` proof for this artifact would close only one of 33
  refined endpoint cases.

No Wave 37 solver telemetry, formula export, finite-field survivor, or bounded
nonhit improves the general interval `708<=n3<=4158`.

## Wave 38: public live-run boundary and exact continuation

- `wave38-solver-harvest/` records a sanitized, read-only snapshot of the two
  inherited live scouts and freezes the exact 33-case, 231-artifact
  proof-producing queue. Both terminal JSON files were absent; current proof
  coverage is `0/33`.
- `wave38-complete-endpoint/` supplies the exact all-prism static schema,
  decoded-candidate oracle, candidate-bound cut catalogs, source-bound cut
  pools, and guarded OPB exporters. The exact residual-only subfamily has
  24,388,892,640 clauses, so the practical route is finite
  solve--cut--check. No target formula was generated or solved.
- `wave38-coclique-rank/` combines a public 13-coclique construction with the
  incidence-projector identity to prove `rank_F7(M)>=13`. A separate verifier
  promotes this scoped implication and leaves 528 arithmetic endpoint rank
  pairs.
- `wave38-higher-order/` derives the signed support-four-cycle imbalance
  200,277, a ternary fixed-triangle rank bridge, and a rank-ten local positive
  control. It exposes simultaneous `B/H` or cross-base compatibility as the
  missing lemma; it does not prove `P>=1`.

All solver activity, partial pools, local controls, and arithmetic survivors
remain nonterminal. The endpoint, upper-bound improvement, Conway-99, and
novelty are `UNKNOWN`.

## Wave 39: edge-local rank, proof shard, and compatibility restrictions

- `wave39-edge-local-rank/` derives the eleven edge-local cycle normal forms
  and the characteristic-seven rank formula
  `25-2*(number of even parts)`. Independent verification promotes the
  universal necessity `rank_F7(M)>=19`.
- `wave39-proof-solver/` exports the `branch15 AND x187=1` OPB shard and
  retains raw, elaborated, and kernel pseudo-Boolean proofs. Independent
  VeriPB replay accepts the raw and kernel proofs. The other polarity shard
  is open, so branch 15 and endpoint proof coverage remain unresolved.
- `wave39-cross-base-rank/` records conditional projection collisions and
  explicit support-four/six dependencies, together with controls refuting a
  universal local rank-twelve shortcut.
- `wave39-simultaneous-bh/` records conditional centered-code and compatible
  `H` overlap restrictions. Its Delsarte transforms are nonnegative and it
  supplies no completion or exclusion.

The Wave 39 packages do not construct a graph, force a prism, close a complete
endpoint case, improve `n3<=4158`, or establish novelty.

## Wave 40: third-fibre rank completion and global edge coupling

- `wave40-rank19-equality/` records the discovery route from the Wave 39
  rank-19 equality type through third-fibre quotient syndromes. It proves the
  conditional stepping stone `n3=4158 => rank_F7(M)>=22`, retains the exact
  `0,4,8,12` matching boundary, and is independently verified.
- `wave40-exact-coupling-model/` extends the third-fibre argument to all
  eleven edge partitions. Its complete subspace certificate and matching
  census give the candidate universal theorem `rank_F7(M)>=25`; a separate
  clean-room implementation promotes that theorem to `VERIFIED`. The
  full-39-block scout is explicitly bounded and non-evidentiary.
- `wave40-edge-type-coupling/` glues the four prism-free edge types into a
  closed incidence complex, exhausts the 4,050 normalized all-`222`
  one-triangle quotients, proves the exact cubic-core Laplacian rank identity,
  and exhausts all `2^18` lifts of one boundary quotient. The resulting
  rank-33 controls survive and do not exclude the endpoint.
- `wave40-rank25-literature/` freezes a bounded primary-source search for the
  exact rank-25 theorem and equivalent formulations. Search nonhits do not
  establish novelty or priority.

Wave 40 raises the verified universal characteristic-seven rank floor from
19 to 25 and reduces conditional endpoint arithmetic from 429 to 330 pairs.
It does not construct a graph, force a prism, close an endpoint case, or
improve the general upper bound `n3<=4158`.

## Wave 43: conditional endpoint rank 28 and alternative-space controls

- `wave43-rank28-motif/` and `wave43-type33-rank2/` exhaust the two local
  rank-27 mechanisms for all four endpoint edge types. A clean-room verifier
  promotes `n3=4158 => rank_F7(M)>=28`.
- `wave43-all-rank33-lifts/` extends the exact component and six-set reduction
  to all 264 canonical rank-33 lifts. Every lift survives.
- `wave43-branch15-two-triangle/` adds 40,800 exact width-four prism cuts to
  branch 15; 34,340 remain active and no probe closes the branch.
- `wave43-joint-completion/` records exact compact CNF and sparse MILP
  formulations for the canonical 45,032-candidate three-way matching.
  Both retained solver runs are `UNKNOWN`.
- `wave43-seven-deck-endpoint/` gives an independently verified exact
  99-support solution of every unrooted count equation through order seven.

The conditional rank theorem removes 16 endpoint arithmetic pairs but does
not exclude `n3=4158`. Count feasibility is a positive control for the
relaxation only, not graph evidence.

## Wave 44: aggregate rooted order-seven control

- `wave44-rooted-flags/` adds every vertex-root, ordered-edge-root, and
  ordered-nonedge-root category equation to the order-seven deck.
- The 170-row system is strictly stronger than the unrooted 81-row system
  but has an exact nonnegative 91-support integer witness at `h11=16632`.
- A floating-point HiGHS `infeasible` report is retained as a refuted
  numerical false negative. Only the exact witness and direct substitution
  are evidentiary.

This closes the aggregate rooted-count lane as a null result. A useful next
step must impose overlapping-subset compatibility, a PSD flag moment matrix,
order-eight variables, or the full simultaneous `B/H` equations.

## Wave 45: positive-semidefinite rooted-flag checkpoint

- `wave45-flag-moment/checkpoint-v1-*` is the immutable discovery checkpoint
  accepted by the clean-room verifier. It contains the exact rooted-moment
  coefficient stream, the two stored-witness attacks, and 17 cuts against 15
  successive exact count witnesses.
- `wave45-flag-moment/README-v1.md`, `replay-v1.py`, and
  `package-manifest-v1.sha256` provide the versioned discovery replay and
  nine-entry package boundary.
- Mutable cutting-plane files and later solver runs in the same directory are
  work in progress and are not part of checkpoint-v1 evidence.

The checkpoint refutes the stored Wave 43 and Wave 44 count vectors, not the
endpoint. Its next solver call timed out, so the full PSD-constrained region
remains `UNKNOWN`.

## Waves 46--49: code, polynomial, and higher rooted moments

- `wave46-f7-code/` records the ordinary characteristic-seven row-code
  consequences and generic positive controls in every rank 28 through 44.
  Independent verification confirms a null obstruction: the distinguished
  projector-row geometry is not captured by the ordinary code constraints.
- `wave47-three-root-moment/` constructs eight exact three-root/two-free Gram
  families. A clean-room verifier reproduces 2,664 exact negative directions
  and 2,657 distinct cuts against the 17 stored witnesses.
- `wave47-branch15-polynomial/` computes the complete stated degree-two
  squarefree Macaulay closure in seven branch-15 windows. Independent replay
  verifies 13 local XOR relations, zero contradictions, zero new unary
  assignments, and the degree-four representation barrier for all 34,340
  active Wave 43 cuts.
- `wave48-conic-moment/` combines the 170 count equations with eleven moment
  families. A clean-room verifier confirms exact affine rank 93, nullity 116,
  and all universal kernels; floating Clarabel/SCS points remain
  non-evidentiary and no exact feasible point or infeasibility witness is
  retained.
- `wave49-five-root-moment/` constructs all 21 canonical five-root/one-free
  Gram families without a target-graph automorphism. Independent comparison
  verifies all 2,520 root relabellings, 42 known-graph controls, and 357 exact
  stored-witness refutations.

These lanes strengthen the finite relaxations and preserve useful failure
information. None solves the complete PSD-constrained count region, closes an
endpoint SAT branch, constructs a graph, or proves `n3<4158`.

## Wave 51: alternative algebra and aggregate controls

- `wave51-global-triple-tensor/` gives an explicit nonnegative symmetric
  triple-count tensor for the five triangle-pair relations. Independent replay
  verifies the aggregate control and refutes its interpretation as an
  association scheme.
- `wave51-seidel-smith/` derives a candidate conditional Smith normal form
  and a symmetric-square rank bound. Its independent verifier corrects the
  discovery spectrum and verifies the unaffected scoped theorem.

Both discovery packages are necessary-condition or relaxation work. Neither
constructs a graph, supplies pair-specific quadruple compatibility, excludes
the endpoint, or improves `n3<=4158`.

## Wave 52: one-root coherent closure

- `wave52-coherent-closure/` derives the forced 19-triangle `3K6` root and
  `B2/C4/D0` cross-sector caps, then applies exact 2-WL to both the partial
  relation structure and a completion-free 163-node incidence lift.
- Explicit integral cap completions survive. Sixty-four canonical
  two-factor-profile diagnostics produce 39 different closure fingerprints,
  proving that completed colors depend on arbitrary local choices.

This is a discovery null result. Independent verification accepts the finite
arithmetic and color refinement only; no graph or improved bound follows.

## Waves 53--55: proof cover, two-root lift, cut correction, and bounded search

- `wave53-proof-cover/` freezes the exact normalized 33-case endpoint cover
  and exports `branch15 AND x187=0`. Its bounded proof-tool transcripts end
  with `UNKNOWN` or `VERIFIED NO CONCLUSION`; none is a terminal proof.
- `wave53-multi-root-wl/` merges two rooted cap systems for relations
  `K,B,C,D`. It derives one forced-true shared candidate in relation `B` and
  exact 2-WL/folklore-3-WL closures. Positive local controls survive in every
  relation.
- `wave53-exact-cut-loop/` records four exact rational witnesses and three
  retained Wave 49 cuts. Its headline that all 128 tested matrices are
  indefinite is refuted by independent replay: eight Wave 45 matrices are
  positive semidefinite, due to a doubled-off-diagonal source defect.
- `wave54-centered-enumerator/` constructs an exact seven-weight formal
  ordinary enumerator satisfying the frozen integral MacWilliams system.
  It is not a realized ternary code.
- `wave55-branch15-remainder-search/` retains the exact solver transcript and
  metadata from a 120-second run on the open branch-15 shard. Exact returns
  `UNKNOWN`; the ignored 488 MB nonterminal proof prefix is not evidence.

The corrected fixed 177-cut rational relaxation and formal enumerator remain
feasible, while endpoint proof coverage remains `0/33`. No graph, endpoint
exclusion, strict upper bound below 4158, or novelty claim follows.

## Waves 56--59: alternative closure, incidence, and spectral spaces

- `wave56-percolation-closure/` derives the nonedge closure dichotomy,
  `n3+3P=4158`, `R=18H`, `6H<=P`, and the exact 23-mask/35-profile endpoint
  multicover. Independent verification accepts the finite conditional scope.
- `wave57-star-complement/` derives correct projector and star-set formulas
  but overstates the live parameter space. Its verifier retains a
  `REFUTED_IN_PART` verdict: prior Wave 36 leaves three live rows and cubic
  wedge counting sharpens the four-cycle ceiling from 89 to 27.
- `wave58-cross-incidence-rank/` combines the corrected rank transfer with
  exact normalized `m=4` and `m=6` component censuses. Independent replay
  verifies the three-row synthesis and all exact-set-versus-bound wording.
- `wave59-incidence-spectral-excess/` recasts the endpoint as a
  `(7,3)`-biregular point--triangle incidence graph and an 18-regular
  triangle graph. It derives exact spectra, distance layers, predistance
  defects, pair-neighborhood Gram rank, and short Ihara cycle counts.
  Independent verification accepts every scoped finite claim.

None of these packages constructs or excludes the simultaneous `B,A_Y`
system. Non-distance-regularity is not nonexistence. The endpoint, strict
upper-bound improvement, Conway-99, and novelty remain `UNKNOWN`.

## Waves 60--63: integer information beyond scalar incidence geometry

- `wave60-c3-incidence-design/` classifies the 18 fibre-preserving
  twelve-vertex component types, all 1,140 triples, 275 safe coordinate
  orbits, and their allowed six-set columns. Its bounded searches are
  `UNKNOWN`.
- `wave61-c3-finite-field/` tests the complete triple set in several finite
  fields and pair-coordinate parity spaces. No triple is eliminated. The
  cubic section is limited to its displayed identities and scalar totals.
- `wave62-terwilliger-sdp/` diagonalizes the one-root signed-edge invariant
  projector SDP and a degree-24 Schur family exactly. All endpoint parameters
  survive.
- `wave63-c3-integer-cone/` stores exact rational pair-cone witnesses for a
  fixed 74-lane stress subset. Every coefficient is at most one, but none of
  the witnesses is a zero-one design.

Independent verification accepts each finite scope, with the Wave 61 wording
correction and Wave 62 tautology-count clarification. Integer and higher-order
compatibility, a compatible `A_Y`, endpoint exclusion, and Conway-99 remain
`UNKNOWN`.

## Waves 64--65: rooted transition design and hypergraph algebra

- `wave64-rooted-transition-design/` identifies the 84 residual labels with
  the edges of `K14-7K2`, enumerates 35,560 matching blocks and 840 allowed
  transitions, stores a 140-block relaxation witness, and gives an exact
  rational point of the stronger linear master. Its complete binary
  codegree closure is specified but unsolved.
- `wave65-rooted-hypergraph-algebra/` studies `B=T+D` through the incidence
  factorization `D+5I=ZZ^T`, the 140-vertex block graph, trace and four-cycle
  identities, scalar spectral coupling, averaged PSD lanes, and an exact
  local positive control that fails the target moments.

Independent verification accepts both finite scopes. Neither package supplies
an integral strong witness, endpoint exclusion, graph, or strict upper bound
below 4158.

## Wave 66: spherical-code and difference-lattice shift

- `wave66-spherical-code-shift/` lifts the negative-eigenspace embedding to
  99 equiangular lines of common angle `1/7` in `R^45`, centers it to an even
  rank-44 lattice `M`, and derives exact dual-denominator, determinant,
  discriminant-group, dual-minimum, and Milgram restrictions.
- The independent verifier records three discovery corrections: the imported
  universal lower rank was 27 rather than the endpoint-only 28; one listed
  weight-eight fact is unused; and only eight, not all 17, imported rank rows
  survive.
- With those corrections, the universal conclusion is
  `rank_F7(2A-J+I) in {28,30,32,34,36,38,40,42}`.

No lattice realization, graph, norm-14 exclusion, endpoint contradiction, or
literature-priority result is supplied. Conway-99 remains `UNKNOWN`.
