# Wave 207 ternary adjacency-code bridge

This package maps a hypothetical weight-eight `A_Delta` word to a nonzero
point word in the ternary adjacency kernel.  It proves, using exact signed
neighbor moments, that every nonzero point word has weight at least twelve.
The endpoint image is therefore restricted to weights `14,17,20,23`.

Replay with:

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts/wave207-ternary-adjacency-code-bridge/test_exact_check.py
.\.venv\Scripts\python.exe -B `
  attempts/wave207-ternary-adjacency-code-bridge/exact_check.py `
  --verify attempts/wave207-ternary-adjacency-code-bridge/exact-results.json
```

The weight-fourteen JSON control is not a graph and not a codeword.  The
desired distance `24`, equality classification, endpoint exclusion, and
global Conway-99 problem remain `UNKNOWN`.
