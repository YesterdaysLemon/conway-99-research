# Failed routes and non-results

- Orbit 0: a 45-second binary MILP for symmetry, zero diagonal, all entries of
  `FD`, all degrees, and ten selected pair values returned no primal before
  its cap.  This is inconclusive.
- Orbit 4: the identical 45-second test also returned no primal before its
  cap.  This is inconclusive.
- Denominator-2 and denominator-4 integer-grid versions were tried for each of
  orbits 0 and 4 with 20-second caps.  None returned a primal.  These non-hits
  are not rational infeasibility certificates.
- An exact-rational SMT attempt for orbit 0 exceeded its time cap with no model
  and no refutation.  It is not evidence.
- Trace, square-trace, characteristic-polynomial integrality, the rational
  `U/K` decomposition, and the mod-2 minimal-polynomial restriction are all
  compatible with a completion.  They do not exclude any of the three cases.
- The explicit orbit-29 graph satisfies the complete linear relaxation but
  violates 2,416 off-diagonal quadratic equations.  It is not a 99-vertex
  graph, an SRG, or evidence that such a graph exists.

No search in this package assumes an automorphism of the target graph, and no
solver exit code is used as a certificate.
