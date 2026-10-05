# Recovery and reconstruction provenance

This repository is a new AI-assisted reconstruction made in October 2026 from the supplied autonomous TurtleBot project description. It is not recovered graduation-project code. Original SLAM maps, smoke/violence datasets, trained model weights and integration logs were unavailable.

A separate TurtleBot4 course color-approach script was recovered from Appendix C of `TurtleBot4_Project2_Report (1).docx`. That report lists four team members including Adham Wagdy. Its report SHA256 is `eb58b834c6d10cc0fbd118326854e4b06a7b568f653db4702849e3274a9e0449`. It is team work, not sole authorship, and is preserved separately. No team source is copied into this MIT reconstruction or relicensed.

New work here includes the velocity supervisor, temporal vision baseline, training/manifest tools, ROS2 integration scripts, launch composition and tests. SLAM and navigation algorithms are supplied by upstream SLAM Toolbox and Nav2, not claimed as algorithms written by the portfolio owner. TurtleBot3 simulation is supplied by ROBOTIS.

`config/nav2.yaml` is an upstream ROBOTIS Waffle Pi configuration from `ROBOTIS-GIT/turtlebot3`, commit `0c0be84e3f5c3194fb2adea8426a58a96060eab5`, under Apache 2.0; its license is `config/ROBOTIS-LICENSE`. Other new code is MIT. Simulation source checkout: `ROBOTIS-GIT/turtlebot3_simulations`, Jazzy commit `45633014a14e8f438495b532a723e4ad45cbbd31` (Apache 2.0), obtained during validation, not vendored.

The small smoke checkpoint is newly trained on the credited public D-Fire subset. It is not a recovered historical model. RWF-2000's official repository currently withholds video downloads for privacy reasons and restricts modification, redistribution and commercial use. No RWF-2000 videos or model trained on them are included. Synthetic video fixtures validate software plumbing only and never establish violence-detection quality.
