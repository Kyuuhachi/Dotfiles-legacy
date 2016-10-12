#!/usr/bin/env python3
import i3ipc
import Xlib
from Xlib import X, XK

display = Xlib.display.Display()
root = display.screen().root
i3ipc = i3ipc.Connection()

class i3:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "i3(%s)" % repr(self.cmd)
	def __call__(self): i3ipc.command(self.cmd)

class run:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "run(%s)" % repr(self.cmd)
	def __call__(self): i3ipc.command("exec --no-startup-id " + self.cmd)

class mode:
	def __init__(self, id): self.id = id
	def __repr__(self): return "mode(%s)" % repr(self.id)
	def __call__(self): grab_keys(None, self.id)

def parse_key(k):
	if k[0] == "<" and k[-1] == ">":
		return (0, 0)
	parts = k.split("-")
	modmask = 0
	for mod in parts[:-1]:
		mods = {"c": X.ControlMask, "s": X.ShiftMask, "w": X.Mod4Mask, "a": X.Mod1Mask}
		if mod not in mods:
			raise Exception("Invalid mod '%s'" % mod)
		modmask |= mods[mod]
	keycode = display.keysym_to_keycode(XK.string_to_keysym(parts[-1]))
	if keycode == 0:
		raise Exception("Invalid key '%s'" % parts[-1])
	return (keycode, modmask)

keymap = None
callbacks = {}
def grab_keys(*maps):
	global callbacks
	newcallbacks = {}

	keys = {}
	for map in maps:
		keys.update(keymap[map])

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
	display.sync()

	callbacks = newcallbacks

def start(keys):
	global keymap, root
	display.set_error_handler(print)

	import Xlib.keysymdef
	for group in Xlib.keysymdef.__all__:
		XK.load_keysym_group(group)

	global keymap
	keymap = keys
	grab_keys(None)

	while True:
		evt = display.next_event()
		if evt.type == X.KeyPress:
			k = evt.detail, evt.state & 0xFF
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
		"w-u": run("compose ~/dot/htmlent.txt"),

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

		"w-r": mode("resize"),
	},
	"resize": {
		"<name>": "Resize",
		"s": i3("layout splith"),
		"s-s": i3("layout tabbed"),
		"v": i3("layout splitv"),
		"s-v": i3("layout stacking"),

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
	keys[None]["w-%d" % (n % 10)] = i3("workspace %d" % n)
	keys[None]["w-s-%d" % (n % 10)] = i3("move container to workspace %d; workspace %d" % (n, n))
for k, d in zip("hjkl", ["left", "down", "up", "right"]):
	keys[None]["w-%s" % k] = i3("focus %s" % d)
	keys[None]["w-s-%s" % k] = i3("move %s" % d)

print(keys)
start(keys)
