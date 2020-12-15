from .. import doc as d
from .. import convert
from .. import color as c

@convert.register(str.__repr__)
def convert_str(ctx, value):
	if value == "":
		return c.STRING('""')
	return _string(value, "")

printable_bytes = frozenset(range(32, 127)) | frozenset(b"\r\n\t")
@convert.register(bytes.__repr__)
def convert_bytes(ctx, value):
	def show(string):
		o = []
		delim = "'" if '"' in string and "'" not in string else '"'
		for s in string:
			esc = repr(s)[1:-1]
			if s == "\u3000":
				esc = s
			if s == delim:
				esc = "\\" + s
			o.append(c.FAINT(esc) if esc != s else esc)
		return c.STRING(d.Concat([delim] + o + [delim]))

	if value == b"":
		return c.STRING('b""')

	if value == bytes(len(value)):
		return convert.convert_call(ctx, bytes, len(value))

	if all(x in printable_bytes for x in value):
		return _string(value.decode("ascii"), "b")

	def byte(b):
		if b == 0:
			return c.FAINT(f"{b:02X}")
		if b in printable_bytes:
			return c.ITALIC(f"{b:02X}")
		return f"{b:02X}"

	bs = [byte(b) for b in value]

	return convert.convert_call_full(ctx, bytes.fromhex, [(None, d.Concat(bs))])

def _string(value, prefix):
	def show(string):
		o = []
		delim = "'" if '"' in string and "'" not in string else '"'
		for s in string:
			esc = repr(s)[1:-1]
			if s == "\u3000":
				esc = s
			if s == delim:
				esc = "\\" + s
			o.append(c.FAINT(esc) if esc != s else esc)
		return c.STRING(d.Concat([prefix, delim] + o + [delim]))

	inline = show(value)
	block = []
	for i, line in enumerate(value.splitlines(True)):
		if i:
			block.append(d.HARDLINE)
		block.append(show(line))

	return d.Align(d.Group(len(block)*4, d.FlatChoice(
		d.Concat([
			"(",
			d.Nest(4, d.Concat([d.HARDLINE, *block])),
			d.HARDLINE,
			")"
		]),
		c.STRING(inline),
	)))
