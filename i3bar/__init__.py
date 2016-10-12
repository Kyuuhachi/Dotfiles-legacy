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
				seg.click(cmd["button"])
				update(seg)
			except Exception as e:
				import traceback
				print(traceback.format_exc())

	def read(self):
		for line in sys.stdin:
			yield json.loads(line.strip(","))

class _OutputHandler(i3bar.util.Timer):
	def _update(self, seg):
		def convert(seg):
			segOut = seg.getOutput()

			val = _proto.copy()
			val["instance"] = str(id(seg))
			if type(segOut) == str:
				val["full_text"] = segOut
			if type(segOut) == tuple:
				if segOut[0]:
					val["full_text"] = segOut[0]
				if segOut[1]:
					val["color"] = segOut[1]
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

	def start(self):
		print('{"version":1,"click_events":true}\n[\n[]', file=sys.stderr)
		super().start()

	def run(self):
		for seg in _segments:
			self._update(seg)
		self.printStatus()

	def printStatus(self):
		list = []
		for seg in _segments:
			if seg._out:
				list.insert(0, dict(seg._out))
		print("," + json.dumps(list), file=sys.stderr)
		sys.stderr.flush()

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

class Segment:
	_out = None
	def start(self):
		pass
	def getOutput(self):
		return ""
	def click(self, button):
		pass
