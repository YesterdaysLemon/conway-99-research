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
