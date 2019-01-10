from gi.repository import Gtk, GLib
import os.path
import time
import cairo
import simplebat

__all__ = ["Battery"]

class Battery(Gtk.EventBox):
	def __init__(self, path, verbose=0, spacing=3):
		super().__init__()
		self.path = path
		self.verbose = verbose

		self.icon = BatteryIcon()
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.tooltip = Gtk.Grid()
		n = 0
		def row(l):
			nonlocal n
			left = Gtk.Label(l, xalign=0)
			right = Gtk.Label(xalign=1)
			self.tooltip.attach(left, 0, n, 1, 1)
			self.tooltip.attach(right, 1, n, 1, 1)
			n += 1
			return right
		self.tt_status = row("Status")
		self.tt_energy = row("Energy")
		self.tt_current = row("Current")
		self.tt_voltage = row("Voltage")
		self.tt_capacity = row("Capacity")
		self.tooltip.show_all()
		self.set_has_tooltip(True)

		def tooltip(self, x, y, keyboard, tooltip):
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

	def update(self):
		if os.path.exists(self.path):
			self.show()
		else:
			self.hide()
			return True

		bat = simplebat.BatteryStatus(self.path)

		self.tt_status.set_text(bat.status)
		self.tt_energy.set_text(f"{bat.energy_now}/{bat.energy_full} Wh ({bat.energy_now/bat.energy_full*100:.1f}%)")
		self.tt_current.set_text(f"{bat.current:+} W")

		self.tt_voltage.set_text(f"{bat.voltage_now}/{bat.voltage_design} V ({(bat.voltage_now/bat.voltage_design-1)*100:+.1f}%)")
		self.tt_capacity.set_text(f"{bat.energy_full}/{bat.energy_design} Wh ({bat.energy_full/bat.energy_design*100:.1f}%)")

		charge = bat.energy_now / bat.energy_full
		self.icon.set_value(charge)
		text = "{:.0f}%".format(charge*100)

		if self.verbose > 0:
			if abs(bat.current) > 0.01:
				symbol = {"Charging": "↑", "Discharging": "↓"}.get(bat.status, "")

				remainingTime = time.strftime("%H:%M", time.gmtime(bat.remaining))
				text += " {}{:.2f}W ({})".format(symbol, abs(bat.current), remainingTime)
			elif self.verbose > 1:
				text += "  -.--W (--:--)"
		self.text.set_text(text)

		return True

class BatteryIcon(Gtk.DrawingArea):
	def __init__(self):
		super().__init__()
		self.set_value(0)

	def set_value(self, v):
		self.value = v
		self.queue_draw()

	def do_draw(self, ctx):
		ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		ctx.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		fontsize = (metrics.get_ascent() - metrics.get_descent()) / 1024
		pos = (self.get_allocated_height() - fontsize) // 2
		ctx.translate(0, pos)

		def path(pts):
			ctx.new_sub_path()
			for x, y in pts:
				ctx.line_to(x, y)
			ctx.close_path()

		t = max(1, int(fontsize/10))
		h = int(fontsize)
		w = int(fontsize * 1.7) # Doesn't include the nub
		self.set_size_request(w+t, h)

		T = t*2
		W = (w-T*2+0.25)*min(self.value, 1)
		path([
			(T, h-T),
			(T + W, h-T),
			(T + W, T),
			(T, T),
		])

		path([
			(t, h-t),
			(w-t, h-t),
			(w-t, h*3/4-t),
			(w, h*3/4-t),
			(w, h*1/4+t),
			(w-t, h*1/4+t),
			(w-t, t),
			(t, t),
		])

		path([
			(0, h),
			(w, h),
			(w, h*3/4),
			(w+t, h*3/4),
			(w+t, h*1/4),
			(w, h*1/4),
			(w, 0),
			(0, 0),
		])

		ctx.fill()
