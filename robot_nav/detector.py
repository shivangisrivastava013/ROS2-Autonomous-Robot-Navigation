import logging
import time
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class ObjectDetector:
    """
    Real-time vision detector for obstacle detection and safety object classification
    using YOLOv8 (Ultralytics). Explicitly requires mock_mode=True for synthetic output.
    """

    def __init__(
        self,
        model_name: str = "yolov8n.pt",
        confidence_threshold: float = 0.5,
        mock_mode: bool = False,
    ):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.mock_mode = mock_mode
        self.model = None

        if not self.mock_mode:
            self._init_model()

    def _init_model(self) -> None:
        try:
            from ultralytics import YOLO

            logger.info(f"Loading YOLO model '{self.model_name}'...")
            self.model = YOLO(self.model_name)
            logger.info("YOLO model loaded successfully.")
        except Exception as e:
            raise RuntimeError(
                f"YOLO model '{self.model_name}' could not be loaded: {e}. "
                "Use mock_mode=True explicitly for simulated detections."
            ) from e

    def detect_objects(self, frame_np: np.ndarray) -> List[Dict[str, Any]]:
        """
        Processes camera image frame and extracts bounding boxes, confidence scores, and class names.
        """
        t0 = time.perf_counter()
        if self.mock_mode:
            return self._generate_mock_detections(frame_np)

        if self.model is None:
            raise RuntimeError("YOLO detector is uninitialized.")

        results = self.model(frame_np, verbose=False)[0]
        latency_ms = (time.perf_counter() - t0) * 1000.0

        detections: List[Dict[str, Any]] = []
        for box in results.boxes:
            conf = float(box.conf[0].cpu().item())
            if conf >= self.confidence_threshold:
                cls_id = int(box.cls[0].cpu().item())
                name = self.model.names[cls_id]
                xyxy = box.xyxy[0].cpu().numpy().tolist()
                detections.append(
                    {
                        "class": name,
                        "class_name": name,
                        "confidence": round(conf, 3),
                        "bbox": [round(c, 1) for c in xyxy],
                        "source": self.model_name,
                        "inference_ms": round(latency_ms, 2),
                    }
                )
        return detections

    def _generate_mock_detections(self, frame_np: np.ndarray) -> List[Dict[str, Any]]:
        h, w = frame_np.shape[:2] if frame_np is not None and frame_np.ndim >= 2 else (240, 320)
        return [
            {
                "class": "obstacle",
                "class_name": "obstacle",
                "confidence": 0.94,
                "bbox": [100.0, 80.0, 180.0, 200.0],
                "source": "synthetic_mock",
                "inference_ms": 12.5,
            },
            {
                "class": "target_waypoint",
                "class_name": "target_waypoint",
                "confidence": 0.88,
                "bbox": [20.0, 30.0, 70.0, 90.0],
                "source": "synthetic_mock",
                "inference_ms": 12.5,
            },
        ]
