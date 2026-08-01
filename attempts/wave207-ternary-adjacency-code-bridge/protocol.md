# Wave 207 ternary adjacency-code bridge protocol

## Frozen scope

Assume a hypothetical strongly regular graph with parameters

```text
(v,k,lambda,mu)=(99,14,1,2)
```

and work over `F_3`.  Let `A` be its adjacency matrix, let `B` be the
`99 x 231` point--triangle incidence matrix, and let

```text
G=BB^T=A+I,
E=A+I-J.
```

The discovery question is whether parameter identities alone prove

```text
d(ker_F3 A)>=24.
```

The endpoint-specific input is a hypothetical weight-eight word

```text
a in A_Delta subset im(B^T)
```

with four coefficients `1` and four coefficients `2`.  For `a=B^T c`, put
`b=Ba`.  The package must audit the bridge from `a` to `b`, including the
possibility `b=0`, before using any minimum-distance statement.

## Permitted methods

- exact adjacency-algebra identities;
- signed neighbor counts and exact first/second common-neighbor moments;
- pointwise inequalities with an exact rational Farkas certificate;
- a small aggregate hostile control, provided it is explicitly labelled as
  neither a graph nor a codeword.

## Excluded methods

- no search for a 99-vertex graph;
- no SAT, MILP, or isomorph rejection as evidence;
- no assumed automorphism;
- no promotion from aggregate moment feasibility to graph or codeword
  existence;
- no promotion of a conditional endpoint contradiction to a global result.

## Claims submitted for verification

1. If `a=B^T c` has weight eight and composition `4+4`, then `b=Ba` is a
   nonzero word in `ker_F3 A`, satisfies `b.b=2`, and has

   ```text
   wt(b) in {2,5,8,11,14,17,20,23}.
   ```

2. Every nonzero word in `ker_F3 A` has weight at least twelve, using only
   the SRG parameters and signed neighbor equations.

3. Consequently the endpoint bridge narrows the image weight to

   ```text
   wt(b) in {14,17,20,23}.
   ```

4. The submitted weight-fourteen aggregate control satisfies all recorded
   first/second moment and local `7K_2` matching-sum equations, but its support
   degree sequence is deliberately nongraphical.  It is a boundary witness
   for this proof method, not a graph and not a codeword.

## Status wall

The reverse inequality `d(ker_F3 A)>=24`, an equality classification, the
exclusion of the four surviving image weights, the rank-eleven endpoint, and
the global Conway-99 problem all remain `UNKNOWN` unless independently proved.
