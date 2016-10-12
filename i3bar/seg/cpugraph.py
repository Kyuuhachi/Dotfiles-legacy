import i3bar
import i3bar.util
import psutil

__all__ = ["CpuGraph"]
class CpuGraph(i3bar.util.Timer, i3bar.Segment):
	interval = 1

	data = [0] * 12
	def run(self):
		val = psutil.cpu_percent()
		self.data = self.data[1:] + [val]

	def getOutput(self):
		return braillegraph((round(x / 25) for x in self.data), False)

def group(data, count=2, default=None):
	it = iter(data)
	while True:
		out = [default] * count
		for n in range(0, count):
			try:
				out[n] = next(it)
			except StopIteration:
				if n:
					yield tuple(out)
				raise
		yield tuple(out)

def braille(bits):
	idx = [6, 2, 1, 0, 7, 5, 4, 3]
	char = 0x2800
	for i in range(8):
		if bits & 1 << i:
			char |= 1 << idx[i]
	return chr(char)

def braillegraph(data, fill=False):
	def fillFunc(x):
		return ((1 << x) - 1) & 15
	def topFunc(x):
		n = fillFunc(x)
		return n & ~(n >> 1)
	func = [topFunc, fillFunc][fill]

	return "".join([
		braille(a | b << 4)
		for a, b in group(map(func, data), 2, 0)
	])
