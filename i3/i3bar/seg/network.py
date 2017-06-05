import i3bar
import basiciw

__all__ = ["Network"]
class Network(i3bar.Segment):
	name = "wlan0"

	def getOutput(self):
		out = {}
		ssid = basiciw.iwinfo(self.name)["essid"]
		if ssid == "":
			ssid = "DOWN"
			out["urgent"] = True
		out["full_text"] = " {}".format(ssid)
		return out
