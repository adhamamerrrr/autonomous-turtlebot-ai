Updated security flow
=====================

The robot/ML code must NOT write directly to the `violations` collection.
It should write unassigned detections to:

  smoke_detections

Required fields:

  detectionType: "Smoking"
  confidence: 0.0 to 1.0
  location: robot/map location
  robotId: robot identifier, e.g. "TB4-01"
  status: "Pending Review"
  source: "YOLO ML Model" or "Robot Camera"
  timestamp: server timestamp
  photoUrl: optional image URL
  photoBase64: optional JPEG image encoded as base64

Security guard flow:

  1. Guard sees pending detection photo in Security Dashboard.
  2. Guard chooses False Alarm OR True Violation.
  3. If False Alarm: only `smoke_detections` is updated. No student sees anything.
  4. If True Violation: guard enters student ID manually.
  5. App creates a confirmed document in `violations` with confirmed=true.
  6. Student account only displays violations where studentId matches and confirmed=true.

Test command:

  python3 integration_bridge/ml_image_to_pending_detection.py \
    --image /home/ubuntu/Downloads/smoke.jpg \
    --model best.pt \
    --service-account serviceAccountKey.json \
    --conf 0.15 \
    --location "Building A - Floor 2" \
    --robot-id TB4-01
