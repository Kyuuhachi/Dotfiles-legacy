import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import neovim
import urllib.parse

_callback = sys.argv[1]

nvim = neovim.attach("stdio")
DBusGMainLoop(set_as_default=True)
def sync(file, pos, time):
	try:
		file = urllib.parse.urlparse(file)
		if file.scheme != "file": return
		file = file.path
		if not nvim.call("bufexists", file):
			return
		bufnr = nvim.call("bufnr", nvim.call("bufname", file))

		win = findViableWindow(nvim, bufnr, nvim.current.tabpage)
		if win:
			r, c = int(pos[0]), int(pos[1])
			win.cursor = (r, c+1)
			nvim.command(f"tabn {win.tabpage.number}")
	except Exception as e:
		nvim.command(f"echom {str(e)!r}")

def findViableWindow(nvim, bufnr, tab):
	viable = None
	for win in nvim.windows:
		if win.buffer.number == bufnr:
			if win.tabpage.number == tab:
				return win
			if not viable:
				viable = win
	return viable

dbus.SessionBus().add_signal_receiver(sync, signal_name="SyncSource", dbus_interface="org.gnome.evince.Window")
GLib.MainLoop().run()
