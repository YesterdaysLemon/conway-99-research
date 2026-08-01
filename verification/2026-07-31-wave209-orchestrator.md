# Wave 209 orchestrator decision

```yaml
role: orchestrator
date_utc: 2026-08-01T03:48:00Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Decide which Wave 209 rank-three and rank-four symbolic reductions may
  enter public project state after independent verification.
inputs:
  - path: attempts/wave209-four-survivor-globalization/protocol.md
    sha256: 3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196
  - path: attempts/wave209-four-survivor-globalization/post-freeze-inputs.sha256
    sha256: 5a1117778a044ec11a211b34861529e3fbce99e393245338befdd3b33a6a7fbb
  - path: attempts/wave209-four-survivor-globalization/upstream-delta.md
    sha256: 0d6f4d8f3beaf90151eff21c968526c1149892e019eef6d24492504f0cbf5f10
  - path: attempts/wave209-rank3-trade-proof-a/package-manifest.sha256
    sha256: 521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
  - path: verification/wave209-four-survivor-verifier/package-manifest.sha256
    sha256: 7e20ac726cc4823360e49d3fcf08e5c8ff6c7f219c5d1cbbba781d015fe59c91
  - path: attempts/wave209-rank4-norm56-proof-b/package-manifest.sha256
    sha256: 2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b
  - path: verification/wave209-rank4-point-signature-verifier/package-manifest.sha256
    sha256: 62c32cfa278a677053353d5a3c21c01600cadc867d597f5135ab32a6fdb1c07a
  - path: verification/2026-07-31-wave209-integration-audit.md
    sha256: eda1a6569a545ce6d4b550f56e01ee4f6396da1edfea3e5017c4e7ab357c0d99
method: >-
  Promote only complete labelled finite reductions and exact certificates;
  retain the verifier-derived 352-to-346 delta as DERIVED; preserve every
  anonymous-census, outside-equation, adjacency, endpoint, and target wall.
outputs:
  - path: logs/2026-07-31-wave209-public-checkpoint.json
    sha256: a9f231f16f7ca5fbe20327577ba5da43e5fd1c4c49f3396ee7c11c5e74925cbb
limitations:
  - No surviving census is an adjacency graph or complete eigenvector.
  - No one independently promotes the six-row verifier discovery here.
  - Every global endpoint remains UNKNOWN.
  - AGENTS.md names Orchestrator as a project role but omits it from the
    fenced run-report role enum; this report retains the semantic role and
    records that pre-existing schema gap instead of changing sealed inputs.
```

## Decision

Promote with exact scope:

- `VERIFIED_CONDITIONAL`: matched product-zero selected-line crosses vanish in
  the rank-three branch;
- `VERIFIED_CONDITIONAL`: support 14 forces `x=1`, the unique rooted support
  type, `(17,61,7)`, 4,480 deficit bijections, and 204 marked graphs;
- `VERIFIED_CONDITIONAL_AGGREGATE`: support 20 excludes `x=0,10`, restricts
  the labelled `x=2` cases to six, and has exactly 352 aggregate rows;
- `DERIVED_CONDITIONAL`: adding the selected-line degree-three cap removes
  six of those rows and leaves 346;
- `VERIFIED_CONDITIONAL`: rank-four parity forbids an even `q`, while the
  marked zero-projector bound is saturated at line norm 168;
- `VERIFIED_CONDITIONAL`: exact Farkas certificates exclude 198 of the 249
  labelled rank-four branches and leave 51 anonymous census controls, 17 per
  form;
- `VERIFIED_SCOPE_VETO`: none of the marked, point-signature, line-signature,
  or aggregate controls implies outside adjacency or a graph completion.

Retain without promotion:

```text
all three rank-four forms:           SURVIVE
51 rank-four labelled branches:      CENSUS-FEASIBLE ONLY
204 rank-three weight-14 marked H:   NOT COMPLETIONS
4480 rank-three deficit bijections:  NOT COMPLETIONS
346 combined weight-20 rows:         DERIVED NECESSARY DATA ONLY
rank-11 endpoint:                    UNKNOWN
n3=4158 endpoint:                    UNKNOWN
Conway-99:                           UNKNOWN
```

## Inflection

Wave 209 shows that scalar moments and separated point/line censuses are no
longer the right boundary.  The next legitimate constraint must couple the
same named outside points to the same named residual triangles and adjacency
rows.  Wave 210 therefore attacks typed point-to-line incidence and selected
marked-to-outside column compatibility, without enumerating an unknown
99-vertex graph.
