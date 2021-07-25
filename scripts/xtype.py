#!/usr/bin/env python3
import argparse
import Xlib.display
import Xlib.keysymdef
import Xlib.XK
from Xlib import X
import time
import main

def xtype(keysyms):
	N = 8
	start_code = 255-N
	display = Xlib.display.Display()
	for a in range(0, len(keysyms), N):
		chunk = list(enumerate(keysyms[a:a+N], start_code))
		display.change_keyboard_mapping(start_code, [(sym,) * 8 for code, sym in chunk])
		while 1:
			if display.next_event().type == X.MappingNotify:
				break
		for code, sym in chunk:
			display.xtest_fake_input(X.KeyPress, code)
			display.xtest_fake_input(X.KeyRelease, code)
		display.sync()
		if a+N <= len(keysyms): time.sleep(0.05)

def get_char(char):
	char = ord(char)
	if 0x20 <= char <= 0x7F or 0x80 <= char <= 0xFF:
		return char
	if chr(char) in "\r\n\t\x1B":
		return 0xFF00 | char
	return char | 0x01000000

argp = argparse.ArgumentParser(description="Types a string using Xtest")
argp.add_argument("string", nargs="+", help="The string to type")
argp.add_argument("-s", "--keysym", action="store_true", help="Specify keysym(s) by name instead of chars")
@main(argp=argp)
def __main__(string, keysym):
	if keysym:
		for group in Xlib.keysymdef.__all__:
			Xlib.XK.load_keysym_group(group)
		syms = []
		for key in string:
			try:
				syms.append(Xlib.XK.string_to_keysym(key) or int(key, base=16))
			except:
				print(f"Invalid keysym: {key}")
	else:
		syms = [get_char(ch) for ch in " ".join(string)]
	if syms:
		xtype(syms)
