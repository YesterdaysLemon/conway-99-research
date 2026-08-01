# Failed routes and scope boundaries

## Ambient support nondegeneracy is unnecessary

The support span of the `z_i` may be degenerate for the ambient 11-space
form.  The proof does not restrict that form.  It first multiplies the
operator equation by the inverse ambient form and obtains the ordinary
tensor equation `V Lambda V^T=0`.  A left inverse for a basis matrix of
the support span then gives the coefficient-space equation.

Any proof applying a Witt index directly to the ambient support span would
need an unjustified nondegeneracy hypothesis.

## The relevant Witt form is the coefficient form

`Lambda=diag(a_i)` is nondegenerate because every coefficient on the
support is nonzero.  The row space of `V`, not the column span in the
ambient geometry, is totally isotropic in `F_3^k`.

Characteristic three causes no radical: the diagonal entries are one or
two, both invertible.

## Dual distance is used only after returning to original columns

Dual distance at least four does not directly lower-bound an arbitrary
relation among quadratic tensors.  Its valid use here is:

```text
any three original columns z_i are independent,
so the support projective points contain no collinear triple.
```

The tensor relation supplies the separate span-rank upper bound.

## A generic projective bound is insufficient without the small cap audit

Projective distinctness alone would allow all points of `PG(2,3)`.  The
no-three-collinear transfer is essential.  Exact exhaustion gives the
plane cap maximum four.

## Weight nine is not proved

An exact weight-eight control satisfies the tensor relation, no-three
dependence, singular-column condition, and nonsquare 11-space condition.
Thus those local ingredients cannot yield weight at least nine.

The control does not lie in a demonstrated `im(B^T)`, does not extend to
the 231-column frame, and has no target incidence or graph.  A stronger
bound might still follow from those missing global premises.

## Endpoint status is unchanged

The addendum strengthens only the conditional support bound for the
already-derived tensor-balance code.  It does not independently verify that
code's existence and proves no endpoint exclusion or Conway-99 result.
