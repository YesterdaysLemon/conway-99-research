# Wave 206 construction, literature, and hostile controls

This package is a discovery-lane submission, not the Wave 206 verifier.

It contains two exact, deliberately relaxed results:

1. Two realizations on the same labeled `99 by 231` linear triple incidence
   satisfy rank-six star coupling, rank-11 square-zero centered Grams,
   `sum_x P_x=0`, and have identical complete labeled `99 by 99` matrices `g`
   and `H`, but their three-center tensors differ on 209,952 ordered entries.
2. Two 99-projector zero-sum controls attain the universal fixed-center bound
   `rank_F3(tau_y)=21` while their diagonal and full entry distributions vary.

The first result is a stronger compatibility blueprint than a pair-local
control, but it is not an SRG or endpoint construction. It is disconnected,
has nonuniform `lambda` and `mu`, has extra triangles, reuses projective
directions, and separates `tau` only on cross-component triples. The second
result has no coupled 231-column incidence. All gaps are repeated in
`exact-results.json`.

## Files

- `certificate.json`: reflection word, simplex, incidence generator, and
  selected controls.
- `exact_check.py`: independent deterministic reconstruction and exact checks.
- `test_exact_check.py`: reproduction and mutation tests.
- `exact-results.json`: frozen machine-readable findings and status wall.
- `derivation.md`: mathematical construction and rank-21 derivation.
- `literature-sources.json`: theorem-by-theorem primary-source hypothesis
  ledger.
- `literature-audit.md`: audit narrative and transfer boundaries.
- `failed-routes.md`: failed inferences and bounded-search restrictions.
- `input-freeze.sha256`: frozen Wave 206 inputs.
- `run-report.yaml`: AGENTS.md run-report record.
- `package-manifest.sha256`: final package hashes.

## Reproduce

From the repository root:

```powershell
python -B attempts\wave206-three-center-hostile-controls\exact_check.py `
  --verify-results attempts\wave206-three-center-hostile-controls\exact-results.json

python -m pytest -q attempts\wave206-three-center-hostile-controls
```

The checker uses only the Python standard library. The test runner requires
`pytest`.

## Status

```text
shared relaxed implication determines tau:  REFUTED
fixed-y rank bound 21 is sharp:             DERIVED
stronger coupled rank-21 control:           UNKNOWN
Conway-99:                                  UNKNOWN
rank-11 endpoint:                           UNKNOWN
n3=4158 endpoint:                           UNKNOWN
Q>=7060:                                    NOT PROVED
automorphism assumption:                    NONE
```
