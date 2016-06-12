from Xlib.display import Display
from Xlib import X, XK
from Xlib.protocol.event import KeyPress
from Xlib.protocol import request

import signal
import time

class Kbd:
	def __init__(self, out):
		signal.signal(signal.SIGUSR1, self.run)
		self.out = out
		self.sel = None

	def run(self, a, b):
		self.sel = self.out.last()
		self.out.update(None)

		disp = Display()
		root = disp.screen().root
		for n in range(0, 10):
			if root.grab_keyboard(False, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime) == 0:
				break
			time.sleep(0.01)

		while 1:
			evt = root.display.next_event()
			if evt.type == X.KeyPress:
				sym = disp.keycode_to_keysym(evt.detail, 0)
				char = XK.keysym_to_string(sym)
				if (evt.state & 0x4 and char == 'c') or sym == XK.XK_Escape:
					break

				if sym == XK.XK_Left or char in ['a', 'h']:
					self.sel = self.out.prev(self.sel)
				if sym == XK.XK_Right or char in ['d', 'l']:
					self.sel = self.out.next(self.sel)
				if sym == XK.XK_Home:
					self.sel = self.out.first()
				if sym == XK.XK_End:
					self.sel = self.out.last()

				if char == ' ':
					self.sel.click(1)
					break
				if sym == XK.XK_Up or char in ['w', 'k']:
					self.sel.click(4)
				if sym == XK.XK_Down or char in ['s', 'j']:
					self.sel.click(5)

				self.out.update(None)
		request.UngrabKeyboard(display=root.display, time=X.CurrentTime)
		disp.flush()

		self.sel = None
		self.out.update(None)
