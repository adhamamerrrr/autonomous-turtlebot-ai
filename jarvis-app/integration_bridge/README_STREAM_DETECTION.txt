NGU Campus Assistant - ML Stream Pending Detection
==================================================

Purpose
-------
This script connects the current YOLO model to Firebase for live/video testing.
It does NOT create a student violation directly.
It creates a pending document in Firestore collection:

    smoke_detections

The Security Guard account reviews it, then marks it as False Alarm or confirms it
as a true violation and manually enters the student ID.

Files
-----
- best.pt
- serviceAccountKey.json      <-- you must add this locally; it is not included in the package
- ml_stream_to_pending_detection.py
- ml_image_to_pending_detection.py
- requirements.txt

Setup
-----
cd ~/Downloads/integrated_stream_test/ngu_campus_assistant/integration_bridge
cp /home/ubuntu/Downloads/serviceAccountKey.json serviceAccountKey.json
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

Image test
----------
python3 ml_image_to_pending_detection.py \
  --image /home/ubuntu/Downloads/smoke.jpg \
  --model best.pt \
  --service-account serviceAccountKey.json \
  --conf 0.15 \
  --location "Building A - Floor 2" \
  --robot-id TB4-01

Video file test
---------------
Put a video at /home/ubuntu/Downloads/smoke_video.mp4 then run:

python3 ml_stream_to_pending_detection.py \
  --source /home/ubuntu/Downloads/smoke_video.mp4 \
  --model best.pt \
  --service-account serviceAccountKey.json \
  --conf 0.15 \
  --frame-skip 5 \
  --cooldown 20 \
  --location "Building A - Floor 2" \
  --robot-id TB4-01 \
  --show

Camera test
-----------
python3 ml_stream_to_pending_detection.py \
  --source 0 \
  --model best.pt \
  --service-account serviceAccountKey.json \
  --conf 0.15 \
  --frame-skip 5 \
  --cooldown 20 \
  --location "Building A - Floor 2" \
  --robot-id TB4-01 \
  --show

Useful options
--------------
--frame-skip 5       Run model every 5 frames to reduce lag.
--cooldown 20        Send only one Firebase alert every 20 seconds.
--max-alerts 1       Stop after sending one pending detection.
--save-local         Save evidence photos locally in ./evidence.
--no-latest-only     Process every frame sequentially. Default drops old frames to reduce delay.

Expected app result
-------------------
Security Guard -> Security Dashboard:
You should see a Pending Smoke Detection with image, confidence, robot ID, location, and time.
It will not appear in student account until the guard confirms it and enters the student ID.
