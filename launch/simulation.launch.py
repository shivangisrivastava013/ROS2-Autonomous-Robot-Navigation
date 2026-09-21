import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    pkg_share = get_package_share_directory("robot_nav")
    rviz_file = os.path.join(pkg_share, "rviz", "navigation.rviz")

    nav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, "launch", "navigation.launch.py"))
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_file],
        output="screen",
    )

    return LaunchDescription([nav_launch, rviz_node])
