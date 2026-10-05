"""Decision-level fusion of laser clearance and camera hazard state.

This is a software demonstration, not a certified collision/safety controller.
"""
from dataclasses import dataclass
import math

@dataclass
class Observation:
    stamp: float
    front: float
    rear: float
    complete: bool


def clearance(ranges, angle_min, angle_increment, range_min, range_max, stamp):
    """Use 60-degree sectors; +inf denotes valid no-return, NaN/zero invalid."""
    sectors = {'front': [], 'rear': []}
    invalid = {'front': False, 'rear': False}
    if (not ranges or not all(math.isfinite(x) for x in (angle_min, angle_increment, range_min, range_max, stamp))
            or angle_increment == 0 or range_max <= range_min):
        return Observation(stamp, 0., 0., False)
    for i, distance in enumerate(ranges):
        angle = math.atan2(math.sin(angle_min+i*angle_increment), math.cos(angle_min+i*angle_increment))
        sector = 'front' if abs(angle) <= math.pi/6 else 'rear' if abs(angle) >= 5*math.pi/6 else None
        if sector:
            if distance == float('inf'):
                sectors[sector].append(range_max)
            elif not math.isfinite(distance) or not range_min <= distance <= range_max:
                invalid[sector] = True
            else:
                sectors[sector].append(distance)
    complete = all(sectors[s] and not invalid[s] for s in sectors)
    return Observation(stamp, min(sectors['front'], default=0.), min(sectors['rear'], default=0.), complete)


class Gate:
    """Explicit stale-input stops, bounded speeds and latched visual alerts."""
    def __init__(self, stop_distance=.4, sensor_timeout=.7, command_timeout=.3):
        self.stop_distance = stop_distance
        self.sensor_timeout = sensor_timeout
        self.command_timeout = command_timeout
        self.scan = None
        self.camera_stamp = None
        self.hazard = False
        self.command = (0., 0., float('-inf'))

    def decide(self, now):
        if self.hazard:
            return 0., 0., 'visual_alert_latched'
        if self.scan is None or not self.scan.complete:
            return 0., 0., 'invalid_scan'
        ages = [now-self.scan.stamp, now-self.camera_stamp if self.camera_stamp is not None else float('inf')]
        if any(not 0 <= age <= self.sensor_timeout for age in ages):
            return 0., 0., 'stale_sensor'
        v,w,stamp = self.command
        if not 0 <= now-stamp <= self.command_timeout or not all(math.isfinite(x) for x in (v,w)):
            return 0., 0., 'stale_or_invalid_command'
        distance = self.scan.front if v >= 0 else self.scan.rear
        # Stop rotation too when either sector is close. This does not cover the full footprint.
        if distance < self.stop_distance or min(self.scan.front, self.scan.rear) < .25:
            return 0., 0., 'obstacle'
        return max(-.15,min(.15,v)), max(-.7,min(.7,w)), 'clear'
