import i3bar
import time
import subprocess

__all__ = ["Clock"]
class Clock(i3bar.Segment):
	def getOutput(self):
		return time.strftime("%T")

	def click(self, button, name):
		if button == 1:
			subprocess.Popen(["gsimplecal"])
