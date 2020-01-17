#!/usr/bin/env python3
import argparse
import urllib.parse
import handler
import os
import subprocess
import sys
import config
import mime
import util
import shlex

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
		return {
			"cond_or":     lambda *cs: any(test_cond(c) for c in cs),
			"cond_and":    lambda *cs: all(test_cond(c) for c in cs),
			"cond_mime":   lambda t, s: (t,s) in mimes,
			"cond_mime2":  lambda t: t in mimeClasses,
			"cond_icon":   lambda i: i in icons,
			"cond_scheme": lambda s: s == scheme,
			"cond_host":   lambda h: h in hand.hosts,
			"cond_parent": lambda n: n == parent,
			"cond_else":   lambda: True
		}[type](*args)

	output = f"{hand.url}\n"\
		f"{', '.join(f'{maj}/{min}' for maj, min in mimes)}\n"\
		f"{', '.join(f'@{ic}' for ic in icons)}"

	for cond, cmd in config.config:
		if test_cond(cond):
			util.notify(f"Opening {cmd}", output)
			return cmd
	util.notify(f"Couldn't open :(", output)

def transform_cmd(cmd, h, env):
	if cmd[1]: # Shell command
		out, = subprocess.check_output(["getent", "passwd", str(os.getuid())]).decode().splitlines()
		yield out.split(":")[6]
		yield "-c"
		yield " ".join(map(shlex.quote, cmd[0]))
		os.putenv("TUNA_URL", h.url)
		os.putenv("TUNA_PATH", h.path)
	else: # Plain command
		for arg in cmd[0]:
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
	while args.file.startswith("http:") and not args.file.startswith("http://"):
		# Workaround for https://github.com/mate-desktop/mate-terminal/blob/1.22/src/terminal-util.c#L195
		args.file = "http:/" + args.file[5:]

	try:
		scheme = urllib.parse.urlparse(args.file).scheme
		print(f"[Frozen Tuna] Opening {args.file}", file=sys.stderr)
		h = handler.registry[scheme](args.file)
		print(f"[Frozen Tuna]   Possible mime types: {h.mimes}", file=sys.stderr)
		cmd = get_command(scheme, h)
		print(f"[Frozen Tuna]   {cmd}", file=sys.stderr)
		cmd = list(transform_cmd(cmd, h, os.environ))
		print(f"[Frozen Tuna]   ({cmd})", file=sys.stderr)

	except Exception:
		import traceback
		util.notify("Error", traceback.format_exc())
		raise

	if cmd:
		if not args.dry_run:
			if args.sync:
				os.execlp(*cmd)
			else:
				subprocess.Popen(cmd)
	else:
		util.notify(f"Don't know how to handle {h.url}")

__main__()
