from gi.repository import Gtk, Gdk, GLib
from psutil import virtual_memory

__all__ = ["RAM"]

class RAM(Gtk.EventBox):
	def __init__(self):
		super().__init__()

		self.text = Gtk.Label()
		self.add(self.text)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.click)

	def update(self):
		mem = virtual_memory()
		self.text.set_text("{:.1f} MB".format((mem.total - mem.available) / 1024**2))
		return True

	def click(self, _, evt):
		pass
