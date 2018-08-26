#!/usr/bin/env python3
import argparse
KEYCODE = 250

def xtype(keysyms, keycode=KEYCODE):
	keysyms = list(enumerate(keysyms, keycode))
	print(keysyms)
	import Xlib.display
	from Xlib import X
	display = Xlib.display.Display()
	display.change_keyboard_mapping(keycode, [(sym,) * 8 for code, sym in keysyms])
	while 1:
		e = display.next_event()
		if e.type == X.MappingNotify:
			for code, sym in keysyms:
				display.xtest_fake_input(X.KeyPress, code)
				display.xtest_fake_input(X.KeyRelease, code)
			break
	display.sync()

def get_char(char):
	char = ord(char)
	if 0x80 <= char <= 0xFF:
		return char
	if chr(char) in "\r\n\t\x1B":
		return 0xFF00 | char
	return char | 0x01000000

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Types a string using Xtest")
	parser.add_argument("string", nargs="+", help="The string to type")
	parser.add_argument("-s", "--keysym", action="store_true", help="Specify keysym by name instead of chars")
	args = parser.parse_args()

	syms = []
	if args.keysym:
		import Xlib.keysymdef
		import Xlib.XK
		for group in Xlib.keysymdef.__all__:
			Xlib.XK.load_keysym_group(group)
		for key in args.string:
			try:
				keysym = Xlib.XK.string_to_keysym(key) or int(key, base=16)
			except:
				print("Invalid keysym: %s" % key)
				continue
			else:
				syms.append(keysym)
	else:
		for char in " ".join(args.string):
			syms.append(get_char(char))
	xtype(syms)
