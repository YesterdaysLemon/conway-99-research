# Wave 207 kernel-endpoint proof C

This package proves one exact parameter-only refinement: any weight-fourteen
word in the ternary adjacency kernel of a hypothetical `srg(99,14,1,2)` must
have seven `+1` and seven `-1` coordinates.  Two pointwise Farkas
certificates exclude the four unbalanced compositions.

It does **not** exclude weight fourteen.  The balanced branch and endpoint
weights `17`, `20`, and `23` remain `UNKNOWN`.

Replay with

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v `
  attempts\wave207-kernel-endpoint-proof-c\test_exact_check.py
.\.venv\Scripts\python.exe -B `
  attempts\wave207-kernel-endpoint-proof-c\exact_check.py `
  --verify attempts\wave207-kernel-endpoint-proof-c\exact-results.json
```

The balanced JSON control is not a graph and not a codeword.  Its declared
nongraphical degree sequence is a hostile boundary check, not existence
evidence.

