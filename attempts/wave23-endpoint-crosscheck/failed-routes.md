# Endpoint route ledger

## Trace alone

At `n3=705`, `B` has rank 44 and trace 48.  Ordinary AM--GM gives only

```text
det(B) <= floor((12/11)^44) = 45.
```

This leaves the determinant/index pair
`(h,det(Q),det(B))=(9,5,45)`.  Trace alone does not exclude the endpoint.

## Cauchy without the modulo-eight trace-square congruence

Cauchy gives `tr(B^2)>=576/11`.  Integrality and the Newton parity alone can
permit the next even value 54.  At 54, the `k=2` Maclaurin bound still has
integer cap 45, so `(9,5,45)` survives.  The congruence
`tr(B^2)=4 mod 8`, derived from `B=I+2C`, is essential; it raises the first
possible value to 60.

## Determinant/index factorization without the scaled-dual obstruction

The improved determinant cap 42, `det(Q)>=5`, 3,7-smoothness, and the
modulo-four residues leave only `h=1`.  If one stops there, ten formal pairs
`(1,det(Q),det(Q))` with `det(Q)=5,9,...,41` survive.

The missing bridge is that `S=21G^{-1}` is itself even integral positive
definite with determinant `h`.  At `h=1` it would be an even unimodular
positive-definite lattice of rank 44, forbidden by the signature theorem.

## Omitting the even determinant congruence for Q

If `det(Q)=3` is incorrectly admitted, the formal pair
`(h,det(Q),det(B))=(9,3,27)` survives the new cap.  Rank 44 forces every odd
determinant of the even Gram matrix `Q` to be `1 mod 4`; together with the
signature obstruction this gives `det(Q)>=5`.

## Omitting index smoothness

If the audited fact `h | 21^44` is dropped, the spurious pair `(5,5,25)`
survives.  The 3,7-smooth index restriction is therefore active.

## Modular ranks at odd primes

The frozen premises give `B=I mod 2L`, `rank_F2(B)=44`, and
`rank_F2(A4)=rank_F2(M)=44`.  They do not supply an endpoint contradiction
from ranks modulo 3, 5, or 7.  No such rank claim is promoted.  The binary
congruence is used through the trace-square residue and odd determinant.

## Boundary

The combined exact route excludes `n3=705`, but it does not construct or
exclude `srg(99,14,1,2)`.  Target status remains `UNKNOWN`, and novelty has
not been assessed.
