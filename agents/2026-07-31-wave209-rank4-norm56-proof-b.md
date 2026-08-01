# Wave 209 proof B: rank-four norm-56 point signatures

```yaml
role: proof_b
date_utc: 2026-08-01T03:10:56Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: >-
  Conditional rank-four M7g branch: global triangle/projector reduction,
  parity audit, complete labelled relabeling coverage, and exact 99-point
  joint-signature exclusions with positive controls for every survivor.
inputs: attempts/wave209-rank4-norm56-proof-b/input-freeze.sha256
method: >-
  Integral incidence algebra; zero-eigenspace projector interpolation;
  mod-two odd-support equations; exact S4xS4 label-map enumeration; complete
  {-1,0,+1}^8 point-signature moment systems; integer Farkas certificates;
  and solver-independent replay of all exclusion and feasibility artifacts.
command: >-
  .\.venv\Scripts\python.exe -B
  attempts\wave209-rank4-norm56-proof-b\exact_check.py --verify ;
  .\.venv\Scripts\python.exe -B -m unittest -v
  attempts\wave209-rank4-norm56-proof-b\test_exact_check.py
outputs: attempts/wave209-rank4-norm56-proof-b/package-manifest.sha256
limitations:
  - Discovery status is DERIVED pending source-blind verification.
  - Fifty-one labelled branches survive the point-signature census.
  - Surviving integer censuses are not graph completions or eigenvectors.
  - Conway-99 remains UNKNOWN.
```

## Exact result

For `t=B^Tq` and triangle intersection adjacency `C=B^TB-3I`, the sealed
norm-56 branch gives

```text
Ct=0,  t.t=168,  t_S=-3alpha,
sum(t outside S)=0,  ||t outside S||^2=96.
```

The zero-eigenspace projector is `P0=(J-F)/21`.  On every surviving rank-four
form, the marked interpolation minimum is exactly 168, so the norm condition
is sharp and `t` is the unique real projector interpolant.

Parity rules out the suggested division by two immediately:

```text
p=q mod 2 lies in ker_F2(A),
U^Tp=1_8,
s=B^Tp=t mod 2 lies in ker_F2(C),
s_S=1_8.
```

Thus `q` is not even and no norm-14 classification applies.

The stronger pointwise formula is

```text
q_x=(1/3) sum_i alpha_i s_i(x),
```

where `s_i=-1` on `T_i`, `+1` at an outside point adjacent to its unique
`T_i` point, and zero otherwise.  Exact single and pair tables reduce the
249 labelled branches, first proved to form 24 constraint-relabeling orbits,
to:

```text
17 orbits / 198 labelled branches: exact Farkas exclusion,
 7 orbits /  51 labelled branches: exact integer census control.
```

Each Farkas certificate is checked on all 2,187 divisible signatures with
`A^Ty>=0` and `b^Ty<0`.  Each positive control is checked against all 279
point-signature equations and transported to every labelled branch.  No
solver exit code is a certificate.

## Boundary

The seven surviving orbit representatives have selected-intersection
profiles `m=1,1,3,4,5,5,7`; together they cover 51 labelled branches.  Their
99-row controls do not name graph points, encode adjacency between rows,
couple to the 223 residual triangle types, or satisfy all rows of
`Aq=-4q`.  The next layer is that point/triangle/adjacency coupling.  The
global status remains `UNKNOWN`.
