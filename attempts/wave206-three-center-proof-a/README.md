# Wave 206 three-center proof A

This package derives the fixed-root rank-21 three-center Gram model, the
exact four-vertex nonneighbor-fiber geometry, a 21-coordinate first/quadratic
moment formulation, and complete finite marginal censuses for the frozen
low-`t` controls.

The main conclusion is deliberately narrow: all exact root-relative
three-center conditions checked here remain underdetermined.  The missing
constraints include the third pair module of each labelled triple and,
ultimately, coupling the four operators in every fiber through one shared
231-column realization.  No Conway-99 endpoint is proved or refuted.

## Reproduce

From the repository root:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave206-three-center-proof-a\exact_check.py --verify attempts\wave206-three-center-proof-a\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave206-three-center-proof-a\test_exact_check.py
```

## Files

- `protocol.md`: frozen lane and integrity rules.
- `derivation.md`: proofs, exact censuses, scope, and next invariant.
- `failed-routes.md`: refuted or non-evidentiary routes.
- `exact_check.py`: deterministic finite-field checker.
- `test_exact_check.py`: independent assertions over the generated result.
- `exact-results.json`: machine-readable census and witness ledgers.
- `input-freeze.sha256`: frozen upstream inputs.
- `run-report.yaml`: required discovery report.
- `package-manifest.sha256`: hashes of the completed package.

Status: `DERIVED`, pending independent verification.
