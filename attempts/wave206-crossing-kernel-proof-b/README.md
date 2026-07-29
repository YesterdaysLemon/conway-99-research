# Wave 206 Proof B: crossing kernel and compression coordinates

This sealed discovery package derives, over `F_3` on the conditional
prism-free rank-11 branch:

- the exact 21-coordinate realization of every fixed-middle compression
  `P_yP_xP_y` inside the supported entries of `Q o M_x`;
- the nondegenerate coordinate trace matrix
  `J_star=C^T C+2I_21`, with determinant two;
- the global identity `Gamma=sum_y Tau^(y)`, together with the crossing
  relations `W^TW=0` and `(WW^T)^2=0`;
- a forced nonzero, nonconstant diagonal tensor-relation code
  `A_Delta=im(B^T) intersect ker(a -> D diag(a)D)`; and
- the tensor-balanced partition `R_0=R_1=R_2` induced by a nonzero word of
  that code.

The checker also verifies the characteristic-three radical warning and a
99-projector hostile control in which every fixed-middle slice has rank 21
while the fourth-trace matrix has rank 96.

Run:

```powershell
.\.venv\Scripts\python.exe -B attempts\wave206-crossing-kernel-proof-b\exact_check.py --verify attempts\wave206-crossing-kernel-proof-b\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave206-crossing-kernel-proof-b\test_exact_check.py
```

Status remains `UNKNOWN`.  Independent verification is required before any
claim is promoted.
