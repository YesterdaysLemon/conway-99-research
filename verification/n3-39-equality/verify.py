#!/usr/bin/env python3
"""Exact finite checks for the Wave 11 exclusion of ``n3 = 39``.

The human proof supplies the reduction from a putative ``srg(99,14,1,2)``
to thirteen active graph-triangles.  On those triangles ``L`` is the side
graph and ``K`` is explicitly the simple complement of ``L``.  This compact,
standard-library checker replays the finite arithmetic and every local branch
of the repaired point-incidence proof.

It is a regression companion to a conditional proof, not a standalone
nonexistence certificate for the Conway graph.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from typing import Sequence


ACTIVE_ORDER = 13
K_DEGREE = 6
K_EDGE_COUNT = ACTIVE_ORDER * K_DEGREE // 2
WAVE6_BRANCH_DEGREES = (4, 8, 10, 12, 12, 6, 10, 12, 8, 12, 10, 12)


def active_q_sequences(n3_count: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate active-q multisets from the Wave 7 handshake constraints."""

    if n3_count < 0 or (2 * n3_count) % 3:
        raise ValueError("2*n3 must be a nonnegative multiple of three")
    q_sum = 2 * n3_count // 3
    results: list[tuple[int, ...]] = []

    def visit(remaining: int, least: int, values: tuple[int, ...]) -> None:
        if remaining == 0:
            active_count = len(values)
            if values and all(3 * value <= active_count - 1 for value in values):
                results.append(values)
            return
        for value in range(least, min(12, remaining) + 1):
            visit(remaining - value, value, (*values, value))

    visit(q_sum, 2, ())
    return tuple(results)


def k_degree_profile(q_values: Sequence[int]) -> tuple[int, ...]:
    """Return degrees in ``K = complement(L[active])``."""

    active_count = len(q_values)
    return tuple(active_count - 1 - 3 * value for value in q_values)


def forced_singletons_at_triangle(k_degree: int) -> int:
    """Three nonempty point cliques compete for distinct incident K-edges."""

    if k_degree < 0:
        raise ValueError("K-degree must be nonnegative")
    return max(0, 3 - k_degree)


def crossing_masks(left_order: int, right_order: int) -> tuple[int, ...]:
    """Enumerate simple bipartite masks with every degree in ``{0,2}``."""

    if left_order < 0 or right_order < 0:
        raise ValueError("crossing orders must be nonnegative")
    bit_count = left_order * right_order
    if bit_count > 20:
        raise ValueError("direct crossing enumeration is intentionally local")
    accepted = []
    for mask in range(1 << bit_count):
        left_degrees = [0] * left_order
        right_degrees = [0] * right_order
        for left in range(left_order):
            for right in range(right_order):
                if mask >> (left * right_order + right) & 1:
                    left_degrees[left] += 1
                    right_degrees[right] += 1
        if all(value in (0, 2) for value in (*left_degrees, *right_degrees)):
            accepted.append(mask)
    return tuple(accepted)


def crossing_edge_counts(left_order: int, right_order: int) -> frozenset[int]:
    return frozenset(mask.bit_count() for mask in crossing_masks(left_order, right_order))


def local_point_types(k_degree: int = K_DEGREE) -> tuple[tuple[int, int, int], ...]:
    """Enumerate sorted sizes of the three point sets through one triangle."""

    if k_degree < 3:
        raise ValueError("three non-singleton point sets need degree at least three")
    return tuple(
        sizes
        for sizes in combinations_with_replacement(range(2, k_degree + 2), 3)
        if sum(size - 1 for size in sizes) <= k_degree
    )


def forbidden_common_point_triple(point_sets: Sequence[frozenset[int]]) -> bool:
    """Detect a Berge triangle of three distinct linear point sets."""

    if len(point_sets) != 3 or len(set(point_sets)) != 3:
        raise ValueError("three distinct point sets are required")
    intersections = [
        point_sets[left] & point_sets[right]
        for left, right in combinations(range(3), 2)
    ]
    return all(len(item) == 1 for item in intersections) and len(set().union(*intersections)) == 3


def expansion_bound(point_size: int) -> tuple[int, int, bool]:
    """Return available vertices, required external representatives, feasibility."""

    if not 2 <= point_size <= ACTIVE_ORDER:
        raise ValueError("active point size must lie between two and thirteen")
    available = ACTIVE_ORDER - point_size
    required = 2 * point_size
    return available, required, required <= available


def point_resource_profiles() -> tuple[tuple[int, int, int], ...]:
    """Enumerate size-2/3/4 incidence profiles before local elimination."""

    profiles = []
    for x4 in range(10):
        for x3 in range(14):
            for x2 in range(20):
                if 2 * x2 + 3 * x3 + 4 * x4 != 3 * ACTIVE_ORDER:
                    continue
                consumed = x2 + 3 * x3 + 6 * x4
                if consumed <= K_EDGE_COUNT:
                    profiles.append((x2, x3, x4))
    return tuple(profiles)


def flower_crossing_extensions(root_size: int, petals: Sequence[int]) -> int:
    """Count all local degree-{0,2} crossing choices for an ordered flower."""

    if len(petals) % 2:
        raise ValueError("petals must occur in pairs")
    root_external = root_size - 1
    count = 1
    for offset in range(0, len(petals), 2):
        left_external = petals[offset] - 1
        right_external = petals[offset + 1] - 1
        count *= len(crossing_masks(root_external, left_external))
        count *= len(crossing_masks(root_external, right_external))
        count *= len(crossing_masks(left_external, right_external))
    return count


def size_four_flower_statistics() -> dict[str, int]:
    """Exhaust all ordered petal-size profiles around a size-four point."""

    total = 0
    capacity_rejections = 0
    feasible = 0
    minimum_224 = 4
    crossing_extensions = 0
    minimum_root_degree = ACTIVE_ORDER
    for petals in product((2, 3, 4), repeat=8):
        total += 1
        external_slots = sum(size - 1 for size in petals)
        if external_slots > ACTIVE_ORDER - 4:
            capacity_rejections += 1
            continue
        feasible += 1
        type_224 = sum(
            petals[offset] == petals[offset + 1] == 2
            for offset in range(0, 8, 2)
        )
        minimum_224 = min(minimum_224, type_224)
        extensions = flower_crossing_extensions(4, petals)
        crossing_extensions += extensions
        # Two 224 occurrences give four pairwise-distinct external endpoints.
        root_degree_lower = (4 - 1) + 2 * min(2, type_224)
        minimum_root_degree = min(minimum_root_degree, root_degree_lower)
        if type_224 < 3 or root_degree_lower <= K_DEGREE:
            raise AssertionError("a size-four flower escaped its degree contradiction")
    return {
        "total_profiles": total,
        "capacity_rejections": capacity_rejections,
        "feasible_profiles": feasible,
        "minimum_type_224_occurrences": minimum_224,
        "crossing_extensions": crossing_extensions,
        "minimum_root_degree_lower": minimum_root_degree,
    }


def u_degree(size_three_points: int) -> int:
    """Degree in ``U=K-F`` after point-clique edges are removed."""

    if not 0 <= size_three_points <= 3:
        raise ValueError("a triangle has between zero and three size-three points")
    return K_DEGREE - (3 + size_three_points)


def size_three_flower_statistics() -> dict[str, int]:
    """Exhaust all ordered size-2/3 petals around a size-three point."""

    classifications = Counter()
    extension_totals = Counter()
    total = 0
    for petals in product((2, 3), repeat=6):
        total += 1
        external_slots = sum(size - 1 for size in petals)
        if external_slots > ACTIVE_ORDER - 3:
            classifications["capacity"] += 1
            continue

        pairs = tuple((petals[offset], petals[offset + 1]) for offset in range(0, 6, 2))
        extensions = flower_crossing_extensions(3, petals)
        if any(left != right for left, right in pairs):
            # At a 233 occurrence, the size-two mate has four forced U-neighbors.
            if 4 <= max(u_degree(value) for value in range(4)):
                raise AssertionError("the type-233 U-degree contradiction disappeared")
            classifications["type_233"] += 1
            extension_totals["type_233"] += extensions
            continue

        type_223 = sum(pair == (2, 2) for pair in pairs)
        type_333 = 3 - type_223
        violating_roots = []
        for index, pair in enumerate(pairs):
            petal_size_three_count = sum(size == 3 for size in pair)
            capacity = 2 - petal_size_three_count
            forced = 2 * (type_223 - int(pair == (2, 2)))
            if forced > capacity:
                violating_roots.append(index)
        if not violating_roots:
            raise AssertionError(
                f"a 223/333 root pattern survived: petals={petals}, types={(type_223, type_333)}"
            )
        classifications["root_u_degree"] += 1
        extension_totals["root_u_degree"] += extensions

    return {
        "total_profiles": total,
        "capacity_rejections": classifications["capacity"],
        "type_233_rejections": classifications["type_233"],
        "root_u_degree_rejections": classifications["root_u_degree"],
        "type_233_crossing_extensions": extension_totals["type_233"],
        "root_u_crossing_extensions": extension_totals["root_u_degree"],
        "feasible_crossing_extensions": sum(extension_totals.values()),
    }


def ceil_multiple_of_three(value: int) -> int:
    return 3 * ((value + 2) // 3)


def verify() -> None:
    q39 = active_q_sequences(39)
    expected_q39 = (
        (2,) * 13,
        (2,) * 10 + (3, 3),
        (2,) * 7 + (3,) * 4,
        (2,) * 4 + (3,) * 6,
    )
    if q39 != expected_q39:
        raise AssertionError(f"unexpected n3=39 active profiles: {q39}")

    degree_profiles = tuple(k_degree_profile(profile) for profile in q39)
    expected_histograms = (
        Counter({6: 13}),
        Counter({5: 10, 2: 2}),
        Counter({4: 7, 1: 4}),
        Counter({3: 4, 0: 6}),
    )
    if tuple(Counter(profile) for profile in degree_profiles) != expected_histograms:
        raise AssertionError("wrong K-degree profiles")
    mixed_forced_singletons = tuple(
        sum(forced_singletons_at_triangle(degree) for degree in profile if degree < 3)
        for profile in degree_profiles[1:]
    )
    if mixed_forced_singletons != (2, 8, 18):
        raise AssertionError("mixed-profile singleton count changed")

    point_types = local_point_types()
    expected_types = (
        (2, 2, 2),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 5),
        (2, 3, 3),
        (2, 3, 4),
        (3, 3, 3),
    )
    if point_types != expected_types:
        raise AssertionError(f"wrong local point types: {point_types}")
    singleton_crossings = {
        right: crossing_edge_counts(1, right)
        for right in range(1, 5)
    }
    if singleton_crossings != {right: frozenset((0,)) for right in range(1, 5)}:
        raise AssertionError("a singleton-side crossing survived")

    bounds = tuple(expansion_bound(size) for size in range(2, ACTIVE_ORDER + 1))
    if tuple(size for size, bound in zip(range(2, ACTIVE_ORDER + 1), bounds, strict=True) if bound[2]) != (2, 3, 4):
        raise AssertionError("the expansion bound changed")

    resource_profiles = point_resource_profiles()
    if len(resource_profiles) != 20 or not all(profile[1] % 2 for profile in resource_profiles):
        raise AssertionError("point resource profiles changed")

    size4 = size_four_flower_statistics()
    expected_size4 = {
        "total_profiles": 6_561,
        "capacity_rejections": 6_552,
        "feasible_profiles": 9,
        "minimum_type_224_occurrences": 3,
        "crossing_extensions": 33,
        "minimum_root_degree_lower": 7,
    }
    if size4 != expected_size4:
        raise AssertionError(f"size-four flower census changed: {size4}")

    if tuple(u_degree(value) for value in range(4)) != (3, 2, 1, 0):
        raise AssertionError("F/U degree table changed")
    size3 = size_three_flower_statistics()
    expected_size3 = {
        "total_profiles": 64,
        "capacity_rejections": 7,
        "type_233_rejections": 50,
        "root_u_degree_rejections": 7,
        "type_233_crossing_extensions": 700,
        "root_u_crossing_extensions": 217,
        "feasible_crossing_extensions": 917,
    }
    if size3 != expected_size3:
        raise AssertionError(f"size-three flower census changed: {size3}")

    if (ACTIVE_ORDER * 3) % 2 != 1:
        raise AssertionError("the all-size-two parity contradiction disappeared")

    branch_bounds = tuple(
        max(42, ceil_multiple_of_three(4 * degree))
        for degree in WAVE6_BRANCH_DEGREES
    )
    expected_branch_bounds = (42, 42, 42, 48, 48, 42, 42, 48, 42, 48, 42, 48)
    if branch_bounds != expected_branch_bounds:
        raise AssertionError(f"wrong Wave 11 branch bounds: {branch_bounds}")

    print("PASS n3=39 equality exclusion arithmetic")
    print("active_q_n3_39", [list(profile) for profile in q39])
    print("K_degree_histograms", [dict(sorted(item.items())) for item in expected_histograms])
    print("mixed_forced_singletons", list(mixed_forced_singletons))
    print("local_point_types", [list(profile) for profile in point_types])
    print("point_resource_profiles", len(resource_profiles))
    print("size4_flower_statistics", size4)
    print("size3_flower_statistics", size3)
    print("global_n3_lower_bound", 42)
    print("global_p6_lower_bound", 209_286 + 42)
    print("branch_n3_bounds", list(branch_bounds))
    print("target_result", "UNKNOWN")


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise ValueError("this checker takes no arguments")
    verify()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
