from gi.repository import Gtk, Gdk, GLib
import util
import time

__all__ = ["Clock"]

class Clock(Gtk.EventBox):
	def __init__(self, format="%T"):
		super().__init__()
		self.format = format

		box = Gtk.Box()
		self.text = Gtk.Label()
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.text.show()
		box.show()
		self.show()

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.click)

	def update(self):
		self.text.set_text(time.strftime(self.format, time.localtime(round(time.time()))))
		return True

	def click(self, _, evt):
		if (evt.button, evt.type) == (1, Gdk.EventType.BUTTON_PRESS):
			cal = Gtk.Calendar()
			cal.set_display_options(Gtk.CalendarDisplayOptions.SHOW_WEEK_NUMBERS | Gtk.CalendarDisplayOptions.SHOW_DAY_NAMES | Gtk.CalendarDisplayOptions.SHOW_HEADING)
			self.popup = util.make_popup(cal, self)
			self.popup.show_all()
