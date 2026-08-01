# Wave 207 verifier replay log

All commands ran from
`C:\Users\Yeste\OneDrive\Documents\math conjecture` with repository commit
`c58fd917ea8f9622e1388f10b0e0e3c709ba4854`.  `python` below always means the
repository interpreter `\.venv\Scripts\python.exe`.  No system Python was
used for a verdict.

## Source-blind freeze

```powershell
Get-FileHash -Algorithm SHA256 `
  verification\wave207-incidence-tensor-rigidity\protocol-freeze.md
```

```text
exit code: 0
SHA256: e381877375f1f5f270e7ad064db570494a7df12dc0bbf01a0df0d24b67884444
```

## Discovery-package manifests

A verifier-owned PowerShell loop parsed every nonblank manifest line,
accepted either the two-space or `*` SHA256 separator, recomputed every file
hash with `Get-FileHash`, and failed closed on malformed or mismatching
entries.

```text
PASS proof A manifest:       8/8 entries
manifest SHA256: 544e9d469dc0666ff3463f5c7f3b41a4ad3acfde857100c422dd3acea4c6d8ab

PASS proof B manifest:       9/9 entries
manifest SHA256: 87158d7931f6f2440bb176670368b112055b84a0e358a1b6b8ea18cb630e756d

PASS ternary bridge:        11/11 entries
manifest SHA256: 31e3abf3a7e16bf80eb8de4721c683f41d4d20d55f90564398e4d638b3414f99

PASS M7g bridge:            11/11 entries
manifest SHA256: 3fa21f164fd7a7afb13c546447e3a42f9ae870d2d1b8cd5030d254ee61a5c561

PASS kernel endpoint proof C: 11/11 entries
manifest SHA256: bb0a3e8b4821f7533330fcdd9b0fb58085eaefcb2281f387b7356784efacd2e6

combined manifest-loop exit code: 0
```

## Proof A replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-incidence-tensor-code-proof-a\exact_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave207-incidence-tensor-code-proof-a\test_exact_check.py
```

```text
exact result: PASS: Wave207 incidence-tensor canonical checks
unit tests: 3/3 passed
exit code: 0
```

## Proof B replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-mixed-four-center-proof-b\exact_check.py `
  --verify attempts\wave207-mixed-four-center-proof-b\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave207-mixed-four-center-proof-b -p "test_*.py" -v
```

```text
exact result: PASS
unit tests: 5/5 passed
exit code: 0
```

## Ternary adjacency-code bridge replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-ternary-adjacency-code-bridge\exact_check.py `
  --verify attempts\wave207-ternary-adjacency-code-bridge\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave207-ternary-adjacency-code-bridge\test_exact_check.py
```

```text
exact result: PASS
unit tests: 10/10 passed
exit code: 0
```

## M7g incidence-bridge replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-m7g-incidence-bridge\exact_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave207-m7g-incidence-bridge\test_exact_check.py
```

```text
exact result: PASS: Wave207 M7g incidence bridge exact checks
unit tests: 5/5 passed
exit code: 0
```

## Kernel endpoint proof-C replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-kernel-endpoint-proof-c\exact_check.py `
  --verify attempts\wave207-kernel-endpoint-proof-c\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave207-kernel-endpoint-proof-c\test_exact_check.py
```

```text
exact result: PASS
unit tests: 8/8 passed
exit code: 0
```

## Clean-room verifier replay

The clean-room checker imports no Wave 207 discovery module.  It uses the
published M7g representative, verifier-owned finite-field routines, and
reads the frozen rank-four JSON only as candidate certificate data.

```powershell
.\.venv\Scripts\python.exe -B `
  verification\wave207-incidence-tensor-rigidity\independent_check.py --write
.\.venv\Scripts\python.exe -B `
  verification\wave207-incidence-tensor-rigidity\independent_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v `
  verification\wave207-incidence-tensor-rigidity\test_independent_check.py
```

```text
archive write: PASS
archive replay: PASS: Wave207 clean-room verifier result
unit tests: 13/13 passed
exit code: 0
```

The thirteen verifier tests cover M7g rank/cap invariants, all concurrent
matchings, the 81-word enumerator, all 27 polar forms and four sign classes,
729 Gram-radical examples, transition ranks and rectangular edge cases, the
abstract four-center control, point-code identities, the signed-neighbor
distance certificate, both weight-fourteen Farkas certificates, the
nongraphical weight-fourteen control, the restricted 23-vertex certificate,
and the global status wall.

## Primary-source handling

The primary arXiv PDF and gzip e-print were downloaded transiently, hashed,
and inspected.  Their hashes and the relevant source-line mapping are in
`literature-source-audit.md`.  Both transient third-party files and the
generated `__pycache__` were removed from the verifier directory before the
package manifest was constructed.  The source bytes can be recovered by
redownloading arXiv:2405.12011.
