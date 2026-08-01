#!/usr/bin/env python3
"""Clean-room verifier for the sealed Wave 208 marked-M7g proof-B package.

No discovery module is imported.  The only discovery artifact read here is
the pair of explicit local candidate controls, which are replayed as
certificates rather than trusted as results.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import independent_m7g_norm as gf3  # noqa: E402

Q = 3
ARCHIVE = HERE / "proof-b-independent-results.json"
CONTROL_PATH = ROOT / "attempts" / "wave208-marked-m7g-proof-b" / "local-controls.json"
VECTORS = (
    (1, 2, 2, 2),
    (1, 0, 2, 2),
    (1, 2, 0, 2),
    (1, 2, 2, 0),
    (1, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
)
ALLOWED_WEIGHTS = {14, 17, 20, 23}


def normalize_projective(vector: tuple[int, ...]) -> tuple[int, ...]:
    first = next(value for value in vector if value % Q)
    scale = 1 if first % Q == 1 else 2
    return tuple(scale * value % Q for value in vector)


def weight_eight_linear_relations() -> list[tuple[int, ...]]:
    rows = [[VECTORS[column][row] for column in range(8)] for row in range(4)]
    basis = gf3.nullspace(rows)
    words = set()
    for coefficients in product(range(Q), repeat=len(basis)):
        word = tuple(
            sum(coefficients[i] * basis[i][j] for i in range(len(basis))) % Q
            for j in range(8)
        )
        if all(word):
            words.add(normalize_projective(word))
    return sorted(words)


def tensor_relations() -> list[tuple[int, ...]]:
    rows = []
    for i in range(4):
        for j in range(i, 4):
            rows.append([VECTORS[k][i] * VECTORS[k][j] % Q for k in range(8)])
    return [word for word in weight_eight_linear_relations() if all(sum(row[k] * word[k] for k in range(8)) % Q == 0 for row in rows)]


def projective_line(left: tuple[int, ...], right: tuple[int, ...]) -> frozenset[tuple[int, ...]]:
    points = set()
    for a, b in product(range(Q), repeat=2):
        vector = tuple((a * left[i] + b * right[i]) % Q for i in range(4))
        if any(vector):
            points.add(normalize_projective(vector))
    if len(points) != 4:
        raise AssertionError("selected pair does not span a projective line")
    return frozenset(points)


def perfect_matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [tuple()]
    first = vertices[0]
    rows = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for suffix in perfect_matchings(rest):
            rows.append(((first, second),) + suffix)
    return rows


def concurrent_secant_matchings() -> list[dict[str, object]]:
    rows = []
    for matching in perfect_matchings(tuple(range(8))):
        common = set(projective_line(VECTORS[matching[0][0]], VECTORS[matching[0][1]]))
        for left, right in matching[1:]:
            common &= projective_line(VECTORS[left], VECTORS[right])
        if common:
            if len(common) != 1:
                raise AssertionError("secants have non-unique concurrency")
            rows.append(
                {
                    "pairs": [list(pair) for pair in matching],
                    "point": list(next(iter(common))),
                }
            )
    return rows


def form_space() -> list[list[list[int]]]:
    evaluations = [gf3.symmetric_evaluation_row(vector) for vector in VECTORS]
    basis = gf3.nullspace(evaluations)
    if len(basis) != 3:
        raise AssertionError("vanishing form space is not three-dimensional")
    forms = []
    for coefficients in product(range(Q), repeat=3):
        coordinates = [
            sum(coefficients[i] * basis[i][j] for i in range(3)) % Q
            for j in range(10)
        ]
        form = gf3.symmetric_matrix(coordinates)
        if any(gf3.dot_form(vector, form, vector) for vector in VECTORS):
            raise AssertionError("form does not vanish on the eight-set")
        forms.append(form)
    if len({tuple(form[i][i] for i in (1, 2, 3)) for form in forms}) != 27:
        raise AssertionError("lower diagonal does not label all forms")
    return forms


def components(edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    adjacency = [set() for _ in range(8)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(range(8))
    rows = []
    while unseen:
        stack = [min(unseen)]
        unseen.remove(stack[0])
        row = []
        while stack:
            vertex = stack.pop()
            row.append(vertex)
            for neighbor in sorted(adjacency[vertex] & unseen):
                unseen.remove(neighbor)
                stack.append(neighbor)
        rows.append(sorted(row))
    return sorted(rows)


def point_memberships(selected: tuple[tuple[int, int], ...]) -> list[tuple[int, ...]]:
    memberships: list[tuple[int, ...]] = [tuple(edge) for edge in selected]
    incidences = [0] * 8
    for left, right in selected:
        incidences[left] += 1
        incidences[right] += 1
    if any(value > 3 for value in incidences):
        raise AssertionError("a selected triangle has more than three intersection points")
    for index, value in enumerate(incidences):
        memberships.extend([(index,)] * (3 - value))
    return memberships


def marked_profile(
    ones_edges: tuple[tuple[int, int], ...], signs: tuple[int, ...]
) -> tuple[dict[str, int], dict[str, int], int]:
    refined: Counter[tuple[int, int, int, int, int, int, int]] = Counter()
    coarse: Counter[tuple[int, int, int, int]] = Counter()
    accepted = 0
    for mask in range(1 << len(ones_edges)):
        selected = tuple(edge for bit, edge in enumerate(ones_edges) if mask & (1 << bit))
        memberships = point_memberships(selected)
        h_value = sum(signs[left] * signs[right] for left, right in selected)
        if h_value % Q != 1:
            continue
        integer_values = [sum(signs[index] for index in membership) for membership in memberships]
        residues = [value % Q for value in integer_values]
        weight = sum(value != 0 for value in residues)
        if weight not in ALLOWED_WEIGHTS:
            continue
        positive = residues.count(1)
        negative = residues.count(2)
        if weight == 14 and (positive, negative) != (7, 7):
            continue
        same = sum(signs[left] == signs[right] for left, right in selected)
        opposite = len(selected) - same
        norm = sum(value * value for value in integer_values)
        refined[(len(selected), same, opposite, weight, positive, negative, norm)] += 1
        coarse[(same, opposite, weight, len(selected))] += 1
        accepted += 1
    refined_rows = {
        f"m{m}_same{same}_opposite{opposite}_w{weight}_p{positive}_n{negative}_norm{norm}": count
        for (m, same, opposite, weight, positive, negative, norm), count in sorted(refined.items())
    }
    coarse_rows = {
        f"same{same}_opposite{opposite}_w{weight}_m{m}": count
        for (same, opposite, weight, m), count in sorted(coarse.items())
    }
    return refined_rows, coarse_rows, accepted


def form_census(signs: tuple[int, ...]) -> dict[str, object]:
    distribution: Counter[int] = Counter()
    no_one = 0
    form_rows = []
    minus_profiles = []
    plus_profiles = []
    for form in form_space():
        gram = [[gf3.dot_form(left, form, right) for right in VECTORS] for left in VECTORS]
        ones = tuple((i, j) for i, j in combinations(range(8), 2) if gram[i][j] == 1)
        if not ones:
            no_one += 1
        signed_sum = sum(signs[i] * signs[j] * gram[i][j] for i, j in combinations(range(8), 2))
        distribution[signed_sum] += 1
        residual_norm = 7 * (24 - 2 * signed_sum)
        if residual_norm % 9:
            continue
        refined, coarse, accepted = marked_profile(ones, signs)
        diagonal = [form[i][i] for i in (1, 2, 3)]
        rank = gf3.rank_mod3(form)
        degrees = [sum(vertex in edge for edge in ones) for vertex in range(8)]
        graph_components = components(ones)
        if signed_sum == -24:
            if sorted(degrees) != [2] * 8 or sorted(map(len, graph_components)) != [4, 4]:
                raise AssertionError("rank-four product-one graph is not 2C4")
            minus_profiles.append(refined)
        elif signed_sum == 12:
            plus = set(range(4))
            minus = set(range(4, 8))
            if any((left in plus) == (right in plus) for left, right in ones):
                raise AssertionError("rank-three product-one edge has equal signs")
            if sorted(degrees) != [3] * 8:
                raise AssertionError("rank-three graph is not K4,4 minus a matching")
            plus_profiles.append(refined)
        else:
            raise AssertionError("unexpected divisible residual")
        form_rows.append(
            {
                "diagonal": diagonal,
                "rank": rank,
                "signed_polar_sum": signed_sum,
                "residual_squared_norm": residual_norm,
                "divided_residual_squared_norm": residual_norm // 9,
                "product_one_edges": len(ones),
                "same_sign_product_one_edges": sum(signs[i] == signs[j] for i, j in ones),
                "product_one_component_sizes": sorted(map(len, graph_components)),
                "accepted_labelled_intersection_subsets": accepted,
                "coarse_profile": coarse,
            }
        )
    if distribution != Counter({-24: 3, -12: 4, 0: 19, 12: 1}):
        raise AssertionError("signed polar distribution differs")
    if no_one != 4:
        raise AssertionError("Wave207 no-product-one count differs")
    if len(form_rows) != 4 or len(minus_profiles) != 3 or len(plus_profiles) != 1:
        raise AssertionError("four-form residual differs")
    if any(profile != minus_profiles[0] for profile in minus_profiles[1:]):
        raise AssertionError("rank-four marked profiles differ")
    minus_coarse = next(row.pop("coarse_profile") for row in form_rows if row["signed_polar_sum"] == -24)
    plus_coarse = next(row.pop("coarse_profile") for row in form_rows if row["signed_polar_sum"] == 12)
    for row in form_rows:
        row.pop("coarse_profile", None)
    divisibility_excluded = sum(count for value, count in distribution.items() if (7 * (24 - 2 * value)) % 9)
    return {
        "signed_polar_sum_distribution": {str(key): distribution[key] for key in sorted(distribution)},
        "wave207_no_product_one_forms": no_one,
        "divisibility_excluded_forms": divisibility_excluded,
        "additional_wave207_survivors_excluded": divisibility_excluded - no_one,
        "surviving_forms": sorted(form_rows, key=lambda row: tuple(row["diagonal"])),
        "minus24_intersection_profiles": minus_profiles[0],
        "minus24_coarse_profile": minus_coarse,
        "plus12_intersection_profiles": plus_profiles[0],
        "plus12_coarse_profile": plus_coarse,
    }


def graph_metrics(vertex_count: int, edges: set[tuple[int, int]]) -> dict[str, object]:
    degrees = [sum(vertex in edge for edge in edges) for vertex in range(vertex_count)]
    common_histogram: Counter[str] = Counter()
    for left, right in combinations(range(vertex_count), 2):
        common = sum(
            tuple(sorted((left, vertex))) in edges and tuple(sorted((right, vertex))) in edges
            for vertex in range(vertex_count)
            if vertex not in (left, right)
        )
        adjacent = (left, right) in edges
        if common > (1 if adjacent else 2):
            raise AssertionError("local lambda/mu cap fails")
        common_histogram[f"{'edge' if adjacent else 'nonedge'}_{common}"] += 1
    triangles = [
        triple
        for triple in combinations(range(vertex_count), 3)
        if all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2))
    ]
    prism_count = 0
    for left, right in combinations(triangles, 2):
        if set(left) & set(right):
            continue
        cross = [(u, v) for u in left for v in right if tuple(sorted((u, v))) in edges]
        if len(cross) == 3 and len({u for u, _ in cross}) == 3 and len({v for _, v in cross}) == 3:
            prism_count += 1
    return {
        "maximum_degree": max(degrees),
        "common_neighbor_histogram": dict(sorted(common_histogram.items())),
        "graph_triangles": len(triangles),
        "triangular_prisms": prism_count,
    }


def replay_controls(signs: tuple[int, ...], canonical_gram: list[list[int]]) -> list[dict[str, object]]:
    payload = json.loads(CONTROL_PATH.read_text(encoding="utf-8"))
    rows = []
    for candidate in payload["controls"]:
        triangles = [tuple(row) for row in candidate["triangles"]]
        vertex_count = max(max(row) for row in triangles) + 1
        if len(triangles) != 8 or any(len(set(row)) != 3 for row in triangles):
            raise AssertionError("bad selected triangle list")
        intersections = {
            (i, j) for i, j in combinations(range(8), 2) if set(triangles[i]) & set(triangles[j])
        }
        if intersections != {tuple(row) for row in candidate["selected_triangle_intersections"]}:
            raise AssertionError("declared intersections differ")
        if any(len(set(triangles[i]) & set(triangles[j])) != 1 for i, j in intersections):
            raise AssertionError("selected triangles share multiple points")
        internal = {tuple(sorted(edge)) for triangle in triangles for edge in combinations(triangle, 2)}
        extra = {tuple(sorted(edge)) for edge in candidate["extra_edges"]}
        if internal & extra or any(left == right for left, right in extra):
            raise AssertionError("bad extra edge list")
        edges = internal | extra
        for i, j in combinations(range(8), 2):
            cross_count = sum(
                left != right and tuple(sorted((left, right))) in edges
                for left in triangles[i]
                for right in triangles[j]
            )
            expected = 4 if (i, j) in intersections else canonical_gram[i][j]
            if cross_count != expected:
                raise AssertionError("selected-pair cross count differs")
        memberships = [
            tuple(index for index, triangle in enumerate(triangles) if vertex in triangle)
            for vertex in range(vertex_count)
        ]
        b_values = [sum(signs[index] for index in membership) for membership in memberships]
        if b_values != candidate["b_integer"]:
            raise AssertionError("candidate point image differs")
        neighbor_sums = [
            sum(b_values[other] for other in range(vertex_count) if tuple(sorted((vertex, other))) in edges)
            for vertex in range(vertex_count)
        ]
        if neighbor_sums != [3 * value for value in b_values]:
            raise AssertionError("internal eigenvector equation fails")
        metrics = graph_metrics(vertex_count, edges)
        if metrics["maximum_degree"] > 14 or metrics["triangular_prisms"]:
            raise AssertionError("local graph cap fails")

        # Hostile one-row extension: a new zero-coordinate vertex adjacent to
        # exactly one nonzero coordinate preserves all internal equations and
        # local upper caps, but violates the omitted outside equation M b=0.
        witness_neighbor = next(index for index, value in enumerate(b_values) if value)
        extended_edges = set(edges)
        extended_edges.add((witness_neighbor, vertex_count))
        extended_metrics = graph_metrics(vertex_count + 1, extended_edges)
        outside_value = b_values[witness_neighbor]
        if outside_value == 0 or extended_metrics["maximum_degree"] > 14:
            raise AssertionError("outside hostile witness failed")
        rows.append(
            {
                "name": candidate["name"],
                "vertices": vertex_count,
                "outside_vertices_missing": 99 - vertex_count,
                "edges": len(edges),
                "selected_intersections": len(intersections),
                "point_weight": sum(value % Q != 0 for value in b_values),
                "integer_b_norm": sum(value * value for value in b_values),
                "graph_triangles": metrics["graph_triangles"],
                "maximum_induced_degree": metrics["maximum_degree"],
                "induced_triangular_prisms": metrics["triangular_prisms"],
                "exact_AUb_equals_3b": True,
                "lambda_mu_caps": True,
                "hostile_outside_row_dot_b": outside_value,
                "hostile_extension_preserves_upper_caps": True,
                "full_outside_equation_implied": False,
                "global_completion_implied": False,
            }
        )
    return rows


def build_result() -> dict[str, object]:
    linear = weight_eight_linear_relations()
    tensor = tensor_relations()
    if len(linear) != 4 or tensor != [(1, 1, 1, 1, 2, 2, 2, 2)]:
        raise AssertionError("linear/tensor relation distinction fails")
    matchings = concurrent_secant_matchings()
    if len(matchings) != 4:
        raise AssertionError("concurrent-secant matching count differs")
    signs = tuple(1 if value == 1 else -1 for value in tensor[0])
    census = form_census(signs)
    canonical = next(form for form in form_space() if [form[i][i] for i in (1, 2, 3)] == [2, 2, 2])
    canonical_gram = [[gf3.dot_form(left, canonical, right) for right in VECTORS] for left in VECTORS]
    controls = replay_controls(signs, canonical_gram)

    # Symbolic SRG calculation on the zero-sum space:
    # (A+4I)(A-3I)=A^2+A-12I=2J, so r=(A-3I)b is a -4 eigenvector.
    # Its norm is 7(3||b||^2-b^TAb)=7(24-2S_D).
    return {
        "source_code_imported": False,
        "projective_linear_weight_eight_relations": [list(row) for row in linear],
        "projective_linear_weight_eight_relation_classes": len(linear),
        "projective_tensor_weight_eight_relations": [list(row) for row in tensor],
        "projective_tensor_weight_eight_relation_classes": len(tensor),
        "concurrent_secant_matchings": matchings,
        "concurrent_secant_matching_count": len(matchings),
        "relation_matching_objects_identified": False,
        "spectral_identity": {
            "residual": "r=(A-3I)b_integer",
            "annihilator_on_zero_sum": "(A+4I)(A-3I)=0",
            "residual_eigenvalue": -4,
            "coordinate_divisor_from_Ab_mod3": 3,
            "norm": "7*(24-2*S_D)",
            "necessary_congruence": "S_D=3 mod 9",
        },
        **census,
        "local_controls": controls,
        "full_outside_equations_supplied": False,
        "full_99_vertex_completion_supplied": False,
        "complete_graph_certificate": False,
        "complete_nonexistence_certificate": False,
        "global_status": "UNKNOWN",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build_result()
    if args.verify:
        expected = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError("independent proof-B archive differs")
        print("PASS: independent Wave208 proof-B reconstruction")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
