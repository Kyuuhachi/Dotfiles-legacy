from Xlib.display import Display
import i3ipc
import os
import sys

stdout = sys.stdout
sys.stdout = os.fdopen(os.dup(sys.stderr.fileno()), "w", 1)

display = Display()
i3 = i3ipc.Connection()

def reload():
	python = sys.executable
	os.execl(python, python, *sys.argv)
