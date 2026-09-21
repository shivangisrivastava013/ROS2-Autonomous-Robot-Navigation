import json
import logging
import time
from typing import Any, Dict

logger = logging.getLogger(__name__)

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    HAS_RCLPY = True
except ImportError:
    HAS_RCLPY = False
    Node = object


class TelemetryNode(Node if HAS_RCLPY else object):
    """
    ROS2 Telemetry Node aggregating robot position, orientation, velocity,
    LiDAR clearance, vision detections, and navigation status for storage in PostgreSQL / Zenoh.
    """

    def __init__(self, node_name: str = "telemetry_node"):
        if HAS_RCLPY:
            super().__init__(node_name)

        self.latest_status = {}

        if HAS_RCLPY:
            self.status_sub = self.create_subscription(String, "/navigation_status", self.status_callback, 10)
            self.get_logger().info(f"ROS2 Telemetry Node '{node_name}' initialized.")

    def status_callback(self, msg) -> None:
        try:
            self.latest_status = json.loads(msg.data)
            self.record_telemetry(self.latest_status)
        except Exception as e:
            logger.error(f"Telemetry recording error: {e}")

    def record_telemetry(self, status: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "timestamp": time.time(),
            "robot_x": status.get("robot_x", 0.0),
            "robot_y": status.get("robot_y", 0.0),
            "linear_x": status.get("linear_x", 0.0),
            "angular_z": status.get("angular_z", 0.0),
            "front_clearance": status.get("front_clearance", 10.0),
            "state": status.get("state", "UNKNOWN"),
            "status": status.get("status", "IDLE"),
        }
        return payload


def main(args=None):
    if not HAS_RCLPY:
        logger.warning("rclpy not installed. Running TelemetryNode in standalone mode.")
        node = TelemetryNode()
        res = node.record_telemetry({"robot_x": 1.2, "status": "FORWARD"})
        print(f"[Standalone Telemetry Output]: {res}")
        return

    rclpy.init(args=args)
    node = TelemetryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
