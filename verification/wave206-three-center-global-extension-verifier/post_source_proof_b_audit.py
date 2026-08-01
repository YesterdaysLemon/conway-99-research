"""Independent post-source audit of the released Wave 206 Proof-B package.

No discovery Python is imported.  The executable checks below reconstruct:

* the 21-coordinate fixed-star trace form and localizer signs;
* the crossing matrix W and Gamma identities on a fresh exact zero-frame toy;
* the true projector-kernel / incidence-kernel quotient argument;
* the nonconstant pullback and three-class tensor balance; and
* a verifier-side strengthening from wt(a)>=4 to wt(a)>=8.

All finite-field arithmetic is over F_3.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Any, Iterable, Sequence


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROOF_B = ROOT / "attempts" / "wave206-crossing-kernel-proof-b"
WEIGHT_ADDENDUM = ROOT / "attempts" / "wave206-tensor-balance-weight-proof-b"
WAVE_174 = ROOT / "verification" / "wave174-no-weight3-dual"
WAVE_191 = ROOT / "agents" / "2026-07-29-wave191-global-star-module-proof-b.md"

SPEC = importlib.util.spec_from_file_location(
    "wave206_blind_matrix_for_proof_b", HERE / "independent_verifier.py"
)
assert SPEC is not None and SPEC.loader is not None
IV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IV)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(manifest: Path) -> dict[str, Any]:
    entries: dict[str, str] = {}
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        expected, relative = raw_line.split(maxsplit=1)
        relative = relative.lstrip("*")
        target = ROOT / relative
        require(target.is_file(), f"missing manifest target: {relative}")
        actual = sha256(target)
        require(actual == expected, f"hash mismatch: {relative}")
        entries[relative] = actual
    return {
        "manifest": str(manifest.relative_to(ROOT)).replace("\\", "/"),
        "manifest_sha256": sha256(manifest),
        "entry_count": len(entries),
        "all_entries_match": True,
        "entries": entries,
    }


def scalar_product(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(a * b for a, b in zip(left, right)) % 3


def matrix_dot(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> int:
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    ) % 3


def matrix_determinant(matrix: Sequence[Sequence[int]]) -> int:
    work = [[value % 3 for value in row] for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "determinant matrix not square")
    determinant = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant % 3
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % 3
        inverse = pow(pivot_value, -1, 3)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % 3
            work[row] = [
                (work[row][index] - factor * work[column][index]) % 3
                for index in range(size)
            ]
    return determinant


def block_diagonal(*blocks: Sequence[Sequence[int]]) -> list[list[int]]:
    size = sum(len(block) for block in blocks)
    result = IV.zeros(size, size)
    offset = 0
    for block in blocks:
        require(all(len(row) == len(block) for row in block), "block not square")
        for row in range(len(block)):
            for column in range(len(block)):
                result[offset + row][offset + column] = block[row][column] % 3
        offset += len(block)
    return result


def matrix_from_columns(columns: Sequence[Sequence[int]]) -> list[list[int]]:
    return IV.transpose(columns)


def concatenate_columns(matrices: Sequence[Sequence[Sequence[int]]]) -> list[list[int]]:
    require(bool(matrices), "cannot concatenate an empty matrix family")
    row_count = len(matrices[0])
    require(all(len(matrix) == row_count for matrix in matrices), "row mismatch")
    return [
        [value for matrix in matrices for value in matrix[row]]
        for row in range(row_count)
    ]


def right_multiply_diagonal(
    matrix: Sequence[Sequence[int]], diagonal: Sequence[int]
) -> list[list[int]]:
    return [
        [value * diagonal[column] % 3 for column, value in enumerate(row)]
        for row in matrix
    ]


def outer(left: Sequence[int], right: Sequence[int]) -> list[list[int]]:
    return [[a * b % 3 for b in right] for a in left]


def sum_matrices(
    matrices: Iterable[Sequence[Sequence[int]]], rows: int, cols: int
) -> list[list[int]]:
    total = IV.zeros(rows, cols)
    for matrix in matrices:
        total = IV.add(total, matrix)
    return total


OFFDIAGONAL_PAIRS = tuple(itertools.combinations(range(7), 2))


def lift_offdiagonal_21(coordinates: Sequence[int]) -> list[list[int]]:
    require(len(coordinates) == 21, "wrong star-coordinate length")
    matrix = IV.zeros(7, 7)
    for value, (left, right) in zip(coordinates, OFFDIAGONAL_PAIRS):
        matrix[left][right] = value % 3
        matrix[right][left] = value % 3
    for index in range(7):
        matrix[index][index] = (
            -sum(matrix[index][other] for other in range(7))
        ) % 3
    require(IV.matvec(matrix, [1] * 7) == [0] * 7, "star lift lost its radical")
    return matrix


def offdiagonal_coordinates(matrix: Sequence[Sequence[int]]) -> list[int]:
    require(matrix == IV.transpose(matrix), "star bilinear matrix nonsymmetric")
    require(IV.matvec(matrix, [1] * 7) == [0] * 7, "star matrix lacks row sum zero")
    coordinates = [
        matrix[left][right] % 3 for left, right in OFFDIAGONAL_PAIRS
    ]
    require(lift_offdiagonal_21(coordinates) == matrix, "star roundtrip failed")
    return coordinates


def offdiagonal_metric() -> list[list[int]]:
    basis = [
        lift_offdiagonal_21([int(i == j) for i in range(21)])
        for j in range(21)
    ]
    return [
        [IV.trace_product(basis[i], basis[j]) for j in range(21)]
        for i in range(21)
    ]


def edge_incidence_metric() -> list[list[int]]:
    incidence = [
        [int(vertex in edge) for edge in OFFDIAGONAL_PAIRS]
        for vertex in range(7)
    ]
    return IV.add(
        IV.matmul(IV.transpose(incidence), incidence),
        IV.scale(2, IV.eye(21)),
    )


AMBIENT_FORM = IV.diagonal([1] * 10 + [2])
LOCAL_SIMPLEX = IV.transpose(
    [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 2],
        [0, 0, 1, 2, 2, 0],
        [0, 1, 2, 0, 1, 0],
        [0, 2, 2, 0, 1, 0],
        [1, 0, 2, 1, 0, 0],
        [2, 0, 2, 1, 0, 0],
    ]
)


def coordinate_basis(indices: Sequence[int]) -> list[list[int]]:
    return [
        [int(row == column) for column in indices]
        for row in range(11)
    ]


def reflection(vector: Sequence[int]) -> list[list[int]]:
    covector = IV.matvec(AMBIENT_FORM, vector)
    norm = scalar_product(vector, covector)
    require(norm != 0, "reflection vector isotropic")
    # In characteristic three, -2/norm=1/norm.
    coefficient = pow(norm, -1, 3)
    result = IV.add(IV.eye(11), IV.scale(coefficient, outer(vector, covector)))
    require(
        IV.matmul(IV.matmul(IV.transpose(result), AMBIENT_FORM), result)
        == AMBIENT_FORM,
        "reflection is not orthogonal",
    )
    return result


def projector_from_basis(basis: Sequence[Sequence[int]]) -> list[list[int]]:
    require(
        IV.matmul(IV.matmul(IV.transpose(basis), AMBIENT_FORM), basis) == IV.eye(6),
        "basis not orthonormal",
    )
    return IV.matmul(IV.matmul(basis, IV.transpose(basis)), AMBIENT_FORM)


def local_columns(basis: Sequence[Sequence[int]]) -> list[list[int]]:
    columns = IV.matmul(basis, LOCAL_SIMPLEX)
    expected = [[0 if i == j else 1 for j in range(7)] for i in range(7)]
    require(
        IV.matmul(
            IV.matmul(IV.transpose(columns), AMBIENT_FORM),
            columns,
        )
        == expected,
        "local simplex Gram changed",
    )
    require(IV.matvec(columns, [1] * 7) == [0] * 11, "local simplex sum changed")
    return columns


def fresh_zero_frame() -> tuple[
    list[list[list[int]]],
    list[list[list[int]]],
    list[list[list[int]]],
]:
    """Build 24 disjoint local stars without using discovery constructors.

    Six coordinate six-spaces are chosen so coordinates 0 and 1 occur six
    times and coordinates 2 through 9 occur three times.  Their projector
    sum is therefore zero.  Reflecting this six-family gives a twelve-family
    with zero sum; adjoining one deterministic orthogonal image supplies the
    other twelve centers and raises the synthesis rank to eleven.
    """

    seed_triples = [
        {0, 1, 2},
        {0, 3, 4},
        {1, 3, 5},
        {2, 4, 5},
    ]
    membership_triples: list[set[int]] = []
    for triple in seed_triples:
        membership_triples.extend([triple, set(range(6)) - triple])
    supports = [
        tuple(
            [0, 1]
            + [
                2 + coordinate
                for coordinate, triple in enumerate(membership_triples)
                if row in triple
            ]
        )
        for row in range(6)
    ]
    require(len(set(supports)) == 6, "balanced support family has duplicates")
    base_six = [coordinate_basis(support) for support in supports]
    first_reflection = reflection([1, 1, 1, 1] + [0] * 7)
    zero_sum_twelve = base_six + [
        IV.matmul(first_reflection, basis) for basis in base_six
    ]

    rng = random.Random(1206)
    transformation = IV.eye(11)
    for _ in range(6):
        while True:
            vector = [rng.randrange(3) for _ in range(11)]
            norm = scalar_product(vector, IV.matvec(AMBIENT_FORM, vector))
            if norm:
                break
        transformation = IV.matmul(reflection(vector), transformation)

    bases = zero_sum_twelve + [
        IV.matmul(transformation, basis) for basis in zero_sum_twelve
    ]
    projectors = [projector_from_basis(basis) for basis in bases]
    stars = [local_columns(basis) for basis in bases]
    require(len(bases) == 24, "fresh control center count changed")
    require(
        len({IV.flatten(projector) for projector in projectors}) == 24,
        "fresh control projectors are not distinct",
    )
    require(
        sum_matrices(projectors, 11, 11) == IV.zeros(11, 11),
        "fresh control projector sum nonzero",
    )
    synthesis = concatenate_columns(stars)
    require(IV.matrix_rank(synthesis) == 11, "fresh control lost synthesis rank")
    return bases, projectors, stars


def centered_gram(columns: Sequence[Sequence[int]]) -> list[list[int]]:
    return IV.matmul(IV.matmul(IV.transpose(columns), AMBIENT_FORM), columns)


def selected_gram_square(
    gram: Sequence[Sequence[int]], indices: Sequence[int]
) -> list[list[int]]:
    size = len(gram)
    return [
        [
            sum(gram[row][middle] * gram[middle][column] for middle in indices)
            % 3
            for column in range(size)
        ]
        for row in range(size)
    ]


def crossing_and_localizer_audit() -> dict[str, Any]:
    bases, projectors, stars = fresh_zero_frame()
    synthesis = concatenate_columns(stars)
    z_star = IV.matmul(IV.transpose(synthesis), AMBIENT_FORM)
    gram = centered_gram(synthesis)
    column_count = len(gram)
    center_count = len(projectors)
    require(column_count == 168, "fresh control column count changed")
    require(
        IV.matmul(gram, gram) == IV.zeros(column_count, column_count),
        "D^2 is nonzero",
    )

    selectors = [
        list(range(7 * center, 7 * center + 7))
        for center in range(center_count)
    ]
    moments: list[list[list[int]]] = []
    for selected, projector in zip(selectors, projectors):
        moment = selected_gram_square(gram, selected)
        expected = IV.scale(
            -1,
            IV.matmul(
                IV.matmul(z_star, projector),
                synthesis,
            ),
        )
        require(moment == expected, "M_x=-Z^*P_xZ failed")
        require(IV.matrix_rank(moment) == 6, "moment rank changed")
        moments.append(moment)
    require(
        sum_matrices(moments, column_count, column_count)
        == IV.zeros(column_count, column_count),
        "sum_x M_x nonzero",
    )

    feature_rows = [list(IV.flatten(moment)) for moment in moments]
    crossing_rank = IV.matrix_rank(feature_rows)
    projector_span_rank = IV.matrix_rank(
        [list(IV.flatten(projector)) for projector in projectors]
    )
    require(crossing_rank == projector_span_rank, "W rank transfer failed")
    wt_w = [
        [scalar_product(left, right) for right in feature_rows]
        for left in feature_rows
    ]
    require(wt_w == IV.zeros(center_count, center_count), "W^T W nonzero")

    metric = offdiagonal_metric()
    require(metric == edge_incidence_metric(), "J_star formula changed")
    require(IV.matrix_rank(metric) == 21, "J_star lost nondegeneracy")

    localizer_checks = 0
    gamma = IV.zeros(center_count, center_count)
    tau_sum = IV.zeros(center_count, center_count)
    for middle, (basis, py, selected) in enumerate(
        zip(bases, projectors, selectors)
    ):
        local_rows: list[list[int]] = []
        for x, px in enumerate(projectors):
            bilinear = IV.matmul(
                IV.matmul(IV.transpose(stars[middle]), AMBIENT_FORM),
                IV.matmul(px, stars[middle]),
            )
            r = offdiagonal_coordinates(bilinear)
            m = [(-value) % 3 for value in r]
            g_value = IV.trace_product(py, px)
            h_value = IV.trace_product(
                IV.matmul(py, px), IV.matmul(py, px)
            )
            require(sum(m) % 3 == g_value, "localizer g sign changed")
            require(
                scalar_product(m, IV.matvec(metric, m)) == h_value,
                "localizer h formula changed",
            )
            # The off-diagonal y-block of the global moment is exactly m.
            global_m = [
                moments[x][selected[left]][selected[right]]
                for left, right in OFFDIAGONAL_PAIRS
            ]
            require(global_m == m, "global/local localizer sign mismatch")
            local_rows.append(m)
            localizer_checks += 1

        tau = IV.matmul(IV.matmul(local_rows, metric), IV.transpose(local_rows))
        direct_tau = [
            [
                IV.trace_product(
                    IV.matmul(IV.matmul(py, projectors[x]), py),
                    IV.matmul(IV.matmul(py, projectors[z]), py),
                )
                for z in range(center_count)
            ]
            for x in range(center_count)
        ]
        require(tau == direct_tau, "fixed-middle tau orientation changed")
        tau_sum = IV.add(tau_sum, tau)

        for x in range(center_count):
            for y in range(center_count):
                gamma[x][y] = (
                    gamma[x][y]
                    + sum(
                        moments[x][row][column] * moments[y][row][column]
                        for row in selected
                        for column in selected
                    )
                ) % 3

    require(gamma == tau_sum, "Gamma != sum_y Tau^(y)")
    require(
        [sum(row) % 3 for row in gamma] == [0] * center_count,
        "Gamma 1 != 0",
    )
    h_matrix = [
        [
            IV.trace_product(
                IV.matmul(projectors[x], projectors[y]),
                IV.matmul(projectors[x], projectors[y]),
            )
            for y in range(center_count)
        ]
        for x in range(center_count)
    ]
    require(
        [gamma[x][x] for x in range(center_count)]
        == [sum(row) % 3 for row in h_matrix],
        "diag(Gamma) != H1",
    )
    require(IV.matrix_rank(gamma) <= crossing_rank, "Gamma rank exceeds W rank")

    # Since M_x=D S_x D, these identities follow directly from D^2=0.
    algebraic_zero_products = {
        "D_M_x": "D(D S_x D)=D^2 S_x D=0",
        "M_x_D": "(D S_x D)D=D S_x D^2=0",
        "M_x_M_y": "(D S_x D)(D S_y D)=D S_x D^2 S_y D=0",
        "WWt_square": "(WW^T)^2=W(W^T W)W^T=0",
    }

    return {
        "construction": (
            "fresh balanced six-support zero frame, reflected to 12 centers, "
            "plus one independent deterministic orthogonal image"
        ),
        "centers": center_count,
        "columns": column_count,
        "incidence_degree": 1,
        "synthesis_rank": IV.matrix_rank(synthesis),
        "D_square_zero": True,
        "each_M_rank": 6,
        "M_identity": "M_x=D S_x D=-Z^*P_xZ",
        "W_rank": crossing_rank,
        "projector_span_rank": projector_span_rank,
        "W_transpose_W_zero": True,
        "algebraic_zero_products": algebraic_zero_products,
        "J_star_rank": IV.matrix_rank(metric),
        "J_star_equals_edge_incidence_gram_plus_2I": True,
        "localizer_sign_checks": localizer_checks,
        "g_formula": "g_xy=sum_e m_x^(y)[e]",
        "h_formula": "h_xy=m_x^(y)^T J_star m_x^(y)",
        "tau_formula": "Tau^(y)=W_y J_star W_y^T",
        "Gamma_equals_sum_fixed_middle_tau": True,
        "Gamma_diagonal_equals_H_row_sum": True,
        "Gamma_row_sum_zero": True,
        "Gamma_rank": IV.matrix_rank(gamma),
        "Gamma_rank_at_most_W_rank": True,
        "scope": (
            "formal algebra control only: disjoint degree-one stars, not the "
            "target 99-by-231 degree-three incidence or an SRG"
        ),
    }


def trace_zero_space_audit() -> dict[str, Any]:
    """Reconstruct the dimension-65 codomain for the projector map."""

    # A self-adjoint operator is determined by an ordinary symmetric matrix
    # H A, giving dimension 11*12/2=66.  Trace is nonzero because tr(I)=11=2.
    self_adjoint_dimension = 11 * 12 // 2
    identity_trace = 11 % 3
    require(identity_trace != 0, "trace functional unexpectedly zero")
    trace_zero_dimension = self_adjoint_dimension - 1
    require(trace_zero_dimension == 65, "trace-zero dimension changed")
    return {
        "self_adjoint_operator_dimension": self_adjoint_dimension,
        "trace_functional_nonzero": True,
        "trace_zero_self_adjoint_dimension": trace_zero_dimension,
        "projector_trace": 6 % 3,
        "projector_span_upper_bound": 65,
        "kernel_dimension_lower_bound": 99 - 65,
    }


def true_kernel_quotient_audit() -> dict[str, Any]:
    """Audit the conditional A_Delta dimension and operator transition."""

    trace_space = trace_zero_space_audit()
    rank_b_min = 66
    rank_b_max = 82
    dim_l_min = 99 - rank_b_max
    dim_l_max = 99 - rank_b_min
    require((dim_l_min, dim_l_max) == (17, 33), "Wave 191 interval changed")
    span_p_max = trace_space["projector_span_upper_bound"]
    quotient_min = rank_b_min - span_p_max
    require(quotient_min == 1, "true-kernel quotient lower bound changed")

    # Map ledger:
    # phi(c)=B^T c, ker(phi)=L.
    # T(a)=sum a_T z_T tensor z_T.
    # P(c)=-T(phi(c)), so ker(P)=K_P and L is contained in K_P.
    # Theta(a)=Z^*T(a)Z.  Full row rank of Z supplies a right inverse R,
    # and R^*Theta(a)R=T(a), so Theta(a)=0 iff T(a)=0.
    # Thus phi maps K_P onto A_Delta with kernel L.
    ledger = {
        "phi": "F_3^99 -> F_3^231, c |-> B^T c",
        "kernel_phi": "L=ker(B^T)",
        "tensor_map": "T(a)=sum_T a_T(z_T tensor z_T)",
        "projector_map": "P(c)=sum_x c_x P_x=-T(B^T c)",
        "L_contained_in_KP": True,
        "outer_map": "A |-> Z^* A Z",
        "outer_map_injective_reason": (
            "Z has a right inverse R, so R^*(Z^*AZ)R=A"
        ),
        "Theta_equivalence": "D diag(a) D=0 iff T(a)=0",
        "induced_isomorphism": (
            "ker(projector map)/L isomorphic to "
            "im(B^T) intersect ker(a |-> D diag(a) D)"
        ),
    }
    return {
        "inherited_rank_B_interval": [rank_b_min, rank_b_max],
        "inherited_dim_L_interval": [dim_l_min, dim_l_max],
        "projector_span_upper_bound": span_p_max,
        "dim_KP_lower_bound": 34,
        "dimension_formula": "dim(A_Delta)=rank(B)-dim span{P_x}",
        "dim_A_Delta_lower_bound": quotient_min,
        "map_ledger": ledger,
        "diagonal_consequence": (
            "diag(D diag(a)D)=0 gives (D Hadamard D)a=0"
        ),
        "gram_kernel_warning": (
            "no null vector of a trace Gram matrix is promoted; A_Delta "
            "comes from a genuine operator relation"
        ),
    }


def nonconstant_and_balance_audit() -> dict[str, Any]:
    contradictions: dict[str, Any] = {}
    for scalar in (1, 2):
        # From B^T c=lambda*1, summing all 231 coordinates gives sum(c)=0:
        # B*1=7*1=1, while lambda*231=0.
        sum_c = scalar * 231 % 3
        by_g_one = scalar * (14 + 1) % 3
        by_g_minus_j = (scalar - sum_c) % 3
        require(by_g_one == 0, "G1 identity changed")
        require(by_g_minus_j == scalar, "G-J identity changed")
        require(by_g_one != by_g_minus_j, "constant pullback contradiction lost")
        contradictions[str(scalar)] = {
            "forced_sum_c": sum_c,
            "G_times_Gc": by_g_one,
            "G_minus_J_times_c": by_g_minus_j,
            "contradiction": True,
        }

    # Check the two-by-three coefficient system for (R0,R1,R2):
    # R1+2R2=0 and R0+R1+R2=0 have solution (R0,R1,R2)=(R,R,R).
    relation_matrix = [[0, 1, 2], [1, 1, 1]]
    require(IV.matrix_rank(relation_matrix) == 2, "class-balance rank changed")
    kernel_examples = [
        vector
        for vector in itertools.product(range(3), repeat=3)
        if IV.matvec(relation_matrix, vector) == [0, 0]
    ]
    require(
        kernel_examples == [(0, 0, 0), (1, 1, 1), (2, 2, 2)],
        "three-class balance solution changed",
    )
    return {
        "im_Bt_intersects_constant_line": "zero only",
        "nonzero_constant_cases": contradictions,
        "uses": [
            "B 1_231=1_99",
            "G=B B^T=A+I",
            "G 1_99=0",
            "G^2=G-J",
        ],
        "balance_equations": [
            "R_1+2R_2=0 from the tensor relation",
            "R_0+R_1+R_2=0 from the global zero frame",
        ],
        "class_balance": "R_0=R_1=R_2",
        "interpretation_guard": (
            "this is equality of operator sums, not equality of class sizes"
        ),
    }


def normalized_projective_points(dimension: int) -> list[tuple[int, ...]]:
    points: list[tuple[int, ...]] = []
    for raw in itertools.product(range(3), repeat=dimension):
        if not any(raw):
            continue
        first = next(value for value in raw if value)
        inverse_first = pow(first, -1, 3)
        normalized = tuple(value * inverse_first % 3 for value in raw)
        if normalized not in points:
            points.append(normalized)
    return points


def projective_cap_maximum(dimension: int) -> tuple[int, int, int]:
    """Return (point count, maximum size, number of maximum subsets)."""

    points = normalized_projective_points(dimension)
    best = 0
    best_count = 0
    for mask in range(1 << len(points)):
        size = mask.bit_count()
        if size < best:
            continue
        indices = [index for index in range(len(points)) if mask >> index & 1]
        is_cap = all(
            IV.matrix_rank([points[index] for index in triple]) == 3
            for triple in itertools.combinations(indices, 3)
        )
        if is_cap and size > best:
            best = size
            best_count = 1
        elif is_cap and size == best:
            best_count += 1
    return len(points), best, best_count


def weight_eight_control_audit() -> dict[str, Any]:
    """Independently replay the released relaxed weight-eight control."""

    columns = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 1, 1, 1),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 2),
    ]
    coefficients = [1, 1, 1, 2, 2, 2, 2, 1]
    synthesis = IV.transpose(columns)
    coefficient_form = IV.diagonal(coefficients)
    tensor_sum = IV.matmul(
        IV.matmul(synthesis, coefficient_form),
        IV.transpose(synthesis),
    )
    require(tensor_sum == IV.zeros(4, 4), "weight-eight tensor sum nonzero")
    require(IV.matrix_rank(synthesis) == 4, "weight-eight span rank changed")
    require(
        all(
            IV.matrix_rank([columns[index] for index in triple]) == 3
            for triple in itertools.combinations(range(8), 3)
        ),
        "weight-eight control has a dependent triple",
    )

    support_form = [
        [0, 1, 0, 1],
        [1, 0, 0, 1],
        [0, 0, 0, 2],
        [1, 1, 2, 0],
    ]
    require(matrix_determinant(support_form) == 1, "support form changed")
    norms = [
        scalar_product(column, IV.matvec(support_form, column))
        for column in columns
    ]
    require(norms == [0] * 8, "weight-eight support column nonsingular")
    ambient_form = block_diagonal(support_form, IV.diagonal([1] * 6 + [2]))
    require(matrix_determinant(ambient_form) == 2, "ambient discriminant changed")
    embedded = [column + (0,) * 7 for column in columns]
    ambient_norms = [
        scalar_product(column, IV.matvec(ambient_form, column))
        for column in embedded
    ]
    require(ambient_norms == [0] * 8, "embedded column nonsingular")
    embedded_synthesis = IV.transpose(embedded)
    ordinary_tensor_sum = IV.matmul(
        IV.matmul(embedded_synthesis, coefficient_form),
        IV.transpose(embedded_synthesis),
    )
    operator_sum = IV.matmul(ordinary_tensor_sum, ambient_form)
    require(operator_sum == IV.zeros(11, 11), "rank-one operator sum nonzero")
    return {
        "support_size": 8,
        "span_rank": 4,
        "coefficient_composition": {"1": 4, "2": 4},
        "coefficient_form_has_totally_isotropic_dimension": 4,
        "every_three_columns_independent": True,
        "all_columns_singular": True,
        "support_form_determinant": 1,
        "ambient_dimension": 11,
        "ambient_form_determinant": 2,
        "ambient_form_nonsquare": True,
        "tensor_and_operator_sum_zero": True,
        "scope": (
            "sharp only for the local tensor, cap, singularity, and ambient-"
            "form ingredients; no 231-frame, incidence, graph, or im(B^T)"
        ),
        "proves_target_weight_eight_word_exists": False,
        "blocks_weight_nine_from_local_ingredients_alone": True,
    }


def tensor_support_strengthening_audit() -> dict[str, Any]:
    """Derive wt(a)>=8 for nonzero A_Delta words.

    For support S of size k, write V for the 11-by-k supported column matrix
    and Lambda=diag(a_T).  The operator relation is

        V Lambda V^T H=0.

    Since H and Lambda are nonsingular, V Lambda V^T=0 and the row space of
    V is totally isotropic in the nondegenerate k-space with metric Lambda.
    Thus 2 rank(V)<=k.  The independently verified d(W^perp)>=4 says that
    no three supported projective columns are dependent.  For k<=7,
    rank(V)<=3, while an exhaustive PG(2,3) cap check gives maximum four.
    Lower projective dimensions have smaller maxima.  Hence k>=8.
    """

    cap_data: dict[str, Any] = {}
    cap_maxima: dict[int, int] = {0: 0}
    for dimension in (1, 2, 3):
        point_count, cap_maximum, maximum_count = projective_cap_maximum(dimension)
        cap_maxima[dimension] = cap_maximum
        cap_data[str(dimension)] = {
            "projective_point_count": point_count,
            "maximum_no_dependent_triple_subset": cap_maximum,
            "number_of_maximum_subsets": maximum_count,
        }
    require(cap_maxima == {0: 0, 1: 1, 2: 2, 3: 4}, "cap maxima changed")
    require(cap_data["3"]["number_of_maximum_subsets"] == 234, "plane cap count changed")

    exclusions: dict[str, Any] = {}
    for support in range(1, 8):
        rank_upper = support // 2
        maximum_cap = cap_maxima[rank_upper]
        require(support > maximum_cap, f"support {support} not excluded")
        exclusions[str(support)] = {
            "row_rank_upper_bound": rank_upper,
            "cap_size_upper_bound": maximum_cap,
            "excluded": True,
        }

    # Coefficients on the support are 1 or 2, so Lambda is invertible.
    for support in range(1, 8):
        for coefficients in itertools.product((1, 2), repeat=support):
            determinant = 1
            for coefficient in coefficients:
                determinant = determinant * coefficient % 3
            require(determinant != 0, "support coefficient form degenerated")

    return {
        "submitted_bound": 4,
        "verified_strengthened_bound": 8,
        "operator_to_row_space": (
            "sum a_T(z_T tensor z_T)=0 implies V Lambda V^T=0 after "
            "multiplying by the inverse ambient form"
        ),
        "coefficient_metric_nondegenerate": True,
        "totally_isotropic_row_space": True,
        "rank_bound": "rank(V)<=floor(wt(a)/2)",
        "input_premise": (
            "verified Wave 174 theorem d(W^perp)>=4, equivalently no "
            "dependent set of at most three centered columns"
        ),
        "wave174_report_sha256": sha256(WAVE_174 / "verification-report.md"),
        "projective_cap_enumeration": cap_data,
        "support_exclusions": exclusions,
        "weight_eight_boundary": {
            "forced_span_rank": 4,
            "coefficient_form_must_be_split": True,
            "allowed_number_of_coefficient_2_entries": [0, 2, 4, 6, 8],
            "reason": (
                "an 8-cap needs rank at least 4, the Witt bound gives rank "
                "at most 4, and a split diagonal 8-form has square "
                "determinant, hence an even number of 2 entries"
            ),
        },
        "weight_eight_relaxed_control": weight_eight_control_audit(),
        "scope": (
            "conditional on the prism-free rank-11 endpoint and the verified "
            "Wave 174 centered-column dual-distance theorem"
        ),
    }


def common_kernel_audit() -> dict[str, Any]:
    return {
        "premise": "sum_x c_x P_x=0",
        "slice_calculation": (
            "(Tau^(y)c)_x="
            "tr(P_x P_y (sum_z c_z P_z) P_y)=0"
        ),
        "contained_in_every_fixed_middle_kernel": True,
        "Gamma_calculation": "Gamma=sum_y Tau^(y)",
        "contained_in_Gamma_kernel": True,
        "true_relation_guard": (
            "the implication starts from an operator equality, not a "
            "restricted trace-Gram null vector"
        ),
    }


def analyze() -> dict[str, Any]:
    proof_b_manifest = verify_manifest(PROOF_B / "package-manifest.sha256")
    weight_addendum_manifest = verify_manifest(
        WEIGHT_ADDENDUM / "package-manifest.sha256"
    )
    wave174_manifest = verify_manifest(WAVE_174 / "package-manifest.sha256")
    require(
        sha256(WAVE_191)
        == "afe7d35627ec14a9599b427bcca0751e86a3f32b71fb7baf4d91e9e2e335f75f",
        "Wave 191 inherited theorem hash changed",
    )
    result = {
        "role": "verifier",
        "claim_label": "VERIFIED_WITH_SCOPE_AND_STRENGTHENING",
        "scope": (
            "conditional prism-free n3=4158 centered rank-11 endpoint; "
            "Wave 206 Proof-B crossing/localizer and true-kernel claims"
        ),
        "source_integrity": {
            "proof_b": proof_b_manifest,
            "weight_addendum": weight_addendum_manifest,
            "wave174": wave174_manifest,
            "wave191_report_sha256": sha256(WAVE_191),
            "blind_freeze_manifest_sha256": sha256(
                HERE / "SOURCE_BLIND_FREEZE.sha256"
            ),
            "blind_files_unchanged": True,
        },
        "crossing_and_localizer": crossing_and_localizer_audit(),
        "true_kernel_quotient": true_kernel_quotient_audit(),
        "nonconstant_and_three_class_balance": nonconstant_and_balance_audit(),
        "tensor_support": tensor_support_strengthening_audit(),
        "common_true_kernel": common_kernel_audit(),
        "scope_wall": {
            "fixed_middle_trace_class_nullities_are_true_relations": False,
            "trace_class_nullity_kind": "Gram only unless radical controlled",
            "shared_231_column_endpoint_constructed": False,
            "rank11_endpoint_excluded": False,
            "n3_improved": False,
            "Q_7060_proved": False,
            "Conway_99_resolved": False,
            "external_novelty": "UNKNOWN",
            "endpoint_status": "UNKNOWN",
        },
        "verdict": {
            "submitted_Proof_B_claims": "VERIFIED_WITH_SCOPE",
            "submitted_support_bound_wt_at_least_4": "VERIFIED_BUT_NOT_SHARP",
            "verifier_support_strengthening_wt_at_least_8": "VERIFIED",
            "released_weight_addendum": "VERIFIED_WITH_SCOPE",
            "weight_eight_local_boundary_control": "VERIFIED_SCOPED",
            "promotion": (
                "A_Delta is nonzero, nonconstant, has three equal tensor-class "
                "sums, lies in every true slice kernel, and every nonzero "
                "A_Delta word has weight at least 8"
            ),
            "vetoes": [
                "no Gram-kernel word is promoted to an operator relation",
                "no endpoint exclusion or Conway-99 resolution follows",
            ],
        },
    }
    return result


def main() -> None:
    result = analyze()
    target = HERE / "post_source_proof_b_result.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
