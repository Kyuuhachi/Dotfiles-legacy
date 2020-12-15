from gi.repository import Gtk, GLib
from icebar import simplewifi
from math import pi

__all__ = ["Wifi"]
class Wifi(Gtk.EventBox):
	def __init__(self, *, spacing=3):
		super().__init__()

		self.icon = WifiIcon(visible=True)
		self.text = Gtk.Label(visible=True)
		box = Gtk.Box(spacing=spacing, visible=True)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.tooltip = Gtk.Grid()
		n = 0
		def row(l):
			nonlocal n
			left = Gtk.Label(l, xalign=0, visible=True)
			right = Gtk.Label(xalign=1, visible=True)
			self.tooltip.attach(left, 0, n, 1, 1)
			self.tooltip.attach(right, 1, n, 1, 1)
			n += 1
			return right
		self.tt_name = row("Name")
		self.tt_ssid = row("SSID")
		self.tt_quality = row("Quality")
		self.tt_ipv4 = row("IPv4")
		self.tt_ipv6 = row("IPv6")
		self.tt_mac = row("MAC")

		def tooltip(self, x, y, keyboard, tooltip):
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.show()

	def update(self):
		for (name, up, essid, quality, ipv4, ipv6, mac) in simplewifi.wifi_status():
			if essid is not None:
				break
		else:
			(name, up, essid, quality, ipv4, ipv6, mac) = (None,) * 7

		if up is not None and essid is not None:
			self.set_opacity(1)
			self.set_has_tooltip(True)
			self.tt_name.set_text(name)
			self.tt_ssid.set_text(essid)
			self.tt_quality.set_text("{}%".format(quality or 0))
			self.tt_ipv4.set_text(ipv4 or "-")
			self.tt_ipv6.set_text(ipv6 or "-")
			self.tt_mac.set_text(mac or "-")
			self.icon.set_value(1/4 + (quality or 0)/100*3/4)
		else:
			self.set_opacity(0.5)
			self.set_has_tooltip(False)
			self.icon.set_value(0)
		self.text.set_text({None: "ERROR", False: "OFF", True: essid or "DOWN"}[up])

		return True

class WifiIcon(Gtk.DrawingArea):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_value(0)

	def set_value(self, v):
		self.value = v
		self.queue_draw()

	def do_draw(self, ctx):
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		ctx.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		fontsize = (metrics.get_ascent() - metrics.get_descent()) / 1024
		pos = (self.get_allocated_height() - fontsize) // 2
		ctx.translate(0, pos)

		self.set_size_request(fontsize*1.6, fontsize*1.6)

		ctx.translate(fontsize*0.8, fontsize)
		ctx.scale(fontsize/10, fontsize/10)

		def path(r):
			ctx.arc(0, 0, 3*r, -pi/2-pi/4, -pi/2+pi/4)
			ctx.arc_negative(0, 0, 3*r+2,  -pi/2+pi/4, -pi/2-pi/4)
			ctx.fill()

		if self.value <= 0/4: ctx.set_source_rgba(r, g, b, a/2)
		path(0)
		if self.value <= 1/4: ctx.set_source_rgba(r, g, b, a/2)
		path(1)
		if self.value <= 2/4: ctx.set_source_rgba(r, g, b, a/2)
		path(2)
		if self.value <= 3/4: ctx.set_source_rgba(r, g, b, a/2)
		path(3)
