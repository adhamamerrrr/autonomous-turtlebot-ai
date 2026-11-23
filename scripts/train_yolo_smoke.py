"""Optional YOLO smoke-localization experiment (not a trained model).

Requires: pip install ultralytics
Requires an authorized, locally available YOLO dataset YAML with smoke boxes.
Do not use the image-level classification manifest as detection labels.
"""
import argparse
import json
from pathlib import Path


def check_dataset(config):
    import yaml
    with Path(config).open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if not isinstance(data, dict):
        raise ValueError("Expected YOLO dataset mapping")
    for key in ("train", "val", "names"):
        if key not in data:
            raise ValueError(f"Missing dataset field: {key}")
    names = data["names"]
    values = list(names.values()) if isinstance(names, dict) else names
    if not isinstance(values, list) or not any(
        isinstance(name, str) and name.strip().lower() == "smoke"
        for name in values
    ):
        raise ValueError("Dataset must define a 'smoke' detection class")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True,
                        help="Authorized YOLO bounding-box dataset YAML")
    parser.add_argument("--weights", default="yolo11n.pt",
                        help="Pretrained Ultralytics weights (download may be required)")
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--project", default="runs/smoke_detection")
    args = parser.parse_args()
    if args.epochs < 1 or args.imgsz < 32 or args.batch < 1:
        parser.error("epochs and batch must be positive; imgsz must be at least 32")
    try:
        check_dataset(args.data)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    try:
        from ultralytics import YOLO
    except ImportError:
        parser.error("Install the optional dependency: pip install ultralytics")
    model = YOLO(args.weights)
    model.train(data=str(args.data.resolve()), epochs=args.epochs,
                imgsz=args.imgsz, batch=args.batch, device=args.device,
                project=args.project, name="experiment", seed=42)
    print(json.dumps({
        "training": "completed",
        "project": args.project,
        "note": "Training success alone is not evaluation. Inspect validation mAP, "
                "smoke precision/recall and independent test data before claims."
    }, indent=2))


if __name__ == "__main__":
    main()
