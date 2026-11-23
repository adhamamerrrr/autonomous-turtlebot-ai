Compressed OAK-D camera script
==============================

Use this script if you want to subscribe to the compressed camera topic:

  /oakd/rgb/preview/image_raw/compressed

Script:

  ml_ros_compressed_camera_to_pending_detection.py

Run:

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

Notes:
- This script subscribes to sensor_msgs/CompressedImage.
- It reduces ROS network bandwidth compared with the raw topic.
- It still decodes frames on the computer before YOLO inference.
- It creates PENDING detections only in Firestore smoke_detections.
- Guard confirmation in the Flutter app is still required before a student violation is created.
