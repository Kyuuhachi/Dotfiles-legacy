import i3py.bar
from psutil import virtual_memory

class Ram(i3py.bar.Segment):
	def getOutput(self):
		mem = virtual_memory()
		out = {}
		out["full_text"] = "{:.1f} MB".format((mem.used - mem.cached - mem.buffers) / 1024**2)
		if mem.percent >= 75: out["urgent"] = True
		return out
