# Wave 212 proof-A protocol: quadratic K-block algebra

## Frozen conditional input

For each Wave 210 survivor orbit `0`, `4`, and `29`, use its committed
`14 x 85` incidence matrix `F` and the Wave 211 decomposition

```text
U = im(F^T) + <1>,              dim(U)=14,
K = ker(F) intersect 1^perp,    dim(K)=71.
```

A completion would be a symmetric zero-diagonal binary matrix `D` satisfying

```text
F D       = 2J - (A_S+I)F,
D^2 + D   = 12I + 2J - F^T F.
```

The input is frozen by exact SHA-256 hashes.  No automorphism of a target
graph is assumed.

## Exact questions

1. Determine the complete Jordan type of `F^T F` over `F_2`, not just its
   rank, and transport it through the Artin--Schreier equation
   `D^2+D=F^T F`.
2. Reduce the conditional characteristic polynomial of `D` modulo two and
   test the parity form forced by a symmetric zero-diagonal matrix of odd
   order.
3. Reconstruct the exact orthogonal projector `P_U` and the forced operator
   `D P_U`, then compute the diagonal local multiplicities of the conditional
   `3` and `-4` projectors on `K`.
4. Test every off-diagonal binary choice against the two exact `2 x 2`
   positive-semidefinite projector minors.

## Status discipline

These are necessary consequences only.  A consistent result closes a
shortcut; it is not a construction.  Proof A labels its own work `DERIVED`,
does not promote it to `VERIFIED`, and preserves global status `UNKNOWN`.

