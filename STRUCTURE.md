# Checked structural baseline

This file collects consequences of the frozen target. `DERIVED` means the
argument is reproduced in this project; it does not imply novelty.

## Global counts (`DERIVED`)

Any Conway 99-graph has:

- spectrum `14^1, 3^54, (-4)^44`;
- 693 edges;
- 231 triangles, with the edges partitioned among them;
- seven triangles through every vertex;
- 4,158 nonedges;
- 2,079 four-cycles; and
- 84 four-cycles through every vertex.

The clique number is exactly three: triangles exist, while a `K_4` would put
each of its edges in two triangles. Hoffman's ratio bound gives independence
number at most 22 and therefore chromatic number at least five.

The complement would be `srg(99,84,71,72)`. The Laplacian spectrum is
`0^1, 11^54, 18^44`, so the matrix-tree theorem forces

```text
spanning_trees = 11^54 * 18^44 / 99.
```

## Rooted counts (`DERIVED`)

For a root `x`, write `N1=N(x)` and `N2=V-(N1 union {x})`. The induced graph
on `N1` is `7 K_2`, and `N2` is the 12-regular 84-vertex residual graph from
[CONJECTURE.md](CONJECTURE.md). It has:

- 504 internal edges;
- 84 triangles with one vertex in `N1` and two in `N2`;
- 140 triangles entirely inside `N2`; and
- five fully residual triangles through each residual vertex.

For residual labels `p,q`, let `t=|p intersection q|`, which is 0 or 1. Their
required number of common residual neighbors is:

| label relation | residual edge? | common residual neighbors |
|---|---:|---:|
| `t=1` | yes | 0 |
| `t=1` | no | 1 |
| `t=0` | yes | 1 |
| `t=0` | no | 2 |

## Triangle-intersection graph (`DERIVED`, literature-aligned)

Create a graph `T` whose 231 vertices are the triangles of the putative graph,
joining two when they share a vertex. If `N` is the 99-by-231 vertex-triangle
incidence matrix, then

```text
N N^T = A + 7 I,
N^T N = 3 I + adjacency(T).
```

It follows that `T` is 18-regular with forced spectrum

```text
18^1, 7^54, 0^44, (-3)^132.
```

This viewpoint agrees with Petro and Phillips' clique-graph treatment. It is
another exact formulation, not currently a construction.

## Automorphism restrictions (`CITED`, not independently recomputed)

The strongest combined published restrictions in the current audit imply

```text
Aut(G) is one of: trivial, C2, C3.
```

An order-three action would be fixed-point-free. This summary combines results
of Wilbrink, Behbahani--Lam, Crnkovic--Maksimovic, and Cesarz--Woldar; see
[SOURCES.bib](SOURCES.bib) and the dated literature report under `agents/`.

The full project never assumes one of these groups. The automorphism group of
the rooted *uncompleted scaffold* is `C2 wreath S7`; using it to select one
representative from equivalent rooted labelings is safe. Requiring any of it
to survive as an automorphism of the completed graph is not safe.

## Exact residual pair table (`DERIVED`)

The 84 residual labels have 924 intersecting unordered pairs and 2,562
disjoint unordered pairs. The block equations force this complete table:

| labels | residual edge? | common residual neighbors | pair count |
|---|---:|---:|---:|
| intersect | yes | 0 | 84 |
| intersect | no | 1 | 840 |
| disjoint | yes | 1 | 420 |
| disjoint | no | 2 | 2,142 |

Thus each residual vertex has two intersecting-label neighbors, ten
disjoint-label neighbors, 20 intersecting-label nonneighbors, and 51
disjoint-label nonneighbors.

The 84 intersecting-label edges form a 2-regular graph with no triangles. The
420 disjoint-label edges split among 140 edge-disjoint residual triangles. For
every residual vertex `u`, its induced neighborhood is

```text
5 K_2 disjoint-union 2 K_1.
```

The two isolated neighbors are precisely its intersecting-label neighbors.

There are 1,071 four-cycles wholly inside the residual graph, and every
residual vertex lies in 51 of them. This follows because only the 2,142
disjoint-label nonedges have two residual common neighbors; each residual
four-cycle is counted by its two diagonals.

## Seven forced multiple-of-four cycle systems (`DERIVED`)

For a root-neighbor coordinate `a`, let `F_a` be the 12 residual labels that
contain it. For each of the seven matched coordinate pairs `a,mate(a)`, the
partition

```text
F_a, F_mate(a), remaining labels
```

is equitable with quotient matrix

```text
[1 1 10]
[1 1 10]
[2 2  8].
```

Both fiber-induced graphs and the bipartite graph between the two fibers are
perfect matchings. The induced graph on their 24 vertices is a 2-factor. Its
cycles alternate same-side and cross edges, and a closed cycle uses an even
number of cross edges. Every component length is therefore divisible by four.

The possible cycle-length multisets are exactly the 11 partitions of 24 into
multiples of four. This is a pruning condition with no completed-graph symmetry
assumption. Its novelty in the literature has not been established.

These 11 multisets are only coarse cycle types. They are not 11 orbits of the
full 24-vertex configuration under the scaffold stabilizer, so fixing one
24-vertex representative per multiset would be an unsafe symmetry reduction.
The separate 11-branch split in `attempts/2026-07-22-eleven-branch-cover.md`
fixes a matching inside one 12-vertex fiber and is not this rejected shortcut.

## Residual spectrum (`DERIVED`)

Let `B` be the residual adjacency matrix and `C` the fixed endpoint-incidence
matrix. Since

```text
C C^T = 11 I + J - M,
```

`B` acts on `im(C^T)` with eigenvalues `12^1, (-2)^6, 0^7`. On `ker(C)`, the
block equation gives `B^2+B-12I=0`. Dimension and trace then force

```text
spectrum(B) = 12^1, 3^40, 0^7, (-2)^6, (-4)^30.
```

In particular, a putative residual graph is connected.
