# Named _mpd because I need to import the mpd module
import i3bar
import i3bar.util
import i3bar.ipc
import dmenu
import os.path
import re
from mpd import MPDClient
import threading

__all__ = ["MPD"]

def stripfname(title):
	title = os.path.basename(title)
	title = re.sub(r"^[0-9\-]+(\.| -) ", "", title) # Strip leading numbers ("xx. " and "xx - ") (and also "x-xx - " for multiparts)
	title = re.sub(r"\.[^.]+?$", "", title) # Strip file extension
	return title

def gettitle(track):
	if "title" in track:
		title = track["title"]
	elif "file" in track:
		title = stripfname(track["file"])
	else:
		title = "<Unknown>"
	return title

def quote(s):
	return s.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")

class MPD(i3bar.Segment):
	def __init__(self, dmenu_color=None):
		self.color = dmenu_color
		self._mpd = threading.local()

	def start(self):
		i3bar.ipc.register("mpd-play", self.play)
		i3bar.ipc.register("mpd-stop", self.stop)
		i3bar.ipc.register("mpd-album", self.album)
		self.updateloop()

	@property
	def mpd(self):
		if hasattr(self._mpd, "mpd"):
			try:
				self._mpd.mpd.status()
			except BrokenPipeError:
				del self._mpd.mpd
		if not hasattr(self._mpd, "mpd"):
			self._mpd.mpd = MPDClient()
			self._mpd.mpd.connect(os.getenv("MPD_HOST", "localhost"), os.getenv("MPD_PORT", None))
		return self._mpd.mpd

	@i3bar.util.OtherThread
	def updateloop(self):
		while True:
			self.mpd.idle()
			i3bar.update(self)

	def getOutput(self):
		status = self.mpd.status()
		if status["state"] not in ["play", "pause"]:
			return None
		currentsong = self.mpd.currentsong()
		title = gettitle(currentsong)
		progress = len(title) * float(status["elapsed"]) / float(status["duration"])

		segs = [
			{
				"full_text": {"play": " ", "pause": " "}.get(status["state"], "? "),
				"name": "symbol",
				"separator": False,
				"separator_block_width": 0
			},
			*({
				"full_text": "<span {format}>{char}</span>".format(format="underline='single'" if i <= progress - 0.5 else "", char=quote(c)),
				"markup": "pango",
				"name": "title-{}".format(i),
				"separator": False,
				"separator_block_width": 0
			} for i, c in enumerate(title)),
			{
				"full_text": "<span></span>",
				"markup": "pango"
			}
		]
		return reversed(segs)

	def click(self, button, name):
		if name == "symbol":
			if button == 1:
				self.play()
		elif name.startswith("title-"):
			if button == 1:
				self.seek(int(name[6:]))
			if button == 2:
				self.album()

	def seek(self, n):
		title = gettitle(self.mpd.currentsong())
		self.mpd.seekcur(n / len(title) * float(self.mpd.status()["duration"]))

	def stop(self):
		self.mpd.stop()

	def play(self):
		if self.mpd.status()["state"] != "play":
			self.mpd.play()
		else:
			self.mpd.pause()

	def album(self):
		def select(path):
			files = [("file" in f, f.get("file", f.get("directory"))) for f in self.mpd.lsinfo(path)]
			vals = {}
			for isfile, fpath in files:
				name = os.path.basename(fpath)
				if isfile:
					name = stripfname(name)
				else:
					name += '/'
				vals[name] = (isfile, fpath)
			keys = [""] + sorted(vals, key=lambda l: (vals[l][0], l))
			vals[""] = (True, path)
			out = dmenu.show(keys, background_selected=self.color)
			if out not in vals:
				return None
			isfile, path = vals[out]
			return path if isfile else select(path)

		track = select("")
		if track is not None:
			self.mpd.clear()
			self.mpd.add(track)
			self.mpd.play()
