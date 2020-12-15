from gi.repository import Gtk, GLib
from shutil import disk_usage

__all__ = ["Disk"]

class Disk(Gtk.EventBox):
	def __init__(self, path="/"):
		super().__init__()

		self.path = path
		self.text = Gtk.Label(visible=True)
		self.add(self.text)

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
		self.tt_used = row("Used")
		self.tt_total = row("Total")
		self.tt_free = row("Free")

		def tooltip(self, x, y, keyboard, tooltip):
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)
		self.set_has_tooltip(True)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.show()

	def update(self):
		mem = disk_usage(self.path)
		self.text.set_text("{:.1f} GB".format(mem.free / 1024**3))
		self.tt_used.set_text("{:.1f} GB".format(mem.used / 1024**3))
		self.tt_total.set_text("{:.1f} GB".format(mem.total / 1024**3))
		self.tt_free.set_text("{:.1f} GB".format(mem.free / 1024**3))
		return True

