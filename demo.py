import time
import numpy as np
from robot_nav.node import AutonomousNavSimulator


def main():
    print("[+] Initializing ROS2 Autonomous Navigation & YOLO Simulation Loop...")
    sim = AutonomousNavSimulator()

    print("[*] Starting 10-step Waypoint Navigation Loop:\n")
    print(f"{'Step':<6} | {'Front Dist (m)':<16} | {'Cmd Linear (x)':<16} | {'Cmd Angular (z)':<16} | {'Navigation Status'}")
    print("-" * 85)

    for step in range(1, 11):
        # Simulate LiDAR ranges (obstacle appears at step 5)
        ranges = np.ones(360) * 3.5
        if step in [5, 6]:
            ranges[0:30] = 0.6  # Obstacle ahead

        lidar_info = sim.process_lidar_scan(ranges)
        detections = sim.detector.detect_objects(np.zeros((200, 200, 3), dtype=np.uint8))
        cmd = sim.compute_navigation_command(lidar_info, detections)

        print(f"{step:<6} | {lidar_info['front_clearance']:<16.2f} | {cmd['linear_x']:<16.2f} | {cmd['angular_z']:<16.2f} | {cmd['status']}")
        time.sleep(0.1)

    print("\n[+] ROS2 Simulation Completed Successfully!")
    print(f"[*] Final Robot Position: X={cmd['robot_x']} m, Y={cmd['robot_y']} m")


if __name__ == '__main__':
    main()
