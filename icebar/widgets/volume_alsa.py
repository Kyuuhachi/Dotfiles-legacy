from gi.repository import Gtk, GLib
import simplealsa

__all__ = ["AlsaVolume"]

class AlsaVolume(Gtk.EventBox):
	def __init__(self, card="hw:0", name=("Master", "Speaker"), id=0, base=80, spacing=3):
		super().__init__()

		self.icon = Gtk.Label("♪")
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.icon.show()
		self.text.show()
		box.show()
		self.show()

		self.base = base

		self.alsa = simplealsa.Alsa(card)
		self.volume = self.alsa.selem(name[0])
		self.mute = self.alsa.selem(name[1])

		self.min, self.max = self.volume.mB_range

		self.update_volume()
		self.update_mute()
		self.volume.callback(self.update_volume)
		self.mute.callback(self.update_mute)

		def update(*_):
			self.alsa.handle_events()
			return True
		for fd in self.alsa.fds():
			GLib.io_add_watch(fd.fd, GLib.IO_IN, update)

	def update_volume(self, *_):
		self.text.set_text("{:.1f} dB".format(self.volume.mB.all / 100 + self.base))
	def update_mute(self, *_):
		self.set_opacity(1 if self.mute.switch.all else 0.5)
