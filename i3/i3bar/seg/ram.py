import i3bar
from psutil import virtual_memory

__all__ = ["Ram"]
class Ram(i3bar.Segment):
	def getOutput(self):
		mem = virtual_memory()
		out = {}
		out["full_text"] = "{:.1f} MB".format(mem.used / 1024**2)
		if mem.percent >= 75:
			out["urgent"] = True
		return out
