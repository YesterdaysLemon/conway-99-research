# Retained failed runs

## Hostile-route parameterization

The first invocation of `exact_check.py` stopped before producing a result:

```text
CheckError: e2 endpoint bound is not 1122
```

The endpoint-specific Maclaurin checker was being reused deliberately with
the hostile value `tr(B^2)=54`, which should produce `e2=1125` and the old
determinant cap 45.  The function was split into a general exact computation
plus an optional endpoint-value gate.  The endpoint path still requires
`e2=1122`, `e2/C(44,2)=51/43`, and cap 42; only the hostile relaxation calls
the ungated arithmetic path.  The corrected run and all 25 tests pass.

No solver, floating-point calculation, or candidate Wave-23 artifact was
used.
