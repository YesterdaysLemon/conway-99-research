"""Clean-room exact checks for the Wave 207 verifier.

This file deliberately does not import either Wave 207 discovery module.  It
uses the M7g representative printed in Kaipa--Pradhan arXiv:2405.12011 and
plain finite-field linear algebra over F_3.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence


P = 3
HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "independent-results.json"
ROOT = HERE.parents[1]
LOCAL_CERTIFICATE = (
    ROOT / "attempts" / "wave207-m7g-incidence-bridge" / "local-rank4-certificate.json"
)


def transpose(matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix, strict=True)]


def matmul(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> list[list[int]]:
    if not left or not right:
        return []
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right))) % P
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matvec(matrix: Sequence[Sequence[int]], vector: Sequence[int]) -> tuple[int, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) % P for row in matrix)


def rref(matrix: Sequence[Sequence[int]]) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    work = [[entry % P for entry in row] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = 1 if work[pivot_row][column] == 1 else 2
        work[pivot_row] = [(scale * value) % P for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][j] - factor * work[pivot_row][j]) % P
                for j in range(len(work[0]))
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivot_columns


def rank(matrix: Sequence[Sequence[int]]) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    if not matrix:
        return []
    reduced, pivots = rref(matrix)
    free = [column for column in range(len(matrix[0])) if column not in pivots]
    basis: list[tuple[int, ...]] = []
    for free_column in free:
        vector = [0] * len(matrix[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % P
        basis.append(tuple(vector))
    return basis


def matrix_from_columns(columns: Sequence[Sequence[int]]) -> list[list[int]]:
    return transpose(columns)


def linear_combination(
    basis: Sequence[Sequence[int]], coefficients: Sequence[int]
) -> tuple[int, ...]:
    if not basis:
        return ()
    return tuple(
        sum(coefficients[i] * basis[i][j] for i in range(len(basis))) % P
        for j in range(len(basis[0]))
    )


def projective_normalize(vector: Sequence[int]) -> tuple[int, ...]:
    if not any(vector):
        raise ValueError("zero vector is not projective")
    first = next(value % P for value in vector if value % P)
    scale = 1 if first == 1 else 2
    return tuple(scale * value % P for value in vector)


def projective_points(dimension: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            projective_normalize(vector)
            for vector in product(range(P), repeat=dimension)
            if any(vector)
        }
    )


def veronese(vector: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        vector[i] * vector[j] % P
        for i in range(len(vector))
        for j in range(i, len(vector))
    )


def published_m7g_original() -> tuple[list[tuple[int, ...]], tuple[int, ...], list[tuple[int, int]]]:
    """Return a line-paired M7g representative from arXiv:2405.12011.

    Independent column signs are then chosen so its unique quadratic
    relation is also a true linear relation.  Projective points are unchanged.
    """

    points = [
        (1, 0, 0, 0),
        (1, 0, 0, 1),
        (0, 1, 0, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
        (1, 1, 1, 2),
    ]
    tensor_relation = (1, 2, 1, 2, 1, 2, 2, 1)
    pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
    return points, tensor_relation, pairs


def linearizing_sign_classes(
    projective_points_: Sequence[Sequence[int]], tensor_relation: Sequence[int]
) -> list[tuple[int, ...]]:
    matrix_columns = len(projective_points_)
    classes: list[tuple[int, ...]] = []
    for signs in product((1, 2), repeat=matrix_columns):
        if signs[0] != 1:
            continue
        signed = [
            tuple(signs[i] * coordinate % P for coordinate in point)
            for i, point in enumerate(projective_points_)
        ]
        if not any(matvec(matrix_from_columns(signed), tensor_relation)):
            classes.append(signs)
    return classes


def published_m7g() -> tuple[list[tuple[int, ...]], tuple[int, ...], list[tuple[int, int]], tuple[int, ...]]:
    points, tensor_relation, pairs = published_m7g_original()
    sign_classes = linearizing_sign_classes(points, tensor_relation)
    if len(sign_classes) != 4:
        raise AssertionError("M7g did not have four relative linearizing sign classes")
    column_signs = sign_classes[0]
    signed_points = [
        tuple(column_signs[i] * value % P for value in point)
        for i, point in enumerate(points)
    ]
    return signed_points, tensor_relation, pairs, column_signs


def vector_relation_words(columns: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    matrix = matrix_from_columns(columns)
    return [
        word
        for word in product(range(P), repeat=len(columns))
        if not any(matvec(matrix, word))
    ]


def perfect_matchings(vertices: tuple[int, ...]) -> Iterable[tuple[tuple[int, int], ...]]:
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second), *matching)


def line_contains(
    point: Sequence[int], left: Sequence[int], right: Sequence[int]
) -> bool:
    return rank(matrix_from_columns([left, right, point])) <= 2


def no_three_lines_coplanar(
    columns: Sequence[Sequence[int]],
    common_point: Sequence[int],
    matching: Sequence[tuple[int, int]],
) -> bool:
    for triple in combinations(matching, 3):
        witnesses = [columns[pair[0]] for pair in triple]
        if rank(matrix_from_columns([common_point, *witnesses])) < 4:
            return False
    return True


def concurrency_audit(
    columns: Sequence[Sequence[int]], expected_pairs: Sequence[tuple[int, int]]
) -> dict[str, object]:
    projective_support = {projective_normalize(column) for column in columns}
    candidates = projective_points(4)
    valid: list[tuple[tuple[tuple[int, int], ...], tuple[int, ...]]] = []
    for matching in perfect_matchings(tuple(range(8))):
        intersections = [
            point
            for point in candidates
            if all(line_contains(point, columns[i], columns[j]) for i, j in matching)
        ]
        for point in intersections:
            if point in projective_support:
                continue
            if no_three_lines_coplanar(columns, point, matching):
                valid.append((matching, point))
    expected_normalized = {tuple(sorted(pair)) for pair in expected_pairs}
    recovered_matchings = [
        {tuple(sorted(pair)) for pair in matching} for matching, _point in valid
    ]
    return {
        "projective_points_checked": len(candidates),
        "perfect_matchings_checked": 105,
        "valid_external_concurrent_matchings": len(valid),
        "each_matching_has_a_unique_common_point": all(
            sum(
                all(line_contains(point, columns[i], columns[j]) for i, j in matching)
                for point in candidates
            )
            == 1
            for matching, _point in valid
        ),
        "expected_source_pairing_is_recovered": expected_normalized in recovered_matchings,
        "valid_matchings": [
            {
                "pairs": [list(pair) for pair in matching],
                "external_point": list(point),
            }
            for matching, point in valid
        ],
        "all_valid_matchings_have_no_three_secants_coplanar": all(
            no_three_lines_coplanar(columns, point, matching)
            for matching, point in valid
        ),
        "note": (
            "M7g is the unique surviving projective orbit, but this labelled "
            "eight-set has four valid concurrent-secant decompositions"
        ),
    }


def quadratic_evaluation_row(vector: Sequence[int]) -> list[int]:
    row: list[int] = []
    for i in range(4):
        for j in range(i, 4):
            coefficient = vector[i] * vector[j]
            if i != j:
                coefficient *= 2
            row.append(coefficient % P)
    return row


def symmetric_matrix(coordinates: Sequence[int], dimension: int) -> list[list[int]]:
    matrix = [[0] * dimension for _ in range(dimension)]
    cursor = 0
    for i in range(dimension):
        for j in range(i, dimension):
            matrix[i][j] = matrix[j][i] = coordinates[cursor] % P
            cursor += 1
    return matrix


def bilinear(
    left: Sequence[int], form: Sequence[Sequence[int]], right: Sequence[int]
) -> int:
    return sum(
        left[i] * form[i][j] * right[j]
        for i in range(len(left))
        for j in range(len(right))
    ) % P


def graph_signature(adjacency: Sequence[set[int]]) -> dict[str, object]:
    unseen = set(range(len(adjacency)))
    components: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        unseen.remove(seed)
        component: list[int] = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in sorted(adjacency[vertex] & unseen):
                unseen.remove(neighbor)
                stack.append(neighbor)
        components.append(sorted(component))
    degrees = sorted(len(neighbors) for neighbors in adjacency)
    edge_count = sum(degrees) // 2
    component_sizes = sorted(len(component) for component in components)
    key = (edge_count, tuple(component_sizes), tuple(degrees))
    names = {
        (28, (8,), (7,) * 8): "K8",
        (12, (4, 4), (3,) * 8): "2K4",
        (4, (2, 2, 2, 2), (1,) * 8): "4K2",
        (8, (4, 4), (2,) * 8): "2C4",
    }
    if key not in names:
        raise AssertionError(f"unexpected graph signature: {key}")
    return {
        "name": names[key],
        "edges": edge_count,
        "component_sizes": component_sizes,
        "degrees": degrees,
    }


def polar_net_audit(columns: Sequence[Sequence[int]]) -> dict[str, object]:
    evaluations = [quadratic_evaluation_row(column) for column in columns]
    basis = nullspace(evaluations)
    if len(basis) != 3:
        raise AssertionError("M7g polar net did not have dimension three")
    rank_counts: Counter[int] = Counter()
    graph_counts: Counter[str] = Counter()
    graph_details: dict[str, dict[str, object]] = {}
    for coefficients in product(range(P), repeat=3):
        form_coordinates = linear_combination(basis, coefficients)
        form = symmetric_matrix(form_coordinates, 4)
        if any(bilinear(column, form, column) for column in columns):
            raise AssertionError("polar-net form failed to vanish on M7g")
        form_rank = rank(form)
        rank_counts[form_rank] += 1
        adjacency = [set() for _ in columns]
        for i, j in combinations(range(len(columns)), 2):
            if bilinear(columns[i], form, columns[j]) == 0:
                adjacency[i].add(j)
                adjacency[j].add(i)
        signature = graph_signature(adjacency)
        graph_counts[signature["name"]] += 1
        graph_details[signature["name"]] = signature
    projective_rank_counts = {
        str(form_rank): count // 2
        for form_rank, count in sorted(rank_counts.items())
        if form_rank
    }
    return {
        "form_space_dimension": len(basis),
        "affine_forms": 27,
        "rank_counts": {str(key): rank_counts[key] for key in sorted(rank_counts)},
        "projective_nonzero_rank_counts": projective_rank_counts,
        "zero_graph_counts": dict(sorted(graph_counts.items())),
        "zero_graph_details": dict(sorted(graph_details.items())),
    }


def no_one_polar_forms(columns: Sequence[Sequence[int]]) -> dict[str, int]:
    evaluations = [quadratic_evaluation_row(column) for column in columns]
    basis = nullspace(evaluations)
    counts: Counter[int] = Counter()
    for coefficients in product(range(P), repeat=len(basis)):
        form = symmetric_matrix(linear_combination(basis, coefficients), 4)
        off_diagonal = [
            bilinear(columns[i], form, columns[j])
            for i, j in combinations(range(len(columns)), 2)
        ]
        if 1 not in off_diagonal:
            counts[rank(form)] += 1
    return {str(key): counts[key] for key in sorted(counts)}


def m7g_audit() -> dict[str, object]:
    columns, tensor_relation, pairs, column_signs = published_m7g()
    original_points, _relation_again, _pairs_again = published_m7g_original()
    sign_classes = linearizing_sign_classes(original_points, tensor_relation)
    no_one_by_sign_class = []
    for signs in sign_classes:
        signed = [
            tuple(signs[i] * coordinate % P for coordinate in point)
            for i, point in enumerate(original_points)
        ]
        no_one_by_sign_class.append(
            {
                "signs": list(signs),
                "no_one_offdiagonal_forms_by_rank": no_one_polar_forms(signed),
            }
        )
    column_matrix = matrix_from_columns(columns)
    veronese_matrix = matrix_from_columns([veronese(column) for column in columns])
    tensor_kernel = nullspace(veronese_matrix)
    words = vector_relation_words(columns)
    weights = Counter(sum(value != 0 for value in word) for word in words)
    every_three_independent = all(
        rank(matrix_from_columns([columns[i] for i in subset])) == 3
        for subset in combinations(range(8), 3)
    )
    linear_zero = not any(matvec(column_matrix, tensor_relation))
    tensor_zero = not any(matvec(veronese_matrix, tensor_relation))
    if len(tensor_kernel) != 1:
        raise AssertionError("quadratic relation was not unique")
    return {
        "source_representative": "Kaipa--Pradhan arXiv:2405.12011 M7g",
        "columns": [list(column) for column in columns],
        "chosen_relative_column_signs": list(column_signs),
        "linearizing_relative_sign_classes": len(sign_classes),
        "no_one_offdiagonal_audit_by_sign_class": no_one_by_sign_class,
        "tensor_relation": list(tensor_relation),
        "tensor_relation_composition": {
            "1": tensor_relation.count(1),
            "2": tensor_relation.count(2),
        },
        "column_rank": rank(column_matrix),
        "every_three_independent": every_three_independent,
        "veronese_rank": rank(veronese_matrix),
        "quadratic_relation_nullity": 8 - rank(veronese_matrix),
        "displayed_relation_is_linear": linear_zero,
        "displayed_relation_is_quadratic": tensor_zero,
        "concurrency": concurrency_audit(columns, pairs),
        "linear_relation_code": {
            "dimension": 8 - rank(column_matrix),
            "words": len(words),
            "weight_enumerator": {str(key): weights[key] for key in sorted(weights)},
        },
        "polar_net": polar_net_audit(columns),
    }


def symmetric_coordinates(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    return tuple(
        matrix[i][j] % P
        for i in range(len(matrix))
        for j in range(i, len(matrix))
    )


def symmetric_basis(dimension: int) -> list[list[list[int]]]:
    basis: list[list[list[int]]] = []
    for i in range(dimension):
        for j in range(i, dimension):
            matrix = [[0] * dimension for _ in range(dimension)]
            matrix[i][j] = 1
            matrix[j][i] = 1
            basis.append(matrix)
    return basis


def congruence_map_rank(cross: Sequence[Sequence[int]]) -> int:
    source_dimension = len(cross[0])
    columns = []
    for feature in symmetric_basis(source_dimension):
        image = matmul(matmul(cross, feature), transpose(cross))
        columns.append(symmetric_coordinates(image))
    return rank(matrix_from_columns(columns))


def transition_rank_audit() -> dict[str, object]:
    square: dict[str, int] = {}
    for cross_rank in range(7):
        cross = [
            [1 if i == j and i < cross_rank else 0 for j in range(6)]
            for i in range(6)
        ]
        actual = congruence_map_rank(cross)
        expected = cross_rank * (cross_rank + 1) // 2
        if actual != expected:
            raise AssertionError((cross_rank, actual, expected))
        square[str(cross_rank)] = actual
    rectangular_cases = []
    for rows, columns, cross_rank in ((4, 6, 3), (6, 4, 3), (3, 7, 2)):
        cross = [
            [1 if i == j and i < cross_rank else 0 for j in range(columns)]
            for i in range(rows)
        ]
        actual = congruence_map_rank(cross)
        rectangular_cases.append(
            {
                "shape": [rows, columns],
                "rank_C": cross_rank,
                "symmetric_transition_rank": actual,
                "expected": cross_rank * (cross_rank + 1) // 2,
            }
        )
    return {
        "square_6_by_6_ranks": square,
        "rectangular_edge_cases": rectangular_cases,
        "formula": "rank(S -> C S C^T)=rank(C)*(rank(C)+1)/2 over F3",
    }


def vector_span(columns: Sequence[Sequence[int]]) -> set[tuple[int, ...]]:
    if not columns:
        return {()}
    dimension = len(columns[0])
    return {
        tuple(
            sum(coefficients[j] * columns[j][i] for j in range(len(columns))) % P
            for i in range(dimension)
        )
        for coefficients in product(range(P), repeat=len(columns))
    }


def gram_radical_exhaustion() -> dict[str, object]:
    ambient_form = [[1, 0], [0, 2]]
    checked = 0
    radical_example = None
    for entries in product(range(P), repeat=6):
        synthesis = [list(entries[:3]), list(entries[3:])]
        gram = matmul(matmul(transpose(synthesis), ambient_form), synthesis)
        kernel_gram = [
            vector
            for vector in product(range(P), repeat=3)
            if not any(matvec(gram, vector))
        ]
        kernel_synthesis = [
            vector
            for vector in product(range(P), repeat=3)
            if not any(matvec(synthesis, vector))
        ]
        feature_columns = [tuple(column) for column in transpose(synthesis)]
        feature_span = vector_span(feature_columns)
        radical = {
            vector
            for vector in feature_span
            if not any(
                bilinear(vector, ambient_form, feature)
                for feature in feature_span
            )
        }
        image_of_gram_kernel = {matvec(synthesis, vector) for vector in kernel_gram}
        if image_of_gram_kernel != radical:
            raise AssertionError("Gram-kernel image did not equal the feature radical")
        if len(kernel_gram) != len(kernel_synthesis) * len(radical):
            raise AssertionError("short exact sequence cardinalities failed")
        if radical_example is None and len(radical) > 1 and rank(synthesis) > rank(gram):
            radical_example = {
                "synthesis": synthesis,
                "synthesis_rank": rank(synthesis),
                "gram": gram,
                "gram_rank": rank(gram),
                "kernel_synthesis_size": len(kernel_synthesis),
                "kernel_gram_size": len(kernel_gram),
                "radical_size": len(radical),
            }
        checked += 1
    return {
        "synthesis_maps_exhausted": checked,
        "ambient_form": ambient_form,
        "exact_sequence_checked": True,
        "sequence": "0 -> ker(R) -> ker(R^T H R) -> rad(im R) -> 0",
        "nontrivial_radical_example": radical_example,
    }


def standard_basis(dimension: int, index: int) -> tuple[int, ...]:
    return tuple(1 if coordinate == index else 0 for coordinate in range(dimension))


def add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple((left[i] + right[i]) % P for i in range(len(left)))


def symmetric_square_span_columns(space: Sequence[Sequence[int]]) -> list[tuple[int, ...]]:
    dimension = len(space[0])
    output: list[tuple[int, ...]] = []
    for i in range(len(space)):
        for j in range(i, len(space)):
            matrix = [[0] * dimension for _ in range(dimension)]
            for row in range(dimension):
                for column in range(dimension):
                    if i == j:
                        value = space[i][row] * space[i][column]
                    else:
                        value = (
                            space[i][row] * space[j][column]
                            + space[j][row] * space[i][column]
                        )
                    matrix[row][column] = value % P
            output.append(symmetric_coordinates(matrix))
    return output


def restriction_map_rank(graphs: Sequence[Sequence[Sequence[int]]]) -> int:
    columns: list[tuple[int, ...]] = []
    for p_index in range(5):
        for q_index in range(5):
            outputs: list[int] = []
            for graph in graphs:
                k_matrix = [[0] * 5 for _ in range(5)]
                k_matrix[p_index][q_index] = 1
                left = matmul(k_matrix, graph)
                right = matmul(transpose(graph), transpose(k_matrix))
                total = [
                    [(left[i][j] + right[i][j]) % P for j in range(5)]
                    for i in range(5)
                ]
                outputs.extend(symmetric_coordinates(total))
            columns.append(tuple(outputs))
    return rank(matrix_from_columns(columns))


def four_center_control() -> dict[str, object]:
    ell = standard_basis(11, 0)
    u = [standard_basis(11, 1 + index) for index in range(5)]
    w = [standard_basis(11, 6 + index) for index in range(5)]
    identity = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
    companion = [
        [0, 0, 0, 0, 2],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    spaces: list[list[tuple[int, ...]]] = [
        [ell, *u],
        [ell, *w],
        [ell, *[add(u[index], w[index]) for index in range(5)]],
    ]
    fourth = [ell]
    for column in range(5):
        graph_vector = tuple(
            sum(companion[row][column] * w[row][coordinate] for row in range(5)) % P
            for coordinate in range(11)
        )
        fourth.append(add(u[column], graph_vector))
    spaces.append(fourth)

    accumulated: list[tuple[int, ...]] = []
    cumulative: list[int] = []
    for space in spaces:
        accumulated.extend(symmetric_square_span_columns(space))
        cumulative.append(rank(matrix_from_columns(accumulated)))
    local_gram_ranks = []
    for space in spaces:
        gram = [
            [sum(x * y for x, y in zip(left, right, strict=True)) % P for right in space]
            for left in space
        ]
        local_gram_ranks.append(rank(gram))
    return {
        "cumulative_symmetric_square_ranks": cumulative,
        "restriction_rank_on_25_K_coordinates": restriction_map_rank(
            [identity, companion]
        ),
        "local_six_space_gram_ranks": local_gram_ranks,
        "scope": "abstract four-space control only; not endpoint data",
    }


def point_code_supplement() -> dict[str, object]:
    allowed_weights = [weight for weight in range(1, 25) if weight % 3 == 2]
    return {
        "hypothesis": "hypothetical wt(a)=8 A_Delta word with four 1s and four 2s",
        "sum_a_mod3": 0,
        "sum_c_mod3_from_B1_equals_1": 0,
        "a_dot_a_mod3": 8 % P,
        "b_dot_b_mod3_from_G_squared_equals_G_minus_J": 2,
        "b_is_nonzero": True,
        "allowed_weights_at_most_24": allowed_weights,
        "sharpened_weight_upper": max(allowed_weights),
        "rank_zero_K8_case": {
            "D_restriction_zero_forces": "eight pairwise disjoint anticomplete triangles",
            "then_weight_b": 24,
            "then_b_dot_b_mod3": 24 % P,
            "contradicts_required_b_dot_b_mod3": 2,
            "verdict": "EXCLUDED_CONDITIONALLY",
        },
        "no_one_offdiagonal_extension": {
            "identity": "b.b=a^T(B_S^T B_S)a=2*sum_intersections(a_i*a_j)=2",
            "intersection_requires_restricted_gram_value": 1,
            "excluded_affine_forms_per_relative_sign_class": {
                "rank_0": 1,
                "rank_2": 3,
            },
            "relative_sign_classes_checked": 4,
            "verdict": "EXCLUDED_CONDITIONALLY",
        },
    }


def signed_neighbor_distance_audit() -> dict[str, object]:
    """Recompute the parameter-only ``d(ker A) >= 12`` certificate.

    This is deliberately independent of the Wave 207 discovery checker.  The
    only inputs are ``(v,k,lambda,mu)=(99,14,1,2)`` and the congruence
    ``i_v == j_v (mod 3)`` for a signed word in ``ker_F3(A)``.
    """

    def choose_two(value: int) -> int:
        return value * (value - 1) // 2

    def base_function(i_value: int, j_value: int) -> int:
        return (
            choose_two(i_value)
            + choose_two(j_value)
            + 2 * i_value * j_value
            - i_value
            - j_value
        )

    base_table = [
        {"i": i_value, "j": j_value, "F": base_function(i_value, j_value)}
        for i_value in range(15)
        for j_value in range(15)
        if (i_value - j_value) % P == 0
    ]
    if any(entry["F"] < 0 for entry in base_table):
        raise AssertionError("the signed-neighbor base function became negative")

    low_weight_bounds = []
    for weight in range(1, 10):
        maximum_product = (weight // 2) * (weight - weight // 2)
        upper = weight * weight + 2 * maximum_product
        if not upper < 15 * weight:
            raise AssertionError("the base inequality did not exclude a low weight")
        low_weight_bounds.append(
            {"weight": weight, "required": 15 * weight, "upper": upper}
        )

    weight_ten_compositions = []
    for positive in range(11):
        negative = 10 - positive
        if (positive - negative) % P == 0:
            weight_ten_compositions.append(
                {
                    "positive": positive,
                    "negative": negative,
                    "upper": 100 + 2 * positive * negative,
                }
            )
    survivors = [
        item
        for item in weight_ten_compositions
        if item["upper"] >= 15 * 10
    ]
    if survivors != [{"positive": 5, "negative": 5, "upper": 150}]:
        raise AssertionError("unexpected weight-ten composition survivor")
    zero_types = sorted(
        (i_value, j_value)
        for i_value in range(15)
        for j_value in range(15)
        if (i_value - j_value) % P == 0 and base_function(i_value, j_value) == 0
    )
    if zero_types != [(0, 0), (0, 3), (1, 1), (3, 0)]:
        raise AssertionError("unexpected equality cases in the base inequality")
    if 5 * 4 % 3 == 0:
        raise AssertionError("weight-ten common-neighbor contradiction disappeared")

    def phi(membership: str, i_value: int, j_value: int) -> int:
        value = (
            -12 * i_value
            + 8 * j_value
            + 12 * choose_two(i_value)
            - 6 * choose_two(j_value)
            + 4 * i_value * j_value
        )
        if membership == "P":
            value += 6 * i_value + 4 * j_value
        elif membership == "N":
            value += 3 - 3 * j_value
        return value

    ranges = {"P": (6, 4), "N": (7, 3), "O": (7, 4)}
    phi_tables: dict[str, list[dict[str, int]]] = {}
    for membership, (maximum_i, maximum_j) in ranges.items():
        table = [
            {
                "i": i_value,
                "j": j_value,
                "Phi": phi(membership, i_value, j_value),
            }
            for i_value in range(maximum_i + 1)
            for j_value in range(maximum_j + 1)
            if (i_value - j_value) % P == 0
        ]
        if any(entry["Phi"] < 0 for entry in table):
            raise AssertionError(f"negative weight-eleven Phi value in {membership}")
        phi_tables[membership] = table

    positive, negative = 7, 4
    global_farkas_sum = (
        3 * negative
        - 12 * 14 * positive
        + 8 * 14 * negative
        + 12 * positive * (positive - 1)
        - 6 * negative * (negative - 1)
        + 8 * positive * negative
    )
    if global_farkas_sum != -60:
        raise AssertionError("weight-eleven Farkas sum changed")

    return {
        "scope": "parameter-only for any hypothetical srg(99,14,1,2)",
        "moment_identities": {
            "sum_i": "14p",
            "sum_j": "14n",
            "sum_choose_i_2": "p(p-1)-e_P",
            "sum_choose_j_2": "n(n-1)-e_N",
            "sum_i_j": "2pn-e_PN",
        },
        "base_function_nonnegative_on_all_neighbor_ranges": True,
        "base_table_entries_checked": len(base_table),
        "weights_1_through_9": low_weight_bounds,
        "weight_10": {
            "admissible_compositions": weight_ten_compositions,
            "only_inequality_survivor": [5, 5],
            "base_equality_types": [list(item) for item in zero_types],
            "same_sign_common_neighbor_sum": 20,
            "contradiction_modulo_3": True,
        },
        "weight_11": {
            "hard_composition_up_to_global_sign": [7, 4],
            "phi_tables": phi_tables,
            "all_phi_values_nonnegative": True,
            "global_farkas_sum": global_farkas_sum,
            "contradiction": True,
        },
        "derived_minimum_distance_lower_bound": 12,
        "not_proved": [
            "existence of a weight-12 word",
            "d(ker_F3 A)>=24",
            "classification at weight 24",
        ],
    }


def weight_fourteen_aggregate_control_audit() -> dict[str, object]:
    """Validate the submitted aggregate control, while rejecting it as a graph."""

    records = [
        ("P", 0, 0, 0, 0, 0, 5),
        ("P", 6, 0, 3, 0, 0, 2),
        ("N", 0, 0, 0, 0, 0, 5),
        ("N", 0, 6, 0, 1, 0, 1),
        ("N", 0, 6, 0, 3, 0, 1),
        ("O", 0, 0, 0, 0, 0, 3),
        ("O", 1, 1, 0, 0, 0, 80),
        ("O", 3, 3, 0, 1, 0, 2),
    ]

    for _, i_value, j_value, h_pp, h_nn, h_pn, _ in records:
        p_singles = i_value - 2 * h_pp - h_pn
        n_singles = j_value - 2 * h_nn - h_pn
        occupied_pairs = h_pp + h_nn + h_pn + p_singles + n_singles
        if min(h_pp, h_nn, h_pn, p_singles, n_singles) < 0 or occupied_pairs > 7:
            raise AssertionError("submitted local 7K2 record is infeasible")
        if (i_value - j_value) % P:
            raise AssertionError("submitted record violates the ternary check")

    def total(index: int, membership: str | None = None) -> int:
        return sum(
            record[6] * record[index]
            for record in records
            if membership is None or record[0] == membership
        )

    category_counts = {
        membership: sum(record[6] for record in records if record[0] == membership)
        for membership in ("P", "N", "O")
    }
    sum_i = total(1)
    sum_j = total(2)
    e_positive = total(1, "P") // 2
    e_negative = total(2, "N") // 2
    e_cross_from_positive = total(2, "P")
    e_cross_from_negative = total(1, "N")
    choose_i = sum(
        count * i_value * (i_value - 1) // 2
        for _, i_value, _, _, _, _, count in records
    )
    choose_j = sum(
        count * j_value * (j_value - 1) // 2
        for _, _, j_value, _, _, _, count in records
    )
    sum_ij = sum(
        count * i_value * j_value
        for _, i_value, j_value, _, _, _, count in records
    )
    matching_totals = {
        "h_pp": total(3),
        "h_nn": total(4),
        "h_pn": total(5),
    }
    expected = {
        "category_counts": {"P": 7, "N": 7, "O": 85},
        "sum_i": 98,
        "sum_j": 98,
        "e_positive": 6,
        "e_negative": 6,
        "e_cross": 0,
        "choose_i": 36,
        "choose_j": 36,
        "sum_ij": 98,
        "matching_totals": {"h_pp": 6, "h_nn": 6, "h_pn": 0},
    }
    actual = {
        "category_counts": category_counts,
        "sum_i": sum_i,
        "sum_j": sum_j,
        "e_positive": e_positive,
        "e_negative": e_negative,
        "e_cross": e_cross_from_positive,
        "choose_i": choose_i,
        "choose_j": choose_j,
        "sum_ij": sum_ij,
        "matching_totals": matching_totals,
    }
    if e_cross_from_positive != e_cross_from_negative or actual != expected:
        raise AssertionError("weight-fourteen aggregate identities failed")

    positive_degrees = sorted(
        i_value
        for membership, i_value, _, _, _, _, count in records
        if membership == "P"
        for _ in range(count)
    )
    negative_degrees = sorted(
        j_value
        for membership, _, j_value, _, _, _, count in records
        if membership == "N"
        for _ in range(count)
    )
    if positive_degrees != [0, 0, 0, 0, 0, 6, 6] or negative_degrees != positive_degrees:
        raise AssertionError("declared nongraphical obstruction changed")
    return {
        "transcribed_candidate_records": len(records),
        "aggregate_identities": actual,
        "all_local_7K2_records_feasible": True,
        "positive_internal_degree_multiset": positive_degrees,
        "negative_internal_degree_multiset": negative_degrees,
        "nongraphical_reason": (
            "a degree-six vertex must meet all six peers, contradicting the five "
            "declared degree-zero peers"
        ),
        "is_graph": False,
        "is_codeword": False,
        "evidentiary_status": "hostile stopping control only",
    }


def local_rank_four_certificate_audit() -> dict[str, object]:
    """Independently validate the restricted 23-vertex candidate data."""

    certificate = json.loads(LOCAL_CERTIFICATE.read_text(encoding="utf-8"))
    columns = [
        (1, 2, 2, 2),
        (1, 0, 2, 2),
        (1, 2, 0, 2),
        (1, 2, 2, 0),
        (1, 1, 1, 1),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
    ]
    signs = (1, 1, 1, 1, 2, 2, 2, 2)
    d1, d2, d3 = (int(value) for value in certificate["form_diagonal"])
    alpha = (d1 + d2 + d3) % P
    form = [
        [alpha, 0, 0, 0],
        [0, d1, (-alpha - d3) % P, (-alpha - d2) % P],
        [0, (-alpha - d3) % P, d2, (-alpha - d1) % P],
        [0, (-alpha - d2) % P, (-alpha - d1) % P, d3],
    ]
    gram = [
        [bilinear(columns[i], form, columns[j]) for j in range(8)]
        for i in range(8)
    ]
    if rank(form) != 4 or any(gram[i][i] for i in range(8)):
        raise AssertionError("candidate polar form is not the stated rank-four form")
    zero_adjacency = [set() for _ in range(8)]
    for i, j in combinations(range(8), 2):
        if gram[i][j] == 0:
            zero_adjacency[i].add(j)
            zero_adjacency[j].add(i)
    if graph_signature(zero_adjacency)["name"] != "2C4":
        raise AssertionError("candidate polar zero graph is not 2C4")

    triangles = [tuple(int(vertex) for vertex in row) for row in certificate["triangles"]]
    memberships = [
        tuple(int(index) for index in row) for row in certificate["vertex_memberships"]
    ]
    vertex_count = len(memberships)
    if vertex_count != 23 or len(triangles) != 8:
        raise AssertionError("candidate dimensions changed")
    recomputed_memberships = [
        tuple(index for index, triangle in enumerate(triangles) if vertex in triangle)
        for vertex in range(vertex_count)
    ]
    if memberships != recomputed_memberships:
        raise AssertionError("candidate membership list disagrees with its triangles")
    intersections = {
        (i, j)
        for i, j in combinations(range(8), 2)
        if set(triangles[i]) & set(triangles[j])
    }
    if intersections != {(0, 3)} or any(
        len(set(triangles[i]) & set(triangles[j])) != 1 for i, j in intersections
    ):
        raise AssertionError("candidate selected intersections changed")
    if any(len(membership) > 2 for membership in memberships):
        raise AssertionError("candidate violates its no-triple-membership restriction")

    internal_edges = {
        tuple(sorted((int(left), int(right))))
        for left, right in certificate["internal_edges"]
    }
    expected_internal_edges = {
        tuple(sorted(edge))
        for triangle in triangles
        for edge in combinations(triangle, 2)
    }
    extra_edges = {
        tuple(sorted((int(left), int(right))))
        for left, right in certificate["extra_edges"]
    }
    if internal_edges != expected_internal_edges or internal_edges & extra_edges:
        raise AssertionError("candidate internal/extra edge partition failed")
    edges = internal_edges | extra_edges
    if any(left == right or not (0 <= left < right < vertex_count) for left, right in edges):
        raise AssertionError("candidate edge endpoints are invalid")

    for i, j in combinations(range(8), 2):
        adjacency_count = sum(
            left != right and tuple(sorted((left, right))) in edges
            for left in triangles[i]
            for right in triangles[j]
        )
        if (i, j) in intersections:
            if adjacency_count != 4 or gram[i][j] != 1:
                raise AssertionError("intersecting selected pair has the wrong local data")
        elif adjacency_count != gram[i][j]:
            raise AssertionError("disjoint selected pair has the wrong cross-edge count")

    b_vector = [sum(signs[index] for index in membership) % P for membership in memberships]
    if b_vector != certificate["b"]:
        raise AssertionError("candidate b is not its signed incidence image")
    local_adjacency_times_b = [
        sum(
            b_vector[other]
            for other in range(vertex_count)
            if other != vertex and tuple(sorted((vertex, other))) in edges
        )
        % P
        for vertex in range(vertex_count)
    ]
    if any(local_adjacency_times_b) or sum(value * value for value in b_vector) % P != 2:
        raise AssertionError("candidate local adjacency equations or norm failed")

    degrees = [
        sum(
            other != vertex and tuple(sorted((vertex, other))) in edges
            for other in range(vertex_count)
        )
        for vertex in range(vertex_count)
    ]
    common_histogram: Counter[str] = Counter()
    for left, right in combinations(range(vertex_count), 2):
        common = sum(
            third not in (left, right)
            and tuple(sorted((left, third))) in edges
            and tuple(sorted((right, third))) in edges
            for third in range(vertex_count)
        )
        adjacent = (left, right) in edges
        if common > (1 if adjacent else 2):
            raise AssertionError("candidate violates a local lambda/mu cap")
        common_histogram[f"{'edge' if adjacent else 'nonedge'}_{common}"] += 1
    graph_triangles = [
        triple
        for triple in combinations(range(vertex_count), 3)
        if all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2))
    ]
    prisms = 0
    for left, right in combinations(graph_triangles, 2):
        if set(left) & set(right):
            continue
        cross_edges = [
            (u, v)
            for u in left
            for v in right
            if tuple(sorted((u, v))) in edges
        ]
        if (
            len(cross_edges) == 3
            and len({u for u, _ in cross_edges}) == 3
            and len({v for _, v in cross_edges}) == 3
        ):
            prisms += 1
    if prisms:
        raise AssertionError("candidate contains an induced triangular prism")

    relation_words = vector_relation_words(columns)
    supports = {
        frozenset(index for index, value in enumerate(word) if value)
        for word in relation_words
        if any(word)
    }
    circuits = {
        support for support in supports if not any(other < support for other in supports)
    }
    circuit_counts = Counter(len(support) for support in circuits)
    cross_realizations: Counter[tuple[int, int]] = Counter()
    for support in circuits:
        realizations = 0
        for left, right in combinations(range(vertex_count), 2):
            hits = [
                int(left in triangles[index]) + int(right in triangles[index])
                for index in support
            ]
            if all(hit == 1 for hit in hits) and any(
                left in triangles[index] for index in support
            ) and any(right in triangles[index] for index in support):
                realizations += 1
        cross_realizations[(len(support), realizations)] += 1
    if circuit_counts != Counter({4: 12, 5: 8}) or cross_realizations != Counter(
        {(4, 0): 12, (5, 0): 8}
    ):
        raise AssertionError("candidate internal circuit audit failed")

    return {
        "input_path": str(LOCAL_CERTIFICATE.relative_to(ROOT)).replace("\\", "/"),
        "restriction": "pair-specific selected intersections and no triple memberships",
        "vertices": vertex_count,
        "edges": len(edges),
        "selected_intersections": sorted([list(pair) for pair in intersections]),
        "form_rank": rank(form),
        "zero_graph": graph_signature(zero_adjacency)["name"],
        "local_adjacency_times_b_zero_on_23_coordinates": True,
        "does_not_check_76_outside_coordinates_of_Ab": True,
        "b_norm_mod3": sum(value * value for value in b_vector) % P,
        "maximum_induced_degree": max(degrees),
        "common_neighbor_histogram": dict(sorted(common_histogram.items())),
        "graph_triangles": len(graph_triangles),
        "induced_triangular_prisms": prisms,
        "edges_missing_their_required_common_neighbor_inside": common_histogram["edge_0"],
        "internal_projective_circuits": {
            str(weight): circuit_counts[weight] for weight in sorted(circuit_counts)
        },
        "circuit_cross_realizations": {
            f"weight{weight}_multiplicity{multiplicity}": count
            for (weight, multiplicity), count in sorted(cross_realizations.items())
        },
        "verdict": "RESTRICTED_LOCAL_COMPATIBILITY_ONLY",
    }


def weight_fourteen_composition_audit() -> dict[str, object]:
    """Clean-room replay of the two weight-fourteen Farkas certificates."""

    def admissible_types(positive: int, negative: int) -> list[tuple[str, int, int]]:
        limits = {
            "P": (positive - 1, negative),
            "N": (positive, negative - 1),
            "O": (positive, negative),
        }
        return [
            (membership, i_value, j_value)
            for membership, (maximum_i, maximum_j) in limits.items()
            for i_value in range(maximum_i + 1)
            for j_value in range(maximum_j + 1)
            if i_value + j_value <= 14 and (i_value - j_value) % P == 0
        ]

    def phi_thirteen(membership: str, i_value: int, j_value: int) -> int:
        indicator_negative = int(membership == "N")
        return (
            indicator_negative
            + 4 * i_value
            - 2 * j_value
            + j_value * (j_value - 1)
            + indicator_negative * j_value
            - 2 * i_value * j_value
            - 2 * indicator_negative * i_value
        )

    def phi_ten(membership: str, i_value: int, j_value: int) -> int:
        indicator_negative = int(membership == "N")
        return (
            3 * i_value
            - 2 * j_value
            + j_value * (j_value - 1)
            - i_value * j_value
            + indicator_negative * (j_value - i_value)
        )

    table_thirteen = []
    for membership, i_value, j_value in admissible_types(1, 13):
        value = phi_thirteen(membership, i_value, j_value)
        if membership == "P" or (membership == "O" and i_value == 0):
            factored = j_value * (j_value - 3)
        elif membership == "O":
            factored = (j_value - 1) * (j_value - 4)
        elif i_value == 0:
            factored = (j_value - 1) ** 2
        else:
            factored = (j_value - 1) * (j_value - 3)
        if value != factored or value < 0:
            raise AssertionError("the 1+13 pointwise certificate failed")
        table_thirteen.append(
            {"membership": membership, "i": i_value, "j": j_value, "Phi": value}
        )

    table_ten = []
    for membership, i_value, j_value in admissible_types(4, 10):
        value = phi_ten(membership, i_value, j_value)
        factored = (j_value - (2 if membership == "N" else 3)) * (
            j_value - i_value
        )
        if value != factored or value < 0:
            raise AssertionError("the 4+10 pointwise certificate failed")
        table_ten.append(
            {"membership": membership, "i": i_value, "j": j_value, "Phi": value}
        )

    global_thirteen = 13 + 4 * 14 - 2 * 14 * 13 + 2 * 13 * 12 - 4 * 13
    global_ten = 3 * 14 * 4 - 2 * 14 * 10 + 2 * 10 * 9 - 2 * 4 * 10
    if global_thirteen != -35 or global_ten != -12:
        raise AssertionError("a weight-fourteen global Farkas sum changed")
    compositions = [
        [positive, 14 - positive]
        for positive in range(15)
        if (positive - (14 - positive)) % P == 0
    ]
    if compositions != [[1, 13], [4, 10], [7, 7], [10, 4], [13, 1]]:
        raise AssertionError("weight-fourteen composition list changed")

    lift_samples = []
    for positive, negative in [(1, 13), (4, 10), (7, 7), (10, 4), (13, 1)]:
        difference = positive - negative
        lift_parameter = difference // 3
        if difference != 3 * lift_parameter:
            raise AssertionError("integer lift parameter is not integral")
        p_residual = 2 * positive * difference - 6 * lift_parameter * positive
        n_residual = 2 * negative * difference - 6 * lift_parameter * negative
        if p_residual or n_residual:
            raise AssertionError("category-summed integer lift did not collapse")
        lift_samples.append(
            {
                "composition": [positive, negative],
                "t": lift_parameter,
                "P_residual": p_residual,
                "N_residual": n_residual,
            }
        )

    return {
        "admissible_compositions_before_farkas": compositions,
        "one_plus_thirteen": {
            "admissible_types_checked": len(table_thirteen),
            "minimum_phi": min(row["Phi"] for row in table_thirteen),
            "maximum_phi": max(row["Phi"] for row in table_thirteen),
            "zero_types": sum(row["Phi"] == 0 for row in table_thirteen),
            "all_pointwise_values_nonnegative": True,
            "global_sum": global_thirteen,
            "excluded": True,
        },
        "four_plus_ten": {
            "admissible_types_checked": len(table_ten),
            "minimum_phi": min(row["Phi"] for row in table_ten),
            "maximum_phi": max(row["Phi"] for row in table_ten),
            "zero_types": sum(row["Phi"] == 0 for row in table_ten),
            "all_pointwise_values_nonnegative": True,
            "global_sum": global_ten,
            "excluded": True,
        },
        "negation_excludes": [[13, 1], [10, 4]],
        "only_surviving_composition": [7, 7],
        "integer_lift_identity": "z=Ax/3; Az=4x-z+2t*1",
        "category_summed_lift_residuals": lift_samples,
        "weight_14_excluded": False,
        "balanced_branch": "UNKNOWN",
        "weights_17_20_23": "UNKNOWN",
    }


def build_result() -> dict[str, object]:
    return {
        "format": "wave207-incidence-tensor-rigidity-clean-room-v1",
        "field": 3,
        "m7g": m7g_audit(),
        "gram_radical": gram_radical_exhaustion(),
        "transition_rank": transition_rank_audit(),
        "four_center_control": four_center_control(),
        "point_code_supplement": point_code_supplement(),
        "signed_neighbor_distance": signed_neighbor_distance_audit(),
        "weight_fourteen_aggregate_control": weight_fourteen_aggregate_control_audit(),
        "weight_fourteen_composition": weight_fourteen_composition_audit(),
        "local_rank_four_certificate": local_rank_four_certificate_audit(),
        "scope_wall": {
            "rank_11_endpoint": "UNKNOWN",
            "n3_4158_endpoint": "UNKNOWN",
            "Q_ge_7060": "NOT_PROVED",
            "graph_constructed": False,
            "counterexample_or_nonexistence_proof": False,
            "conway_99": "UNKNOWN",
        },
    }


def render(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--verify", action="store_true")
    action.add_argument("--print", action="store_true")
    args = parser.parse_args()
    data = build_result()
    if args.write:
        ARCHIVE.write_text(render(data), encoding="utf-8", newline="\n")
        print(f"WROTE: {ARCHIVE}")
    elif args.verify:
        archived = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        if archived != data:
            raise SystemExit("independent result does not match archived JSON")
        print("PASS: Wave207 clean-room verifier result")
    else:
        print(render(data), end="")


if __name__ == "__main__":
    main()
