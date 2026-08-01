import json
import unittest

import exact_check


class ExactCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = exact_check.build_results()

    def test_sealed_results_match(self):
        expected = json.loads(exact_check.RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(self.payload, expected)

    def test_completion_census(self):
        census = self.payload["conditional_completion_census_common_to_all_three_orbits"]
        self.assertEqual(census["forced_outside_edge_split"], {"q0": 456, "q1": 64})
        self.assertEqual(census["forced_all_outside_triangles"], 152)
        self.assertEqual(census["forced_four_cycles_total"], 2079)

    def test_controls_are_exactly_restricted(self):
        rows = self.payload["hostile_incidence_controls"]
        self.assertEqual([row["orbit_index"] for row in rows], [0, 4, 29])
        self.assertTrue(all(row["colored_q1_edges"] == 64 for row in rows))
        self.assertTrue(all(row["outside_triangle_blocks"] == 152 for row in rows))
        self.assertTrue(all(row["degree_equations_satisfied"] == 85 for row in rows))
        self.assertTrue(all(row["selected_pair_values_satisfied"] == 10 for row in rows))
        self.assertTrue(all(row["target_zero_violations"] == 0 for row in rows))
        self.assertTrue(all(not row["is_full_quadratic_solution"] for row in rows))


if __name__ == "__main__":
    unittest.main()
