"""Run the newly trained checkpoint on a supplied local RGB image."""
import argparse
import json
import cv2
from autonomous_turtlebot_ai.vision import Predictor
p=argparse.ArgumentParser()
p.add_argument('image')
p.add_argument('--model',default='checkpoints/smoke.pt')
a=p.parse_args()
image=cv2.imread(a.image)
if image is None: p.error('Cannot decode image')
score=Predictor(a.model,'smoke').score([cv2.cvtColor(image,cv2.COLOR_BGR2RGB)])
print(json.dumps({'smoke_probability':score,'threshold':.5,'event_prediction':score>=.5,
                  'warning':'Small public-data baseline; not a reliable safety detector.'},indent=2))
