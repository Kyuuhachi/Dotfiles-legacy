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
from icebar.lib import aioglib
asyncio.get_event_loop_policy().set_event_loop(aioglib.GLibEventLoop())
asyncio.get_event_loop_policy().set_child_watcher(aioglib.GLibChildWatcher())

import importlib.util
import appdirs
from pathlib import Path
from icebar.widgets import Separator

# asyncio.get_event_loop_policy().get_event_loop().set_debug(True)
# import logging
# logging.basicConfig(level=logging.DEBUG)

def get_config():
	p = Path(appdirs.user_config_dir("icebar.py"))
	spec = importlib.util.spec_from_file_location("config", p)
	config = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(config)
	return config

config = get_config()

style_provider = Gtk.CssProvider()
style_provider.load_from_data(config.CSS.encode())
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def set_strut(gdkwin: Gtk.Window):
	from Xlib import display, Xatom
	height = gdkwin.get_height()
	width = Gdk.Display.get_default().get_monitor_at_window(gdkwin).get_geometry().width

	disp = display.Display()
	xwin = disp.create_resource_object("window", gdkwin.get_xid())
	xwin.change_property(
		disp.intern_atom("_NET_WM_STRUT"),
		Xatom.CARDINAL, 32,
		[0,0,0,height])
	xwin.change_property(
		disp.intern_atom("_NET_WM_STRUT_PARTIAL"),
		Xatom.CARDINAL, 32,
		[0,0,0,height, 0,0, 0,0, 0,0, 0,width])
	disp.sync()
	disp.close()
	print(height, width)

def mkwin():
	w = Gtk.Window(type_hint=Gdk.WindowTypeHint.DOCK, decorated=False, app_paintable=True)
	w.set_visual(Gdk.Screen.get_default().get_rgba_visual())
	w.resize(1, 1)
	w.realize()
	return w

def create_window():
	bg = mkwin()

	fg = mkwin()
	fg.get_window().set_override_redirect(True)
	fg.set_transient_for(bg)

	def on_bg_configure(win, evt):
		fg.move(*bg.get_position())
		fg.resize(bg.get_size()[0], 1)
	def on_fg_configure(win, evt):
		bg.resize(1, fg.get_size()[1])
		set_strut(bg.get_window())

	bg.connect("configure-event", on_bg_configure)
	fg.connect("configure-event", on_fg_configure)

	bg.connect("show", lambda win: fg.show())
	bg.connect("hide", lambda win: fg.hide())
	bg.connect("destroy", lambda win: fg.destroy())

	return bg, fg

def main():
	print("icebar!")
	bg, fg = create_window()
	bg_box = Gtk.Box(name="bg", visible=True)
	bg.add(bg_box)

	fg_box = Gtk.Box(name="fg", visible=True)
	fg.add(fg_box)
	right = []

	def update_seps(_=None):
		lastVisible = False
		for w, sep in right:
			sep.set_visible(lastVisible)
			lastVisible = w.is_visible()

	for w in config.left():
		fg_box.pack_start(w, False, False, 1)

	for w in config.right():
		sep = Separator()
		right.append((w, sep))
		w.connect("show", update_seps)
		w.connect("hide", update_seps)
		fg_box.pack_end(sep, False, False, 0)
		fg_box.pack_end(w, False, False, 4)

	def set_shape(win, *_):
		fg_box.get_window().set_child_input_shapes()
		fg.get_window().set_child_input_shapes()

	fg.connect("draw", set_shape)

	bg.show()
	update_seps()

	signal.signal(signal.SIGINT, lambda s, f: asyncio.get_event_loop().stop())
	asyncio.get_event_loop().run_forever()
