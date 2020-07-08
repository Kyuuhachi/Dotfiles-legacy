from gi.repository import Gtk, GLib
import tempfile
import asyncio
import os
import os.path
import re
rx = re.compile(r"#(.+) #(.+)# -> #(.+)#(?: (.+))?".replace("#", r"\x1B\[[0-9;]*m"))

__all__ = ["Pacman"]

class Pacman(Gtk.EventBox):
	def __init__(self, timeout=3600, spacing=3):
		super().__init__()

		self.icon = PacmanIcon(visible=True)
		self.text = Gtk.Label(visible=True)
		box = Gtk.Box(spacing=spacing, visible=True)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.tooltip = Gtk.Label(visible=True)
		self.tooltip.set_line_wrap(True)
		self.set_has_tooltip(True)

		def tooltip(self, x, y, keyboard, tooltip):
			self.tooltip.set_text(", ".join(f"({name})" if ign else name for (name, _, _, ign) in self.updates))
			tooltip.set_custom(self.tooltip)
			return True
		self.connect("query-tooltip", tooltip)

		GLib.timeout_add_seconds(timeout, self.update)
		self.update()

	def update(self):
		async def subproc(cmd):
			proc = await asyncio.create_subprocess_exec(
				*cmd,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.DEVNULL)
			(out, _) = await proc.communicate()
			return out.decode(errors="surrogateescape")

		async def doUpdate():
			with tempfile.TemporaryDirectory(prefix="icebar-pacman-") as d:
				dbpath = await subproc(["pacman-conf", "DBPath",])
				os.symlink(
					os.path.join(dbpath.rstrip("\n"), "local"),
					os.path.join(d, "local"),
				)

				await subproc([
					"fakeroot", "--",
					"pacman", "-Sy",
					"--dbpath", d,
					"--logfile", "/dev/null",
				])

				data = await subproc([
					"pacman", "-Qu",
					"--dbpath", d,
					"--logfile", "/dev/null",
					"--color", "always",
				])
				self.updates = [rx.match(line).groups() for line in data.splitlines()]
				count = sum(1 for (_, _, _, ign) in self.updates if not ign)
				self.set_visible(count)
				self.text.set_text(str(count))
				
		asyncio.ensure_future(doUpdate())
		return True

class PacmanIcon(Gtk.DrawingArea):
	def do_draw(self, ctx):
		style = self.get_style_context()
		r, g, b, a = style.get_color(style.get_state())
		ctx.set_source_rgba(r, g, b, a)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		fontsize = (metrics.get_ascent() - metrics.get_descent()) / 1024
		pos = (self.get_allocated_height() - fontsize) // 2
		ctx.translate(0, pos)

		def path(pts):
			ctx.new_sub_path()
			for x, y in pts:
				ctx.line_to(x, y)
			ctx.close_path()

		t = max(1, fontsize//8)
		self.set_size_request(t*10, t*10)
		ctx.scale(t,t)

		ctx.translate(5, 0)

		path([ (1,0), (1,4), (4,4), (0,8), (-4,4), (-1,4), (-1,0) ])
		path([ (-5,10), (-5,7), (-2,7), (0,9), (2,7), (5,7), (5,10) ])

		ctx.fill()
