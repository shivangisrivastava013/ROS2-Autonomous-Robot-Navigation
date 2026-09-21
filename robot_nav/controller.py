import logging
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VelocityCommand:
    """
    ROS2 geometry_msgs/Twist velocity command container.
    """

    linear_x: float
    angular_z: float
    status: str
    state_name: str
    robot_x: float = 0.0
    robot_y: float = 0.0


class ObstacleAvoidanceController:
    """
    Pure Python Obstacle Avoidance Controller implementing a multi-state machine
    with configurable safety thresholds and YOLO hazard detection integration.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or {}
        nav_cfg = cfg.get("navigation", {})

        self.stop_distance = float(nav_cfg.get("stop_distance", 0.45))
        self.slowdown_distance = float(nav_cfg.get("slowdown_distance", 1.0))
        self.forward_speed = float(nav_cfg.get("forward_speed", 0.35))
        self.turning_speed = float(nav_cfg.get("turning_speed", 0.7))
        self.recovery_timeout = float(nav_cfg.get("recovery_timeout_seconds", 4.0))

        perc_cfg = cfg.get("perception", {})
        self.safety_classes = set(perc_cfg.get("safety_classes", ["person", "car", "bicycle", "obstacle"]))
        self.confidence_threshold = float(perc_cfg.get("confidence_threshold", 0.60))

        self.state = "FORWARD"
        self.position = [0.0, 0.0]
        self.orientation_rad = 0.0
        self.stuck_counter = 0

    def compute_command(
        self,
        front_distance: float,
        left_distance: float,
        right_distance: float,
        detections: Optional[List[Dict[str, Any]]] = None,
        dt: float = 0.1,
    ) -> VelocityCommand:
        """
        Computes velocity command based on LiDAR clearances and vision detections.
        """
        # Clean inputs (handle NaN/inf values)
        front_dist = self._clean_distance(front_distance)
        left_dist = self._clean_distance(left_distance)
        right_dist = self._clean_distance(right_distance)

        # Check vision safety hazards
        hazard_detected = self._check_vision_hazards(detections)

        # State transition logic
        if hazard_detected or front_dist < (self.stop_distance * 0.7):
            self.state = "EMERGENCY_STOP"
        elif front_dist <= self.stop_distance:
            self.stuck_counter += 1
            if self.stuck_counter > (self.recovery_timeout / dt):
                self.state = "RECOVERY"
            else:
                self.state = "TURN_LEFT" if left_dist >= right_dist else "TURN_RIGHT"
        elif front_dist <= self.slowdown_distance:
            self.stuck_counter = 0
            self.state = "SLOW_DOWN"
        else:
            self.stuck_counter = 0
            self.state = "FORWARD"

        # Velocity output mapping
        if self.state == "EMERGENCY_STOP":
            linear_x = 0.0
            angular_z = 0.0
            status = "EMERGENCY STOP (HAZARD DETECTED)"
        elif self.state == "RECOVERY":
            linear_x = -0.15  # Back up slightly
            angular_z = self.turning_speed
            status = "RECOVERY MANEUVER (UNSTUCK)"
        elif self.state == "TURN_LEFT":
            linear_x = 0.05
            angular_z = self.turning_speed
            status = "OBSTACLE AVOIDANCE (TURNING LEFT)"
        elif self.state == "TURN_RIGHT":
            linear_x = 0.05
            angular_z = -self.turning_speed
            status = "OBSTACLE AVOIDANCE (TURNING RIGHT)"
        elif self.state == "SLOW_DOWN":
            linear_x = self.forward_speed * 0.5
            angular_z = 0.0
            status = "SLOW DOWN (OBSTACLE AHEAD)"
        else:  # FORWARD
            linear_x = self.forward_speed
            angular_z = 0.0
            status = "WAYPOINT TRACKING (FORWARD)"

        # Update pose simulation
        self.orientation_rad += angular_z * dt
        self.position[0] += linear_x * math.cos(self.orientation_rad) * dt
        self.position[1] += linear_x * math.sin(self.orientation_rad) * dt

        return VelocityCommand(
            linear_x=round(linear_x, 2),
            angular_z=round(angular_z, 2),
            status=status,
            state_name=self.state,
            robot_x=round(self.position[0], 2),
            robot_y=round(self.position[1], 2),
        )

    def _check_vision_hazards(self, detections: Optional[List[Dict[str, Any]]]) -> bool:
        if not detections:
            return False

        for det in detections:
            cls_name = det.get("class", det.get("class_name", ""))
            conf = float(det.get("confidence", 0.0))

            if cls_name in self.safety_classes and conf >= self.confidence_threshold:
                logger.warning(f"Vision safety hazard detected: '{cls_name}' (conf: {conf:.2f})")
                return True

        return False

    @staticmethod
    def _clean_distance(val: float) -> float:
        if val is None or math.isnan(val) or math.isinf(val) or val < 0.0:
            return 10.0  # Max clearance fallback
        return float(val)
