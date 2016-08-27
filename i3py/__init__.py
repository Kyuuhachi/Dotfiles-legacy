import Xlib.threaded
import Xlib.display
import i3ipc
import os
import sys
import i3py.util

stdout = sys.stdout
sys.stdout = os.fdopen(os.dup(sys.stderr.fileno()), "w", 1)
sys.stderr = sys.stdout

i3ipc.WorkspaceEvent = lambda data, conn: data
i3ipc.GenericEvent = lambda data: data
i3ipc.WindowEvent = lambda data, conn: data
i3ipc.BarconfigUpdateEvent = lambda data: data
i3ipc.BindingEvent = lambda data: data
i3ipc.Con = lambda data, parent, conn: data

display = Xlib.display.Display()
i3 = i3ipc.Connection()

def reload():
	python = sys.executable
	os.execl(python, python, *sys.argv)

i3.subscriptions = 0xFF
i3py.util.OtherThread(i3.main)()
