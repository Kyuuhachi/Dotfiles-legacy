import sys

assert __name__ != "__main__", "This file can not be run directly"

def main(function=None, /, **kwargs):
	if function is None:
		return lambda function: main(function, **kwargs)
	if isMain():
		runMain(function, **kwargs)
	return function
sys.modules[__name__] = main

def isMain():
	frame = sys._getframe()
	while frame is not None:
		if frame.f_code and frame.f_code.co_filename == __file__:
			frame = frame.f_back
			continue
		return frame.f_globals.get("__name__") == "__main__"

runners = {}
runners[None] = lambda f, kwargs: f(**kwargs)

try:
	import asyncio
except ImportError: pass
else:
	def run_asyncio(f, kwargs):
		return asyncio.run(f(**kwargs))
	runners[asyncio] = run_asyncio

try:
	import trio
except ImportError: pass
else:
	def run_trio(f, kwargs):
		if "asks" in sys.modules:
			sys.modules["asks"].init("trio")
		return trio.run(f, **kwargs)
	runners[trio] = run_trio

def runMain(f, *, argp=None, aio=None):
	args = {}
	if argp is not None:
		args = argp.parse_args().__dict__
	if aio not in runners:
		raise Exception(f"invalid runner: {aio!r}")
	try:
		v = runners[aio](f, args)
		if v is not None:
			sys.exit(v)
	except KeyboardInterrupt:
		sys.exit(131)
