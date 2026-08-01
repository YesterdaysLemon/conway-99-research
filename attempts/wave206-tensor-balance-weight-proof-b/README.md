# Wave 206 tensor-balance weight addendum

This separate Proof-B addendum proves, pending independent verification,
that every nonzero word in the Wave 206 tensor-balance intersection code

```text
A_Delta=im(B^T) intersect ker(a -> D diag(a)D)
```

has weight at least eight.

The proof combines:

- a coefficient-space Witt bound from `V diag(a)V^T=0`;
- the verified original-column dual distance at least four;
- exact cap maxima `1,2,4` in vector dimensions `1,2,3`; and
- a weight-eight exact control showing the audited local ingredients cannot
  prove weight at least nine.

Run:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave206-tensor-balance-weight-proof-b\exact_check.py --verify attempts\wave206-tensor-balance-weight-proof-b\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave206-tensor-balance-weight-proof-b\test_exact_check.py
```

The sealed crossing-kernel package is an immutable input and was not
modified.  Endpoint and Conway-99 status remain `UNKNOWN`.
