from gi.repository import Gtk, Gdk, Keybinder
import os
import dbus
import util

__all__ = ["Volume"]

PROPS = "org.freedesktop.DBus.Properties"

import ctypes
DLL = ctypes.CDLL("libpulse.so.0")
volume_to_db = DLL.pa_sw_volume_to_dB
volume_to_db.argtypes = (ctypes.c_uint32,)
volume_to_db.restype = ctypes.c_double
volume_from_db = DLL.pa_sw_volume_from_dB
volume_from_db.argtypes = (ctypes.c_double,)
volume_from_db.restype = ctypes.c_uint32

VOLUME_NORM = volume_from_db(0)
VOLUME_UI_MAX = volume_from_db(11)

LABEL_FORMAT = "<small>{:+.1f} dB</small>"

def pulse_bus_address():
	if 'PULSE_DBUS_SERVER' in os.environ:
		address = os.environ['PULSE_DBUS_SERVER']
	else:
		bus = dbus.SessionBus()
		server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
		address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface=PROPS)
	return address

class Volume(Gtk.EventBox):
	def __init__(self, keys=False, spacing=3):
		super().__init__()

		self.icon = Gtk.Label()
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.icon.show()
		self.text.show()
		box.show()
		self.show()

		self.build_popup()

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.click)

		self.pulse_bus = dbus.connection.Connection(pulse_bus_address())
		self.pulse_core = self.pulse_bus.get_object(None, "/org/pulseaudio/core1")

		self.pulse_core.ListenForSignal("org.PulseAudio.Core1.FallbackSinkUpdated", [self.pulse_core], dbus_interface="org.PulseAudio.Core1")
		self.pulse_core.ListenForSignal("org.PulseAudio.Core1.FallbackSinkUnset", [self.pulse_core], dbus_interface="org.PulseAudio.Core1")

		self.default_sink = None
		self.updateSink(self.pulse_core.Get("org.PulseAudio.Core1", "FallbackSink", dbus_interface=PROPS))

		self.pulse_bus.add_signal_receiver(self.updateSink, "FallbackSinkUpdated")
		self.pulse_bus.add_signal_receiver(self.unsetSink, "FallbackSinkUnset")
		self.pulse_bus.add_signal_receiver(self.updateVolume, "VolumeUpdated")
		self.pulse_bus.add_signal_receiver(self.updateMute, "MuteUpdated")

		if keys:
			Keybinder.bind("AudioMute", self.toggleMute)
			Keybinder.bind("AudioRaiseVolume", self.changeVolume, +5)
			Keybinder.bind("AudioLowerVolume", self.changeVolume, -5)

	def build_popup(self):
		self.label = Gtk.Label()
		self.slider = Gtk.Scale()
		self.slider.set_draw_value(False)
		self.slider.set_range(0, VOLUME_UI_MAX)
		self.slider.set_increments(VOLUME_NORM/100, VOLUME_NORM/20)
		self.slider.add_mark(VOLUME_NORM, Gtk.PositionType.RIGHT, "")
		self.slider.connect("change-value", self.changeSlider)
		self.button = Gtk.ToolButton()
		self.button.set_halign(Gtk.Align.CENTER)
		self.button.connect("clicked", self.toggleMute)

		self.slider.set_orientation(Gtk.Orientation.VERTICAL)
		self.slider.set_inverted(True)
		self.slider.set_size_request(0, 150)
		box = Gtk.Box()
		box.set_orientation(Gtk.Orientation.VERTICAL)
		box.pack_start(self.label, False, False, 0)
		box.pack_start(self.slider, True, True, 0)
		box.pack_start(self.button, False, False, 0)
		self.popup = util.make_popup(util.framed(box), self)

	def unsetSink(self):
		if self.default_sink:
			self.pulse_core.StopListeningForSignal("org.PulseAudio.Core1.Device.VolumeUpdated", dbus_interface="org.PulseAudio.Core1")
			self.pulse_core.StopListeningForSignal("org.PulseAudio.Core1.Device.MuteUpdated", dbus_interface="org.PulseAudio.Core1")

	def updateSink(self, sink):
		self.unsetSink()
		self.default_sink = self.pulse_bus.get_object(None, sink)
		self.pulse_core.ListenForSignal("org.PulseAudio.Core1.Device.VolumeUpdated", [self.default_sink], dbus_interface="org.PulseAudio.Core1")
		self.pulse_core.ListenForSignal("org.PulseAudio.Core1.Device.MuteUpdated", [self.default_sink], dbus_interface="org.PulseAudio.Core1")
		self.updateVolume(self.default_sink.Get("org.PulseAudio.Core1.Device", "Volume", dbus_interface=PROPS))
		self.updateMute(self.default_sink.Get("org.PulseAudio.Core1.Device", "Mute", dbus_interface=PROPS))

	def updateVolume(self, vol):
		self.text.set_text("{:.0f}%".format(100 * max(vol) / VOLUME_NORM))
		self.icon.set_text("♪")
		self.slider.set_value(max(vol))
		self._updatePopup()

	def updateMute(self, mute):
		self.set_opacity(0.5 if mute else 1)
		self.button.set_icon_name("audio-volume-muted" if mute else "audio-volume-high")

	def click(self, _, evt):
		if (evt.button, evt.type) == (1, Gdk.EventType.BUTTON_PRESS):
			if self.popup.is_visible():
				self.popup.hide()
			else:
				self.popup.show_all()

	def _updatePopup(self):
		self.label.set_markup(LABEL_FORMAT.format(volume_to_db(int(self.slider.get_value()))))

	def changeSlider(self, w, mode, val):
		a = w.get_adjustment()
		if val < a.get_lower(): val = a.get_lower()
		if val > a.get_upper(): val = a.get_upper()
		val = round(val / VOLUME_NORM * 100) * VOLUME_NORM / 100
		self.default_sink.Set("org.PulseAudio.Core1.Device", "Volume", dbus.Array([int(val)], "u"), dbus_interface=PROPS)

	def toggleMute(self, _):
		self.default_sink.Set("org.PulseAudio.Core1.Device", "Mute", not self.default_sink.Get("org.PulseAudio.Core1.Device", "Mute", dbus_interface=PROPS), dbus_interface=PROPS)

	def changeVolume(self, _, d):
		val = max(self.default_sink.Get("org.PulseAudio.Core1.Device", "Volume", dbus_interface=PROPS))
		val = round(val / VOLUME_NORM * 100 + d) * VOLUME_NORM / 100
		if val < 0: val = 0
		self.default_sink.Set("org.PulseAudio.Core1.Device", "Volume", dbus.Array([int(val)], "u"), dbus_interface=PROPS)
