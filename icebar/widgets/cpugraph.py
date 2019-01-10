from gi.repository import Gtk, GLib
import cairo
import util

from collections import namedtuple
Sample = namedtuple("Sample", "user system iowait")

__all__ = ["CPUGraph"]

class CPUGraph(Gtk.DrawingArea):
	def __init__(self, width=50, interval=100):
		super().__init__()
		self.last_cpu = None
		self.samples = [Sample(0, 0, 0)] * width
		self.cores = 1

		GLib.timeout_add(interval, self.update)
		self.connect("draw", self.draw)
		self.set_size_request(width, 0)

	def update(self):
		import psutil
		cpu = psutil.cpu_times()
		self.cores = psutil.cpu_count()
		if self.last_cpu:
			tot = (psutil._cpu_tot_time(cpu) - psutil._cpu_tot_time(self.last_cpu)) or 1e10 # Sometimes zero, so set it to something huge
			self.samples.pop(0)
			self.samples.append(Sample(
				(cpu.user - self.last_cpu.user) / tot,
				(cpu.system - self.last_cpu.system) / tot,
				(cpu.iowait - self.last_cpu.iowait) / tot,
			))
		self.last_cpu = cpu
		self.queue_draw()
		return True

	def draw(self, _, ctx):
		ctx.set_antialias(cairo.ANTIALIAS_NONE)
		ctx.set_line_width(1)
		ctx.set_line_join(cairo.LINE_JOIN_BEVEL)
		ctx.set_line_cap(cairo.LINE_CAP_BUTT)

		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())

		font_height = util.get_height(self)
		height = self.get_allocated_height()
		ctx.translate(0, (height - font_height) // 2 + 1)

		ctx.set_source_rgba(r, g, b, a/6)
		h = font_height-1
		for n in range(self.cores+1):
			y = int(n/self.cores*h)
			ctx.move_to(0, y)
			ctx.line_to(self.get_allocated_width(), y)
		ctx.stroke()

		def draw_graph(f):
			i = enumerate(map(lambda y: int((1-f(y))*h), self.samples))
			py = 0
			for x, y in i:
				if py - y > 1:
					ctx.line_to(x-1, y+1)
				if py - y < -1:
					ctx.line_to(x-1, y-1)
				ctx.line_to(x, y)
				py = y
			ctx.stroke()

		ctx.set_source_rgba((r+1)/2, (g+0)/2, (b+0)/2, a/2)
		draw_graph(lambda a: a.iowait)

		ctx.set_source_rgba(r, g, b, a/2)
		draw_graph(lambda a: a.system)

		ctx.set_source_rgba(r, g, b, a)
		draw_graph(lambda a: a.user)
