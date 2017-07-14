import i3bar
import basiciw

__all__ = ["Network"]
class Network(i3bar.Segment):
	def __init__(self, interface):
		self.interface = interface

	def getOutput(self):
		out = {}
		ssid = basiciw.iwinfo(self.interface)["essid"]
		if ssid == "":
			ssid = "DOWN"
			out["urgent"] = True
		out["full_text"] = " {}".format(ssid)
		return out
