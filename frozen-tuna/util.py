import os
import os.path
import subprocess
XDG_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
XDG_DATA_DIRS = os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":")

def getFiles(name):
	ret = []
	for dir in [XDG_HOME] + XDG_DATA_DIRS:
		path = os.path.join(dir, name)
		if os.path.exists(path) and path not in ret:
			ret.append(path)
	return ret

TEXT_CHARS = bytes([7, 8, 9, 10, 12, 13, 27]) + bytes(range(0x20, 0x100))
def isBinaryString(bytes):
	return bool(bytes.translate(None, TEXT_CHARS))

def notify(*args):
	subprocess.Popen(["notify-send", *args])
