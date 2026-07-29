"""Independent post-source audit of the released Wave 206 hostile package.

The discovery package is treated only as certificate data and a set of claims.
No discovery Python is imported.  Matrix arithmetic comes from the sealed
source-blind verifier implementation.
"""

from __future__ import annotations

from collections import Counter, deque
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DISCOVERY = ROOT / "attempts" / "wave206-three-center-hostile-controls"
BLIND_MODULE = HERE / "independent_verifier.py"
SPEC = importlib.util.spec_from_file_location("wave206_blind_matrix", BLIND_MODULE)
assert SPEC is not None and SPEC.loader is not None
IV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IV)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def column(vector: Sequence[int]) -> list[list[int]]:
    return [[value % 3] for value in vector]


def gram(columns: Sequence[Sequence[int]], form: Sequence[Sequence[int]]) -> list[list[int]]:
    return IV.matmul(IV.matmul(IV.transpose(columns), form), columns)


def frame_operator(
    vectors: Iterable[Sequence[int]], form: Sequence[Sequence[int]]
) -> list[list[int]]:
    out = IV.zeros(len(form), len(form))
    for vector in vectors:
        vector_column = column(vector)
        vector_star = IV.matmul(IV.transpose(vector_column), form)
        out = IV.add(out, IV.matmul(vector_column, vector_star))
    return out


def projectors_from_certificate(
    certificate: dict[str, Any]
) -> tuple[
    list[list[int]],
    list[list[list[int]]],
    list[list[list[int]]],
    list[list[list[int]]],
]:
    form = IV.diagonal(certificate["ambient_form_diagonal"])
    transform = IV.eye(11)
    coefficient_columns = IV.transpose(certificate["simplex_coefficient_vectors"])
    expected_simplex_gram = [[0 if i == j else 1 for j in range(7)] for i in range(7)]
    bases: list[list[list[int]]] = []
    projectors: list[list[list[int]]] = []
    simplices: list[list[list[int]]] = []

    for index, vector in enumerate(certificate["projector_pool"]["reflection_vectors"]):
        vector_column = column(vector)
        norm = IV.matmul(
            IV.matmul(IV.transpose(vector_column), form), vector_column
        )[0][0]
        require(norm != 0, f"reflection {index} singular root")
        outer = IV.matmul(
            vector_column, IV.matmul(IV.transpose(vector_column), form)
        )
        reflection = IV.add(IV.eye(11), IV.scale(pow(norm, -1, 3), outer))
        require(
            IV.matmul(IV.matmul(IV.transpose(reflection), form), reflection) == form,
            f"reflection {index} not orthogonal",
        )
        transform = IV.matmul(reflection, transform)
        basis = [row[:6] for row in transform]
        require(gram(basis, form) == IV.eye(6), f"basis {index} not orthonormal")
        projector = IV.matmul(IV.matmul(basis, IV.transpose(basis)), form)
        require(IV.matmul(projector, projector) == projector, f"projector {index} not idempotent")
        require(
            IV.matmul(IV.transpose(projector), form) == IV.matmul(form, projector),
            f"projector {index} not self-adjoint",
        )
        require(IV.matrix_rank(projector) == 6, f"projector {index} wrong rank")
        require(IV.trace(projector) == 0, f"projector {index} wrong trace")
        simplex = IV.matmul(basis, coefficient_columns)
        require(gram(simplex, form) == expected_simplex_gram, f"simplex {index} bad Gram")
        require(IV.matvec(simplex, [1] * 7) == [0] * 11, f"simplex {index} bad sum")
        require(
            frame_operator(IV.transpose(simplex), form) == IV.scale(-1, projector),
            f"simplex {index} bad frame operator",
        )
        bases.append(basis)
        projectors.append(projector)
        simplices.append(simplex)

    require(len(projectors) == 34, "wrong projector pool size")
    require(len({IV.flatten(projector) for projector in projectors}) == 34, "projectors repeat")
    return form, bases, projectors, simplices


def build_blocks(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    specification = certificate["shared_incidence"]
    blocks: list[dict[str, Any]] = []
    for component_index, component in enumerate(specification["components"]):
        offset = component["offset"]
        size = component["size"]
        for shift in range(size // 3):
            blocks.append(
                {
                    "component_index": component_index,
                    "color": 0,
                    "vertices": (
                        offset + shift,
                        offset + shift + size // 3,
                        offset + shift + 2 * size // 3,
                    ),
                }
            )
        for orbit in specification["full_orbits"]:
            for shift in range(size):
                local_vertices = sorted(
                    {(shift + item) % size for item in orbit["starter"]}
                )
                require(len(local_vertices) == 3, "degenerate block")
                blocks.append(
                    {
                        "component_index": component_index,
                        "color": orbit["first_color"] + (shift % 3),
                        "vertices": tuple(offset + item for item in local_vertices),
                    }
                )
    require(len(blocks) == 231, "wrong block count")
    return blocks


def incidence_audit(
    certificate: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[list[int]], list[list[int]], dict[str, Any]]:
    blocks = build_blocks(certificate)
    incidence = IV.zeros(99, len(blocks))
    for block_index, block in enumerate(blocks):
        for vertex in block["vertices"]:
            incidence[vertex][block_index] = 1

    row_degrees = [sum(row) for row in incidence]
    column_degrees = [
        sum(incidence[row][block] for row in range(99))
        for block in range(len(blocks))
    ]
    require(row_degrees == [7] * 99, "wrong row degrees")
    require(column_degrees == [3] * 231, "wrong column degrees")

    pair_counts = [
        [
            sum(incidence[x][block] * incidence[z][block] for block in range(231))
            for z in range(99)
        ]
        for x in range(99)
    ]
    require(
        all(pair_counts[x][z] <= 1 for x in range(99) for z in range(99) if x != z),
        "incidence not linear",
    )
    adjacency = [
        [int(x != z and pair_counts[x][z] == 1) for z in range(99)]
        for x in range(99)
    ]
    require([sum(row) for row in adjacency] == [14] * 99, "wrong graph degree")
    require(
        all(
            pair_counts[x][z] == adjacency[x][z] + (7 if x == z else 0)
            for x in range(99)
            for z in range(99)
        ),
        "integer BBt identity failed",
    )

    incident_colors = [
        sorted(block["color"] for block in blocks if vertex in block["vertices"])
        for vertex in range(99)
    ]
    require(incident_colors == [list(range(7)) for _ in range(99)], "star colors failed")

    edges = [
        (x, z)
        for x in range(99)
        for z in range(x + 1, 99)
        if adjacency[x][z]
    ]
    all_triangles = {
        (x, y, z)
        for x in range(99)
        for y in range(x + 1, 99)
        if adjacency[x][y]
        for z in range(y + 1, 99)
        if adjacency[x][z] and adjacency[y][z]
    }
    designated = {tuple(sorted(block["vertices"])) for block in blocks}
    edge_common = Counter(
        sum(adjacency[x][w] * adjacency[z][w] for w in range(99))
        for x, z in edges
    )
    nonedge_common = Counter(
        sum(adjacency[x][w] * adjacency[z][w] for w in range(99))
        for x in range(99)
        for z in range(x + 1, 99)
        if not adjacency[x][z]
    )

    unvisited = set(range(99))
    component_sizes: list[int] = []
    while unvisited:
        start = min(unvisited)
        unvisited.remove(start)
        queue = deque([start])
        size = 0
        while queue:
            vertex = queue.popleft()
            size += 1
            for neighbor, edge in enumerate(adjacency[vertex]):
                if edge and neighbor in unvisited:
                    unvisited.remove(neighbor)
                    queue.append(neighbor)
        component_sizes.append(size)

    summary = {
        "point_count": 99,
        "block_count": 231,
        "row_degree": min(row_degrees),
        "column_degree": min(column_degrees),
        "linear_triple_system": True,
        "point_graph_degree": min(map(sum, adjacency)),
        "point_graph_edge_count": len(edges),
        "connected_component_sizes": sorted(component_sizes),
        "all_graph_triangle_count": len(all_triangles),
        "designated_block_triangle_count": len(designated),
        "extra_graph_triangle_count": len(all_triangles - designated),
        "edge_common_neighbor_distribution": {
            str(key): edge_common[key] for key in sorted(edge_common)
        },
        "nonedge_common_neighbor_distribution": {
            str(key): nonedge_common[key] for key in sorted(nonedge_common)
        },
        "each_vertex_sees_each_color_once": True,
        "integer_bbt_identity_checked": True,
        "ternary_bbt_identity_checked": all(
            (pair_counts[x][z] - adjacency[x][z] - int(x == z)) % 3 == 0
            for x in range(99)
            for z in range(99)
        ),
    }
    return blocks, incidence, adjacency, summary


def normalized_direction(vector: Sequence[int]) -> tuple[int, ...]:
    pivot = next((value % 3 for value in vector if value % 3), None)
    require(pivot is not None, "zero block vector")
    inverse = pow(pivot, -1, 3)
    return tuple((inverse * value) % 3 for value in vector)


def pair_g(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> int:
    return IV.trace_product(left, right)


def pair_h(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> int:
    product = IV.matmul(left, right)
    return IV.trace_product(product, product)


def tau(
    left: Sequence[Sequence[int]],
    middle: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
) -> int:
    return IV.trace_product(IV.matmul(left, middle), IV.matmul(right, middle))


def component_of(vertex: int, components: Sequence[dict[str, Any]]) -> int:
    for index, component in enumerate(components):
        if component["offset"] <= vertex < component["offset"] + component["size"]:
            return index
    raise AssertionError("vertex outside components")


def shared_realization(
    type_indices: Sequence[int],
    certificate: dict[str, Any],
    form: Sequence[Sequence[int]],
    projectors: Sequence[Sequence[Sequence[int]]],
    simplices: Sequence[Sequence[Sequence[int]]],
    blocks: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    components = certificate["shared_incidence"]["components"]
    vertex_types = [component_of(vertex, components) for vertex in range(99)]
    point_projectors = [projectors[type_indices[kind]] for kind in vertex_types]
    block_vectors = [
        [
            simplices[type_indices[block["component_index"]]][row][block["color"]]
            for row in range(11)
        ]
        for block in blocks
    ]

    star_coupling = True
    for vertex in range(99):
        vectors = [
            block_vectors[index]
            for index, block in enumerate(blocks)
            if vertex in block["vertices"]
        ]
        if frame_operator(vectors, form) != IV.scale(-1, point_projectors[vertex]):
            star_coupling = False
            break
    require(star_coupling, "star-projector coupling failed")

    projector_sum = IV.matrix_sum(point_projectors)
    global_frame = frame_operator(block_vectors, form)
    column_matrix = IV.transpose(block_vectors)
    centered_gram = gram(column_matrix, form)
    centered_square = IV.matmul(centered_gram, centered_gram)

    full_g = [
        [pair_g(point_projectors[x], point_projectors[z]) for z in range(99)]
        for x in range(99)
    ]
    full_h = [
        [pair_h(point_projectors[x], point_projectors[z]) for z in range(99)]
        for x in range(99)
    ]
    selected = [projectors[index] for index in type_indices]
    type_tau = [
        [
            [tau(selected[x], selected[y], selected[z]) for z in range(3)]
            for y in range(3)
        ]
        for x in range(3)
    ]

    slice_summaries: list[dict[str, Any]] = []
    sizes = [component["size"] for component in components]
    for middle in range(3):
        full_slice = [
            [
                type_tau[vertex_types[x]][middle][vertex_types[z]]
                for z in range(99)
            ]
            for x in range(99)
        ]
        representative = components[middle]["offset"]
        require(full_slice == IV.transpose(full_slice), "fixed-y slice nonsymmetric")
        require(all(sum(row) % 3 == 0 for row in full_slice), "fixed-y contraction failed")
        require(full_slice[representative] == full_g[representative], "fixed-y g row failed")
        require(
            [full_slice[x][x] for x in range(99)] == full_h[representative],
            "fixed-y H diagonal failed",
        )
        slice_summaries.append(
            {
                "middle_component": middle,
                "rank_over_F3": IV.matrix_rank(full_slice),
                "row_sums_zero": True,
                "y_row_equals_g": True,
                "diagonal_equals_H": True,
            }
        )
        require(
            all(
                sum(sizes[z] * type_tau[x][middle][z] for z in range(3)) % 3 == 0
                for x in range(3)
            ),
            "type contraction failed",
        )

    directions = Counter(normalized_direction(vector) for vector in block_vectors)
    return {
        "type_indices": list(type_indices),
        "point_projectors": point_projectors,
        "block_vectors": block_vectors,
        "full_g": full_g,
        "full_H": full_h,
        "type_tau": type_tau,
        "star_projector_coupling": star_coupling,
        "sum_projectors_zero": IV.is_zero(projector_sum),
        "global_column_frame_zero": IV.is_zero(global_frame),
        "column_span_rank": IV.matrix_rank(column_matrix),
        "centered_gram_rank": IV.matrix_rank(centered_gram),
        "centered_gram_square_zero": IV.is_zero(centered_square),
        "all_block_columns_singular": all(centered_gram[i][i] == 0 for i in range(231)),
        "distinct_projective_direction_count": len(directions),
        "projective_direction_multiplicity_distribution": {
            str(key): value for key, value in sorted(Counter(directions.values()).items())
        },
        "fixed_y_slices": slice_summaries,
    }


def distribution(values: Iterable[int]) -> dict[str, int]:
    counts = Counter(value % 3 for value in values)
    return {str(value): counts[value] for value in range(3)}


def fixed_y_rank_control(
    specification: dict[str, Any],
    form: Sequence[Sequence[int]],
    projectors: Sequence[Sequence[Sequence[int]]],
    simplices: Sequence[Sequence[Sequence[int]]],
) -> dict[str, Any]:
    span = specification["projector_pool_indices"]
    unique_indices = list(range(span["start"], span["stop_exclusive"]))
    labels = [
        index
        for index in unique_indices
        for _ in range(specification["multiplicity_per_type"])
    ]
    fixed_pool_index = specification["fixed_y_pool_index"]
    fixed_label = labels.index(fixed_pool_index)
    fixed = projectors[fixed_pool_index]
    fixed_star = simplices[fixed_pool_index]
    fixed_star_adjoint = IV.rectangular_adjoint(fixed_star, form)

    unique_compressions = [
        IV.matmul(IV.matmul(fixed, projectors[index]), fixed)
        for index in unique_indices
    ]
    unique_star_matrices = [
        IV.matmul(IV.matmul(fixed_star_adjoint, projectors[index]), fixed_star)
        for index in unique_indices
    ]
    unique_coordinates = [IV.coordinates_21(matrix) for matrix in unique_star_matrices]
    metric = IV.coordinate_metric_21()
    unique_slice = IV.gram_from_vectors(unique_coordinates, metric)
    direct_unique_slice = [
        [IV.trace_product(unique_compressions[x], unique_compressions[z]) for z in range(33)]
        for x in range(33)
    ]
    require(unique_slice == direct_unique_slice, "21-coordinate slice mismatch")

    label_positions = [unique_indices.index(index) for index in labels]
    full_slice = [
        [unique_slice[label_positions[x]][label_positions[z]] for z in range(99)]
        for x in range(99)
    ]
    full_projectors = [projectors[index] for index in labels]
    require(IV.is_zero(IV.matrix_sum(full_projectors)), "rank-control projector sum nonzero")
    require(full_slice == IV.transpose(full_slice), "rank-control slice nonsymmetric")
    require(all(sum(row) % 3 == 0 for row in full_slice), "rank-control row sum nonzero")
    require(
        full_slice[fixed_label] == [pair_g(fixed, projector) for projector in full_projectors],
        "rank-control g row mismatch",
    )
    require(
        [full_slice[x][x] for x in range(99)]
        == [pair_h(fixed, projector) for projector in full_projectors],
        "rank-control H diagonal mismatch",
    )
    coordinate_rank = IV.matrix_rank(IV.columns_matrix(unique_coordinates))
    return {
        "fixed_y_pool_index": fixed_pool_index,
        "sum_projectors_zero": True,
        "unique_coordinate_rank": coordinate_rank,
        "unique_slice_rank": IV.matrix_rank(unique_slice),
        "full_slice_rank": IV.matrix_rank(full_slice),
        "full_diagonal_distribution": distribution(full_slice[x][x] for x in range(99)),
        "full_entry_distribution": distribution(value for row in full_slice for value in row),
        "unique_diagonal_distribution": distribution(unique_slice[x][x] for x in range(33)),
        "unique_entry_distribution": distribution(value for row in unique_slice for value in row),
        "slice_symmetric": True,
        "row_sums_zero": True,
        "y_row_equals_g": True,
        "diagonal_equals_H": True,
        "seven_star_21_coordinate_model_used": True,
    }


def mutation_checks(certificate: dict[str, Any]) -> dict[str, bool]:
    outcomes: dict[str, bool] = {}

    reflection_mutation = copy.deepcopy(certificate)
    reflection_mutation["projector_pool"]["reflection_vectors"][0] = [0] * 11
    try:
        projectors_from_certificate(reflection_mutation)
    except AssertionError:
        outcomes["zero_reflection_root_rejected"] = True
    else:
        outcomes["zero_reflection_root_rejected"] = False

    simplex_mutation = copy.deepcopy(certificate)
    simplex_mutation["simplex_coefficient_vectors"][0][0] = (
        simplex_mutation["simplex_coefficient_vectors"][0][0] + 1
    ) % 3
    try:
        projectors_from_certificate(simplex_mutation)
    except AssertionError:
        outcomes["simplex_mutation_rejected"] = True
    else:
        outcomes["simplex_mutation_rejected"] = False

    incidence_mutation = copy.deepcopy(certificate)
    incidence_mutation["shared_incidence"]["full_orbits"][1]["starter"] = [0, 1, 5]
    try:
        incidence_audit(incidence_mutation)
    except AssertionError:
        outcomes["incidence_orbit_mutation_rejected"] = True
    else:
        outcomes["incidence_orbit_mutation_rejected"] = False

    return outcomes


def source_ledger_audit(ledger: dict[str, Any]) -> dict[str, Any]:
    entries = {entry["identifier"]: entry for entry in ledger["sources"]}
    required = {
        "arXiv:2012.12977v2",
        "arXiv:1201.1798v2",
        "arXiv:0806.2317v1",
        "arXiv:0903.5169v1",
        "doi:10.2206/kyushujm.48.323",
        "arXiv:2110.07109v2",
        "internal-exact-linear-algebra",
    }
    require(set(entries) == required, "source ledger identifiers changed")
    require(
        "spanning" in " ".join(entries["arXiv:2012.12977v2"]["hypotheses"]).lower(),
        "finite-frame spanning hypothesis omitted",
    )
    require(
        "positive" in " ".join(entries["arXiv:1201.1798v2"]["hypotheses"]).lower()
        and "real" in " ".join(entries["arXiv:1201.1798v2"]["hypotheses"]).lower(),
        "fusion-frame real/positive hypotheses omitted",
    )
    require(
        "(2t-2)-design" in " ".join(entries["arXiv:0806.2317v1"]["hypotheses"]),
        "Roy design hypothesis omitted",
    )
    require(
        "association scheme" in " ".join(entries["arXiv:0903.5169v1"]["hypotheses"]).lower(),
        "Suda scheme hypothesis omitted",
    )
    require(
        "actual" in " ".join(entries["doi:10.2206/kyushujm.48.323"]["hypotheses"]).lower(),
        "actual SRG premise omitted",
    )
    require(
        "connected" in " ".join(entries["arXiv:2110.07109v2"]["hypotheses"]).lower(),
        "connected graph premise omitted",
    )
    return {
        "ledger_entry_count": len(entries),
        "all_required_entries_present": True,
        "finite_frame_spanning_scope_retained": True,
        "real_positive_fusion_frame_scope_retained": True,
        "complex_design_angle_annihilator_scope_retained": True,
        "triple_regularity_extra_hypotheses_retained": True,
        "terwilliger_actual_graph_basepoint_scope_retained": True,
        "bounded_non_discovery_remains_UNKNOWN": (
            ledger["bounded_non_discovery"]["claim_label"] == "UNKNOWN"
            and ledger["bounded_non_discovery"]["absence_is_nonexistence_evidence"] is False
        ),
        "manual_primary_source_check": {
            "arXiv:2012.12977v2": "Proposition 3.5 and Remark 3.7 retain the frame/spanning hypothesis, especially at c=0.",
            "arXiv:1201.1798v2": "Section 5 is real Grassmannian harmonic analysis with positive weights; Theorem 5.3, Definition 5.5, Theorem 5.7, and Remark 5.8 do not transfer to the F_3 zero-sum frame.",
            "arXiv:0806.2317v1": "Theorem 10.5 assumes a (2t-2)-design, exactly t inner products, and annihilators; its t=2 example still assumes a 2-design.",
            "arXiv:0903.5169v1": "Definition 2.7 and Lemma 2.8 start from a symmetric association scheme; Corollary 3.1 concerns tight spherical 4-designs.",
            "doi:10.2206/kyushujm.48.323": "The cited paper studies the subconstituent algebra of an actual strongly regular graph.",
            "arXiv:2110.07109v2": "The definition uses a finite connected simple graph, its adjacency matrix, and basepoint distance idempotents.",
        },
    }


def compare_to_frozen(
    audit: dict[str, Any], frozen: dict[str, Any]
) -> dict[str, bool]:
    collision = frozen["shared_incidence_tau_collision"]
    return {
        "incidence_summary_matches": all(
            audit["incidence"][key] == collision["incidence"][key]
            for key in (
                "point_count",
                "block_count",
                "row_degree",
                "column_degree",
                "linear_triple_system",
                "point_graph_degree",
                "point_graph_edge_count",
                "connected_component_sizes",
                "all_graph_triangle_count",
                "designated_block_triangle_count",
                "extra_graph_triangle_count",
                "edge_common_neighbor_distribution",
                "nonedge_common_neighbor_distribution",
                "each_vertex_sees_each_color_once",
            )
        ),
        "different_type_triples_match": (
            audit["collision"]["different_type_triples"]
            == collision["different_type_triples"]
        ),
        "different_ordered_entries_match": (
            audit["collision"]["different_ordered_tau_entries"]
            == collision["different_ordered_tau_entries"]
        ),
        "rank_control_A_matches": (
            audit["rank21_controls"]["A"]["full_slice_rank"]
            == frozen["fixed_y_rank21_controls"]["controls"]["A"]["fixed_y_slice_rank_over_F3"]
            and audit["rank21_controls"]["A"]["full_diagonal_distribution"]
            == frozen["fixed_y_rank21_controls"]["controls"]["A"]["fixed_y_slice_diagonal_distribution"]
            and audit["rank21_controls"]["A"]["full_entry_distribution"]
            == frozen["fixed_y_rank21_controls"]["controls"]["A"]["fixed_y_slice_entry_distribution"]
        ),
        "rank_control_B_matches": (
            audit["rank21_controls"]["B"]["full_slice_rank"]
            == frozen["fixed_y_rank21_controls"]["controls"]["B"]["fixed_y_slice_rank_over_F3"]
            and audit["rank21_controls"]["B"]["full_diagonal_distribution"]
            == frozen["fixed_y_rank21_controls"]["controls"]["B"]["fixed_y_slice_diagonal_distribution"]
            and audit["rank21_controls"]["B"]["full_entry_distribution"]
            == frozen["fixed_y_rank21_controls"]["controls"]["B"]["fixed_y_slice_entry_distribution"]
        ),
    }


def analyze() -> dict[str, Any]:
    certificate = load_json(DISCOVERY / "certificate.json")
    frozen = load_json(DISCOVERY / "exact-results.json")
    ledger = load_json(DISCOVERY / "literature-sources.json")
    form, bases, projectors, simplices = projectors_from_certificate(certificate)
    blocks, _incidence, _adjacency, incidence = incidence_audit(certificate)

    specifications = certificate["shared_incidence_realizations"]
    realization_a = shared_realization(
        specifications["A_projector_pool_indices_by_component"],
        certificate,
        form,
        projectors,
        simplices,
        blocks,
    )
    realization_b = shared_realization(
        specifications["B_projector_pool_indices_by_component"],
        certificate,
        form,
        projectors,
        simplices,
        blocks,
    )
    require(realization_a["full_g"] == realization_b["full_g"], "full labeled g differs")
    require(realization_a["full_H"] == realization_b["full_H"], "full labeled H differs")

    type_a = realization_a["type_tau"]
    type_b = realization_b["type_tau"]
    different_type_triples = [
        [x, y, z]
        for x in range(3)
        for y in range(3)
        for z in range(3)
        if type_a[x][y][z] != type_b[x][y][z]
    ]
    components = certificate["shared_incidence"]["components"]
    sizes = [component["size"] for component in components]
    different_ordered_entries = sum(
        sizes[x] * sizes[y] * sizes[z] for x, y, z in different_type_triples
    )
    require(
        all(sorted(triple) == [0, 1, 2] for triple in different_type_triples),
        "tau difference escapes cross-component triples",
    )

    rank_controls = {
        name: fixed_y_rank_control(specification, form, projectors, simplices)
        for name, specification in certificate["fixed_y_rank_controls"].items()
    }

    audit: dict[str, Any] = {
        "claim_label": "VERIFIED_SCOPED",
        "released_package": "attempts/wave206-three-center-hostile-controls",
        "discovery_python_imported": False,
        "blind_matrix_layer_reused": True,
        "projector_pool": {
            "count": len(projectors),
            "distinct_count": len({IV.flatten(projector) for projector in projectors}),
            "all_rank_6": all(IV.matrix_rank(projector) == 6 for projector in projectors),
            "all_trace_zero": all(IV.trace(projector) == 0 for projector in projectors),
            "all_self_adjoint_idempotent": all(
                IV.check_projector(projector, form) for projector in projectors
            ),
            "all_seven_simplices_valid": all(
                gram(simplex, form) == [[0 if i == j else 1 for j in range(7)] for i in range(7)]
                and IV.matvec(simplex, [1] * 7) == [0] * 11
                and frame_operator(IV.transpose(simplex), form) == IV.scale(-1, projector)
                for simplex, projector in zip(simplices, projectors)
            ),
            "joined_selected_basis_rank_A": IV.matrix_rank(
                [bases[0][row] + bases[2][row] + bases[9][row] for row in range(11)]
            ),
            "joined_selected_basis_rank_B": IV.matrix_rank(
                [bases[0][row] + bases[2][row] + bases[15][row] for row in range(11)]
            ),
        },
        "incidence": incidence,
        "realizations": {
            "A": {
                key: value
                for key, value in realization_a.items()
                if key not in {"point_projectors", "block_vectors", "full_g", "full_H", "type_tau"}
            },
            "B": {
                key: value
                for key, value in realization_b.items()
                if key not in {"point_projectors", "block_vectors", "full_g", "full_H", "type_tau"}
            },
        },
        "collision": {
            "same_complete_labelled_g": True,
            "same_complete_labelled_H": True,
            "tau_type_table_A": type_a,
            "tau_type_table_B": type_b,
            "different_type_triples": different_type_triples,
            "different_ordered_tau_entries": different_ordered_entries,
            "all_differences_cross_component": True,
            "refuted_implication": (
                "the checked relaxed shared-incidence, rank-11, zero-frame, "
                "star-projector, complete-g, and complete-H premises determine tau"
            ),
            "target_endpoint_counterexample": False,
        },
        "rank21_controls": rank_controls,
        "mutations": mutation_checks(certificate),
        "source_ledger": source_ledger_audit(ledger),
        "premise_gaps": {
            "shared_control": frozen["shared_incidence_tau_collision"]["missing_target_premises"],
            "rank21_controls": frozen["fixed_y_rank21_controls"]["missing_target_premises"],
            "restriction_ledger": frozen["bounded_search_ledger"],
        },
        "status": {
            "Conway-99": "UNKNOWN",
            "rank-11 endpoint": "UNKNOWN",
            "n3=4158 endpoint": "UNKNOWN",
            "actual nonedge h": "UNKNOWN",
            "Q>=7060": "NOT PROVED",
            "automorphism assumption": "NONE",
        },
    }
    audit["frozen_comparison"] = compare_to_frozen(audit, frozen)
    assert_expected(audit)
    return audit


def assert_expected(result: dict[str, Any]) -> None:
    require(result["projector_pool"]["count"] == 34, "pool count")
    require(result["projector_pool"]["distinct_count"] == 34, "pool distinctness")
    require(result["projector_pool"]["all_rank_6"], "pool ranks")
    require(result["projector_pool"]["all_self_adjoint_idempotent"], "pool projectors")
    require(result["projector_pool"]["all_seven_simplices_valid"], "pool simplices")
    require(result["projector_pool"]["joined_selected_basis_rank_A"] == 11, "A span")
    require(result["projector_pool"]["joined_selected_basis_rank_B"] == 11, "B span")

    incidence = result["incidence"]
    require(incidence["connected_component_sizes"] == [27, 36, 36], "components")
    require(incidence["point_graph_edge_count"] == 693, "edges")
    require(incidence["all_graph_triangle_count"] == 1329, "triangles")
    require(incidence["extra_graph_triangle_count"] == 1098, "extra triangles")

    for realization in result["realizations"].values():
        require(realization["star_projector_coupling"], "star coupling")
        require(realization["sum_projectors_zero"], "projector sum")
        require(realization["global_column_frame_zero"], "column frame")
        require(realization["column_span_rank"] == 11, "column span")
        require(realization["centered_gram_rank"] == 11, "D rank")
        require(realization["centered_gram_square_zero"], "D square")
        require(realization["distinct_projective_direction_count"] == 19, "directions")
        require(
            realization["projective_direction_multiplicity_distribution"]
            == {"9": 5, "12": 12, "21": 2},
            "direction multiplicities",
        )
        require(
            all(item["rank_over_F3"] == 3 for item in realization["fixed_y_slices"]),
            "shared fixed-y ranks",
        )

    collision = result["collision"]
    require(collision["same_complete_labelled_g"], "g equality")
    require(collision["same_complete_labelled_H"], "H equality")
    require(collision["different_ordered_tau_entries"] == 209952, "tau count")
    require(len(collision["different_type_triples"]) == 6, "tau support")
    require(not collision["target_endpoint_counterexample"], "scope inflation")

    expected_controls = {
        "A": ({"0": 30, "1": 33, "2": 36}, {"0": 3078, "1": 3195, "2": 3528}),
        "B": ({"0": 33, "1": 15, "2": 51}, {"0": 2925, "1": 3411, "2": 3465}),
    }
    for name, (diagonal_counts, entry_counts) in expected_controls.items():
        control = result["rank21_controls"][name]
        require(control["unique_coordinate_rank"] == 21, f"{name} coordinate rank")
        require(control["unique_slice_rank"] == 21, f"{name} unique rank")
        require(control["full_slice_rank"] == 21, f"{name} full rank")
        require(control["full_diagonal_distribution"] == diagonal_counts, f"{name} diagonal")
        require(control["full_entry_distribution"] == entry_counts, f"{name} entries")

    require(all(result["mutations"].values()), "mutation checks")
    require(all(result["frozen_comparison"].values()), "frozen result mismatch")
    require(result["source_ledger"]["bounded_non_discovery_remains_UNKNOWN"], "literature scope")


def main() -> None:
    result = analyze()
    output = HERE / "post_source_hostile_result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
