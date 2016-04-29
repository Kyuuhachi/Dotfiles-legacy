import i3py
import basiciw

class Network(i3py.Segment):
	file = "/sys/class/net/wlan0/operstate"
	def getOutput(self):
		up = False
		with open(self.file) as f:
			up = f.read().strip() == "up"

		if not up:
			return {"full_text": "wlan0: DOWN", "urgent": True}

		iwi = basiciw.iwinfo("wlan0")
		ssid = iwi["essid"]
		quality = iwi["quality"]["quality"] / iwi["quality"]["quality_max"] * 100
		return "%s (%d%%)" % (ssid, round(quality))
