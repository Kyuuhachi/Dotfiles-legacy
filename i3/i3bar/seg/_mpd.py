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
				i3bar.update(self)

	def getOutput(self):
		with open() as mpd:
			status = mpd.status()
			state = status["state"]
			if state not in ["pause", "play"]:
				return None
			title = gettitle(mpd.currentsong())
			sym = "" if state == "play" else " " # 
			t = status["time"].split(':')
			prog = int((len(title) + 1) * int(t[0]) / (int(t[1]) or 1)) # MIDIs have no length!?
			pre, post = quote(title[:prog]), quote(title[prog:])
			out = "{} <span underline='single'>{}</span>{}".format(sym, pre, post)
			return {"full_text": out, "markup": "pango"}

	def click(self, button, name):
		if button == 1:
			self.play()
		if button == 2:
			self.album()
		if button == 3:
			self.restart()

	def restart(self):
		with open() as mpd:
			mpd.stop()
			mpd.play()

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
