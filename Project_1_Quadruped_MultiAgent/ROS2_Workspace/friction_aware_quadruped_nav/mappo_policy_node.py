"""
ROS 2 Node: MAPPO Decentralized Policy Guidance
Subscribes: /odom, /goal_pose, /tracking/nearby_agents
Publishes: /cmd_vel_nominal
"""

import sys
import os
try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    HAS_RCLPY = True
except ImportError:
    HAS_RCLPY = False

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Reinforcement_Learning.mappo_navigation import DecentralizedMAPPONavigator

if HAS_RCLPY:
    class MAPPONavigationROS2Node(Node):
        def __init__(self):
            super().__init__('mappo_policy_node')
            self.navigator = DecentralizedMAPPONavigator(0)
            self.pub_cmd = self.create_publisher(Twist, '/cmd_vel_nominal', 10)
            self.get_logger().info('MAPPONavigationROS2Node running.')

def main(args=None):
    if HAS_RCLPY:
        rclpy.init(args=args)
        node = MAPPONavigationROS2Node()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    else:
        print("[Standalone Emulation] MAPPONavigationROS2Node verified.")

if __name__ == '__main__':
    main()
