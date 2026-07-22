#!/usr/bin/env python3
"""Calibration tests for the rooted SAT encodings."""

from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

from sat_model import EncodedRootModel, main, solve_model


class DirectSatEncodingTests(unittest.TestCase):
    def test_pair_count_two_is_sat_and_decodes_srg_9_4_1_2(self) -> None:
        for variant in ("compact", "direct"):
            with self.subTest(variant=variant):
                encoded = EncodedRootModel.build(2, variant)
                satisfiable, model, _ = solve_model(encoded, "cadical300")
                self.assertTrue(satisfiable)
                self.assertIsNotNone(model)
                certificate = encoded.full_certificate(model or [])
                self.assertEqual(certificate["vertices"], 9)
                self.assertEqual(len(certificate["edges"]), 18)

                adjacency = [set() for _ in range(9)]
                for first, second in certificate["edges"]:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
                self.assertEqual([len(neighbors) for neighbors in adjacency], [4] * 9)
                for first in range(9):
                    for second in range(first + 1, 9):
                        common = len(adjacency[first].intersection(adjacency[second]))
                        self.assertEqual(common, 1 if second in adjacency[first] else 2)

    def test_native_pair_count_two_is_sat_and_decodes_srg_9_4_1_2(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "native")
        satisfiable, model, _ = solve_model(encoded, "minicard")
        self.assertTrue(satisfiable)
        self.assertIsNotNone(model)
        certificate = encoded.full_certificate(model or [])
        self.assertEqual(certificate["vertices"], 9)
        self.assertEqual(len(certificate["edges"]), 18)

    def test_pair_count_three_is_unsat_negative_control(self) -> None:
        for variant in ("compact", "direct"):
            with self.subTest(variant=variant):
                encoded = EncodedRootModel.build(3, variant)
                satisfiable, model, _ = solve_model(encoded, "cadical300")
                self.assertIs(satisfiable, False)
                self.assertIsNone(model)

    def test_small_encoding_statistics_are_deterministic(self) -> None:
        statistics = EncodedRootModel.build(2, "compact").statistics()
        self.assertEqual(statistics["named_edge_variables"], 6)
        self.assertEqual(statistics["named_wedge_variables"], 12)
        self.assertGreater(statistics["total_variables"], 18)
        self.assertGreater(statistics["clauses"], 24)

    def test_compact_encoding_is_smaller_than_direct_encoding(self) -> None:
        compact = EncodedRootModel.build(3, "compact").statistics()
        direct = EncodedRootModel.build(3, "direct").statistics()
        self.assertLess(compact["total_variables"], direct["total_variables"])
        self.assertLess(compact["clauses"], direct["clauses"])

    def test_native_target_statistics_are_deterministic(self) -> None:
        statistics = EncodedRootModel.build(7, "compact", "native").statistics()
        self.assertEqual(statistics["cardinality_backend"], "native")
        self.assertEqual(statistics["total_variables"], 289_338)
        self.assertEqual(statistics["clauses"], 285_852)
        self.assertEqual(statistics["native_atmost_constraints"], 5_838)

    def test_native_constraints_reject_non_cardinality_solver(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "native")
        with self.assertRaisesRegex(ValueError, "minicard"):
            solve_model(encoded, "cadical300")

    def test_native_opb_export_preserves_every_small_constraint(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "native")
        lines = encoded.opb_text().splitlines()
        self.assertEqual(lines[0], "* #variable= 18 #constraint= 50")
        rendered = lines[1:]
        self.assertEqual(
            len(rendered),
            len(encoded.cnf.clauses) + len(encoded.cnf.atmosts),
        )

        def parse_lower_bound(line: str) -> tuple[list[int], int]:
            left, right = line.removesuffix(" ;").split(" >= ")
            tokens = left.split()
            self.assertEqual(tokens[::2], ["+1"] * (len(tokens) // 2))
            literals = [
                -int(token[2:]) if token.startswith("~x") else int(token[1:])
                for token in tokens[1::2]
            ]
            return literals, int(right)

        sources: list[tuple[str, list[int], int]] = [
            ("clause", list(clause), 1) for clause in encoded.cnf.clauses
        ]
        sources.extend(
            ("atmost", list(literals), int(bound))
            for literals, bound in encoded.cnf.atmosts
        )

        for line, (kind, source_literals, source_bound) in zip(rendered, sources):
            output_literals, output_bound = parse_lower_bound(line)
            variables = sorted(
                {abs(literal) for literal in source_literals + output_literals}
            )
            for values in product((False, True), repeat=len(variables)):
                assignment = dict(zip(variables, values))

                def truth(literal: int) -> bool:
                    value = assignment[abs(literal)]
                    return value if literal > 0 else not value

                source_sum = sum(truth(literal) for literal in source_literals)
                source_holds = (
                    source_sum >= source_bound
                    if kind == "clause"
                    else source_sum <= source_bound
                )
                output_holds = (
                    sum(truth(literal) for literal in output_literals) >= output_bound
                )
                self.assertEqual(source_holds, output_holds)

    def test_cnf_formula_rejects_opb_export(self) -> None:
        encoded = EncodedRootModel.build(2, "compact", "cnf")
        with self.assertRaisesRegex(ValueError, "native-cardinality"):
            encoded.opb_text()

    def test_cli_reports_mutually_exclusive_outputs_first(self) -> None:
        with self.assertRaisesRegex(SystemExit, "mutually exclusive"):
            main(["--cardinality", "native", "--cnf", "x.cnf", "--opb", "x.opb"])

    def test_cli_opb_output_uses_reproducible_lf_endings(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "pair2.opb"
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    main(
                        [
                            "--pair-count",
                            "2",
                            "--cardinality",
                            "native",
                            "--opb",
                            str(output),
                        ]
                    ),
                    0,
                )
            payload = output.read_bytes()
            self.assertNotIn(b"\r\n", payload)
            self.assertTrue(payload.endswith(b"\n"))

    def test_n3_normalization_is_the_single_expected_unit(self) -> None:
        encoded = EncodedRootModel.build(7, "compact", "native")
        before = encoded.statistics()
        literal = encoded.add_n3_normalization()
        after = encoded.statistics()
        indices = encoded.root.label_index()

        self.assertEqual(indices[(0, 2)], 0)
        self.assertEqual(indices[(2, 4)], 24)
        self.assertEqual(literal, encoded.edge_literal(0, 24))
        self.assertEqual(literal, 24)
        self.assertEqual(encoded.cnf.clauses[-1], [24])
        self.assertEqual(after["total_variables"], before["total_variables"])
        self.assertEqual(after["clauses"], before["clauses"] + 1)
        self.assertEqual(
            after["native_atmost_constraints"],
            before["native_atmost_constraints"],
        )
        self.assertEqual(
            encoded.opb_text().splitlines()[0],
            "* #variable= 289338 #constraint= 291691",
        )

    def test_n3_normalization_rejects_non_target_scaffolds(self) -> None:
        for pair_count in (2, 3):
            with self.subTest(pair_count=pair_count):
                encoded = EncodedRootModel.build(pair_count, "compact", "native")
                with self.assertRaisesRegex(ValueError, "only to pair_count 7"):
                    encoded.add_n3_normalization()

    def test_cli_rejects_unsafe_n3_legacy_branch_combination(self) -> None:
        with self.assertRaisesRegex(SystemExit, "joint symmetry"):
            main(["--pair-count", "7", "--n3", "--branch", "6"])

    def test_cli_rejects_n3_on_every_non_target_scaffold(self) -> None:
        for pair_count in (2, 3):
            with self.subTest(pair_count=pair_count):
                with self.assertRaisesRegex(SystemExit, "target --pair-count 7"):
                    main(["--pair-count", str(pair_count), "--n3"])

    def test_direct_api_rejects_n3_legacy_branch_in_either_order(self) -> None:
        n3_first = EncodedRootModel.build(7, "compact", "native")
        n3_first.add_n3_normalization()
        with self.assertRaisesRegex(ValueError, "joint symmetry cover"):
            n3_first.add_matching_branch(0, (6,))

        branch_first = EncodedRootModel.build(7, "compact", "native")
        branch_first.add_matching_branch(0, (6,))
        with self.assertRaisesRegex(ValueError, "joint symmetry cover"):
            branch_first.add_n3_normalization()

    def test_only_small_matching_branch_is_still_sat(self) -> None:
        encoded = EncodedRootModel.build(2, "compact")
        encoded.add_matching_branch(0, (1,))
        satisfiable, _, _ = solve_model(encoded, "cadical300")
        self.assertTrue(satisfiable)


if __name__ == "__main__":
    unittest.main()
