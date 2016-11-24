#!/usr/bin/env python3
import socket
import dbus

def getUPower():
	obj = dbus.SystemBus().get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	return dbus.Interface(obj, "org.freedesktop.UPower")

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/var/run/acpid.socket")

for l in sock.makefile("r"):
	l = l.rstrip('\n')
	type, name, cmd = l.split(maxsplit=2)
	if (type, name, cmd) == ("button/lid", "LID", "close"):
		getUPower().Suspend()
	print(type, name, cmd)

# 'button/lid LID close\n'
# 'button/lid LID open\n'
