# Wave 206 proof A: failed and bounded routes

## `tau` as a function of adjacency type

The initial hope was that the relation of `z` to the fixed root `y`, together
with the forced root-star block placement, would determine
`tau_(xy;z)`.  Exact marginal module enumeration refutes that hope at the
pair-local level: every tested edge and nonedge placement realizes all three
field values against each of the four sealed fixed-pair controls.

This does not impose the `x,z` pair module and therefore does not decide
whether the full labelled graph type of `x,y,z` determines `tau`.  Nor does
it show that all three values occur in an actual endpoint graph.  It shows
only that a proof must use the third pair and/or simultaneous shared-column
constraints beyond the root relation and one module at a time.

## Scalar contraction as a direct `h` filter

The contraction

```text
sum_(z not in {x,y}) tau_(xy;z)=-h_xy-g_xy
```

was tested against the exact root-relative placement multiplicities.
Marginal 97-entry ledgers meet it for every surviving `t=6,7` control.  These
ledgers omit every prescribed `x,z` pair module, a common operator sum, and a
common 231-column realization, so they are obstruction controls rather than
graph certificates.

## Rank 21 plus zero row sums

Formal self-adjoint-operator controls satisfy all rank, symmetry, diagonal,
root-row, and row-sum conditions while preserving every tested value of `h`.
The one residual operator in each control is not graph-derived.  Hence these
linear-algebraic conditions by themselves cannot close the argument.

## Simultaneous grouped operator selection

An exploratory Z3 model attempted to select representative modules for the
seven edge-block groups and 21 nonedge-fiber groups so that their exact
operator sum vanished.  The run was stopped after approximately 400 seconds
without a result.  It was not a complete search, produced no certificate,
and is not evidence for feasibility or infeasibility.  No solver output is
included in the package.

## Gram-kernel shortcut

No Gram-kernel word was treated as a relation among the underlying columns.
The route was excluded by protocol unless a separate vector or
nondegeneracy argument supplies the missing implication.

## Remaining route

The next useful target is a four-center or shared-column law coupling the
four operators in each labelled nonneighbor fiber.  The 21-coordinate model
shows the exact interface: each fiber has one marked coordinate, but all
centers can contribute to that coordinate, so an owner-bit equation does not
follow from the global coordinate sum without additional structure.
