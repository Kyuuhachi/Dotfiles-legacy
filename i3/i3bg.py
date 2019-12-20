import Xlib.threaded
import Xlib
import Xlib.display
from Xlib import Xatom
import subprocess

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

def mkseed(name=""):
	import platform
	import os
	import pwd
	import hashlib
	host = platform.node()
	user = pwd.getpwuid(os.getuid()).pw_name
	return int.from_bytes(hashlib.sha1(f"{user}@{host}/{name}".encode()).digest(), "little")

def mkrand(name=""):
	import random
	return random.Random(mkseed(name))

async def change_workspace(i3, gen_bg, name):
	try:
		hue = int(name)/10 + mkrand().random()
	except ValueError:
		hue = mkrand(name).random()

	if name not in colors:
		colors[name] = gen_colors(hue)

	proc = subprocess.Popen(["xrdb", "-merge"], stdin=subprocess.PIPE)
	proc.communicate(input=colors[name].encode())
	proc.wait()

	cmd = i3.command(i3.COMMAND, "reload")

	display = Xlib.display.Display()
	screen = display.screen()
	w, h = screen.width_in_pixels, screen.height_in_pixels
	if (name, w, h) not in backgrounds:
		backgrounds[name, w, h] = screen.root.create_pixmap(w, h, screen.root_depth)
		gen_bg(backgrounds[name, w, h], hue, name)

	id = backgrounds[name, w, h].id
	screen.root.change_property(display.get_atom("_XROOTPMAP_ID"), Xatom.PIXMAP, 32, [id])
	screen.root.change_property(display.get_atom("ESETROOT_PMAP_ID"), Xatom.PIXMAP, 32, [id])
	screen.root.change_attributes(background_pixmap=id)
	screen.root.clear_area(0, 0, w, h)

	display.sync()
	await cmd

def gen_colors(hue):
	colormap = []
	for k, (s, v) in c.items():
		colormap.append("%s:#%06X" % (k, hsv2rgb(hue, s, v)))
	return "\n".join(colormap)

def register(gen_bg):
	import asyncio
	async def run():
		import simplei3
		i3 = await simplei3.i3ipc()

		for output in await i3.command(i3.GET_OUTPUTS):
			if output["current_workspace"]:
				await change_workspace(i3, gen_bg, output["current_workspace"])

		@i3.on_event
		async def workspace_event(type, payload):
			if type == i3.E_WORKSPACE and payload["change"] == "focus":
				await change_workspace(i3, gen_bg, payload["current"]["name"])
		await i3.command(i3.SUBSCRIBE, ["workspace"])
	asyncio.ensure_future(run())
	asyncio.get_event_loop().run_forever()
