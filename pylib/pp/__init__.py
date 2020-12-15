from dataclasses import dataclass
import sys
import types

from . import converters # noqa
from . import convert, render, layout
from . import doc as d

@dataclass
class Context:
	scope: "Scope"
	at: [bool,str]

@dataclass
class Scope:
	module: str
	modules: dict
	ids: dict

def findscope(depth):
	modules = {}
	ids = {}
	f = sys._getframe(depth+1)
	module = {**f.f_globals, **f.f_locals}
	for k, v in module.items():
		if not k.startswith("_"):
			if type(v) == types.ModuleType:
				modules[v.__name__] = k + "."
			ids[id(v)] = k

	modules[module["__name__"]] = ""

	return Scope(module["__name__"], modules, ids)

def prepr(v, width=79, *, at=False, contextdepth=0):
	ctx = Context(
		scope=findscope(depth=contextdepth+1),
		at=at,
	)
	return render.render(
		layout.layout(
			convert.convert(ctx, v),
			width=width,
		),
	)

def pprint(*v, width=79, at=False, contextdepth=0, sep=" ", **kwargs):
	ctx = Context(
		scope=findscope(depth=contextdepth+1),
		at=at,
	)
	out = []
	for v in v:
		if out: out.append(sep)
		out.append(convert.convert(ctx, v))
	return print(render.render(
		layout.layout(
			d.Concat(out),
			width=width,
		),
	), **kwargs)
