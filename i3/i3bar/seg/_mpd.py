# Named _mpd because I need to import the mpd module
import i3bar
import i3bar.util
import i3bar.ipc
import dmenu
import os.path
import re
from mpd import MPDClient
from contextlib import contextmanager

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

@contextmanager
def open():
	mpd = MPDClient()
	try:
		mpd.connect(os.path.expanduser("~/.mpd/socket"), None)
	except:
		pass
	yield mpd
	mpd.close()
	mpd.disconnect()

class MPD(i3bar.Segment):
	def __init__(self, dmenu_color=None):
		self.color = dmenu_color

	def start(self):
		i3bar.ipc.register("mpd-play", self.play)
		i3bar.ipc.register("mpd-stop", self.stop)
		i3bar.ipc.register("mpd-album", self.album)
		self.updateloop()

	@i3bar.util.OtherThread
	def updateloop(self):
		with open() as mpd:
			while True:
				mpd.idle()
				i3bar.log("asdf")
				i3bar.update(self)

	def getOutput(self):
		with open() as mpd:
			status = mpd.status()
			title = gettitle(mpd.currentsong())
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
		with open() as mpd:
			title = gettitle(mpd.currentsong())
			mpd.seekcur(n / len(title) * float(mpd.status()["duration"]))

	def stop(self):
		with open() as mpd:
			mpd.stop()

	def play(self):
		with open() as mpd:
			if mpd.status()["state"] != "play":
				mpd.play()
			else:
				mpd.pause()

	def album(self):
		with open() as mpd:
			def id(a): return a
			def select(path):
				files = [("file" in f, f.get("file", f.get("directory"))) for f in mpd.lsinfo(path)]
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
				mpd.clear()
				mpd.add(track)
				mpd.play()
