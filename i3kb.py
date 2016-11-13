#!/usr/bin/env python3
import i3ipc
import Xlib
from Xlib import X, XK

display = Xlib.display.Display()
root = display.screen().root
i3ipc = i3ipc.Connection()

if True:
	def system(cmd):
		print(cmd)
		print(i3ipc.command(cmd))
		import sys
		sys.stdout.flush()
else:
	system = i3ipc.command

class i3:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "i3(%r)" % self.cmd
	def __call__(self): system(self.cmd)

class run:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "run(%r)" % self.cmd
	def __call__(self): system("exec --no-startup-id %s" % self.cmd)

class mode:
	def __init__(self, id): self.id = id
	def __repr__(self): return "mode(%r)" % self.id
	def __call__(self): grab_keys(self.id)

mods = {"c": X.ControlMask, "s": X.ShiftMask, "w": X.Mod4Mask, "a": X.Mod1Mask}
modmask = 0
for mod in mods:
	modmask |= mods[mod]

def parse_key(k):
	if k[0] == "<" and k[-1] == ">":
		return (0, 0)
	parts = k.split("-")
	modmask = 0
	for mod in parts[:-1]:
		if mod not in mods:
			raise Exception("Invalid mod '%s'" % mod)
		modmask |= mods[mod]
	keycode = display.keysym_to_keycode(XK.string_to_keysym(parts[-1]))
	if keycode == 0:
		print("Invalid key '%s'" % parts[-1])
	return (keycode, modmask)

keymap = None
callbacks = {}
def grab_keys(*maps):
	global callbacks

	keys = {}
	def add(map):
		if "<extends>" in keymap[map]:
			add(keymap["map"]["<extends>"])
		keys.update(keymap[map])
	for map in maps:
		add(map)

	for key in callbacks.keys():
		root.ungrab_key(key[0], key[1])

	callbacks = {}
	for k in keys:
		code, mask = parse_key(k)
		if (code, mask) == (0, 0):
			continue
		callbacks[code, mask] = keys[k]
		callbacks[code, mask | X.Mod2Mask] = keys[k]
		callbacks[code, mask | X.LockMask] = keys[k]
		callbacks[code, mask | X.Mod2Mask | X.LockMask] = keys[k]

	for key in callbacks.keys():
		root.grab_key(key[0], key[1], 1, X.GrabModeAsync, X.GrabModeAsync)
	display.sync()

def start(keys):
	global keymap, root

	import Xlib.keysymdef
	for group in Xlib.keysymdef.__all__:
		XK.load_keysym_group(group)

	global keymap
	keymap = keys
	grab_keys(None)

	while True:
		evt = display.next_event()
		if evt.type == X.KeyPress:
			k = evt.detail, evt.state & modmask
			if k in callbacks:
				callbacks[k]()

keys = {
	None: {
		"XF86_MonBrightnessUp":   run("xbacklight -inc 20 -time 0"),
		"XF86_MonBrightnessDown": run("xbacklight -dec 20 -time 0"),
		"XF86_AudioMute":         run("echo mute | nc -U /tmp/i3py"),
		"XF86_AudioRaiseVolume":  run("echo inc  | nc -U /tmp/i3py"),
		"XF86_AudioLowerVolume":  run("echo dec  | nc -U /tmp/i3py"),

		"w-Print":   run("scrot    '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),
		"w-s-Print": run("scrot -u '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),

		"w-Return": run("i3-sensible-terminal"),
		"w-d": run("dmenu_run"),
		"Caps_Lock": run("compose ~/dot/htmlent.txt"),

		"w-c": i3("reload"),
		"w-z": i3("restart"),
		"c-a-BackSpace": i3("exit"),

		"w-x": i3("kill"),
		"w-s-x": i3("focus parent;" * 10 + "kill"),

		"w-f": i3("fullscreen"),
		"w-a": i3("focus parent"),
		"w-s-a": i3("focus child"),
		"w-space": i3("focus mode_toggle"),
		"w-s-space": i3("floating toggle"),

		"w-1": i3("workspace 1"),
		"w-2": i3("workspace 2"),
		"w-3": i3("workspace 3"),
		"w-4": i3("workspace 4"),
		"w-5": i3("workspace 5"),
		"w-6": i3("workspace 6"),
		"w-7": i3("workspace 7"),
		"w-8": i3("workspace 8"),
		"w-9": i3("workspace 9"),
		"w-0": i3("workspace 10"),

		"w-s-1": i3("move container to workspace 1; workspace 1"),
		"w-s-2": i3("move container to workspace 2; workspace 2"),
		"w-s-3": i3("move container to workspace 3; workspace 3"),
		"w-s-4": i3("move container to workspace 4; workspace 4"),
		"w-s-5": i3("move container to workspace 5; workspace 5"),
		"w-s-6": i3("move container to workspace 6; workspace 6"),
		"w-s-7": i3("move container to workspace 7; workspace 7"),
		"w-s-8": i3("move container to workspace 8; workspace 8"),
		"w-s-9": i3("move container to workspace 9; workspace 9"),
		"w-s-0": i3("move container to workspace 10; workspace 10"),

		"w-h": i3("focus left"),
		"w-j": i3("focus down"),
		"w-k": i3("focus up"),
		"w-l": i3("focus right"),

		"w-s-h": i3("move left"),
		"w-s-j": i3("move down"),
		"w-s-k": i3("move up"),
		"w-s-l": i3("move right"),

		"w-r": mode("resize"),
	},
	"resize": {
		"<name>": "Resize",
		"<extends>": None,

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

start(keys)
