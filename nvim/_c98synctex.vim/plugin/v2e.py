import sys
import dbus
from pathlib import Path

ed = "org.gnome.evince."
es = "/org/gnome/evince/"

_pdf = Path(sys.argv[1]).as_uri()
_r, _c = int(sys.argv[2]), int(sys.argv[3])
_path = sys.argv[4]

bus = dbus.SessionBus()
name = bus.call_blocking(f"{ed}Daemon", f"{es}Daemon", f"{ed}Daemon",
	"FindDocument", "sb", (_pdf, True), timeout=0.1)
window_list = bus.call_blocking(name, f"{es}Evince", f"{ed}Application",
	"GetWindowList", "", (), timeout=0.1)
bus.call_blocking(name, window_list[0], f"{ed}Window",
	"SyncView", "s(ii)u", (_path, (_r, _c), 0), timeout=0.1)
