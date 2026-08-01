# Wave 208 verifier delta after the Wave 209 protocol freeze

The historical `input-freeze.sha256` records the Wave 208 verifier-manifest
bytes actually available when the Wave 209 protocol was frozen:

```text
frozen  5cc06aa4171eb1ea66227f87fe9f63f90a41c93403d6fa2e8b8627bc1b828fd1
path    verification/wave208-global-residual-verifier/package-manifest.sha256
```

The current corrected and independently re-audited public Wave 208 package is:

```text
current c9551a7c4d62a57f081b8008f49b9e27fb0372f50a7d114e10136557242fbab4
audit   eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754
```

Those current hashes are pinned in `post-freeze-inputs.sha256`.  The old
outer hash is deliberately not replaced: doing so would misstate the bytes
used at protocol-freeze time.  The earlier manifest contents are not present
in this worktree, so a file-by-file byte delta cannot be reconstructed from
the outer hash alone.  No such reconstruction is claimed.

This is an evidence-provenance correction, not a retroactive input change.
The Wave 209 rank-three and rank-four verifiers independently reconstruct the
finite objects they promote, and the current Wave 208 integration retains the
same four-survivor and global-`UNKNOWN` boundary imported by this protocol.
