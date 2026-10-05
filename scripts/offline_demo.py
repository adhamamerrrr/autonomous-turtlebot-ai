"""Synthetic control trace: no ROS, hardware, camera model or physical claims."""
import json
from autonomous_turtlebot_ai.safety import Gate, Observation

gate=Gate()
trace=[]
def record(name,t):
    v,w,state=gate.decide(t)
    trace.append({'scenario':name,'linear':v,'angular':w,'state':state})
record('no sensor data',0.)
gate.scan=Observation(1.,2.,2.,True); gate.camera_stamp=1.; gate.command=(.1,.2,1.)
record('fresh clear path',1.1)
gate.scan.front=.2
record('near obstacle',1.1)
gate.scan.front=2.; gate.hazard=True
record('injected visual alert',1.1)
gate.hazard=False
record('stale camera and scan',2.)
assert [x['state'] for x in trace]==['invalid_scan','clear','obstacle','visual_alert_latched','stale_sensor']
print(json.dumps({'data':'synthetic software control inputs','trace':trace},indent=2))
