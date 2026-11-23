"""
ML stream bridge for the NGU Campus Assistant project.

Purpose:
    Camera/video -> YOLO cigarette/vape detection -> Firestore smoke_detections

This script DOES NOT create a confirmed student violation. It only creates a
pending smoke detection for the security guard to review in the Flutter app.

Examples:
    # Video file test
    python3 ml_stream_to_pending_detection.py --source /home/ubuntu/Downloads/smoke_video.mp4 --conf 0.15 --show

    # Laptop webcam / USB camera
    python3 ml_stream_to_pending_detection.py --source 0 --conf 0.15 --show

    # Robot camera later can be connected through ROS separately. This script is for OpenCV sources.
"""

import argparse
import base64
import os
import queue
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import cv2
import firebase_admin
from firebase_admin import credentials, firestore
from ultralytics import YOLO


class LatestFrameSource:
    """Reads frames in a background thread and keeps only the newest frame.

    This avoids the common delay problem where inference is slower than the
    camera stream and the program keeps processing old frames.
    """

    def __init__(self, source):
        self.source = int(source) if str(source).isdigit() else source
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open source: {source}")
        self.q: "queue.Queue[Tuple[bool, Optional[object]]]" = queue.Queue(maxsize=1)
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()
        return self

    def _reader(self):
        while self.running:
            ok, frame = self.cap.read()
            if not ok:
                self._put_latest((False, None))
                break
            self._put_latest((True, frame))

    def _put_latest(self, item):
        # Remove old frame if queue is full, then put newest frame.
        if self.q.full():
            try:
                self.q.get_nowait()
            except queue.Empty:
                pass
        try:
            self.q.put_nowait(item)
        except queue.Full:
            pass

    def read(self):
        try:
            return self.q.get(timeout=2.0)
        except queue.Empty:
            return False, None

    def release(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self.cap.release()


def init_firebase(service_account_path: str):
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Firebase service account not found: {service_account_path}")
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def encode_frame_base64_jpeg(frame, max_width: int = 900, quality: int = 75) -> str:
    height, width = frame.shape[:2]
    if width > max_width:
        scale = max_width / width
        frame = cv2.resize(frame, (max_width, int(height * scale)))
    ok, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        raise RuntimeError("Could not encode frame as JPEG")
    return base64.b64encode(buffer).decode("utf-8")


def save_local_evidence(frame, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("smoke_%Y%m%d_%H%M%S_%f.jpg")
    path = str(Path(output_dir) / filename)
    cv2.imwrite(path, frame)
    return path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run YOLO cigarette/vape detection on a video/camera stream and send pending detections to Firebase."
    )
    parser.add_argument("--source", default="0", help="Camera index, video path, or stream URL. Example: 0 or smoke_video.mp4")
    parser.add_argument("--model", default="best.pt", help="YOLO model path")
    parser.add_argument("--service-account", default="serviceAccountKey.json", help="Firebase Admin SDK key JSON")
    parser.add_argument("--conf", type=float, default=0.15, help="YOLO confidence threshold")
    parser.add_argument("--imgsz", type=int, default=640, help="YOLO image size")
    parser.add_argument("--frame-skip", type=int, default=5, help="Run inference every N frames")
    parser.add_argument("--cooldown", type=float, default=20.0, help="Seconds between Firebase pending alerts")
    parser.add_argument("--max-alerts", type=int, default=0, help="Stop after N alerts. 0 means unlimited")
    parser.add_argument("--location", default="Building A - Floor 2", help="Location text sent to Firebase")
    parser.add_argument("--robot-id", default="TB4-01", help="Robot ID sent to Firebase")
    parser.add_argument("--target-classes", default="cigarette,vape", help="Comma-separated class names that should trigger a pending smoke detection")
    parser.add_argument("--show", action="store_true", help="Show preview window with detections")
    parser.add_argument("--no-latest-only", action="store_true", help="Process frames sequentially instead of dropping old frames")
    parser.add_argument("--save-local", action="store_true", help="Save detected evidence photos locally in ./evidence")
    parser.add_argument("--evidence-dir", default="evidence", help="Local folder for evidence images when --save-local is used")
    return parser.parse_args()


def open_sequential_source(source):
    src = int(source) if str(source).isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open source: {source}")
    return cap


def main():
    args = parse_args()

    if not os.path.exists(args.model):
        raise FileNotFoundError(f"Model not found: {args.model}")

    db = init_firebase(args.service_account)
    model = YOLO(args.model)
    target_classes = {c.strip().lower() for c in args.target_classes.split(',') if c.strip()}

    print("Starting ML stream bridge...")
    print(f"Source: {args.source}")
    print(f"Model classes: {model.names}")
    print(f"Target classes: {sorted(target_classes)}")
    print("Firestore collection: smoke_detections")
    print("This creates PENDING detections only. Guard confirmation creates real violations.")
    print("Press Ctrl+C to stop. If --show is used, press q in the preview window.")

    latest_only = not args.no_latest_only
    source = None
    cap = None

    if latest_only:
        source = LatestFrameSource(args.source).start()
    else:
        cap = open_sequential_source(args.source)

    frame_index = 0
    last_alert_time = 0.0
    alerts_sent = 0

    try:
        while True:
            if latest_only:
                ok, frame = source.read()
            else:
                ok, frame = cap.read()

            if not ok or frame is None:
                print("Video/camera source ended or no frame received.")
                break

            frame_index += 1
            if frame_index % max(1, args.frame_skip) != 0:
                if args.show:
                    cv2.imshow("Campus Assistant ML Stream", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                continue

            results = model.predict(frame, conf=args.conf, imgsz=args.imgsz, device="cpu", verbose=False)
            result = results[0]

            best_detection = None
            for box in result.boxes:
                cls_id = int(box.cls[0])
                class_name = str(model.names[cls_id]).lower()
                confidence = float(box.conf[0])
                if class_name in target_classes:
                    if best_detection is None or confidence > best_detection["confidence"]:
                        best_detection = {"class_name": class_name, "confidence": confidence}

            annotated = result.plot()

            if best_detection:
                now = time.time()
                conf = best_detection["confidence"]
                print(f"{datetime.now().strftime('%H:%M:%S')} Detected {best_detection["class_name"]}, confidence={conf:.3f}")

                if now - last_alert_time >= args.cooldown:
                    # Send annotated frame so the guard sees the detection box.
                    photo_base64 = encode_frame_base64_jpeg(annotated)
                    doc = {
                        "detectionType": "Smoking",
                        "confidence": conf,
                        "location": args.location,
                        "robotId": args.robot_id,
                        "status": "Pending Review",
                        "source": "YOLO ML Stream Detector",
                        "photoBase64": photo_base64,
                        "timestamp": firestore.SERVER_TIMESTAMP,
                    }

                    if args.save_local:
                        local_path = save_local_evidence(annotated, args.evidence_dir)
                        doc["localEvidencePath"] = local_path
                        print(f"Saved local evidence: {local_path}")

                    db.collection("smoke_detections").add(doc)
                    last_alert_time = now
                    alerts_sent += 1
                    print("Pending smoke detection sent to Firebase.")

                    if args.max_alerts and alerts_sent >= args.max_alerts:
                        print(f"Reached max alerts ({args.max_alerts}). Stopping.")
                        break
                else:
                    remaining = args.cooldown - (now - last_alert_time)
                    print(f"Cooldown active. Duplicate alert not sent. Remaining {remaining:.1f}s")

            if args.show:
                cv2.imshow("Campus Assistant ML Stream", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        if source is not None:
            source.release()
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print(f"Total pending detections sent: {alerts_sent}")


if __name__ == "__main__":
    main()
