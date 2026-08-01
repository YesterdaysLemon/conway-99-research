# Wave 208: M7g norm divisibility

This package derives and exactly replays a conditional mod-nine obstruction
on the 27 labelled polar forms associated with a hypothetical M7g
weight-eight word.  It retains all four relative column orientations and
does not quotient scalar-multiple forms.

Run:

```powershell
.venv\Scripts\python.exe attempts\wave208-m7g-norm-divisibility\exact_check.py --verify
.venv\Scripts\python.exe -m unittest attempts\wave208-m7g-norm-divisibility\test_exact_check.py -v
```

Discovery verdict: `DERIVED`.  The calculation excludes 23 forms per
orientation and leaves four.  Global status: `UNKNOWN`.

