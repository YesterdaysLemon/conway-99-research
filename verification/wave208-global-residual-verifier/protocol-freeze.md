# Wave 208 source-blind verifier protocol freeze

## Role and source barrier

This verifier freezes its obligations before opening either discovery lane:

```text
attempts/wave208-integer-lift-proof-a/
attempts/wave208-marked-m7g-proof-b/
```

The freeze uses only the overall Wave 208 protocol, the target statement,
and already-verified Wave 207 inputs.  Discovery code may not be imported by
the independent checker after the barrier is lifted.

## Frozen inputs

```text
3f3def2dd84610fd352d257b0b7d5b014f160901f63e6c2b91038e4734053740  attempts/wave208-global-residual-rigidity/protocol.md
7b4e67a28dbae58dffbf8f06a5fcb0241b12c34807dcb145ef2ff5c70d4c1c58  CONJECTURE.md
4c320426a735774b36dd806cf77d6df97a98bf4e38d4c3e2b856424445a0a4de  verification/2026-07-31-wave207-integration-audit.md
63aa632350e7191075203de6a7568ca0a3e387925d99f824a073eed12db00023  verification/wave207-incidence-tensor-rigidity/package-manifest.sha256
```

Frozen git commit:

```text
c58fd917ea8f9622e1388f10b0e0e3c709ba4854
```

## Independently derived lane-A obligations

For a ternary point-code word represented by `x in {0,1,-1}^99`, put

```text
w=wt(x),
P={x=1}, N={x=-1},
p=|P|, n=|N|,
p-n=3t,
z=Ax/3 in Z^99.
```

From

```text
A^2=12I-A+2J,
A1=14*1,
```

the verifier must reconstruct:

```text
Az=4x-z+2t*1,                                    (A1)
sum(z)=14t,                                       (A2)
3||z||^2=4w-x.z+6t^2.                            (A3)
```

The spectrum is `14^1,3^54,(-4)^44`.  If `u_3,u_-4` are the squared norms
of the two nonconstant spectral projections of `x`, then

```text
u_3   =(3x.z+4w-18t^2/11)/7 >=0,                 (A4)
u_-4  =(3w-3x.z+t^2)/7 >=0.                      (A5)
```

Every neighborhood induces `7K2`.  Coordinatewise,

```text
3z_v=sum_(u~v)x_u,
z_v in {-4,-3,...,4}.                             (A6)
```

The baseline must retain every arithmetically possible sign composition for
weights 17, 20, and 23.  The only imported composition exclusion is the
verified Wave 207 statement that weight 14 must be `7+7`.

## Independently derived lane-B obligations

For a marked selected-union `U` with outside set `O`, write

```text
A=[A_U  M^T]
  [ M   A_O].
```

Since the selected-incidence word `b` is zero off `U`, full `Ab=0` means

```text
A_U b_U=0,                                        (B1)
M b_U=0.                                          (B2)
```

The 23-vertex control checks only (B1).  It supplies no row of (B2).
Moreover the SRG square identity forces

```text
M^T M=12I_U-A_U+2J_U-A_U^2.                      (B3)
```

Every candidate `M` must be binary, have 76 rows when `|U|=23`, meet the
inside/outside degree equations, and extend to an `A_O` satisfying all
remaining blocks of the SRG identity.  A rational or category-sum solution
is not a graph.

Product one remains deliberately ambiguous.  The verifier will retain both:

1. two triangles meeting in one vertex; and
2. two disjoint triangles with exactly one cross edge.

Both have centered product one.  A lane that silently equates product one
with intersection fails.

The relation `a=B^Tc` is global: all 223 unselected triangle sums must be
zero and the eight selected sums must equal their marked signs.  A local
point vector or an `M^TM` aggregate does not establish this row-space
membership.

## Hostile test matrix

The independent suite will reject:

1. deletion of an arithmetically possible sign composition at weights
   17, 20, or 23;
2. identification of every product-one pair with an intersection;
3. promotion of `A_Ub_U=0` to `Ab=0` without all outside rows `Mb_U=0`;
4. promotion of a scalar, rational, moment, or category aggregate to a
   binary graphical completion;
5. setting unknown enumerator coefficients to zero;
6. treating a restricted scout non-hit or solver status as nonexistence;
7. any status stronger than `UNKNOWN` without a complete target graph or a
   complete independently checked nonexistence certificate.

## Promotion gate

The verifier may promote a scoped identity only if it is independently
reconstructed and its source manifest is sealed.  It will veto any endpoint
or global claim that omits a surviving composition, a product-one branch,
outside coordinates, binary graphical realization, or full-incidence
membership.

Initial status remains:

```text
Conway-99:                    UNKNOWN
rank-11 prism-free endpoint:  UNKNOWN
rigorous n3 interval:         708<=n3<=4158
conditional Q bound:          Q>=7059
```

