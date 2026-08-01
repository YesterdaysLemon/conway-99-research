import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wave211_exact_check", HERE / "exact_check.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExactCheckTests(unittest.TestCase):
    def test_committed_results_replay_exactly(self) -> None:
        observed = MODULE.json.loads(MODULE.json.dumps(MODULE.analyze()))
        expected = MODULE.json.loads(MODULE.RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(observed, expected)

    def test_forced_action_factorization(self) -> None:
        self.assertEqual(len(MODULE.forced_action_polynomial()), 15)

    def test_manifest(self) -> None:
        MODULE.verify_manifest()


if __name__ == "__main__":
    unittest.main()
