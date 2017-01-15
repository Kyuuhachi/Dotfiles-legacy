#!/usr/bin/env python3
import socket
import subprocess

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/var/run/acpid.socket")

for l in sock.makefile("r"):
	l = l.rstrip('\n')
	type, name, cmd = l.split(maxsplit=2)
	if (type, name, cmd) == ("button/lid", "LID", "close"):
		subprocess.Popen(["xtype", "-s", "XF86_Standby"])
