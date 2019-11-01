#!/usr/bin/env hebi
import argparse.(ArgumentParser)
import urllib.parse.(urlparse)
import handler
import os
import subprocess
import sys.(stderr)
import config
import mime
import util.(notify)
import shlex

local get_icons = fun mimes:
	set $ gen:
		for m in mimes:
			if m in mime.ICONS:
				local icon = mime.ICONS[m]
				if icon.endswith("-x-generic"):
					yield icon[:-10]
			else:
				yield m.split("/", 1)[0]

local get_command = fun scheme, hand:
	local mimes = hand.mimes ! map@(fun a: a.split("/")) ! set
	local icons = get_icons(hand.mimes)
	local mimeClasses = mimes ! map@(fun (type,_): type) ! set
	local parent = with open(`/proc/{os.getppid()}/cmdline", "rb") as f:
		f.read().split(0x'00')[0].decode()

	local test_cond = fun (type, args):
		{
			cond_or     -> fun *cs: any(cs ! map@(test_cond(c)))
			cond_and    -> fun *cs: all(cs ! map@(test_cond(c)))
			cond_mime   -> fun t, s: (t, s) in mimes
			cond_mime2  -> fun t: t in mimeClasses
			cond_icon   -> fun i: i in icons
			cond_scheme -> fun s: s == scheme
			cond_host   -> fun h: h in hand.hosts
			cond_parent -> fun n: n == parent
			cond_else   -> fun: true
		}[type](*args)

	local output = "\n".join $ gen:
		yield hand.url
		yield ", ".join $ mimes ! map@(fun (maj, min): `{maj}/{min}`)
		yield ", ".join $ icons ! map@(fun ic: `@{ic}`

	for cond, cmd in config.config if test_cond(cond):
		notify(`Opening {cmd}`, output)
		return cmd
	notify("Couldn't open.", output)

local transform_cmd = fun (cmd, isshell), h, env:
	list $ gen:
		if isshell:
			local out = subprocess.check_output(["getent", "passwd", os.getuid() ! str]).decode()[:-1]
			yield out.split(":")[6] -- Shell
			yield "-c"
			yield cmd ! map@(shlex.quote) ! " ".join
			os.putenv("TUNA_URL", h.url)
			os.putenv("TUNA_PATH", h.path)
		else for arg in cmd:
			if arg.startswith("$"):
				yield env[arg[1:]]
			else if arg.startswith("%"):
				local (_, c) = arg
				if c == "u": yield h.url
				else if c == "f": yield h.path
				else: raise ValueError(arg)
			else:
				yield arg

global argp = ArgumentParser() <! fun @:
	@add_argument("-n", "--dry-run", action="store_true", help="Don't open the file, only figure out how")
	@add_argument("-s", "--sync",    action="store_true", help="Don't fork, so you can wait for the process to close") # TODO make detection also async
	@add_argument("file")

if __main__:
	local args = argp.parse_args()

	local cmd = try:
		local scheme = urlparse(args.file).scheme
		print(`[Frozen Tuna] Opening {args.file}`, file=stderr)
		local h = handler.registry[scheme](args.file)
		print(`[Frozen Tuna]   Possible mime types: {h.mimes}`, file=stderr)
		local cmd = get_command(scheme, h)
		print(`[Frozen Tuna]   {cmd}`, file=stderr)
		local cmd = transform_cmd(cmd, h, os.environ)
		print(`[Frozen Tuna]   ({cmd})`, file=stderr)
		cmd
	except:
		notify("Error", import traceback..format_exc())
		raise

	if not cmd:
		notify(`Don't know how to handle {h.url}`)
	else if args.dry_run:
		pass
	else if args.sync:
		os.execlp(*cmd)
	else:
		subprocess.Popen(cmd)
