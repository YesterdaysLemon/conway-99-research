#!/usr/bin/env python3
"""Canonical perfect-matching branches for one rooted endpoint fiber.

For the Conway model, a fiber S_u has 12 residual vertices naturally grouped
by six fixed scaffold pairs. Perfect matchings on S_u have exactly 11 orbits
under C2 wreath S6, indexed by integer partitions of 6.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Iterator, Sequence

from root_model import RootModel


Matching = tuple[tuple[int, int], ...]


def integer_partitions(total: int, maximum: int | None = None) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def perfect_matchings(vertices: tuple[int, ...]) -> Iterator[Matching]:
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for rest in perfect_matchings(remainder):
            yield ((first, second),) + rest


def canonical_matching(partition: Sequence[int]) -> Matching:
    """Build a representative whose union with fixed pairs has this cycle type."""

    if not partition or any(type(part) is not int or part < 1 for part in partition):
        raise ValueError("partition must contain positive integers")
    if tuple(partition) != tuple(sorted(partition, reverse=True)):
        raise ValueError("partition must be in nonincreasing order")

    matching: list[tuple[int, int]] = []
    pair_offset = 0
    for part in partition:
        if part == 1:
            matching.append((2 * pair_offset, 2 * pair_offset + 1))
        else:
            component_pairs = list(range(pair_offset, pair_offset + part))
            for index, pair in enumerate(component_pairs):
                next_pair = component_pairs[(index + 1) % part]
                matching.append((2 * pair + 1, 2 * next_pair))
        pair_offset += part

    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def matching_type(matching: Sequence[tuple[int, int]], pair_count: int) -> tuple[int, ...]:
    """Return component sizes after contracting the fixed matching pairs."""

    vertices = set(range(2 * pair_count))
    used: set[int] = set()
    pair_graph = [set() for _ in range(pair_count)]
    loops: set[int] = set()

    for raw_left, raw_right in matching:
        left, right = sorted((raw_left, raw_right))
        if left not in vertices or right not in vertices or left == right:
            raise ValueError("matching contains an invalid endpoint")
        if left in used or right in used:
            raise ValueError("matching reuses an endpoint")
        used.update((left, right))
        first_pair, second_pair = left // 2, right // 2
        if first_pair == second_pair:
            loops.add(first_pair)
        else:
            pair_graph[first_pair].add(second_pair)
            pair_graph[second_pair].add(first_pair)

    if used != vertices:
        raise ValueError("matching does not cover every endpoint")

    components: list[int] = []
    seen: set[int] = set()
    for start in range(pair_count):
        if start in seen:
            continue
        if start in loops:
            if pair_graph[start]:
                raise ValueError("invalid matching component mixes a loop and other edges")
            seen.add(start)
            components.append(1)
            continue
        stack = [start]
        size = 0
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            size += 1
            stack.extend(pair_graph[current] - seen)
        components.append(size)

    return tuple(sorted(components, reverse=True))


def orbit_type_counts(pair_count: int = 6) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings(tuple(range(2 * pair_count))):
        counts[matching_type(matching, pair_count)] += 1
    return counts


def endpoint_generators(pair_count: int) -> tuple[tuple[int, ...], ...]:
    """Generators for the automorphism group of the fixed endpoint matching."""

    identity = tuple(range(2 * pair_count))
    generators: list[tuple[int, ...]] = []
    for pair in range(pair_count):
        permutation = list(identity)
        permutation[2 * pair], permutation[2 * pair + 1] = (
            permutation[2 * pair + 1],
            permutation[2 * pair],
        )
        generators.append(tuple(permutation))
    for pair in range(pair_count - 1):
        permutation = list(identity)
        left = 2 * pair
        right = left + 2
        permutation[left], permutation[right] = permutation[right], permutation[left]
        permutation[left + 1], permutation[right + 1] = (
            permutation[right + 1],
            permutation[left + 1],
        )
        generators.append(tuple(permutation))
    return tuple(generators)


def permute_matching(matching: Matching, permutation: Sequence[int]) -> Matching:
    return tuple(
        sorted(
            tuple(sorted((permutation[left], permutation[right])))
            for left, right in matching
        )
    )


def orbit_sizes_via_generators(pair_count: int = 6) -> dict[tuple[int, ...], int]:
    """Exhaustively compute matching orbits under C2 wreath S_pair_count."""

    unseen = set(perfect_matchings(tuple(range(2 * pair_count))))
    generators = endpoint_generators(pair_count)
    sizes: dict[tuple[int, ...], int] = {}

    while unseen:
        representative = min(unseen)
        orbit = {representative}
        frontier = [representative]
        while frontier:
            current = frontier.pop()
            for generator in generators:
                image = permute_matching(current, generator)
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        unseen.difference_update(orbit)
        orbit_type = matching_type(representative, pair_count)
        if orbit_type in sizes:
            raise AssertionError(f"matching type {orbit_type} splits into multiple orbits")
        sizes[orbit_type] = len(orbit)

    return sizes


def parse_partition(text: str, expected_sum: int) -> tuple[int, ...]:
    try:
        parts = tuple(int(part) for part in text.replace(",", "+").split("+") if part)
    except ValueError as exc:
        raise ValueError(f"invalid partition {text!r}") from exc
    if not parts or sum(parts) != expected_sum:
        raise ValueError(f"partition must sum to {expected_sum}")
    parts = tuple(sorted(parts, reverse=True))
    return parts


def canonical_branch_decisions(
    root: RootModel, coordinate: int, partition: Sequence[int]
) -> dict[tuple[int, int], bool]:
    """Fix all edges inside S_coordinate to one canonical matching."""

    expected_sum = root.pair_count - 1
    if sum(partition) != expected_sum:
        raise ValueError(f"partition must sum to {expected_sum}")
    fiber = root.containing(coordinate)
    if len(fiber) != 2 * expected_sum:
        raise AssertionError("unexpected endpoint-fiber size")

    # Order fiber vertices by their other endpoint. This places scaffold mates
    # consecutively, so positions (0,1), (2,3), ... form the fixed matching.
    other_endpoint_and_label: list[tuple[int, int]] = []
    for label_index in fiber:
        label = root.labels[label_index]
        other = label[1] if label[0] == coordinate else label[0]
        other_endpoint_and_label.append((other, label_index))
    ordered_fiber = [
        label_index for _, label_index in sorted(other_endpoint_and_label)
    ]

    representative = canonical_matching(tuple(sorted(partition, reverse=True)))
    true_edges = {
        tuple(sorted((ordered_fiber[left], ordered_fiber[right])))
        for left, right in representative
    }
    return {
        tuple(sorted((first, second))): tuple(sorted((first, second))) in true_edges
        for first, second in combinations(ordered_fiber, 2)
    }


def summary(pair_count: int = 6) -> dict[str, Any]:
    counts = orbit_type_counts(pair_count)
    generator_orbits = orbit_sizes_via_generators(pair_count)
    if dict(counts) != generator_orbits:
        raise AssertionError("matching types do not agree with generated group orbits")
    return {
        "format": "fiber-matching-orbits-v1",
        "pair_count": pair_count,
        "matching_count": sum(counts.values()),
        "orbit_count": len(counts),
        "orbits": [
            {
                "partition": list(partition),
                "labeled_matchings": counts[partition],
                "generated_orbit_size": generator_orbits[partition],
                "representative": [list(edge) for edge in canonical_matching(partition)],
            }
            for partition in sorted(counts, reverse=True)
        ],
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-count", type=int, default=6)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = summary(args.pair_count)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
