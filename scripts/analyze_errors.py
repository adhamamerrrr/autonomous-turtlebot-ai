"""Identify missed events and false alarms from an existing held-out evaluation.

Uses the test split's manifest order, matching train.py's unshuffled test
DataLoader. Does not require original media files or expose their contents.
"""
import argparse
import csv
import json
from pathlib import Path

from scripts.audit_model import confusion


def error_rows(manifest_rows, labels, scores, threshold=0.5):
    tests = [row for row in manifest_rows if row.get("split") == "test"]
    if len(tests) != len(labels) or len(labels) != len(scores):
        raise ValueError("Test manifest and evaluation lengths differ")
    confusion(labels, scores, threshold)  # validate probabilities and labels
    errors = []
    for row, label, score in zip(tests, labels, scores):
        if int(row["label"]) != label:
            raise ValueError("Manifest order or labels do not match test results")
        predicted = int(score >= threshold)
        if predicted != label:
            errors.append({
                "path": row["path"],
                "group": row["group"],
                "actual": label,
                "predicted": predicted,
                "score": score,
                "error_type": "missed_event" if label == 1 else "false_alarm",
            })
    return sorted(errors, key=lambda item: (item["error_type"], abs(item["score"] - threshold)), reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Optional JSON report destination")
    args = parser.parse_args()
    with args.manifest.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    report = json.loads(args.results.read_text(encoding="utf-8"))
    test = report["test"]
    errors = error_rows(rows, test["labels"], test["scores"])
    payload = {
        "task": report.get("task"),
        "false_alarms": sum(e["error_type"] == "false_alarm" for e in errors),
        "missed_events": sum(e["error_type"] == "missed_event" for e in errors),
        "errors": errors,
        "note": "Error inspection only; test labels must not guide model selection or threshold tuning.",
    }
    output = json.dumps(payload, indent=2) + "\n"
    if args.output:
        if args.output.resolve() in (args.manifest.resolve(), args.results.resolve()):
            parser.error("Output must not overwrite input data")
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
