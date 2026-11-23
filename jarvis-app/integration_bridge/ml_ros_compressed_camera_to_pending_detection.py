"""
ROS 2 TurtleBot4 compressed camera bridge for the NGU Campus Assistant project.

Purpose:
    TurtleBot4 ROS compressed image topic -> YOLO cigarette/vape detection -> Firestore smoke_detections

This script subscribes to sensor_msgs/CompressedImage, so use it with topics like:
    /oakd/rgb/preview/image_raw/compressed

It DOES NOT create confirmed student violations. It creates PENDING smoke detections only.
The security guard reviews the photo in the Flutter app and then confirms or rejects it.

Example:
    source /opt/ros/jazzy/setup.bash
    export ROS_DOMAIN_ID=0
    export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    unset ROS_LOCALHOST_ONLY

    python3 ml_ros_compressed_camera_to_pending_detection.py \
      --topic /oakd/rgb/preview/image_raw/compressed \
      --model best.pt \
      --service-account serviceAccountKey.json \
      --conf 0.05 \
      --imgsz 640 \
      --process-fps 3 \
      --cooldown 20 \
      --location "Building A - Floor 2" \
      --robot-id TB4-01 \
      --show
"""

import argparse
import base64
import os
import threading
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
from ultralytics import YOLO

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import CompressedImage


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
    filename = datetime.now().strftime("ros_compressed_smoke_%Y%m%d_%H%M%S_%f.jpg")
    path = str(Path(output_dir) / filename)
    cv2.imwrite(path, frame)
    return path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Subscribe to TurtleBot4 ROS compressed camera topic, run YOLO cigarette/vape detection, and send pending detections to Firebase."
    )
    parser.add_argument("--topic", default="/oakd/rgb/preview/image_raw/compressed", help="ROS 2 CompressedImage topic")
    parser.add_argument("--model", default="best.pt", help="YOLO model path")
    parser.add_argument("--service-account", default="serviceAccountKey.json", help="Firebase Admin SDK key JSON")
    parser.add_argument("--conf", type=float, default=0.15, help="YOLO confidence threshold")
    parser.add_argument("--imgsz", type=int, default=640, help="YOLO image size")
    parser.add_argument("--process-fps", type=float, default=2.0, help="How many latest frames to process per second")
    parser.add_argument("--cooldown", type=float, default=20.0, help="Seconds between Firebase pending alerts")
    parser.add_argument("--max-alerts", type=int, default=0, help="Stop after N alerts. 0 means unlimited")
    parser.add_argument("--location", default="Building A - Floor 2", help="Location text sent to Firebase")
    parser.add_argument("--robot-id", default="TB4-01", help="Robot ID sent to Firebase")
    parser.add_argument("--target-classes", default="cigarette,vape", help="Comma-separated class names that should trigger a pending smoke detection")
    parser.add_argument("--device", default="cpu", help="YOLO device, usually cpu unless CUDA works")
    parser.add_argument("--show", action="store_true", help="Show preview window with detections")
    parser.add_argument("--save-local", action="store_true", help="Save detected evidence photos locally in ./evidence_ros_compressed")
    parser.add_argument("--evidence-dir", default="evidence_ros_compressed", help="Local folder for evidence images")
    return parser.parse_args()


class RosCompressedCameraSmokeDetector(Node):
    def __init__(self, args):
        super().__init__("campus_assistant_compressed_smoke_detector")
        self.args = args
        self.lock = threading.Lock()
        self.latest_frame = None
        self.latest_stamp = None
        self.received_frames = 0
        self.decoded_frames = 0
        self.processed_frames = 0
        self.last_alert_time = 0.0
        self.alerts_sent = 0

        if not os.path.exists(args.model):
            raise FileNotFoundError(f"Model not found: {args.model}")

        self.db = init_firebase(args.service_account)
        self.model = YOLO(args.model)
        self.target_classes = {c.strip().lower() for c in args.target_classes.split(',') if c.strip()}

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.subscription = self.create_subscription(CompressedImage, args.topic, self.image_callback, qos)
        timer_period = 1.0 / max(args.process_fps, 0.1)
        self.timer = self.create_timer(timer_period, self.process_latest_frame)

        self.get_logger().info("Starting ROS COMPRESSED camera ML bridge...")
        self.get_logger().info(f"Topic: {args.topic}")
        self.get_logger().info(f"Model classes: {self.model.names}")
        self.get_logger().info(f"Target classes: {sorted(self.target_classes)}")
        self.get_logger().info("Firestore collection: smoke_detections")
        self.get_logger().info("This creates PENDING detections only. Guard confirmation creates real violations.")

    def image_callback(self, msg: CompressedImage):
        self.received_frames += 1
        try:
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is None:
                self.get_logger().warning("Could not decode compressed frame")
                return
        except Exception as exc:
            self.get_logger().error(f"Compressed image decode failed: {exc}")
            return

        with self.lock:
            # Latest-frame-only: overwrite old frame to avoid delay.
            self.latest_frame = frame
            self.latest_stamp = msg.header.stamp
            self.decoded_frames += 1

    def process_latest_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return
            frame = self.latest_frame.copy()

        self.processed_frames += 1
        results = self.model.predict(
            frame,
            conf=self.args.conf,
            imgsz=self.args.imgsz,
            device=self.args.device,
            verbose=False,
        )
        result = results[0]

        best_detection = None
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = str(self.model.names[cls_id]).lower()
            confidence = float(box.conf[0])
            if class_name in self.target_classes:
                if best_detection is None or confidence > best_detection["confidence"]:
                    best_detection = {"class_name": class_name, "confidence": confidence}

        annotated = result.plot()

        if best_detection:
            now = time.time()
            conf = best_detection["confidence"]
            self.get_logger().info(f"Detected {best_detection["class_name"]}, confidence={conf:.3f}")

            if now - self.last_alert_time >= self.args.cooldown:
                photo_base64 = encode_frame_base64_jpeg(annotated)
                doc = {
                    "detectionType": "Smoking",
                    "confidence": conf,
                    "location": self.args.location,
                    "robotId": self.args.robot_id,
                    "status": "Pending Review",
                    "source": "YOLO ROS TurtleBot4 Compressed Camera Detector",
                    "photoBase64": photo_base64,
                    "timestamp": firestore.SERVER_TIMESTAMP,
                }

                if self.args.save_local:
                    local_path = save_local_evidence(annotated, self.args.evidence_dir)
                    doc["localEvidencePath"] = local_path
                    self.get_logger().info(f"Saved local evidence: {local_path}")

                self.db.collection("smoke_detections").add(doc)
                self.last_alert_time = now
                self.alerts_sent += 1
                self.get_logger().info("Pending smoke detection sent to Firebase.")

                if self.args.max_alerts and self.alerts_sent >= self.args.max_alerts:
                    self.get_logger().info(f"Reached max alerts ({self.args.max_alerts}). Stopping.")
                    rclpy.shutdown()
            else:
                remaining = self.args.cooldown - (now - self.last_alert_time)
                self.get_logger().info(f"Cooldown active. Duplicate alert not sent. Remaining {remaining:.1f}s")

        if self.args.show:
            cv2.imshow("Campus Assistant ROS Compressed Camera", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                rclpy.shutdown()

    def destroy_node(self):
        cv2.destroyAllWindows()
        self.get_logger().info(f"Received compressed frames: {self.received_frames}")
        self.get_logger().info(f"Decoded frames: {self.decoded_frames}")
        self.get_logger().info(f"Processed frames: {self.processed_frames}")
        self.get_logger().info(f"Total pending detections sent: {self.alerts_sent}")
        super().destroy_node()


def main():
    args = parse_args()
    rclpy.init()
    node = RosCompressedCameraSmokeDetector(args)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()
        else:
            node.destroy_node()


if __name__ == "__main__":
    main()
