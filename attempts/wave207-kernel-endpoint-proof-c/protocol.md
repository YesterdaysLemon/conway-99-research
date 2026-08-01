# Wave 207 kernel-endpoint proof C protocol

## Frozen assumptions

Assume a hypothetical strongly regular graph `X` with

```text
(v,k,lambda,mu)=(99,14,1,2),
A^2=12I-A+2J.
```

Work over `F_3`.  The only imported endpoint theorem is the frozen Wave 207
ternary-code bridge:

```text
a hypothetical weight-eight A_Delta word produces a nonzero
b in ker_F3(A) with wt(b) in {14,17,20,23}.
```

For an arbitrary nonzero `x in ker_F3(A)`, use representatives in
`{0,1,-1}` and write `P={x=1}`, `N={x=-1}`, `p=|P|`, `n=|N|`,
`w=p+n`, and `p-n=3t`.  Put

```text
z=Ax/3 in Z^99.
```

This is integral because `Ax=0 mod 3`.

## Permitted methods

- exact integer consequences of the SRG adjacency identity;
- signed support and common-neighbor moments;
- the pointwise lift `Az=4x-z+2t*1`;
- equitable/quotient and local `7K_2` arithmetic;
- exact rational linear-programming certificates used only to discover or
  verify aggregate consequences;
- MacWilliams/Pless identities when all required code inputs are proved.

## Excluded methods and status discipline

- no search for a 99-vertex graph, SAT/MILP graph construction, or assumed
  automorphism;
- no inference from aggregate feasibility to existence of a graph or codeword;
- no claim that `d(ker_F3 A)>=24` unless every composition at weights
  `14,17,20,23` is rigorously excluded;
- no promotion of an endpoint exclusion to a global Conway-99 result without
  the independently frozen upstream implications;
- failed inequalities and feasible aggregate controls are retained.

## Target

Symbolically exclude all four endpoint weights.  If that fails, freeze the
strongest exact reduction, list every surviving composition, and leave the
endpoint and global target `UNKNOWN`.

