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

## Poster-reported detection metrics

| Metric | Poster value |
| --- | ---: |
| Precision | 0.921 |
| Recall | 0.909 |
| mAP@0.5 | 0.955 |
| mAP@0.5:0.95 | 0.761 |
| Best F1 | 0.910 |
| Reported confidence threshold | 0.350 |

These evaluation metrics are reported in the project presentation.

## Supporting evidence

The supplied assets include three indoor mapping photographs, a ROS visualization photograph, a robot assembly illustration, and three poster versions. The mapping and visualization images document the robotics component of the project.

## Trained smoke-detection model artifact

The trained smoke-detection checkpoint has been uploaded to the repository root as [`best.pt`](../best.pt). It is for **smoke/smoking detection**, not violence detection. The checkpoint contains the project's trained model weights for smoke detection.
