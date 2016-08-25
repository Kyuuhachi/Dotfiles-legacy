import json, os, sys, threading, logging
import i3py.util
from i3py.bar.kbd import Kbd

class _InputHandler(threading.Thread):
	def run(self):
		sys.stdin.readline()
		for cmd in self.read():
			try:
				seg = _map[int(cmd["instance"])]
				seg.click(cmd["button"])
				update(seg)
			except Exception as e:
				import traceback
				print(traceback.format_exc())

	def read(self):
		for line in sys.stdin:
			yield json.loads(line.strip(","))

class _OutputHandler(i3py.util.Timer):
	def start(self):
		super().start()
		self.print('{"version":1,"click_events":true}\n[\n[]')

	def _update(self, seg):
		def convert(seg):
			segOut = seg.getOutput()

			val = _proto.copy()
			val["instance"] = str(id(seg))
			if type(segOut) == str:
				val["full_text"] = segOut
			if type(segOut) == tuple:
				if segOut[0]: val["full_text"] = segOut[0]
				if segOut[1]: val["color"] = segOut[1]
			if type(segOut) == dict:
				val.update(segOut)

			if "full_text" in val:
				return val
			else:
				return None

		try:
			seg._out = convert(seg)
		except Exception:
			import traceback
			print(traceback.format_exc())

	def update(self, *seg):
		for s in seg:
			self._update(s)
		self.printStatus()

	def run(self):
		for seg in _segments:
			self._update(seg)
		self.printStatus()

	def printStatus(self):
		list = []
		for seg in _segments:
			if seg._out:
				out = dict(seg._out)
				if _kbd.sel != None:
					if _kbd.sel == seg:
						out["border"] = "#FF0000"
					elif type(seg).click != Segment.click:
						out["border"] = "#7F0000"
				list.insert(0, out)
		self.print("," + json.dumps(list))

	def print(self, *args):
		print(*args, file=_stdout)
		_stdout.flush()

_stdout = sys.stdout
sys.stdout = os.fdopen(os.dup(sys.stderr.fileno()), "w", 1) #No buffering; I want to be able to tail -f it

_in = _InputHandler()
_out = _OutputHandler()
_segments = []
_map = {}
_proto = {}
_kbd = Kbd()

def update(*seg):
	_out.update(*seg)

def add(seg):
	_segments.append(seg)
	_map[id(seg)] = seg

def proto(val):
	_proto.update(val)

def start():
	_kbd.start()
	_in.start()
	_out.start()
	for seg in _segments:
		seg.start() #For timers and such

class Segment:
	_out = None
	def start(self):
		pass
	def getOutput(self):
		return ""
	def click(self, button):
		pass