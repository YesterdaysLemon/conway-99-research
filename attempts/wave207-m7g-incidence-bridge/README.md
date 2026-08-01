# Wave 207 M7g incidence bridge

This package derives an exact signed-intersection obstruction from
`a in im(B^T)`, excludes four of the 27 polar restrictions on a hypothetical
weight-eight `M_7g` support, and archives one restricted 23-vertex rank-four
local compatibility certificate.

Run:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave207-m7g-incidence-bridge\exact_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave207-m7g-incidence-bridge\test_exact_check.py
```

`scout.py` is a restricted discovery aid.  It assumes every selected
intersection is pair-specific and therefore does not enumerate triple
memberships.  A returned model is independently checked; a non-hit is not a
nonexistence result.

The archived certificate is not a 99-vertex graph, a 231-column frame, or a
counterexample.  Endpoint and Conway-99 status remain `UNKNOWN`.

