from .. import doc as d
from .. import convert
from .. import color as c
import typing as T
from pathlib import Path
import dis
from weakref import WeakKeyDictionary

import sys
import types

@convert.register(object.__repr__, prio=1)
def convert_object(ctx, value: object):
	return convert.tagged(ctx,
		convert.identifier(ctx, type(value)),
		convert.identity(ctx, value),
	)

@convert.register(type.__repr__)
def convert_type(ctx, value: type):
	return convert.tagged(ctx,
		"class ",
		convert.identifier(ctx, value),
	)

# Extracting data
prefixes = dict[Path, Path]()
if sys.prefix != "/usr":
	prefixes[Path(sys.prefix)] = Path("$env")
prefixes[Path.home()] = Path("~")

def _get_module_path(path: Path) -> Path:
	for prefix, name in prefixes.items():
		if path.is_relative_to(prefix):
			return name / path.relative_to(prefix)
	return path

def _get_module_path_s(path: str) -> str:
	return str(_get_module_path(Path(path)))

_module_path_cache = dict[str, types.ModuleType]() # path → module
_seen_modules = set[str]() # module id
def _get_module_by_path(path: str) -> T.Optional[types.ModuleType]:
	if path in _module_path_cache:
		return _module_path_cache[path]

	for modid in sys.modules.keys() - _seen_modules:
		mod = sys.modules[modid]
		if isinstance(mod, types.ModuleType) and mod.__spec__ and mod.__spec__.has_location and mod.__spec__.origin is not None:
			_module_path_cache[mod.__spec__.origin] = mod

	return _module_path_cache.get(path)

#

@convert.register(types.ModuleType.__repr__)
def convert_module(ctx, value: types.ModuleType):
	spec = value.__spec__
	if spec is None: return NotImplemented

	name = c.IDENTIFIER(spec.name or "?")
	if spec.origin is None:
		if spec.loader is None:
			vals = []
		else:
			vals = [" ", c.RESET(d.Concat(["(", convert.convert(ctx, spec.loader), ")"]))]
	else:
		if spec.has_location:
			vals = [" from ", c.RESET(_get_module_path_s(spec.origin))]
		else:
			vals = [" ", c.RESET(d.Concat(["(", spec.origin, ")"]))]

	return convert.tagged(ctx, "module ", name, *vals)

@convert.register(types.FrameType.__repr__)
def convert_frame(ctx, value: types.FrameType):
	# <frame at 0xXXXX, file '/xx/xxx', line xx, code xx>
	return convert.tagged(ctx, repr(value)[1:-1])
