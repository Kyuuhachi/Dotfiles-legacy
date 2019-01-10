import gi
gi.require_version("IBus", "1.0")
from gi.repository import Gtk, Gdk, GLib, IBus as _IBus

__all__ = ["IBus"]

class IBus(Gtk.EventBox):
	def __init__(self, names):
		super().__init__()
		self.names = names

		self.text = Gtk.Label()
		self.add(self.text)

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.click)

		self.bus = _IBus.Bus.new()
		self.bus.set_watch_ibus_signal(True)
		self.bus.connect("global-engine-changed", self.change_engine)
		GLib.idle_add(self.change_engine, self.bus, self.bus.get_global_engine().get_name(), priority=200)

		self.text.show()

	def change_engine(self, bus, engine):
		if engine in self.names:
			self.text.set_text(self.names[engine])
			self.show()
		else:
			self.hide()

	def click(self, _, evt):
		pass
