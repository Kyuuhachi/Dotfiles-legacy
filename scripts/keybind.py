#!/usr/bin/env python3

import i3ipc
import subprocess
import os
import sys
import itertools

_i3 = i3ipc.Connection()
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
			active = {}
			active.update(keys[None])
			active.update(keys[self.id])
			grab_keys(active)
		else:
			i3("mode default")()
			grab_keys(keys[None])

keys = {
	None: {
		"w-q": fun, 
		"XF86_MonBrightnessUp":   run("xbacklight -inc 20 -time 0"),
		"XF86_MonBrightnessDown": run("xbacklight -dec 20 -time 0"),
		"XF86_AudioMute":         run("echo mute | nc -U /tmp/i3py"),
		"XF86_AudioRaiseVolume":  run("echo inc  | nc -U /tmp/i3py"),
		"XF86_AudioLowerVolume":  run("echo dec  | nc -U /tmp/i3py"),
		"w-t":                    run("echo kbd  | nc -U /tmp/i3py"),

		"w-Print":   run("scrot    '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),
		"w-s-Print": run("scrot -u '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),

		"w-Return": run("i3-sensible-terminal"),
		"w-d": run("dmenu_run"),
		"w-u": run("compose ~/dot/htmlent.txt"),

		"w-c": i3("reload"),
		"w-s-c": i3("restart"),
		"w-z": lambda: os.execv(__file__, sys.argv),
		"w-s-z": run("i3bar-restart i3bar"),
		"c-a-BackSpace": i3("exit"),

		"w-x": i3("kill"),
		"w-s-x": i3("focus parent;" * 10 + "kill"),

		"w-f": i3("fullscreen"),
		"w-a": i3("focus parent"),
		"w-s-a": i3("focus child"),
		"w-space": i3("focus mode_toggle"),
		"w-s-space": i3("floating toggle"),

		"w-r": mode("resize"),
	},
	"resize": {
		"<name>": "Resize",
		"w-s": i3("layout splith"),
		"w-v": i3("layout splitv"),
		"w-s-s": i3("layout stacking"),
		"w-s-t": i3("layout tabbed"),

		"h": i3("resize shrink width  10 px"),
		"j": i3("resize grow   height 10 px"),
		"k": i3("resize shrink height 10 px"),
		"l": i3("resize grow   width  10 px"),

		"s-h": i3("resize shrink width  1 px"),
		"s-j": i3("resize grow   height 1 px"),
		"s-k": i3("resize shrink height 1 px"),
		"s-l": i3("resize grow   width  1 px"),

		"Escape": mode(None)
	}
}

for n in range(1, 11):
	keys[None]["w-%d" % (n%10)] = i3("workspace %d" % n)
	keys[None]["w-s-%d" % (n%10)] = i3("move container to workspace %d; workspace %d" % (n, n))
for k, d in zip("hjkl", ["left", "down", "up", "right"]):
	keys[None]["w-%s" % k] = i3("focus %s" % d)
	keys[None]["w-s-%s" % k] = i3("move %s" % d)

def get_focus_pid():
	def traverse(obj, func):
		ret = func(obj)
		if ret != None:
			yield ret
		if isinstance(obj, dict):
			for k in obj:
				yield from traverse(obj[k], func)
		elif isinstance(obj, list):
			for k in range(len(obj)):
				yield from traverse(obj[k], func)

	import json
	s = _i3.message(i3ipc.MessageType.GET_TREE, "")
	obj = json.loads(s)

	def get_winid(obj):
		if not isinstance(obj, dict):
			return None
		if not obj.get("focused", False):
			return None
		return obj.get("window", None)
	winid = list(traverse(obj, get_winid))
	if len(winid):
		win = disp.create_resource_object("window", winid[0])
		focus = win.get_full_property(disp.get_atom("_NET_WM_PID"), 0).value[0]
		return focus

from Xlib import X, XK
from Xlib.display import Display
disp = Display()
root = disp.screen().root
disp.set_error_handler(print)

import Xlib.keysymdef
for group in Xlib.keysymdef.__all__:
	XK.load_keysym_group(group)

def parse_key(k):
	if k[0] == "<" and k[-1] == ">":
		return (0, 0)
	parts = k.split("-")
	modmask = 0
	for mod in parts[:-1]:
		mods = { "c": X.ControlMask, "s": X.ShiftMask, "w": X.Mod4Mask, "a": X.Mod1Mask }
		if mod not in mods:
			raise Exception("Invalid mod '%s'" % mod)
		modmask |= mods[mod]
	keycode = disp.keysym_to_keycode(XK.string_to_keysym(parts[-1]))
	if keycode == 0:
		raise Exception("Invalid key '%s'" % parts[-1])
	return (keycode, modmask)

callbacks = {}
def grab_keys(keys):
	global callbacks
	newcallbacks = {}

	for k in keys:
		code, mask = parse_key(k)
		if (code, mask) == (0, 0):
			continue
		newcallbacks[code, mask] = keys[k]
		newcallbacks[code, mask | X.Mod2Mask] = keys[k]
		newcallbacks[code, mask | X.LockMask] = keys[k]
		newcallbacks[code, mask | X.Mod2Mask | X.LockMask] = keys[k]

	for key in callbacks.keys():
		root.ungrab_key(key[0], key[1])
	for key in newcallbacks.keys():
		root.grab_key(key[0], key[1], 1, X.GrabModeAsync, X.GrabModeAsync)
	disp.sync()

	callbacks = newcallbacks

	keynames = sorted(sorted(keys), key=lambda l: parse_key(l))
	print(", ".join(keynames))

grab_keys(keys[None])

while True:
	evt = root.display.next_event()
	if evt.type == X.KeyPress:
		callbacks[evt.detail, evt.state]()
