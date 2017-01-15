#!/usr/bin/env python3
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
DBusGMainLoop(set_as_default=True)

interface = 'org.gnome.SessionManager'
object = '/org/gnome/SessionManager'

class SessionManager(dbus.service.Object):
	def __init__(self):
		dbus.service.Object.__init__(self, dbus.service.BusName(interface, bus=dbus.SessionBus()), object)

	@dbus.service.method(dbus_interface=interface, in_signature="susu", out_signature="u")
	def Inhibit(self, app_id, toplevel_xid, reason, flags):
		return 0

sessmgr = SessionManager()

loop = GLib.MainLoop()
loop.run()
