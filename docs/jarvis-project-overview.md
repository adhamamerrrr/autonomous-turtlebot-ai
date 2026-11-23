# J.A.R.V.I.S. — Autonomous Campus Assistant and Smoking Detection System

J.A.R.V.I.S. stands for **Joint Assistant for Robotics, Vision, Interaction & Security** (wording used in the supplied project poster).

## Project concept

The supplied graduation-project posters describe a TurtleBot 4-based autonomous campus assistant combining navigation, voice assistance, smoking detection, cloud connectivity and human review.

## System architecture

- **Robot:** TurtleBot 4 with ROS 2 Jazzy and Nav2 for navigation.
- **Edge inference:** OAK-D Lite VPU for first-stage candidate smoking detection.
- **PC verification:** YOLO-based recheck with a confidence threshold.
- **Backend:** Firebase Firestore for robot status, detections, commands and reviews.
- **Mobile interface:** Flutter dashboard for patrol controls, incident review and student warnings.
- **Human-in-the-loop:** Security personnel confirm or reject candidate incidents.

## Two-stage detection workflow

1. Edge model identifies a candidate smoking event.
2. Candidate image is sent for PC-side recheck.
3. The recheck filters low-confidence detections and queues qualifying cases.
4. A human reviewer confirms or rejects the incident.
5. Confirmed incidents can be reflected in the application's warning records.

## Smoke-detection model evaluation (supplied project results)

The project materials compare four training runs. **Run 4** is labeled the final selected model, with phone/pen/background fine-tuning. The figures below are transcribed from the supplied charts and run summary; they have not been independently recomputed from a test dataset.

| Run | Precision | Recall | mAP@0.5 | Best F1 | Missed cigarette | Missed vape | Background false positives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 — fixed dataset, 20 epochs | 0.893 | 0.843 | 0.920 | 0.870 | 212 | 174 | 628 |
| 2 — fixed dataset, 50 epochs | 0.923 | 0.887 | 0.948 | 0.900 | 148 | 112 | 458 |
| 3 — robot-style background fine-tune | 0.927 | 0.890 | 0.947 | 0.910 | 159 | 104 | 462 |
| **4 — phone/pen/background fine-tune (selected)** | **0.921** | **0.909** | **0.955** | **0.910** | **129** | **87** | **447** |

The supplied project poster additionally reports mAP@0.5:0.95 of 0.761 and a confidence threshold of 0.350. These values should be attributed to the project presentation unless independently reproduced.

## Integrated application and evidence

The supplied `ngu_campus_assistant_new_model_integrated.zip` contains Flutter application source (`lib/main.dart`), Android/iOS project files, and Python integration bridges for image, live video, streaming video, ROS camera, and compressed ROS camera detections. Its `integration_bridge/best.pt` is the supplied newer smoke-detection checkpoint. The supplied screenshots show the TB4-01 robot control interface, security review queue, and reviewed detections interface. Do not publish live credentials or configuration secrets from the application archive.

The newer model has been uploaded separately as [`jarvis-best-new.pt`](../jarvis-best-new.pt). The existing root `best.pt` remains the earlier model. The [sanitized Flutter and Python integration source archive](../jarvis-github-source-safe.zip) is also uploaded.

## Supporting evidence

The supplied assets include three indoor mapping photographs, a ROS visualization photograph, a robot assembly illustration, and three poster versions. The mapping and visualization images document the robotics component of the project.

## Trained smoke-detection model artifact

The selected newer smoke-detection checkpoint is [`jarvis-best-new.pt`](../jarvis-best-new.pt), with an earlier checkpoint preserved as [`best.pt`](../best.pt). It is for **smoke/smoking detection**, not violence detection. The checkpoint contains the project's trained model weights for smoke detection.

## Architecture and workflow diagrams

Five supplied project diagrams document the following subsystem designs:

1. **Integrated system architecture:** TurtleBot 4 robot, external Ubuntu PC, J.A.R.V.I.S. voice pipeline, ROS 2 Jazzy topics, Nav2 patrol/navigation nodes, sensors, and safety control.
2. **Detailed deployment architecture:** External PC voice processing and monitoring, on-robot patrol/navigation and sensor interfaces, ROS 2 DDS communication, staff JSON data, maps, waypoints, and logs.
3. **Voice assistant interaction:** Wake word → voice activity detection → speech-to-text → intent recognition → dialogue management → reachability/confirmation → ROS 2 command → robot execution → text-to-speech.
4. **Navigation/patrol startup:** Robot bring-up → saved map → AMCL localization → initial pose → TF verification → RViz → Nav2 → waypoint patrol loop and recovery actions.
5. **Smoke detection and human review:** OAK-D Lite/YOLOv8n candidate detection → PC-side recheck → pending security review → human confirmation or false-alarm rejection → Firebase records → student visibility of confirmed violations only.

The diagrams are architectural references. They should not by themselves be treated as proof that every subsystem was integrated or tested. Original diagram images should be added under `docs/architecture/` for inline README display.
