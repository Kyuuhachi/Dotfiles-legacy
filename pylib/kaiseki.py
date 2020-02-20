import numpy as np
import dataclasses
from dataclasses import dataclass, field
from contextlib import contextmanager
from os import isatty
import mmap
import sys
import re

__all__ = ["Reader"]

escape = re.compile("[\x00-\x1F\x7F\x80-\x9F]")

class B(bytes):
	def __repr__(self):
		return " ".join("%02X" % x for x in self)
	__str__ = __repr__

@dataclass
class Reader:
	dt: bytes = field(repr=False)
	encoding: str = "ascii"
	i: int = 0

	def __setitem__(self, n, v):
		if isinstance(v, int):
			v = (v % 256**n).to_bytes(n, "little")
		if isinstance(v, list):
			v = bytes(v)
		v2 = self.dt[self.i:self.i+n]
		if v != v2:
			try: a = " (%s)" % escape.sub("·", v.decode(self.encoding))
			except: a = ""
			try: b = " (%s)" % escape.sub("·", v2.decode(self.encoding))
			except: b = ""
			raise ValueError(f"At 0x{self.i:04x}: expected '{B(v)!s}'{a}, found '{B(v2)!s}'{b}")
		self.i += n

	def __getitem__(self, n):
		v = self.dt[self.i:self.i+n]
		if len(v) != n:
			raise ValueError(f"At 0x{self.i:04x}: tried to read {n} bytes, but only {len(v)} were available")
		self.i += n
		return B(v)

	def byte(self):
		v = self.dt[self.i]
		self.i += 1
		return v

	@property
	def remaining(self):
		return len(self.dt) - self.i

	def __bool__(self):
		return self.remaining != 0

	def __len__(self):
		return len(self.dt)

	def one(self, dtype):
		return self.some(1, dtype)[0]

	def some(self, shape, dtype):
		x = np.ndarray(shape, dtype, buffer=self.dt, offset=self.i)
		self.i += x.nbytes
		return x

	def until(self, delim, size=None):
		if size:
			v = self[size]
			try: v = v[:v.index(delim)]
			except ValueError: pass
		else:
			i = self.dt.find(delim, self.i)
			if i == -1: raise ValueError(f"Did not find delimiter '{delim}'")
			v = self.dt[self.i:i]
			self.i = i+len(delim)
		return B(v)

	def at(self, i=None):
		return dataclasses.replace(self, i=i if i is not None else self.i)

	def u1(self): return self.byte()
	def u2(self): return self.u1() | self.u1() <<  8
	def u4(self): return self.u2() | self.u2() << 16
	def u8(self): return self.u4() | self.u4() << 32

	def i1(self): return _sign(self.u1(), 1<< 7)
	def i2(self): return _sign(self.u2(), 1<<15)
	def i4(self): return _sign(self.u4(), 1<<31)
	def i8(self): return _sign(self.u8(), 1<<63)

	def f4(self, *, allow_nan=False):
		a = self.one("f4")
		if not allow_nan and not np.isfinite(a):
			raise ValueError(float(a))
		return float(a)

	def zstr(self, size=None, encoding=None, errors="strict"):
		return self.until(b"\0", size).decode(encoding or self.encoding, errors=errors)

	def __iter__(self):
		while self.remaining:
			yield self.byte()

	@classmethod
	@contextmanager
	def open(cls, file, *args, **kwargs):
		with open(file, "rb") as f:
			yield cls(mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ), *args, **kwargs)

	def dump(self, *,
			start=None, lines=None, length=None, end=None,
			width=None, encoding="auto", mark=frozenset(), file=sys.stderr):
		if start is None:
			start = self.i

		mark = frozenset(mark)

		if encoding == "auto": encoding = self.encoding
		if width is None:      width = 72 if encoding is None else 48

		assert (lines is not None) + (length is not None) + (end is not None) <= 1
		if   length is not None: length = length
		elif end    is not None: length = end - start
		elif lines  is not None: length = lines * width
		else:                    length = width

		if hasattr(file, "fileno") and isatty(file.fileno()):
			fmt = ""
			def format(f):
				nonlocal fmt
				if f != fmt:
					hl.append("\x1B[m")
					hl.append(fmt := f)
		else:
			def format(f): pass

		hl = []
		for i in range(start, start+length, width):
			chunk = self.dt[i:min(i+width, start+length)]
			if not chunk: break

			format("")
			hl.append("{:0{}X}".format(i, len("%X" % len(self))))
			hl.append(" ")

			for j, b in enumerate(chunk, i):
				if   0x00 == b       : newfmt = "\x1B[2m"
				elif 0x20 <= b < 0x7F: newfmt = "\x1B[38;5;10m"
				elif 0xFF == b       : newfmt = "\x1B[38;5;9m"
				else:                  newfmt = ""

				format(newfmt)
				hl.append("%02X" % b)

				if j+1 == self.i:
					format("\x1B[7m")
				elif j+1 in mark:
					format("")

				hl.append("•" if j+1 in mark else " ")

			if encoding is not None:
				format("")
				hl.append(escape.sub("·", chunk.decode(encoding, errors="replace")))
			else:
				hl.pop() # Trailing space
			hl.append("\n")

		if hl and 0 < length <= width:
			hl.pop()
		format("")
		print("".join(hl), file=file)

def _sign(x, y): return x - 2*(x & y)
