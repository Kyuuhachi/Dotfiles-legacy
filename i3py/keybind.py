#!/usr/bin/env python3

import i3ipc
import subprocess
import os
import sys
import itertools
from i3py import i3 as _i3
from i3py import display
import i3py.util

from Xlib import X, XK
_root = display.screen().root

class i3:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "i3(%s)" % repr(self.cmd)
	def __call__(self): _i3.command(self.cmd)
class run:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "run(%s)" % repr(self.cmd)
	def __call__(self): subprocess.Popen(self.cmd, shell=True)
class mode:
	def __init__(self, id): self.id = id
	def __repr__(self): return "mode(%s)" % repr(self.id)
	def __call__(self):
		if self.id:
			i3("mode '%s'" % keys[self.id]["<name>"])()
			_grab_keys(None, self.id)
		else:
			i3("mode default")()
			_grab_keys(None)

def _parse_key(k):
	if k[0] == "<" and k[-1] == ">":
		return (0, 0)
	parts = k.split("-")
	modmask = 0
	for mod in parts[:-1]:
		mods = { "c": X.ControlMask, "s": X.ShiftMask, "w": X.Mod4Mask, "a": X.Mod1Mask }
		if mod not in mods:
			raise Exception("Invalid mod '%s'" % mod)
		modmask |= mods[mod]
	keycode = display.keysym_to_keycode(XK.string_to_keysym(parts[-1]))
	if keycode == 0:
		raise Exception("Invalid key '%s'" % parts[-1])
	return (keycode, modmask)

_keymap = None
_callbacks = {}
def _grab_keys(*maps):
	global _callbacks
	newcallbacks = {}

	keys = {}
	for map in maps:
		keys.update(_keymap[map])

	for k in keys:
		code, mask = _parse_key(k)
		if (code, mask) == (0, 0):
			continue
		newcallbacks[code, mask] = keys[k]
		newcallbacks[code, mask | X.Mod2Mask] = keys[k]
		newcallbacks[code, mask | X.LockMask] = keys[k]
		newcallbacks[code, mask | X.Mod2Mask | X.LockMask] = keys[k]

	for key in _callbacks.keys():
		_root.ungrab_key(key[0], key[1])
	for key in newcallbacks.keys():
		_root.grab_key(key[0], key[1], 1, X.GrabModeAsync, X.GrabModeAsync)
	display.sync()

	_callbacks = newcallbacks

	keynames = sorted(sorted(keys), key=lambda l: _parse_key(l))

def start(keys):
	global _keymap, _root
	display.set_error_handler(print)

	import Xlib.keysymdef
	for group in Xlib.keysymdef.__all__:
		XK.load_keysym_group(group)

	global _keymap
	_keymap = keys
	_grab_keys(None)
	_run()

@i3py.util.OtherThread
def _run():
	while True:
		evt = display.next_event()
		if evt.type == X.KeyPress:
			_callbacks[evt.detail, evt.state]()
