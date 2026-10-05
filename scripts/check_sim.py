"""Observe a running Gazebo+SLAM+Nav2 launch and execute one short goal.

Run this in a second terminal. It writes actual observations, never a fabricated
success report. A failed assertion means that integration is not validated.
"""
import json
import math
from pathlib import Path
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import qos_profile_sensor_data, QoSProfile, DurabilityPolicy
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav2_msgs.action import NavigateToPose
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time

rclpy.init(); node=Node('simulation_probe')
state={'scans':0,'images':0,'odom':0,'map':None,'last_scan':None,'last_velocity':None}
def scan(msg): state.update(scans=state['scans']+1,last_scan=msg)
def image(msg): state['images']+=1
def odom(msg): state['odom']+=1
def grid(msg): state['map']=msg
node.create_subscription(LaserScan,'/scan',scan,qos_profile_sensor_data)
node.create_subscription(Image,'/camera/image_raw',image,qos_profile_sensor_data)
node.create_subscription(Odometry,'/odom',odom,10)
node.create_subscription(OccupancyGrid,'/map',grid,QoSProfile(depth=1,durability=DurabilityPolicy.TRANSIENT_LOCAL))
node.create_subscription(TwistStamped,'/cmd_vel',lambda m:state.update(last_velocity=m.twist.linear.x),10)
client=ActionClient(node,NavigateToPose,'/navigate_to_pose')
buffer=Buffer(); listener=TransformListener(buffer,node)
def until(condition,seconds):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline and not condition(): rclpy.spin_once(node,timeout_sec=.1)
    assert condition(), 'Timed out waiting for simulation condition'
try:
    until(lambda:state['scans']>=5 and state['images']>=5 and state['map'] is not None,90)
    until(lambda:buffer.can_transform('map','base_footprint',Time()),30)
    assert client.wait_for_server(timeout_sec=30.), 'Navigation action server unavailable'
    transform=buffer.lookup_transform('map','base_footprint',Time()).transform
    q=transform.rotation
    yaw=math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z))
    goal=NavigateToPose.Goal(); goal.pose=PoseStamped()
    goal.pose.header.frame_id='map'; goal.pose.header.stamp=node.get_clock().now().to_msg()
    goal.pose.pose.position.x=transform.translation.x+.5*math.cos(yaw)
    goal.pose.pose.position.y=transform.translation.y+.5*math.sin(yaw)
    goal.pose.pose.orientation=transform.rotation
    pending=client.send_goal_async(goal); until(pending.done,20)
    handle=pending.result(); assert handle.accepted, 'Goal rejected'
    outcome=handle.get_result_async(); until(outcome.done,120)
    status=outcome.result().status
    assert status==4, f'Nav2 goal did not succeed, status={status}'
    publishers=node.get_publishers_info_by_topic('/cmd_vel')
    assert publishers and all(p.node_name=='portfolio_supervisor' for p in publishers), 'Velocity bypass detected'
    grid=state['map']
    result={'source':'Actual ROS2 Jazzy + Gazebo Harmonic + TurtleBot3 Waffle Pi',
        'scans_received':state['scans'],'camera_images_received':state['images'],'odom_received':state['odom'],
        'map_width':grid.info.width,'map_height':grid.info.height,'map_resolution':grid.info.resolution,
        'known_map_cells':sum(x>=0 for x in grid.data),'navigation_goal_status':status,
        'goal':{'x':goal.pose.pose.position.x,'y':goal.pose.pose.position.y},
        'robot_velocity_publishers':[p.node_name for p in publishers],
        'limitations':'One short goal in one simulated world; no hardware or public violence-model validation.'}
    Path('results').mkdir(exist_ok=True); Path('results/gazebo_check.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
finally:
    node.destroy_node(); rclpy.shutdown()
