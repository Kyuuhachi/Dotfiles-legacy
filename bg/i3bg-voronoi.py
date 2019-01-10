#!/usr/bin/env python3
import i3bg
from Xlib import X

def gen_bg(pixmap, hue, seed):
	from scipy.spatial import Voronoi
	geom = pixmap.get_geometry()
	w, h = geom.width, geom.height
	rand = i3bg.mkrand(seed)

	border = [(w // 2, 0 - h), (w // 2, h + h), (0 - w, h // 2), (w + w, h // 2)]
	points = border + [(rand.random() * w, rand.random() * h) for _ in range(160)]
	vor = Voronoi(points)
	polys = [[(int(v[0]), int(v[1])) for v in vor.vertices[region]] for region in vor.regions]

	def randcolor(rand, hue):
		h = (rand() * 2 - 1) / 360 * 12
		s = rand() * 0.8 + 0.2
		v = rand() * 0.8 + 0.2
		return i3bg.hsv2rgb(hue + h, s, v)

	paint = pixmap.create_gc()
	for verts in polys:
		paint.change(foreground=randcolor(rand.random, hue))
		pixmap.fill_poly(paint, X.Convex, X.CoordModeOrigin, verts)

i3bg.register(gen_bg)
