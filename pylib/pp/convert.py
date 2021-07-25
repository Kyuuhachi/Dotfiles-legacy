import functools
from . import doc as d
from . import color as c

converters = []
def register(what, prio=0):
	def wrapper(func):
		if what is not None:
			func2 = lambda ctx, v: func(ctx, v) if type(v).__repr__ is what else NotImplemented
		else:
			func2 = lambda ctx, v: func(ctx, v)
		functools.wraps(func)(func2)
		func2._prio = prio

		# Can't use bisect here since it doesn't support key
		lo, hi = 0, len(converters)
		while lo < hi:
			mid = (lo+hi)//2
			if func2._prio < converters[mid]._prio: hi = mid
			else: lo = mid+1
		converters.insert(lo, func2)

		return func
	return wrapper

@register(None, prio=float("-inf"))
def convert_pp(ctx, value):
	for t in type(value).__mro__:
		if "__pp__" in t.__dict__:
			return value.__pp__(ctx)
		if "__repr__" in t.__dict__: # If a subclass overrides repr but not pp, don't use that pp
			break
	return NotImplemented

@register(None, prio=float("inf"))
def convert_repr(ctx, value):
	fail = c.Color((41,))
	return d.Concat([
		identifier(ctx, type(value)),
		fail("("),
		repr(value),
		fail(")"),
	])

def convert(ctx, value):
	for f in converters:
		try:
			v = f(ctx, value)
			if v is NotImplemented: continue
			return c.RESET(v)
		except Exception as e:
			import sys
			print(f"{value!r}: {e!r}\n", file=sys.stderr)
			import traceback
			traceback.print_exc()
	assert False, "convert_repr should catch everything"

def convert_call(ctx, func, /, *args, **kwargs):
	return convert_call_full(ctx, func, [(None, convert(ctx, v)) for v in args] + [(k, convert(ctx, v)) for k, v in kwargs.items()])

def convert_call_full(ctx, func, args):
	if not isinstance(func, d.Doc):
		func = identifier(ctx, func)
	items = []
	for i, (k, v) in enumerate(args):
		if k is not None:
			items.append(d.Concat([c.ARGUMENT(k), "=", v]))
		else:
			items.append(v)
	return d.Concat([func, bracket(ctx, "(", items, ")")])

def bracket(ctx, start, items, end, trailing=False, prio=1):
	if not items:
		return d.Concat([start, end])
	out = []
	for i, v in enumerate(items):
		if i:
			out.append(",")
			out.append(d.LINE)
		out.append(v)
	if trailing and out:
		out.append(",")
	return d.Group(len(items)*prio,
		d.Concat([
			start,
			d.Nest(4, d.Concat([d.SOFTLINE] + out)), d.SOFTLINE,
			end,
		])
	)

def identifier(ctx, what):
	if id(what) in ctx.scope.ids:
		name = ctx.scope.ids[id(what)]
	else:
		name = what.__qualname__
		name = name.replace("<lambda>", "λ")
		name = name.replace(".<locals>.", ":")
		name = moduleprefix(ctx, what) + name
	return c.IDENTIFIER(name)

def moduleprefix(ctx, what):
	scope = ctx.scope
	module = what.__module__

	if module in ["builtins", scope.module, None]:
		return ""

	suffix = ""
	while True:
		if module in scope.modules:
			return scope.modules[module] + suffix
		if "." not in module:
			return what.__module__+"."
		[module, nextsuffix] = module.rsplit(".", 1)
		suffix += nextsuffix + "."

def identity(ctx, what):
	if ctx.at is False:
		return ""
	elif ctx.at is True:
		pos = c.FAINT(f"{id(what):x}")
	elif ctx.at == "color":
		pos = c.Color((38,5,16+hash(what)%216))(f"{id(what):x}")
	else:
		raise ValueError(ctx.at)
	return d.Concat([c.FAINT(" at 0x"), pos])

def tagged(ctx, *args):
	return c.TAGGED(d.Concat(["<", *args, ">"]))
