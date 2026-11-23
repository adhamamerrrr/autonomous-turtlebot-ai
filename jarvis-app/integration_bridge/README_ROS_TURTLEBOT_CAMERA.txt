ROS TURTLEBOT4 CAMERA INTEGRATION
=================================

Goal:
  TurtleBot4 OAK-D camera topic -> YOLO smoking detection -> Firebase smoke_detections -> Security Guard Dashboard.

This script creates pending detections only. It does not create confirmed student violations.
The guard confirms/rejects detections inside the Flutter app.

IMPORTANT:
  Run this on the Ubuntu computer that can see the TurtleBot4 ROS 2 topics.
  Do not run this on Windows.

1) Source ROS and set network variables
--------------------------------------
Use the same ROS_DOMAIN_ID that works with your robot. If your robot uses 0, use 0.

  source /opt/ros/jazzy/setup.bash
  export ROS_DOMAIN_ID=0
  export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
  unset ROS_LOCALHOST_ONLY

2) Check that the robot camera topic exists
------------------------------------------

  ros2 topic list | grep -E "oakd|image|rgb|camera"

Expected topic is usually:

  /oakd/rgb/preview/image_raw

Check frames are arriving:

  ros2 topic hz /oakd/rgb/preview/image_raw

3) Prepare Python environment
-----------------------------
Use --system-site-packages so Python can see ROS packages like rclpy and cv_bridge.

  cd ~/Downloads/integrated_stream_test/ngu_campus_assistant/integration_bridge
  python3 -m venv --system-site-packages venv_ros
  source venv_ros/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt

If cv_bridge is missing:

  sudo apt update
  sudo apt install ros-jazzy-cv-bridge ros-jazzy-sensor-msgs -y

4) Copy Firebase Admin key
--------------------------

  cp /home/ubuntu/Downloads/serviceAccountKey.json serviceAccountKey.json

5) Run YOLO on TurtleBot4 camera topic
--------------------------------------

  source /opt/ros/jazzy/setup.bash
  export ROS_DOMAIN_ID=0
  export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
  unset ROS_LOCALHOST_ONLY
  source venv_ros/bin/activate

  python3 ml_ros_camera_to_pending_detection.py \
    --topic /oakd/rgb/preview/image_raw \
    --model best.pt \
    --service-account serviceAccountKey.json \
    --conf 0.05 \
    --process-fps 2 \
    --cooldown 20 \
    --location "Building A - Floor 2" \
    --robot-id TB4-01 \
    --show

6) Expected result
------------------
When smoking is detected:

  Pending smoke detection sent to Firebase.

Then open the Flutter app:

  Security Guard -> Security Dashboard

You should see a pending smoke detection with a photo.

Troubleshooting
---------------
If no camera topic appears:
  - Make sure robot and Ubuntu PC are on the same network.
  - Make sure ROS_DOMAIN_ID matches the robot.
  - Run: ros2 topic list
  - Check that the OAK-D node is running on TurtleBot4.

If topic exists but no frames:
  - Run: ros2 topic hz /oakd/rgb/preview/image_raw
  - If 0 Hz, restart the camera/OAK-D bringup.

If rclpy or cv_bridge import fails:
  - Make sure you used: python3 -m venv --system-site-packages venv_ros
  - Make sure you sourced ROS before running the script.
  - Install: sudo apt install ros-jazzy-cv-bridge ros-jazzy-sensor-msgs -y

If there is delay:
  - Lower process rate: --process-fps 1
  - Lower image size: --imgsz 416
  - Keep cooldown: --cooldown 20
  - The script already uses latest-frame-only logic.
