"""Exact Wave 206 hostile three-center controls over F_3.

The first control keeps one labelled 99x231 linear incidence, rank-six star
projectors, rank-11 square-zero centered Grams, sum_x P_x=0, and the complete
pair matrices g and H fixed while changing the three-center tensor tau.

The second control shows that the universal fixed-y Gram bound rank(tau_y)<=21
is sharp for 99 rank-six projectors whose sum is zero.  It is not coupled to
the 231-column incidence.  Every target premise missing from either relaxed
control is emitted in the machine-readable result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any, Iterable


FIELD = 3
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EXPECTED_INPUTS = {
    "attempts/wave206-three-center-global-extension/protocol.md":
        "66c20334e284a26cc771ee86d97e678cb67b6efb4648b2af2fffe480fb5a9103",
    "verification/2026-07-29-wave205-integration-audit.md":
        "f50b5591cb0e1e3dfdd835a22fd9156dd3a2a039323388889a6fa5e756a0a297",
    "verification/2026-07-29-wave205-orchestrator.md":
        "9b9711ad4b9ac902161833b4a5825404e95ba6f443462ac3d79532df704b2deb",
    "verification/wave205-fourth-trace-globalization-verifier/package-manifest.sha256":
        "b93f65f72db94539c7d42d7eca6debbaf3a5c4a401db3b812a80549bcb9b8325",
    "attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256":
        "2c9976b6cb07a3036df07fd0e7ceb7ffce6a339651d604fcecdcf8c0c3da3d96",
    "attempts/wave205-global-fourth-moment-proof-b/package-manifest.sha256":
        "a91a2a1cdbc129fa66e9d63b34031a774d5af78c458d18d9a1aadd7e4be217e7",
    "attempts/wave205-fourth-trace-globalization/protocol.md":
        "a1d45fc0a82b9944a9e020ded3945e75944e0e00202eacbb20eb05598e30bf4d",
}

Matrix = list[list[int]]


def mod(value: int) -> int:
    return value % FIELD


def zero_matrix(height: int, width: int) -> Matrix:
    return [[0] * width for _ in range(height)]


def identity(size: int) -> Matrix:
    return [[int(row == column) for column in range(size)] for row in range(size)]


def diagonal(entries: Iterable[int]) -> Matrix:
    values = [mod(value) for value in entries]
    return [
        [values[row] if row == column else 0 for column in range(len(values))]
        for row in range(len(values))
    ]


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [mod(left[row][column] + right[row][column]) for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def scalar_matrix(scalar: int, matrix: Matrix) -> Matrix:
    return [[mod(scalar * entry) for entry in row] for row in matrix]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix shape mismatch")
    return [
        [
            mod(
                sum(
                    left[row][inner] * right[inner][column]
                    for inner in range(len(right))
                )
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matrix_trace(matrix: Matrix) -> int:
    return mod(sum(matrix[index][index] for index in range(len(matrix))))


def flatten(matrix: Matrix) -> list[int]:
    return [entry for row in matrix for entry in row]


def gf3_rref(matrix: Matrix) -> tuple[Matrix, list[int]]:
    if not matrix:
        return [], []
    rows = [[mod(entry) for entry in row] for row in matrix]
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("ragged matrix")
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        source = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if source is None:
            continue
        rows[pivot_row], rows[source] = rows[source], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, FIELD)
        rows[pivot_row] = [mod(inverse * entry) for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                mod(rows[row][index] - multiplier * rows[pivot_row][index])
                for index in range(width)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def gf3_rank(matrix: Matrix) -> int:
    return len(gf3_rref(matrix)[1])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs() -> dict[str, str]:
    observed = {relative: sha256(ROOT / relative) for relative in EXPECTED_INPUTS}
    if observed != EXPECTED_INPUTS:
        raise AssertionError({"expected": EXPECTED_INPUTS, "observed": observed})
    return observed


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def distribution(values: Iterable[int]) -> dict[str, int]:
    counts = Counter(values)
    return {str(value): counts[value] for value in range(FIELD)}


def normalized_direction(vector: list[int]) -> tuple[int, ...]:
    first = next((entry for entry in vector if entry), None)
    require(first is not None, "zero direction")
    inverse = pow(first, -1, FIELD)
    return tuple(mod(inverse * entry) for entry in vector)


def load_certificate() -> dict[str, Any]:
    return json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))


def gram(columns: Matrix, form: Matrix) -> Matrix:
    return matrix_multiply(matrix_multiply(transpose(columns), form), columns)


def rank_one_operator(vector: list[int], form: Matrix) -> Matrix:
    column = [[entry] for entry in vector]
    return matrix_multiply(matrix_multiply(column, transpose(column)), form)


def frame_operator(vectors: list[list[int]], form: Matrix) -> Matrix:
    result = zero_matrix(len(form), len(form))
    for vector in vectors:
        result = matrix_add(result, rank_one_operator(vector, form))
    return result


def projector_pool(
    certificate: dict[str, Any],
) -> tuple[Matrix, list[Matrix], list[Matrix], list[Matrix]]:
    form = diagonal(certificate["ambient_form_diagonal"])
    transform = identity(11)
    bases: list[Matrix] = []
    projectors: list[Matrix] = []
    simplices: list[Matrix] = []
    coefficient_columns = transpose(certificate["simplex_coefficient_vectors"])
    expected_simplex_gram = [
        [0 if row == column else 1 for column in range(7)] for row in range(7)
    ]

    for word_index, vector in enumerate(
        certificate["projector_pool"]["reflection_vectors"]
    ):
        column = [[entry] for entry in vector]
        norm = matrix_multiply(matrix_multiply(transpose(column), form), column)[0][0]
        require(norm != 0, f"reflection {word_index} has singular root")
        outer = matrix_multiply(
            column, matrix_multiply(transpose(column), form)
        )
        reflection = matrix_add(identity(11), scalar_matrix(pow(norm, -1, FIELD), outer))
        require(
            matrix_multiply(matrix_multiply(transpose(reflection), form), reflection)
            == form,
            f"reflection {word_index} is not orthogonal",
        )
        transform = matrix_multiply(reflection, transform)
        basis = [row[:6] for row in transform]
        require(gram(basis, form) == identity(6), f"basis {word_index} not orthonormal")
        projector = matrix_multiply(
            matrix_multiply(basis, transpose(basis)), form
        )
        require(
            matrix_multiply(projector, projector) == projector,
            f"projector {word_index} not idempotent",
        )
        require(
            matrix_multiply(transpose(projector), form)
            == matrix_multiply(form, projector),
            f"projector {word_index} not self-adjoint",
        )
        require(gf3_rank(projector) == 6, f"projector {word_index} rank changed")
        require(matrix_trace(projector) == 0, f"projector {word_index} trace changed")
        simplex = matrix_multiply(basis, coefficient_columns)
        require(
            gram(simplex, form) == expected_simplex_gram,
            f"simplex {word_index} Gram changed",
        )
        require(
            [mod(sum(row)) for row in simplex] == [0] * 11,
            f"simplex {word_index} sum changed",
        )
        require(
            frame_operator(transpose(simplex), form) == scalar_matrix(2, projector),
            f"simplex {word_index} frame identity changed",
        )
        bases.append(basis)
        projectors.append(projector)
        simplices.append(simplex)

    require(len(projectors) == 34, "pool size changed")
    require(
        len({tuple(flatten(projector)) for projector in projectors}) == 34,
        "pool projectors are not distinct",
    )
    return form, bases, projectors, simplices


def pair_invariants(left: Matrix, right: Matrix) -> tuple[int, int]:
    product = matrix_multiply(left, right)
    return matrix_trace(product), matrix_trace(matrix_multiply(product, product))


def tau(left: Matrix, middle: Matrix, right: Matrix) -> int:
    return matrix_trace(
        matrix_multiply(
            matrix_multiply(matrix_multiply(left, middle), right), middle
        )
    )


def component_blocks(
    component: dict[str, Any], shared_specification: dict[str, Any]
) -> list[dict[str, Any]]:
    offset = component["offset"]
    size = component["size"]
    blocks: list[dict[str, Any]] = []
    for translate in range(size // 3):
        blocks.append(
            {
                "component": component["name"],
                "color": 0,
                "vertices": [
                    offset + translate,
                    offset + translate + size // 3,
                    offset + translate + 2 * size // 3,
                ],
                "source": {"kind": "short_orbit", "translate": translate},
            }
        )
    for orbit in shared_specification["full_orbits"]:
        starter = orbit["starter"]
        first_color = orbit["first_color"]
        for translate in range(size):
            vertices = sorted({(translate + entry) % size for entry in starter})
            require(len(vertices) == 3, "degenerate cyclic block")
            blocks.append(
                {
                    "component": component["name"],
                    "color": first_color + translate % 3,
                    "vertices": [offset + vertex for vertex in vertices],
                    "source": {
                        "kind": "full_orbit",
                        "starter": list(starter),
                        "translate": translate,
                    },
                }
            )
    return blocks


def build_incidence(
    certificate: dict[str, Any],
) -> tuple[list[dict[str, Any]], Matrix, Matrix, dict[str, Any]]:
    shared_specification = certificate["shared_incidence"]
    components = shared_specification["components"]
    blocks = [
        block
        for component in components
        for block in component_blocks(component, shared_specification)
    ]
    for block_id, block in enumerate(blocks):
        block["id"] = block_id
    require(len(blocks) == 231, "block count changed")

    incidence = zero_matrix(99, 231)
    for block in blocks:
        for vertex in block["vertices"]:
            incidence[vertex][block["id"]] = 1
    require([sum(row) for row in incidence] == [7] * 99, "row degrees changed")
    require(
        [sum(incidence[row][column] for row in range(99)) for column in range(231)]
        == [3] * 231,
        "column degrees changed",
    )
    bbt = [
        [
            sum(incidence[left][column] * incidence[right][column] for column in range(231))
            for right in range(99)
        ]
        for left in range(99)
    ]
    require(
        all(
            bbt[left][right] <= 1
            for left in range(99)
            for right in range(99)
            if left != right
        ),
        "incidence is not linear",
    )
    adjacency = [
        [int(left != right and bbt[left][right] == 1) for right in range(99)]
        for left in range(99)
    ]
    require([sum(row) for row in adjacency] == [14] * 99, "point degree changed")
    require(
        all(
            bbt[left][right]
            == adjacency[left][right] + (7 if left == right else 0)
            for left in range(99)
            for right in range(99)
        ),
        "integer BB^T identity changed",
    )
    require(
        all(
            mod(bbt[left][right])
            == mod(adjacency[left][right] + int(left == right))
            for left in range(99)
            for right in range(99)
        ),
        "ternary BB^T identity changed",
    )
    require(
        all(
            sorted(block["color"] for block in blocks if vertex in block["vertices"])
            == list(range(7))
            for vertex in range(99)
        ),
        "star colors changed",
    )

    edges = [
        (left, right)
        for left in range(99)
        for right in range(left + 1, 99)
        if adjacency[left][right]
    ]
    triangles = [
        (left, middle, right)
        for left in range(99)
        for middle in range(left + 1, 99)
        for right in range(middle + 1, 99)
        if adjacency[left][middle]
        and adjacency[left][right]
        and adjacency[middle][right]
    ]
    designated = {tuple(sorted(block["vertices"])) for block in blocks}
    edge_lambda = Counter(
        sum(adjacency[left][vertex] * adjacency[right][vertex] for vertex in range(99))
        for left, right in edges
    )
    nonedge_mu = Counter(
        sum(adjacency[left][vertex] * adjacency[right][vertex] for vertex in range(99))
        for left in range(99)
        for right in range(left + 1, 99)
        if not adjacency[left][right]
    )

    unseen = set(range(99))
    component_sizes: list[int] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue: deque[int] = deque([start])
        seen = {start}
        while queue:
            vertex = queue.popleft()
            for neighbor, is_edge in enumerate(adjacency[vertex]):
                if is_edge and neighbor not in seen:
                    seen.add(neighbor)
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        component_sizes.append(len(seen))

    summary = {
        "point_count": 99,
        "block_count": 231,
        "row_degree": 7,
        "column_degree": 3,
        "linear_triple_system": True,
        "point_graph_degree": 14,
        "point_graph_edge_count": len(edges),
        "integer_bbt_identity": "BB^T=A+7I",
        "ternary_bbt_identity": "BB^T=A+I over F_3",
        "each_vertex_sees_each_color_once": True,
        "connected_component_sizes": sorted(component_sizes),
        "all_graph_triangle_count": len(triangles),
        "designated_block_triangle_count": len(designated),
        "extra_graph_triangle_count": len(set(triangles) - designated),
        "edge_common_neighbor_distribution": {
            str(key): edge_lambda[key] for key in sorted(edge_lambda)
        },
        "nonedge_common_neighbor_distribution": {
            str(key): nonedge_mu[key] for key in sorted(nonedge_mu)
        },
    }
    return blocks, incidence, adjacency, summary


def component_index(vertex: int, components: list[dict[str, Any]]) -> int:
    for index, component in enumerate(components):
        if component["offset"] <= vertex < component["offset"] + component["size"]:
            return index
    raise AssertionError("vertex outside components")


def shared_realization(
    name: str,
    type_indices: list[int],
    certificate: dict[str, Any],
    form: Matrix,
    projectors: list[Matrix],
    simplices: list[Matrix],
    blocks: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[Matrix], Matrix, Matrix, list[list[list[int]]]]:
    components = certificate["shared_incidence"]["components"]
    vertex_types = [component_index(vertex, components) for vertex in range(99)]
    projector_rows = [projectors[type_indices[kind]] for kind in vertex_types]
    component_by_name = {
        component["name"]: index for index, component in enumerate(components)
    }
    block_vectors = [
        transpose(simplices[type_indices[component_by_name[block["component"]]]])[
            block["color"]
        ]
        for block in blocks
    ]
    for vertex in range(99):
        incident = [
            block_vectors[block["id"]]
            for block in blocks
            if vertex in block["vertices"]
        ]
        require(
            frame_operator(incident, form) == scalar_matrix(2, projector_rows[vertex]),
            f"{name}: star coupling changed at vertex {vertex}",
        )

    projector_sum = zero_matrix(11, 11)
    for projector in projector_rows:
        projector_sum = matrix_add(projector_sum, projector)
    require(projector_sum == zero_matrix(11, 11), f"{name}: sum P_x changed")
    require(
        frame_operator(block_vectors, form) == zero_matrix(11, 11),
        f"{name}: global frame changed",
    )
    column_matrix = transpose(block_vectors)
    centered_gram = gram(column_matrix, form)
    require(gf3_rank(column_matrix) == 11, f"{name}: column rank changed")
    require(gf3_rank(centered_gram) == 11, f"{name}: D rank changed")
    require(
        matrix_multiply(centered_gram, centered_gram) == zero_matrix(231, 231),
        f"{name}: D^2 changed",
    )
    require(
        all(centered_gram[index][index] == 0 for index in range(231)),
        f"{name}: nonsingular block column",
    )

    pair_g = [
        [
            pair_invariants(projector_rows[left], projector_rows[right])[0]
            for right in range(99)
        ]
        for left in range(99)
    ]
    pair_h = [
        [
            pair_invariants(projector_rows[left], projector_rows[right])[1]
            for right in range(99)
        ]
        for left in range(99)
    ]
    type_projectors = [projectors[index] for index in type_indices]
    tau_types = [
        [
            [tau(type_projectors[left], type_projectors[middle], type_projectors[right])
             for right in range(3)]
            for middle in range(3)
        ]
        for left in range(3)
    ]
    component_sizes = [component["size"] for component in components]
    require(
        all(
            mod(
                sum(
                    component_sizes[right] * tau_types[left][middle][right]
                    for right in range(3)
                )
            )
            == 0
            for left in range(3)
            for middle in range(3)
        ),
        f"{name}: tau contraction changed",
    )

    fixed_y_rows: list[dict[str, Any]] = []
    for middle in range(3):
        small_slice = [
            [tau_types[left][middle][right] for right in range(3)]
            for left in range(3)
        ]
        full_slice = [
            [
                tau_types[vertex_types[left]][middle][vertex_types[right]]
                for right in range(99)
            ]
            for left in range(99)
        ]
        require(full_slice == transpose(full_slice), f"{name}: tau_y not symmetric")
        require(
            [mod(sum(row)) for row in full_slice] == [0] * 99,
            f"{name}: tau_y row sum changed",
        )
        y_vertex = components[middle]["offset"]
        require(
            full_slice[y_vertex] == pair_g[y_vertex],
            f"{name}: tau_y y-row is not g",
        )
        require(
            [full_slice[index][index] for index in range(99)] == pair_h[y_vertex],
            f"{name}: tau_y diagonal is not H_y*",
        )
        fixed_y_rows.append(
            {
                "component": components[middle]["name"],
                "representative_y": y_vertex,
                "three_type_slice": small_slice,
                "rank_over_F3": gf3_rank(full_slice),
                "row_sums_zero": True,
                "y_row_equals_g_y_star": True,
                "diagonal_equals_H_y_star": True,
            }
        )

    directions = Counter(normalized_direction(vector) for vector in block_vectors)
    return (
        {
            "projector_pool_indices_by_component": type_indices,
            "projector_type_counts": {
                str(type_indices[index]): components[index]["size"] for index in range(3)
            },
            "sum_projectors_zero": True,
            "global_column_frame_zero": True,
            "ambient_column_span_rank": gf3_rank(column_matrix),
            "centered_gram_rank": gf3_rank(centered_gram),
            "centered_gram_square_zero": True,
            "all_block_columns_singular": True,
            "distinct_projective_direction_count": len(directions),
            "projective_direction_multiplicity_distribution": {
                str(key): value
                for key, value in sorted(Counter(directions.values()).items())
            },
            "fixed_y_slices": fixed_y_rows,
        },
        projector_rows,
        pair_g,
        pair_h,
        tau_types,
    )


def fixed_y_rank_control(
    name: str,
    specification: dict[str, Any],
    form: Matrix,
    projectors: list[Matrix],
) -> dict[str, Any]:
    span = specification["projector_pool_indices"]
    indices = list(range(span["start"], span["stop_exclusive"]))
    labels = [
        pool_index
        for pool_index in indices
        for _ in range(specification["multiplicity_per_type"])
    ]
    require(len(labels) == 99, f"{name}: label count changed")
    y_index = labels.index(specification["fixed_y_pool_index"])
    projector_rows = [projectors[index] for index in labels]
    projector_sum = zero_matrix(11, 11)
    for projector in projector_rows:
        projector_sum = matrix_add(projector_sum, projector)
    require(projector_sum == zero_matrix(11, 11), f"{name}: sum P_x changed")
    fixed = projector_rows[y_index]
    compressed = [
        matrix_multiply(matrix_multiply(fixed, projector), fixed)
        for projector in projector_rows
    ]
    slice_matrix = [
        [
            matrix_trace(matrix_multiply(compressed[left], compressed[right]))
            for right in range(99)
        ]
        for left in range(99)
    ]
    require(slice_matrix == transpose(slice_matrix), f"{name}: slice not symmetric")
    require(
        [mod(sum(row)) for row in slice_matrix] == [0] * 99,
        f"{name}: row sums changed",
    )
    g_row = [pair_invariants(fixed, projector)[0] for projector in projector_rows]
    h_row = [pair_invariants(fixed, projector)[1] for projector in projector_rows]
    require(slice_matrix[y_index] == g_row, f"{name}: y row is not g")
    require(
        [slice_matrix[index][index] for index in range(99)] == h_row,
        f"{name}: diagonal is not H",
    )
    unique_slice = [
        [
            tau(projectors[left], fixed, projectors[right])
            for right in indices
        ]
        for left in indices
    ]
    require(gf3_rank(unique_slice) == 21, f"{name}: unique slice rank changed")
    require(gf3_rank(slice_matrix) == 21, f"{name}: full slice rank changed")
    compressed_coordinate_rank = gf3_rank([flatten(operator) for operator in compressed])
    require(compressed_coordinate_rank == 21, f"{name}: operator span rank changed")
    return {
        "projector_count": 99,
        "distinct_projector_type_count": len(indices),
        "multiplicity_per_type": specification["multiplicity_per_type"],
        "fixed_y_label": y_index,
        "fixed_y_pool_index": specification["fixed_y_pool_index"],
        "sum_projectors_zero": True,
        "fixed_y_slice_symmetric": True,
        "fixed_y_slice_row_sums_zero": True,
        "fixed_y_slice_y_row_equals_g_y_star": True,
        "fixed_y_slice_diagonal_equals_H_y_star": True,
        "fixed_y_slice_rank_over_F3": gf3_rank(slice_matrix),
        "compressed_operator_coordinate_rank_over_F3": compressed_coordinate_rank,
        "fixed_y_slice_entry_distribution": distribution(flatten(slice_matrix)),
        "fixed_y_slice_diagonal_distribution": distribution(
            slice_matrix[index][index] for index in range(99)
        ),
        "unique_33_type_slice_entry_distribution": distribution(flatten(unique_slice)),
        "unique_33_type_slice_diagonal_distribution": distribution(
            unique_slice[index][index] for index in range(33)
        ),
    }


def analyze() -> dict[str, Any]:
    inputs = verify_inputs()
    certificate = load_certificate()
    require(certificate["field"] == FIELD, "certificate field changed")
    form, bases, projectors, simplices = projector_pool(certificate)
    blocks, incidence, adjacency, incidence_summary = build_incidence(certificate)
    del incidence, adjacency

    shared_specs = certificate["shared_incidence_realizations"]
    a_data = shared_realization(
        "A",
        shared_specs["A_projector_pool_indices_by_component"],
        certificate,
        form,
        projectors,
        simplices,
        blocks,
    )
    b_data = shared_realization(
        "B",
        shared_specs["B_projector_pool_indices_by_component"],
        certificate,
        form,
        projectors,
        simplices,
        blocks,
    )
    a_summary, _, g_a, h_a, tau_a = a_data
    b_summary, _, g_b, h_b, tau_b = b_data
    require(g_a == g_b, "full g matrices differ")
    require(h_a == h_b, "full H matrices differ")
    differing_type_triples = [
        (left, middle, right)
        for left in range(3)
        for middle in range(3)
        for right in range(3)
        if tau_a[left][middle][right] != tau_b[left][middle][right]
    ]
    components = certificate["shared_incidence"]["components"]
    sizes = [component["size"] for component in components]
    differing_ordered_entries = sum(
        sizes[left] * sizes[middle] * sizes[right]
        for left, middle, right in differing_type_triples
    )
    require(
        differing_type_triples
        == [(0, 1, 2), (0, 2, 1), (1, 0, 2),
            (1, 2, 0), (2, 0, 1), (2, 1, 0)],
        "tau separation support changed",
    )
    require(differing_ordered_entries == 209952, "tau separation count changed")

    pair_signatures = [
        {
            "component_pair": [left, right],
            "g": pair_invariants(
                projectors[shared_specs["A_projector_pool_indices_by_component"][left]],
                projectors[shared_specs["A_projector_pool_indices_by_component"][right]],
            )[0],
            "H": pair_invariants(
                projectors[shared_specs["A_projector_pool_indices_by_component"][left]],
                projectors[shared_specs["A_projector_pool_indices_by_component"][right]],
            )[1],
        }
        for left in range(3)
        for right in range(left + 1, 3)
    ]

    rank_controls = {
        name: fixed_y_rank_control(name, specification, form, projectors)
        for name, specification in certificate["fixed_y_rank_controls"].items()
    }
    require(
        rank_controls["A"]["fixed_y_slice_diagonal_distribution"]
        != rank_controls["B"]["fixed_y_slice_diagonal_distribution"],
        "sharp controls do not vary diagonal",
    )
    require(
        rank_controls["A"]["fixed_y_slice_entry_distribution"]
        != rank_controls["B"]["fixed_y_slice_entry_distribution"],
        "sharp controls do not vary tau",
    )

    result = {
        "claim_label": "CANDIDATE",
        "field": FIELD,
        "inputs": inputs,
        "certificate_sha256": sha256(HERE / "certificate.json"),
        "projector_pool": {
            "claim_label": "DERIVED",
            "ambient_dimension": 11,
            "ambient_form_diagonal": certificate["ambient_form_diagonal"],
            "reflection_word_length": len(
                certificate["projector_pool"]["reflection_vectors"]
            ),
            "distinct_projector_count": len(projectors),
            "every_projector_rank": 6,
            "every_projector_trace": 0,
            "every_projector_self_adjoint": True,
            "every_projector_idempotent": True,
            "every_projector_has_seven_singular_simplex": True,
            "simplex_gram": "J_7-I_7",
            "simplex_frame_identity": "P=-sum(z tensor z)",
            "joined_selected_basis_rank_A": gf3_rank(
                [
                    bases[0][row] + bases[2][row] + bases[9][row]
                    for row in range(11)
                ]
            ),
            "joined_selected_basis_rank_B": gf3_rank(
                [
                    bases[0][row] + bases[2][row] + bases[15][row]
                    for row in range(11)
                ]
            ),
        },
        "shared_incidence_tau_collision": {
            "claim_label": "REFUTED",
            "refuted_implication": (
                "the explicitly checked relaxed shared-incidence, rank-11, "
                "zero-frame, star-projector, full-g, and full-H premises "
                "determine the three-center tensor tau"
            ),
            "incidence": incidence_summary,
            "realizations": {"A": a_summary, "B": b_summary},
            "pair_signatures_between_component_types": pair_signatures,
            "same_labelled_99x231_incidence": True,
            "same_full_g_matrix": True,
            "same_full_H_matrix": True,
            "tau_type_tables": {"A": tau_a, "B": tau_b},
            "different_type_triples": [list(item) for item in differing_type_triples],
            "different_ordered_tau_entries": differing_ordered_entries,
            "all_tau_differences_use_one_center_from_each_component": True,
            "tau_contraction_sum_z_zero": True,
            "fixed_y_slice_rank_over_F3": 3,
            "restrictions": [
                "three component-constant projector types selected from the listed 34-type reflection-word pool",
                "the cyclic component incidence has sizes 27, 36, 36",
                "no automorphism assumed",
            ],
            "missing_target_premises": [
                "the point graph is disconnected with component sizes 27,36,36",
                "edge common-neighbor counts are not uniformly lambda=1",
                "nonedge common-neighbor counts are not uniformly mu=2; cross-component nonedges have mu=0",
                "the point graph has 1098 graph triangles beyond the 231 designated blocks",
                "only 19 projective block directions occur, with multiplicities 9, 12, and 21, so projective distinctness fails",
                "the exact selected orthogonality graph and endpoint block-relation profiles are not imposed",
                "prism-free crossing caps, outer-cycle statistics, endpoint t_xy restrictions, distance, cover, and Q constraints are not imposed",
                "the separated triples are cross-component triples; they do not realize any target srg three-center graph type",
            ],
        },
        "fixed_y_rank21_controls": {
            "claim_label": "DERIVED",
            "identity": (
                "tau_y[x,z]=tr((P_y P_x P_y)(P_y P_z P_y)) is the trace "
                "Gram of self-adjoint operators on the six-space E_y"
            ),
            "universal_dimension_bound": 21,
            "controls": rank_controls,
            "rank_bound_attained_in_both_controls": True,
            "diagonal_distribution_varies": True,
            "tau_entry_distribution_varies": True,
            "restrictions": [
                "each control uses a consecutive 33-type prefix or suffix of the listed reflection-word pool",
                "each projector type is repeated exactly three times",
                "sum_x P_x=0 follows and is checked in characteristic three",
                "no automorphism assumed",
            ],
            "missing_target_premises": [
                "the 99 projector labels are not distinct: 33 types each occur three times",
                "no 231-column incidence or star-to-column coupling is imposed",
                "no rank-11 square-zero centered Gram of projectively distinct singular columns is imposed",
                "no srg(99,14,1,2), triangle, lambda, mu, prism, t_xy, distance, cover, or Q premise is imposed",
            ],
        },
        "bounded_search_ledger": {
            "claim_label": "UNKNOWN",
            "pool_size": 34,
            "shared_collision_search_space": "ordered triples of distinct types from the 34-type deterministic reflection-word pool",
            "sharp_rank_search_space": "the two displayed consecutive 33-type windows with multiplicity three",
            "stronger_coupled_rank21_shared_incidence_control_found": False,
            "nonhit_is_evidence_of_nonexistence": False,
            "automorphism_assumption": "NONE",
        },
        "status": {
            "Conway-99": "UNKNOWN",
            "rank-11 endpoint": "UNKNOWN",
            "n3=4158 endpoint": "UNKNOWN",
            "actual nonedge h": "UNKNOWN",
            "Q>=7060": "NOT PROVED",
            "automorphism_assumption": "NONE",
        },
        "next_required_invariant": (
            "a graph-typed joint law for the fixed-y Gram slices tau_y, or an "
            "equivalent four-center/Terwilliger-localizer constraint coupling "
            "different y, is needed; pair data and the checked contraction "
            "alone do not determine tau"
        ),
    }
    verify(result)
    return result


def verify(result: dict[str, Any]) -> None:
    incidence = result["shared_incidence_tau_collision"]["incidence"]
    require(incidence["point_graph_edge_count"] == 693, "edge count changed")
    require(
        incidence["connected_component_sizes"] == [27, 36, 36],
        "component sizes changed",
    )
    require(incidence["all_graph_triangle_count"] == 1329, "triangle count changed")
    require(
        incidence["extra_graph_triangle_count"] == 1098,
        "extra triangle count changed",
    )
    require(
        incidence["edge_common_neighbor_distribution"]
        == {"4": 144, "5": 243, "6": 27, "7": 225, "8": 27, "9": 27},
        "lambda distribution changed",
    )
    require(
        incidence["nonedge_common_neighbor_distribution"]
        == {"0": 3240, "2": 144, "4": 180, "5": 27, "6": 315, "7": 27, "8": 225},
        "mu distribution changed",
    )
    collision = result["shared_incidence_tau_collision"]
    require(collision["same_full_g_matrix"], "g comparison changed")
    require(collision["same_full_H_matrix"], "H comparison changed")
    require(
        collision["different_ordered_tau_entries"] == 209952,
        "tau separation changed",
    )
    require(
        result["projector_pool"]["joined_selected_basis_rank_A"] == 11
        and result["projector_pool"]["joined_selected_basis_rank_B"] == 11,
        "selected star spaces no longer span 11",
    )
    controls = result["fixed_y_rank21_controls"]["controls"]
    require(
        controls["A"]["fixed_y_slice_rank_over_F3"] == 21
        and controls["B"]["fixed_y_slice_rank_over_F3"] == 21,
        "rank-21 sharpness changed",
    )
    require(
        controls["A"]["fixed_y_slice_diagonal_distribution"]
        == {"0": 30, "1": 33, "2": 36},
        "control A diagonal distribution changed",
    )
    require(
        controls["B"]["fixed_y_slice_diagonal_distribution"]
        == {"0": 33, "1": 15, "2": 51},
        "control B diagonal distribution changed",
    )
    require(result["status"]["Conway-99"] == "UNKNOWN", "status inflation")
    require(
        not result["bounded_search_ledger"]["nonhit_is_evidence_of_nonexistence"],
        "bounded nonhit inflated",
    )


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", type=Path)
    parser.add_argument("--verify-results", type=Path)
    args = parser.parse_args()
    result = analyze()
    if args.verify_results:
        observed = json.loads(args.verify_results.read_text(encoding="utf-8"))
        require(observed == result, "frozen results differ")
    if args.write_results:
        write_json(args.write_results, result)
    if not args.write_results and not args.verify_results:
        print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS: Wave206 exact hostile three-center controls")


if __name__ == "__main__":
    main()
