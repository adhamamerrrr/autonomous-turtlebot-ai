"""Video inference contract tests; synthetic video is not a violence dataset."""
import cv2
import numpy as np
import pytest

from scripts.predict_video import predict_video, sample_video


def test_sample_video_eight_frames(tmp_path):
    video = tmp_path / "fixture.avi"
    writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"),
                             5.0, (64, 64))
    assert writer.isOpened()
    for i in range(12):
        writer.write(np.full((64, 64, 3), i * 15, dtype=np.uint8))
    writer.release()
    frames = sample_video(video)
    assert len(frames) == 8
    assert all(frame.shape == (64, 64, 3) for frame in frames)
    assert float(frames[-1].mean()) > float(frames[0].mean())


def test_missing_video_rejected(tmp_path):
    with pytest.raises(ValueError):
        sample_video(tmp_path / "missing.avi")


def test_invalid_threshold_rejected_before_loading_checkpoint(tmp_path):
    with pytest.raises(ValueError):
        predict_video(tmp_path / "missing.avi", tmp_path / "missing.pt", 1.0)
