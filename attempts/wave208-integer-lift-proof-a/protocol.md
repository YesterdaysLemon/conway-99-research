# Wave 208 proof A: integer-lift and short-eigenvector protocol

## Frozen scope

Work conditionally under a hypothetical simple
`srg(99,14,1,2)` with adjacency matrix `A`.  Let a nonzero ternary
adjacency-kernel word be represented by

```text
x in {0,1,-1}^99,
P={x=1}, N={x=-1}, p=|P|, n=|N|,
p-n=3t,
z=Ax/3 in Z^99.
```

The imported Wave 207 endpoint bridge leaves point-image weights
`14,17,20,23`; weight 14 is necessarily balanced `7+7`.  The exact lift is

```text
Az=4x-z+2t*1.
```

## Assigned lane

1. Retain the individual vector `z`, not only category sums.
2. Split the lift into exact integral `3`- and `-4`-eigenvectors and retain
   all norm, residue, and graphical consequences.
3. Attack the balanced weight-14 branch first, including the imported
   complementary-Fano classification of a norm-14 integer `-4`
   eigenvector.
4. Record exact necessary shell data for weights `17,20,23` without
   declaring arithmetic rows realizable.
5. Use only bounded arithmetic/Fano checks.  Do not search for a 99-vertex
   graph and do not assume an automorphism.

## Status wall

Discovery claims are `DERIVED` or `CANDIDATE`.  A restricted partial graph
is a hostile control, not a completion.  Weight 14 is excluded only if every
spectral branch is removed; the global target remains `UNKNOWN` absent an
independent complete proof or graph certificate.

