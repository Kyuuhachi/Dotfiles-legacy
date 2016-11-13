import i3bar
import i3bar.util
import dbus
import os.path
import urllib.parse
import re
import threading

__all__ = ["Totem"]

TOTEM_BUS = "org.mpris.MediaPlayer2.totem"
TOTEM_OBJECT = "/org/mpris/MediaPlayer2"
TOTEM_IFACE = "org.mpris.MediaPlayer2.Player"
def getBus():
	return dbus.SessionBus().get_object(TOTEM_BUS, TOTEM_OBJECT)

class Totem(i3bar.Segment):
	timeout = threading.Thread()
	def getOutput(self):
		try:
			status = getBus().GetAll(TOTEM_IFACE, dbus_interface=dbus.PROPERTIES_IFACE)
			try:
				title = status["Metadata"]["xesam:title"]
			except KeyError:
				path = urllib.parse.unquote(status["Metadata"]["mpris:trackid"])
				title = os.path.basename(path)
				title = re.sub(r"^[0-9\-]+(\.| -) ", "", title) # Strip leading numbers
				title = re.sub(r"\.[a-z0-9]{3,4}$", "", title) # Strip file extension

			if not self.timeout.isAlive():
				title = re.sub(r"\(.+\)", "", title)
				title = re.sub(r"\s+", " ", title).strip()
				maxlen = 40
				if len(title) > maxlen:
					title = title[:maxlen] + "…"

			playing = status["PlaybackStatus"] == "Playing"

			return "{} {}".format(" ▶"[playing], title)
		except dbus.exceptions.DBusException:
			return None

	def showInfo(self):
		if self.timeout.isAlive():
			self.timeout.interrupt()
		else:
			self.timeout = i3bar.util.Timeout(1, lambda: i3bar.update(self))
			self.timeout.start()

	def click(self, button):
		if button == 1:
			getBus().PlayPause()
		if button == 3:
			self.showInfo()
