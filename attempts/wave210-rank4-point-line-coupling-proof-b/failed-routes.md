# Failed routes and retained boundaries

## The 35 unordered triangle-`q` types

Collapsing every point signature to its scalar value `q in {-2,-1,0,1,2}`
gives 35 unordered three-point types.  Even after fixing the eight selected
triangle types from each sealed point control, forbidding residual `|t|>2`,
and imposing the exact incidence, residual sum, and residual squared-norm
rows, all seven orbits have explicit integer controls.  They are archived in
`coarse-q-type-controls.json` and replayed by the default checker.

This relaxation loses which selected triangle a point belongs to and which
residual triangle realizes each signature.  Its feasibility is not evidence
for a graph.

## Separate point and triangle censuses

Wave 209 already retained a 99-row point-signature census and a 223-row
residual-triangle type census for the surviving orbits.  Juxtaposing those
tables does not identify an occurrence of a point signature with an occurrence
inside a residual triangle.  The successful Wave 210 argument begins only
after adding the exact incidence rows (6) and incident-`t` demand rows (7) from
`derivation.md`.

## Pointwise interval bounds

For a selected-union point of membership `M`, the residual degree is
`7-|M|` and its residual triangle-sum demand is

```text
3q+3 sum_(i in M) alpha_i.
```

Every individual demand fits the crude interval allowed by
`t in {-2,-1,0,1,2}`.  Treating points separately therefore gives no
contradiction.  The obstruction is simultaneous grouping into exact
three-point `(d,h,t)` columns.

## Invalid omission of `h=empty` columns

An exploratory shortcut applied the full selected polar `d` margins only to
residual triangles with `h` nonempty.  That produces very small apparent
dual contradictions, but it is invalid: triangles disjoint from the selected
union still contribute to every `d` margin.  The shortcut was rejected.  The
sealed checker retains all locally realizable `h=empty` columns whenever a
certificate uses a row to which they contribute.

## Numerical dual rays

Raw HiGHS rays for the redundant full system can be dense and numerically
ill-conditioned.  Their statuses and floating coefficients were discarded.
The generation helper instead minimizes an L1 dual relaxation, rationalizes a
candidate, and keeps it only if the standard-library integer replay proves
`A^Ty>=0` on every column and `b^Ty<0`.  The archived integers, not solver
output, are the evidence.

## No 99-vertex search or construction

No adjacency matrix, residual--residual triangle intersection graph, or
99-vertex completion was enumerated.  The Farkas inequalities exclude a
necessary typed incidence relaxation and hence the conditional rank-four
branches, but they neither construct a counterexample nor address the
rank-three branch.  Conway-99 remains `UNKNOWN`.
