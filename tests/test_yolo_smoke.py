"""Unit tests for the optional YOLO smoke dataset contract (no GPU required)."""
from pathlib import Path

import pytest

from scripts.train_yolo_smoke import check_dataset


def test_smoke_class_required(tmp_path):
    yaml = pytest.importorskip("yaml")
    config = tmp_path / "data.yaml"
    config.write_text("train: images/train\nval: images/val\nnames: [fire, smoke]\n")
    result = check_dataset(config)
    assert "smoke" in result["names"]
    config.write_text("train: images/train\nval: images/val\nnames: [fire]\n")
    with pytest.raises(ValueError, match="smoke"):
        check_dataset(config)


def test_missing_validation_rejected(tmp_path):
    pytest.importorskip("yaml")
    config = tmp_path / "data.yaml"
    config.write_text("train: images/train\nnames: [smoke]\n")
    with pytest.raises(ValueError, match="val"):
        check_dataset(config)
