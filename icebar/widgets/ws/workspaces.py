from gi.repository import Gtk, GObject, Gdk

from enum import IntFlag

class WSState(IntFlag):
	focused = 1
	focused_other = 2
	urgent = 4

__all__ = ["Workspaces", "WSProvider", "WSState"]

class WSProvider(GObject.Object):
	@GObject.Signal(arg_types=[object])
	def color(self, rgb): pass
	@GObject.Signal(arg_types=[object])
	def workspaces(self, workspaces): pass

	def set_workspace(self, name): pass

class Workspaces(Gtk.Box):
	def __init__(self, provider):
		super().__init__(spacing=1)
		self.provider = provider
		self.provider.connect("color", self.update_color)
		self.provider.connect("workspaces", self.update_workspaces)
		self.buttons = {}
		self.active_color = (0, 0, 0, 0)
		self.show()

	def update_color(self, _, color):
		for button in self.buttons.values():
			button.set_color(color)
		self.active_color = color

	def update_workspaces(self, _, workspaces):
		for name in self.buttons:
			self.buttons[name].hide()
		for i, (name, state) in enumerate(workspaces):
			if name not in self.buttons:
				self.buttons[name] = WorkspaceButton(name, self.active_color, visible=True)
				self.buttons[name].connect("activate", lambda button, name: self.provider.set_workspace(name), name)
				self.pack_start(self.buttons[name], False, False, 0)
			self.buttons[name].set_state(state)
			self.buttons[name].show()
			self.reorder_child(self.buttons[name], i)

PADDING = 4

def blend(a, b, r):
	return tuple(a*(1-r) + b*r for (a, b) in zip(a, b))
def alpha(a, r):
	return (a[0], a[1], a[2], a[3] * r)

class WorkspaceButton(Gtk.EventBox):
	@GObject.Signal
	def activate(self): pass

	def __init__(self, name, color, **kwargs):
		super().__init__(**kwargs)
		self.state = 0
		self.color = Gdk.RGBA(*color)

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", self.on_mouse)
		label = Gtk.Label(label=name, visible=True)
		self.add(label)

		self.style = Gtk.CssProvider()
		label.get_style_context().add_provider(self.style, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	def on_mouse(self, _, evt):
		print(evt)
		if (evt.button, evt.type) == (1, Gdk.EventType.BUTTON_PRESS):
			self.emit("activate")

	def set_state(self, state):
		if state != self.state:
			self.state = state
			self.update()

	def set_color(self, color):
		self.color = Gdk.RGBA(*color)
		self.update()

	def update(self):
		bg = self.color.to_string()
		fg = "currentColor"
		bd = "currentColor"

		if ~self.state & WSState.focused:
			bg = f"alpha({bg}, 0)"
		if ~self.state & (WSState.focused | WSState.focused_other):
			fg = f"alpha({fg}, 0.5)"
		bd = f"alpha({bd}, 0.25)"

		if self.state & WSState.urgent:
			urgent = Gdk.RGBA(4/6, 1/6, 1/6).to_string()
			bg = f"mix({bg}, {urgent}, 0.75)"
			fg = f"mix({fg}, {urgent}, 0.25)"
			bd = f"mix({bd}, {urgent}, 0.50)"

		self.style.load_from_data(f"* {{ border: 1px solid transparent; padding: 0 3px; margin: 1px 0; background: {bg}; color: {fg}; border-color: {bd}; }}".encode())
