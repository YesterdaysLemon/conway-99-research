"""Independent post-source audit of the released Wave 206 Proof-A package.

No discovery Python is imported.  The only discovery inputs used are the
frozen JSON result and the four previously sealed Wave 205 cross-Gram
certificates.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROOF_A = ROOT / "attempts" / "wave206-three-center-proof-a"
CONTROLS_PATH = (
    ROOT / "attempts" / "wave205-nonedge-fourth-trace-proof-a" / "controls.json"
)
SPEC = importlib.util.spec_from_file_location(
    "wave206_blind_matrix_for_proof_a", HERE / "independent_verifier.py"
)
assert SPEC is not None and SPEC.loader is not None
IV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IV)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def controls() -> list[dict[str, Any]]:
    return load_json(CONTROLS_PATH)["controls"]


def cross(control: dict[str, Any]) -> list[list[int]]:
    return [[int(value) for value in row] for row in control["cross_gram_rows"]]


def trace_pair(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> int:
    return IV.trace_product(left, right)


OFFDIAGONAL_PAIRS = tuple(itertools.combinations(range(7), 2))


def lift_offdiagonal_21(coordinates: Sequence[int]) -> list[list[int]]:
    require(len(coordinates) == 21, "wrong off-diagonal coordinate length")
    matrix = IV.zeros(7, 7)
    for value, (left, right) in zip(coordinates, OFFDIAGONAL_PAIRS):
        matrix[left][right] = value % 3
        matrix[right][left] = value % 3
    for index in range(7):
        matrix[index][index] = -sum(matrix[index][other] for other in range(7)) % 3
    require(IV.matvec(matrix, [1] * 7) == [0] * 7, "lift lost row-zero condition")
    return matrix


def offdiagonal_coordinates(matrix: Sequence[Sequence[int]]) -> list[int]:
    require(matrix == IV.transpose(matrix), "coordinate matrix nonsymmetric")
    require(IV.matvec(matrix, [1] * 7) == [0] * 7, "coordinate matrix not row-zero")
    coordinates = [matrix[left][right] % 3 for left, right in OFFDIAGONAL_PAIRS]
    require(lift_offdiagonal_21(coordinates) == matrix, "coordinate roundtrip failed")
    return coordinates


def offdiagonal_metric() -> list[list[int]]:
    basis = [
        lift_offdiagonal_21([int(i == j) for i in range(21)])
        for j in range(21)
    ]
    return [
        [trace_pair(basis[i], basis[j]) for j in range(21)]
        for i in range(21)
    ]


def coordinate_model_audit(base_controls: Sequence[dict[str, Any]]) -> dict[str, Any]:
    star_gram = [[0 if i == j else 1 for j in range(7)] for i in range(7)]
    metric = offdiagonal_metric()
    records: dict[str, Any] = {}
    for control in base_controls:
        c = cross(control)
        compression = IV.matmul(IV.transpose(c), c)
        coordinate_matrix = IV.scale(-1, compression)
        coordinates = offdiagonal_coordinates(coordinate_matrix)
        coordinate_sum = sum(coordinates) % 3
        g_value = IV.trace(compression)
        h_value = trace_pair(compression, compression)
        quadratic = IV.trace(
            IV.matmul(
                IV.matmul(IV.matmul(coordinate_matrix, star_gram), coordinate_matrix),
                star_gram,
            )
        )
        require(g_value == 2 * coordinate_sum % 3, "linear moment failed")
        require(coordinate_sum == control["claimed_t"] % 3, "t moment failed")
        require(h_value == control["claimed_h"], "sealed h mismatch")
        require(h_value == quadratic, "quadratic moment failed")
        records[control["name"]] = {
            "t": control["claimed_t"],
            "coordinate_sum_mod_3": coordinate_sum,
            "g": g_value,
            "h": h_value,
            "quadratic_value": quadratic,
            "coordinate_roundtrip": True,
        }
    return {
        "coordinate_dimension": 21,
        "offdiagonal_coordinate_metric_rank": IV.matrix_rank(metric),
        "controls": records,
        "weighted_relation_projection_derivation": (
            "Z_y^*(sum_x c_x P_x)Z_y=0 gives sum_x c_x R_x=0, hence all 21 coordinates sum to zero"
        ),
        "weighted_relation_requires_genuine_operator_relation": True,
        "gram_kernel_word_alone_is_not_accepted": True,
    }


def graph_and_fiber_audit() -> dict[str, Any]:
    pattern = {
        "both": 2,
        "y_only": 12,
        "x_only": 12,
        "neither": 71,
    }
    require(sum(pattern.values()) == 97, "fixed nonedge count failed")

    fibers = [
        (left, right, bit_left, bit_right)
        for left, right in itertools.combinations(range(7), 2)
        for bit_left in range(2)
        for bit_right in range(2)
    ]
    require(len(fibers) == 84, "fiber partition size failed")
    require(
        len({(left, right, bit_left, bit_right) for left, right, bit_left, bit_right in fibers})
        == 84,
        "fiber labels repeat",
    )

    forbidden = {
        tuple(sorted(edge))
        for edge in (
            ("x00", "x01"),
            ("x10", "x11"),
            ("x00", "x10"),
            ("x01", "x11"),
        )
    }
    allowed = {
        tuple(sorted(("x00", "x11"))),
        tuple(sorted(("x01", "x10"))),
    }
    possible_graphs = [
        sorted(edge for index, edge in enumerate(sorted(allowed)) if mask & (1 << index))
        for mask in range(4)
    ]
    require(len({tuple(graph) for graph in possible_graphs}) == 4, "fiber graph count")

    # Verify the local prism forced by one representative forbidden edge.
    prism_vertices = {"a", "x0", "x1", "y", "b0", "b1"}
    first_triangle = {
        tuple(sorted(edge))
        for edge in (("a", "x0"), ("a", "x1"), ("x0", "x1"))
    }
    second_triangle = {
        tuple(sorted(edge))
        for edge in (("y", "b0"), ("y", "b1"), ("b0", "b1"))
    }
    forced_cross = {
        tuple(sorted(edge))
        for edge in (("y", "a"), ("b0", "x0"), ("b1", "x1"))
    }
    prism_edges = first_triangle | second_triangle | forced_cross
    degrees = Counter(vertex for edge in prism_edges for vertex in edge)
    require(set(degrees) == prism_vertices and set(degrees.values()) == {3}, "not a prism")
    require(len(prism_edges) == 9, "wrong prism edge count")

    return {
        "fixed_nonedge_pattern": pattern,
        "root_neighbor_blocks": 7,
        "root_neighbors_per_block": 2,
        "distinguished_blocks": 2,
        "fiber_count": 21,
        "vertices_per_fiber": 4,
        "total_nonneighbors_partitioned": 84,
        "forbidden_same_endpoint_edges": [list(edge) for edge in sorted(forbidden)],
        "allowed_opposite_diagonals": [list(edge) for edge in sorted(allowed)],
        "possible_induced_fiber_graph_count": len(possible_graphs),
        "representative_forbidden_edge_forces_induced_triangular_prism": True,
        "matching_lemma_scope": "conditional on SRG lambda=1, mu=2 and prism-free P=0",
    }


def binary_degree_two_matrices() -> Iterable[list[list[int]]]:
    patterns = [
        list(pattern)
        for pattern in itertools.product((0, 1), repeat=6)
        if sum(pattern) == 2
    ]

    def recurse(
        rows: list[list[int]], row_index: int, remaining_columns: list[int]
    ) -> Iterable[list[list[int]]]:
        if row_index == 6:
            if remaining_columns == [0] * 6:
                yield rows
            return
        rows_after = 5 - row_index
        for row in patterns:
            remaining = [
                remaining_columns[column] - row[column] for column in range(6)
            ]
            if min(remaining) < 0 or any(value > rows_after for value in remaining):
                continue
            yield from recurse(rows + [row], row_index + 1, remaining)

    yield from recurse([], 0, [2] * 6)


def full_edge_cross(incidence: Sequence[Sequence[int]]) -> list[list[int]]:
    return (
        [[0] + [1] * 6]
        + [
            [1] + [(1 + incidence[row][column]) % 3 for column in range(6)]
            for row in range(6)
        ]
    )


def edge_census() -> tuple[dict[str, Any], list[list[list[int]]]]:
    unique: dict[tuple[int, ...], list[list[int]]] = {}
    labelled = 0
    for incidence in binary_degree_two_matrices():
        c = full_edge_cross(incidence)
        compression = IV.matmul(c, IV.transpose(c))
        unique.setdefault(IV.flatten(compression), compression)
        labelled += 1
    compressions = [unique[key] for key in sorted(unique)]
    profile = Counter(
        (IV.matrix_rank(matrix), IV.trace(matrix), trace_pair(matrix, matrix))
        for matrix in compressions
    )
    return (
        {
            "labelled_degree_two_biadjacency_matrices": labelled,
            "unique_compressions": len(compressions),
            "profile_rank_g_h": {
                f"{rank},{g},{h}": count
                for (rank, g, h), count in sorted(profile.items())
            },
        },
        compressions,
    )


def determinant(matrix: Sequence[Sequence[int]]) -> int:
    size = len(matrix)
    work = [[value % 3 for value in row] for row in matrix]
    result = 1
    for column_index in range(size):
        pivot = next(
            (row for row in range(column_index, size) if work[row][column_index]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column_index:
            work[column_index], work[pivot] = work[pivot], work[column_index]
            result = -result % 3
        pivot_value = work[column_index][column_index]
        result = result * pivot_value % 3
        inverse = pow(pivot_value, -1, 3)
        for row in range(column_index + 1, size):
            factor = work[row][column_index] * inverse % 3
            work[row] = [
                (work[row][col] - factor * work[column_index][col]) % 3
                for col in range(size)
            ]
    return result


def rref_and_pivots(
    matrix: Sequence[Sequence[int]],
) -> tuple[list[list[int]], list[int]]:
    work = [[value % 3 for value in row] for row in matrix]
    if not work:
        return [], []
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots: list[int] = []
    for column_index in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column_index]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column_index], -1, 3)
        work[pivot_row] = [inverse * value % 3 for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column_index] == 0:
                continue
            factor = work[row][column_index]
            work[row] = [
                (work[row][col] - factor * work[pivot_row][col]) % 3
                for col in range(columns)
            ]
        pivots.append(column_index)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivots


def nullspace(matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    reduced, pivots = rref_and_pivots(matrix)
    width = len(matrix[0])
    free = [column for column in range(width) if column not in pivots]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % 3
        basis.append(vector)
    return basis


def minimum_code_weight(basis: Sequence[Sequence[int]]) -> int:
    return min(
        sum(value != 0 for value in vector)
        for coefficients in itertools.product(range(3), repeat=len(basis))
        if any(coefficients)
        for vector in [
            [
                sum(coefficients[i] * basis[i][j] for i in range(len(basis))) % 3
                for j in range(len(basis[0]))
            ]
        ]
    )


def full_two_star_gram(cross_matrix: Sequence[Sequence[int]]) -> list[list[int]]:
    star = [[0 if i == j else 1 for j in range(7)] for i in range(7)]
    return (
        [star[row] + list(cross_matrix[row]) for row in range(7)]
        + [
            [cross_matrix[row][column] for row in range(7)] + star[column]
            for column in range(7)
        ]
    )


def normalized_boundary(
    top_distinct: int, left_distinct: int
) -> tuple[list[list[int]], list[list[int]], list[int], list[int]]:
    top_extra = [0, int(bool(top_distinct))]
    left_extra = [0, int(bool(left_distinct))]
    top = [
        [1, 2] + [2 if column == top_extra[0] else 1 for column in range(5)],
        [2, 1] + [2 if column == top_extra[1] else 1 for column in range(5)],
    ]
    first_two = [
        [2 if row == left_extra[0] else 1, 2 if row == left_extra[1] else 1]
        for row in range(5)
    ]
    row_sums = [6 - sum(row) for row in first_two]
    column_sums = [
        6 - top[0][column + 2] - top[1][column + 2] for column in range(5)
    ]
    return top, first_two, row_sums, column_sums


def binary_matrices_with_margins(
    row_sums: Sequence[int], column_sums: Sequence[int]
) -> Iterable[list[list[int]]]:
    row_patterns = [
        [
            list(pattern)
            for pattern in itertools.product((0, 1), repeat=5)
            if sum(pattern) == row_sum
        ]
        for row_sum in row_sums
    ]

    def recurse(
        rows: list[list[int]], row_index: int, remaining_columns: list[int]
    ) -> Iterable[list[list[int]]]:
        if row_index == 5:
            if remaining_columns == [0] * 5:
                yield rows
            return
        rows_after = 4 - row_index
        for row in row_patterns[row_index]:
            remaining = [
                remaining_columns[column] - row[column] for column in range(5)
            ]
            if min(remaining) < 0 or any(value > rows_after for value in remaining):
                continue
            yield from recurse(rows + [row], row_index + 1, remaining)

    yield from recurse([], 0, list(column_sums))


def low_t_core_matrices(
    row_sums: Sequence[int], column_sums: Sequence[int], core_twos: int
) -> Iterable[list[list[int]]]:
    if core_twos == 0:
        yield from binary_matrices_with_margins(row_sums, column_sums)
        return
    require(core_twos == 1, "only t=6,7 allowed")
    for double_row in range(5):
        for double_column in range(5):
            residual_rows = list(row_sums)
            residual_columns = list(column_sums)
            residual_rows[double_row] -= 2
            residual_columns[double_column] -= 2
            if min(residual_rows) < 0 or min(residual_columns) < 0:
                continue
            for binary in binary_matrices_with_margins(residual_rows, residual_columns):
                if binary[double_row][double_column]:
                    continue
                core = [row[:] for row in binary]
                core[double_row][double_column] = 2
                yield core


def normalized_low_t_matrices(t_value: int) -> Iterable[list[list[int]]]:
    require(t_value in (6, 7), "only t=6,7 allowed")
    for top_distinct in (0, 1):
        for left_distinct in (0, 1):
            top, first_two, row_sums, column_sums = normalized_boundary(
                top_distinct, left_distinct
            )
            for core in low_t_core_matrices(row_sums, column_sums, t_value - 6):
                yield top + [
                    first_two[row] + core[row] for row in range(5)
                ]


def low_t_marked_census() -> dict[str, Any]:
    output: dict[str, Any] = {}
    for t_value in (6, 7):
        counts: Counter[tuple[int, int]] = Counter()
        normalized_total = 0
        for c in normalized_low_t_matrices(t_value):
            normalized_total += 1
            full_gram = full_two_star_gram(c)
            _, pivots = rref_and_pivots(full_gram)
            rank = len(pivots)
            discriminant = (
                determinant([[full_gram[i][j] for j in pivots] for i in pivots])
                if rank <= 11
                else 0
            )
            distance = minimum_code_weight(nullspace(full_gram))
            if rank != 11 or discriminant != 2 or distance < 4:
                continue
            compression = IV.matmul(c, IV.transpose(c))
            h_value = trace_pair(compression, compression)
            marked_r = -compression[0][1] % 3
            counts[(h_value, marked_r)] += 1
        output[str(t_value)] = {
            "normalized_total": normalized_total,
            "admissible_total": sum(counts.values()),
            "counts_by_h_and_r": {
                f"{h},{r}": count for (h, r), count in sorted(counts.items())
            },
        }
    return output


def permute_matrix(
    matrix: Sequence[Sequence[int]], base_to_target: Sequence[int]
) -> list[list[int]]:
    inverse = [0] * 7
    for base, target in enumerate(base_to_target):
        inverse[target] = base
    return [
        [matrix[inverse[row]][inverse[column]] for column in range(7)]
        for row in range(7)
    ]


def edge_options_at_block(
    compressions: Sequence[Sequence[Sequence[int]]], block: int
) -> list[list[list[int]]]:
    mapping = list(range(7))
    mapping[0], mapping[block] = mapping[block], mapping[0]
    return [permute_matrix(matrix, mapping) for matrix in compressions]


def nonedge_options_at_pair(
    pair: tuple[int, int], base_controls: Sequence[dict[str, Any]]
) -> list[list[list[int]]]:
    remaining = [index for index in range(7) if index not in pair]
    unique: dict[tuple[int, ...], list[list[int]]] = {}
    for control in base_controls:
        c = cross(control)
        compression = IV.matmul(c, IV.transpose(c))
        for special_order in (list(pair), list(reversed(pair))):
            for ordinary_order in itertools.permutations(remaining):
                matrix = permute_matrix(compression, special_order + list(ordinary_order))
                unique.setdefault(IV.flatten(matrix), matrix)
    return [unique[key] for key in sorted(unique)]


def marginal_and_scalar_audit(
    base_controls: Sequence[dict[str, Any]],
    edge_compressions: Sequence[Sequence[Sequence[int]]],
) -> dict[str, Any]:
    edge_options = {
        block: edge_options_at_block(edge_compressions, block) for block in range(7)
    }
    nonedge_options = {
        pair: nonedge_options_at_pair(pair, base_controls)
        for pair in itertools.combinations(range(7), 2)
    }
    require(all(len(options) == 270 for options in nonedge_options.values()), "nonedge option count")
    output: dict[str, Any] = {}
    for fixed in base_controls:
        c = cross(fixed)
        fixed_compression = IV.matmul(IV.transpose(c), c)
        edge_values = {
            str(block): sorted(
                {trace_pair(fixed_compression, option) for option in edge_options[block]}
            )
            for block in range(7)
        }
        nonedge_values = {
            f"{pair[0]},{pair[1]}": sorted(
                {trace_pair(fixed_compression, option) for option in nonedge_options[pair]}
            )
            for pair in itertools.combinations(range(7), 2)
        }
        require(all(values == [0, 1, 2] for values in edge_values.values()), "edge tau range")
        require(
            all(values == [0, 1, 2] for values in nonedge_values.values()),
            "nonedge tau range",
        )
        g_value = IV.trace(fixed_compression)
        h_value = trace_pair(fixed_compression, fixed_compression)
        target = -g_value - h_value
        target %= 3
        # The root-relative multiplicities are 14 edge centers and 83 other
        # nonneighbors (four in each fiber except the frozen x itself).
        scalar_entries = [target] + [0] * 13 + [0] * 83
        require(len(scalar_entries) == 97, "scalar ledger length")
        require(sum(scalar_entries) % 3 == target, "scalar ledger contraction")
        output[fixed["name"]] = {
            "g": g_value,
            "h": h_value,
            "required_sum": target,
            "edge_values_by_block": edge_values,
            "nonedge_values_by_pair": nonedge_values,
            "edge_entry_count": 14,
            "other_nonedge_entry_count": 83,
            "ledger_entry_count": len(scalar_entries),
            "ledger_sum": sum(scalar_entries) % 3,
            "every_entry_has_a_root_relative_marginal_module": True,
            "x_z_pair_module_imposed": False,
            "common_operator_sum_imposed": False,
            "shared_231_columns_imposed": False,
        }
    return output


def formal_zero_sum_controls(base_controls: Sequence[dict[str, Any]]) -> dict[str, Any]:
    star_gram = [[0 if i == j else 1 for j in range(7)] for i in range(7)]
    root_identity = IV.matmul(star_gram, star_gram)
    zero = IV.zeros(7, 7)
    output: dict[str, Any] = {}
    for fixed in base_controls:
        c = cross(fixed)
        fixed_compression = IV.matmul(IV.transpose(c), c)
        residual = IV.scale(-1, IV.add(root_identity, fixed_compression))
        operators = [root_identity, fixed_compression, residual] + [zero] * 96
        require(IV.is_zero(IV.matrix_sum(operators)), "formal operator sum")
        gram_matrix = [
            [trace_pair(left, right) for right in operators]
            for left in operators
        ]
        require(gram_matrix == IV.transpose(gram_matrix), "formal Gram symmetry")
        require(all(sum(row) % 3 == 0 for row in gram_matrix), "formal row sums")
        output[fixed["name"]] = {
            "operator_count": 99,
            "operator_sum_zero": True,
            "tau_gram_rank": IV.matrix_rank(gram_matrix),
            "tau_gram_symmetric": True,
            "tau_gram_row_sums_zero": True,
            "residual_graph_derived": False,
        }
    return output


def analyze() -> dict[str, Any]:
    frozen = load_json(PROOF_A / "exact-results.json")
    base_controls = controls()
    edge_summary, edge_compressions = edge_census()
    low_t = low_t_marked_census()
    marginal = marginal_and_scalar_audit(base_controls, edge_compressions)
    coordinate = coordinate_model_audit(base_controls)
    graph = graph_and_fiber_audit()
    formal = formal_zero_sum_controls(base_controls)

    result: dict[str, Any] = {
        "claim_label": "VERIFIED_SCOPED",
        "released_package": "attempts/wave206-three-center-proof-a",
        "discovery_python_imported": False,
        "fixed_y_operator_and_coordinate_model": coordinate,
        "graph_patterns_and_fibers": graph,
        "edge_module_census": edge_summary,
        "marked_coordinate_low_t_census": low_t,
        "marginal_tau_and_scalar_ledgers": marginal,
        "formal_zero_sum_operator_controls": formal,
        "scope_correction": {
            "root_relation_and_y_star_placement_determine_tau": False,
            "x_z_pair_module_imposed": False,
            "full_labelled_three_center_graph_type_determines_tau": "UNKNOWN",
            "simultaneous_shared_operator_completion": "UNKNOWN",
            "shared_231_column_realization": False,
            "t_at_least_8_modules": "UNTESTED",
            "rank_11_endpoint_excluded": False,
            "Conway_99": "UNKNOWN",
        },
        "frozen_comparison": {
            "edge_census_matches": (
                edge_summary["labelled_degree_two_biadjacency_matrices"]
                == frozen["edge_module_census"]["labelled_degree_two_biadjacency_matrices"]
                and edge_summary["unique_compressions"]
                == frozen["edge_module_census"]["unique_compressions"]
            ),
            "low_t_census_matches": all(
                low_t[t]["counts_by_h_and_r"]
                == frozen["marked_coordinate_low_t_census"]["census"][t]["counts_by_h_and_r"]
                for t in ("6", "7")
            ),
            "marginal_residue_sets_match": all(
                all(values == [0, 1, 2] for values in item["edge_values_by_block"].values())
                and all(values == [0, 1, 2] for values in item["nonedge_values_by_pair"].values())
                for item in marginal.values()
            ),
            "scope_matches": (
                frozen["conclusions"]["full_labelled_three_center_graph_type_determines_tau"]
                == "UNKNOWN"
                and frozen["conclusions"]["combined_shared_operator_and_graph_module_completion"]
                == "UNKNOWN"
                and frozen["conclusions"]["rank_11_endpoint_excluded"] is False
            ),
        },
        "status": {
            "Conway-99": "UNKNOWN",
            "rank-11 endpoint": "UNKNOWN",
            "n3=4158 endpoint": "UNKNOWN",
            "actual nonedge h": "UNKNOWN",
            "automorphism assumption": "NONE",
        },
    }
    assert_expected(result)
    return result


def assert_expected(result: dict[str, Any]) -> None:
    coordinate = result["fixed_y_operator_and_coordinate_model"]
    require(coordinate["coordinate_dimension"] == 21, "coordinate dimension")
    require(coordinate["offdiagonal_coordinate_metric_rank"] == 21, "coordinate metric")
    require(coordinate["weighted_relation_requires_genuine_operator_relation"], "relation scope")
    require(coordinate["gram_kernel_word_alone_is_not_accepted"], "Gram-kernel scope")

    graph = result["graph_patterns_and_fibers"]
    require(graph["fixed_nonedge_pattern"] == {"both": 2, "y_only": 12, "x_only": 12, "neither": 71}, "pattern")
    require(graph["fiber_count"] == 21 and graph["total_nonneighbors_partitioned"] == 84, "fibers")
    require(graph["possible_induced_fiber_graph_count"] == 4, "fiber graphs")
    require(graph["representative_forbidden_edge_forces_induced_triangular_prism"], "prism")

    edge = result["edge_module_census"]
    require(edge["labelled_degree_two_biadjacency_matrices"] == 67_950, "edge labelled count")
    require(edge["unique_compressions"] == 130, "edge compression count")
    require(
        edge["profile_rank_g_h"]
        == {"3,0,0": 15, "4,0,0": 60, "4,0,1": 45, "6,0,0": 10},
        "edge profile",
    )

    require(
        result["marked_coordinate_low_t_census"]["6"]["counts_by_h_and_r"]
        == {"1,1": 18},
        "t6 marked census",
    )
    require(
        result["marked_coordinate_low_t_census"]["7"]["counts_by_h_and_r"]
        == {"0,0": 288, "0,1": 9, "1,0": 144, "1,1": 180, "2,0": 144},
        "t7 marked census",
    )
    for ledger in result["marginal_tau_and_scalar_ledgers"].values():
        require(ledger["ledger_entry_count"] == 97, "ledger length")
        require(ledger["ledger_sum"] == ledger["required_sum"], "ledger sum")
        require(not ledger["x_z_pair_module_imposed"], "x-z scope inflation")
        require(not ledger["common_operator_sum_imposed"], "operator scope inflation")
        require(not ledger["shared_231_columns_imposed"], "column scope inflation")

    scope = result["scope_correction"]
    require(not scope["x_z_pair_module_imposed"], "x-z pair falsely imposed")
    require(
        scope["full_labelled_three_center_graph_type_determines_tau"] == "UNKNOWN",
        "triple type status inflation",
    )
    require(scope["simultaneous_shared_operator_completion"] == "UNKNOWN", "completion inflation")
    require(not scope["rank_11_endpoint_excluded"], "endpoint inflation")
    require(scope["Conway_99"] == "UNKNOWN", "Conway status")
    require(all(result["frozen_comparison"].values()), "frozen mismatch")


def main() -> None:
    result = analyze()
    output = HERE / "post_source_proof_a_result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
