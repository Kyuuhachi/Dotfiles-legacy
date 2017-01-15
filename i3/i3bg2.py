#!/usr/bin/env python3
import Xlib.threaded
import Xlib
import Xlib.display
from Xlib import Xatom
from PIL import Image
import os.path
from collections import defaultdict

try:
	import i3ipc.i3ipc as i3ipc
except ImportError:
	import i3ipc

backgrounds = defaultdict(lambda: "#FFFFFF", {
	"6": "#FF00FF",
	"7": "~/Desktop/img.jpg",
})

i3ipc.WorkspaceEvent = lambda data, conn: data
i3ipc.GenericEvent = lambda data: data
i3ipc.WindowEvent = lambda data, conn: data
i3ipc.BarconfigUpdateEvent = lambda data: data
i3ipc.BindingEvent = lambda data: data
i3ipc.Con = lambda data, parent, conn: data
i3 = i3ipc.Connection()

background_cache = {}

def change_workspace(name):
	display = Xlib.display.Display()
	screen = display.screen()
	root = screen.root

	w, h = screen.width_in_pixels, screen.height_in_pixels

	if (name, w, h) not in background_cache:
		background_cache[name, w, h] = gen_bg(root.create_pixmap(w, h, screen.root_depth), name)

	id = background_cache[name, w, h].id
	root.change_property(display.get_atom("_XROOTPMAP_ID"), Xatom.PIXMAP, 32, [id])
	root.change_property(display.get_atom("ESETROOT_PMAP_ID"), Xatom.PIXMAP, 32, [id])
	root.change_attributes(background_pixmap=id)
	display.sync()

def gen_bg(pixmap, name):
	geom = pixmap.get_geometry()
	w, h = geom.width, geom.height
	paint = pixmap.create_gc()
	bg = backgrounds[name]
	if bg[:1] == '#':
		paint.change(foreground=int(bg[1:], 16))
		pixmap.fill_rectangle(paint, 0, 0, w, h)
	else:
		im = Image.open(os.path.expanduser(bg))
		im.thumbnail((w, h), Image.ANTIALIAS)
		pixmap.put_pil_image(paint, 0, 0, im)
	return pixmap

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
