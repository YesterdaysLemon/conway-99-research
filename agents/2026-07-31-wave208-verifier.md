role: verifier
date_utc: "2026-08-01T02:50:43Z"
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Conditional prism-free M7g branch only: verify the norm-divisibility
  reduction and proof-B spectral lift, exact 27-form and marked-subset
  censuses, proof-A integer spectral splitting and complementary-Fano
  overlap reduction, local positive controls, and all outside boundaries.
inputs:
  - path: verification/wave208-global-residual-verifier/blind-freeze.sha256
    sha256: 0b01e077b4e52dacb4e2683903f16b9afa7916ae649b69882cb008c4c9a300d9
  - path: attempts/wave208-global-residual-rigidity/protocol.md
    sha256: 3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740
  - path: attempts/wave208-m7g-norm-divisibility/package-manifest.sha256
    sha256: a633dff62e4e1127b8a0c7329928e110d1fef1e78f1f322bbc4e250e277167f3
  - path: attempts/wave208-marked-m7g-proof-b/package-manifest.sha256
    sha256: f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc
  - path: attempts/wave208-integer-lift-proof-a/package-manifest.sha256
    sha256: 28d69162a8f52bdc325471946efecad890b1edac33f3576bdba8777e32887202
method: >-
  Freeze integer-lift, composition, product-one, outside-coordinate,
  graphical-realization, and status-wall obligations before source access;
  independently reconstruct the labelled M7g polar net without importing
  discovery code; separately enumerate linear and tensor relations, all 105
  perfect matchings, all marked subsets, and both candidate controls; then
  symbolically rederive the point-code spectral split, enumerate every
  residue shell and labelled Fano partition, replay the imported Wave94
  theorem and 22-vertex candidate, compare archived results, and construct
  omitted-outside-row witnesses.
command: >-
  .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\independent_baseline.py
  --verify; .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\independent_m7g_norm.py
  --verify; .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\post_source_m7g_audit.py
  --verify; .venv\Scripts\python.exe -B -m unittest
  verification\wave208-global-residual-verifier\test_independent_baseline.py
  verification\wave208-global-residual-verifier\test_independent_m7g_norm.py
  verification\wave208-global-residual-verifier\test_post_source_m7g_audit.py
  -v; .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\independent_proof_b.py
  --verify; .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\post_source_proof_b_audit.py
  --verify; .venv\Scripts\python.exe -B -m unittest -v
  verification\wave208-global-residual-verifier\test_independent_proof_b.py;
  .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\independent_proof_a.py
  --verify; .venv\Scripts\python.exe -B
  verification\wave208-global-residual-verifier\post_source_proof_a_audit.py
  --verify; .venv\Scripts\python.exe -B -m unittest -v
  verification\wave208-global-residual-verifier\test_independent_proof_a.py
outputs:
  - path: verification/wave208-global-residual-verifier/audit.md
    sha256: e45e916add73ee82d6a1e531cea6d9a7e431bb402ed94016748c6df453dbb81a
  - path: verification/wave208-global-residual-verifier/m7g-norm-independent-results.json
    sha256: 53cbdf2be25497bf653cf52d0aed4b2d5bcac41e205c20a3e53f24b829355f55
  - path: verification/wave208-global-residual-verifier/m7g-norm-post-correction-audit.json
    sha256: d1465edc7eaedb2b1d5fd452ecb269ecfd9b5f704b840edffb3ab2ec8f8ebeae
  - path: verification/wave208-global-residual-verifier/proof-b-independent-results.json
    sha256: 66fff002a34d835e0d513603817834bcbdbc4da4e99934973bb777231dfb0d73
  - path: verification/wave208-global-residual-verifier/proof-b-delta-audit.json
    sha256: 8bfb2dd615e9341ca13a4c85ea47306e9a01fb0b5276abcbf13e2c9c3775d885
  - path: verification/wave208-global-residual-verifier/proof-a-independent-results.json
    sha256: a0ab63233a893af8631b4306ee68e2cb10fecbacad1c2a5391f1c7f7e77582c7
  - path: verification/wave208-global-residual-verifier/proof-a-delta-audit.json
    sha256: 0f45bb1c6743d2b7a6c60ef758769057c72c0ca10c1e09d3dcb68ea357248eef
limitations: >-
  Four polar forms survive: three rank-four norm-56 branches and rank-three
  point-weight 14 and 20 branches. The local controls enforce only internal
  necessary equations; outside coordinates, binary completion, and the full
  incidence frame remain absent. Proof A excludes no residual weight: five
  other balanced shells, the q=0 one-cross-edge case, the norm-14
  alpha=0/k=2,3,4 cases, and every weight-17/20/23 arithmetic branch remain.
  No graph or nonexistence certificate is supplied; the endpoint and global
  Conway-99 status remain UNKNOWN.
