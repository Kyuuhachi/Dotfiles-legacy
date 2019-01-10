import Xlib.threaded
import Xlib
import Xlib.display
from Xlib import Xatom
import i3ipc.i3ipc as i3ipc
import subprocess

i3ipc.WorkspaceEvent = lambda data, conn: data
i3ipc.GenericEvent = lambda data: data
i3ipc.WindowEvent = lambda data, conn: data
i3ipc.BarconfigUpdateEvent = lambda data: data
i3ipc.BindingEvent = lambda data: data
i3ipc.Con = lambda data, parent, conn: data
i3 = i3ipc.Connection()

backgrounds = {}
colors = {}

c = {
	"i3.focused.bdr":   (0.50, 0.60),
	"i3.focused.bg":    (0.66, 0.47),
	"i3.focused.ind":   (0.81, 0.96),
	"i3.ifocused.bdr":  (0.00, 0.20),
	"i3.ifocused.bg":   (0.10, 0.42),
	"i3.ifocused.ind":  (0.10, 0.31),
	"i3.unfocused.bdr": (0.00, 0.20),
	"i3.unfocused.bg":  (0.00, 0.13),
	"i3.unfocused.ind": (0.10, 0.02),
	"i3.bar.bg":        (0.00, 0.14),
	"i3.bar.text":      (0.00, 0.86),
	"i3.bar.sep":       (0.00, 0.40),
}

def hsv2rgb(h, s, v):
	import colorsys
	rgb = colorsys.hsv_to_rgb(h % 1, s, v)
	return int(rgb[0] * 0xFF) << 16 | int(rgb[1] * 0xFF) << 8 | int(rgb[2] * 0xFF)

def mkrand(seed):
	import random
	return random.Random(mkseed(seed))

def mkseed(seed):
	import platform
	import os
	import pwd
	return sum(map(ord, f"{pwd.getpwuid(os.getuid())}@{platform.node()}:{seed}")) & 0xFFFFFFFF

def change_workspace(name):
	print(f"Changing to {name}", flush=True)
	display = Xlib.display.Display()
	screen = display.screen()
	root = screen.root

	w, h = screen.width_in_pixels, screen.height_in_pixels
	try:
		hue = int(name)/10+1/3
	except:
		hue = mkrand(name).random()

	if name not in colors:
		colors[name] = gen_colors(hue)
	proc = subprocess.Popen(["xrdb", "-merge"], stdin=subprocess.PIPE)
	proc.communicate(input=colors[name].encode())
	proc.wait()
	i3.command("reload")

	if (name, w, h) not in backgrounds:
		backgrounds[name, w, h] = root.create_pixmap(w, h, screen.root_depth)
		gen_bg(backgrounds[name, w, h], hue, name)
	id = backgrounds[name, w, h].id
	root.change_property(display.get_atom("_XROOTPMAP_ID"), Xatom.PIXMAP, 32, [id])
	root.change_property(display.get_atom("ESETROOT_PMAP_ID"), Xatom.PIXMAP, 32, [id])
	root.change_attributes(background_pixmap=id)
	root.clear_area(0, 0, w, h)
	display.sync()

def gen_colors(hue):
	colormap = []
	for k, (s, v) in c.items():
		colormap.append("%s:#%06X" % (k, hsv2rgb(hue, s, v)))
	return "\n".join(colormap)

def gen_bg(pixmap, hue, name):
	raise NotImplemented

def register(gen_bg):
	globals()["gen_bg"] = gen_bg

	for output in i3.get_outputs():
		if output["current_workspace"]:
			change_workspace(output["current_workspace"])
	def workspace_event(i3, evt):
		if evt["change"] != "focus":
			return
		change_workspace(evt["current"]["name"])
	i3.on("workspace", workspace_event)
	i3.subscriptions = 0xFF
	i3.main()
