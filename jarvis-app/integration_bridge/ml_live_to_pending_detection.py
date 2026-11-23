import argparse
import base64
import os
import time
from datetime import datetime

import cv2
import firebase_admin
from firebase_admin import credentials, firestore
from ultralytics import YOLO


def frame_to_base64_jpeg(frame, max_width=800, quality=70):
    h, w = frame.shape[:2]
    if w > max_width:
        scale = max_width / w
        frame = cv2.resize(frame, (max_width, int(h * scale)))
    ok, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        raise RuntimeError('Could not encode frame as JPEG')
    return base64.b64encode(buffer).decode('utf-8')


def init_firebase(service_account_path):
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f'Firebase service account not found: {service_account_path}')
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def open_source(source):
    # Allow webcam source like "0" or a video/image path.
    if str(source).isdigit():
        return cv2.VideoCapture(int(source))
    return cv2.VideoCapture(source)


def main():
    parser = argparse.ArgumentParser(description='Run YOLO smoking detection and send pending detections to Firebase for guard review.')
    parser.add_argument('--source', default='0', help='Camera index, video path, or stream URL. Example: 0 or /home/ubuntu/Downloads/smoke_video.mp4')
    parser.add_argument('--model', default='best.pt', help='YOLO model path')
    parser.add_argument('--service-account', default='serviceAccountKey.json', help='Firebase Admin SDK JSON')
    parser.add_argument('--conf', type=float, default=0.15, help='YOLO confidence threshold')
    parser.add_argument('--imgsz', type=int, default=640, help='YOLO input image size')
    parser.add_argument('--frame-skip', type=int, default=5, help='Run detection every N frames')
    parser.add_argument('--cooldown', type=float, default=15.0, help='Seconds between Firebase alerts')
    parser.add_argument('--location', default='Robot Camera Test Location', help='Robot/map location text')
    parser.add_argument('--robot-id', default='TB4-01', help='Robot ID')
    parser.add_argument('--target-classes', default='cigarette,vape', help='Comma-separated class names that should trigger a pending smoke detection')
    parser.add_argument('--show', action='store_true', help='Show video preview with YOLO boxes')
    args = parser.parse_args()

    if not os.path.exists(args.model):
        raise FileNotFoundError(f'Model not found: {args.model}')

    db = init_firebase(args.service_account)
    model = YOLO(args.model)
    target_classes = {c.strip().lower() for c in args.target_classes.split(',') if c.strip()}

    cap = open_source(args.source)
    if not cap.isOpened():
        raise RuntimeError(f'Could not open video source: {args.source}')

    print('Started ML live detector.')
    print('Press q in the video window to stop, or Ctrl+C in terminal.')
    print(f'Sending pending detections to Firestore collection: smoke_detections')
    print(f'Model classes: {model.names}')
    print(f'Target classes: {sorted(target_classes)}')

    frame_index = 0
    last_alert_time = 0.0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print('Video source ended or frame could not be read.')
                break

            frame_index += 1
            if frame_index % max(1, args.frame_skip) != 0:
                if args.show:
                    cv2.imshow('YOLO Smoking Detector', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                continue

            results = model.predict(frame, conf=args.conf, imgsz=args.imgsz, device='cpu', verbose=False)
            result = results[0]

            smoking_detected = False
            best_confidence = 0.0
            best_class_name = None

            for box in result.boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[cls_id].lower()
                if class_name in target_classes and confidence > best_confidence:
                    smoking_detected = True
                    best_confidence = confidence
                    best_class_name = class_name

            if smoking_detected:
                print(f'{datetime.now().strftime("%H:%M:%S")} Detected {best_class_name}, confidence={best_confidence:.3f}')
                now = time.time()
                if now - last_alert_time >= args.cooldown:
                    photo_base64 = frame_to_base64_jpeg(frame)
                    db.collection('smoke_detections').add({
                        'detectionType': 'Smoking',
                        'confidence': best_confidence,
                        'location': args.location,
                        'robotId': args.robot_id,
                        'status': 'Pending Review',
                        'source': 'YOLO ML Live Detector',
                        'photoBase64': photo_base64,
                        'timestamp': firestore.SERVER_TIMESTAMP,
                    })
                    last_alert_time = now
                    print('Pending smoke detection sent to Firebase for security guard review.')
                else:
                    remaining = args.cooldown - (now - last_alert_time)
                    print(f'Cooldown active, not sending duplicate alert. Remaining: {remaining:.1f}s')

            if args.show:
                annotated = result.plot()
                cv2.imshow('YOLO Smoking Detector', annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        print('Stopped by user.')
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
