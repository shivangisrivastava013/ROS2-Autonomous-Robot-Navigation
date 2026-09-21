from robot_nav.navigation_node import NavigationNode


def test_navigation_node_standalone_control_loop():
    node = NavigationNode()
    status = node.control_loop()

    assert "linear_x" in status
    assert "angular_z" in status
    assert "status" in status
    assert "front_clearance" in status
