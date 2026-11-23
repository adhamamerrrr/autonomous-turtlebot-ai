# Laser-Based Localization Results

## Beam-Based Sensor Model

The pose log-likelihood heatmap uses a beam-based sensor model with sigma_hit = 0.3 m and a 4-cell search stride. The annotated reference pose is (280, 185).

## Laser Scan — Polar View

The scan spans 250 degrees (±125 degrees from a heading of 0 degrees). The polar plot shows shorter ranges toward corridor walls and longer ranges along the corridor.

## Laser-Range Measurement — Map Overlay

The map overlay places the robot at (280, 185), with heading 0 degrees, a 250-degree field of view, and 2-degree angular increments. Red points represent obstacle hits, and cyan rays represent the sampled laser measurements.

## Interpretation

These visualizations illustrate occupancy-map ray casting and probabilistic sensor-to-map pose scoring. Bright heatmap regions indicate comparatively higher pose likelihood under the model, not independently verified localization accuracy.

| Parameter | Value |
| --- | --- |
| Reference pose | (280, 185) |
| Heading | 0 degrees |
| Laser FOV | 250 degrees |
| Angular step | 2 degrees |
| sigma_hit | 0.3 m |
| Pose search stride | 4 cells |

The associated three plot images are not yet included in this repository.
