import i3bar
import i3bar.util
import i3bar.ipc
import dmenu
import os.path
import re
import threading
from mpd import MPDClient
from contextlib import contextmanager

__all__ = ["MPD"]

def gettitle(track, maxlen=None):
	if "title" in track:
		title = track["title"]
	elif "file" in track:
		title = os.path.basename(track["file"])
		title = re.sub(r"^[0-9\-]+(\.| -) ", "", title) # Strip leading numbers
		title = re.sub(r"\..+?$", "", title) # Strip file extension
	else:
		title = "<Unknown>"
	if maxlen is not None:
		if len(title) > maxlen:
			for r in [r"\s", r"[^\w\d]"]:
				tmp = re.sub(r, "", title)
				if len(tmp) <= maxlen:
					return tmp
			return title[:maxlen - 1] + "…"
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
	def __init__(self):
		self.timeout = threading.Thread()

	def start(self):
		i3bar.ipc.register("mpd-play", self.play)
		i3bar.ipc.register("mpd-stop", self.stop)
		i3bar.ipc.register("mpd-album", self.album)
		i3bar.ipc.register("mpd-show", self.show)
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
			title = gettitle(mpd.currentsong(), None if self.timeout.isAlive() else 40)
			sym = "" if state == "play" else " " # 
			t = status["time"].split(':')
			prog = int((len(title) + 1) * int(t[0] / int(t[1])))
			pre, post = quote(title[:prog]), quote(title[prog:])
			out = "{} <span underline='single'>{}</span>{}".format(sym, pre, post)
			i3bar.log(out)
			return {"full_text": out, "markup": "pango"}

	def click(self, button):
		if button == 1:
			self.play()
		if button == 2:
			self.album()
		if button == 3:
			self.show()

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
			def find_dir(path):
				dirs = [a["directory"] for a in mpd.lsinfo(path) if "directory" in a]
				if not dirs:
					return path
				fnames = {os.path.basename(f): f for f in dirs}
				fnames[""] = None
				out = dmenu.Dmenu().show(sorted(fnames))
				if out not in fnames:
					return None
				if fnames[out] is None:
					return path
				return find_dir(fnames[out])
			album = find_dir("")
			if album is not None:
				mpd.clear()
				mpd.add(album)
				mpd.play()

	def show(self):
		if self.timeout.isAlive():
			self.timeout.interrupt()
		else:
			self.timeout = i3bar.util.Timeout(0.5, lambda: i3bar.update(self))
			self.timeout.start()
