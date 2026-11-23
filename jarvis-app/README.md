# J.A.R.V.I.S. Flutter application and detection integration

This folder contains the extracted, browsable Flutter application and Python integration source for the TurtleBot 4 campus assistant.

## Source code

- [Flutter application](lib/main.dart)
- [Flutter package dependencies](pubspec.yaml)
- [Widget test](test/widget_test.dart)
- [Image detection bridge](integration_bridge/ml_image_to_pending_detection.py)
- [Live camera detection bridge](integration_bridge/ml_live_to_pending_detection.py)
- [Video stream detection bridge](integration_bridge/ml_stream_to_pending_detection.py)
- [ROS camera detection bridge](integration_bridge/ml_ros_camera_to_pending_detection.py)
- [ROS compressed camera detection bridge](integration_bridge/ml_ros_compressed_camera_to_pending_detection.py)
- [Sample database utility](integration_bridge/seed_sample_database.py)
- [Python dependencies](integration_bridge/requirements.txt)
- [Model setup](MODEL_SETUP.md)

## Selected smoke-detection model

The selected newer trained checkpoint is [`jarvis-best-new.pt`](../jarvis-best-new.pt). The earlier [`best.pt`](../best.pt) remains available. See [model setup](MODEL_SETUP.md) for configuring a local model copy.

## Source archive and assets

The [original sanitized source archive](../jarvis-github-source-safe.zip) is retained for convenience. Text source files have now been extracted into this folder. The NGU logo image is still inside the ZIP and has not yet been uploaded as a standalone image.

Never commit Firebase service-account keys or other credentials.
