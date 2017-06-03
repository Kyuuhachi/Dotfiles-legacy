import i3bar

__all__ = ["Temp"]
class Temp(i3bar.Segment): # TODO use psutil
	file = "/sys/class/thermal/thermal_zone0/temp"

	def getOutput(self):
		with open(self.file, "r") as f:
			temp = float(f.read().strip()) / 1000
		return {
			"full_text": "{}°C".format(round(temp)),
			"urgent": temp >= 90
		}
