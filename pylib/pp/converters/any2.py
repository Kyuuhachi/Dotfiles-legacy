import re
from .. import doc as d, convert
import reprise

arg_rx = re.compile(r"""
(?:(?:(\w+)\s*=\s*)?\x00)
""", re.VERBOSE)

call_rx = re.compile(fr"""^
\s*
(?P<name>[\w.]+) \s*
\( \s*
	(?:{arg_rx.pattern}\s*,\s*)*{arg_rx.pattern}? \s*
\) \s*
$""", re.VERBOSE)

@convert.register(None, prio=1)
def convert_any(ctx, value):
	if not hasattr(value.__repr__, "__func__"):
		return NotImplemented

	a, values = reprise.reprise_split(value)
	try:
		name, args = reprise.parse_call((a, values))
		if name in [type(value).__name__, type(value).__qualname__]:
			name = convert.identifier(ctx, type(value))
		return convert.convert_call_full(ctx, name, [
			(k, convert.convert(ctx, v))
			for k, v in args
		])
	except TypeError:
		xs = []
		for b, val in zip(a, values):
			xs.append(b)
			xs.append(convert.convert(ctx, val))
		xs.append(a[-1])
		return d.Concat(xs)
