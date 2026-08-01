# Wave 210 rank-four point/line coupling verifier protocol

Sealed source-blind at `2026-08-01T04:18:28Z`, before any Wave 210 discovery
file was opened.  At sealing time only the filenames in
`attempts/wave210-rank4-point-line-coupling-proof-b/` and the orchestrator's
outer-manifest digest were known.

## Frozen claim and boundary

Audit the claimed *necessary* point-to-residual-triangle coupling for every
one of the seven Wave 209 rank-four survivor orbits, and the transport of an
orbit result to all 51 labelled branches.  This audit can verify only the
rank-four branch under the inherited Wave 206 endpoint assumptions.  It must
not alter the global or rank-three status, both of which remain `UNKNOWN`.

## Independent reconstruction protocol

1. Authenticate the prior Wave 209 point-signature inputs using
   `input-freeze.sha256`, and parse the two frozen JSON controls without
   importing Wave 209 or Wave 210 Python code.
2. Reconstruct the 223 residual lines from the labelled 99-vertex incidence
   model.  For every selected point--line incidence, group residual lines by
   the inherited value `H[h]`; compute each point's degree and its required
   incident-`t` total.
3. Enumerate every allowed point signature and every allowed local residual
   triangle column directly from the defining nonnegative-integer conditions.
   Record the complete ordered row and column keys.  No target automorphism,
   coordinate ordering assumption, or stabilizer restriction is permitted.
4. For each of the seven Wave 209 orbit representatives, build the exact
   integer equality system `A x = b`, `x >= 0`.  Derive an integer/rational
   Farkas row `y` whose orientation is checked by direct dot products:
   `y^T A >= 0` componentwise and `y^T b < 0`.  Solver status is never accepted
   as a certificate.
5. Seal the independently generated rows, columns, systems, and dual checks.
   Only then open the Wave 210 source package.  Compare full ordered and
   unordered matrices/columns/certificates, validate its manifest, transport
   orbit conclusions to all 51 labelled Wave 209 branches by explicit
   permutation data, and replay hostile mutations (dual sign, coefficient,
   RHS, column deletion/addition, and branch-map corruption).

## Restrictions to audit

- residual-line completeness (exactly 223, no duplicates);
- selected-incidence completeness and derivation;
- all `H[h]` groups and their membership;
- point-degree and incident-`t` demand equations;
- local-signature and local-triangle-column completeness;
- exact arithmetic only;
- seven orbit representatives and all 51 labelled branches;
- no assumed automorphism of the target graph or certificate;
- every symmetry quotient accompanied by explicit expansion/transport data.

## Stop rule

If the clean-room reconstruction cannot be completed in the allotted run,
publish a precise `UNKNOWN`/pending-verification wall.  A source replay alone
cannot earn `VERIFIED`.
