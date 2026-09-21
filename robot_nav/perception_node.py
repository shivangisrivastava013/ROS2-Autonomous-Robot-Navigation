import json
import logging

import numpy as np

from .detector import ObjectDetector

logger = logging.getLogger(__name__)

try:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image
    from std_msgs.msg import String

    HAS_RCLPY = True
except ImportError:
    HAS_RCLPY = False
    Node = object


class PerceptionNode(Node if HAS_RCLPY else object):
    """
    ROS2 Perception Node processing camera image frames with YOLOv8.
    Subscribes to /camera/image_raw and publishes /detections.
    """

    def __init__(
        self,
        node_name: str = "perception_node",
        model_name: str = "yolov8n.pt",
        confidence_threshold: float = 0.5,
        mock_mode: bool = False,
    ):
        if HAS_RCLPY:
            super().__init__(node_name)

        self.detector = ObjectDetector(
            model_name=model_name,
            confidence_threshold=confidence_threshold,
            mock_mode=mock_mode,
        )

        if HAS_RCLPY:
            self.image_sub = self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)
            self.det_pub = self.create_publisher(String, "/detections", 10)
            self.get_logger().info(f"ROS2 Perception Node '{node_name}' initialized.")

    def image_callback(self, msg) -> None:
        """
        Processes ROS Image message and publishes detections JSON.
        """
        try:
            # Basic raw uint8 image unpacking
            h, w = msg.height, msg.width
            frame_np = np.frombuffer(msg.data, dtype=np.uint8).reshape((h, w, -1))
            if frame_np.shape[2] > 3:
                frame_np = frame_np[:, :, :3]

            detections = self.detector.detect_objects(frame_np)

            det_msg = String()
            det_msg.data = json.dumps(detections)
            self.det_pub.publish(det_msg)
        except Exception as e:
            logger.error(f"Perception node processing error: {e}")


def main(args=None):
    if not HAS_RCLPY:
        logger.warning("rclpy not installed. Running PerceptionNode in standalone mode.")
        detector = ObjectDetector(mock_mode=True)
        img = np.zeros((240, 320, 3), dtype=np.uint8)
        dets = detector.detect_objects(img)
        print(f"[Standalone Perception Output]: {dets}")
        return

    rclpy.init(args=args)
    node = PerceptionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
