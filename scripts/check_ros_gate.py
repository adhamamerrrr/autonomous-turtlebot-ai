"""Live ROS2 graph integration using synthetic messages, not Gazebo or model evidence."""
import json
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String
from autonomous_turtlebot_ai.supervisor import Supervisor

rclpy.init()
supervisor=Supervisor()
probe=Node('gate_probe')
scan_pub=probe.create_publisher(LaserScan,'/scan',10)
camera_pub=probe.create_publisher(Image,'/camera/image_raw',10)
# Supervisor defaults to Twist for standalone testing; launch enables TwistStamped for Nav2.
from geometry_msgs.msg import Twist
command_pub=probe.create_publisher(Twist,'/cmd_vel_nav',10)
alert_pub=probe.create_publisher(String,'/portfolio/alerts',10)
received=[]
probe.create_subscription(TwistStamped,'/cmd_vel',lambda m:received.append(m.twist.linear.x),10)
executor=SingleThreadedExecutor(); executor.add_node(probe); executor.add_node(supervisor)
def drive(distance,duration=.8):
    deadline=time.monotonic()+duration
    while time.monotonic()<deadline:
        scan=LaserScan(); scan.angle_min=-math.pi; scan.angle_increment=2*math.pi/360
        scan.range_min=.1; scan.range_max=3.5; scan.ranges=[distance]*360
        image=Image(); image.width=1; image.height=1; image.encoding='rgb8'; image.step=3; image.data=bytes([0,0,0])
        command=Twist(); command.linear.x=.1
        scan_pub.publish(scan); camera_pub.publish(image); command_pub.publish(command)
        executor.spin_once(timeout_sec=.05)
try:
    drive(2.,1.5)
    assert received and any(v>.05 for v in received[-5:]), 'No clear-path velocity'
    drive(.2)
    assert received[-1]==0., 'Obstacle did not stop'
    alert_pub.publish(String(data=json.dumps({'kind':'smoke','active':True})))
    drive(2.)
    assert supervisor.gate.hazard and received[-1]==0., 'Alert did not stop'
    print('ROS2 graph check passed: clear motion, obstacle stop, visual alert latch')
finally:
    executor.shutdown(); probe.destroy_node(); supervisor.destroy_node(); rclpy.shutdown()
