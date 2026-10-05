"""Real smoke-model ROS2 alert path, replaying a public validation image.

Use a separate ROS_DOMAIN_ID from Gazebo. This is image replay, not simulated
smoke physics and not a benchmark of violence or real-time system latency.
"""
import csv
import json
from pathlib import Path
import time
import cv2
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from sensor_msgs.msg import Image
from std_msgs.msg import String
from autonomous_turtlebot_ai.vision import Predictor
from autonomous_turtlebot_ai.detector import Detector
p=Predictor('checkpoints/smoke.pt','smoke')
rows=list(csv.DictReader(open('data/dfire-small/manifest.csv')))
chosen=None
for row in rows:
    if row['split']=='val' and row['label']=='1':
        rgb=cv2.cvtColor(cv2.imread('data/dfire-small/'+row['path']),cv2.COLOR_BGR2RGB)
        score=p.score([rgb])
        if score>=.5:
            chosen=(row,rgb,score); break
assert chosen is not None, 'No smoke-positive validation image clears the fixed threshold'
row,rgb,score=chosen
rclpy.init(args=['--ros-args','-p','smoke_model:=checkpoints/smoke.pt'])
detector=Detector(); probe=Node('model_alert_probe')
pub=probe.create_publisher(Image,'/camera/image_raw',10); alerts=[]
probe.create_subscription(String,'/portfolio/alerts',lambda m:alerts.append(json.loads(m.data)),10)
executor=SingleThreadedExecutor();executor.add_node(detector);executor.add_node(probe)
try:
    deadline=time.monotonic()+8
    last_publish=0.
    while time.monotonic()<deadline and not any(a.get('active') and a.get('kind')=='smoke' for a in alerts):
        if time.monotonic()-last_publish>.25:
            image=Image();image.height,image.width=rgb.shape[:2];image.encoding='rgb8'
            image.step=image.width*3;image.data=rgb.tobytes();image.header.stamp=probe.get_clock().now().to_msg()
            pub.publish(image);last_publish=time.monotonic()
        executor.spin_once(timeout_sec=.05)
    active=[a for a in alerts if a.get('active') and a.get('kind')=='smoke']
    assert active, 'Trained smoke checkpoint failed to emit an alert through ROS2'
    result={'source':'D-Fire validation-image replay over live ROS2','image':row['path'],
            'selection':'first validation smoke image whose fixed-threshold prediction is positive; not random evaluation',
            'score':score,'active_alert':active[-1],
            'limitations':'Same image replayed; does not establish surveillance reliability or Gazebo smoke simulation.'}
    Path('results/model_alert_check.json').write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))
finally:
    executor.shutdown();probe.destroy_node();detector.destroy_node();rclpy.shutdown()
