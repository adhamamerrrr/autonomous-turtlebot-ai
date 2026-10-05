"""Camera event classification and JSON alerts, with explicit missing-model status."""
from collections import deque
import json
import time
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import String
from .vision import Predictor, image_rgb

class Detector(Node):
    def __init__(self):
        super().__init__('portfolio_detector')
        self.declare_parameter('smoke_model', '')
        self.declare_parameter('violence_model', '')
        self.declare_parameter('alert_threshold', .5)
        self.threshold = float(self.get_parameter('alert_threshold').value)
        if not math.isfinite(self.threshold) or not 0 <= self.threshold <= 1:
            raise ValueError('Alert threshold must be finite and between 0 and 1')
        self.models = {}
        for task in ('smoke', 'violence'):
            path = self.get_parameter(task+'_model').value
            if path:
                self.models[task] = Predictor(path,task)
            else:
                self.get_logger().warning(f'{task} model absent: detection disabled, not a negative prediction')
        self.frames = deque(maxlen=8)
        self.votes = {task: deque(maxlen=3) for task in self.models}
        self.last_frame = float('-inf')
        self.publisher = self.create_publisher(String,'/portfolio/alerts',10)
        self.create_subscription(Image,'/camera/image_raw',self.image,qos_profile_sensor_data)
        self.create_timer(5., self.health)

    def health(self):
        self.publisher.publish(String(data=json.dumps({'kind':'detector_status','active':False,
            'enabled':list(self.models),'camera_age_seconds':time.monotonic()-self.last_frame})))

    def image(self, msg):
        now = time.monotonic()
        if now-self.last_frame < .2:
            return
        if now-self.last_frame > 1.:
            self.frames.clear()
            for votes in self.votes.values():
                votes.clear()
        try:
            frame = image_rgb(msg.data, msg.width, msg.height, msg.step, msg.encoding)
        except Exception as exc:
            self.get_logger().error(f'Image conversion failed: {exc}')
            return
        self.last_frame = now
        self.frames.append(frame)
        for task,predictor in self.models.items():
            if len(self.frames) < predictor.frames:
                continue
            started = time.monotonic()
            score = predictor.score(list(self.frames)[-predictor.frames:])
            self.votes[task].append(score >= self.threshold)
            active = len(self.votes[task]) == 3 and all(self.votes[task])
            self.publisher.publish(String(data=json.dumps({'kind':task,'active':active,'score':score,
                'threshold':self.threshold,'consecutive_predictions':3,'inference_seconds':time.monotonic()-started,
                'stamp_sec':msg.header.stamp.sec,'stamp_nanosec':msg.header.stamp.nanosec})))

def main():
    rclpy.init()
    node = Detector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
