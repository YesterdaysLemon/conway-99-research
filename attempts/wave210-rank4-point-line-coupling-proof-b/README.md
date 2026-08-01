# Wave 210 rank-four point--line coupling

This proof-B package derives an exact conditional exclusion of the seven
Wave 209 rank-four survivor orbits (51 labelled branches).  It couples each
99-point signature row to exact three-point residual-triangle decompositions,
then archives an integer Farkas certificate for every orbit.

The default replay uses only the Python standard library:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave210-rank4-point-line-coupling-proof-b\coupling_check.py --verify
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave210-rank4-point-line-coupling-proof-b\test_coupling_check.py
```

`--generate` is a discovery helper requiring SciPy/HiGHS.  It rewrites the
candidate certificate and coarse-control archives, but each output is then
subjected to the same exact integer replay.  Solver status is not evidence.

Key files:

* `derivation.md`: necessity and Farkas derivation;
* `coupling-certificates.json`: seven sparse integer duals;
* `coarse-q-type-controls.json`: positive controls for the failed 35-type
  scalar relaxation;
* `exact-results.json`: machine-readable result summary;
* `failed-routes.md`: unsuccessful relaxations and scope walls;
* `input-freeze.sha256`: frozen upstream inputs; and
* `package-manifest.sha256`: sealed output hashes.

Status is `DERIVED`, pending an independent verifier.  The result is
conditional on the frozen endpoint and Wave 208/209 rank-four reduction.  It
does not address the rank-three branch, and Conway-99 remains `UNKNOWN`.
