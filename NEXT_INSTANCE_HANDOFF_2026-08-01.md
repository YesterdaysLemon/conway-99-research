# Next-instance handoff: Wave 212 verified rank-four closure and rank-three wall

```yaml
role: orchestrator
date_utc: 2026-08-01T05:33:00Z
git_commit: 698f4db2cecd67fb4b9cfa8ff2bf7b375d9d93f3
claim_label: UNKNOWN
scope: >-
  Handoff of the independently verified conditional exclusion of every
  rank-four survivor and the exact, still-open rank-three quadratic boundary.
inputs:
  - path: verification/wave212-rank4-full-coupling-verifier/package-manifest.sha256
    sha256: 01427c528c465c70a770313c67d3c966addd333c9f88f19507a75effc7dddc65
  - path: attempts/wave212-rank3-common-neighbor-proof-b/package-manifest.sha256
    sha256: 6fbd4427f701d63e40df2718057dab37b0b7930cc5dc9f0ed7ecf76eab813447
  - path: attempts/wave212-rank3-quadratic-algebra-proof-a/package-manifest.sha256
    sha256: 10dbc03ce2ea6e9f5bed46ab5b735fe36d6dddd073a40010c947e59f516496ab
  - path: verification/wave212-rank3-symbolic-verifier/package-manifest.sha256
    sha256: 0a291b568380eb7addef534a1af1d533c6d09ed1c8f33676f1c2225e5c1fb258
method: >-
  Preserve source/verifier separation, replay exact integer certificates,
  retain hostile controls with their actual failed equations, record the
  verifier-side Jordan correction without self-promotion, and stop at the
  first honest global wall.
outputs:
  - path: NEXT_INSTANCE_HANDOFF_2026-08-01.md
limitations:
  - Every result is conditional on the frozen rank-11 endpoint reductions.
  - Rank three is not constructed or excluded.
  - The verifier-derived Jordan allocation awaits separate promotion.
  - No graph, counterexample, unrestricted nonexistence proof, or Conway-99
    resolution is claimed.
```

## State to trust

Wave 212 closes the old Wave 210 rank-four verification veto.  A clean-room
verifier first reconstructed seven larger systems with all 2,187 integral
point signatures, 4,752 rows, and 19,348--20,524 columns, then sealed seven
new exact integer Farkas vectors.  After unsealing, it independently rebuilt
the geometric membership filter and matched every semantic row and column of
the source systems:

```text
orbit       0      2      4     11     12     14     23
points    444    576    532    532    488    510    444
rows     1266   1530   1442   1442   1354   1398   1266
W cols  12110  11444  11672  11672  11888  12003  12110
```

All seven archived Wave 210 duals replay exactly with `A^T y>=0` and
`b^T y<0`.  Exact sign-preserving data transports cover all 51 labelled
branches and 601,377 local patterns without assuming an automorphism of an
unknown graph.  Therefore all three rank-four forms are conditionally
excluded.  This is `VERIFIED`; it says nothing about rank three.

## Rank-three exact boundary

For each surviving rank-three orbit `0,4,29`, a completion would have

```text
64 outside edges with support overlap one,
456 outside edges with support overlap zero,
152 all-outside triangles,
2079 total four-cycles.
```

The support-refined four-cycle counts are
`1211,588,40+220,12,8`.  Simultaneous support-colour one-factors exist in all
three orbits.  The committed labelled incidence controls satisfy all 85
degrees, all ten selected pair values, and all 104 zero-target rows, but only
`499/534/532` of 1,190 `FD` entries and `1256/1259/1299` of 3,570 quadratic
pair rows.  They are hostile controls, not completions.

Over `F_2`, `F^T F` has power ranks `12,8,4,2,0` and Jordan type
`J5^2+J3^2+J1^69`.  Conditional projector diagonals and every `2 x 2` minor
allow both adjacency choices for all 3,570 pairs.  The independent verifier
also proved that the forced action on `U` is nilpotent, so every nontrivial
Artin--Schreier chain is zero-primary and conditional ranks of
`D,D^2,...,D^5` are `52,48,44,42,40`.  This last sharpening was discovered
by the verifier and remains `DERIVED` pending separate independent promotion.

## Status wall

```text
rank-four forms:                    3/3 CONDITIONALLY EXCLUDED (VERIFIED)
rank-four labelled branches:       51/51 CONDITIONALLY EXCLUDED (VERIFIED)
rank-three case orbits:             0,4,29 STILL OPEN
full 85 x 85 outside block D:       NONE
full 99-vertex adjacency:           NONE
rank-11 endpoint:                   UNKNOWN
n3=4158 endpoint:                   UNKNOWN
rigorous n3 interval:               708<=n3<=4158
Conway-99:                          UNKNOWN
```

The public ledgers deliberately remain at Wave 209 in this bounded wrap-up;
the Wave 212 packages and this handoff are the review surface for the next
integration pass.

## Reproduction

Run from the repository root with the repository interpreter:

```powershell
& '.\.venv\Scripts\python.exe' -B `
  attempts\wave212-rank3-common-neighbor-proof-b\exact_check.py --verify
& '.\.venv\Scripts\python.exe' -B `
  attempts\wave212-rank3-quadratic-algebra-proof-a\exact_check.py --verify
& '.\.venv\Scripts\python.exe' -B `
  verification\wave212-rank3-symbolic-verifier\independent_verify.py --verify
& '.\.venv\Scripts\python.exe' -B -m unittest -v `
  verification\wave212-rank4-full-coupling-verifier\test_post_source_audit.py
```

## Next legitimate task

Do not repeat rank, trace, degree-only, coloured-matching, global triangle,
four-cycle, or `2 x 2` projector relaxations.  The live problem is the
simultaneous entrywise enforcement of

```text
F D       = 2J-(A_S+I)F,
D^2+D     = 12I+2J-F^T F,
D 1       = 14 1-F^T 1
```

for rank-three orbits `0,4,29`, preferably through a proof-producing
forbidden-common-neighbor or higher-projector-minor argument.  Preserve
`UNKNOWN` unless a complete `85 x 85` block, a checked 99-vertex graph, or a
global nonexistence certificate is produced.

The isolated branch is `codex/wave212-global-coupling`; the prior clean
handoff branch and draft PR #6 remain untouched.
