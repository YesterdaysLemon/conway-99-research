# Wave 207 source-blind hostile verification protocol

This protocol was frozen before opening or executing any Wave 207 discovery
artifact, including `attempts/wave207-*` and
`agents/2026-07-31-wave207-*.md`.  The only project sources read before this
freeze were `AGENTS.md`, `CONJECTURE.md`, the relevant sealed Wave
174/176/191/206 verifier records, and the corresponding ledger entries.

```yaml
role: verifier
date_utc: 2026-08-01T01:22:24Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: UNKNOWN
scope: >-
  Hostile independent audit of five frozen Wave 207 claims about the
  conditional prism-free n3=4158 rank-11 endpoint: incidence-kernel
  consequences, weight-eight projective geometry, canonical finite
  enumerations, abstract mixed-center Gram algebra, and the unchanged
  global status wall.
inputs:
  AGENTS.md: 4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3
  CONJECTURE.md: 7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58
  STATUS.yaml: 2b29a8c6a5fb6471ad95ad3ac612e364cc5ffd83cba1744159b50ec8f5717291
  CLAIMS.yaml: 03028cb60fa298b5b4cd1f8109713fdbea4bef021bb8818d7fd029bfcd3757ec
  OBLIGATIONS.yaml: d2364acff4b4f8b4ac51edbe324e29b5362e6a399bc8a9596ee7b83572198767
  verification/wave174-no-weight3-dual/package-manifest.sha256: ac34c8a3b045bec70e3a2080cb4365c0ea43cc732b313ecb3cec355a28f23450
  verification/wave174-no-weight3-dual/verification-report.md: 59bc0e470a7d007aa2ddaec262a2f3046c8df7da56192bdab90327962feb9b0a
  verification/wave176-star-projector-circuits/package-manifest.sha256: 2c2b2964d47e235bc1dc3faaf6f6cb870aed9a7595f61d41e8babbd863622c39
  verification/wave176-star-projector-circuits/audit.md: f58577409f39e98b06bfbe206221d3d278f0c473bcf5057afc381094d5e65d05
  verification/wave191-exact-three-residual-verifier/package-manifest.sha256: a14f43310fb5ead05c4bd50b376f3d9d90ec77a92bc00f8c3b7326013f975ab2
  verification/wave191-exact-three-residual-verifier/audit.md: a20df1532452adf0e738a51c17ab0f8661b08ae8ebbcd06d0eaf62a4b0a0868e
  verification/wave206-three-center-global-extension-verifier/package-manifest.sha256: 3368b0b1995e40f294530cefb596cd2722a859d22aaa672190c55dbd23107ecf
  verification/wave206-three-center-global-extension-verifier/audit.md: b1524bf3c923d5e52cb28c6899774130b3c1a9467cfb6d54a2de014d8b555a3e
  verification/2026-07-29-wave206-integration-audit.md: 2fdb00f86cadecb5430011fbd938a3fda44e9314f21db005dacf10e9eb4f6341
  logs/2026-07-29-wave206-public-checkpoint.json: 50408288e47da5a89f67c800e0450177c1f04b0d90dae1cb205153d80917fb03
method: >-
  Freeze exact claims and failure criteria; independently implement F3
  row reduction, projective normalization, kernel enumeration, graph
  invariants/isomorphism, and symmetric-power transition maps without
  importing discovery modules; then inspect source derivations, manifests,
  primary literature, and replay the sealed discovery suites with the
  repository virtual environment.  Attack missing rank, injectivity,
  characteristic-three, projective-distinctness, and scope hypotheses.
command: >-
  To be recorded exactly in the final verifier run report after the
  independent implementation and source replay are complete.
outputs:
  - verification/wave207-incidence-tensor-rigidity/protocol-freeze.md
  - verification/wave207-incidence-tensor-rigidity/SOURCE_BLIND_PROTOCOL.sha256
  - verifier-owned code, results, tests, audit, manifests, and command logs
    under verification/wave207-incidence-tensor-rigidity/
  - agents/2026-07-31-wave207-verifier.md
limitations:
  - Every target theorem is conditional on a putative prism-free n3=4158
    rank-11 endpoint unless it is explicitly an abstract algebra statement.
  - Finite enumeration certifies only the precisely enumerated canonical
    model and normalization; classification needs a proved reduction to it.
  - A theorem citation is usable only if its hypotheses are mapped to the
    endpoint objects, not merely because the conclusion resembles them.
  - No endpoint exclusion, graph construction, counterexample, novelty,
    priority, strict n3 improvement, Q>=7060, or Conway-99 resolution may be
    inferred from the frozen claims.
```

## Frozen notation and premises

All finite-field algebra is over `F_3`.  Use the prior verified endpoint
notation only after checking dimensions and orientations from sealed inputs:

- `B` is the point-triangle incidence matrix and `a` is a triangle-coordinate
  word;
- `D` is the centered-column Gram matrix, `Z` is a full-row-rank synthesis
  matrix for the centered columns, and the exact relations connecting
  `B,D,Z` must be checked rather than inferred from names;
- `A_Delta = im(B^T) intersect ker(a |-> D diag(a) D)`;
- a conditional weight-eight word has eight projectively distinct columns,
  support rank four, and no dependent triple only if the Wave 174 premise
  applies to precisely these columns;
- the Wave 206 tensor relation is a true operator identity.  Gram-kernel
  vectors may not be promoted to true relations without an injectivity or
  rank argument.

Any mismatch of dimensions, transpose conventions, field, or conditional
premises is a veto, not something the verifier may silently repair.

## Frozen claims and hostile tests

### C1. Incidence-kernel strengthening

Claim to test: every `a in A_Delta` satisfies both `D a=0` and `Z a=0`.
This is intended to correct the Wave 206 caveat that the tensor condition by
itself did not supply a centered-column linear relation.

Required checks:

1. Derive `D a=0` only from verified incidence identities and
   `a in im(B^T)`, checking matrix orientations and the exact identity
   (`BD=0` or its correctly oriented equivalent).
2. Derive `Z a=0` only after proving `ker(D)=ker(Z)` in the actual endpoint
   model, including full row rank of `Z`, nondegeneracy of the ambient form,
   and `D=Z^*Z` (with the correct adjoint/form matrix).
3. Test the failure modes when the synthesis matrix lacks full row rank or
   the ambient form restricts degenerately: `Da=0` need not imply `Za=0`.
4. Separate the incidence consequence from the nonlinear tensor-kernel
   condition; report if `A_Delta` is stronger than needed for either step.

### C2. Weight-eight composition and projective classification

Claim to test: conditional on `wt(a)=8`, the nonzero coefficients consist of
exactly four `1`s and four `2`s, and the eight projective support points have
the unique Kaipa-Pradhan `M7g` geometry: four disjoint paired secants concur
at a point outside the support, and no three of those four secant lines are
coplanar.

Required checks:

1. Reconfirm rank four and projective distinctness/no dependent triple for
   the exact support, with no hidden passage from vector dependence to
   projective collinearity.
2. Combine the verified tensor equation with `Za=0`; independently derive
   all hypotheses of the cited finite-geometry classification.
3. Inspect the primary Kaipa-Pradhan source (arXiv:2405.12011), locate the
   exact theorem/table defining `M7g`, and map every hypothesis, field,
   equivalence relation, and conclusion.  A name/table match alone fails.
4. Independently enumerate or canonically normalize the finite rank-four
   configurations where practical, quotienting only by proved projective
   equivalences.  Verify uniqueness by an explicit invariant/canonical
   representative, not by a solver exit code.
5. For the proposed four pairs, compute all four secants, their common
   intersection, prove the intersection is outside the eight points, and
   test every triple of secants for coplanarity.
6. Enumerate coefficient compositions allowed by all equations.  Veto the
   `4+4` conclusion if it depends on a normalization that can globally swap
   `1` and `2` without preserving the claimed count (the count itself is
   swap-invariant) or on an unproved uniqueness premise.

### C3. Canonical finite enumerations

Claims to test for the canonical support:

```text
linear-relation weight enumerator = 1 + 24 y^4 + 16 y^5 + 32 y^6 + 8 y^8;
restricted polar zero-graphs      = K8, 2K4, 4K2, 2C4.
```

Required checks:

1. Put the eight columns into a verifier-owned explicit `4 x 8` canonical
   matrix and record its hash and rank.
2. Enumerate all `3^dim ker` relation words independently; require exactly
   81 words, the stated weight counts summing to 81, and direct equality to
   the displayed polynomial.
3. Define the restricted polar form and zero-graph adjacency before
   computing.  Check symmetry, diagonal convention, simple-graph
   conversion, degree sequence, connected components, edge count, and exact
   graph isomorphism for every listed type.
4. Record multiplicities/orbits of graph types if the source claims them;
   do not report a set of names as a complete classification without
   exhausting the relevant parameter or relation orbit.
5. Attack coordinate rescaling, point reordering, global coefficient
   scaling, and alternate pairings.  The enumerator should be invariant;
   any graph statement must say precisely what is invariant and under which
   equivalence.

### C4. Abstract Gram exact sequence and transition rank

Claim to test: Proof B's abstract Gram construction gives the stated exact
sequence, and a transition matrix `C` induces rank
`binom(rank(C)+1,2)` on the relevant symmetric-square map.  In addition,
true `A_Delta` projector relations are annihilated by every feature obtained
linearly from sandwiches and mixed traces.

Required checks:

1. Rewrite the proposed sequence with named domains, codomains, maps, and
   bases.  Verify well-definedness, each consecutive composition is zero,
   equality of image and kernel at every term, and every asserted
   injection/surjection.  Dimension counts alone are insufficient.
2. Independently form the map on symmetric matrices for transition ranks
   `r=0,...` in small rectangular and square examples over `F_3`; compare
   exact row-reduction rank with `r(r+1)/2`.
3. Prove the general rank formula by reducing `C` with invertible row and
   column operations and checking that characteristic two is the only
   polarization hazard; explicitly confirm it over `F_3`.
4. Test singular, rectangular, zero-rank, and full-rank edge cases, and
   distinguish the symmetric-square map from a map on all matrices or from
   a Gram matrix whose rank can fall because a restricted pairing is
   degenerate.
5. For any true relation `sum_x c_x P_x=0`, symbolically factor each claimed
   sandwich/mixed-trace feature through that linear sum.  Record the exact
   quantifier on centers and fixed external matrices.  A nonlinear or
   relation-dependent choice of feature is outside the annihilation claim.
6. Confirm this is an obstruction-method boundary: these linear features
   vanish on all true relations and therefore cannot by themselves
   distinguish or exclude an `A_Delta` relation.

### C5. Global status wall

Claim to test: C1--C4 yield neither endpoint exclusion nor a global proof or
counterexample.  Preserve exactly:

```text
Conway-99:                    UNKNOWN
rank-11 endpoint:             UNKNOWN
n3=4158 endpoint:             UNKNOWN
graph construction:           NONE
counterexample/nonexistence:   NONE
Q>=7060:                      NOT PROVED
strict n3 improvement:         NONE
```

Any finite canonical enumeration, literature classification, or abstract
feature-kernel theorem must remain conditional/local unless a complete map
back to every endpoint constraint is checked.

## Post-freeze source audit and replay

Only after hashing this protocol:

1. inventory and hash every file in
   `attempts/wave207-incidence-tensor-code-proof-a/`,
   `attempts/wave207-mixed-four-center-proof-b/`, and the Wave 207 literature
   report;
2. inspect derivations, run reports, manifests, exact results, and tests;
3. verify manifest entries before trusting replay results;
4. replay all submitted commands with `\.venv\Scripts\python.exe` and save
   stdout/stderr plus exit codes under the verifier directory;
5. implement and run verifier-owned computations without importing discovery
   modules where practical;
6. compare source and independent results field by field;
7. report discrepancies as findings.  Do not edit discovery artifacts or
   shared ledgers, and do not silently repair a source claim.

## Verdict rules

- `VERIFIED`: all hypotheses and mappings are established, independent exact
  computation agrees, edge cases pass, and scope is explicit.
- `REFUTED`: an exact counterexample or failed required identity is recorded.
- `UNKNOWN`: evidence is incomplete, a cited theorem is inapplicable or not
  mapped, an enumeration is restricted without a completeness proof, or an
  asserted exact sequence is not fully established.

Each of C1--C5 receives its own verdict.  A source test pass is never itself
a mathematical verdict.

## Required final run-report schema

The final verifier report must include this schema with concrete paths,
hashes, commands, and limitations:

```yaml
role: verifier
date_utc: YYYY-MM-DDTHH:MM:SSZ
git_commit: full_hash
claim_label: CITED | DERIVED | VERIFIED | CANDIDATE | REFUTED | UNKNOWN
scope: exact statement or restricted subproblem
inputs: paths and sha256 hashes
method: concise description
command: exact reproducible command, if computational
outputs: paths and sha256 hashes
limitations: explicit caveats
```
