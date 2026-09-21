import os
from glob import glob

from setuptools import find_packages, setup

package_name = "robot_nav"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.world")),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Shivangi Srivastava",
    maintainer_email="shivangisrivastava013@gmail.com",
    description="ROS2 Autonomous Robot Navigation with YOLOv8 Vision Perception",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "navigation_node = robot_nav.navigation_node:main",
            "perception_node = robot_nav.perception_node:main",
            "telemetry_node = robot_nav.telemetry_node:main",
        ],
    },
)
