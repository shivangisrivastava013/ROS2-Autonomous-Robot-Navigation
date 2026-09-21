import numpy as np
import pytest

from robot_nav.detector import ObjectDetector


def test_missing_model_raises_error():
    with pytest.raises(RuntimeError, match="could not be loaded"):
        ObjectDetector(model_name="non_existent_yolo.pt", mock_mode=False)


def test_mock_mode_schema():
    detector = ObjectDetector(mock_mode=True)
    frame = np.zeros((240, 320, 3), dtype=np.uint8)

    dets = detector.detect_objects(frame)
    assert len(dets) > 0
    assert dets[0]["source"] == "synthetic_mock"
    assert "class" in dets[0]
    assert "confidence" in dets[0]
    assert len(dets[0]["bbox"]) == 4
