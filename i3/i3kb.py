#!/usr/bin/env python3
#{{{
import i3ipc
import Xlib
import Xlib.display
from Xlib import X, XK
import subprocess

display = Xlib.display.Display()
i3ipc = i3ipc.Connection()

class i3:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "i3(%r)" % self.cmd
	def __call__(self): return i3ipc.command(self.cmd)

class run:
	def __init__(self, cmd): self.cmd = cmd
	def __repr__(self): return "run(%r)" % self.cmd
	def __call__(self):
		try:
			return subprocess.Popen(self.cmd, shell=True)
		except Exception as e:
			pass

class mode:
	def __init__(self, id): self.id = id
	def __repr__(self): return "mode(%r)" % self.id
	def __call__(self): return grab_keys(self.id)

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
	keysym = XK.string_to_keysym(parts[-1])
	if keysym == 0:
		print("Invalid key '%s'" % parts[-1])
	return (keysym, modmask)

keymap = None
bound = {}
keys = {}
def grab_keys(*maps):
	global keys
	keys = {}
	def add(map):
		if "<extends>" in keymap[map]:
			add(keymap[map]["<extends>"])
		for k, f in keymap[map].items():
			keys[parse_key(k)] = f
	for map in maps:
		add(map)

	rebind()
	display.sync()

def rebind():
	global bound
	root = display.screen().root
	for key in bound.keys():
		root.ungrab_key(key[0], key[1])

	bound = {}
	for (code, mask), func in keys.items():
		code = display.keysym_to_keycode(code)
		if (code, mask) == (0, 0):
			continue
		bound[code, mask] = func
		bound[code, mask | X.Mod2Mask] = func
		bound[code, mask | X.LockMask] = func
		bound[code, mask | X.Mod2Mask | X.LockMask] = func

	for key in bound.keys():
		root.grab_key(key[0], key[1], 1, X.GrabModeAsync, X.GrabModeAsync)

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
			print(type(evt), evt.detail, hex(evt.state), flush=True)
			k = evt.detail, evt.state & modmask
			print(k, bound.get(k, None), flush=True)
			if k in bound:
				bound[k]()
		if evt.type == X.MappingNotify and evt.request == X.MappingKeyboard:
			print(evt, flush=True)
			display.refresh_keyboard_mapping(evt)
			rebind()
#}}}

def backlight(mode):
	m = float(subprocess.check_output("brightnessctl -q m", shell=True))
	states = [0, 1] + [(a/10)**2*m for a in range(2, 11)]
	def closest(list, n):
		aux = []
		for v in list:
			aux.append(abs(n - v))
		return aux.index(min(aux))

	def f():
		n = float(subprocess.check_output("brightnessctl -q g", shell=True))
		idx = closest(states, n) + mode
		if 0 <= idx < len(states):
			run("brightnessctl -q s %d" % states[idx])()
	return f

toggle_cmd = """
window=$(xprop -root -notype _NET_ACTIVE_WINDOW | pcregrep -xo1 '_NET_ACTIVE_WINDOW: window id # (?!0x0)(0x[0-9a-f]+)') || exit
pid=$(xprop -id $window -notype _NET_WM_PID | pcregrep -xo1 '_NET_WM_PID = (\d+)') || exit
state=$(ps --no-headers -o state $pid) || exit
kill -$([[ $state == T ]] && echo CONT || echo STOP) $pid
"""

keys = {
	None: {
		"XF86_MonBrightnessUp":   backlight(+1),
		"XF86_MonBrightnessDown": backlight(-1),

		"Print":   run("maim -ksu                           | xclip -selection clipboard -t image/png"),
		"s-Print": run("maim -k                             | xclip -selection clipboard -t image/png"),
		"a-Print": run("maim -ki $(xdotool getactivewindow) | xclip -selection clipboard -t image/png"),

		"w-Return":  i3("exec --no-startup-id x-terminal-emulator"),
		"w-d":       i3("exec --no-startup-id dmenu_run"),
		"Caps_Lock": i3("exec --no-startup-id compose ~/dot/htmlent.txt"),
		"w-Romaji":  i3("exec --no-startup-id kanjidraw"),

		"w-x": i3("kill"),
		"w-s-x": i3("focus parent;" * 10 + "kill"),
		"w-p": run(toggle_cmd),

		"w-f": i3("fullscreen"),
		"w-s-f": i3("border toggle"),
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
		"w-s-m": i3("move position center"),

		"w-c-h": i3("resize shrink width  10 px"),
		"w-c-j": i3("resize grow   height 10 px"),
		"w-c-k": i3("resize shrink height 10 px"),
		"w-c-l": i3("resize grow   width  10 px"),
		"w-c-m": i3("move position center"),

		"w-c-s-h": i3("resize shrink width  1 px"),
		"w-c-s-j": i3("resize grow   height 1 px"),
		"w-c-s-k": i3("resize shrink height 1 px"),
		"w-c-s-l": i3("resize grow   width  1 px"),
	}
}

start(keys)
