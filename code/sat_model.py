#!/usr/bin/env python3
"""Direct exact SAT encoding of the rooted residual graph.

This is discovery code. A SAT model is decoded into a complete edge-list
certificate and must be checked by the independent validators. An UNSAT return
does not become evidence unless the exact CNF and a proof artifact are checked.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Sequence

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from matching_orbits import canonical_branch_decisions, parse_partition
from root_model import RootModel


@dataclass
class EncodedRootModel:
    root: RootModel
    cnf: CNF
    pool: IDPool
    edge_variables: dict[tuple[int, int], int]
    wedge_variables: dict[tuple[int, int, int], int]
    variant: str

    @classmethod
    def build(cls, pair_count: int, variant: str = "compact") -> "EncodedRootModel":
        if variant not in ("compact", "direct"):
            raise ValueError("variant must be 'compact' or 'direct'")
        root = RootModel.build(pair_count)
        root.validate_fixed_identities()
        cnf = CNF()
        pool = IDPool()

        edge_variables: dict[tuple[int, int], int] = {}
        for first, second in combinations(range(root.residual_count), 2):
            edge_variables[(first, second)] = pool.id(("edge", first, second))

        wedge_variables: dict[tuple[int, int, int], int] = {}
        for first, second in combinations(range(root.residual_count), 2):
            for center in range(root.residual_count):
                if center in (first, second):
                    continue
                wedge_variables[(first, second, center)] = pool.id(
                    ("wedge", first, second, center)
                )

        encoded = cls(root, cnf, pool, edge_variables, wedge_variables, variant)
        if variant == "compact":
            encoded._add_wedge_implications()
        else:
            encoded._add_wedge_definitions()
        encoded._add_coordinate_incidence_equalities()
        if variant == "compact":
            encoded._add_common_neighbor_upper_bounds()
        else:
            encoded._add_common_neighbor_equalities()
        return encoded

    def edge_literal(self, first: int, second: int) -> int:
        if first == second:
            raise ValueError("the residual graph has no loop variables")
        if first > second:
            first, second = second, first
        return self.edge_variables[(first, second)]

    def _add_wedge_definitions(self) -> None:
        # y_(p,q;r) <-> (x_(p,r) and x_(q,r)).
        for (first, second, center), wedge in self.wedge_variables.items():
            left = self.edge_literal(first, center)
            right = self.edge_literal(second, center)
            self.cnf.append([-wedge, left])
            self.cnf.append([-wedge, right])
            self.cnf.append([wedge, -left, -right])

    def _add_wedge_implications(self) -> None:
        # The compact encoding needs only (x_(p,r) and x_(q,r)) -> y_(p,q;r).
        # Global wedge counting proves that all upper bounds below become exact.
        for (first, second, center), wedge in self.wedge_variables.items():
            left = self.edge_literal(first, center)
            right = self.edge_literal(second, center)
            self.cnf.append([-left, -right, wedge])

    def _add_exactly(self, literals: list[int], bound: int) -> None:
        encoding = CardEnc.equals(
            lits=literals,
            bound=bound,
            vpool=self.pool,
            encoding=EncType.seqcounter,
        )
        self.cnf.extend(encoding.clauses)

    def _add_at_most(self, literals: list[int], bound: int) -> None:
        encoding = CardEnc.atmost(
            lits=literals,
            bound=bound,
            vpool=self.pool,
            encoding=EncType.seqcounter,
        )
        self.cnf.extend(encoding.clauses)

    def _add_coordinate_incidence_equalities(self) -> None:
        # This is the scalar form of M B + B X = 2J-B in CONJECTURE.md.
        for label_index in range(self.root.residual_count):
            for coordinate in range(self.root.coordinate_count):
                literals = [
                    self.edge_literal(label_index, other)
                    for other in self.root.containing(coordinate)
                    if other != label_index
                ]
                target = self.root.coordinate_neighbor_target(coordinate, label_index)
                self._add_exactly(literals, target)

    def _add_common_neighbor_equalities(self) -> None:
        # sum_r y_(p,q;r) + x_(p,q) = 2-|label(p) intersection label(q)|.
        for first, second in combinations(range(self.root.residual_count), 2):
            intersection = len(
                set(self.root.labels[first]).intersection(self.root.labels[second])
            )
            literals = [
                self.wedge_variables[(first, second, center)]
                for center in range(self.root.residual_count)
                if center not in (first, second)
            ]
            literals.append(self.edge_literal(first, second))
            self._add_exactly(literals, 2 - intersection)

    def _add_common_neighbor_upper_bounds(self) -> None:
        # Profile equalities force degree 2m-2. For m=7 the total number of
        # actual wedges equals the sum of these upper bounds, making the
        # one-way wedge encoding exact. The same identity holds for every m.
        for first, second in combinations(range(self.root.residual_count), 2):
            intersection = len(
                set(self.root.labels[first]).intersection(self.root.labels[second])
            )
            literals = [
                self.wedge_variables[(first, second, center)]
                for center in range(self.root.residual_count)
                if center not in (first, second)
            ]
            literals.append(self.edge_literal(first, second))
            self._add_at_most(literals, 2 - intersection)

    def statistics(self) -> dict[str, Any]:
        return {
            "variant": self.variant,
            "pair_count": self.root.pair_count,
            "full_vertex_count": 2 * self.root.pair_count**2 + 1,
            "residual_vertex_count": self.root.residual_count,
            "named_edge_variables": len(self.edge_variables),
            "named_wedge_variables": len(self.wedge_variables),
            "total_variables": self.cnf.nv,
            "clauses": len(self.cnf.clauses),
        }

    def residual_edges_from_model(self, model: Sequence[int]) -> list[tuple[int, int]]:
        positive = {literal for literal in model if literal > 0}
        return [
            edge for edge, variable in self.edge_variables.items() if variable in positive
        ]

    def add_matching_branch(self, coordinate: int, partition: Sequence[int]) -> None:
        decisions = canonical_branch_decisions(self.root, coordinate, partition)
        for edge, present in decisions.items():
            literal = self.edge_variables[edge]
            self.cnf.append([literal if present else -literal])

    def full_certificate(self, model: Sequence[int]) -> dict[str, Any]:
        """Decode a SAT assignment into the complete normalized graph."""

        coordinate_offset = 1
        residual_offset = 1 + self.root.coordinate_count
        full_edges: list[tuple[int, int]] = []

        for coordinate in range(self.root.coordinate_count):
            full_edges.append((0, coordinate_offset + coordinate))

        for pair in range(self.root.pair_count):
            full_edges.append(
                (coordinate_offset + 2 * pair, coordinate_offset + 2 * pair + 1)
            )

        for label_index, label in enumerate(self.root.labels):
            residual_vertex = residual_offset + label_index
            for coordinate in label:
                full_edges.append((coordinate_offset + coordinate, residual_vertex))

        for first, second in self.residual_edges_from_model(model):
            full_edges.append((residual_offset + first, residual_offset + second))

        full_edges = [tuple(sorted(edge)) for edge in full_edges]
        full_edges.sort()
        return {
            "format": "srg-edge-list-v1",
            "vertices": 2 * self.root.pair_count**2 + 1,
            "edges": [list(edge) for edge in full_edges],
        }


def solve_model(
    encoded: EncodedRootModel,
    solver_name: str,
    conflict_budget: int | None = None,
) -> tuple[bool | None, list[int] | None, dict[str, Any]]:
    with Solver(
        name=solver_name,
        bootstrap_with=encoded.cnf.clauses,
        use_timer=True,
    ) as solver:
        if conflict_budget is None:
            satisfiable = solver.solve()
        else:
            solver.conf_budget(conflict_budget)
            satisfiable = solver.solve_limited()
        model = solver.get_model() if satisfiable is True else None
        statistics = {
            "solver": solver_name,
            "conflict_budget": conflict_budget,
            "solver_time_seconds": solver.time_accum(),
            "accumulated_stats": solver.accum_stats(),
        }
    return satisfiable, model, statistics


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair-count", type=int, default=2)
    parser.add_argument("--variant", choices=("compact", "direct"), default="compact")
    parser.add_argument(
        "--branch",
        help="canonical fiber-matching partition, e.g. 6 or 3+2+1",
    )
    parser.add_argument("--branch-coordinate", type=int, default=0)
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument(
        "--conflict-budget",
        type=int,
        help="return UNKNOWN after this many conflicts instead of running unbounded",
    )
    parser.add_argument("--cnf", type=Path, help="optional DIMACS output")
    parser.add_argument("--candidate", type=Path, help="decoded SAT certificate output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.candidate and not args.solve:
        raise SystemExit("--candidate requires --solve")
    if args.conflict_budget is not None and args.conflict_budget < 1:
        raise SystemExit("--conflict-budget must be positive")

    encoded = EncodedRootModel.build(args.pair_count, args.variant)
    if args.branch:
        partition = parse_partition(args.branch, args.pair_count - 1)
        encoded.add_matching_branch(args.branch_coordinate, partition)
    report: dict[str, Any] = {"encoding": encoded.statistics()}
    if args.branch:
        report["branch"] = {
            "coordinate": args.branch_coordinate,
            "partition": list(partition),
        }

    if args.cnf:
        args.cnf.parent.mkdir(parents=True, exist_ok=True)
        encoded.cnf.to_file(str(args.cnf))
        report["cnf"] = str(args.cnf)

    if args.solve:
        satisfiable, model, solver_statistics = solve_model(
            encoded,
            args.solver,
            args.conflict_budget,
        )
        report["result"] = (
            "SAT_MODEL"
            if satisfiable is True
            else "UNSAT_UNVERIFIED"
            if satisfiable is False
            else "UNKNOWN"
        )
        report["solver"] = solver_statistics

        if satisfiable is True and model is not None and args.candidate:
            candidate = encoded.full_certificate(model)
            args.candidate.parent.mkdir(parents=True, exist_ok=True)
            args.candidate.write_text(
                json.dumps(candidate, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            report["candidate"] = str(args.candidate)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
