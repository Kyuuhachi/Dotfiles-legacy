from gi.repository import Gtk, GLib
from math import pi

import simplealsa

__all__ = ["AlsaVolume"]

class AlsaVolume(Gtk.EventBox):
	def __init__(self, card="hw:0", name=("Master", "Speaker"), id=0, base=80, spacing=3):
		super().__init__()

		stack = Gtk.Overlay(visible=True)
		iconP = Gtk.DrawingArea(visible=True)
		self.text = Gtk.Label(visible=True)
		self.icon = VolumeIcon(iconP, self.text, visible=True)
		box = Gtk.Box(spacing=spacing, visible=True)
		box.pack_start(iconP, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		stack.add(box)
		stack.add_overlay(self.icon)
		self.add(stack)

		self.base = base

		self.alsa = simplealsa.Alsa(card)
		self.volume = self.alsa.selem(name[0])
		self.mute = self.alsa.selem(name[1])

		self.min, self.max = self.volume.mB_range

		self.update_volume()
		self.update_mute()
		self.volume.callback(self.update_volume)
		self.mute.callback(self.update_mute)

		def update(*_):
			self.alsa.handle_events()
			return True
		for fd in self.alsa.fds():
			GLib.io_add_watch(fd.fd, GLib.IO_IN, update)

		self.show()

	def update_volume(self, *_):
		mn, mx = self.volume.mB_range
		self.text.set_text("{:.1f} dB".format(self.volume.mB.all / 100 + self.base))
		self.icon.set_value((self.volume.mB.all - mn)/100)
	def update_mute(self, *_):
		self.set_opacity(1 if self.mute.switch.all else 0.5)

class VolumeIcon(Gtk.DrawingArea):
	def __init__(self, placeholder, text, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_value(0)
		self.placeholder = placeholder
		self.text = text

	def set_value(self, v):
		self.value = v
		self.queue_draw()

	def do_draw(self, ctx):
		ctx.push_group()
		ctx.save()
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		ctx.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		fontsize = (metrics.get_ascent() - metrics.get_descent()) / 1024
		pos = (self.get_allocated_height() - fontsize) // 2
		ctx.translate(0, pos)

		self.placeholder.set_size_request(fontsize * 1.6, 0)

		ctx.translate(7, 4)

		ctx.move_to(-8, 3)
		ctx.line_to(-5, 3)
		ctx.line_to(-1, 7)
		ctx.line_to(-1,-7)
		ctx.line_to(-5,-3)
		ctx.line_to(-8,-3)
		ctx.close_path()
		ctx.fill()

		ctx.set_line_cap(1)
		ctx.set_line_width(1.5)
		for a in range(int(self.value/10)):
			ctx.arc(0, 0, 3+a*3, -pi/3, pi/3)
			ctx.stroke()

		ctx.restore()
		ctx.translate(*self.text.translate_coordinates(self, 0, 0))
		ctx.set_operator(9)
		for a in [-2,-1,0,1,2]:
			for b in [-2,-1,0,1,2]:
				if a*a+b*b==8: continue
				ctx.save()
				ctx.translate(a, b)
				self.text.do_draw(self.text, ctx)
				ctx.restore()
		ctx.pop_group_to_source()
		ctx.paint()
