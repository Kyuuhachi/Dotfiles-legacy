from Xlib.display import Display
from Xlib import X, XK
from Xlib.protocol.event import KeyPress
from Xlib.protocol import request

import signal
import time

import i3py
import i3py.util

class Kbd:
	def __init__(self, out):
		signal.signal(signal.SIGUSR1, i3py.util.OtherThread(self.run))
		self.out = out
		self.sel = None

	def run(self, a, b):
		disp = Display()
		root = disp.screen().root
		for n in range(0, 10):
			if root.grab_keyboard(False, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime) == 0:
				break
			time.sleep(0.01)

		self.sel = self.last()
		self.out.update(None)

		while 1:
			evt = root.display.next_event()
			if evt.type == X.KeyPress:
				sym = disp.keycode_to_keysym(evt.detail, 0)
				char = XK.keysym_to_string(sym)
				if (evt.state & 0x4 and char == 'c') or sym == XK.XK_Escape:
					break

				if sym == XK.XK_Left or char in ['a', 'h']:
					self.sel = self.prev(self.sel)
				if sym == XK.XK_Right or char in ['d', 'l']:
					self.sel = self.next(self.sel)
				if sym == XK.XK_Home:
					self.sel = self.first()
				if sym == XK.XK_End:
					self.sel = self.last()

				if sym == XK.XK_Return or char in [' ']:
					self.sel.click(1)
					break
				if sym == XK.XK_Up or char in ['w', 'k']:
					self.sel.click(4)
				if sym == XK.XK_Down or char in ['s', 'j']:
					self.sel.click(5)

				self.out.update(None)

		self.sel = None
		self.out.update(None)

		request.UngrabKeyboard(display=root.display, time=X.CurrentTime)
		disp.flush()

	def find(self, list):
		for seg in list[1:]:
			if seg._out != None and type(seg).click != i3py.Segment.click:
				return seg
		return list[0]
	def prev(self, sel):
		return self.find(i3py._segments[i3py._segments.index(sel)::1])
	def next(self, sel):
		return self.find(i3py._segments[i3py._segments.index(sel)::-1])
	def first(self):
		return self.find([None] + i3py._segments[::-1])
	def last(self):
		return self.find([None] + i3py._segments[::1])
