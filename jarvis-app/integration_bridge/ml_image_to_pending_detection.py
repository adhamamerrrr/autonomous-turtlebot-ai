import argparse
import base64
import os

import cv2
import firebase_admin
from firebase_admin import credentials, firestore
from ultralytics import YOLO


def image_to_base64_jpeg(path: str, max_width: int = 800, quality: int = 70) -> str:
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not read image: {path}")

    height, width = image.shape[:2]
    if width > max_width:
        scale = max_width / width
        image = cv2.resize(image, (max_width, int(height * scale)))

    ok, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        raise ValueError("Could not encode image as JPEG")

    return base64.b64encode(buffer).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Send YOLO smoke detections as pending guard-review records.")
    parser.add_argument("--image", required=True, help="Path to image frame")
    parser.add_argument("--model", default="best.pt", help="Path to YOLO model")
    parser.add_argument("--service-account", default="serviceAccountKey.json", help="Firebase Admin SDK JSON")
    parser.add_argument("--conf", type=float, default=0.15, help="YOLO confidence threshold")
    parser.add_argument("--location", default="Robot Camera", help="Robot/detection location")
    parser.add_argument("--robot-id", default="TB4-01", help="Robot ID")
    parser.add_argument("--target-classes", default="cigarette,vape", help="Comma-separated class names that should trigger a pending smoke detection")
    args = parser.parse_args()

    for path in [args.image, args.model, args.service_account]:
        if not os.path.exists(path):
            raise FileNotFoundError(path)

    if not firebase_admin._apps:
        cred = credentials.Certificate(args.service_account)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    model = YOLO(args.model)
    target_classes = {c.strip().lower() for c in args.target_classes.split(',') if c.strip()}
    print(f"Model classes: {model.names}")
    print(f"Target classes: {sorted(target_classes)}")

    results = model.predict(
        source=args.image,
        conf=args.conf,
        imgsz=640,
        save=True,
        device="cpu",
    )

    sent = 0
    photo_base64 = image_to_base64_jpeg(args.image)

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[cls_id]
            print(f"Detected: {class_name} confidence={confidence:.3f}")

            if class_name.lower() in target_classes:
                db.collection("smoke_detections").add({
                    "detectionType": "Smoking",
                    "confidence": confidence,
                    "location": args.location,
                    "robotId": args.robot_id,
                    "status": "Pending Review",
                    "source": "YOLO ML Model",
                    "photoBase64": photo_base64,
                    "timestamp": firestore.SERVER_TIMESTAMP,
                })
                sent += 1
                print("Pending smoke detection sent to Firebase for guard review.")

    if sent == 0:
        print("No cigarette/vape detection sent.")
    else:
        print(f"Total pending detections sent: {sent}")


if __name__ == "__main__":
    main()
