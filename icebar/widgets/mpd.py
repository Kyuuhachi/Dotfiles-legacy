from gi.repository import Gtk, Gdk, Pango, Keybinder
import cairo
import os
import os.path
import asyncio
import re
import enum
import util

class MPDClosedError(Exception): pass
class MPDError(Exception): pass

host = os.getenv("MPD_HOST", "localhost")
port = os.getenv("MPD_PORT", None)

class MpdClient:
	async def __aenter__(self):
		try:
			r, w = await asyncio.open_unix_connection(host)
		except ConnectionRefusedError:
			raise MPDClosedError("Couldn't connect to MPD")
		if await r.readline() != b'OK MPD 0.20.0\n':
			raise MPDClosedError("Wrong magic!")
		self.r, self.w = r, w
		return self

	async def __aexit__(self, exc_type, exc, tb):
		self.w.write_eof()

	async def send(self, command, *args):
		escape = lambda s: "".join("\\"[c not in '\\"':] + c for c in s)
		words = [command] + [f'"{escape(a)}"' for a in args]
		self.w.write(" ".join(words).encode() + b"\n")

	async def recv(self):
		response = []
		while True:
			data = await self.r.readline()
			if not data and self.r.at_eof():
				raise MPDClosedError("Connection closed")
			line = data.decode().rstrip("\n")
			if line.startswith("ACK "):
				raise MPDError(line)
			if line == "OK":
				return response
			response.append(tuple(line.split(": ", 1)))

	async def __call__(self, *command):
		await self.send(*command)
		return await self.recv()

	async def list(self, commands):
		for command in commands:
			await self.send(*command)
		return await self.recv()

__all__ = ["MPD2"]

def stripfname(title, num=False):
	title = os.path.basename(title)
	if not num:
		title = re.sub(r"^[0-9\-]+(\.| -) ", "", title) # Strip leading numbers ("xx. " and "xx - ") (and also "x-xx - " for multiparts)
	title = re.sub(r"\.[^.]+?$", "", title) # Strip file extension
	return title

def gettitle(track, num=False):
	if "Title" in track:
		title = track["Title"]
		if num and "Track" in track:
			title = f"{track['Track']} - {track['Title']}"
		else:
			title = track["Title"]
	elif "file" in track:
		title = stripfname(track["file"], num=num)
	else:
		title = "<Unknown>"
	return title

class MpdState(enum.IntEnum):
	error = 0
	stop = 1
	pause = 2
	play = 3

def run_mpd(f, *args):
	async def coro():
		async with MpdClient() as mpd:
			return await f(mpd, *args)
	return asyncio.ensure_future(coro())

def run_mpd_sync(f, *args):
	async def coro():
		async with MpdClient() as mpd:
			return await f(mpd, *args)
	return asyncio.get_event_loop().run_until_complete(coro())

class save_state:
	def __init__(self, mpd):
		self.mpd = mpd
	async def __aenter__(self):
		self.status = dict(await self.mpd("status"))
		print(self.status)
		return self.status

	async def __aexit__(self, exc_type, exc, tb):
		await self.mpd.list([
			{
				"stop": ["stop"],
				"pause": ["pause", "1"],
				"play": ["pause", "0"],
			}[self.status["state"]],
			["repeat", self.status["repeat"]],
			["random", self.status["random"]],
			["single", self.status["single"]],
			["consume", self.status["consume"]],
		])

async def do_toggle(mpd):
	state = dict(await mpd("status"))["state"]
	if state != "play":
		await mpd("play")
	else:
		await mpd("pause")

async def do_stop(mpd):
	await mpd("stop")

async def do_prev(mpd):
	async with save_state(mpd) as status:
		if float(status.get("elapsed", 1e10)) < 1:
			await mpd("previous")
		else:
			await mpd("seekcur", "0")

async def do_prev2(mpd):
	async with save_state(mpd) as status:
		await mpd("random", str(1-int(status["random"])))
		await mpd("previous")

async def do_next(mpd):
	async with save_state(mpd):
		await mpd("next")

async def do_next2(mpd):
	async with save_state(mpd) as status:
		await mpd("random", str(1-int(status["random"])))
		await mpd("next")

async def add_playlist(mpd, path, add):
	async with save_state(mpd):
		if not add:
			await mpd("clear")
		await mpd("add", path)

async def do_command(mpd, *command):
	await mpd(*command)

class MPD2(Gtk.EventBox):
	def __init__(self, keys=False, spacing=3):
		super().__init__()

		self.icon = Gtk.Label()
		self.text = ProgressLabel()
		scroll = util.scrollable(self.text, h=False, v=None)
		scroll.set_propagate_natural_width(True)
		self.text.connect("hide", lambda _: scroll.hide())
		self.text.connect("show", lambda _: scroll.show())
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(scroll, False, False, 0)
		self.add(box)

		self.treestore = Gtk.TreeStore(str, str, str) # Display name, search name, filename

		async def toggle_repeat(mpd):
			status = dict(await mpd("status"))
			if status["single"] == "1":
				await mpd.list([["single", "0"], ["repeat", "0"]])
			elif status["repeat"] == "1":
				await mpd.list([["single", "1"], ["repeat", "1"]])
			else:
				await mpd.list([["single", "0"], ["repeat", "1"]])
		self.repBtn = Gtk.Button(image=Gtk.Image())
		self.repBtn.connect("clicked", lambda _: run_mpd(toggle_repeat))
		self.repBtn.connect("clicked", lambda b: b.set_state_flags(Gtk.StateFlags.CHECKED, False))

		async def toggle_shuffle(mpd):
			status = dict(await mpd("status"))
			await mpd("random", "01"[status["random"] == "0"])
		self.shufBtn = Gtk.Button(image=Gtk.Image())
		self.shufBtn.connect("clicked", lambda _: run_mpd(toggle_shuffle))
		self.shufBtn.connect("clicked", lambda b: b.set_state_flags(Gtk.StateFlags.CHECKED, False))

		p = Gdk.EventType.BUTTON_PRESS
		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", lambda _, e: (e.type, e.button) == (p, 3) and self.open_popup())
		self.icon.set_has_window(True)
		self.icon.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.icon.connect("button-press-event", lambda _, e: (e.type, e.button) == (p, 1) and run_mpd(do_toggle))
		self.icon.connect("button-press-event", lambda _, e: (e.type, e.button) == (p, 2) and run_mpd(do_stop))
		self.text.set_has_window(True)
		self.text.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		async def click_text(mpd, pos):
			if pos < .05:
				await do_prev(mpd)
			elif pos > .95:
				await do_next(mpd)
			else:
				status = dict(await mpd("status"))
				if "duration" in status:
					await mpd("seekcur", str(pos * float(status["duration"])))
		self.text.connect("button-press-event", lambda l, e: (e.type, e.button) == (p, 1) and run_mpd(click_text, e.x / l.get_allocated_width()))

		self.popup = None

		if keys:
			Keybinder.bind("AudioPlay", lambda _: run_mpd(do_toggle))
			Keybinder.bind("<Shift>AudioPlay", lambda _: run_mpd(do_stop))
			Keybinder.bind("AudioPrev", lambda _: run_mpd(do_prev))
			Keybinder.bind("<Shift>AudioPrev", lambda _: run_mpd(do_prev2))
			Keybinder.bind("AudioNext", lambda _: run_mpd(do_next))
			Keybinder.bind("<Shift>AudioNext", lambda _: run_mpd(do_next2))

		self.ticker_running = asyncio.Event()
		self.ticker_running.set()
		asyncio.ensure_future(self.run_ticker())
		asyncio.ensure_future(self.run_idler())

	async def run_ticker(self):
		while True:
			try:
				async with MpdClient() as mpd:
					while True:
						await self.ticker_running.wait()
						await self.update_status(mpd)
						await asyncio.sleep(0.1)
			except MPDClosedError as e:
				await asyncio.sleep(1)

	async def run_idler(self):
		while True:
			try:
				async with MpdClient() as mpd:
					await self.update_status(mpd)
					await self.update_database(mpd)
					await self.update_options(mpd)
					while True:
						changed = dict(await mpd("idle"))["changed"]
						if changed == "player": await self.update_status(mpd)
						if changed == "database": await self.update_database(mpd)
						if changed == "options": await self.update_options(mpd)
			except MPDClosedError as e:
				self.set_state(MpdState.error)
				await asyncio.sleep(1)

	async def update_database(self, mpd):
		async def create_playlist(mpd, node, path):
			files = []
			for k, v in await mpd("lsinfo", path):
				if k in ["file", "directory"]:
					files.append({"_type": k})
				files[-1][k] = v

			for f in files:
				if f["_type"] == "file":
					self.treestore.append(node, row=[gettitle(f, num=True), gettitle(f), f["file"]])
				elif f["_type"] == "directory":
					dirname = os.path.basename(f["directory"])
					child = self.treestore.append(node, row=[dirname, dirname, f["directory"]])
					await create_playlist(mpd, child, f["directory"])

		self.treestore.clear()
		self.treestore.append(None, row=["—", "", ""])
		await create_playlist(mpd, None, "")

	async def update_status(self, mpd):
		status = dict(await mpd("status"))
		self.set_state(MpdState[status["state"]])

		if "elapsed" in status and "duration" in status:
			self.text.set_bounds(float(status["elapsed"]), float(status["duration"]))

		song = dict(await mpd("currentsong"))
		self.text.set_text(gettitle(song))

	def set_state(self, state):
		self.icon.set_text(""[state])
		self.text.set_visible(state >= MpdState.pause)
		self.set_opacity(1 if state >= MpdState.pause else 0.25)

		if state == MpdState.play:
			self.ticker_running.set()
		else:
			self.ticker_running.clear()

	async def update_options(self, mpd):
		status = dict(await mpd("status"))
		set_icon = lambda c, s: c.get_image().set_from_icon_name(f"media-playlist-{s}-symbolic", Gtk.IconSize.BUTTON)
		set_flag = lambda c, f, v: c.set_state_flags(f, False) if v else c.unset_state_flags(f)

		set_icon(self.repBtn, "repeat" + "-song" * int(status["single"]))
		set_icon(self.shufBtn, "shuffle")
		set_flag(self.repBtn, Gtk.StateFlags.CHECKED, int(status["repeat"]))
		set_flag(self.shufBtn, Gtk.StateFlags.CHECKED, int(status["random"]))

	def open_popup(self):
		tree = Gtk.TreeView(self.treestore, enable_search=True, search_column=1, headers_visible=False)
		tree.set_search_equal_func(search_tree, tree)
		tree.insert_column_with_attributes(0, "Title", Gtk.CellRendererText(), text=0)
		tree.connect("row-activated", lambda _, path, __: run_mpd(add_playlist, tree.get_model()[path][-1], getattr(Gtk.get_current_event(), "state", 0) & Gdk.ModifierType.SHIFT_MASK))

		@run_mpd_sync
		async def coro(mpd):
			current_song = dict(await mpd("currentsong")).get("file")
			def walk(model, path, iter):
				if model[iter][-1] == current_song:
					tree.expand_to_path(path)
					tree.scroll_to_cell(path, None, True, 0.5, 0.5)
					tree.set_cursor(path, None, False)
			self.treestore.foreach(walk)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		stree = util.scrollable(tree, h=None)
		stree.set_size_request(0, 300)
		vbox.pack_start(stree, False, False, 0)

		buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, spacing=4)
		self.repBtn.unparent()
		self.shufBtn.unparent()
		buttons.add(self.repBtn)
		buttons.add(self.shufBtn)
		vbox.pack_end(buttons, True, True, 2)

		self.popup = util.make_popup(util.framed(vbox), self)
		self.popup.show_all()

class ProgressLabel(Gtk.Label):
	def __init__(self):
		Gtk.Label.__init__(self)
		self.set_bounds(0, 0)

	def set_bounds(self, current, max):
		self.current = current
		self.max = max
		self.queue_draw()

	def do_draw(self, ctx):
		Gtk.Label.do_draw(self, ctx) # super() doesn't work for some reason

		if not self.current or not self.max: return

		style = self.get_style_context()
		color = style.get_color(style.get_state())

		ctx.set_line_cap(cairo.LINE_CAP_BUTT)
		ctx.set_source_rgba(*color)

		pango = self.get_pango_context()
		metrics = pango.get_metrics()
		height = self.get_allocated_height() * Pango.SCALE
		pos = (height + metrics.get_ascent()-metrics.get_descent())/2

		upos, thick = metrics.get_underline_position(), metrics.get_underline_thickness()
		pos -= upos
		pos /= Pango.SCALE
		thick /= Pango.SCALE

		len = self.current / self.max * self.get_allocated_width()
		ctx.move_to(0, pos)
		ctx.line_to(len, pos)
		ctx.line_to(len, pos + thick)
		ctx.line_to(0, pos + thick)
		ctx.fill()

def search_tree(model, column, key, rowiter, tree):
	if key == key.lower():
		match = lambda row: key.lower() in row[column].lower()
	else:
		match = lambda row: key in row[column]
	def expand_row(row):
		should_expand = any([expand_row(child) for child in row.iterchildren()])
		if should_expand:
			tree.expand_to_path(row.path)
		else:
			tree.collapse_row(row.path)
		return should_expand or match(row)
	row = model[rowiter]
	expand_row(row)
	return not match(row)
