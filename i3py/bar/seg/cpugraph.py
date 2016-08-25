import i3py.bar
import i3py.util
import psutil

class CpuGraph(i3py.util.Timer, i3py.bar.Segment):
	data = [0] * 12
	def run(self):
		val = psutil.cpu_percent()
		self.data = self.data[1:] + [val]

	def getOutput(self):
		return i3py.util.braillegraph((round(x / 25) for x in self.data), False)
