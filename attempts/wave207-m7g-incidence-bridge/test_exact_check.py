#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exact_check  # noqa: E402


class ExactCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.certificate = json.loads(exact_check.CERTIFICATE.read_text(encoding="utf-8"))

    def run_mutation(self, mutate) -> None:
        data = copy.deepcopy(self.certificate)
        mutate(data)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mutated.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                exact_check.build_result(path)

    def test_archived_result_replays(self) -> None:
        expected = json.loads(exact_check.RESULT.read_text(encoding="utf-8"))
        self.assertEqual(exact_check.build_result(), expected)

    def test_mutated_b_is_rejected(self) -> None:
        self.run_mutation(lambda data: data["b"].__setitem__(0, 1))

    def test_deleted_edge_is_rejected(self) -> None:
        self.run_mutation(lambda data: data["extra_edges"].pop())

    def test_wrong_form_is_rejected(self) -> None:
        self.run_mutation(lambda data: data.__setitem__("form_diagonal", [0, 0, 2]))

    def test_fake_intersection_is_rejected(self) -> None:
        self.run_mutation(lambda data: data["selected_triangle_intersections"].append([1, 2]))


if __name__ == "__main__":
    unittest.main()

