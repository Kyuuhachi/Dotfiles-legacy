#!/usr/bin/env python3
import i3bg
import subprocess
import os.path
import struct

def gen_bg(pixmap, hue, name):
	geom = pixmap.get_geometry()
	w, h = geom.width, geom.height
	# w, h = w//2, h//2
	sugoi = os.path.join(os.path.dirname(__file__), "sugoi")
	print(sugoi)
	data = subprocess.check_output([sugoi, str(w), str(h), str(i3bg.mkseed(name)), str(hue)])
	w, h = struct.unpack_from("=II", data, 0)
	pixels = data[8:]

	from Xlib import X
	from Xlib.protocol import request

	pad = pixmap.display.info.bitmap_format_scanline_pad
	unit = pixmap.display.info.bitmap_format_scanline_unit
	maxlen = (pixmap.display.info.max_request_length << 2) - request.PutImage._request.static_size

	stride = roundup(w * unit, pad) >> 3
	segh = maxlen // stride
	gc = pixmap.create_gc()
	for segy in range(0, h, segh):
		cursegh = min(segh, h - segy)
		pixmap.put_image(gc, 0, segy, w, cursegh, X.ZPixmap, 24, 0, pixels[segy*w*4:(segy+cursegh)*w*4])

def roundup(value, unit):
	return (value + (unit - 1)) & ~(unit - 1)

i3bg.register(gen_bg)
