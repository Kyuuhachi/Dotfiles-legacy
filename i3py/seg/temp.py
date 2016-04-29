import i3py

class Temp(i3py.Segment):
	file = "/sys/class/thermal/thermal_zone0/temp"

	def getOutput(self):
		with open(self.file, "r") as f:
			temp = float(f.read().strip()) / 1000
		out = {}
		out["full_text"] = "%d°C" % round(temp)
		if temp >= 90: out["urgent"] = True
		return out
