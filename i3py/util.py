import threading
import time

class Timer:
	interval = 1
	_target = None
	name = None

	def __init__(self, interval=None, target=None, name=None):
		if interval: self.interval = interval
		if target: self._target = target
		if name: self.name = name

	def start(self):
		self._thread = threading.Thread(target=self._run, name=str(self.name) + "-event")
		self._thread2 = threading.Thread(target=self._sig, name=str(self.name) + "-timer")
		self._event = threading.Event()
		self._thread.start()
		self._thread2.start()

	def interrupt(self):
		self._event.set()

	def run(self):
		pass

	def _run(self):
		if not self._target: self._target = self.run
		while True:
			self._target()
			self._event.wait()
			self._event.clear()

	def _sig(self):
		while True:
			time.sleep(self.interval)
			self.interrupt()

def group(data, count=2, default=None):
	it = iter(data)
	while True:
		out = [default] * count
		for n in range(0, count):
			try:
				out[n] = next(it)
			except StopIteration:
				if n != 0: yield tuple(out)
				raise
		yield tuple(out)

def braille(bits):
	idx = [6, 2, 1, 0, 7, 5, 4, 3]
	char = 0x2800
	for i in range(8):
		if bits & 1 << i: char |= 1 << idx[i]
	return chr(char)

def braillegraph(data, fill=False):
	def fillFunc(x):
		return ((1 << x) - 1) & 15
	def topFunc(x):
		n = fillFunc(x);
		return n & ~(n >> 1)
	func = fillFunc if fill else topFunc

	return "".join([
		braille(a | b << 4)
		for a, b in group(map(func, data), 2, 0)
	])
