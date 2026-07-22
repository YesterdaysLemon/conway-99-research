# Frozen target: Conway's 99-graph problem

## Canonical question

Does there exist a finite simple undirected strongly regular graph with
parameters

```text
(v, k, lambda, mu) = (99, 14, 1, 2)?
```

That is, does there exist a graph `G=(V,E)` satisfying all of the following?

1. `|V| = 99`.
2. Every vertex has degree 14.
3. Every adjacent pair has exactly one common neighbor.
4. Every nonadjacent pair has exactly two common neighbors.

All graphs in this project are finite, simple, undirected, and loopless unless
explicitly stated otherwise.

## Conway's formulation

Conway asked whether a 99-vertex graph exists in which every edge belongs to a
unique triangle and every nonedge belongs to a unique quadrilateral.

For a simple graph, the first condition says that adjacent vertices have one
common neighbor. For nonadjacent vertices `u,v`, every unordered pair of common
neighbors determines one 4-cycle through `u,v`; hence a unique quadrilateral
means exactly two common neighbors. Together with the feasible-parameter
relation, these are the `srg(99,14,1,2)` conditions. The project uses the
strongly regular formulation as the frozen target because it makes regularity
and cycle conventions explicit.

## Matrix certificate

Let `A` be a `99 x 99` matrix, `I` the identity, and `J` the all-ones matrix.
A positive certificate is a matrix satisfying

1. `A` is symmetric;
2. every entry is 0 or 1;
3. the diagonal is zero; and
4. `A^2 = 12 I - A + 2 J` over the integers.

The diagonal of the identity forces every row to contain 14 ones. Off-diagonal
entries then say that adjacent pairs have one common neighbor and nonadjacent
pairs have two. Thus this compact identity is both necessary and sufficient.

## Immediate spectral constraints

On the all-ones vector, `A` has eigenvalue 14. On its orthogonal complement,
the matrix identity becomes

```text
A^2 + A - 12 I = 0,
```

whose roots are 3 and -4. Trace and dimension give the forced spectrum

```text
14^1, 3^54, (-4)^44.
```

This is a necessary consistency check, but a matrix with this spectrum alone
is not a certificate for the target.

## Root-normalized 84-vertex formulation

Fix a vertex `x`.

- `N(x)` has 14 vertices.
- Each vertex of `N(x)` has exactly one neighbor within `N(x)`, so the induced
  graph is `7 K_2`.
- The remaining set `R` has 84 vertices.
- Each `z in R` has exactly two neighbors in `N(x)`, and those two neighbors
  are nonadjacent.
- Conversely, each nonedge of `7 K_2` labels exactly one vertex of `R`.

There are `binom(14,2)-7 = 84` such nonedges, so this correspondence is a
bijection. Each residual vertex has degree 12 inside `R`.

Let `M` be the adjacency matrix of the matching `7 K_2`, let `B` be the
`14 x 84` incidence matrix of the 84 nonedges, and let `X` be the unknown
adjacency matrix on `R`. Under the ordering `{x}, N(x), R`, the full matrix is

```text
    [ 0   1^T   0 ]
A = [ 1    M    B ]
    [ 0   B^T   X ].
```

The target becomes finding a symmetric binary zero-diagonal `X` satisfying

```text
X 1 = 12 1,
M B + B X = 2 J - B,
X^2 + B^T B = 12 I - X + 2 J.
```

These equations are over the integers. They are an exact reformulation, not a
relaxation.

## Resolution standard

A claimed construction must include a complete adjacency matrix or edge list
and pass at least two independent exact validators. A claimed nonexistence
proof must be a complete human proof, a checked formal proof, or a complete
machine proof whose encoding, proof artifact, and proof checker are all public
and reproducible. Solver timeouts, heuristic failures, floating-point
optimization, or searches with an unproved symmetry assumption do not resolve
the problem.
