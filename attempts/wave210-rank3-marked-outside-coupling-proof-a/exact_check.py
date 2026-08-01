#!/usr/bin/env python3
"""Exact labelled Wave 210 coupling census for the rank-three weight-14 branch.

The search never constructs a 99-vertex graph.  It enumerates the eight
selected line labels, ordered partitions of the fourteen signed support
points, and the exact support-neighbourhood multiset of the 85 zero points.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path


SIGNS = (1, 1, 1, 1, -1, -1, -1, -1)
POLAR = (
    (0, 2, 2, 2, 0, 1, 1, 1),
    (2, 0, 2, 2, 1, 0, 1, 1),
    (2, 2, 0, 2, 1, 1, 0, 1),
    (2, 2, 2, 0, 1, 1, 1, 0),
    (0, 1, 1, 1, 0, 2, 2, 2),
    (1, 0, 1, 1, 2, 0, 2, 2),
    (1, 1, 0, 1, 2, 2, 0, 2),
    (1, 1, 1, 0, 2, 2, 2, 0),
)
PRODUCT_ONE_EDGES = tuple(
    (i, j) for i in range(4) for j in range(4, 8) if POLAR[i][j] == 1
)
ROOTED_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
    (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
)


def graph(edges: tuple[tuple[int, int], ...], n: int) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(n)]
    for u, v in edges:
        rows[u].add(v)
        rows[v].add(u)
    return tuple(frozenset(row) for row in rows)


G7 = graph(ROOTED_EDGES, 7)
DEFICITS = tuple(
    (u, v)
    for u, v in combinations(range(7), 2)
    if (1 if v in G7[u] else 2) - len(G7[u] & G7[v]) == 1
)
EXTERNAL_THIRD = frozenset(
    edge for edge in ROOTED_EDGES if not (G7[edge[0]] & G7[edge[1]])
)


def support_edges() -> frozenset[tuple[int, int]]:
    edges = set(ROOTED_EDGES)
    edges.update((u + 7, v + 7) for u, v in ROOTED_EDGES)
    edges.add((0, 7))
    return frozenset(tuple(sorted(edge)) for edge in edges)


SUPPORT_EDGES = support_edges()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "exact-results.json"
CONTROLS = HERE / "hostile-controls.json"

INPUT_HASHES = {
    "AGENTS.md": "4d3e4590a8634cafaf5d87f288be211497f60a8f5ab40094a83f555724e469b3",
    "attempts/wave209-four-survivor-globalization/protocol.md":
        "3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196",
    "attempts/wave209-rank3-trade-proof-a/package-manifest.sha256":
        "521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1",
    "verification/wave209-four-survivor-verifier/package-manifest.sha256":
        "7e20ac726cc4823360e49d3fcf08e5c8ff6c7f219c5d1cbbba781d015fe59c91",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_inputs() -> dict[str, str]:
    observed = {name: sha256(ROOT / name) for name in INPUT_HASHES}
    assert observed == INPUT_HASHES
    return observed


def marked_graphs() -> tuple[tuple[tuple[int, int], ...], ...]:
    """All 204 labelled five-edge selected-intersection graphs."""
    allowed = {(3, 1, 1, 0), (2, 2, 1, 0)}
    out = []
    for chosen in combinations(PRODUCT_ONE_EDGES, 5):
        degree = [0] * 8
        for i, j in chosen:
            degree[i] += 1
            degree[j] += 1
        if tuple(sorted(degree[:4], reverse=True)) not in allowed:
            continue
        if tuple(sorted(degree[4:], reverse=True)) not in allowed:
            continue
        pi = degree[:4].index(0)
        ni = 4 + degree[4:].index(0)
        if (pi, ni) not in PRODUCT_ONE_EDGES:
            continue
        out.append(tuple(chosen))
    assert len(out) == 204
    return tuple(out)


@lru_cache(maxsize=None)
def ordered_packings(degrees: tuple[int, int, int, int]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Every ordered support-block packing for four labelled same-sign lines."""
    sizes = tuple(3 - d for d in degrees)
    out: list[tuple[tuple[int, ...], ...]] = []

    def rec(index: int, remaining: frozenset[int], blocks: list[tuple[int, ...]]) -> None:
        if index == 4:
            if not remaining:
                out.append(tuple(blocks))
            return
        size = sizes[index]
        for block in combinations(sorted(remaining), size):
            if size == 3 and any(tuple(sorted(edge)) not in SUPPORT_EDGES for edge in combinations(block, 2)):
                continue
            if size == 2 and tuple(sorted(block)) not in EXTERNAL_THIRD:
                continue
            rec(index + 1, remaining - frozenset(block), blocks + [tuple(block)])

    rec(0, frozenset(range(7)), [])
    return tuple(out)


def deficit_columns(matching: tuple[int, ...]) -> tuple[tuple[frozenset[int], ...], tuple[tuple[int, ...], ...]] | None:
    """Return seven t=2 columns and the exact 7x7 t=1 multiplicity matrix."""
    residual = [[2] * 7 for _ in range(7)]
    residual[0][0] = 1
    for v in G7[0]:
        residual[v][0] -= 1
        residual[0][v] -= 1
    columns = []
    for p_index, n_index in enumerate(matching):
        p_edge = DEFICITS[p_index]
        n_edge = DEFICITS[n_index]
        columns.append(frozenset((*p_edge, *(v + 7 for v in n_edge))))
        for p in p_edge:
            for n in n_edge:
                residual[p][n] -= 1
    if min(map(min, residual)) < 0:
        return None
    return tuple(columns), tuple(tuple(row) for row in residual)


def valid_deficit_matchings() -> tuple[tuple[int, ...], ...]:
    out = tuple(p for p in permutations(range(7)) if deficit_columns(p) is not None)
    assert len(out) == 4480
    return out


def line_sets(
    h: tuple[tuple[int, int], ...],
    p_blocks: tuple[tuple[int, ...], ...],
    n_blocks_local: tuple[tuple[int, ...], ...],
) -> tuple[tuple[frozenset[int], ...], tuple[frozenset[int], ...]]:
    """Return support blocks and incident marked-zero indices for all lines."""
    blocks = tuple(frozenset(b) for b in p_blocks) + tuple(
        frozenset(v + 7 for v in b) for b in n_blocks_local
    )
    incident = []
    for line in range(8):
        incident.append(frozenset(e for e, pair in enumerate(h) if line in pair))
    return blocks, tuple(incident)


Case = tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]


@lru_cache(maxsize=1)
def labelled_cases() -> tuple[Case, ...]:
    """Expand every labelled H through every ordered P/N block packing."""
    rows: list[Case] = []
    for h in marked_graphs():
        degree = [0] * 8
        for i, j in h:
            degree[i] += 1
            degree[j] += 1
        for p_blocks in ordered_packings(tuple(degree[:4])):
            for n_blocks in ordered_packings(tuple(degree[4:])):
                rows.append((h, p_blocks, n_blocks))
    assert len(rows) == 20_928
    assert len(set(rows)) == len(rows)
    return tuple(rows)


@lru_cache(maxsize=1)
def support_automorphisms() -> tuple[tuple[int, ...], ...]:
    """Complete automorphism group of the fixed rooted seven-point graph."""
    edge_set = set(ROOTED_EDGES)
    rows = []
    for tail in permutations(range(1, 7)):
        relabel = (0, *tail)
        image = {
            tuple(sorted((relabel[u], relabel[v]))) for u, v in ROOTED_EDGES
        }
        if image == edge_set:
            rows.append(relabel)
    assert len(rows) == 4
    return tuple(rows)


def transform_case(
    case: Case,
    line_permutation: tuple[int, ...],
    p_automorphism: tuple[int, ...],
    n_automorphism: tuple[int, ...],
    swap_signs: bool,
) -> Case:
    """Apply one proved symmetry of the polar matrix and support graph."""
    h, p_blocks, n_blocks = case
    blocks: list[tuple[int, ...] | None] = [None] * 8
    if not swap_signs:
        image_h = tuple(sorted(
            (line_permutation[i], 4 + line_permutation[j - 4]) for i, j in h
        ))
        for i in range(4):
            blocks[line_permutation[i]] = tuple(sorted(p_automorphism[v] for v in p_blocks[i]))
            blocks[4 + line_permutation[i]] = tuple(sorted(n_automorphism[v] for v in n_blocks[i]))
    else:
        image_h = tuple(sorted(
            (line_permutation[j - 4], 4 + line_permutation[i]) for i, j in h
        ))
        for i in range(4):
            blocks[line_permutation[i]] = tuple(sorted(p_automorphism[v] for v in n_blocks[i]))
            blocks[4 + line_permutation[i]] = tuple(sorted(n_automorphism[v] for v in p_blocks[i]))
    assert all(block is not None for block in blocks)
    return image_h, tuple(blocks[:4]), tuple(blocks[4:])  # type: ignore[arg-type]


@lru_cache(maxsize=1)
def case_orbits() -> tuple[tuple[Case, int], ...]:
    """Partition all 20,928 labelled cases, rather than assuming equivalence."""
    all_cases = set(labelled_cases())
    unseen = set(all_cases)
    rows: list[tuple[Case, int]] = []
    line_group = tuple(permutations(range(4)))
    support_group = support_automorphisms()
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_case(representative, line_perm, p_auto, n_auto, swap)
            for swap in (False, True)
            for line_perm in line_group
            for p_auto in support_group
            for n_auto in support_group
        }
        assert orbit <= all_cases
        unseen.difference_update(orbit)
        rows.append((representative, len(orbit)))
    assert len(rows) == 33
    assert sum(size for _, size in rows) == 20_928
    assert Counter(size for _, size in rows) == Counter({768: 22, 384: 10, 192: 1})
    return tuple(rows)


def encode_case(case: Case) -> dict[str, object]:
    h, p_blocks, n_blocks = case
    return {
        "H": [list(edge) for edge in h],
        "P_blocks": [list(block) for block in p_blocks],
        "N_blocks": [list(block) for block in n_blocks],
    }


@lru_cache(maxsize=1)
def symmetry_audit() -> dict[str, object]:
    """Prove the cache group preserves every frozen labelled structure."""
    line_maps = []
    for swap in (False, True):
        for perm in permutations(range(4)):
            mapping = tuple(
                (4 + perm[i] if swap else perm[i]) for i in range(4)
            ) + tuple(
                (perm[i] if swap else 4 + perm[i]) for i in range(4)
            )
            assert all(
                POLAR[i][j] == POLAR[mapping[i]][mapping[j]]
                for i in range(8) for j in range(8)
            )
            line_maps.append(mapping)
    assert len(set(line_maps)) == 48

    edge_index = {edge: index for index, edge in enumerate(DEFICITS)}
    deficit_permutations = []
    for auto in support_automorphisms():
        image = tuple(
            edge_index[tuple(sorted((auto[u], auto[v])))] for u, v in DEFICITS
        )
        assert sorted(image) == list(range(7))
        deficit_permutations.append(image)

    valid = set(valid_deficit_matchings())
    for matching in valid:
        for p_image in deficit_permutations:
            for n_image in deficit_permutations:
                direct = [None] * 7
                swapped = [None] * 7
                for p_edge, n_edge in enumerate(matching):
                    direct[p_image[p_edge]] = n_image[n_edge]
                    swapped[n_image[n_edge]] = p_image[p_edge]
                assert tuple(direct) in valid
                assert tuple(swapped) in valid
    return {
        "polar_line_group_order": 48,
        "support_graph_automorphism_group_order": 4,
        "all_4480_deficit_bijections_closed_under_independent_support_relabelling_and_sign_swap": True,
    }


def column_types(
    t2: tuple[frozenset[int], ...], residual: tuple[tuple[int, ...], ...]
) -> tuple[tuple[frozenset[int], int, str], ...]:
    rows: list[tuple[frozenset[int], int, str]] = [
        (column, 1, f"t2:{i}") for i, column in enumerate(t2)
    ]
    rows.extend(
        (frozenset((p, n + 7)), residual[p][n], f"t1:{p},{n}")
        for p in range(7) for n in range(7) if residual[p][n]
    )
    rows.append((frozenset(), 17, "t0"))
    return tuple(rows)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def selected_union_feasible(
    h: tuple[tuple[int, int], ...],
    blocks: tuple[frozenset[int], ...],
    incident: tuple[frozenset[int], ...],
    chosen_columns: tuple[frozenset[int], ...],
) -> tuple[bool, tuple[tuple[int, int], ...] | None]:
    """Solve the remaining at-most-ten marked-zero adjacency bits exactly."""
    # Vertex ids 0..13 are support, 14..18 are the five marked zeros.
    fixed = set(SUPPORT_EDGES)
    for z, column in enumerate(chosen_columns):
        fixed.update(edge(s, 14 + z) for s in column)
    optional = []
    for a, b in combinations(range(5), 2):
        if set(h[a]) & set(h[b]):
            fixed.add((14 + a, 14 + b))
        else:
            optional.append((14 + a, 14 + b))

    lines = tuple(
        frozenset((*blocks[i], *(14 + z for z in incident[i]))) for i in range(8)
    )
    assert all(len(row) == 3 for row in lines)

    # Fixed contribution and a 28-bit coefficient mask per optional edge.
    targets = []
    fixed_counts = []
    coefficients = []
    for i, j in combinations(range(8), 2):
        targets.append(4 if (i, j) in h else POLAR[i][j])
        fixed_counts.append(sum(edge(u, v) in fixed for u in lines[i] for v in lines[j] if u != v))
        coefficients.append(tuple(
            int((u in lines[i] and v in lines[j]) or (v in lines[i] and u in lines[j]))
            for u, v in optional
        ))
    residual = tuple(t - f for t, f in zip(targets, fixed_counts))
    if min(residual) < 0:
        return False, None

    candidates = []
    for bits in range(1 << len(optional)):
        if all(sum(row[k] for k in range(len(optional)) if bits >> k & 1) == need for row, need in zip(coefficients, residual)):
            candidates.append(bits)
    for bits in candidates:
        edges = fixed | {optional[k] for k in range(len(optional)) if bits >> k & 1}
        adj = graph(tuple(edges), 19)
        if any(
            len(adj[u] & adj[v]) > (1 if v in adj[u] else 2)
            for u, v in combinations(range(19), 2)
        ):
            continue
        return True, tuple(optional[k] for k in range(len(optional)) if bits >> k & 1)
    return False, None


def assignment_exists(
    h: tuple[tuple[int, int], ...],
    blocks: tuple[frozenset[int], ...],
    incident: tuple[frozenset[int], ...],
    types: tuple[tuple[frozenset[int], int, str], ...],
) -> tuple[bool, dict[str, object] | None]:
    """Assign the five labelled marked zeros to distinct column copies."""
    required = tuple(blocks[i] | blocks[j] for i, j in h)
    candidates = tuple(
        tuple(index for index, (column, capacity, _) in enumerate(types) if capacity and need <= column)
        for need in required
    )
    if any(not row for row in candidates):
        return False, None
    order = tuple(sorted(range(5), key=lambda z: len(candidates[z])))
    used = [0] * len(types)
    choice = [-1] * 5

    def rec(depth: int) -> tuple[bool, dict[str, object] | None]:
        if depth == 5:
            columns = tuple(types[choice[z]][0] for z in range(5))
            ok, optional = selected_union_feasible(h, blocks, incident, columns)
            if ok:
                return True, {
                    "column_labels": [types[choice[z]][2] for z in range(5)],
                    "column_supports": [sorted(columns[z]) for z in range(5)],
                    "optional_marked_zero_edges": [list(row) for row in optional or ()],
                }
            return False, None
        z = order[depth]
        for kind in candidates[z]:
            if used[kind] == types[kind][1]:
                continue
            used[kind] += 1
            choice[z] = kind
            ok, witness = rec(depth + 1)
            if ok:
                return ok, witness
            used[kind] -= 1
        return False, None

    return rec(0)


# Abstract outside-column kinds.  A t1 kind is (1,p,n), a t2 kind is
# (2,p_deficit_edge_index,n_deficit_edge_index), and the empty kind is (0,).
ColumnKind = tuple[int, ...]


@lru_cache(maxsize=1)
def abstract_column_kinds() -> tuple[ColumnKind, ...]:
    return (
        *((1, p, n) for p in range(7) for n in range(7)),
        *((2, p_edge, n_edge) for p_edge in range(7) for n_edge in range(7)),
        (0,),
    )


@lru_cache(maxsize=None)
def kind_support(kind: ColumnKind) -> frozenset[int]:
    if kind[0] == 0:
        return frozenset()
    if kind[0] == 1:
        return frozenset((kind[1], kind[2] + 7))
    assert kind[0] == 2
    return frozenset((*DEFICITS[kind[1]], *(v + 7 for v in DEFICITS[kind[2]])))


def kind_label(kind: ColumnKind) -> str:
    if kind[0] == 0:
        return "t0"
    return f"t{kind[0]}:{kind[1]},{kind[2]}"


PAIR_ROWS = tuple(combinations(range(8), 2))


def vector_for_edges(
    lines: tuple[frozenset[int], ...], edges: set[tuple[int, int]] | frozenset[tuple[int, int]]
) -> tuple[int, ...]:
    return tuple(
        sum(edge(u, v) in edges for u in lines[i] for v in lines[j] if u != v)
        for i, j in PAIR_ROWS
    )


@lru_cache(maxsize=None)
def abstract_solutions(case: Case) -> tuple[tuple[tuple[ColumnKind, ...], tuple[tuple[int, int], ...]], ...]:
    """All column-kind assignments satisfying the exact selected-union tests."""
    h, p_blocks, n_blocks = case
    blocks, incident = line_sets(h, p_blocks, n_blocks)
    lines = tuple(
        frozenset((*blocks[i], *(14 + z for z in incident[i]))) for i in range(8)
    )
    assert all(len(row) == 3 for row in lines)

    mandatory_zero_edges = {
        (14 + a, 14 + b)
        for a, b in combinations(range(5), 2)
        if set(h[a]) & set(h[b])
    }
    optional_zero_edges = tuple(
        (14 + a, 14 + b)
        for a, b in combinations(range(5), 2)
        if not (set(h[a]) & set(h[b]))
    )
    base_edges = set(SUPPORT_EDGES) | mandatory_zero_edges
    base_vector = vector_for_edges(lines, base_edges)
    target = tuple(4 if pair in h else POLAR[pair[0]][pair[1]] for pair in PAIR_ROWS)
    optional_vectors = tuple(
        vector_for_edges(lines, {pair}) for pair in optional_zero_edges
    )
    optional_sums: dict[tuple[int, ...], list[int]] = {}
    for bits in range(1 << len(optional_zero_edges)):
        total = tuple(
            sum(optional_vectors[k][r] for k in range(len(optional_zero_edges)) if bits >> k & 1)
            for r in range(len(PAIR_ROWS))
        )
        optional_sums.setdefault(total, []).append(bits)

    required = tuple(blocks[i] | blocks[j] for i, j in h)
    candidates = tuple(
        tuple(kind for kind in abstract_column_kinds() if need <= kind_support(kind))
        for need in required
    )
    assert all(candidates)
    order = tuple(sorted(range(5), key=lambda z: (len(candidates[z]), z)))
    contributions = {
        (z, kind): vector_for_edges(
            lines, {edge(s, 14 + z) for s in kind_support(kind)}
        )
        for z in range(5) for kind in candidates[z]
    }
    chosen: list[ColumnKind | None] = [None] * 5
    used: Counter[ColumnKind] = Counter()
    used_p_deficits: set[int] = set()
    used_n_deficits: set[int] = set()
    solutions: list[tuple[tuple[ColumnKind, ...], tuple[tuple[int, int], ...]]] = []

    def recurse(depth: int, current: tuple[int, ...]) -> None:
        if any(current[r] > target[r] for r in range(len(target))):
            return
        if depth == 5:
            residual = tuple(target[r] - current[r] for r in range(len(target)))
            for bits in optional_sums.get(residual, []):
                added = {
                    optional_zero_edges[k]
                    for k in range(len(optional_zero_edges)) if bits >> k & 1
                }
                all_edges = set(base_edges) | added
                for z, kind in enumerate(chosen):
                    assert kind is not None
                    all_edges.update(edge(s, 14 + z) for s in kind_support(kind))
                adj = graph(tuple(all_edges), 19)
                if any(
                    len(adj[u] & adj[v]) > (1 if v in adj[u] else 2)
                    for u, v in combinations(range(19), 2)
                ):
                    continue
                solutions.append(
                    (
                        tuple(kind for kind in chosen if kind is not None),
                        tuple(sorted(added)),
                    )
                )
            return

        z = order[depth]
        for kind in candidates[z]:
            maximum = 17 if kind[0] == 0 else (2 if kind[0] == 1 else 1)
            if used[kind] >= maximum:
                continue
            if kind[0] == 2 and (kind[1] in used_p_deficits or kind[2] in used_n_deficits):
                continue
            used[kind] += 1
            if kind[0] == 2:
                used_p_deficits.add(kind[1])
                used_n_deficits.add(kind[2])
            chosen[z] = kind
            delta = contributions[z, kind]
            recurse(depth + 1, tuple(current[r] + delta[r] for r in range(len(current))))
            chosen[z] = None
            if kind[0] == 2:
                used_p_deficits.remove(kind[1])
                used_n_deficits.remove(kind[2])
            used[kind] -= 1

    recurse(0, base_vector)
    # The recursion order is not the marked-zero order, but `chosen` is.
    assert len(solutions) == len(set(solutions))
    return tuple(sorted(solutions))


@lru_cache(maxsize=1)
def matching_data() -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    matchings = valid_deficit_matchings()
    residuals = []
    for matching in matchings:
        row = deficit_columns(matching)
        assert row is not None
        residuals.append(row[1])
    return matchings, tuple(residuals)


@lru_cache(maxsize=1)
def availability_masks() -> dict[tuple[int, ...], int]:
    matchings, residuals = matching_data()
    masks: dict[tuple[int, ...], int] = {}
    all_mask = (1 << len(matchings)) - 1
    masks[(0,)] = all_mask
    for p_edge in range(7):
        for n_edge in range(7):
            masks[(2, p_edge, n_edge, 1)] = sum(
                1 << index
                for index, matching in enumerate(matchings)
                if matching[p_edge] == n_edge
            )
    for p in range(7):
        for n in range(7):
            for multiplicity in (1, 2):
                masks[(1, p, n, multiplicity)] = sum(
                    1 << index
                    for index, residual in enumerate(residuals)
                    if residual[p][n] >= multiplicity
                )
    return masks


def solution_availability(solution: tuple[ColumnKind, ...]) -> int:
    masks = availability_masks()
    mask = masks[(0,)]
    counts = Counter(solution)
    for kind, multiplicity in counts.items():
        if kind[0] == 0:
            assert multiplicity <= 17
            continue
        key = (*kind, multiplicity)
        mask &= masks[key]
    return mask


def concrete_columns(
    matching_index: int,
) -> tuple[tuple[frozenset[int], ...], dict[ColumnKind, tuple[int, ...]]]:
    matchings, residuals = matching_data()
    matching = matchings[matching_index]
    residual = residuals[matching_index]
    row = deficit_columns(matching)
    assert row is not None
    t2, _ = row
    columns = list(t2)
    ids: dict[ColumnKind, tuple[int, ...]] = {
        (2, p_edge, matching[p_edge]): (p_edge,) for p_edge in range(7)
    }
    for p in range(7):
        for n in range(7):
            start = len(columns)
            columns.extend(frozenset((p, n + 7)) for _ in range(residual[p][n]))
            if residual[p][n]:
                ids[(1, p, n)] = tuple(range(start, len(columns)))
    start = len(columns)
    columns.extend(frozenset() for _ in range(17))
    ids[(0,)] = tuple(range(start, len(columns)))
    assert len(columns) == 85
    return tuple(columns), ids


def verify_F_identity(columns: tuple[frozenset[int], ...]) -> bool:
    """Check FF^T=12I-A_S+2J-A_S^2 entry by entry."""
    assert len(columns) == 85
    assert Counter(len(column) for column in columns) == Counter({0: 17, 2: 61, 4: 7})
    gram = F_gram_matrix()
    for u in range(14):
        for v in range(14):
            observed = sum(u in column and v in column for column in columns)
            assert observed == gram[u][v]
    return True


def rational_rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for r in range(len(rows)):
            if r == rank or not rows[r][column]:
                continue
            scale = rows[r][column]
            rows[r] = [a - scale * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


@lru_cache(maxsize=1)
def F_gram_matrix() -> tuple[tuple[int, ...], ...]:
    support_adj = graph(tuple(SUPPORT_EDGES), 14)
    matrix = tuple(
        tuple(
            12 * int(u == v)
            - int(v in support_adj[u])
            + 2
            - (len(support_adj[u]) if u == v else len(support_adj[u] & support_adj[v]))
            for v in range(14)
        )
        for u in range(14)
    )
    signed = (1,) * 7 + (-1,) * 7
    assert all(sum(matrix[u][v] * signed[v] for v in range(14)) == 0 for u in range(14))
    assert rational_rank(matrix) == 13
    return matrix


@lru_cache(maxsize=None)
def perfect_matching_count(neighbor_masks: tuple[int, ...], remaining: int) -> int:
    if remaining == 0:
        return 1
    lowest = (remaining & -remaining).bit_length() - 1
    choices = neighbor_masks[lowest] & remaining & ~(1 << lowest)
    total = 0
    while choices:
        bit = choices & -choices
        other = bit.bit_length() - 1
        total += perfect_matching_count(
            neighbor_masks, remaining & ~(1 << lowest) & ~(1 << other)
        )
        choices ^= bit
    return total


def local_matching_counts(
    columns: tuple[frozenset[int], ...],
    fixed_zero_edges: frozenset[tuple[int, int]] = frozenset(),
) -> tuple[int, ...] | None:
    """Count completions of every support vertex's forced local 1-factor."""
    support_adj = graph(tuple(SUPPORT_EDGES), 14)
    counts = []
    for support in range(14):
        internal = tuple(sorted(support_adj[support]))
        outside = tuple(index for index, column in enumerate(columns) if support in column)
        vertices = tuple((0, u) for u in internal) + tuple((1, z) for z in outside)
        known = [set() for _ in vertices]
        for left, right in combinations(range(len(vertices)), 2):
            a_kind, a = vertices[left]
            b_kind, b = vertices[right]
            adjacent = False
            if a_kind == b_kind == 0:
                adjacent = b in support_adj[a]
            elif a_kind != b_kind:
                s = a if a_kind == 0 else b
                z = a if a_kind == 1 else b
                adjacent = s in columns[z]
            else:
                adjacent = edge(a, b) in fixed_zero_edges
            if adjacent:
                known[left].add(right)
                known[right].add(left)
        if any(len(row) > 1 for row in known):
            return None
        if any(not known[index] and vertices[index][0] == 0 for index in range(len(vertices))):
            return None
        unmatched = tuple(
            vertices[index][1]
            for index in range(len(vertices))
            if vertices[index][0] == 1 and not known[index]
        )
        neighbor_masks = []
        for z in unmatched:
            mask = 0
            for index, w in enumerate(unmatched):
                if z != w and columns[z] & columns[w] == {support}:
                    mask |= 1 << index
            neighbor_masks.append(mask)
        count = perfect_matching_count(tuple(neighbor_masks), (1 << len(unmatched)) - 1)
        if count == 0:
            return None
        counts.append(count)
    return tuple(counts)


def concrete_solution(
    solution: tuple[ColumnKind, ...], matching_index: int
) -> tuple[tuple[frozenset[int], ...], tuple[int, ...]]:
    columns, ids = concrete_columns(matching_index)
    used: Counter[ColumnKind] = Counter()
    selected = []
    for kind in solution:
        copy = used[kind]
        assert copy < len(ids[kind])
        selected.append(ids[kind][copy])
        used[kind] += 1
    return columns, tuple(selected)


def selected_local_extension(
    case: Case,
    solution: tuple[ColumnKind, ...],
    optional_edges: tuple[tuple[int, int], ...],
    matching_index: int,
) -> tuple[int, ...] | None:
    h = case[0]
    columns, selected = concrete_solution(solution, matching_index)
    fixed = {
        edge(selected[a], selected[b])
        for a, b in combinations(range(5), 2)
        if set(h[a]) & set(h[b])
    }
    fixed.update(
        edge(selected[a - 14], selected[b - 14]) for a, b in optional_edges
    )
    return local_matching_counts(columns, frozenset(fixed))


@lru_cache(maxsize=1)
def requirement_patterns() -> tuple[tuple[tuple[int, ...], ...], ...]:
    patterns = set()
    for h, p_blocks, n_blocks in labelled_cases():
        blocks, _ = line_sets(h, p_blocks, n_blocks)
        patterns.add(tuple(sorted(tuple(sorted(blocks[i] | blocks[j])) for i, j in h)))
    assert len(patterns) == 232
    return tuple(sorted(patterns))


def requirements_assignable(
    requirements: tuple[tuple[int, ...], ...], matching_index: int
) -> bool:
    """Containment-only five-column assignment with exact multiplicities."""
    matchings, residuals = matching_data()
    matching = matchings[matching_index]
    residual = residuals[matching_index]
    candidates, order = requirement_candidates(requirements)
    used: Counter[ColumnKind] = Counter()

    def capacity(kind: ColumnKind) -> int:
        if kind[0] == 0:
            return 17
        if kind[0] == 1:
            return residual[kind[1]][kind[2]]
        return int(matching[kind[1]] == kind[2])

    def recurse(depth: int) -> bool:
        if depth == 5:
            return True
        z = order[depth]
        for kind in candidates[z]:
            if used[kind] == capacity(kind):
                continue
            used[kind] += 1
            if recurse(depth + 1):
                return True
            used[kind] -= 1
        return False

    return recurse(0)


@lru_cache(maxsize=None)
def requirement_candidates(
    requirements: tuple[tuple[int, ...], ...]
) -> tuple[tuple[tuple[ColumnKind, ...], ...], tuple[int, ...]]:
    candidates = tuple(
        tuple(
            kind for kind in abstract_column_kinds()
            if frozenset(requirement) <= kind_support(kind)
        )
        for requirement in requirements
    )
    assert all(candidates)
    order = tuple(sorted(range(5), key=lambda z: (len(candidates[z]), z)))
    return candidates, order


@lru_cache(maxsize=1)
def containment_catalog() -> tuple[dict[str, object], ...]:
    rows = []
    for pattern in requirement_patterns():
        matching_indices = [
            index for index in range(4480) if requirements_assignable(pattern, index)
        ]
        rows.append({
            "requirements": [list(row) for row in pattern],
            "compatible_deficit_bijections": len(matching_indices),
            "first_matching_index": matching_indices[0],
        })
    counts = [int(row["compatible_deficit_bijections"]) for row in rows]
    assert min(counts) == 422
    assert max(counts) == 2116
    return tuple(rows)


@lru_cache(maxsize=1)
def base_local_matching_census() -> dict[str, object]:
    neighborhood_counts: Counter[int] = Counter()
    signatures: Counter[tuple[int, ...]] = Counter()
    admissible = 0
    for matching_index in range(4480):
        columns, _ = concrete_columns(matching_index)
        assert verify_F_identity(columns)
        counts = local_matching_counts(columns)
        if counts is None:
            continue
        admissible += 1
        neighborhood_counts.update(counts)
        signatures[tuple(sorted(counts))] += 1
    assert admissible == 4480
    assert neighborhood_counts == Counter({
        68: 7808, 78: 17536, 90: 1536, 594: 18496, 604: 17344,
    })
    return {
        "deficit_bijections_checked": 4480,
        "configurations_admitting_all_14_local_matchings": admissible,
        "distinct_sorted_14_neighborhood_count_signatures": len(signatures),
        "individual_neighborhood_perfect_matching_count_distribution": {
            str(value): count for value, count in sorted(neighborhood_counts.items())
        },
    }


def bit_indices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


@lru_cache(maxsize=1)
def orbit_coupling_catalog() -> tuple[dict[str, object], ...]:
    rows = []
    for orbit_index, (case, orbit_size) in enumerate(case_orbits()):
        solutions = abstract_solutions(case)
        preliminary_mask = 0
        solution_masks = []
        for solution, optional in solutions:
            mask = solution_availability(solution)
            solution_masks.append((solution, optional, mask))
            preliminary_mask |= mask

        final_indices = []
        witness = None
        for matching_index in bit_indices(preliminary_mask):
            for solution, optional, mask in solution_masks:
                if not (mask >> matching_index) & 1:
                    continue
                local_counts = selected_local_extension(
                    case, solution, optional, matching_index
                )
                if local_counts is None:
                    continue
                final_indices.append(matching_index)
                if witness is None:
                    matchings, residuals = matching_data()
                    columns, selected_ids = concrete_solution(solution, matching_index)
                    witness = {
                        "matching_index": matching_index,
                        "deficit_bijection": list(matchings[matching_index]),
                        "t1_residual_matrix": [list(row) for row in residuals[matching_index]],
                        "selected_column_kinds": [kind_label(kind) for kind in solution],
                        "selected_column_ids": list(selected_ids),
                        "selected_column_supports": [
                            sorted(columns[column]) for column in selected_ids
                        ],
                        "optional_marked_zero_edges": [list(row) for row in optional],
                        "local_perfect_matching_counts": list(local_counts),
                    }
                break
        assert len(final_indices) == len(set(final_indices))
        rows.append({
            "orbit_index": orbit_index,
            "labelled_case_orbit_size": orbit_size,
            "representative": encode_case(case),
            "selected_union_abstract_solutions": len(solutions),
            "deficit_bijections_after_polar_and_induced_caps": preliminary_mask.bit_count(),
            "deficit_bijections_after_local_matching_extension": len(final_indices),
            "witness": witness,
        })
    assert len(rows) == 33
    assert sum(bool(row["witness"]) for row in rows) == 3
    assert sum(
        int(row["labelled_case_orbit_size"])
        * int(row["deficit_bijections_after_local_matching_extension"])
        for row in rows
    ) == 55_296
    return tuple(rows)


@lru_cache(maxsize=1)
def expanded_survivor_summary() -> dict[str, object]:
    """Expand the three surviving representatives back to labelled cases."""
    surviving_representatives = {
        row["orbit_index"]
        for row in orbit_coupling_catalog()
        if row["witness"] is not None
    }
    expanded: set[Case] = set()
    for orbit_index, (representative, _) in enumerate(case_orbits()):
        if orbit_index not in surviving_representatives:
            continue
        expanded.update(
            transform_case(representative, line_perm, p_auto, n_auto, swap)
            for swap in (False, True)
            for line_perm in permutations(range(4))
            for p_auto in support_automorphisms()
            for n_auto in support_automorphisms()
        )
    assert len(expanded) == 1536
    h_counts = Counter(case[0] for case in expanded)
    assert Counter(h_counts.values()) == Counter({16: 96})

    def degree_type(h: tuple[tuple[int, int], ...]) -> str:
        degree = [sum(i in pair for pair in h) for i in range(8)]
        p = ",".join(map(str, sorted(degree[:4], reverse=True)))
        n = ",".join(map(str, sorted(degree[4:], reverse=True)))
        return f"P_{p}__N_{n}"

    h_type_counts = Counter(degree_type(h) for h in h_counts)
    assert h_type_counts == Counter({
        "P_3,1,1,0__N_2,2,1,0": 36,
        "P_2,2,1,0__N_3,1,1,0": 36,
        "P_2,2,1,0__N_2,2,1,0": 24,
    })
    return {
        "distinct_labelled_H_surviving": len(h_counts),
        "ordered_packings_per_surviving_H": 16,
        "surviving_H_degree_type_counts": dict(sorted(h_type_counts.items())),
        "P_3,1,1,0__N_3,1,1,0_H_surviving": 0,
    }


@lru_cache(maxsize=1)
def build_hostile_controls() -> dict[str, object]:
    """One explicit 19-point/F-column control for each surviving case orbit."""
    controls = []
    for row in orbit_coupling_catalog():
        witness = row["witness"]
        if witness is None:
            continue
        orbit_index = int(row["orbit_index"])
        case = case_orbits()[orbit_index][0]
        h, p_blocks, n_blocks = case
        matching_index = int(witness["matching_index"])
        solution = next(
            solution
            for solution, optional in abstract_solutions(case)
            if [kind_label(kind) for kind in solution] == witness["selected_column_kinds"]
            and [list(edge) for edge in optional] == witness["optional_marked_zero_edges"]
            and (solution_availability(solution) >> matching_index) & 1
        )
        optional = next(
            optional
            for candidate, optional in abstract_solutions(case)
            if candidate == solution
            and [list(edge) for edge in optional] == witness["optional_marked_zero_edges"]
        )
        columns, selected = concrete_solution(solution, matching_index)
        assert verify_F_identity(columns)
        outside_vertices = tuple(14 + column for column in selected)
        blocks, incident = line_sets(h, p_blocks, n_blocks)
        lines = tuple(
            tuple(sorted((*blocks[i], *(outside_vertices[z] for z in incident[i]))))
            for i in range(8)
        )
        fixed_zero_edges = {
            edge(outside_vertices[a], outside_vertices[b])
            for a, b in combinations(range(5), 2)
            if set(h[a]) & set(h[b])
        }
        fixed_zero_edges.update(
            edge(outside_vertices[a - 14], outside_vertices[b - 14])
            for a, b in optional
        )
        union_edges = set(SUPPORT_EDGES) | fixed_zero_edges
        union_edges.update(
            edge(support, 14 + column)
            for column in selected for support in columns[column]
        )
        selected_vertices = set(range(14)) | set(outside_vertices)
        adj = graph(tuple(union_edges), 99)
        for i, j in PAIR_ROWS:
            observed = sum(
                v in adj[u] for u in lines[i] for v in lines[j] if u != v
            )
            assert observed == (4 if (i, j) in h else POLAR[i][j])
        for u, v in combinations(sorted(selected_vertices), 2):
            common = len((adj[u] & adj[v]) & selected_vertices)
            assert common <= (1 if v in adj[u] else 2)
        c = [1] * 7 + [-1] * 7 + [0] * 85
        for vertex in selected_vertices:
            assert sum(c[other] for other in adj[vertex] & selected_vertices) == 3 * c[vertex]
        controls.append({
            "orbit_index": orbit_index,
            "orbit_size": row["labelled_case_orbit_size"],
            "case": encode_case(case),
            "deficit_matching_index": matching_index,
            "deficit_bijection": witness["deficit_bijection"],
            "F_columns_support_neighbors": [sorted(column) for column in columns],
            "selected_outside_column_indices": list(selected),
            "selected_outside_vertex_ids": list(outside_vertices),
            "selected_triangles": [list(line) for line in lines],
            "selected_union_edges": [list(pair) for pair in sorted(union_edges)],
            "local_perfect_matching_counts": witness["local_perfect_matching_counts"],
            "checks": {
                "F_F_transpose_block_identity": True,
                "selected_polar_cross_count_matrix": True,
                "mandatory_triangle_edges": True,
                "induced_lambda_mu_caps": True,
                "induced_Ac_equals_3c": True,
                "all_14_support_local_matchings_extend": True,
            },
        })
    assert len(controls) == 3
    return {
        "claim_label": "CANDIDATE",
        "scope": "three orbit-representative 19-point controls with complete 85-column F multisets",
        "controls": controls,
        "limitations": [
            "these controls omit most outside-outside adjacencies and are not 99-vertex graphs",
            "they certify survival of necessary local equations, not existence of an SRG completion",
        ],
    }


@lru_cache(maxsize=1)
def build_results() -> dict[str, object]:
    inputs = verify_inputs()
    symmetries = symmetry_audit()
    containment = containment_catalog()
    orbit_rows = orbit_coupling_catalog()
    orbit_distribution = Counter(
        (
            int(row["selected_union_abstract_solutions"]),
            int(row["deficit_bijections_after_local_matching_extension"]),
        )
        for row in orbit_rows
    )
    total_raw = 20_928 * 4480
    total_surviving = sum(
        int(row["labelled_case_orbit_size"])
        * int(row["deficit_bijections_after_local_matching_extension"])
        for row in orbit_rows
    )
    assert total_raw == 93_757_440
    total_abstract_assignment_branches = sum(
        int(row["labelled_case_orbit_size"])
        * sum(
            solution_availability(solution).bit_count()
            for solution, _ in abstract_solutions(case_orbits()[int(row["orbit_index"])][0])
        )
        for row in orbit_rows
    )
    assert total_abstract_assignment_branches == 73_728
    return {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "inputs": inputs,
        "upstream_delta": {
            "wave209_verifier_weight20_352_to_346": "recorded but not imported; this Wave210 lane is restricted to the weight-14 branch",
            "delta_claim_label": "DERIVED in the sealed verifier package",
            "independent_reproduction_in_this_lane": False,
        },
        "label_coverage": {
            "labelled_H_cases": 204,
            "ordered_support_block_packing_cases": 20_928,
            "distinct_base_requirement_multisets": 232,
            "support_graph_automorphisms_enumerated": 4,
            "polar_line_symmetries_enumerated": 48,
            "proved_case_orbits": 33,
            "case_orbit_size_distribution": {
                "192": 1, "384": 10, "768": 22,
            },
            "capacity_compatible_deficit_bijections": 4480,
            "raw_H_packing_deficit_branches": total_raw,
            "symmetry_audit": symmetries,
        },
        "containment_only": {
            "patterns": list(containment),
            "minimum_compatible_deficit_bijections": min(
                int(row["compatible_deficit_bijections"]) for row in containment
            ),
            "maximum_compatible_deficit_bijections": max(
                int(row["compatible_deficit_bijections"]) for row in containment
            ),
            "patterns_with_at_least_one_assignment": sum(
                int(row["compatible_deficit_bijections"]) > 0 for row in containment
            ),
        },
        "selected_union_coupling": {
            "orbit_catalog": list(orbit_rows),
            "orbit_solution_survival_distribution": {
                f"abstract_solutions_{solutions}_matching_bijections_{matchings}": count
                for (solutions, matchings), count in sorted(orbit_distribution.items())
            },
            "case_orbits_surviving": sum(bool(row["witness"]) for row in orbit_rows),
            "labelled_H_packing_cases_surviving": sum(
                int(row["labelled_case_orbit_size"])
                for row in orbit_rows if row["witness"]
            ),
            "labelled_H_packing_deficit_branches_surviving": total_surviving,
            "abstract_column_assignment_branches_surviving": total_abstract_assignment_branches,
            "fraction_of_raw_branches": f"{total_surviving}/{total_raw}",
            "expanded_labelled_survivors": expanded_survivor_summary(),
            "all_surviving_selected_unions_extend_local_matchings": all(
                row["deficit_bijections_after_polar_and_induced_caps"]
                == row["deficit_bijections_after_local_matching_extension"]
                for row in orbit_rows
            ),
        },
        "base_local_matching": base_local_matching_census(),
        "unresolved_outside_block": {
            "F_rank_over_Q": rational_rank(F_gram_matrix()),
            "left_kernel_generator": [1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1],
            "top_right_block_equation": "F D = 2J - (A_S+I)F",
            "bottom_right_block_equation": "D^2+D = 12I+2J-F^T F",
            "status": "not solved; no 85-vertex D adjacency matrix is supplied",
        },
        "limitations": [
            "the 33-orbit cache is used only after all 20,928 labelled H/packing cases are explicitly generated and partitioned under 48 proved polar-line symmetries and two independent four-element support automorphism groups",
            "the 55,296 survivors are necessary selected-union and local-neighborhood controls, not 99-vertex graph completions",
            "outside-outside edges beyond the forced local matchings, the full 85-vertex D block equations, all degrees, and all common-neighbor equalities remain unresolved",
            "no target automorphism is assumed and no global graph, endpoint exclusion, or Conway-99 resolution is supplied",
        ],
    }


def smoke() -> None:
    assert DEFICITS == ((1, 4), (1, 5), (2, 3), (2, 6), (3, 5), (4, 6), (5, 6))
    hs = marked_graphs()
    assert Counter(
        (tuple(sorted(Counter(i for e in h for i in e if i < 4).values(), reverse=True)),
         tuple(sorted(Counter(i for e in h for i in e if i >= 4).values(), reverse=True)))
        for h in hs
    ) == Counter({((3, 1, 1), (3, 1, 1)): 12, ((3, 1, 1), (2, 2, 1)): 36,
                  ((2, 2, 1), (3, 1, 1)): 36, ((2, 2, 1), (2, 2, 1)): 120})
    assert len(valid_deficit_matchings()) == 4480
    assert len(labelled_cases()) == 20_928
    assert len(requirement_patterns()) == 232
    assert len(case_orbits()) == 33
    print("smoke PASS", len(hs), len(labelled_cases()), len(case_orbits()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        smoke()
        return
    payload = build_results()
    if args.write:
        RESULTS.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        CONTROLS.write_text(
            json.dumps(build_hostile_controls(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print("wrote", RESULTS.as_posix(), CONTROLS.as_posix())
        return
    if args.verify:
        expected = json.loads(RESULTS.read_text(encoding="utf-8"))
        assert payload == expected
        expected_controls = json.loads(CONTROLS.read_text(encoding="utf-8"))
        assert build_hostile_controls() == expected_controls
        print("verified", RESULTS.as_posix(), CONTROLS.as_posix())
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
