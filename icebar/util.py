from gi.repository import Gtk, Gdk, Pango

__all__ = ["symbol", "get_height", "popupify", "make_popup", "framed", "scrollable"]

def symbol(symbols, f):
	if f <= 0: return symbols[0]
	if f >= 1: return symbols[-1]
	return symbols[int(len(symbols) * f)]

def safely(f, default=None):
	try:
		return f()
	except Exception:
		return default

def get_height(self):
	pango = self.get_pango_context()
	layout = Pango.Layout(pango)
	layout.set_text("|", 1)
	return layout.get_pixel_extents()[1].height

def popupify(win, parent):
	win.set_decorated(False)
	win.set_type_hint(Gdk.WindowTypeHint.UTILITY)
	win.set_keep_above(True)
	win.connect("realize", lambda win: win.get_window().set_override_redirect(False))

	win.connect("show", lambda win, parent: win.set_transient_for(parent.get_toplevel()), parent)

	def resize(self, parent):
		parw = parent.get_toplevel()
		w, h = self.get_allocated_width(), self.get_allocated_height()
		ppos = parent.get_allocation()
		winx, winy = parw.get_position()
		ppos.x += winx
		ppos.y += winy

		x = ppos.x + (ppos.width-w)/2
		y = ppos.y - h

		screen = self.get_screen()
		curmon = screen.get_monitor_at_window(screen.get_active_window())
		geom = screen.get_monitor_geometry(curmon)
		if x > geom.width - w: x = geom.width - w
		if x < 0: x = 0

		self.move(x, y)
	win.connect("map", resize, parent)

	def on_mouse(win, evt):
		if evt.type == Gdk.EventType.BUTTON_PRESS and evt.window.get_toplevel() != win.get_window():
			win.hide()

	win.connect("show", Gtk.Widget.grab_add)
	win.connect("hide", Gtk.Widget.grab_remove)
	win.connect("button-press-event", on_mouse)
	win.connect("focus-out-event", lambda win, e: win.hide())

def make_popup(widget, parent):
	win = Gtk.Window()
	popupify(win, parent)
	if widget:
		win.add(widget)
	return win

def framed(widget):
	frame = Gtk.Frame()
	frame.add(widget)
	return frame

pol = {
	True: Gtk.PolicyType.AUTOMATIC,
	False: Gtk.PolicyType.EXTERNAL,
	None: Gtk.PolicyType.NEVER,
}
def scrollable(widget, *, h=True, v=True):
	scroll = Gtk.ScrolledWindow(hscrollbar_policy=pol[h], vscrollbar_policy=pol[v])
	scroll.add(widget)
	return scroll

def print_exc(exc):
	try:
		raise exc
	except Exception:
		import traceback
		traceback.print_exc()

def format_exc(exc):
	try:
		raise exc
	except Exception:
		import traceback
		return traceback.format_exc()
