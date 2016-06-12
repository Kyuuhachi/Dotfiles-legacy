import i3py
import basiciw

class Network(i3py.Segment):
	name = "wlan0"

	def getOutput(self):
		out = {}
		ssid = basiciw.iwinfo(self.name)["essid"]
		if ssid == None:
			ssid = "DOWN"
			out["urgent"] = True
		out["full_text"] = "{}: {}".format(self.name, ssid)
		return out
