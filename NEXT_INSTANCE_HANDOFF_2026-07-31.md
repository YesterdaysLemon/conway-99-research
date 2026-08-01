# Next-instance handoff: Wave 209 public checkpoint and Wave 210/211 frontier

```yaml
role: orchestrator
date_utc: 2026-08-01T04:29:11Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: UNKNOWN
scope: >-
  Handoff of the verified public Wave 209 checkpoint, the independently
  reproduced Wave 210 rank-three reduction, the still-unverified Wave 210
  rank-four exclusion claim, and the Wave 211 rank-three stopping wall.
inputs:
  - path: verification/2026-07-31-wave209-integration-audit.md
    sha256: eda1a6569a545ce6d4b550f56e01ee4f6396da1edfea3e5017c4e7ab357c0d99
  - path: attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256
    sha256: d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722
  - path: verification/wave210-rank3-marked-outside-coupling-verifier/package-manifest.sha256
    sha256: d7f30a8c3e5d89c363f88da64d0a0baf2a2c933694e6bf12efdb94e6cd3132fb
  - path: attempts/wave210-rank4-point-line-coupling-proof-b/package-manifest.sha256
    sha256: 7eb45280b61e1612f4d70aa95922b7821e16aa3c426832eadb8995809d5cff78
  - path: verification/wave210-rank4-point-line-coupling-verifier/package-manifest.sha256
    sha256: 1f39e44b07108a78a9b17585224c978bac3ea2d6ece8b8efc85f5e9f84e4e9e5
  - path: attempts/wave211-rank3-outside-block-proof-b/package-manifest.sha256
    sha256: c8066f81ad607d598755442994c7804ebc375f9d637ed33e5cbd8335aae47a10
method: >-
  Preserve the last independently integrated public state, separate sealed
  discovery from independent verification, retain failed relaxations and
  hostile controls, and identify the smallest exact continuation tasks.
outputs:
  - path: README.md
    sha256: 5c2f09069d22d64842ba6e760e48c5574bfea795deccf89643f9ea460de8c6c3
limitations:
  - Conway-99, rank 11, and n3=4158 remain UNKNOWN.
  - The Wave 210 rank-four source claim is DERIVED and has a promotion veto.
  - Wave 211 is a stopping-wall result, not an exclusion or construction.
  - AGENTS.md names Orchestrator as a role but omits it from its fenced enum.
```

## State to trust

The public ledgers currently stop at **Wave 209**.  That checkpoint has an
independent `PASS / NO VETO`: 43/43 manifest entries and 41/41 tests replay,
the rank-three `352` table is aggregate-only, the `346` cap remains
`DERIVED`, and the rank-four point census excludes 198 of 249 labelled
branches while leaving 51 anonymous controls.  No graph or endpoint is
claimed.

Wave 210 rank three is also independently reproduced, but has not been folded
into `CLAIMS.yaml`, `OBLIGATIONS.yaml`, or `STATUS.yaml`.  Conditional on the
rank-three weight-14 survivor, exact marked/outside coupling gives

```text
204 labelled H               -> 96
20,928 ordered packing cases -> 1,536
93,757,440 labelled triples  -> 55,296
33 proved case orbits        -> {0,4,29}
```

The verifier matched complete labelled sets, all 4,480 support-incidence
configurations, all 62,720 local matching vectors, and the order-48/order-4
symmetry actions.  No target automorphism was assumed.  The unknown `85 x 85`
outside block `D` remains absent, so this is not a completion.

## Do not promote yet

The Wave 210 rank-four source package archives seven exact integer Farkas
vectors that claim to exclude all seven remaining constraint orbits, hence all
51 labelled rank-four branches.  Source replay and 7/7 source tests pass, but
the fresh verifier returned `PENDING_VERIFICATION` and vetoed promotion.  Its
blind relaxation recovered the seven orbits, all 51 branches, and the necessary
incidence identities, but it did not independently reconstruct the source's
full 11,444--12,110-column local-triangle matrices.  A bounded verifier replay
timed out and is explicitly neither pass nor failure.

The next verifier must independently generate every admissible point
signature, every realizable residual-triangle type, and every exact local
three-signature decomposition; hash the full row/column universe; then replay
the seven archived duals and hostile mutations on all 51 transported branches.
Until then, all three rank-four forms remain public-status survivors.

## Rank-three stopping wall

Wave 211 proves the forced decomposition

```text
U=im(F^T)+<1>,  dim(U)=14;    K=ker(F) intersect 1^perp,  dim(K)=71.
```

The forced characteristic polynomial on `U` and the conditional spectrum
`3^40,(-4)^31` on `K` are arithmetically consistent.  Orbit 29 has an explicit
520-edge binary hostile control satisfying all 1,190 linear `FD` equations,
all 85 degrees, and ten selected pair values, but it fails 2,416 of 3,570
quadratic pair equations.  It is not an SRG.  Capped searches for orbits 0 and
4 are inconclusive.  This closes the purely linear/spectral shortcut: the next
rank-three attack must use the quadratic common-neighbor block or an equivalent
global invariant.

## Reproduction commands

Run from the repository root with the repository virtual environment:

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave210-rank3-marked-outside-coupling-proof-a\exact_check.py --verify
Push-Location attempts\wave210-rank3-marked-outside-coupling-proof-a
..\..\.venv\Scripts\python.exe -B -m unittest -v test_exact_check.py
Pop-Location

.\.venv\Scripts\python.exe -B `
  verification\wave210-rank3-marked-outside-coupling-verifier\verify_sealed.py
.\.venv\Scripts\python.exe -B `
  verification\wave210-rank3-marked-outside-coupling-verifier\post_source_audit.py --verify
.\.venv\Scripts\python.exe -B -m unittest discover `
  -s verification\wave210-rank3-marked-outside-coupling-verifier `
  -p test_verifier.py -v

.\.venv\Scripts\python.exe -B `
  attempts\wave210-rank4-point-line-coupling-proof-b\coupling_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave210-rank4-point-line-coupling-proof-b\test_coupling_check.py

.\.venv\Scripts\python.exe -B `
  attempts\wave211-rank3-outside-block-proof-b\exact_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave211-rank3-outside-block-proof-b `
  -p test_exact_check.py -v
```

The presealed rank-three verifier's direct `independent_check.py --verify`
has a documented tuple-versus-JSON-list comparison defect after completing the
calculation.  Use the additive sealed `verify_sealed.py`; do not rewrite the
historical verifier seal.

## Recommended continuation order

1. Complete the Wave 210 rank-four fresh verifier described above.
2. Integrate Wave 210 only after that gate; keep rank-three and rank-four
   labels separate if the rank-four verifier remains pending.
3. On rank three, attack `D^2+D=12I+2J-F^TF` for orbits 0, 4, and 29 using
   exact quadratic/common-neighbor structure.  Do not repeat linear `FD`,
   degree-only, scalar-moment, or conditional-spectrum relaxations.
4. Preserve `UNKNOWN` unless a complete 99-vertex adjacency certificate or a
   checked global nonexistence certificate is produced.

The working branch is `codex/wave206-global-extension`; draft PR #6 is the
review surface.  The final handoff commit is the commit containing this file.
