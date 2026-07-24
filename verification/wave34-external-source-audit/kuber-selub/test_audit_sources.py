from __future__ import annotations

import json
import unittest
from pathlib import Path

from audit_sources import scan_lean_source


HERE = Path(__file__).resolve().parent


class LeanScannerTests(unittest.TestCase):
    def test_endpoint_usage_and_trust_tokens(self) -> None:
        sample = """
structure C3QuotientCertificate where
  B : Nat
  triangularOrbits : Nat
  quotientIdentity : True
  regularity : True
  diagonal : True
  spectrum : True
  triangle_congruence : True

theorem C3QuotientCertificate.card_eq_six_or_twentySeven
    (C : C3QuotientCertificate) : True :=
  by
    have := C.diagonal
    have := C.spectrum
    have := C.triangle_congruence
    trivial

#print axioms C3QuotientCertificate.card_eq_six_or_twentySeven
"""
        result = scan_lean_source(sample)
        self.assertFalse(result["packaged_endpoint_mentions_quotient_identity"])
        self.assertFalse(result["packaged_endpoint_mentions_regularity"])
        self.assertTrue(result["packaged_endpoint_mentions_diagonal"])
        self.assertTrue(result["packaged_endpoint_mentions_spectrum"])
        self.assertTrue(result["packaged_endpoint_mentions_triangle_congruence"])
        self.assertTrue(all(value == 0 for value in result["trust_sensitive_counts"].values()))


class FinalArtifactTests(unittest.TestCase):
    def test_unknown_boundary_and_source_retention(self) -> None:
        results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
        sources = json.loads((HERE / "source-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(results["conway_99_target_status"], "UNKNOWN")
        self.assertEqual(results["novelty_status"], "UNKNOWN")
        self.assertFalse(results["kuber"]["graph_to_matrix_bridge_formalized"])
        self.assertEqual(
            results["kuber"]["build_status"], "VERIFIED_CLEAN_EXTERNAL_CLONE"
        )
        self.assertEqual(results["kuber"]["cache_get_status"], "PASS")
        self.assertEqual(
            results["kuber"]["principal_axioms"],
            ["propext", "Classical.choice", "Quot.sound"],
        )
        self.assertFalse(results["selub"]["solver_result_claimed"])
        self.assertFalse(
            sources["retention"]["third_party_source_bytes_present_in_final_package"]
        )

    def test_every_certificate_field_is_classified(self) -> None:
        interface = json.loads((HERE / "lean-interface-map.json").read_text(encoding="utf-8"))
        fields = interface["certificate_fields"]
        self.assertEqual(len(fields), 7)
        self.assertEqual(
            {field["field"] for field in fields},
            {
                "B",
                "triangularOrbits",
                "quotientIdentity",
                "regularity",
                "diagonal",
                "spectrum",
                "triangle_congruence",
            },
        )
        self.assertTrue(
            all(not field["mechanically_derived_from_graph_in_repository"] for field in fields)
        )

    def test_selub_result_boundary(self) -> None:
        selub = json.loads((HERE / "selub-scope.json").read_text(encoding="utf-8"))
        solver = selub["solver_result_audit"]
        self.assertFalse(solver["completed_run_claimed"])
        self.assertFalse(solver["sat_or_unsat_result_claimed"])
        self.assertFalse(solver["proof_or_model_certificate_reported"])


if __name__ == "__main__":
    unittest.main()
