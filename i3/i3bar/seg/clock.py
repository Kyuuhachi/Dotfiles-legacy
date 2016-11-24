import i3bar
import time

__all__ = ["Clock"]
class Clock(i3bar.Segment):
	def getOutput(self):
		return time.strftime("%T")
