from .. import doc as d
from .. import convert
from .. import color as c

from functools import partial
from collections import defaultdict
import ast
import types
import datetime as dt

@convert.register(object.__repr__, prio=1)
def convert_object(ctx, value):
	return convert.tagged(ctx,
		convert.identifier(ctx, type(value)),
		convert.identity(ctx, value),
	)

@convert.register(type.__repr__)
def convert_type(ctx, value):
	return convert.tagged(ctx,
		"class ",
		convert.identifier(ctx, value),
	)

@convert.register(types.ModuleType.__repr__)
def convert_module(ctx, value):
	if not getattr(value, "__spec__", None): return NotImplemented
	spec = value.__spec__

	name = c.IDENTIFIER(spec.name or "?")
	if spec.origin is None:
		if spec.loader is None:
			vals = []
		else:
			vals = [" ", c.RESET(d.Concat(["(", convert.convert(ctx, spec.loader), ")"]))]
	else:
		if spec.has_location:
			vals = [" from ", c.RESET(spec.origin)]
		else:
			vals = [" ", c.RESET(d.Concat(["(", spec.origin, ")"]))]

	return convert.tagged(ctx,
		"module ",
		name,
		*vals
	)


@convert.register(int.__repr__)
@convert.register(float.__repr__)
@convert.register(bool.__repr__)
@convert.register(type(None).__repr__)
def convert_literal(ctx, value):
	return c.CONSTANT(repr(value))


@convert.register(dict.__repr__)
def convert_dict(ctx, value):
	return convert.bracket(ctx, "{", [
		d.Concat([
			convert.convert(ctx, k),
			":",
			d.Group(25, d.Nest(4, d.Concat([
				d.LINE,
				convert.convert(ctx, v)
			])))
		]) for k, v in value.items()
	], "}", prio=5)

@convert.register(defaultdict.__repr__)
def convert_defaultdict(ctx, value):
	return convert.convert_call_full(ctx, defaultdict, [(None, convert.convert(ctx, value.default_factory)), (None, convert_dict(ctx, value))])

@convert.register(list.__repr__)
def convert_list(ctx, value):
	return convert.bracket(ctx, "[", [
		convert.convert(ctx, v) for v in value
	], "]", prio=1.5)

@convert.register(tuple.__repr__)
def convert_tuple(ctx, value):
	return convert.bracket(ctx, "(", [
		convert.convert(ctx, v) for v in value
	], ")", trailing=len(value)==1)

@convert.register(set.__repr__)
def convert_set(ctx, value):
	if not value: return convert.convert_call(ctx, set)
	return convert.bracket(ctx, "{", [
		convert.convert(ctx, v) for v in value
	], "}", prio=1.5)


@convert.register(partial.__repr__)
def convert_partial(ctx, value):
	return convert.convert_call(ctx, partial, value.func, *value.args, **value.keywords)

@convert.register(None)
def convert_ast(ctx, value):
	if not isinstance(value, ast.AST): return NotImplemented

	import _ast
	if ast.__name__ in ctx.scope.modules and _ast.__name__ not in ctx.scope.modules:
		ctx.scope.modules[_ast.__name__] = ctx.scope.modules[ast.__name__]

	args = {}
	for k in value._fields:
		try:
			args[k] = getattr(value, k)
		except AttributeError:
			pass
	return convert.convert_call(ctx, value.__class__, **args)

# datetime

@convert.register(dt.timedelta.__repr__)
def convert_timedelta(ctx, value):
	args = []
	kwargs = {}
	if value.days: kwargs["days"] = value.days
	if value.seconds: kwargs["seconds"] = value.seconds
	if value.microseconds: kwargs["microseconds"] = value.microseconds
	if not kwargs: args.append(0)
	return convert.convert_call(ctx, dt.timedelta, *args, **kwargs)

@convert.register(dt.date.__repr__)
def convert_date(ctx, value):
	return convert.convert_call(ctx, dt.date, value.year, value.month, value.day)

@convert.register(dt.time.__repr__)
def convert_time(ctx, value):
	args = [value.hour, value.minute, value.second, value.microsecond]
	if not args[-1]: args.pop()
	kwargs = {}
	if value.tzinfo is not None: kwargs["tzinfo"] = value.tzinfo
	if value.fold: kwargs["fold"] = 1
	return convert.convert_call(ctx, dt.time, *args, **kwargs)

@convert.register(dt.datetime.__repr__)
def convert_datetime(ctx, value):
	args = [value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond]
	if not args[-1]: args.pop()
	if not args[-1]: args.pop()
	kwargs = {}
	if value.tzinfo is not None: kwargs["tzinfo"] = value.tzinfo
	if value.fold: kwargs["fold"] = 1
	return convert.convert_call(ctx, dt.datetime, *args, **kwargs)

# @convert.register(dt.tzinfo)
# def convert_tzinfo(ctx, value):
# 	if value is dt.tzinfo.utc:
# 		return c.IDENTIFIER(convert.identifier(ctx, dt.tzinfo) + ".utc")
# 	args = [value.offset]
# 	if value.name is not None: args.append(value.name)
# 	return convert.convert_call(ctx, dt.tzinfo, *args)
