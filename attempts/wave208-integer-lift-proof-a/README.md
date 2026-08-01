# Wave 208 integer-lift proof A

This package turns the pointwise lift `z=Ax/3` into exact integral vectors
in both restricted eigenspaces.  Its strongest conditional result concerns
balanced weight 14.

If `q=z-x` has norm 14, then the independently verified short-vector theorem
makes its support the complementary-Fano `7+7` design.  A complete labelled
Fano capacity census and a coupled outside-endpoint argument force

```text
supp(x) intersect supp(q): exactly six opposite signs, no same signs,
|supp(x) union supp(q)|=22,
z: eight +1 and eight -1,
exclusive split: k in {2,3,4} with forced K3/C4 shapes.
```

An exact 22-vertex hostile partial control survives all displayed lift and
eigenvector equations, so this is a strict reduction rather than a
weight-14 exclusion.  The other balanced spectral shells and weights 17,
20, and 23 remain open.  Conway-99 remains `UNKNOWN`.

Reproduce:

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave208-integer-lift-proof-a\exact_check.py `
  --verify attempts\wave208-integer-lift-proof-a\exact-results.json

.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave208-integer-lift-proof-a\test_exact_check.py
```

