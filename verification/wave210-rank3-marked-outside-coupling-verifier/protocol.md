# Wave 210 rank-3 marked-outside coupling: source-blind verification protocol

Frozen at `2026-08-01T03:56:41Z`, before opening any file in the submitted
discovery package.  At freeze time the verifier knew only the task statement,
the package path, the expected outer-manifest digest, and the byte-level
inventory in `input-freeze.sha256`.

## Scope wall

This audit tests a finite, conditional coupling computation.  It does **not**
claim a completion of `D`, a graph construction, a contradiction, or a solution
of Conway 99.  Passing results may support only `DERIVED` status for the exact
enumerated subproblem.  The unrestricted problem remains `UNKNOWN`.

## Frozen target assertions

1. Generate complete labelled sets, without quotienting by a target-graph
   automorphism, and reproduce the transitions `204 H -> 96 H` and
   `20,928 packings -> 1,536 packings`.
2. Generate the complete labelled triple space of size `93,757,440` and its
   accepted subset of size `55,296`; compare complete sorted serializations or
   collision-resistant digests after unsealing, not counts alone.
3. Independently derive the two explicitly permitted bookkeeping actions:
   the order-48 polar action and the order-4 automorphism group of the fixed
   auxiliary graph.  Check closure, identity, inverses, faithful action, orbit
   partitions, stabilizers, and Burnside counts.  No automorphism of the unknown
   target graph may be assumed.
4. Reproduce `33` case orbits and identify exactly `3` accepted case orbits by
   comparing their complete labelled members.
5. Enumerate all `4,480` submitted `F` configurations.  For every configuration,
   compute matrix rank exactly over the declared field and require rank `13`;
   independently decide the stated local one-factor feasibility condition and
   require it for every case.
6. Audit that every search restriction is explicit and logically licensed,
   especially each symmetry quotient, canonical representative, fixed label,
   and local feasibility filter.  Verify that no completion of `D` is produced
   or silently assumed.
7. Run hostile controls that must fail closed: mutate one incidence/coordinate,
   delete and duplicate labelled objects, corrupt an orbit generator, alter a
   claimed rank, break one-factor feasibility, corrupt a stored result, and
   corrupt the package manifest.

## Independent method frozen before unsealing

- Build a clean-room standard-library verifier in this directory.  Discovery
  code will never be imported.
- After this protocol is frozen, inspect the submission solely to recover the
  formal object definitions and upstream references.  Freeze every newly
  identified upstream input by SHA-256 before opening it.
- Re-express objects as immutable tuples/bitmasks and enumerate them with loops
  whose nesting follows the mathematics, not the discovery implementation.
- Use independent canonical serialization and SHA-256 multiset/set digests.
- Implement finite-field Gaussian elimination independently.
- Implement one-factor feasibility independently by exhaustive perfect-matching
  generation/backtracking on the small local graph.
- Generate group closure from independently checked permutations; audit every
  orbit as a disjoint cover of the labelled universe and cross-check with
  Burnside's lemma.
- Only after clean-room outputs are sealed, run the submitted checker/tests and
  compare complete labelled sets, orbit membership, ranks, and feasibility
  witnesses.

## Verdict rule

Return `PASS / NO VETO` only if all manifest hashes, complete labelled-set
comparisons, symmetry audits, exact ranks, feasibility decisions, and hostile
controls reproduce.  Any count-only agreement, unexplained restriction,
unlicensed symmetry, incomplete comparison, or mutation accepted by the checker
is a precise finding and prevents a clean pass.
