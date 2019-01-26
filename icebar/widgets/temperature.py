from gi.repository import Gtk, GLib
import re
import subprocess
import math

__all__ = ["Temperature"]

input_re = re.compile(r"^  (\w+)(\d+)_(\w+): (\d+\.\d+)$")

def get_temps():
	out = subprocess.check_output(["sensors", "-u"]).decode()
	it = iter(out.splitlines())
	for chip in it:
		adapter = next(it)
		assert adapter.startswith("Adapter: ")
		adapter = adapter[9:]

		sensors = []
		for l in it:
			if not l: break
			if l[-1:] == ":":
				sensors.append({"name": l[:-1]})
			else:
				match = input_re.match(l)
				if not match: raise ValueError(l)
				type, n, key, val = match.groups()
				n = int(n) - 1

				sensors[-1]["type"] = type
				sensors[-1][key] = float(val)
		yield chip, adapter, sensors

class Temperature(Gtk.EventBox):
	def __init__(self, chip, which, idle, crit=None, spacing=3):
		super().__init__()
		self.chip = chip
		self.which = which
		self.idle = idle
		self.crit = crit

		self.icon = TempIcon(visible=True)
		self.text = Gtk.Label(visible=True)
		box = Gtk.Box(spacing=spacing, visible=True)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		def tooltip(self, x, y, keyboard, tooltip):
			self.tooltip = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			for chip, adapter, sensors in get_temps():
				label = Gtk.Label(xalign=0, visible=True)
				label.set_markup(f"<b>{chip}</b>: <i>{adapter}</i>")
				self.tooltip.pack_start(label, True, True, 0)

				for sensor in sensors:
					format = {"temp": "{:.1f} °C", "fan": "{:.0f} RPM"}.get(sensor["type"], "{}")
					left = Gtk.Label(sensor["name"], visible=True)
					right = Gtk.Label(format.format(sensor["input"]), visible=True)
					box = Gtk.Box(spacing=7, visible=True)
					box.pack_start(left, False, False, 15)
					box.pack_end(right, False, False, 15)
					self.tooltip.pack_start(box, True, True, 0)

			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)
		self.set_has_tooltip(True)

		self.show()

	def update(self):
		sensor = None
		for chip, adapter, sensors in get_temps():
			if chip == self.chip:
				for sensor in sensors:
					if sensor["name"] == self.which:
						break

		crit = sensor.get("crit", self.crit)
		temp = sensor.get("input", 0.0)
		self.icon.set_value((temp-self.idle)/(crit-self.idle))
		self.text.set_text("{:.0f}°C".format(temp))

		return True

class TempIcon(Gtk.DrawingArea):
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

		self.set_size_request(9, fontsize/20*23)

		t = max(1, fontsize//10)
		ctx.translate(4*t, 8*t)
		if t % 2:
			ctx.translate(-.5, -.5)

		def arc(x, y, r, v, f=ctx.arc):
			f(x, y, r/2, -math.acos(-v/r), -math.acos(v/r))

		h = -7*t

		arc(0, h, 5*t, +5*t)
		arc(0, 0, 7*t, -5*t)
		ctx.close_path()
		ctx.new_sub_path()
		arc(0, h, 3*t, -3*t, f=ctx.arc_negative)
		arc(0, 0, 5*t, +3*t, f=ctx.arc_negative)
		ctx.fill()

		arc(0, 0, 3*t, -t)
		arc(0, h*self.value, t, t)
		ctx.close_path()
		ctx.fill()

		for a in range(0, 3):
			ctx.move_to(5.5*t, h+0+(2*a-0.5)*t)
			ctx.line_to(3.5*t, h+0+(2*a-0.5)*t)
			ctx.line_to(3.5*t, h+t+(2*a-0.5)*t)
			ctx.line_to(5.5*t, h+t+(2*a-0.5)*t)
			ctx.close_path()
			ctx.fill()
