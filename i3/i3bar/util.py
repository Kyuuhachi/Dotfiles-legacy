import threading
import time
import functools

class Timer:
	interval = 1
	name = None

	def __init__(self, interval=None, target=None, name=None):
		if interval:
			self.interval = interval
		if target:
			self.run = target
		if name:
			self.name = name

	def start(self):
		self._thread = threading.Thread(target=self._sig, name=str(self.name or type(self).__name__) + "-timer")
		self._thread.start()

	def interrupt(self):
		self.run()

	def run(self):
		pass

	def _sig(self):
		while True:
			self.interrupt()
			time.sleep(self.interval)

	def isAlive(self):
		return self._thread.isAlive()

class Timeout:
	interval = 1
	name = None
	_cancel = False
	_running = False

	def __init__(self, interval=None, target=None, name=None):
		if interval:
			self.interval = interval
		if target:
			self.run = target
		if name:
			self.name = name

	def start(self):
		self._thread = threading.Thread(target=self._run, name=str(self.name) + "-event")
		self._event = threading.Event()
		self._thread.start()

	def interrupt(self): # TODO add some way to actually cancel it
		self._event.set()

	def run(self):
		pass

	def _run(self):
		self._running = True
		self._event.wait(self.interval)
		self._running = False
		self.run()

	def isAlive(self):
		return self._running

def OtherThread(func):
	@functools.wraps(func)
	def wrap(*args, **kwargs):
		threading.Thread(target=func, name=func.__name__ + "-thread", args=args, kwargs=kwargs).start()
	return wrap
