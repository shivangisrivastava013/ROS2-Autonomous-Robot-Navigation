import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    config_file = os.path.join(get_package_share_directory("robot_nav"), "config", "navigation.yaml")

    return LaunchDescription(
        [
            Node(
                package="robot_nav",
                executable="perception_node",
                name="perception_node",
                output="screen",
                parameters=[config_file],
            ),
            Node(
                package="robot_nav",
                executable="navigation_node",
                name="navigation_node",
                output="screen",
                parameters=[config_file],
            ),
            Node(
                package="robot_nav",
                executable="telemetry_node",
                name="telemetry_node",
                output="screen",
            ),
        ]
    )
