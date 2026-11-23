# Real-World Mapping and ROS Visualization

## Mapping experiment photographs

Three supplied photographs show occupancy-grid maps displayed on a laboratory monitor. Black occupied-cell boundaries outline a large indoor environment with irregular perimeter geometry and scattered interior returns. These are photographs of experimental displays; they are not direct exports of map data and do not independently establish mapping accuracy.

## ROS visualization

Another photograph shows a robot and red point returns in a 3D visualization interface consistent with RViz, alongside an image display. The visible interface indicates sensor data visualization, but the precise sensor model, ROS topic configuration and runtime behavior require confirmation from source code or logs.

## Hardware and design reference

An additional supplied image is an annotated robotic telepresence assembly drawing, labeling the sensor port, speaker grille, height adjustment, articulated base, and other components. Treat this as a design reference, not evidence that every labeled component was built or used.

## Gallery organization

Place the three mapping photographs under `docs/images/mapping/`, the ROS visualization photograph under `docs/images/ros/`, and the assembly drawing under `docs/images/design/` when the original image assets are available in the repository.

For reproducibility, add raw occupancy-grid files, ROS bags, launch files, SLAM parameters, and sensor calibration where available.
