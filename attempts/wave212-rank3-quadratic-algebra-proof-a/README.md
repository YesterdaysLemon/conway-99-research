# Wave 212 rank-three quadratic algebra, proof A

This package gives two exact, non-bruteforce closures for all three Wave 210
rank-three survivor representatives:

- `F^T F mod 2` has Jordan type
  `J_5(0)^2 + J_3(0)^2 + J_1(0)^69`, forcing the four nontrivial
  Artin--Schreier blocks of any hypothetical `D mod 2`;
- exact conditional projectors on `K` have valid strict diagonal local
  multiplicities, and every pair permits both binary adjacency choices under
  both `2 x 2` PSD tests.

Both tests are consistent.  This package constructs and excludes no `D`.
Global status remains `UNKNOWN`.

Replay with only the Python standard library:

```powershell
python attempts\wave212-rank3-quadratic-algebra-proof-a\exact_check.py --verify
Push-Location attempts\wave212-rank3-quadratic-algebra-proof-a
python -m unittest -v test_exact_check.py
Pop-Location
```

