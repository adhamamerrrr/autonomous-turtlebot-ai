# J.A.R.V.I.S. — Autonomous Campus Assistant and Smoking Detection System

J.A.R.V.I.S. stands for **Joint Assistant for Robotics, Vision, Interaction & Security** (wording used in the supplied project poster).

## Project concept

The supplied graduation-project posters describe a TurtleBot 4-based autonomous campus assistant combining navigation, voice assistance, smoking detection, cloud connectivity and human review.

## Proposed architecture shown in the posters

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

These steps describe the architecture presented in the posters; repository code and testing artifacts are needed to establish which stages are operational.

## Poster-reported detection metrics

| Metric | Poster value |
| --- | ---: |
| Precision | 0.921 |
| Recall | 0.909 |
| mAP@0.5 | 0.955 |
| mAP@0.5:0.95 | 0.761 |
| Best F1 | 0.910 |
| Reported confidence threshold | 0.350 |

**Verification note:** These figures are transcribed from the supplied posters and are not independently validated. Include evaluation scripts, dataset definitions, and test logs before treating them as reproducible benchmark results.

## Supporting evidence

The supplied assets include three indoor mapping photographs, a ROS visualization photograph, a robot assembly illustration, and three poster versions. The original binary images should be committed to a gallery directory to make the visual evidence accessible from GitHub.
