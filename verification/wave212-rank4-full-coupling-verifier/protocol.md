# Wave 212 rank-four full-coupling verifier protocol

## Frozen claim

Conditionally on the frozen endpoint and the independently verified Wave208
and Wave209 rank-four reductions, exclude all seven surviving rank-four
constraint orbits and all 51 labelled branches by exact necessary point-line
coupling equations.  Do not promote rank three or the global Conway-99 target.

## Blind phase

Before opening a Wave210 rank-four artifact:

1. reconstruct the three M7g polar forms, 249 marked branches, and 24 exact
   constraint-relabeling orbits from the sealed Wave209 inputs;
2. recover survivor orbit ids `0,2,4,11,12,14,23`;
3. enumerate all 2,187 integral point signatures, every residual triangle
   type, and every coordinatewise unordered three-signature decomposition;
4. build the larger `99+279+2*2187=4752` row systems with all W and X columns;
5. canonical-hash every complete system and replay an exact integer Farkas
   vector on every column; and
6. seal the code, results, and dual archive.

The exact clean-room boundary and one dimension-only orchestrator contact are
recorded in `source-contact-log.md`.  No Wave210 implementation, matrix,
coefficient, mapping, or certificate entry was inspected before the seal.

## Post-seal source audit

After checking the blind seal:

1. verify the Wave210 outer manifest and all 12 entries;
2. independently impose the geometric membership filter
   `M(s)=empty`, `M(s)={i}`, or `M(s)={i,j}` for an edge of `H`;
3. group the negative coordinates of each residual triangle by the forced
   matching `H[h]`, then enumerate every exact unordered local triple;
4. normalize every source row, right-hand side, W column, and X column into a
   semantic canonical ordering and demand complete equality with the
   independent reconstruction;
5. prove mechanically that each filtered system zero-extends into the larger
   blind relaxation;
6. replay every archived integer dual with orientation
   `A^T y >= 0`, `b^T y < 0`;
7. prove the full column bijection and row-feature covariance under checked
   sign-preserving data relabellings, and transport the duals over all 51
   labelled branches; and
8. reject erased/reversed coefficients and hostile RHS, column, and mapping
   mutations.

The data relabellings are isomorphisms of finite constraint systems, not
assumed automorphisms of a hypothetical target graph.  Solver statuses are
never certificates.

## Commands

From the repository root, using the repository environment:

```powershell
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B verification\wave212-rank4-full-coupling-verifier\independent_verify.py --verify-blind
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B verification\wave212-rank4-full-coupling-verifier\independent_verify.py --verify-duals
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B verification\wave212-rank4-full-coupling-verifier\post_source_audit.py --verify
& 'C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe' -B -m unittest -v verification\wave212-rank4-full-coupling-verifier\test_post_source_audit.py
```

## Status wall

Only the conditional rank-four exclusion is eligible for `VERIFIED`.  The
rank-three branch and Conway-99 remain `UNKNOWN`.
