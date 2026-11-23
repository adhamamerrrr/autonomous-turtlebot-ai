"""Run a trained temporal model on an authorized local video.

This command does not ship or train a real violence model. It refuses to run
without a compatible checkpoint. Predictions are research outputs, not proof
of violence or a substitute for human review.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from autonomous_turtlebot_ai.vision import Predictor


def sample_video(path, frames=8):
    """Sample evenly spaced RGB frames, matching the training video loader."""
    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            raise ValueError("Cannot open video")
        count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if count < frames:
            raise ValueError(f"Video must contain at least {frames} frames")
        rgb = []
        for index in np.linspace(0, count - 1, frames).astype(int):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(index))
            ok, frame = cap.read()
            if not ok or frame is None:
                raise ValueError(f"Could not decode video frame {index}")
            rgb.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return rgb
    finally:
        cap.release()


def predict_video(path, checkpoint, threshold=0.5):
    if not 0 < threshold < 1:
        raise ValueError("Threshold must be between 0 and 1")
    predictor = Predictor(checkpoint, "violence")
    score = predictor.score(sample_video(path))
    return {
        "video": str(Path(path)),
        "model": str(Path(checkpoint)),
        "event_score": score,
        "threshold": threshold,
        "flagged_for_review": score >= threshold,
        "disclaimer": (
            "Experimental classifier output only; not evidence of violence. "
            "The supplied checkpoint must be independently evaluated on real, "
            "appropriately licensed data before use."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--model", type=Path, required=True,
                        help="A separately trained compatible violence.pt checkpoint")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Set using validation data, never the held-out test set")
    args = parser.parse_args()
    try:
        result = predict_video(args.video, args.model, args.threshold)
    except (ValueError, OSError, RuntimeError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
