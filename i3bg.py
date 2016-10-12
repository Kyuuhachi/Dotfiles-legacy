#!/usr/bin/env python3
from collections import defaultdict
import Xlib.threaded
import Xlib
from Xlib import Xatom, X
import i3ipc

i3ipc.WorkspaceEvent = lambda data, conn: data
i3ipc.GenericEvent = lambda data: data
i3ipc.WindowEvent = lambda data, conn: data
i3ipc.BarconfigUpdateEvent = lambda data: data
i3ipc.BindingEvent = lambda data: data
i3ipc.Con = lambda data, parent, conn: data
i3 = i3ipc.Connection()

backgrounds = defaultdict(lambda: {})

def change_workspace(workspace):
	display = Xlib.display.Display()
	screen = display.screen()
	root = screen.root

	name = workspace["name"]
	w, h = screen.width_in_pixels, screen.height_in_pixels
	if name not in backgrounds:
		pixmap = root.create_pixmap(w, h, screen.root_depth)
		gen_bg(pixmap, name)
		backgrounds[w, h][name] = pixmap

	root.change_property(display.get_atom("_XROOTPMAP_ID"), Xatom.PIXMAP, 32, [backgrounds[w, h][name].id])
	root.change_property(display.get_atom("ESETROOT_PMAP_ID"), Xatom.PIXMAP, 32, [backgrounds[w, h][name].id])
	root.change_attributes(background_pixmap=backgrounds[w, h][name].id)

	display.sync()

def gen_bg(pixmap, name):
	from scipy.spatial import Voronoi
	import colorsys
	import random
	import hashlib
	geom = pixmap.get_geometry()
	w, h = geom.width, geom.height

	rand = random.Random(int.from_bytes(hashlib.md5(name.encode("utf-8")).digest(), "big"))
	# md5 is supposed to be used as a seed, right?

	border = [(w // 2, 0 - h), (w // 2, h + h), (0 - w, h // 2), (w + w, h // 2)]
	points = [(rand.random() * w, rand.random() * h) for _ in range(16)]
	vor = Voronoi(border + points)
	polys = [[(int(v[0]), int(v[1])) for v in vor.vertices[region]] for region in vor.regions]

	def randcolor(rand, hue):
		h = hue + rand() / 12
		s = rand() * 0.8 + 0.2
		v = rand() * 0.8 + 0.2
		rgb = colorsys.hsv_to_rgb(h, s, v)
		return int(rgb[0] * 0xFF) << 16 | int(rgb[1] * 0xFF) << 8 | int(rgb[2] * 0xFF)

	hue = rand.random()
	paint = pixmap.create_gc()
	for verts in polys:
		paint.change(foreground=randcolor(rand.random, hue))
		pixmap.fill_poly(paint, X.Convex, X.CoordModeOrigin, verts)
	return pixmap

def workspace_event(i3, evt):
	if evt["change"] != "focus":
		return
	change_workspace(evt["current"])
i3.on("workspace", workspace_event)
i3.subscriptions = 0xFF
i3.main()
