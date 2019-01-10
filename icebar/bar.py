#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import os
import sys
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 1)
sys.stderr = os.fdopen(sys.stderr.fileno(), "w", 1)

import signal
import asyncio

import aioglib
asyncio.get_event_loop_policy().set_event_loop(aioglib.GLibEventLoop())
asyncio.get_event_loop_policy().set_child_watcher(aioglib.GLibChildWatcher())

# asyncio.get_event_loop_policy().get_event_loop().set_debug(True)
# import logging
# logging.basicConfig(level=logging.DEBUG)

def get_config():
	import importlib.util
	import appdirs
	import os.path
	for p in [appdirs.user_config_dir("icebar.py"), os.path.expanduser("~/icebar.py")]:
		try:
			spec = importlib.util.spec_from_file_location("config", p)
			config = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(config)
			return config
		except (FileNotFoundError, ImportError):
			pass
	else:
		import config
		return config

config = get_config()

style_provider = Gtk.CssProvider()
style_provider.load_from_data(config.CSS.encode())
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def create_strut(win):
	from Xlib import display, Xatom
	mon = Gdk.Display.get_default().get_primary_monitor()
	def update(mon):
		geom = mon.get_geometry()

		disp = display.Display()
		xwin = disp.create_resource_object("window", win.get_window().get_xid())
		xwin.change_property(
			disp.intern_atom("_NET_WM_STRUT"),
			Xatom.CARDINAL,
			32,
			[0,0,0,config.HEIGHT])
		xwin.change_property(
			disp.intern_atom("_NET_WM_STRUT_PARTIAL"),
			Xatom.CARDINAL,
			32,
			[0,0,0,config.HEIGHT, 0,0, 0,0, 0,0, 0,geom.width])
		disp.sync()
	mon.connect("invalidate", update)
	update(mon)

def mkwin():
	w = Gtk.Window()
	w.set_type_hint(Gdk.WindowTypeHint.DOCK)
	w.set_decorated(False)
	w.set_app_paintable(True)
	w.set_visual(Gdk.Screen.get_default().get_rgba_visual())
	w.connect("realize", create_strut)
	return w

def create_window():
	bg = mkwin()
	bg.realize()
	bg.resize(1, config.HEIGHT)
	bg.get_window().set_child_input_shapes()
	bg.set_name("bg")

	fg = mkwin()
	fg.realize()
	fg.get_window().set_override_redirect(True)
	fg.set_name("fg")
	fg.set_transient_for(bg)

	def onresize(*args):
		fg.move(*bg.get_position())
		fg.resize(*bg.get_size())
		bg.get_window().set_child_input_shapes()

	bg.connect("configure-event", onresize)
	bg.connect("show", lambda win: (fg.hide(), fg.show()))
	bg.connect("hide", lambda win: fg.hide())
	bg.connect("destroy", lambda win: fg.destroy())

	return bg, fg

def draw_bg(self, cr, alpha):
	style = self.get_style_context()
	w, h = self.get_allocated_width(), self.get_allocated_height()
	cr.push_group()
	Gtk.render_background(style, cr, 0, 0, w, h)
	cr.pop_group_to_source()
	cr.paint_with_alpha(alpha)

def __main__():
	bg, fg = create_window()
	box = Gtk.Box()
	fg.connect("draw", draw_bg, 1/2)
	bg.connect("draw", draw_bg, 3/4)
	fg.add(box)
	right = []

	def update_seps(_=None):
		lastVisible = False
		for w, sep in right:
			sep.set_visible(lastVisible)
			lastVisible = w.is_visible()

	from widgets import Separator

	for w in config.left():
		box.pack_start(w, False, False, 1)

	for w in config.right():
		sep = Separator()
		right.append((w, sep))
		w.connect("show", update_seps)
		w.connect("hide", update_seps)
		box.pack_end(sep, False, False, 0)
		box.pack_end(w, False, False, 4)

	def set_shape(win, *_):
		box.get_window().set_child_input_shapes()
		fg.get_window().set_child_input_shapes()

	fg.connect("draw", set_shape)

	box.show()
	bg.show()
	fg.show_all()
	update_seps()

	signal.signal(signal.SIGINT, lambda s, f: asyncio.get_event_loop().stop())
	asyncio.get_event_loop().run_forever()

if __name__ == "__main__": __main__()
