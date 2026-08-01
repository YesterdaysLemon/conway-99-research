# Wave 208 orchestrator decision

```yaml
role: orchestrator
date_utc: 2026-08-01T02:55:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Decide which Wave 208 symbolic reductions may enter public project state
  after manifest-pinned clean-room verification, without changing any
  endpoint or global UNKNOWN status.
inputs:
  protocol: 3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740
  norm_manifest: a633dff62e4e1127b8a0c7329928e110d1fef1e78f1f322bbc4e250e277167f3
  proof_b_manifest: f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc
  proof_a_manifest: 28d69162a8f52bdc325471946efecad890b1edac33f3576bdba8777e32887202
  verifier_manifest: c9551a7c4d62a57f081b8008f49b9e27fb0372f50a7d114e10136557242fbab4
method: >-
  Compare each discovery claim with the final verifier audit; preserve all
  corrections, coverage gaps, and hostile outside-row witnesses; replay
  exact suites and manifests; and promote no arithmetic or local survivor
  to a graph, codeword, endpoint exclusion, or global result.
command: >-
  .\.venv\Scripts\python.exe -B -m unittest -v
  verification\wave208-global-residual-verifier\test_independent_baseline.py
  verification\wave208-global-residual-verifier\test_independent_m7g_norm.py
  verification\wave208-global-residual-verifier\test_post_source_m7g_audit.py
  verification\wave208-global-residual-verifier\test_independent_proof_b.py
  verification\wave208-global-residual-verifier\test_independent_proof_a.py
outputs:
  - verification/2026-07-31-wave208-integration-audit.md
  - verification/2026-07-31-wave208-orchestrator.md
  - logs/2026-07-31-wave208-public-checkpoint.json
limitations:
  - Four marked polar forms and every residual point-code weight remain possible.
  - All displayed finite graph controls omit outside equations and completion.
  - Rank 11, n3=4158, Conway-99, novelty, and priority remain UNKNOWN.
```

## Decision

Promote with exact scope:

- `VERIFIED_CONDITIONAL`: the M7g norm identity forces `S_D=3 mod 9`;
- `VERIFIED_CONDITIONAL`: 23 of all 27 marked polar forms are excluded and
  exactly three rank-four plus one rank-three form survive;
- `VERIFIED_CONDITIONAL`: each rank-four form has 83 marked subsets and an
  integer `-4` residual of squared norm 56;
- `VERIFIED_CONDITIONAL`: the rank-three form has 66 weight-20 and 792
  weight-14 marked subsets and satisfies the exact integer equation
  `A b=3b`;
- `VERIFIED`: the general integer lift splits into explicit integral `-4`
  and `3` eigenvectors with the archived norm and residue-shell identities;
- `VERIFIED_CONDITIONAL`: balanced weight 14 has six `q^2` shells; its
  `q=0` shell reduces to the one-cross-edge row, while its `q^2=14` shell
  reduces to `alpha=0`, `beta=6`, and `k in {2,3,4}`;
- `VERIFIED_RESTRICTED_CONTROL`: the two marked controls and the 22-vertex
  complementary-Fano control only at their displayed internal scope;
- `VERIFIED_SCOPE_VETO`: those controls do not imply an outside code
  equation or an SRG completion.

Retain without promotion:

```text
rank-three point weights 14 and 20:       UNKNOWN
three rank-four norm-56 branches:         UNKNOWN
balanced q^2 shells 0,14,28,42,56,70:    UNKNOWN
point-code weights 14,17,20,23:           NOT EXCLUDED
d(ker_F3(A))>=24:                         NOT PROVED
full marked M7g completion:               UNKNOWN
rank-11 endpoint:                         UNKNOWN
n3=4158 endpoint:                         UNKNOWN
Conway-99:                                UNKNOWN
rigorous n3 interval:                     708<=n3<=4158
conditional Q bound:                     Q>=7059
Q>=7060:                                  NOT PROVED
```

## Findings retained in public state

1. The initial construction's outside-vertex count was invalid because
   eight triangle columns do not fix an eight-vertex union.  The corrected
   sealed derivation makes no count.
2. The proof-B checker did not derive the four concurrent-secant matchings;
   the verifier's complete 105-matching enumeration supplies that coverage.
3. The proof-A checker sampled the spectral formulas; the verifier supplied
   a general symbolic expansion.
4. Explicit one-row extensions preserve every displayed internal equation
   and upper cap while violating an omitted outside equation.  They are hard
   counterexamples to local-to-global promotion.

## Inflection

Wave 208 turns a 23-form ambiguity into two named spectral problems.  The
rank-three branch is a small signed `3`-eigenfunction carried by eight marked
triangles.  The rank-four branch is an integral `-4` eigenfunction of norm
56 with fixed marked triangle sums.  These are the next legitimate symbolic
objects; another unconstrained local model or aggregate moment table cannot
decide the endpoint.
