from robot_nav.controller import ObstacleAvoidanceController


def test_controller_forward_state():
    ctrl = ObstacleAvoidanceController()
    cmd = ctrl.compute_command(front_distance=3.0, left_distance=3.0, right_distance=3.0)

    assert cmd.state_name == "FORWARD"
    assert cmd.linear_x > 0.0
    assert cmd.angular_z == 0.0


def test_controller_slowdown_state():
    ctrl = ObstacleAvoidanceController()
    cmd = ctrl.compute_command(front_distance=0.8, left_distance=2.0, right_distance=2.0)

    assert cmd.state_name == "SLOW_DOWN"
    assert cmd.linear_x < ctrl.forward_speed


def test_controller_turn_left_choice():
    ctrl = ObstacleAvoidanceController()
    # Front blocked (0.40m <= stop_distance 0.45m), left clear (3.0m), right restricted (0.5m) -> turn left
    cmd = ctrl.compute_command(front_distance=0.40, left_distance=3.0, right_distance=0.5)

    assert cmd.state_name == "TURN_LEFT"
    assert cmd.angular_z > 0.0


def test_controller_turn_right_choice():
    ctrl = ObstacleAvoidanceController()
    # Front blocked (0.40m <= stop_distance 0.45m), left restricted (0.5m), right clear (3.0m) -> turn right
    cmd = ctrl.compute_command(front_distance=0.40, left_distance=0.5, right_distance=3.0)

    assert cmd.state_name == "TURN_RIGHT"
    assert cmd.angular_z < 0.0


def test_controller_emergency_stop_on_vision_hazard():
    ctrl = ObstacleAvoidanceController()
    hazard_dets = [{"class": "person", "confidence": 0.92}]
    cmd = ctrl.compute_command(front_distance=3.0, left_distance=3.0, right_distance=3.0, detections=hazard_dets)

    assert cmd.state_name == "EMERGENCY_STOP"
    assert cmd.linear_x == 0.0
    assert cmd.angular_z == 0.0
