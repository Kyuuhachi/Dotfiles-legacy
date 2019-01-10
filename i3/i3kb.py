#!/usr/bin/env python3

import asyncio

def this_should_be_a_module():
	import Xlib
	import Xlib.display
	from Xlib import X, XK
	import Xlib.keysymdef
	for group in Xlib.keysymdef.__all__:
		XK.load_keysym_group(group)

	mods = {"c": X.ControlMask, "s": X.ShiftMask, "w": X.Mod4Mask, "a": X.Mod1Mask}
	modmask = 0
	for mod in mods:
		modmask |= mods[mod]

	def parse_key(k):
		(*parts, sym) = k.split("-")
		modmask = 0
		for mod in parts:
			modmask |= mods[mod]
		keysym = XK.string_to_keysym(sym)
		if keysym == 0:
			print("Invalid key '%s'" % parts)
		return (keysym, modmask)

	display = Xlib.display.Display()
	bound = {}
	all_keys = {}
	def regrab_keys():
		root = display.screen().root

		for key in bound.keys():
			root.ungrab_key(key[0], key[1])
		display.sync()

		bound.clear()
		grab_keys(all_keys)

	def grab_keys(keys):
		for (code, mask), func in keys.items():
			code = display.keysym_to_keycode(code)
			if (code, mask) == (0, 0):
				continue
			bound[code, mask] = func
			bound[code, mask | X.Mod2Mask] = func
			bound[code, mask | X.LockMask] = func
			bound[code, mask | X.Mod2Mask | X.LockMask] = func

		root = display.screen().root
		for key in bound.keys():
			root.grab_key(key[0], key[1], 1, X.GrabModeAsync, X.GrabModeAsync)
		display.sync()

	def bind(keys):
		keys = {parse_key(k): f for k, f in keys.items()}
		grab_keys(keys)
		all_keys.update(keys)

	def start():
		def on_event():
			nonlocal bound
			while display.pending_events():
				evt = display.next_event()
				if evt.type == X.KeyPress:
					k = (evt.detail, evt.state & modmask)
					if k in bound:
						asyncio.ensure_future(bound[k]())
				if evt.type == X.MappingNotify and evt.request == X.MappingKeyboard:
					display.refresh_keyboard_mapping(evt)
					regrab_keys()
		asyncio.get_event_loop().add_reader(display.fileno(), on_event)
		asyncio.get_event_loop().run_forever()
	return bind, start
bind, start = this_should_be_a_module()

async def read_subproc(*cmd):
	proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
	stdout, _ = await proc.communicate()
	return stdout

async def init_backlight():
	max = float(await read_subproc("brightnessctl", "-q", "m"))
	states = [0, 1] + [(a/10)**2*max for a in range(2, 11)]
	def closest(list, n):
		aux = []
		for v in list:
			aux.append(abs(n - v))
		return aux.index(min(aux))

	async def brightness(mode):
		current = float(await read_subproc("brightnessctl", "-q", "g"))
		idx = closest(states, current) + mode
		if 0 <= idx < len(states):
			await asyncio.create_subprocess_exec("brightnessctl", "-q", "s", str(states[idx]))

	bind({
		"XF86_MonBrightnessUp":   lambda: brightness(+1),
		"XF86_MonBrightnessDown": lambda: brightness(-1)
	})

async def init_alsa(card="hw:0", name=("Master", "Speaker")):
	import simplealsa
	alsa = simplealsa.Alsa(card)
	volume = alsa.selem(name[0])
	mute = alsa.selem(name[1])

	def update(*_):
		alsa.handle_events()
	for fd in alsa.fds():
		asyncio.get_event_loop().add_reader(fd.fd, update)

	async def toggleSwitch(): mute.switch.all = not mute.switch.all
	async def setSwitch(v): mute.elem.switch.all = v
	async def changeVolume(n): volume.mB.all += n
	bind({
		"XF86_AudioMute": lambda: toggleSwitch(),
		"XF86_AudioRaiseVolume": lambda: changeVolume(+250),
		"XF86_AudioLowerVolume": lambda: changeVolume(-250),
		"s-XF86_AudioMute": lambda: setSwitch(False),
		"s-XF86_AudioRaiseVolume": lambda: changeVolume(+50),
		"s-XF86_AudioLowerVolume": lambda: changeVolume(-50)
	})

async def init_screenshot():
	async def maim(flags):
		await asyncio.create_subprocess_shell(f"maim {flags} | xclip -selection clipboard -t image/png")
	bind({
		"Print":   lambda: maim("-ksu"),
		"s-Print": lambda: maim("-k"),
		"a-Print": lambda: maim("-ki $(xdotool getactivewindow)"),
	})

async def init_launch():
	async def launch(*cmd):
		import os
		if os.fork() == 0:
			if os.fork() == 0:
				os.execvp(cmd[0], cmd)
			else:
				os._exit(0)
	bind({
		"w-Return":  lambda: launch("x-terminal-emulator"),
		"w-d":       lambda: launch("dmenu_run"),
		"Caps_Lock": lambda: launch("compose"),
	})

async def init_pause():
	async def run():
		await asyncio.create_subprocess_shell("""
			window=$(xprop -root -notype _NET_ACTIVE_WINDOW | pcregrep -xo1 '_NET_ACTIVE_WINDOW: window id # (?!0x0)(0x[0-9a-f]+)') || exit
			pid=$(xprop -id $window -notype _NET_WM_PID | pcregrep -xo1 '_NET_WM_PID = (\d+)') || exit
			state=$(ps --no-headers -o state $pid) || exit
			kill -$([[ $state == T ]] && echo CONT || echo STOP) $pid
		""")
	bind({"w-p": run})

async def init_i3():
	import simplei3
	i3ipc = await simplei3.i3ipc()

	i3 = lambda cmd: lambda: i3ipc.command(i3ipc.COMMAND, cmd)
	bind({
		"w-x": i3("kill"), "w-s-x": i3("focus parent;" * 10 + "kill"),

		"w-f": i3("fullscreen"), "w-s-f": i3("border toggle"),
		"w-a": i3("focus parent"), "w-s-a": i3("focus child"),
		"w-space": i3("focus mode_toggle"), "w-s-space": i3("floating toggle"),
		"w-c-space": i3("move position center"),

		"w-1": i3("workspace 1"),  "w-s-1": i3("move container to workspace 1; workspace 1"),
		"w-2": i3("workspace 2"),  "w-s-2": i3("move container to workspace 2; workspace 2"),
		"w-3": i3("workspace 3"),  "w-s-3": i3("move container to workspace 3; workspace 3"),
		"w-4": i3("workspace 4"),  "w-s-4": i3("move container to workspace 4; workspace 4"),
		"w-5": i3("workspace 5"),  "w-s-5": i3("move container to workspace 5; workspace 5"),
		"w-6": i3("workspace 6"),  "w-s-6": i3("move container to workspace 6; workspace 6"),
		"w-7": i3("workspace 7"),  "w-s-7": i3("move container to workspace 7; workspace 7"),
		"w-8": i3("workspace 8"),  "w-s-8": i3("move container to workspace 8; workspace 8"),
		"w-9": i3("workspace 9"),  "w-s-9": i3("move container to workspace 9; workspace 9"),
		"w-0": i3("workspace 10"), "w-s-0": i3("move container to workspace 10; workspace 10"),

		"w-h": i3("focus left"),  "w-s-h": i3("move left"),
		"w-j": i3("focus down"),  "w-s-j": i3("move down"),
		"w-k": i3("focus up"),    "w-s-k": i3("move up"),
		"w-l": i3("focus right"), "w-s-l": i3("move right"),

		"w-c-h": i3("resize shrink width  10 px"), "w-c-s-h": i3("resize shrink width  1 px"),
		"w-c-j": i3("resize grow   height 10 px"), "w-c-s-j": i3("resize grow   height 1 px"),
		"w-c-k": i3("resize shrink height 10 px"), "w-c-s-k": i3("resize shrink height 1 px"),
		"w-c-l": i3("resize grow   width  10 px"), "w-c-s-l": i3("resize grow   width  1 px"),
	})

asyncio.ensure_future(init_i3())
asyncio.ensure_future(init_backlight())
asyncio.ensure_future(init_alsa())
asyncio.ensure_future(init_launch())
asyncio.ensure_future(init_pause())
asyncio.ensure_future(init_screenshot())
start()
