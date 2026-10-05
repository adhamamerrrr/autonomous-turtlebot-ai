import math
from autonomous_turtlebot_ai.safety import Gate, Observation, clearance

def ready():
    g=Gate(); g.scan=Observation(1.,2.,2.,True); g.camera_stamp=1.; g.command=(.3,2.,1.)
    return g

def test_missing_sensors_stop():
    assert Gate().decide(1.)[:2] == (0.,0.)

def test_bounded_clear_command():
    assert ready().decide(1.1) == (.15,.7,'clear')

def test_stale_and_future_sensor_stop():
    assert ready().decide(2.)[2] == 'stale_sensor'
    assert ready().decide(.9)[2] == 'stale_sensor'

def test_stale_command_stop():
    g=ready(); g.command=(.1,0.,.2)
    assert g.decide(1.1)[2] == 'stale_or_invalid_command'

def test_front_and_reverse_obstacle_stop():
    g=ready(); g.scan.front=.3
    assert g.decide(1.1)[2] == 'obstacle'
    g=ready(); g.scan.rear=.3; g.command=(-.1,0.,1.)
    assert g.decide(1.1)[2] == 'obstacle'

def test_alert_latch_stop():
    g=ready(); g.hazard=True
    assert g.decide(1.1)[2] == 'visual_alert_latched'

def test_nan_scan_invalid_and_infinity_clear():
    ranges=[float('inf')]*360
    good=clearance(ranges,-math.pi,2*math.pi/360,.1,3.5,1.)
    assert good.complete and good.front==3.5
    ranges[180]=float('nan')
    assert not clearance(ranges,-math.pi,2*math.pi/360,.1,3.5,1.).complete

def test_partial_scan_and_invalid_speed():
    assert not clearance([1.],0.,.1,.1,3.5,1.).complete
    g=ready(); g.command=(float('nan'),0.,1.)
    assert g.decide(1.1)[2] == 'stale_or_invalid_command'
