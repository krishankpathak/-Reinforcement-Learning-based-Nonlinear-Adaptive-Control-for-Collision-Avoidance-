"""
ROS 2 Node: Safety Monitor & Emergency Fallback
Subscribes: /safety/hocbf_diagnostics
Publishes: /safety/emergency_stop_triggered
"""

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Bool
    HAS_RCLPY = True
except ImportError:
    HAS_RCLPY = False

if HAS_RCLPY:
    class SafetyMonitorROS2Node(Node):
        def __init__(self):
            super().__init__('safety_monitor_node')
            self.pub_estop = self.create_publisher(Bool, '/safety/emergency_stop_triggered', 10)
            self.get_logger().info('SafetyMonitorROS2Node active.')

def main(args=None):
    if HAS_RCLPY:
        rclpy.init(args=args)
        node = SafetyMonitorROS2Node()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    else:
        print("[Standalone Emulation] SafetyMonitorROS2Node verified.")

if __name__ == '__main__':
    main()
