"""Audit an existing binary classifier evaluation JSON without retraining.

Reads the held-out scores/labels produced by train.py. Does not optimize a
threshold on the test set or claim that a demo score generalizes.
"""
import argparse
import json
from pathlib import Path


def confusion(labels, scores, threshold=0.5):
    if not 0 < threshold < 1:
        raise ValueError("Threshold must be strictly between 0 and 1")
    if not labels or len(labels) != len(scores):
        raise ValueError("Labels and scores must be nonempty and equal length")
    tn = fp = fn = tp = 0
    for label, score in zip(labels, scores):
        if type(label) is not int or label not in (0, 1):
            raise ValueError("Labels must be 0 or 1")
        if type(score) not in (int, float) or not 0 <= score <= 1:
            raise ValueError("Scores must be probabilities between 0 and 1")
        predicted = int(score >= threshold)
        if label == 1 and predicted == 1:
            tp += 1
        elif label == 1:
            fn += 1
        elif predicted == 1:
            fp += 1
        else:
            tn += 1
    def ratio(a, b):
        return a / b if b else 0.0
    return {
        "threshold": threshold,
        "samples": len(labels),
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "accuracy": ratio(tp + tn, len(labels)),
        "event_precision": ratio(tp, tp + fp),
        "event_recall": ratio(tp, tp + fn),
        "event_f1": ratio(2 * tp, 2 * tp + fp + fn),
        "false_positive_rate": ratio(fp, fp + tn),
        "false_negative_rate": ratio(fn, fn + tp),
    }


def audit(report):
    if not isinstance(report, dict) or not isinstance(report.get("test"), dict):
        raise ValueError("Expected a training result JSON with a test object")
    test = report["test"]
    result = confusion(test["labels"], test["scores"])
    if test.get("confusion_matrix") != result["confusion_matrix"]:
        raise ValueError("Stored confusion matrix differs from the raw test scores")
    return {
        "task": report.get("task"),
        "source": report.get("source"),
        "split_counts": report.get("split_counts"),
        "held_out_test": result,
        "interpretation": (
            "These are dataset-specific held-out results. No threshold was selected "
            "on the test set. For safety applications, report missed events and "
            "false alarms; this is not a deployment certification."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.results.read_text(encoding="utf-8")))
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        if args.output.resolve() == args.results.resolve():
            parser.error("Output cannot overwrite input results")
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
