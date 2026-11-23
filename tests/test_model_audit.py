"""Regression tests for held-out binary model evaluation."""
import json
import unittest
from pathlib import Path

from scripts.audit_model import audit, confusion


class EvaluationAuditTests(unittest.TestCase):
    def test_counts_and_metrics(self):
        result = confusion([0, 0, 1, 1], [0.1, 0.8, 0.2, 0.9])
        self.assertEqual(result["confusion_matrix"], [[1, 1], [1, 1]])
        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["event_recall"], 0.5)
        self.assertEqual(result["false_negative_rate"], 0.5)

    def test_rejects_bad_data(self):
        for labels, scores in [([], []), ([1], []), ([2], [0.5]),
                               ([1], [1.1]), ([1], [float("nan")])]:
            with self.subTest(labels=labels, scores=scores):
                with self.assertRaises(ValueError):
                    confusion(labels, scores)
        with self.assertRaises(ValueError):
            confusion([1], [0.5], threshold=1.0)

    def test_saved_smoke_baseline_is_consistent(self):
        report_path = Path(__file__).resolve().parents[1] / "results" / "smoke_results.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        result = audit(report)["held_out_test"]
        self.assertEqual(result["confusion_matrix"], [[41, 9], [25, 25]])
        self.assertAlmostEqual(result["accuracy"], 0.66)
        self.assertAlmostEqual(result["event_recall"], 0.5)

    def test_rejects_mismatched_stored_matrix(self):
        with self.assertRaises(ValueError):
            audit({"test": {"labels": [1], "scores": [0.9],
                            "confusion_matrix": [[1, 0], [0, 0]]}})


if __name__ == "__main__":
    unittest.main()
