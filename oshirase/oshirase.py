from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import dbus
import dbus.service
import signal
import urllib.parse
from dataclasses import dataclass

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

import config

style_provider = Gtk.CssProvider()
style_provider.load_from_data(config.css.encode())
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

@dataclass
class Notification:
	window: Gtk.Window
	timeout: int
	timeout_id: int

class Oshirase(dbus.service.Object):
	def __init__(self, *args):
		super().__init__(*args)
		self.notif = {}
		self.timeout = {}
		self.timeout_id = {}
		self.id = 0

	@dbus.service.method("org.freedesktop.Notifications", in_signature="", out_signature="ssss")
	def GetServerInformation(self): # -> (name, vendor, version, spec_version)
		return "Oshirase", "Kyuuhachi", "0.1", "1.1"

	@dbus.service.method("org.freedesktop.Notifications", in_signature="", out_signature="as")
	def GetCapabilities(self): # -> (caps)
		return ["actions", "action-icons", "body", "body-hyperlinks", "body-markup", "icon-static"]

	@dbus.service.method("org.freedesktop.Notifications", in_signature="u", out_signature="")
	def CloseNotification(self, id): # -> ()
		self.NotificationClosed(id, 3)

	@dbus.service.signal("org.freedesktop.Notifications", signature="uu")
	def NotificationClosed(self, id, reason):
		try:
			if id in self.notif:
				self.notif.pop(id).destroy()
				self.reflow()
			if id in self.timeout:
				del self.timeout[id]
		except Exception:
			import traceback
			traceback.print_exc()
			raise

	@dbus.service.method("org.freedesktop.Notifications", in_signature="susssasa{sv}i", out_signature="u")
	def Notify(self, app_name, id, icon, summary, body, actions, hints, timeout): # -> (id)
		try:
			if id == 0:
				self.id += 1
				id = self.id

			if timeout == -1:
				timeout = [3500, 5000, 0][hints.get("urgency", 0)]
			if timeout != 0:
				self.timeout[id] = timeout
				self.startTimeout(id)

			data = {}
			if app_name: data["app_name"] = str(app_name)
			if summary:  data["title"] = str(summary)
			if body:     data["body"] = str(body)

			if actions:
				data["actions"] = {}
				for action, name in zip(*[map(str, actions)]*2):
					data["actions"][name] = lambda *a, action=action: self.ActionInvoked(id, action)
			data["close"] = lambda *a: self.NotificationClosed(id, 2)

			hints["icon"] = icon
			if image := get_image(hints):
				image.show()
				data["image"] = image
			for key in ["image-data", "image_data", "icon_data", "icon", "image-path", "image_path"]:
				if key in hints:
					del hints[key]

			for k, v in hints.items():
				k = str(k)
				if   isinstance(v, dbus.Boolean): v = bool(v)
				elif isinstance(v, dbus.Int64):   v = int(v)
				elif isinstance(v, dbus.Int32):   v = int(v)
				elif isinstance(v, dbus.Int16):   v = int(v)
				elif isinstance(v, dbus.Byte):    v = int(v)
				elif isinstance(v, dbus.String):  v = str(v)
				else: raise ValueError(k, v)
				data[k] = v

			print(data)
			if id not in self.notif:
				win = Gtk.Window(type_hint=Gdk.WindowTypeHint.NOTIFICATION, decorated=False, app_paintable=True)
				win.set_visual(Gdk.Screen.get_default().get_rgba_visual())
				win.realize()
				win.get_window().set_override_redirect(True)

				win.connect("enter-notify-event", lambda *a: self.stopTimeout(id))
				win.connect("leave-notify-event", lambda *a: self.startTimeout(id))
				self.notif[id] = win

			win = self.notif[id]
			config.show(win, data)
			win.resize(1,1)
			self.reflow()

			return id
		except Exception:
			import traceback
			traceback.print_exc()
			raise

	@dbus.service.signal("org.freedesktop.Notifications", signature="us")
	def ActionInvoked(self, id, action): pass

	def reflow(self):
		d = Gdk.Display.get_default()
		ys = {}
		for win in self.notif.values():
			mon = d.get_monitor_at_window(win.get_window())
			w = mon.get_geometry().width * mon.get_scale_factor()
			size = win.get_size()
			y = ys.get(mon, 0)
			win.get_window().move_resize(w - size.width, y, size.width, size.height)
			win.show()

			ys[mon] = y + size.height

	def stopTimeout(self, id):
		if id in self.timeout_id:
			GLib.source_remove(self.timeout_id.pop(id))

	def startTimeout(self, id):
		self.stopTimeout(id)
		if id in self.timeout:
			self.timeout_id[id] = GLib.timeout_add(self.timeout[id], lambda *a: self.NotificationClosed(id, 2))

def get_image(hints):
	def from_pixbuf(pixbuf):
		width, height = pixbuf.get_width(), pixbuf.get_height()
		factor = config.IMAGE_SIZE / max(width, height)
		if factor < 1:
			pixbuf = pixbuf.scale_simple(width * factor, height * factor, GdkPixbuf.InterpType.BILINEAR)
		return Gtk.Image.new_from_pixbuf(pixbuf)
	for key in ["image-data", "image_data", "icon_data"]:
		if key in hints:
			(width, height, rowstride, hasalpha, bits, nchan, buf) = hints[key]
			return from_pixbuf(Pixbuf.new_from_bytes(GLib.Bytes(buf), GdkPixbuf.Colorspace.RGB, hasalpha, bits, width, height, rowstride))

	for key in ["icon", "image-path", "image_path"]:
		if key in hints:
			icon = hints[key]
			if icon.startswith("file://"):
				return from_pixbuf(Pixbuf.new_from_file(urllib.parse.unquote(icon[7:])))
			elif icon.startswith("/"):
				return from_pixbuf(Pixbuf.new_from_file(icon))
			elif icon:
				return Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG)

session_bus = dbus.SessionBus()
busname = dbus.service.BusName("org.freedesktop.Notifications", session_bus)
service = Oshirase(session_bus, "/org/freedesktop/Notifications")

signal.signal(signal.SIGINT, lambda s, f: Gtk.main_quit())
Gtk.main()
