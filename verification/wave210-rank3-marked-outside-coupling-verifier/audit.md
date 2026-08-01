# Wave 210 rank-three marked/outside coupling audit

```yaml
role: verifier
date_utc: 2026-08-01T04:19:50Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: sealed conditional Wave 210 weight-14 selected-union coupling; no D completion
inputs:
  - path: attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256
    sha256: d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722
  - path: verification/wave210-rank3-marked-outside-coupling-verifier/input-freeze.sha256
    sha256: 717b36cfbfec5d6c22cc968518e08a72e0a9764d1b5ca662dc99f31bd190c11d
  - path: verification/wave210-rank3-marked-outside-coupling-verifier/pre-source-comparison-seal.sha256
    sha256: 8fac8f07e3c3ca2605e30e7e08387586d5ef028881d0fcb865b73c0676f34067
method: independent bitmask enumeration, brute-force automorphism audit, exact rank, perfect-matching recursion, full labelled-set comparison, hostile mutations
command: .venv/Scripts/python.exe -B verification/wave210-rank3-marked-outside-coupling-verifier/verify_sealed.py
outputs:
  - path: verification/wave210-rank3-marked-outside-coupling-verifier/independent-results.json
    sha256: 350134f2e5593d3d83e3463b1a536622db294a127c5fccab05a7b42858ce42bd
  - path: verification/wave210-rank3-marked-outside-coupling-verifier/post-source-audit.json
    sha256: 52c3e04799cc25547f8caad057b7cf224a37bbdb275a6844f806657b0fab76bb
limitations: conditional local reduction only; D unresolved; no 99-vertex graph or exclusion; Conway-99 UNKNOWN
```

## Verdict

**PASS / NO VETO.**  No mathematical, completeness, symmetry, manifest, or
scope discrepancy was found.  The sealed finite claim remains `DERIVED`; the
unrestricted problem remains `UNKNOWN`.

## Independent reconstruction

The source-blind protocol was frozen before opening discovery internals.  A
separate standard-library checker then reconstructed:

| object | before | after / result |
|---|---:|---:|
| labelled marked graphs `H` | 204 | 96 survivors |
| labelled ordered `H`/packing cases | 20,928 | 1,536 survivors |
| labelled case/deficit triples | 93,757,440 | 55,296 survivors |
| all deficit bijections | 5,040 | 4,480 capacity-compatible `F` configurations |
| case orbits | 33 | exactly orbits 0, 4, 29 survive |

The accepted full labelled sets—not merely their counts—were materialized and
compared.  Their SHA-256 digests are:

- all `H`: `c9c26bfef9b2e3f5a5ebe36e527986195a30563052b9d23ace7c24f110484488`;
- all cases: `f372a8be49b588a1c4cb0093b4fa0db9d8d1cf1a38ae65263934804cf62aea9f`;
- surviving `H`: `00d53b199579bb08d77f8b7608ac7f707352c25e47c32417574e6e2c8ea31c45`;
- surviving cases: `d4e3c24aa2454ad35f5afa2512d983e99fc15f682539a243832db62ae7542b68`;
- surviving triples: `2ea2e847d91a77908f8b19d77879ea21c1849fecad4cd4ee91db7926588bf833`.

All 4,480 canonical column multisets and residual matrices agree with the
submission.  Each satisfies the exact common Gram identity.  That Gram matrix
has rational rank 13 and signed kernel `(1^7,-1^7)`; because
`rank(F F^T)=rank(F)` over the rationals/reals, every `F` has rank 13.

All 62,720 support-neighborhood tests were independently counted.  Every one
of the 4,480 configurations is feasible at all 14 support vertices.  The exact
matching-count distribution is `68:7808`, `78:17536`, `90:1536`,
`594:18496`, `604:17344`.

## Completeness and symmetry audit

- `H` is generated as every labelled five-edge subset of the twelve permitted
  opposite-sign pairs satisfying the frozen degree/isolation constraints.
- Support packings are ordered partitions of all seven labelled points; no
  target labels are identified.
- All `7!` deficit-edge bijections are tried before the nonnegative Gram
  residual filter.
- Brute force over all `8!` line permutations gives the complete order-48
  polar automorphism group.  Brute force over all `7!` support permutations
  gives the complete order-4 rooted-support automorphism group.
- Identity, inverses, and closure were checked for both groups and the full
  order-768 coupled action.  It is faithful.  Burnside's fixed-point sum is
  `25,344`, hence exactly `25,344 / 768 = 33` case orbits, with sizes
  `192^1, 384^10, 768^22`.
- All 4,480 deficit bijections are closed under all 32 induced independent
  support relabellings/sign actions.  Complete orbit member sets and complete
  per-orbit matching-index sets agree with discovery.
- These are automorphisms only of the frozen polar and auxiliary support
  structures.  No automorphism of the hypothetical target graph is assumed.

## Hostile controls and manifests

All outer-manifest entries, exact package-file coverage, and upstream input
hashes validate; the observed outer digest is the supplied
`d2c2bef...722`.  An in-memory manifest mutation is rejected.

The three sealed controls for orbits 0, 4, and 29 replay independently: Gram
identity, distinct selected copies, containment, triangle cliques, all 28 polar
counts, induced common-neighbor caps, `Ac=3c`, and all 14 local one-factors pass.
Each control has only a 19-point selected union and at least 80 isolated
outside vertices in its recorded partial adjacency, so none is a 99-vertex
completion.

Hostile mutations rejected a support incidence coordinate change, deleted and
duplicated labelled objects, a bad support-group generator, an altered rank
claim, an incompatible local edge, a changed stored total, a deleted accepted
triple, a corrupt manifest, and a deleted mandatory triangle edge.

## Harness note and stopping wall

The pre-source-sealed `independent_check.py --verify` command completed the full
recomputation but its last assertion compared JSON arrays with in-memory Python
tuples and therefore failed on representation type alone.  The additive
`verify_sealed.py` wrapper performs canonical JSON normalization; it does not
change the sealed enumeration or outputs.  This is a verifier-interface defect,
not a discovery discrepancy.

No `85 x 85` binary block `D` satisfying the remaining block equations is
constructed or excluded.  No degree/common-neighbor completion on 99 vertices
is claimed.  The rank-three branch, rank-11 endpoint, and Conway-99 remain
`UNKNOWN`.
