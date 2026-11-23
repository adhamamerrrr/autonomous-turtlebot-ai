# AI portfolio implementation and evidence matrix

Status as of November 2026. This matrix describes **this portfolio repository**, not the original graduation project's source or measurements. See [PROVENANCE.md](../PROVENANCE.md).

| Capability | Source implemented | Automated tests authored | Model trained | Independent evaluation | Full robot integration verified |
| --- | --- | --- | --- | --- | --- |
| PyTorch smoke image classification | Yes | Yes | Yes, small public-data baseline | Yes, 100 held-out images; 66% accuracy, 50% event recall | No |
| YOLO smoke bounding-box detection | Training CLI only | Dataset YAML checks | **No** | **No** | No |
| Temporal CNN/GRU video event pipeline | Yes | Yes, synthetic fixtures | Synthetic-only software check | **No real-video evidence** | No |
| Video inference CLI | Yes | Synthetic video tests authored | Requires external compatible checkpoint | No real violence evaluation | No |
| ROS2 velocity supervisor and alerts | Yes | Offline and ROS2 checks previously reported | Not applicable | Software checks only | Full Gazebo navigation not verified |
| Smoke false-negative / false-positive audit | Yes | Regression tests authored | Uses existing baseline | Recomputes saved test predictions | Not applicable |

## What recruiters can run

```bash
python scripts/audit_model.py results/smoke_results.json
python scripts/analyze_errors.py --manifest results/smoke_manifest.csv --results results/smoke_results.json
python -m pytest -q tests/test_model_audit.py tests/test_error_analysis.py tests/test_predict_video.py tests/test_yolo_smoke.py
```

Optional localization experiment (requires separately installed Ultralytics, pretrained weights and a properly licensed bounding-box dataset):

```bash
pip install ultralytics
python scripts/train_yolo_smoke.py --data /path/to/data.yaml --device cpu --epochs 40
```

This experiment is **not** the same as the trained image-level smoke classifier. It has no published localization mAP, detection recall, or weights yet. Do not claim it does.

## Evidence needed before claiming production-ready AI

- Verify dataset rights, class labels, and scene/video-level separation.
- Train on authentic data and save experiment configurations, checkpoints and validation results.
- Evaluate an untouched held-out test set with per-class metrics, error analysis, and latency measurements.
- Test ROS2/Gazebo integration on a compatible host; test hardware only with supervision and fail-safe controls.
- Document the applicant's actual team contribution separately from new portfolio reconstruction work.

**No claims:** Real-world violence recognition accuracy, validated YOLO smoke localization, commercial safety suitability, or a completed end-to-end robotics simulation.
