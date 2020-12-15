from gi.repository import Gtk

IMAGE_SIZE = 48

css = """
#notification {
	background-color: rgba(0,0,0,0.7);
	border-radius: .5em;
	margin-top: .5em;
	margin-left: .5em;
	margin-right: .5em;
	padding: .5em;
	min-width: 37em;
}

#title {
	font-weight: bold;
	font-size: 125%;
}

#image {
	padding-right: .5em;
}

#actions {
	border-left: 1px solid rgba(255,255,255,0.3);
	padding-left: .5em;
}

button {
	padding: 0;
	min-width: 0;
	background: none;
	border: none;
}
button:not(:hover) {
	opacity: 0.4;
	border: none;
}

* {
	color: white;
}
"""

capabilities = ["actions", "body", "icon-static"]

def box(vert, *children, **kwargs):
	box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL if vert else Gtk.Orientation.HORIZONTAL, visible=True, **kwargs)
	for i, ch in children:
		box.pack_start(ch, i, i, 0)
	return box

def ebox(w, **kwargs):
	ebox = Gtk.EventBox(visible=True, **kwargs)
	ebox.add(w)
	return ebox

def show(win, data):
	title = Gtk.Label(name="title", xalign=0, valign=0)
	title.set_line_wrap(True)
	if "title" in data:
		title.show()
		title.set_text(data["title"])

	body = Gtk.Label(name="body", xalign=0, valign=0)
	body.set_line_wrap(True)
	if "body" in data:
		body.show()
		body.set_text(data["body"])

	if "image" in data:
		image = data["image"]
		image.set_name("image")
	else:
		image = Gtk.Invisible()

	close = Gtk.Button(
		name="close",
		halign=Gtk.Align.END,
		visible=True,
		relief=Gtk.ReliefStyle.NONE,
		image=Gtk.Image.new_from_icon_name("window-close", Gtk.IconSize.BUTTON),
	)

	actions = Gtk.Box(name="actions", orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.END)
	actions.get_style_context().add_class("linked")

	b = box(False,
		(0, image),
		(1, box(True,
			(0, title),
			(0, body),
		)),
		(0, box(True,
			(0, ebox(close)),
			(1, actions),
		)),
	)
	b.set_name("notification")

	if "actions" in data:
		actions.show()
		for k, v in data["actions"].items():
			btn = Gtk.Button(label=k, visible=True, relief=Gtk.ReliefStyle.NONE)
			btn.connect("clicked", v)
			btn.get_style_context().add_class("action")
			actions.pack_start(ebox(btn), False, False, 0)

	close.connect("clicked", data["close"])

	win.connect("draw", lambda w, a: w.get_window().set_child_input_shapes())
	win.add(b)
