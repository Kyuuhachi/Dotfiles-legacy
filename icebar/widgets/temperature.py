from gi.repository import Gtk, GLib
import re
import subprocess
import util

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

		self.icon = Gtk.Label()
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		def tooltip(self, x, y, keyboard, tooltip):
			self.tooltip = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			for chip, adapter, sensors in get_temps():
				label = Gtk.Label(xalign=0)
				label.set_markup(f"<b>{chip}</b>: <i>{adapter}</i>")
				self.tooltip.pack_start(label, True, True, 0)

				for sensor in sensors:
					format = {"temp": "{:.1f} °C", "fan": "{:.0f} RPM"}.get(sensor["type"], "{}")
					left = Gtk.Label(sensor["name"])
					right = Gtk.Label(format.format(sensor["input"]))
					box = Gtk.Box(spacing=7)
					box.pack_start(left, False, False, 15)
					box.pack_end(right, False, False, 15)
					self.tooltip.pack_start(box, True, True, 0)

			self.tooltip.show_all()
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)
		self.set_has_tooltip(True)

		self.icon.show()
		self.text.show()
		box.show()
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
		self.icon.set_text(util.symbol(["", "", "", "", ""], (temp-self.idle)/(crit-self.idle)))
		self.text.set_text("{:.0f}°C".format(temp))

		return True
