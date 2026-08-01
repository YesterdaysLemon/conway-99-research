role: construction
date_utc: "2026-08-01T02:20:00Z"
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: >-
  Conditional M7g polar-form norm divisibility at the prism-free rank-11
  endpoint.
inputs:
  - path: attempts/wave208-m7g-norm-divisibility/input-freeze.sha256
    sha256: 40e9bf121c63ffe4d1494c39c4aed0ec796e2501293d310a43f6d6b5368e7813
method: >-
  Exact integer SRG norm identity plus complete 27-form enumeration in each
  of four labelled relative sign classes.
command: >-
  .venv\Scripts\python.exe -m unittest attempts\wave208-m7g-norm-divisibility\test_exact_check.py -v
outputs:
  - path: attempts/wave208-m7g-norm-divisibility/exact-results.json
    sha256: ea3481c805a88d233f9e35f1c9e9c61e8546e7f6ddb56add2e552b9a80ec3703
  - path: attempts/wave208-m7g-norm-divisibility/derivation.md
    sha256: 2c480d92d0c9f47d2425b3a0aef0e02d2dd89be27404877f46910395699b46f7
limitations: >-
  Discovery agent does not promote its result. Four polar forms survive;
  global Conway-99 status remains UNKNOWN.
