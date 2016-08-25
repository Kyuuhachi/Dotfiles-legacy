import i3py.bar
import time

class Clock(i3py.bar.Segment):
	def getOutput(self):
		return time.strftime("%T")
