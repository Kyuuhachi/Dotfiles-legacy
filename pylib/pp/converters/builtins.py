from .. import doc as d
from .. import convert
import typing as T

import functools
import ast
import types
import datetime as dt
import pathlib

@convert.register(functools.partial.__repr__)
def convert_partial(ctx, value: functools.partial):
	return convert.convert_call(ctx, type(value), value.func, *value.args, **value.keywords)

@convert.register(None)
def convert_ast(ctx, value: T.Any):
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

@convert.register(types.SimpleNamespace.__repr__)
def convert_simplenamespace(ctx, value: types.SimpleNamespace):
	return convert.convert_call(ctx, type(value), **value.__dict__)

@convert.register(dt.timedelta.__repr__)
def convert_timedelta(ctx, value: dt.timedelta):
	args = []
	kwargs = {}
	if value.days: kwargs["days"] = value.days
	if value.seconds: kwargs["seconds"] = value.seconds
	if value.microseconds: kwargs["microseconds"] = value.microseconds
	if not kwargs: args.append(0)
	return convert.convert_call(ctx, dt.timedelta, *args, **kwargs)

@convert.register(dt.date.__repr__)
def convert_date(ctx, value: dt.date):
	return convert.convert_call(ctx, dt.date, value.year, value.month, value.day)

@convert.register(dt.time.__repr__)
def convert_time(ctx, value: dt.time):
	args = [value.hour, value.minute, value.second, value.microsecond]
	if not args[-1]: args.pop()
	kwargs = dict[str, T.Any]()
	if value.tzinfo is not None: kwargs["tzinfo"] = value.tzinfo
	if value.fold: kwargs["fold"] = 1
	return convert.convert_call(ctx, dt.time, *args, **kwargs)

@convert.register(dt.datetime.__repr__)
def convert_datetime(ctx, value: dt.datetime):
	args = [value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond]
	if not args[-1]: args.pop()
	if not args[-1]: args.pop()
	kwargs = dict[str, T.Any]()
	if value.tzinfo is not None: kwargs["tzinfo"] = value.tzinfo
	if value.fold: kwargs["fold"] = 1
	return convert.convert_call(ctx, dt.datetime, *args, **kwargs)

@convert.register(pathlib.PurePath.__repr__)
def convert_path(ctx, value: pathlib.PurePath):
	import os
	remaps: dict[type[pathlib.PurePath], type[pathlib.PurePath]]
	remaps = ({
		pathlib.PureWindowsPath: pathlib.PurePath,
		pathlib.WindowsPath: pathlib.Path,
	} if os.name == "nt" else {
		pathlib.PurePosixPath: pathlib.PurePath,
		pathlib.PosixPath: pathlib.Path,
	})
	cls = remaps.get(type(value), type(value))

	if issubclass(cls, pathlib.Path) and value.is_relative_to(cls.home()):
		rel = cls("~")/value.relative_to(cls.home())
		return d.Concat([
			convert.convert_call(ctx, cls, rel.as_posix()),
			".expanduser()",
		])

	return convert.convert_call(ctx, cls, value.as_posix())
