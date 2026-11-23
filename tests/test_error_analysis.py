"""Tests for evaluation-to-manifest error attribution."""
import csv
import json
import unittest
from pathlib import Path

from scripts.analyze_errors import error_rows


class ErrorAnalysisTests(unittest.TestCase):
    def test_missed_events_and_false_alarms(self):
        rows = [
            {"path": "train.jpg", "label": "1", "split": "train", "group": "t"},
            {"path": "a.jpg", "label": "0", "split": "test", "group": "a"},
            {"path": "b.jpg", "label": "1", "split": "test", "group": "b"},
        ]
        result = error_rows(rows, [0, 1], [0.9, 0.1])
        self.assertEqual({r["error_type"] for r in result},
                         {"false_alarm", "missed_event"})
        self.assertEqual(len(result), 2)

    def test_mismatched_manifest_rejected(self):
        rows = [{"path": "a.jpg", "label": "1", "split": "test", "group": "a"}]
        with self.assertRaises(ValueError):
            error_rows(rows, [0], [0.3])
        with self.assertRaises(ValueError):
            error_rows(rows, [1, 0], [0.3, 0.7])

    def test_saved_smoke_errors(self):
        root = Path(__file__).resolve().parents[1]
        with (root / "results/smoke_manifest.csv").open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        report = json.loads((root / "results/smoke_results.json").read_text(encoding="utf-8"))
        test = report["test"]
        errors = error_rows(rows, test["labels"], test["scores"])
        self.assertEqual(sum(e["error_type"] == "false_alarm" for e in errors), 9)
        self.assertEqual(sum(e["error_type"] == "missed_event" for e in errors), 25)


if __name__ == "__main__":
    unittest.main()
