#!/usr/bin/env python3
import sys
sys.path = ['/home/yuki/dot/scripts', '/home/yuki/dot/pylib', '/home/yuki/dot/scripts', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/home/yuki/.local/lib/python3.8/site-packages', '/home/yuki/choubun', '/usr/lib/python3.8/site-packages']
from dataenum import dataenum, dataclass
import struct
import os

__all__ = ["Event", "Button", "Axis"]

@dataclass
class Event:
	time: int
	which: "Button | Axis"
	value: "bool | complex"

@dataenum
class Button:
	Y: 0
	B: 1
	A: 2
	X: 3
	L: 4
	R: 5
	ZL: 6
	ZR: 7
	SELECT: 8
	START: 9
	LHAT: 10
	RHAT: 11

@dataenum
class Axis:
	L: 0
	R: 1
	DPAD: 2

eventstruct = struct.Struct("<IhBB")
class events:
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.f = open(self.path, "rb").__enter__()
		self.fd = self.f.fileno()
		self.axes = {}
		list(self.parse(os.read(self.fd, 4096), True))
		return self

	def __exit__(self, *a):
		return self.f.__exit__(*a)

	def __iter__(self):
		while e := os.read(self.fd, 1024):
			yield from self.parse(e)

	def parse(self, e, init=False):
		evts = list(eventstruct.iter_unpack(e))[::-1]
		while evts:
			time, value, type, which = evts.pop()
			assert init == bool(type & 0x80)

			if type & 0x7F == 1:
				assert value in [0, 1]
				yield Event(time, Button[which], bool(value))
			elif type & 0x7F == 2:
				axis = Axis[which>>1]
				if which & 1:
					pos = complex(self.axes[axis].real, value / 0x7FFF)
				elif evts and evts[-1][0] == time and evts[-1][2] == type and evts[-1][3] == (which|1):
					pos = complex(value / 0x7FFF, evts.pop()[1] / 0x7FFF)
				else:
					pos = complex(value / 0x7FFF, self.axes[axis].imag)
				self.axes[axis] = pos
				yield Event(time, axis, pos)
			else:
				assert False, type&0x7F

import cmath
import math

@dataenum
class Zone:
	angle: float

	NEUTRAL: 0 = None
	LEFT:    1 = -math.pi
	UP:      2 = -math.pi/2
	RIGHT:   3 = 0
	DOWN:    4 = math.pi/2

class Zoner:
	def __init__(self, pos):
		self.zone = Zone.NEUTRAL
		self.zone = self.detect(pos)

	def deadzone(self, zone):
		v = 0.5
		if zone == Zone.NEUTRAL: v -= 0.2
		if zone == self.zone: v += 0.1
		return v

	def detect(self, pos):
		if abs(pos) < self.deadzone(Zone.NEUTRAL):
			return Zone.NEUTRAL

		angle = cmath.phase(pos)

		for z in Zone:
			if z.angle is None:
				continue
			rangle = (z.angle - angle) / math.pi * 2
			while rangle < -2: rangle += 4
			while rangle >  2: rangle -= 4

			if abs(rangle) < self.deadzone(z):
				return z
		assert False

	def update(self, pos):
		v = self.detect(pos)
		if v != self.zone:
			self.zone = v
			return v

import evdev
from evdev import UInput
from evdev import ecodes as ec
caps = {
	ec.EV_REL: ( ec.REL_X, ec.REL_Y,)
}
import pprint

with events("/dev/input/js0") as es, UInput(caps) as ui:
	print(ui)
	pprint.pprint(ui.capabilities(verbose=True))
	left = Zoner(es.axes[Axis.L])
	right = Zoner(es.axes[Axis.R])
	for e in es:
		if e.which == Axis.L and (v := left.update(e.value)):
			print("left", v)
		if e.which == Axis.R and (v := right.update(e.value)):
			print("right", v)


		ui.write(ec.EV_KEY, ec.BTN_X, 1)
		ui.write(ec.EV_KEY, ec.BTN_X, 0)
		ui.syn()
		# print(e)
		# if e.type == ecodes.EV_ABS:
		# 	if 0: pass
		# 	elif e.code == ecodes.ABS_X: x = e.value
		# 	elif e.code == ecodes.ABS_Y: y = e.value
		# 	elif e.code == ecodes.ABS_RX: rx = e.value
		# 	elif e.code == ecodes.ABS_RY: ry = e.value
		# 	print(e.code, e.value)
		# if e.type == ecodes.EV_SYN and e.code == ecodes.SYN_REPORT:
		# 	pass
		# 	thumbs(complex(x, y), complex(rx, ry))
