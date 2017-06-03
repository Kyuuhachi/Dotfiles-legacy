import json
import sys
import threading
import i3bar.util

class _InputHandler(threading.Thread):
	def run(self):
		sys.stdin.readline()
		for cmd in self.read():
			try:
				seg = _map[int(cmd["instance"])]
				seg.click(cmd["button"], cmd.get("name", None))
				update(seg)
			except Exception as e:
				import traceback
				i3bar.log(traceback.format_exc())

	def read(self):
		for line in sys.stdin:
			yield json.loads(line.strip(","))

class _OutputHandler(i3bar.util.Timer):
	def _update(self, seg):
		def convert(seg):
			info = seg.getOutput()
			if info is None:
				return []
			if not hasattr(info, "__iter__") or isinstance(info, str) or isinstance(info, dict):
				info = [info]

			out = []
			for segOut in info:
				val = _proto.copy()
				val["instance"] = str(id(seg))
				if isinstance(segOut, str):
					val["full_text"] = segOut
				elif isinstance(segOut, dict):
					val.update(segOut)
				elif segOut is None:
					continue
				out.append(val)
			return out
		try:
			seg._out = convert(seg)
		except Exception:
			import traceback
			print(traceback.format_exc(), file=sys.stderr)

	def update(self, *seg):
		for s in seg:
			self._update(s)
		self.printStatus()

	def start(self):
		print('{"version":1,"click_events":true}\n[\n[]')
		super().start()

	def run(self):
		for seg in _segments:
			self._update(seg)
		self.printStatus()

	def printStatus(self):
		list = []
		for seg in reversed(_segments):
			list += reversed(seg._out)
		print("," + json.dumps(list))
		sys.stdout.flush()

_in = _InputHandler()
_out = _OutputHandler()
_segments = []
_map = {}
_proto = {}

def update(*seg):
	_out.update(*seg)

def add(seg):
	_segments.append(seg)
	_map[id(seg)] = seg

def proto(val):
	_proto.update(val)

def start():
	_in.start()
	_out.start()
	for seg in _segments:
		seg.start()

def log(*args):
	print(*args, file=sys.stderr)
	sys.stderr.flush()

class Segment:
	_out = []
	def start(self):
		pass
	def getOutput(self):
		return ""
	def click(self, button, name):
		pass
