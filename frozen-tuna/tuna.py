#!/usr/bin/env python3
import argparse
import urllib.parse
import handler
import os
import os.path
import subprocess
import sys
import config
import mime
import util

def get_icons(mimes):
	icons = set()
	for m in mimes:
		if m in mime.ICONS:
			icon = mime.ICONS[m]
			if icon.endswith("-x-generic"):
				icon = icon[:-10]
		else:
			icon = m.split("/", 1)[0]
		icons.add(icon)
	return icons

def get_command(scheme, hand):
	mimes = {tuple(mime.split("/")) for mime in hand.mimes}
	icons = get_icons(hand.mimes)
	mimeClasses = {type for type,sub in mimes}
	parent = open(f"/proc/{os.getppid()}/cmdline", "rb").read().split(b"\0")[0].decode()
	def test_cond(c):
		type, args = c
		assert type.startswith("cond_")
		type = type[5:]
		return {
			"or": lambda *cs: any(test_cond(c) for c in cs),
			"and": lambda *cs: all(test_cond(c) for c in cs),
			"mime": lambda t, s: (t,s) in mimes,
			"mime2": lambda t: t in mimeClasses,
			"icon": lambda i: i in icons,
			"scheme": lambda s: s == scheme,
			"host": lambda h: h in hand.hosts,
			"parent": lambda n: n == parent,
			"else": lambda: True
		}[type](*args)

	for cond, cmd in config.config:
		if test_cond(cond):
			return cmd

def transform_cmd(cmd, h, env):
	if isinstance(cmd, str): # Shell command
		out, = subprocess.check_output(["getent", "passwd", str(os.getuid())]).decode().splitlines()
		yield out.split(":")[6]
		yield "-c"
		yield cmd
		os.putenv("TUNA_URL", h.url)
		os.putenv("TUNA_PATH", h.path)
	else: # Plain command
		for arg in cmd:
			if arg.startswith("$"):
				yield env[arg[1:]]
			elif arg.startswith("%"):
				_, c = arg
				if c == "u": yield h.url
				elif c == "f": yield h.path
				else: raise ValueError(arg)
			else:
				yield arg

def __main__():
	argp = argparse.ArgumentParser()
	argp.add_argument("-n", "--dry-run", action="store_true", help="Don't open the file, only figure out how")
	argp.add_argument("-s", "--sync",    action="store_true", help="Don't fork, so you can wait for the process to close") # TODO make detection also async
	argp.add_argument("file")
	args = argp.parse_args()

	try:
		scheme = urllib.parse.urlparse(args.file).scheme
		print(f"[Frozen Tuna] Opening {args.file}", file=sys.stderr)
		h = handler.registry[scheme](args.file)
		print(f"[Frozen Tuna]   Possible mime types: {h.mimes}", file=sys.stderr)
		cmd = get_command(scheme, h)
		print(f"[Frozen Tuna]   {cmd}", file=sys.stderr)
		cmd = list(transform_cmd(cmd, h, os.environ))
	except Exception as e:
		import traceback
		util.notify("Error", traceback.format_exc())
		raise

	if cmd:
		util.notify(f"Opening {cmd}", h.url + "\n" + str(h.mimes))
		if not args.dry_run:
			if args.sync:
				os.execlp(*cmd)
			else:
				subprocess.Popen(cmd)
	else:
		util.notify(f"Don't know how to handle {h.url}")

__main__()