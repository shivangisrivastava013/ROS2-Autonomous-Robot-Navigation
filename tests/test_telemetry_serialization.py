from robot_nav.telemetry_node import TelemetryNode


def test_telemetry_payload_schema():
    node = TelemetryNode()
    status = {
        "robot_x": 1.5,
        "robot_y": 0.5,
        "linear_x": 0.35,
        "angular_z": 0.0,
        "front_clearance": 2.5,
        "state": "FORWARD",
        "status": "WAYPOINT TRACKING (FORWARD)",
    }

    payload = node.record_telemetry(status)
    assert "timestamp" in payload
    assert payload["robot_x"] == 1.5
    assert payload["state"] == "FORWARD"
