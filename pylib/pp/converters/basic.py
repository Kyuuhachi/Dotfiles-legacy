from .. import doc as d
from .. import convert
from .. import color as c

import collections
import types

@convert.register(int.__repr__)
@convert.register(float.__repr__)
@convert.register(bool.__repr__)
@convert.register(type(None).__repr__)
@convert.register(type(NotImplemented).__repr__)
def convert_literal(ctx, value):
	return c.CONSTANT(repr(value))

@convert.register(type(Ellipsis).__repr__)
def convert_ellipsis(ctx, value):
	return c.CONSTANT("...")


@convert.register(dict.__repr__)
def convert_dict(ctx, value):
	return _convert_dict(ctx, value.items())

def _convert_dict(ctx, items):
	return convert.bracket(ctx, "{", [
		d.Concat([
			convert.convert(ctx, k),
			": ",
			convert.convert(ctx, v)
		]) for k, v in items
	], "}", prio=5)

class Unknown():
	def __pp__(self, ctx):
		return (c.CONSTANT + c.FAINT)("???")

@convert.register(type({}.keys()).__repr__)
def convert_dict_keys(ctx, value):
	return d.Concat([
		_convert_dict(ctx, [(v, Unknown()) for v in value]),
		".keys()",
	])

@convert.register(type({}.values()).__repr__)
def convert_dict_values(ctx, value):
	return d.Concat([
		_convert_dict(ctx, [(Unknown(), v) for v in value]),
		".values()",
	])

@convert.register(type({}.items()).__repr__)
def convert_dict_items(ctx, value):
	return d.Concat([
		_convert_dict(ctx, value),
		".items()",
	])

@convert.register(types.MappingProxyType.__repr__)
def convert_mappingproxy(ctx, value):
	return convert.convert_call_full(ctx, types.MappingProxyType, [
		(None, convert_dict(ctx, value))
	])

@convert.register(collections.defaultdict.__repr__)
def convert_defaultdict(ctx, value: collections.defaultdict):
	return convert.convert_call_full(ctx, collections.defaultdict, [
		(None, convert.convert(ctx, value.default_factory)),
		(None, convert_dict(ctx, value))
	])

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

@convert.register(None)
def convert_namedtuple(ctx, value):
	if not hasattr(type(value), "_fields"): return NotImplemented
	if not hasattr(type(value), "_asdict"): return NotImplemented
	return convert.convert_call(ctx, type(value), **value._asdict())
