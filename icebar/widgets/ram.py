from gi.repository import Gtk, GLib
from psutil import virtual_memory

__all__ = ["RAM"]

class RAM(Gtk.EventBox):
	def __init__(self):
		super().__init__()

		self.text = Gtk.Label(visible=True)
		self.add(self.text)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.show()

	def update(self):
		mem = virtual_memory()
		self.text.set_text("{:.1f} MB".format((mem.total - mem.available) / 1024**2))
		return True
