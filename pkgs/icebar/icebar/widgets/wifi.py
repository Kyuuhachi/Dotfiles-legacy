from gi.repository import Gtk, GLib
from icebar.lib import simplewifi
from math import pi
import psutil

__all__ = ["Wifi"]
class Wifi(Gtk.EventBox):
	def __init__(self, *, spacing=3):
		super().__init__()

		self.icon = WifiIcon(visible=True)
		self.text_up = Gtk.Label(visible=True)
		self.text_dn = Gtk.Label(visible=True)
		self.text_up2 = WifiText("↑", visible=True)
		self.text_dn2 = WifiText("↓", visible=True)
		box = Gtk.Box(spacing=spacing, visible=True)
		box.pack_start(self.icon, False, False, 0)

		# box2 = Gtk.Box(visible=True, orientation=Gtk.Orientation.VERTICAL, baseline_position=Gtk.BaselinePosition.CENTER)
		# box2.pack_start(Gtk.Box(visible=True), True, True, 0)
		# box2.pack_start(self.text_up2, False, False, 0)
		# box2.pack_start(self.text_dn2, False, False, 0)
		# box2.pack_start(Gtk.Box(visible=True), True, True, 0)
		# box.pack_start(box2, False, False, 0)

		# box2 = Gtk.Box(visible=True, orientation=Gtk.Orientation.VERTICAL)
		# box2.pack_start(self.text_up, False, False, 0)
		# box2.pack_start(self.text_dn, False, False, 0)
		# box.pack_start(box2, False, False, 0)

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
		self.tt_name = row("Interface")
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
		self.io_prev = {}
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

			def fmt(w, k, name):
				prev = self.io_prev.get(name)
				val = getattr(stat, name)
				if prev is not None:
					a = float(val - prev)
					for u in "KMGTP":
						a /= 1024
						if a < 512: break
					t = f"{a:.1f}{u}"
					w.set_value(val - prev)
				else:
					t = "-"
					w.set_value(None)
				self.io_prev[name] = val
				return f"<small><small>{k}{t}</small></small>"

			stat = psutil.net_io_counters()
			self.text_up.set_markup(fmt(self.text_up2, "↑", "bytes_sent"))
			self.text_dn.set_markup(fmt(self.text_dn2, "↓", "bytes_recv"))
		else:
			self.set_opacity(0.5)
			self.set_has_tooltip(False)
			self.icon.set_value(0)
			self.io_prev.clear()
			self.text.set_text("OFF" if up is False else "ERROR")

		return True

class WifiIcon(Gtk.DrawingArea):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_value(0)

	def set_value(self, v):
		self.value = v
		self.queue_draw()

	def do_draw(self, cr):
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		cr.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		fontsize = (metrics.get_ascent() - metrics.get_descent()) / 1024
		pos = (self.get_allocated_height() - fontsize) // 2
		cr.translate(0, pos)

		self.set_size_request(fontsize*1.6, fontsize*1.6)

		cr.translate(fontsize*0.8, fontsize)
		cr.scale(fontsize/10, fontsize/10)

		def path(r):
			cr.arc(0, 0, 3*r, -pi/2-pi/4, -pi/2+pi/4)
			cr.arc_negative(0, 0, 3*r+2,  -pi/2+pi/4, -pi/2-pi/4)
			cr.fill()

		if self.value <= 0/4: cr.set_source_rgba(r, g, b, a/2)
		path(0)
		if self.value <= 1/4: cr.set_source_rgba(r, g, b, a/2)
		path(1)
		if self.value <= 2/4: cr.set_source_rgba(r, g, b, a/2)
		path(2)
		if self.value <= 3/4: cr.set_source_rgba(r, g, b, a/2)
		path(3)

class WifiText(Gtk.DrawingArea):
	def __init__(self, prefix, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.prefix = prefix
		self.set_value(None)

		style = Gtk.CssProvider()
		self.get_style_context().add_provider(style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		style.load_from_data("* {font-size: 100%; background: black; padding: 2px; margin: -2px;}".encode())

	def set_value(self, v):
		self.value = v
		self.queue_draw()

	def do_draw(self, cr):
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		cr.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		ratio = metrics.get_ascent()/(metrics.get_ascent()+metrics.get_descent())
		fontsize = (metrics.get_ascent() + metrics.get_descent()) / 1024
		self.set_size_request(40, fontsize)

		w, h = self.get_allocated_width(), self.get_allocated_height()
		Gtk.render_background(style, cr, 0, 0, w, h-1)

		cr.translate(0, -metrics.get_descent()/1024*ratio)

		font = pango.get_font_description().copy()
		font.set_size(h*1024*ratio)
		lay = self.create_pango_layout()
		lay.set_text(self.prefix+"012K")
		Gtk.render_layout(style, cr, 0, 0, lay)
