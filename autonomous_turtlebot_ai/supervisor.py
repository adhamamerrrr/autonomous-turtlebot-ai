"""ROS2 velocity gate; Nav2 input is separated from the robot output."""
import json
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String
from std_srvs.srv import Trigger
from .safety import Gate, clearance

class Supervisor(Node):
    def __init__(self):
        super().__init__('portfolio_supervisor')
        self.declare_parameter('stamped_input', False)
        self.gate = Gate()
        self.output = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.status = self.create_publisher(String, '/portfolio/status', 10)
        input_type = TwistStamped if self.get_parameter('stamped_input').value else Twist
        self.create_subscription(input_type, '/cmd_vel_nav', self.command, 10)
        self.create_subscription(LaserScan, '/scan', self.scan, qos_profile_sensor_data)
        self.create_subscription(Image, '/camera/image_raw', self.camera, qos_profile_sensor_data)
        self.create_subscription(String, '/portfolio/alerts', self.alert, 10)
        self.create_service(Trigger, '/portfolio/reset_alert', self.reset)
        self.last_reason = None
        self.create_timer(.05, self.tick)

    def command(self, msg):
        twist = msg.twist if isinstance(msg, TwistStamped) else msg
        self.gate.command = (twist.linear.x, twist.angular.z, time.monotonic())

    def scan(self, msg):
        self.gate.scan = clearance(msg.ranges, msg.angle_min, msg.angle_increment,
                                   msg.range_min, msg.range_max, time.monotonic())

    def camera(self, msg):
        if msg.width > 0 and msg.height > 0 and msg.data:
            self.gate.camera_stamp = time.monotonic()

    def alert(self, msg):
        try:
            event = json.loads(msg.data)
            if event.get('active') is True and event.get('kind') in {'smoke', 'violence'}:
                self.gate.hazard = True
        except (ValueError, TypeError):
            self.get_logger().warning('Ignoring malformed alert')

    def reset(self, request, response):
        self.gate.hazard = False
        response.success = True
        response.message = 'Latch reset; current alerts can relatch it.'
        return response

    def tick(self):
        v,w,reason = self.gate.decide(time.monotonic())
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x, msg.twist.angular.z = v,w
        self.output.publish(msg)
        if reason != self.last_reason:
            self.status.publish(String(data=json.dumps({'state':reason,'linear':v,'angular':w})))
            self.last_reason = reason

def main():
    rclpy.init()
    node = Supervisor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.output.publish(TwistStamped())
        node.destroy_node()
        rclpy.shutdown()
