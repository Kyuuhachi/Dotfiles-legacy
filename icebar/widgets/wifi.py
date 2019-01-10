from gi.repository import Gtk, GLib
from simplewifi import wifi_status

__all__ = ["Wifi"]
class Wifi(Gtk.EventBox):
	def __init__(self, *, spacing=3):
		super().__init__()

		self.icon = Gtk.Label()
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.tooltip = Gtk.Grid()
		n = 0
		def row(l):
			nonlocal n
			left = Gtk.Label(l, xalign=0)
			right = Gtk.Label(xalign=1)
			self.tooltip.attach(left, 0, n, 1, 1)
			self.tooltip.attach(right, 1, n, 1, 1)
			n += 1
			return right
		self.tt_name = row("Name")
		self.tt_ssid = row("SSID")
		self.tt_quality = row("Quality")
		self.tt_ipv4 = row("IPv4")
		self.tt_ipv6 = row("IPv6")
		self.tt_mac = row("MAC")
		self.tooltip.show_all()

		def tooltip(self, x, y, keyboard, tooltip):
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)

		GLib.timeout_add_seconds(1, self.update)
		self.update()

		self.icon.show()
		self.text.show()
		box.show()
		self.show()

	def update(self):
		for (name, up, essid, quality, ipv4, ipv6, mac) in wifi_status():
			if essid is not None:
				break
		else:
			(name, up, essid, quality, ipv4, ipv6, mac) = (None,) * 7

		if up is not None and essid is not None:
			self.set_opacity(1)
			self.set_has_tooltip(True)
			self.tt_name.set_text(name)
			self.tt_ssid.set_text(essid)
			self.tt_quality.set_text("{}%".format(quality or 0))
			self.tt_ipv4.set_text(ipv4 or "-")
			self.tt_ipv6.set_text(ipv6 or "-")
			self.tt_mac.set_text(mac or "-")
		else:
			self.set_opacity(0.5)
			self.set_has_tooltip(False)

		self.icon.set_text({None: "", False:"", True: ""}[up])
		self.text.set_text({None: "ERROR", False: "OFF", True: essid or "DOWN"}[up])

		return True
