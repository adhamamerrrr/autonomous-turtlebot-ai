# AI engineering project walkthrough — graduate interviews

## Problem and system

The original graduation project involved an autonomous TurtleBot and visual detection workflows. The goal was to combine camera-based event detection with navigation and obstacle awareness. Explain precisely which contributions were yours and which belonged to teammates or upstream frameworks.

This repository is a **new portfolio implementation** that demonstrates a ROS2/Gazebo navigation stack, a separate velocity safety gate, and PyTorch-based visual-event processing. It is not the original university source code, model, or original reported accuracy. See [PROVENANCE.md](../PROVENANCE.md).

## Smoke detection: what can be demonstrated

1. **Data preparation:** inspect the source dataset and labels, document source/license, maintain train/validation/test splits, check exact duplicates and source-group overlap.
2. **Modeling:** train a small PyTorch CNN/GRU baseline, select the best epoch using validation macro F1, and preserve the checkpoint and experiment metadata.
3. **Evaluation:** inspect held-out confusion matrix and class-specific recall. Current public-data baseline: 41 true negatives, 9 false positives, 25 false negatives, 25 true positives (100 test images). Accuracy 66%, smoke recall 50%.
4. **Failure analysis:** use `scripts/analyze_errors.py` to inspect missed smoke images and false alarms. Do not tune hyperparameters or thresholds on the held-out test set.
5. **Integration:** demonstrate the ROS2 event pipeline and supervisor separately; full Gazebo end-to-end navigation has not yet passed verification in this environment.

### Reproducible interview commands

```bash
python scripts/audit_model.py results/smoke_results.json
python scripts/analyze_errors.py --manifest results/smoke_manifest.csv --results results/smoke_results.json
pytest -q tests/test_model_audit.py tests/test_error_analysis.py
```

## Violence detection: what can and cannot be claimed

- Implemented: eight-frame video preprocessing, CNN/GRU architecture, training pipeline, checkpoint loading, and video inference CLI.
- Verified historically in this portfolio: synthetic AVI data flow, not meaningful violence classification.
- **Not yet implemented with real evidence:** an independently evaluated, trained real-world violence classifier.
- An authorized video dataset, its usage rights, source-group split, metrics, and failure analysis are required before claiming detection accuracy.

```bash
# Requires a separately trained, evaluated checkpoint:
python scripts/predict_video.py /path/to/video.mp4 --model models/violence/violence.pt
```

## Typical technical questions

**Why use recall for smoke?** Missed smoke events may be more costly than false alarms. Recall must be considered together with precision, false alarms, latency and operational constraints.

**Why separate training and test data?** To avoid choosing a model on the same data used to estimate its generalization. Related images from one scene or video should stay within a single split.

**Why a temporal model for video?** A GRU can summarize motion over frames, unlike a single-frame classifier. This architectural rationale does not prove the model performs well on real videos.

**How does AI connect to robotics?** Camera detections publish alerts; a separate supervisor gates navigation commands alongside LiDAR clearance and freshness checks. SLAM Toolbox and Nav2 provide upstream mapping and navigation rather than being newly implemented here.

**What would you improve next?** Obtain a larger, well-grouped and licensed dataset; compare transfer learning with the small baseline; report per-class metrics and calibration; test on unseen scenes; profile end-to-end latency; validate the robot in a safe simulation.

## How to describe the project on a CV

*Autonomous TurtleBot — computer vision and robotics graduation project (team).* Worked on visual-detection workflows and robot integration. Discuss actual personal contributions in the interview; cite specific results only when original evidence is available.

For this repository, separately state: *Built and evaluated a portfolio PyTorch smoke-detection baseline and temporal video-inference pipeline with reproducible evaluation and error-analysis scripts.* This does not imply the real-world violence model has been trained or deployed.

Never represent the current 66% public-data baseline as the original university project's accuracy, or claim the synthetic video pipeline is a validated violence detector.
