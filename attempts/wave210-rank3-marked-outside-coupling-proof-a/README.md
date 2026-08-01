# Wave 210 rank-three marked/outside coupling

This package couples the Wave 209 weight-14 marked-line census to the exact
85-column support/outside incidence matrix.  It is a complete labelled
selected-union reduction, not a 99-vertex construction or exclusion.

Reproduce with the repository virtual environment:

```powershell
.venv\Scripts\python.exe -B attempts\wave210-rank3-marked-outside-coupling-proof-a\exact_check.py --verify
.venv\Scripts\python.exe -B -m unittest discover -s attempts\wave210-rank3-marked-outside-coupling-proof-a -p test_exact_check.py -v
```

Key artifacts:

- `derivation.md`: symbolic derivation and exact boundary;
- `exact-results.json`: all 232 containment patterns and all 33 proved case
  orbits with survivor counts and witnesses;
- `hostile-controls.json`: three explicit orbit-representative controls,
  including all 85 support columns;
- `failed-routes.md`: nonclosing relaxations and why they fail;
- `package-manifest.sha256`: final package seal.

Current discovery label: `DERIVED`.  Global status: `UNKNOWN`.

