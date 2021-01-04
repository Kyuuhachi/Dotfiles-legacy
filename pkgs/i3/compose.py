#!/usr/bin/env python3
import subprocess

import argparse

from Xlib import X
import Xlib.display

def parse(f):
	chars = {}
	for line in f.read().splitlines():
		line = line.split("#", 1)[0].rstrip()
		if not line: continue
		char, key = line.split("\t", 2)
		key = " ".join(key.split())
		chars[char + " " + key] = char
	return chars

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

def get_keysym(char):
	char = ord(char)
	if 0x20 <= char <= 0x7F or 0x80 <= char <= 0xFF:
		return char
	if chr(char) in "\r\n\t\x1B":
		return 0xFF00 | char
	return char | 0x01000000

argp = argparse.ArgumentParser()
argp.add_argument("list", type=argparse.FileType("r"))
def __main__():
	args = argp.parse_args()
	proc = subprocess.Popen(
		["dmenu", "-f"],
		encoding="utf-8",
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
	)
	try:
		with args.list as f:
			chars = parse(f)

		with proc.stdin:
			for line in chars:
				proc.stdin.write(line + "\n")

		for line in proc.stdout:
			line = line.strip()

			try:
				if line in chars:
					char = chars[line]
				elif line.startswith("#"):
					char = chr(int(line[1:], 16))
				elif line.startswith("="):
					char = str(eval(line[1:]))
				else:
					raise ValueError(line)
			except Exception as e:
				subprocess.Popen(["notify-send", str(e)])
			else:
				xtype([get_keysym(ch) for ch in char])

		proc.wait()
	finally:
		proc.kill()

if __name__ == "__main__": __main__()
