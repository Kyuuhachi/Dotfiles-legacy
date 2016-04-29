import i3py
from i3py import util
import psutil

class CpuGraph(util.Timer, i3py.Segment):
	data = [0] * 12
	def run(self):
		val = psutil.cpu_percent()
		self.data = self.data[1:] + [val]

	def getOutput(self):
		return util.braillegraph((round(x / 25) for x in self.data), False)
