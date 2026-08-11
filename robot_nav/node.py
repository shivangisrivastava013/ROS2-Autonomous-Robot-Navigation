import time
import numpy as np
from typing import Dict
from .detector import ObjectDetector


class AutonomousNavSimulator:
    """
    ROS2 Autonomous Robot Navigation Simulator managing path planning, velocity controls,
    LiDAR range processing, and edge telemetry.
    """

    def __init__(self):
        self.detector = ObjectDetector()
        self.position = [0.0, 0.0]
        self.orientation_deg = 0.0
        self.linear_velocity = 0.5  # m/s
        self.angular_velocity = 0.0  # rad/s

    def process_lidar_scan(self, ranges: np.ndarray) -> Dict[str, float]:
        """
        Processes 360-degree LiDAR range array to check obstacle clearances.
        """
        min_front_dist = float(np.min(ranges[0:30]))
        min_left_dist = float(np.min(ranges[30:90]))
        min_right_dist = float(np.min(ranges[270:330]))

        return {
            "front_clearance": round(min_front_dist, 2),
            "left_clearance": round(min_left_dist, 2),
            "right_clearance": round(min_right_dist, 2),
            "obstacle_detected": min_front_dist < 1.0
        }

    def compute_navigation_command(self, lidar_info: Dict, detections: list) -> Dict[str, float]:
        """
        Calculates ROS2 geometry_msgs/Twist navigation control commands.
        """
        if lidar_info["obstacle_detected"]:
            # Obstacle avoidance maneuver: turn right
            cmd_linear = 0.0
            cmd_angular = -0.8
            status = "OBSTACLE AVOIDANCE (TURNING)"
        else:
            # Move forward towards waypoint
            cmd_linear = self.linear_velocity
            cmd_angular = 0.0
            status = "WAYPOINT TRACKING (FORWARD)"

        # Update position simulation
        self.position[0] += cmd_linear * 0.1
        self.position[1] += cmd_angular * 0.05

        return {
            "linear_x": round(cmd_linear, 2),
            "angular_z": round(cmd_angular, 2),
            "robot_x": round(self.position[0], 2),
            "robot_y": round(self.position[1], 2),
            "status": status
        }
