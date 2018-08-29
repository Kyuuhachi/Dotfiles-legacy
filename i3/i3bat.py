#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gdk
from pathlib import Path

batfile = Path("/sys/class/power_supply/BAT0/capacity")

def main():
	disp = Gdk.Display.get_default()
	assert disp.supports_input_shapes()
	rect = disp.get_primary_monitor().get_geometry()
	win = Gtk.Window()
	win.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)
	win.set_decorated(False)
	win.set_app_paintable(True)
	win.set_keep_above(True)
	win.set_accept_focus(False)
	win.set_visual(disp.get_default_screen().get_rgba_visual())
	win.set_default_size(rect.width, rect.height)
	win.realize()
	win.get_window().set_child_input_shapes()
	win.get_window().set_override_redirect(True)

	win.bat = None
	update(win)
	GLib.timeout_add_seconds(1, update, win)
	win.connect("draw", draw)

	win.show()
	Gtk.main()

def update(win):
	bat = int(batfile.read_bytes())
	if bat != win.bat:
		win.bat = bat
		win.get_window().invalidate_region(win.get_window().get_visible_region(), False)
	return True
def draw_(cr, a, hor):
	import cairo
	if hor:
		g = cairo.LinearGradient(0, 0, cr.get_target().get_width(), 0)
	else:
		g = cairo.LinearGradient(0, 0, 0, cr.get_target().get_height())
	g.add_color_stop_rgba(0, 1, 0, 0, a)
	g.add_color_stop_rgba(0+a/2, 1, 0, 0, 0)
	g.add_color_stop_rgba(1-a/2, 1, 0, 0, 0)
	g.add_color_stop_rgba(1, 1, 0, 0, a)
	cr.set_source(g)
	cr.paint()

def draw(win, cr):
	if win.bat < 10:
		a = (1-win.bat/10)/2
		draw_(cr, a, True)
		draw_(cr, a, False)

if __name__ == "__main__":
	main()
