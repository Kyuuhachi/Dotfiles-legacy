import i3py
import time

class Clock(i3py.Segment):
	def getOutput(self):
		return time.strftime("%T")
