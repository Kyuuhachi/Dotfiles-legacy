from gi.repository import Gtk
import cairo
import util

__all__ = ["Separator"]

class Separator(Gtk.DrawingArea):
	def __init__(self):
		super().__init__()
		self.connect("draw", self.draw)
		self.set_size_request(1, 0)

	def draw(self, _, ctx):
		ctx.set_antialias(cairo.ANTIALIAS_NONE)
		ctx.set_line_width(self.get_allocated_width())
		ctx.set_line_join(cairo.LINE_JOIN_BEVEL)
		ctx.set_line_cap(cairo.LINE_CAP_BUTT)

		style = self.get_style_context()
		color = style.get_color(style.get_state())
		color.alpha /= 4

		font_height = util.get_height(self)
		height = self.get_allocated_height()
		ctx.translate(0, (height - font_height) / 2)

		ctx.set_source_rgba(*color)
		ctx.move_to(1, 0)
		ctx.line_to(1, font_height)
		ctx.stroke()

		self.get_window().set_child_input_shapes()
