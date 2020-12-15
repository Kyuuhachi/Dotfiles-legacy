import re
from .. import doc as d
from .. import convert

arg_rx = re.compile(r"""
(?:(?:(\w+)\s*=\s*)?\x00(\d+)\x01)
""", re.VERBOSE)

call_rx = re.compile(fr"""^
\s*
(?P<name>[\w.]+) \s*
\( \s*
	(?:{arg_rx.pattern}\s*,\s*)*{arg_rx.pattern}? \s*
\) \s*
$""", re.VERBOSE)

def proxy(vals, obj):
	class ProxyMeta(type):
		def __instancecheck__(self, instance):
			return type(obj).__instancecheck__(self, instance)
		def __subclasscheck__(self, instance):
			return type(obj).__subclasscheck__(self, instance)

		def __getattribute__(self, k):
			if k == "__class__": return type(type(obj))
			return proxy(vals, getattr(type(obj), k))

	class Proxy(metaclass=ProxyMeta):
		# This class assumes that there are no NUL or SOH in the repr, which is
		# generally a quite reasonable assumption

		def __repr__(self):
			vals.append(obj)
			return f"\0{len(vals)-1}\1"

		def __getattribute__(self, k):
			if k == "__class__": return type(obj)
			return proxy(vals, getattr(obj, k))
		def __getitem__(self, k): return proxy(vals, obj[k])
		def __iter__(self): return (proxy(vals, x) for x in obj)
		def __call__(self, *a, **kw): return proxy(vals, obj(*a, **kw))

		def __format__(self, fmt): return format(obj, fmt)
		def __str__(self): return str(obj)
		def __bool__(self): return bool(obj)
		def __hash__(self): return hash(obj)
		def __len__(self): return len(obj)

		def __eq__(self, other): return obj == other
		def __ne__(self, other): return obj != other
		def __lt__(self, other): return obj <  other
		def __gt__(self, other): return obj >  other
		def __le__(self, other): return obj <= other
		def __ge__(self, other): return obj >= other

	if hasattr(obj, "__index__"):
		def __index__(self): return obj.__index__()
		Proxy.__index__ = __index__

	return Proxy()


@convert.register(None, prio=2)
def convert_any(ctx, value):
	if not hasattr(value.__repr__, "__func__"):
		return NotImplemented
	p = proxy(vals := [], value)
	format = str(value.__repr__.__func__(p))
	if (m := call_rx.match(format)) and m.group("name") in [type(value).__name__, type(value).__qualname__]:
		args = []
		# findall doesn't work, it gives empty string rather than None
		for m in arg_rx.finditer(format):
			args.append((m.group(1), convert.convert(ctx, vals[int(m.group(2))])))
		return convert.convert_call_full(ctx, type(value), args)
	else:
		xs = []
		start = 0
		for m in re.finditer(r"\x00(\d+)\x01", format):
			xs.append(format[start:m.start()])
			xs.append(convert.convert(ctx, vals[int(m.group(1))]))
			start = m.end()
		xs.append(format[start:])
		return d.Concat(xs)
