import sys
import importlib.util
from pathlib import Path

for f in sys.path:
	path = Path(f) / "PIL/__init__.py"
	if path.exists():
		spec = importlib.util.spec_from_file_location(__name__, path)
		break

mod = importlib.util.module_from_spec(spec)
sys.modules[__name__] = mod
spec.loader.exec_module(mod)
del f, path, mod, spec


import inspect
import tempfile
import subprocess
import shlex

def find_original_caller(arg):
	f = sys._getframe()
	while True:
		locals = f.f_locals
		for a in inspect.signature(type(lambda:0)(f.f_code, {})).parameters:
			if locals.get(a) is arg:
				break
		else:
			return f
		f = f.f_back

outdir = Path(tempfile.gettempdir()) / "pil-imageshow"
	
def show(image, title=None, command=None):
	if title is None:
		caller = find_original_caller(image)
		title = f"{caller.f_code.co_filename}:{caller.f_code.co_name}"
	if not outdir.exists():
		outdir.mkdir(parents=True)
	file = outdir / f"{str(title).replace('/', '%')}.png"
	image.save(file)
	command = "eog {0} &> /dev/null".format(shlex.quote(str(file)))
	subprocess.Popen(command, shell=True)
	
import PIL.ImageShow
PIL.ImageShow.__dict__.clear()
PIL.ImageShow.show = show
