import numpy as np

from robot_nav.controller import ObstacleAvoidanceController
from robot_nav.navigation_node import NavigationNode


def test_nan_and_inf_lidar_handling():
    ranges = np.array([float("nan"), float("inf"), -1.0, 0.3, 2.5, 4.0])
    ctrl = ObstacleAvoidanceController()

    c_nan = ctrl._clean_distance(ranges[0])
    c_inf = ctrl._clean_distance(ranges[1])
    c_neg = ctrl._clean_distance(ranges[2])
    c_valid = ctrl._clean_distance(ranges[3])

    assert c_nan == 10.0
    assert c_inf == 10.0
    assert c_neg == 10.0
    assert c_valid == 0.3


def test_node_lidar_clearance_calculation():
    node = NavigationNode()
    ranges = np.full(360, 5.0)
    ranges[0:15] = 0.4  # Front obstacle at 0.4m

    front_c, left_c, right_c = node.process_lidar_clearance(ranges)
    assert front_c == 0.4
    assert left_c == 5.0
    assert right_c == 5.0
