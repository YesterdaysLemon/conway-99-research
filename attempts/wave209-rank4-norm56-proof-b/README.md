# Wave 209: rank-four norm-56 proof-B lane

This package gives a conditional exact reduction, not an exclusion.  For each
of the three surviving rank-four M7g polar forms, it converts the norm-56
integer `-4` eigenvector into a 231-coordinate triangle-sum vector in the zero
eigenspace of the triangle intersection graph.  It proves projector
saturation, rules out division by two, and imposes the complete 99-point
joint signature census.  Exact integer Farkas certificates exclude 198 of
the 249 labelled branches; seven relabeling orbits containing 51 labelled
branches retain explicit integer census controls.

Run the sealed replay with:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave209-rank4-norm56-proof-b\exact_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave209-rank4-norm56-proof-b\test_exact_check.py
```

`point-signature-controls.json` contains the exact Farkas certificates and
surviving integer controls.  `aggregate-controls.json` records the coarser
triangle-side controls.  Both are checked without trusting solver status.
Neither artifact specifies a graph completion.
