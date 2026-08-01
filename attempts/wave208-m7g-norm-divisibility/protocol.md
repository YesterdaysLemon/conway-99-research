# Wave 208 M7g norm-divisibility protocol

## Frozen scope

Work conditionally at the already sealed prism-free rank-11 endpoint for a
hypothetical `srg(99,14,1,2)`.  Assume a supported weight-eight word
`a in A_Delta` has the verified M7g support and four coefficients of each
nonzero sign.  Let `U` be the `99 x 8` integer point--triangle incidence
matrix on those eight triangles, and let `alpha in {+1,-1}^8` be the
ordinary integer lift of the ternary coefficient word.

The target is only the following necessary-condition question:

> Which of the 27 labelled M7g polar forms can be congruent modulo three to
> the exact selected-triangle matrix `R=U^T A U`?

No graph construction, automorphism, orbit quotient, or completion search is
allowed.  All 27 affine forms and all four relative column-orientation
classes must be retained.

## Frozen identities

For the adjacency matrix `A`,

```text
A^2 = 12 I - A + 2 J.
```

Put `K=U^T U`, `R=U^T A U`, and `H=A U`.  For distinct selected triangles:

* `K_ij=1` exactly when the triangles intersect and is otherwise zero;
* `R_ij=4` for an intersecting pair;
* `R_ij` is the number `q_ij in {0,1,2}` of cross edges for a disjoint pair,
  using the prism-free endpoint to exclude three cross edges.

Thus the residue `Q=R mod 3` has entries in `{0,1,2}`.  A residue-one pair
may be either disjoint with one cross edge or intersecting with exact entry
four.  That ambiguity must not be guessed.

The verified incidence-to-point-code bridge gives `A U alpha = 0 mod 3`.
Consequently every coordinate of the integer vector `H alpha` is divisible
by three, so its squared Euclidean norm is divisible by nine.

## Frozen gates

1. Reconstruct the published labelled M7g representative independently.
2. Recover all four relative sign classes for which the fixed quadratic
   relation is also a true linear relation.
3. Enumerate the entire three-dimensional polar net: 27 affine forms, not
   projective scalar classes.
4. Compute each exact residue representative `q_ij in {0,1,2}` and
   `d(Q)=sum_{i<j} alpha_i alpha_j q_ij`.
5. Derive the norm congruence without choosing which residue-one pairs are
   intersections.
6. Report every survivor, including its rank and zero graph.
7. Keep the global Conway-99 status `UNKNOWN`.  A surviving polar form is not
   a graph, and eliminating polar forms is not a nonexistence certificate.

## Claim labels

Discovery output is at most `DERIVED`.  Only the source-blind verifier may
promote the finite reconstruction or congruence replay to `VERIFIED`.

