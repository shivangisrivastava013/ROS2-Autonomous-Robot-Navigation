import json
import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np

from .controller import ObstacleAvoidanceController

logger = logging.getLogger(__name__)

# Optional rclpy imports for ROS2 runtime
try:
    import rclpy
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from rclpy.node import Node
    from sensor_msgs.msg import LaserScan
    from std_msgs.msg import String

    HAS_RCLPY = True
except ImportError:
    HAS_RCLPY = False
    Node = object  # Dummy base class for standalone execution


class NavigationNode(Node if HAS_RCLPY else object):
    """
    ROS2 Autonomous Robot Navigation Node.
    Subscribes to /scan, /odom, and /detections topics and publishes /cmd_vel and /navigation_status.
    """

    def __init__(self, node_name: str = "navigation_node", config: Optional[Dict[str, Any]] = None):
        if HAS_RCLPY:
            super().__init__(node_name)

        self.controller = ObstacleAvoidanceController(config=config)
        self.latest_scan = None
        self.latest_odom = None
        self.latest_detections = []

        if HAS_RCLPY:
            self.scan_sub = self.create_subscription(LaserScan, "/scan", self.scan_callback, 10)
            self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
            self.det_sub = self.create_subscription(String, "/detections", self.detections_callback, 10)

            self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
            self.status_pub = self.create_publisher(String, "/navigation_status", 10)

            self.timer = self.create_timer(0.1, self.control_loop)
            self.get_logger().info(f"ROS2 Navigation Node '{node_name}' initialized.")

    def scan_callback(self, msg) -> None:
        self.latest_scan = msg.ranges

    def odom_callback(self, msg) -> None:
        self.latest_odom = msg

    def detections_callback(self, msg) -> None:
        try:
            self.latest_detections = json.loads(msg.data)
        except Exception as e:
            logger.error(f"Failed to parse detections JSON: {e}")

    def process_lidar_clearance(self, ranges: np.ndarray) -> Tuple[float, float, float]:
        """
        Extracts front, left, and right clearances from 360-degree LiDAR range array.
        """
        if ranges is None or len(ranges) == 0:
            return 10.0, 10.0, 10.0

        n = len(ranges)
        # Front: 0..n/12 and 11n/12..n
        f_idx1 = ranges[: max(1, n // 12)]
        f_idx2 = ranges[max(0, 11 * n // 12) :]
        front_arr = np.concatenate([f_idx1, f_idx2]) if len(f_idx1) > 0 and len(f_idx2) > 0 else ranges

        # Left: n/12 .. 5n/12
        left_arr = ranges[n // 12 : 5 * n // 12]
        # Right: 7n/12 .. 11n/12
        right_arr = ranges[7 * n // 12 : 11 * n // 12]

        front_c = float(np.min(front_arr)) if len(front_arr) > 0 else 10.0
        left_c = float(np.min(left_arr)) if len(left_arr) > 0 else 10.0
        right_c = float(np.min(right_arr)) if len(right_arr) > 0 else 10.0

        return front_c, left_c, right_c

    def control_loop(self) -> Dict[str, Any]:
        """
        Executes single iteration of navigation control loop.
        """
        ranges = np.array(self.latest_scan) if self.latest_scan is not None else np.full(360, 5.0)
        front_c, left_c, right_c = self.process_lidar_clearance(ranges)

        cmd = self.controller.compute_command(
            front_distance=front_c,
            left_distance=left_c,
            right_distance=right_c,
            detections=self.latest_detections,
            dt=0.1,
        )

        status_payload = {
            "linear_x": cmd.linear_x,
            "angular_z": cmd.angular_z,
            "robot_x": cmd.robot_x,
            "robot_y": cmd.robot_y,
            "status": cmd.status,
            "state": cmd.state_name,
            "front_clearance": round(front_c, 2),
            "left_clearance": round(left_c, 2),
            "right_clearance": round(right_c, 2),
        }

        if HAS_RCLPY and hasattr(self, "cmd_pub"):
            twist_msg = Twist()
            twist_msg.linear.x = float(cmd.linear_x)
            twist_msg.angular.z = float(cmd.angular_z)
            self.cmd_pub.publish(twist_msg)

            status_msg = String()
            status_msg.data = json.dumps(status_payload)
            self.status_pub.publish(status_msg)

        return status_payload


def main(args=None):
    if not HAS_RCLPY:
        logger.warning("rclpy not installed. Running NavigationNode in standalone simulation mode.")
        node = NavigationNode()
        res = node.control_loop()
        print(f"[Standalone Nav Output]: {res}")
        return

    rclpy.init(args=args)
    node = NavigationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
