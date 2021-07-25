import Xlib
import Xlib.display
from Xlib import Xatom as XA
import subprocess
from pathlib import Path

try:
	d = Xlib.display.Display()
	owner = d.get_selection_owner(XA.PRIMARY)
	pid = owner.get_full_property(d.get_atom("_NET_WM_PID"), XA.CARDINAL).value[0]

	focus = d.get_input_focus().focus
	pid2 = focus.get_full_property(d.get_atom("_NET_WM_PID"), XA.CARDINAL).value[0]
	if pid != pid2: exit()

	pwd = focus.get_full_text_property(d.get_atom("TERM_PWD"), d.get_atom("UTF8_STRING"))
except Exception:
	pwd = None

text = subprocess.check_output(["xclip", "-o"], encoding="utf8")
path = Path(text.strip()).expanduser()
if pwd is not None:
	pwd = Path(pwd)
else:
	pwd = Path("~").expanduser()

subprocess.check_call(["drag", pwd/path])
