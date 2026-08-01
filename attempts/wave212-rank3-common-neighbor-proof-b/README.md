# Wave 212 rank-three common-neighbor proof B

This package gives an exact combinatorial reduction of the outside block for
the three Wave 210 rank-three representatives `0`, `4`, and `29`.  It does not
construct or exclude an `srg(99,14,1,2)`.

The main consequences are:

- the 520 outside edges split into 64 support-coloured edges and 456 disjoint-
  support edges;
- the latter must form 152 all-outside triangle blocks;
- the complete four-cycle census by number of support vertices is
  `1211, 588, 260, 12, 8`, with the two-support term split as `40+220`;
- all fourteen coloured one-factors can be chosen simultaneously in every
  orbit, so that layer gives no obstruction;
- explicit labelled `64+152` incidence controls survive degrees, all ten
  selected pair values, and all 104 zero-target pair constraints, but fail
  many `FD` and quadratic equations and are not graph completions.

Reproduce with the repository interpreter:

```powershell
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B `
  attempts\wave212-rank3-common-neighbor-proof-b\exact_check.py --verify

Push-Location attempts\wave212-rank3-common-neighbor-proof-b
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B `
  -m unittest -v test_exact_check.py
Pop-Location
```

The exact status is `DERIVED`; global Conway-99 status remains `UNKNOWN`.
