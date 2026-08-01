# Wave 209 rank-three signed-trade proof A

This package gives exact parameter, common-neighbor, marked-line, and
231-line reductions for both rank-three branches imported from Wave 208.
It does not prove nonexistence and does not construct an
`srg(99,14,1,2)`.

Run from the repository root:

```powershell
.venv\Scripts\python.exe -B attempts\wave209-rank3-trade-proof-a\exact_check.py --verify
.venv\Scripts\python.exe -B -m unittest -v attempts\wave209-rank3-trade-proof-a\test_exact_check.py
```

To emit the complete 430-row pre-structural aggregate catalog as JSON:

```powershell
.venv\Scripts\python.exe -B attempts\wave209-rank3-trade-proof-a\exact_check.py --emit-catalog
```

The support-14 endpoint is a strict conditional reduction to one rooted
support type, one outside signature, 204 labelled selected-intersection
graphs, and 4,480 cross-deficit bijections.  The support-20 endpoint retains
352 aggregate rows.  Global status: `UNKNOWN`.

