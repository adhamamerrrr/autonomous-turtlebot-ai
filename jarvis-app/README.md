# J.A.R.V.I.S. Flutter application and integration source

The [uploaded source archive](../jarvis-github-source-safe.zip) contains the Flutter mobile application and Python integration scripts for the TurtleBot 4 campus assistant.

## Source archive layout

- `jarvis-app/lib/main.dart` — Flutter application entry point and UI
- `jarvis-app/pubspec.yaml` / `pubspec.lock` — Flutter dependencies
- `jarvis-app/test/widget_test.dart` — Flutter widget test
- `jarvis-app/integration_bridge/ml_image_to_pending_detection.py` — image detection bridge
- `jarvis-app/integration_bridge/ml_live_to_pending_detection.py` — live camera bridge
- `jarvis-app/integration_bridge/ml_stream_to_pending_detection.py` — stream detection bridge
- `jarvis-app/integration_bridge/ml_ros_camera_to_pending_detection.py` — ROS camera bridge
- `jarvis-app/integration_bridge/ml_ros_compressed_camera_to_pending_detection.py` — compressed ROS image bridge
- `jarvis-app/integration_bridge/seed_sample_database.py` — sample data utility
- `jarvis-app/integration_bridge/requirements.txt` — Python dependencies
- `jarvis-app/integration_bridge/data.yaml` — model dataset configuration

## Official checkpoint

Use [`jarvis-best-new.pt`](../jarvis-best-new.pt) as the selected newer smoke-detection model. The earlier [`best.pt`](../best.pt) remains for comparison. If an integration script expects `best.pt` in its working directory, explicitly supply or copy the selected checkpoint there.

## Important distinction

The downloadable ZIP contains the source files; the source files have **not yet been extracted into individual GitHub paths**. The diagrams and screenshots supplied in the project discussion are likewise not yet published as image files. See [project overview](../docs/jarvis-project-overview.md) for the supplied evaluation figures and workflow descriptions.
