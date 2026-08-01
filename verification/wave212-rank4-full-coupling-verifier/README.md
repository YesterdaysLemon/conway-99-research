# Wave 212 rank-four full-coupling verifier

This package closes the Wave210 rank-four verification gap by reconstructing
and comparing the complete point-line systems, rather than accepting solver
status or replaying certificates against a different relaxation.

The clean-room lane first built a strictly larger full-signature relaxation:
2,187 point signatures, 4,752 rows, and roughly twenty thousand W/X columns
per survivor orbit.  Seven independent integer Farkas vectors exclude those
larger systems exactly.  After sealing, the verifier reconstructed the
source's geometric membership filter and forced `H[h]` grouping, matched all
seven smaller matrices column-for-column, and replayed the seven archived
integer duals.

The checked conclusion is conditional: all 51 Wave209 rank-four branches are
excluded.  No graph automorphism is assumed.  Rank three and the global
Conway-99 problem remain `UNKNOWN`.

See `protocol.md` for the exact gates, `audit.md` for the verdict and evidence
boundary, and `source-contact-log.md` for the clean-room chronology.
