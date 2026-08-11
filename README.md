# Autonomous Robot Navigation & Real-Time YOLO Object Detection System

[![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge)](https://github.com/ultralytics/ultralytics)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

An end-to-end autonomous robot navigation system combining **ROS2 middleware**, **Gazebo physics simulation**, **YOLOv8 real-time object detection** for obstacle avoidance, and **Zenoh low-latency distributed telemetry**.

---

## 🌟 Key Capabilities
- 🤖 **ROS2 Control Architecture:** Autonomous waypoint path planning and `/cmd_vel` velocity command generation.
- 👁️ **Edge Computer Vision:** YOLOv8 integration for real-time target recognition and dynamic obstacle avoidance.
- 📡 **Distributed Telemetry:** Zenoh low-latency publish-subscribe bus for edge robot state tracking & PostgreSQL database logging.
- 🐳 **Docker Containerization:** Fully reproducible ROS2 Humble simulation environment.

---

## 📁 Repository Structure
```text
ROS2-Autonomous-Robot-Navigation/
├── robot_nav/              # Core ROS2 & Computer Vision Package
│   ├── __init__.py
│   ├── node.py             # Autonomous Navigation Simulator
│   └── detector.py         # YOLOv8 Vision & Obstacle Detector
├── launch/                 # Gazebo & RViz Launch Files
├── demo.py                 # 1-Command Navigation Simulation Loop
├── Dockerfile              # Container Build Spec
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚡ Quick Start
```bash
git clone https://github.com/shivangisrivastava013/ROS2-Autonomous-Robot-Navigation.git
cd ROS2-Autonomous-Robot-Navigation

pip install -r requirements.txt
python demo.py
```

---

## 👤 Author
**Shivangi Srivastava**  
MS in Artificial Intelligence @ NJIT  
[LinkedIn Profile](https://www.linkedin.com/in/shivangisrivastava013/) | [Portfolio](https://shivangisrivastava013.github.io/shivangi-portfolio/)
