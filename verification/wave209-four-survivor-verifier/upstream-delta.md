# Upstream documentation delta after the blind freeze

The source-blind `input-freeze.sha256` records the bytes actually read before
the verifier protocol was written.  After that barrier was established,
another agent corrected the already-public Wave 208 integration audit:

```text
before  61b3279f9c48cf3b72755ce047cdb8b30a3125596452c7fa5ff72bd8ed3548e8
after   eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754
path    verification/2026-07-31-wave208-integration-audit.md
```

The changed passage refines the already-public weight-14 `q=0` explanation:
the 13-same-sign-edge row exceeds wedge capacity; the 12-edge equality case
forces internal-edge triangle saturation and then contradicts four forced
odd degrees; the 11-edge row survives with one cross edge.  It does not alter
the Wave 208 verdict, retained branches, or `UNKNOWN` status.

The original hash is deliberately not replaced in `input-freeze.sha256`,
because doing so would misstate the bytes used to create the blind protocol.
The new bytes are treated as a post-freeze public-input delta and are pinned
in `post-freeze-inputs.sha256`.
