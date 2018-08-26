import gi
gi.require_version("GLib", "2.0")
from gi.repository import GLib, Gio

import asyncio
from asyncio.unix_events import SelectorEventLoop as SelectorLoop
from asyncio.unix_events import AbstractChildWatcher as ChildWatcher
import selectors
from collections import namedtuple

def to_cond(events):
	cond = GLib.IOCondition(0)
	if events & selectors.EVENT_READ: cond |= GLib.IOCondition.IN
	if events & selectors.EVENT_WRITE: cond |= GLib.IOCondition.OUT
	return cond

def from_cond(cond):
	events = 0
	if cond & GLib.IOCondition.IN: events |= selectors.EVENT_READ
	if cond & GLib.IOCondition.OUT: events |= selectors.EVENT_WRITE
	return events | 3 # XXX This shouldn't work

class GLibSelector(selectors._BaseSelectorImpl):
	def __init__(self, ctx=None):
		super().__init__()
		if ctx is None:
			ctx = GLib.MainContext.default()
		self.ctx = ctx
		self.tags = {}

		self.source = GLib.Source()
		self.source.attach(self.ctx)
		self.source.prepare = lambda: (False, self.timeout)
		self.source.check = lambda: False
		self.source.dispatch = self.dispatch
		self.timeout = None
		self.ready_fds = None

	def register(self, fileobj, events, data=None):
		key = super().register(fileobj, events, data)
		tag = self.source.add_unix_fd(key.fd, to_cond(events))
		self.tags[key.fd] = tag
		return key

	def modify(self, fileobj, events, data=None):
		try:
			key = self._fd_to_key[self._fileobj_lookup(fileobj)]
		except KeyError:
			raise KeyError("{!r} is not registered".format(fileobj)) from None
		if events != key.events:
			self.source.modify_unix_fd(self.tags[key.fd], to_cond(events))
		key = key._replace(fileobj=fileobj, events=events, data=data)
		self._fd_to_key[key.fd] = key
		return key

	def unregister(self, fileobj):
		key = super().unregister(fileobj)
		self.source.remove_unix_fd(self.tags.pop(key.fd))
		return key

	def dispatch(self, cbk, _):
		for fd, tag in self.tags.items():
			events = from_cond(self.source.query_unix_fd(tag))
			if events:
				self.ready.append((self._fd_to_key[fd], events))
		return True

	def select(self, timeout=None):
		self.ready = []

		if timeout is None:
			self.timeout = -1
			self.ctx.iteration(True)
		elif timeout > 0:
			self.timeout = int(timeout*1000)
			self.ctx.iteration(True)
		else:
			self.timeout = 0
			self.ctx.iteration(False)

		return self.ready

class GLibChildWatcher(ChildWatcher):
	def __init__(self):
		self._sources = {}

	def attach_loop(self, loop):
		pass

	def add_child_handler(self, pid, callback, *args):
		self.remove_child_handler(pid)

		def _glib_callback(pid, status):
			import os
			self._sources.pop(pid)
			GLib.source_remove(source)

			if os.WIFSIGNALED(status):
				returncode = -os.WTERMSIG(status)
			elif os.WIFEXITED(status):
				returncode = os.WEXITSTATUS(status)
			else:
				returncode = status
			callback(pid, returncode, *args)
		source = GLib.child_watch_add(0, pid, _glib_callback)
		self._sources[pid] = source

	def remove_child_handler(self, pid):
		try:
			source = self._sources.pop(pid)
		except KeyError:
			return False

		GLib.source_remove(source)
		return True

	def close(self):
		for source, callback, args in self._sources.values():
			GLib.source_remove(source)

	def __enter__(self):
		return self

	def __exit__(self, a, b, c):
		pass

class GLibEventLoop(SelectorLoop):
	def __init__(self):
		super().__init__(GLibSelector())
