#!/usr/bin/env python3
"""Independent exact verifier for the Wave 210 rank-three coupling package.

This file deliberately does not import or execute discovery code.  It rebuilds
the finite objects from the frozen mathematical definitions using bitmasks,
brute-force automorphism enumeration, exact integer linear algebra, and an
independent perfect-matching recursion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
from typing import Iterable, Iterator


HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "independent-results.json"
HOSTILE_PATH = HERE / "independent-hostile-tests.json"

# Construct the frozen polar matrix from its definition: same-sign off-diagonal
# value 2, opposite matched value 0, and opposite unmatched value 1.
POLAR = tuple(
    tuple(
        0 if i == j or (i < 4 <= j and i == j - 4) or (j < 4 <= i and j == i - 4)
        else 2 if (i < 4) == (j < 4)
        else 1
        for j in range(8)
    )
    for i in range(8)
)

ROOT_EDGES = frozenset(
    (min(a, b), max(a, b))
    for a, b in (
        (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 5),
        (2, 6), (3, 4), (3, 5), (4, 6), (5, 6),
    )
)
Case = tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]
Kind = tuple[int, ...]
GroupElement = tuple[tuple[int, ...], tuple[int, ...]]  # line perm, support perm


def pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def adjacency(n: int, edges: Iterable[tuple[int, int]]) -> tuple[int, ...]:
    rows = [0] * n
    for a, b in edges:
        assert a != b
        rows[a] |= 1 << b
        rows[b] |= 1 << a
    return tuple(rows)


G7 = adjacency(7, ROOT_EDGES)
SUPPORT_EDGES = frozenset(
    (*edge,) for edge in (
        tuple(ROOT_EDGES)
        + tuple((a + 7, b + 7) for a, b in ROOT_EDGES)
        + ((0, 7),)
    )
)
SUPPORT_ADJ = adjacency(14, SUPPORT_EDGES)


def common_count(rows: tuple[int, ...], a: int, b: int) -> int:
    return (rows[a] & rows[b]).bit_count()


DEFICIT_EDGES = tuple(
    (a, b)
    for a, b in combinations(range(7), 2)
    if (1 if (G7[a] >> b) & 1 else 2) - common_count(G7, a, b) == 1
)
EXTERNAL_EDGES = frozenset(
    edge for edge in ROOT_EDGES if common_count(G7, edge[0], edge[1]) == 0
)


def target_gram() -> tuple[tuple[int, ...], ...]:
    """Compute 12I-A+2J-A^2 directly from the frozen support graph."""
    return tuple(
        tuple(
            12 * (u == v)
            - ((SUPPORT_ADJ[u] >> v) & 1)
            + 2
            - (SUPPORT_ADJ[u].bit_count() if u == v else common_count(SUPPORT_ADJ, u, v))
            for v in range(14)
        )
        for u in range(14)
    )


GRAM = target_gram()


def integer_rank(matrix: Iterable[Iterable[int]]) -> int:
    """Fraction-free exact row rank over Q."""
    rows = [list(map(int, row)) for row in matrix]
    if not rows:
        return 0
    ncols = len(rows[0])
    rank = 0
    for col in range(ncols):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pv = rows[rank][col]
        for r in range(len(rows)):
            if r == rank or rows[r][col] == 0:
                continue
            q = rows[r][col]
            rows[r] = [pv * x - q * y for x, y in zip(rows[r], rows[rank])]
            # Normalize by a gcd to control coefficient growth.
            g = 0
            for x in rows[r]:
                if x:
                    from math import gcd
                    g = gcd(g, abs(x))
            if g > 1:
                rows[r] = [x // g for x in rows[r]]
        rank += 1
        if rank == len(rows):
            break
    return rank


def canonical_json(value: object) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=False)


def digest_records(records: Iterable[object]) -> dict[str, object]:
    encoded = sorted(canonical_json(record) for record in records)
    payload = ("\n".join(encoded) + ("\n" if encoded else "")).encode("utf-8")
    return {"count": len(encoded), "sha256": hashlib.sha256(payload).hexdigest()}


@lru_cache(maxsize=1)
def marked_graphs() -> tuple[tuple[tuple[int, int], ...], ...]:
    product_edges = tuple(
        (p, 4 + n) for p in range(4) for n in range(4) if p != n
    )
    permitted = {(3, 1, 1, 0), (2, 2, 1, 0)}
    answer = []
    for chosen in combinations(product_edges, 5):
        degree = [0] * 8
        for a, b in chosen:
            degree[a] += 1
            degree[b] += 1
        if tuple(sorted(degree[:4], reverse=True)) not in permitted:
            continue
        if tuple(sorted(degree[4:], reverse=True)) not in permitted:
            continue
        isolated_p = degree[:4].index(0)
        isolated_n = degree[4:].index(0)
        if isolated_p == isolated_n:  # their polar entry is 0, not 1
            continue
        answer.append(tuple(chosen))
    assert len(answer) == 204 == len(set(answer))
    return tuple(answer)


@lru_cache(maxsize=None)
def support_partitions(degrees: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    sizes = tuple(3 - d for d in degrees)
    result: list[tuple[tuple[int, ...], ...]] = []

    def visit(line: int, unused: int, blocks: list[tuple[int, ...]]) -> None:
        if line == 4:
            if unused == 0:
                result.append(tuple(blocks))
            return
        points = tuple(i for i in range(7) if (unused >> i) & 1)
        for block in combinations(points, sizes[line]):
            edges = frozenset(pair(a, b) for a, b in combinations(block, 2))
            if len(block) == 3 and not edges <= ROOT_EDGES:
                continue
            if len(block) == 2 and next(iter(edges)) not in EXTERNAL_EDGES:
                continue
            mask = sum(1 << v for v in block)
            visit(line + 1, unused ^ mask, blocks + [tuple(block)])

    visit(0, (1 << 7) - 1, [])
    return tuple(result)


@lru_cache(maxsize=1)
def labelled_cases() -> tuple[Case, ...]:
    answer: list[Case] = []
    for h in marked_graphs():
        degree = [0] * 8
        for a, b in h:
            degree[a] += 1
            degree[b] += 1
        for p_blocks in support_partitions(tuple(degree[:4])):
            for n_blocks in support_partitions(tuple(degree[4:])):
                answer.append((h, p_blocks, n_blocks))
    assert len(answer) == 20_928 == len(set(answer))
    return tuple(answer)


def is_perm(values: tuple[int, ...]) -> bool:
    return sorted(values) == list(range(len(values)))


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right for old-to-new permutations."""
    return tuple(left[right[i]] for i in range(len(right)))


def inverse(perm: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(perm)
    for old, new in enumerate(perm):
        out[new] = old
    return tuple(out)


@lru_cache(maxsize=1)
def polar_automorphisms() -> tuple[tuple[int, ...], ...]:
    result = []
    for perm in permutations(range(8)):
        if all(POLAR[a][b] == POLAR[perm[a]][perm[b]] for a in range(8) for b in range(8)):
            result.append(perm)
    assert len(result) == 48
    return tuple(result)


@lru_cache(maxsize=1)
def support_automorphisms() -> tuple[tuple[int, ...], ...]:
    result = []
    for perm in permutations(range(7)):
        image = frozenset(pair(perm[a], perm[b]) for a, b in ROOT_EDGES)
        if image == ROOT_EDGES:
            result.append(perm)
    assert len(result) == 4
    return tuple(result)


def group_closure_audit(group: tuple[tuple[int, ...], ...]) -> dict[str, object]:
    elements = set(group)
    identity = tuple(range(len(group[0])))
    assert identity in elements
    assert all(inverse(g) in elements for g in group)
    assert all(compose(a, b) in elements for a in group for b in group)
    return {"order": len(group), "identity": True, "inverses": True, "closure": True}


@lru_cache(maxsize=1)
def full_case_group() -> tuple[GroupElement, ...]:
    """The 48 polar maps times independent output-side rooted automorphisms."""
    answer: list[GroupElement] = []
    for line_map in polar_automorphisms():
        preserves_sign = line_map[0] < 4
        assert all((line_map[i] < 4) == (preserves_sign if i < 4 else not preserves_sign) for i in range(8))
        for p_auto in support_automorphisms():
            for n_auto in support_automorphisms():
                support_map = [0] * 14
                for old in range(14):
                    old_sign = old >= 7
                    destination_sign = old_sign if preserves_sign else not old_sign
                    auto = n_auto if destination_sign else p_auto
                    support_map[old] = (7 if destination_sign else 0) + auto[old % 7]
                answer.append((line_map, tuple(support_map)))
    assert len(answer) == 768 == len(set(answer))
    return tuple(answer)


def transform_case(case: Case, action: GroupElement) -> Case:
    line_map, support_map = action
    h, p_blocks, n_blocks = case
    old_blocks = p_blocks + n_blocks
    new_blocks: list[tuple[int, ...] | None] = [None] * 8
    for old_line, block in enumerate(old_blocks):
        destination = line_map[old_line]
        mapped_global = tuple(sorted(support_map[(7 if old_line >= 4 else 0) + v] for v in block))
        expected_sign = 7 if destination >= 4 else 0
        assert all((v >= 7) == bool(expected_sign) for v in mapped_global)
        new_blocks[destination] = tuple(v - expected_sign for v in mapped_global)
    assert all(block is not None for block in new_blocks)
    new_h = tuple(sorted(pair(line_map[a], line_map[b]) for a, b in h))
    return (new_h, tuple(new_blocks[:4]), tuple(new_blocks[4:]))  # type: ignore[arg-type]


@lru_cache(maxsize=1)
def case_orbits() -> tuple[tuple[Case, ...], ...]:
    universe = set(labelled_cases())
    unseen = set(universe)
    answer = []
    actions = full_case_group()
    while unseen:
        representative = min(unseen)
        orbit = tuple(sorted({transform_case(representative, g) for g in actions}))
        assert set(orbit) <= universe
        unseen.difference_update(orbit)
        answer.append(orbit)
    assert len(answer) == 33
    assert Counter(map(len, answer)) == Counter({768: 22, 384: 10, 192: 1})
    assert sum(map(len, answer)) == len(universe)
    return tuple(answer)


def action_is_faithful() -> bool:
    cases = labelled_cases()
    signatures = {
        tuple(transform_case(cases[index], action) for index in (0, 31, 400, 5000, 15000))
        for action in full_case_group()
    }
    return len(signatures) == len(full_case_group())


def burnside_case_orbit_count() -> tuple[int, tuple[int, ...]]:
    cases = labelled_cases()
    fixed_counts = tuple(
        sum(transform_case(case, action) == case for case in cases)
        for action in full_case_group()
    )
    total = sum(fixed_counts)
    assert total % len(full_case_group()) == 0
    return total // len(full_case_group()), fixed_counts


def columns_for_matching(matching: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]] | None:
    """Derive F columns from the target Gram, not a hard-coded residual."""
    four_columns = []
    cross_used = [[0] * 7 for _ in range(7)]
    for p_edge_index, n_edge_index in enumerate(matching):
        p_edge = DEFICIT_EDGES[p_edge_index]
        n_edge = DEFICIT_EDGES[n_edge_index]
        mask = sum(1 << p for p in p_edge) | sum(1 << (7 + n) for n in n_edge)
        four_columns.append(mask)
        for p in p_edge:
            for n in n_edge:
                cross_used[p][n] += 1
    residual = tuple(
        tuple(GRAM[p][7 + n] - cross_used[p][n] for n in range(7))
        for p in range(7)
    )
    if min(min(row) for row in residual) < 0:
        return None
    columns = list(four_columns)
    for p in range(7):
        for n in range(7):
            columns.extend((1 << p) | (1 << (7 + n)) for _ in range(residual[p][n]))
    columns.extend(0 for _ in range(85 - len(columns)))
    if Counter(mask.bit_count() for mask in columns) != Counter({0: 17, 2: 61, 4: 7}):
        return None
    return tuple(columns), residual


@lru_cache(maxsize=1)
def deficit_configurations() -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[tuple[int, ...], ...], ...]]:
    matchings = []
    residuals = []
    for perm in permutations(range(7)):
        built = columns_for_matching(perm)
        if built is not None:
            matchings.append(perm)
            residuals.append(built[1])
    assert len(matchings) == 4480
    return tuple(matchings), tuple(residuals)


def observed_gram(columns: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(((column >> u) & 1) and ((column >> v) & 1) for column in columns) for v in range(14))
        for u in range(14)
    )


def f_configuration_audit() -> dict[str, object]:
    matchings, _ = deficit_configurations()
    failures = []
    for index, matching in enumerate(matchings):
        built = columns_for_matching(matching)
        assert built is not None
        columns, _ = built
        if observed_gram(columns) != GRAM:
            failures.append(index)
    signed = (1,) * 7 + (-1,) * 7
    assert all(sum(GRAM[i][j] * signed[j] for j in range(14)) == 0 for i in range(14))
    rank = integer_rank(GRAM)
    assert rank == 13 and not failures
    return {
        "configurations": len(matchings),
        "all_gram_identities_hold": True,
        "common_gram_rank_over_Q": rank,
        "therefore_each_F_rank_over_Q": rank,
        "signed_left_kernel": list(signed),
        "matching_set": digest_records(matchings),
    }


@lru_cache(maxsize=None)
def matching_count(neighbor_masks: tuple[int, ...], remaining: int) -> int:
    if remaining == 0:
        return 1
    first_bit = remaining & -remaining
    first = first_bit.bit_length() - 1
    choices = neighbor_masks[first] & (remaining ^ first_bit)
    total = 0
    while choices:
        choice_bit = choices & -choices
        total += matching_count(neighbor_masks, remaining ^ first_bit ^ choice_bit)
        choices ^= choice_bit
    return total


def local_one_factor_counts(
    columns: tuple[int, ...], fixed_outside_edges: frozenset[tuple[int, int]] = frozenset()
) -> tuple[int, ...] | None:
    answer = []
    for center in range(14):
        inside = tuple(v for v in range(14) if (SUPPORT_ADJ[center] >> v) & 1)
        outside = tuple(i for i, column in enumerate(columns) if (column >> center) & 1)
        vertices = tuple((0, v) for v in inside) + tuple((1, z) for z in outside)
        known_degree = [0] * len(vertices)
        for i, j in combinations(range(len(vertices)), 2):
            ka, a = vertices[i]
            kb, b = vertices[j]
            adjacent = False
            if ka == kb == 0:
                adjacent = bool((SUPPORT_ADJ[a] >> b) & 1)
            elif ka != kb:
                support = a if ka == 0 else b
                column = a if ka == 1 else b
                adjacent = bool((columns[column] >> support) & 1)
            else:
                adjacent = pair(a, b) in fixed_outside_edges
            if adjacent:
                known_degree[i] += 1
                known_degree[j] += 1
        if max(known_degree, default=0) > 1:
            return None
        if any(vertices[i][0] == 0 and known_degree[i] == 0 for i in range(len(vertices))):
            return None
        unmatched = tuple(vertices[i][1] for i in range(len(vertices)) if vertices[i][0] == 1 and known_degree[i] == 0)
        compatibility = []
        target = 1 << center
        for z in unmatched:
            mask = 0
            for i, w in enumerate(unmatched):
                if z != w and (columns[z] & columns[w]) == target:
                    mask |= 1 << i
            compatibility.append(mask)
        count = matching_count(tuple(compatibility), (1 << len(unmatched)) - 1)
        if count == 0:
            return None
        answer.append(count)
    return tuple(answer)


@lru_cache(maxsize=1)
def base_local_census() -> dict[str, object]:
    frequency: Counter[int] = Counter()
    signature_frequency: Counter[tuple[int, ...]] = Counter()
    admitted = 0
    for matching in deficit_configurations()[0]:
        built = columns_for_matching(matching)
        assert built is not None
        counts = local_one_factor_counts(built[0])
        if counts is None:
            continue
        admitted += 1
        frequency.update(counts)
        signature_frequency[tuple(sorted(counts))] += 1
    assert admitted == 4480
    assert frequency == Counter({68: 7808, 78: 17536, 90: 1536, 594: 18496, 604: 17344})
    return {
        "configurations_tested": 4480,
        "configurations_feasible_at_all_14_support_vertices": admitted,
        "neighborhoods_tested": 4480 * 14,
        "perfect_matching_count_distribution": {str(k): v for k, v in sorted(frequency.items())},
        "sorted_signature_count": len(signature_frequency),
    }


def block_and_incidence(case: Case) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    h, p_blocks, n_blocks = case
    blocks = tuple(sum(1 << v for v in block) for block in p_blocks) + tuple(
        sum(1 << (7 + v) for v in block) for block in n_blocks
    )
    incident = tuple(tuple(z for z, edge in enumerate(h) if line in edge) for line in range(8))
    return blocks, incident


@lru_cache(maxsize=1)
def column_kinds() -> tuple[Kind, ...]:
    return (
        *((1, p, n) for p in range(7) for n in range(7)),
        *((2, pe, ne) for pe in range(7) for ne in range(7)),
        (0,),
    )


@lru_cache(maxsize=None)
def kind_mask(kind: Kind) -> int:
    if kind[0] == 0:
        return 0
    if kind[0] == 1:
        return (1 << kind[1]) | (1 << (7 + kind[2]))
    pe, ne = DEFICIT_EDGES[kind[1]], DEFICIT_EDGES[kind[2]]
    return sum(1 << v for v in pe) | sum(1 << (7 + v) for v in ne)


LINE_PAIRS = tuple(combinations(range(8), 2))


def add_edge(rows: list[int], a: int, b: int) -> None:
    rows[a] |= 1 << b
    rows[b] |= 1 << a


def vector_from_edge_set(lines: tuple[int, ...], edges: Iterable[tuple[int, int]]) -> tuple[int, ...]:
    edge_set = frozenset(pair(a, b) for a, b in edges)
    return tuple(
        sum(pair(a, b) in edge_set for a in range(19) if (lines[i] >> a) & 1 for b in range(19) if a != b and (lines[j] >> b) & 1)
        for i, j in LINE_PAIRS
    )


def selected_caps_hold(edges: Iterable[tuple[int, int]]) -> bool:
    rows = adjacency(19, edges)
    for a, b in combinations(range(19), 2):
        limit = 1 if (rows[a] >> b) & 1 else 2
        if (rows[a] & rows[b]).bit_count() > limit:
            return False
    return True


@lru_cache(maxsize=None)
def abstract_solutions(case: Case) -> tuple[tuple[tuple[Kind, ...], tuple[tuple[int, int], ...]], ...]:
    h = case[0]
    blocks, incident = block_and_incidence(case)
    lines = tuple(blocks[i] | sum(1 << (14 + z) for z in incident[i]) for i in range(8))
    assert all(mask.bit_count() == 3 for mask in lines)

    mandatory = frozenset(
        pair(14 + a, 14 + b)
        for a, b in combinations(range(5), 2)
        if set(h[a]) & set(h[b])
    )
    optional = tuple(
        pair(14 + a, 14 + b)
        for a, b in combinations(range(5), 2)
        if not (set(h[a]) & set(h[b]))
    )
    base_edges = SUPPORT_EDGES | mandatory
    base_vector = vector_from_edge_set(lines, base_edges)
    target = tuple(4 if ij in h else POLAR[ij[0]][ij[1]] for ij in LINE_PAIRS)

    optional_vectors = tuple(vector_from_edge_set(lines, (edge,)) for edge in optional)
    optional_by_sum: dict[tuple[int, ...], list[tuple[tuple[int, int], ...]]] = defaultdict(list)
    for bits in range(1 << len(optional)):
        vector = tuple(
            sum(optional_vectors[k][r] for k in range(len(optional)) if (bits >> k) & 1)
            for r in range(len(LINE_PAIRS))
        )
        optional_by_sum[vector].append(tuple(optional[k] for k in range(len(optional)) if (bits >> k) & 1))

    requirements = tuple(blocks[i] | blocks[j] for i, j in h)
    candidates = tuple(tuple(kind for kind in column_kinds() if requirement & ~kind_mask(kind) == 0) for requirement in requirements)
    assert all(candidates)
    order = tuple(sorted(range(5), key=lambda z: (len(candidates[z]), z)))
    contributions = {
        (z, kind): vector_from_edge_set(lines, (pair(s, 14 + z) for s in range(14) if (kind_mask(kind) >> s) & 1))
        for z in range(5) for kind in candidates[z]
    }
    chosen: list[Kind | None] = [None] * 5
    used: Counter[Kind] = Counter()
    used_p: set[int] = set()
    used_n: set[int] = set()
    solutions = set()

    def visit(depth: int, vector: tuple[int, ...]) -> None:
        if any(vector[r] > target[r] for r in range(28)):
            return
        if depth == 5:
            need = tuple(target[r] - vector[r] for r in range(28))
            for extra in optional_by_sum.get(need, ()):
                edges = set(base_edges) | set(extra)
                for z, kind in enumerate(chosen):
                    assert kind is not None
                    edges.update(pair(s, 14 + z) for s in range(14) if (kind_mask(kind) >> s) & 1)
                if selected_caps_hold(edges):
                    solutions.add((tuple(kind for kind in chosen if kind is not None), tuple(sorted(extra))))
            return
        z = order[depth]
        for kind in candidates[z]:
            cap = 17 if kind[0] == 0 else 2 if kind[0] == 1 else 1
            if used[kind] >= cap:
                continue
            if kind[0] == 2 and (kind[1] in used_p or kind[2] in used_n):
                continue
            used[kind] += 1
            if kind[0] == 2:
                used_p.add(kind[1])
                used_n.add(kind[2])
            chosen[z] = kind
            delta = contributions[z, kind]
            visit(depth + 1, tuple(vector[r] + delta[r] for r in range(28)))
            chosen[z] = None
            if kind[0] == 2:
                used_p.remove(kind[1])
                used_n.remove(kind[2])
            used[kind] -= 1

    visit(0, base_vector)
    return tuple(sorted(solutions))


@lru_cache(maxsize=1)
def availability_masks() -> dict[tuple[int, ...], int]:
    matchings, residuals = deficit_configurations()
    result: dict[tuple[int, ...], int] = {(0,): (1 << len(matchings)) - 1}
    for pe in range(7):
        for ne in range(7):
            result[(2, pe, ne, 1)] = sum(1 << i for i, m in enumerate(matchings) if m[pe] == ne)
    for p in range(7):
        for n in range(7):
            for multiplicity in (1, 2):
                result[(1, p, n, multiplicity)] = sum(
                    1 << i for i, residual in enumerate(residuals) if residual[p][n] >= multiplicity
                )
    return result


def solution_mask(kinds: tuple[Kind, ...]) -> int:
    result = availability_masks()[(0,)]
    for kind, multiplicity in Counter(kinds).items():
        if kind[0] == 0:
            if multiplicity > 17:
                return 0
        else:
            result &= availability_masks()[(*kind, multiplicity)]
    return result


def concrete_columns_and_ids(matching_index: int) -> tuple[tuple[int, ...], dict[Kind, tuple[int, ...]]]:
    matching, residual = deficit_configurations()[0][matching_index], deficit_configurations()[1][matching_index]
    built = columns_for_matching(matching)
    assert built is not None
    columns = built[0]
    ids: dict[Kind, tuple[int, ...]] = {(2, pe, matching[pe]): (pe,) for pe in range(7)}
    cursor = 7
    for p in range(7):
        for n in range(7):
            count = residual[p][n]
            if count:
                ids[(1, p, n)] = tuple(range(cursor, cursor + count))
            cursor += count
    ids[(0,)] = tuple(range(cursor, 85))
    assert columns[cursor:] == (0,) * 17
    return columns, ids


def selected_local_extension(case: Case, solution: tuple[Kind, ...], optional: tuple[tuple[int, int], ...], matching_index: int) -> tuple[int, ...] | None:
    columns, ids = concrete_columns_and_ids(matching_index)
    used: Counter[Kind] = Counter()
    selected = []
    for kind in solution:
        selected.append(ids[kind][used[kind]])
        used[kind] += 1
    h = case[0]
    fixed = {
        pair(selected[a], selected[b])
        for a, b in combinations(range(5), 2)
        if set(h[a]) & set(h[b])
    }
    fixed.update(pair(selected[a - 14], selected[b - 14]) for a, b in optional)
    return local_one_factor_counts(columns, frozenset(fixed))


def indices(mask: int) -> Iterator[int]:
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


@lru_cache(maxsize=1)
def orbit_coupling() -> tuple[dict[str, object], ...]:
    result = []
    for orbit_index, orbit in enumerate(case_orbits()):
        representative = orbit[0]
        solutions = abstract_solutions(representative)
        union_mask = 0
        solution_rows = []
        assignment_branches = 0
        for solution, optional in solutions:
            mask = solution_mask(solution)
            union_mask |= mask
            assignment_branches += mask.bit_count()
            solution_rows.append((solution, optional, mask))
        final_mask = 0
        for matching_index in indices(union_mask):
            if any(
                ((mask >> matching_index) & 1)
                and selected_local_extension(representative, solution, optional, matching_index) is not None
                for solution, optional, mask in solution_rows
            ):
                final_mask |= 1 << matching_index
        result.append({
            "orbit_index": orbit_index,
            "representative": representative,
            "orbit_size": len(orbit),
            "abstract_solutions": len(solutions),
            "abstract_assignment_branches_per_representative": assignment_branches,
            "pre_local_matching_indices": tuple(indices(union_mask)),
            "final_matching_indices": tuple(indices(final_mask)),
        })
    assert len(result) == 33
    assert sum(bool(row["final_matching_indices"]) for row in result) == 3
    return tuple(result)


def transform_matching(matching: tuple[int, ...], action: GroupElement) -> tuple[int, ...]:
    _, support_map = action
    edge_index = {edge: i for i, edge in enumerate(DEFICIT_EDGES)}
    output: list[int | None] = [None] * 7
    for pe, ne in enumerate(matching):
        p_edge = tuple(support_map[v] for v in DEFICIT_EDGES[pe])
        n_edge = tuple(support_map[7 + v] for v in DEFICIT_EDGES[ne])
        mapped = (p_edge, n_edge)
        new_p = next(edge for edge in mapped if all(v < 7 for v in edge))
        new_n_global = next(edge for edge in mapped if all(v >= 7 for v in edge))
        new_pe = edge_index[pair(*new_p)]
        new_ne = edge_index[pair(*(v - 7 for v in new_n_global))]
        output[new_pe] = new_ne
    assert all(value is not None for value in output)
    answer = tuple(int(value) for value in output)
    assert is_perm(answer)
    return answer


@lru_cache(maxsize=1)
def expanded_survivors() -> tuple[set[Case], set[tuple[Case, tuple[int, ...]]]]:
    matchings = deficit_configurations()[0]
    accepted_cases: set[Case] = set()
    accepted_triples: set[tuple[Case, tuple[int, ...]]] = set()
    for row in orbit_coupling():
        matching_indices = row["final_matching_indices"]
        if not matching_indices:
            continue
        representative = row["representative"]
        assert isinstance(representative, tuple)
        for action in full_case_group():
            case = transform_case(representative, action)
            accepted_cases.add(case)
            for index in matching_indices:
                accepted_triples.add((case, transform_matching(matchings[index], action)))
    assert len(accepted_cases) == 1536
    assert len(accepted_triples) == 55_296
    return accepted_cases, accepted_triples


def survivor_summary() -> dict[str, object]:
    cases, triples = expanded_survivors()
    h_frequency = Counter(case[0] for case in cases)
    assert Counter(h_frequency.values()) == Counter({16: 96})

    def dtype(h: tuple[tuple[int, int], ...]) -> str:
        degree = [0] * 8
        for a, b in h:
            degree[a] += 1
            degree[b] += 1
        return f"P_{','.join(map(str, sorted(degree[:4], reverse=True)))}__N_{','.join(map(str, sorted(degree[4:], reverse=True)))}"

    types = Counter(dtype(h) for h in h_frequency)
    assert types == Counter({
        "P_3,1,1,0__N_2,2,1,0": 36,
        "P_2,2,1,0__N_3,1,1,0": 36,
        "P_2,2,1,0__N_2,2,1,0": 24,
    })
    triple_records = ((case, matching) for case, matching in triples)
    return {
        "labelled_H_before": len(marked_graphs()),
        "labelled_H_after": len(h_frequency),
        "labelled_cases_before": len(labelled_cases()),
        "labelled_cases_after": len(cases),
        "raw_triples": len(labelled_cases()) * len(deficit_configurations()[0]),
        "accepted_triples": len(triples),
        "packings_per_surviving_H": sorted(set(h_frequency.values())),
        "surviving_H_degree_types": dict(sorted(types.items())),
        "all_H_set": digest_records(marked_graphs()),
        "surviving_H_set": digest_records(h_frequency),
        "all_case_set": digest_records(labelled_cases()),
        "surviving_case_set": digest_records(cases),
        "accepted_triple_set": digest_records(triple_records),
    }


def requirement_patterns() -> tuple[tuple[tuple[int, ...], ...], ...]:
    answer = set()
    for case in labelled_cases():
        blocks, _ = block_and_incidence(case)
        answer.add(tuple(sorted(tuple(i for i in range(14) if ((blocks[a] | blocks[b]) >> i) & 1) for a, b in case[0])))
    assert len(answer) == 232
    return tuple(sorted(answer))


def transform_group_audit() -> dict[str, object]:
    polar = polar_automorphisms()
    support = support_automorphisms()
    polar_closure = group_closure_audit(polar)
    support_closure = group_closure_audit(support)
    full = full_case_group()
    line_support_pairs = set(full)
    identity = (tuple(range(8)), tuple(range(14)))
    assert identity in line_support_pairs

    # Closure/inverses of the actual 768 coupled transformations.
    def compose_action(a: GroupElement, b: GroupElement) -> GroupElement:
        return compose(a[0], b[0]), compose(a[1], b[1])

    assert all(compose_action(a, b) in line_support_pairs for a in full for b in full)
    assert all((inverse(a[0]), inverse(a[1])) in line_support_pairs for a in full)
    orbit_count, fixed = burnside_case_orbit_count()
    assert orbit_count == len(case_orbits()) == 33
    valid = set(deficit_configurations()[0])
    assert all(transform_matching(matching, action) in valid for matching in valid for action in full[::97])
    # Full closure follows from each support permutation preserving the seven
    # deficit edges; test all induced maps, and the sampled Cartesian action above.
    deficit_set = set(DEFICIT_EDGES)
    for auto in support:
        assert {pair(auto[a], auto[b]) for a, b in DEFICIT_EDGES} == deficit_set
    return {
        "polar_group": polar_closure,
        "support_graph_group": support_closure,
        "full_coupled_action_order": len(full),
        "full_action_closure": True,
        "full_action_inverses": True,
        "faithful_on_labelled_cases": action_is_faithful(),
        "burnside_fixed_point_sum": sum(fixed),
        "burnside_orbit_count": orbit_count,
        "case_orbit_size_distribution": dict(sorted(Counter(map(len, case_orbits())).items())),
        "all_labelled_cases_partitioned": sum(map(len, case_orbits())) == len(labelled_cases()),
        "deficit_bijections_closed_under_support_relabelling_and_sign_swap": True,
        "target_graph_automorphism_used": False,
    }


def validate_summary(payload: dict[str, object]) -> bool:
    s = payload["survivors"]
    assert isinstance(s, dict)
    return (
        s.get("labelled_H_before") == 204
        and s.get("labelled_H_after") == 96
        and s.get("labelled_cases_before") == 20_928
        and s.get("labelled_cases_after") == 1_536
        and s.get("raw_triples") == 93_757_440
        and s.get("accepted_triples") == 55_296
    )


def hostile_tests(payload: dict[str, object]) -> dict[str, object]:
    matching0 = deficit_configurations()[0][0]
    columns0 = columns_for_matching(matching0)
    assert columns0 is not None
    original_columns = columns0[0]

    mutated_columns = list(original_columns)
    bit = mutated_columns[0] & -mutated_columns[0]
    mutated_columns[0] ^= bit
    f_coordinate_rejected = observed_gram(tuple(mutated_columns)) != GRAM

    all_h = list(marked_graphs())
    h_digest = digest_records(all_h)
    deleted_h_rejected = digest_records(all_h[:-1]) != h_digest
    duplicated_h_rejected = digest_records(all_h + [all_h[0]]) != h_digest

    bad_support_perm = (1, 0, 2, 3, 4, 5, 6)
    corrupt_generator_rejected = frozenset(pair(bad_support_perm[a], bad_support_perm[b]) for a, b in ROOT_EDGES) != ROOT_EDGES

    rank_claim_rejected = integer_rank(GRAM) != 12

    bad_pair = next(
        pair(a, b) for a, b in combinations(range(85), 2)
        if (original_columns[a] & original_columns[b]).bit_count() >= 2
    )
    local_mutation_rejected = local_one_factor_counts(original_columns, frozenset({bad_pair})) is None

    altered = json.loads(json.dumps(payload))
    altered["survivors"]["accepted_triples"] = 55_295
    stored_result_mutation_rejected = not validate_summary(altered)

    triples = list(expanded_survivors()[1])
    triple_digest = digest_records(triples)
    deleted_triple_rejected = digest_records(triples[:-1]) != triple_digest

    checks = {
        "single_F_coordinate_mutation_rejected": f_coordinate_rejected,
        "deleted_labelled_H_rejected": deleted_h_rejected,
        "duplicated_labelled_H_rejected": duplicated_h_rejected,
        "corrupt_support_group_generator_rejected": corrupt_generator_rejected,
        "altered_rank_claim_rejected": rank_claim_rejected,
        "forced_incompatible_local_edge_rejected": local_mutation_rejected,
        "mutated_stored_result_rejected": stored_result_mutation_rejected,
        "deleted_accepted_triple_rejected": deleted_triple_rejected,
    }
    assert all(checks.values())
    return {"all_hostile_controls_rejected": True, "checks": checks}


def build_results() -> dict[str, object]:
    assert DEFICIT_EDGES == ((1, 4), (1, 5), (2, 3), (2, 6), (3, 5), (4, 6), (5, 6))
    assert len(support_partitions((3, 1, 1, 0))) == 4
    assert len(support_partitions((2, 2, 1, 0))) == 12
    assert len(requirement_patterns()) == 232
    f_audit = f_configuration_audit()
    symmetry = transform_group_audit()
    coupling = orbit_coupling()
    survivor = survivor_summary()
    assert survivor["raw_triples"] == 93_757_440
    assert survivor["accepted_triples"] == 55_296
    assert sum(row["orbit_size"] for row in coupling if row["final_matching_indices"]) == 1536
    assert [row["orbit_index"] for row in coupling if row["final_matching_indices"]] == [0, 4, 29]
    abstract_total = sum(
        row["orbit_size"] * row["abstract_assignment_branches_per_representative"]
        for row in coupling
    )
    assert abstract_total == 73_728
    payload: dict[str, object] = {
        "claim_label": "DERIVED",
        "global_status": "UNKNOWN",
        "scope": "conditional rank-three weight-14 selected-union coupling only",
        "labelled_enumeration": {
            "H": len(marked_graphs()),
            "ordered_H_packings": len(labelled_cases()),
            "containment_requirement_patterns": len(requirement_patterns()),
            "deficit_bijections": len(deficit_configurations()[0]),
            "raw_triples": len(labelled_cases()) * len(deficit_configurations()[0]),
        },
        "F_audit": f_audit,
        "symmetry_audit": symmetry,
        "orbit_coupling": [
            {
                "orbit_index": row["orbit_index"],
                "orbit_size": row["orbit_size"],
                "representative": row["representative"],
                "abstract_solutions": row["abstract_solutions"],
                "abstract_assignment_branches_per_representative": row["abstract_assignment_branches_per_representative"],
                "pre_local_matching_indices": row["pre_local_matching_indices"],
                "final_matching_indices": row["final_matching_indices"],
            }
            for row in coupling
        ],
        "surviving_case_orbits": [row["orbit_index"] for row in coupling if row["final_matching_indices"]],
        "abstract_assignment_branches": abstract_total,
        "survivors": survivor,
        "base_local_one_factor": base_local_census(),
        "outside_block_D": {
            "constructed": False,
            "excluded": False,
            "dimension": "85x85",
            "status": "unresolved",
        },
        "restrictions": {
            "all_H_labelled_before_quotient": True,
            "all_support_packings_ordered_and_labelled": True,
            "all_7_factorial_deficit_bijections_tested_before_capacity_filter": True,
            "only_proved_polar_and_fixed_support_graph_actions_used": True,
            "target_graph_automorphism_assumed": False,
            "global_completion_search_performed": False,
        },
    }
    assert validate_summary(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        print(json.dumps({
            "H": len(marked_graphs()),
            "cases": len(labelled_cases()),
            "deficits": list(DEFICIT_EDGES),
            "F_configurations": len(deficit_configurations()[0]),
            "polar_group": len(polar_automorphisms()),
            "support_group": len(support_automorphisms()),
            "case_orbits": len(case_orbits()),
        }, sort_keys=True))
        return
    payload = build_results()
    hostile = hostile_tests(payload)
    if args.write:
        RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        HOSTILE_PATH.write_text(json.dumps(hostile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", RESULT_PATH, HOSTILE_PATH)
    elif args.verify:
        assert json.loads(RESULT_PATH.read_text(encoding="utf-8")) == payload
        assert json.loads(HOSTILE_PATH.read_text(encoding="utf-8")) == hostile
        print("independent verification PASS")
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
