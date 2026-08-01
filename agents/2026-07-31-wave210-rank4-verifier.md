# Wave 210 rank-four coupling verifier

## Outcome

`PENDING_VERIFICATION`; promotion to `VERIFIED` is vetoed for this run.

I sealed a source-blind protocol, input hashes, an independent necessary
incidence relaxation, and matrix hashes before opening the proof-B package.
The blind work recovered the seven Wave 209 survivor orbits and all 51
labelled branches, checked the 99-point/223-line census invariants, derived
the `H[h]` matching groups, point residual degree, and exact incident-`t`
demand.  It assumed no target automorphism.

After unsealing, the source was found to enumerate exact three-signature
local triangle columns over the full admissible signature universe.  My blind
relaxation instead fixed one archived pair of survivor controls and used
separate point-role incidence columns.  Its hashes therefore cannot
authenticate the source matrices or Farkas vectors.  This is a verification
gap, not a detected mathematical contradiction.

The assigned outer manifest digest matched, and all 12 manifest entries
matched.  A bounded source replay plus unittest command exceeded 64 seconds
without a captured completion result; the remaining test processes and cache
were cleaned up.  Timeouts were not promoted to evidence.

See
`verification/wave210-rank4-point-line-coupling-verifier/audit.md` for the
derivation audit, exact gap, and continuation checklist.  Rank three and the
global Conway-99 claim remain `UNKNOWN`.
