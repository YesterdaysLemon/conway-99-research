# Wave 207 mixed four-center proof B

This `DERIVED` package analyzes the simultaneous sandwich map

```text
A |-> (P_y A P_y restricted to E_y)_y
```

and the mixed tensor

```text
M[(y,x),(v,z)]=tr((P_yP_xP_y)(P_vP_zP_v)).
```

The main exact conclusions are:

- Gram nullity exceeds true synthesis-kernel nullity by exactly the radical
  dimension of the relevant sandwich-feature span.
- The full cross-center `21 by 21` transition has rank
  `binom(rank(C_yv)+1,2)`.
- Four middle centers are the first possible full ambient certificate;
  after a full-span pair, the remaining test is a rank-25 linear system on
  one `5 by 5` cross matrix.
- Any true `A_Delta` projector relation is annihilated functorially by all
  linear sandwiches and mixed trace pairings, so this route cannot classify
  or exclude it without nonlinear or graph-typed data.

The package does not establish the rank-66 or rank-25 certificate for the
endpoint.  Rank 11, `n3=4158`, and Conway-99 remain `UNKNOWN`.

## Replay

```powershell
.\.venv\Scripts\python.exe -B `
  attempts\wave207-mixed-four-center-proof-b\exact_check.py `
  --verify attempts\wave207-mixed-four-center-proof-b\exact-results.json

.\.venv\Scripts\python.exe -B -m unittest discover `
  -s attempts\wave207-mixed-four-center-proof-b `
  -p "test_*.py" -v
```

The exact checker uses only deterministic `F_3` row reduction, a symbolic
symmetric-square transition calculation, and Rabin identities for one
displayed degree-five polynomial.  It performs no graph or configuration
search.
