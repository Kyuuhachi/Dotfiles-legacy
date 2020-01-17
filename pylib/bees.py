import numpy as np
import dataclasses
from dataclasses import dataclass, field
from contextlib import contextmanager
import mmap
import sys

chars = str.maketrans("".join(map(chr, range(32))) + "\x7F", "·␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟␡")

class B(bytes):
	def __repr__(self):
		return " ".join("%02X" % x for x in self)
	__str__ = __repr__

@dataclass
class R:
	dt: bytes = field(repr=False)
	encoding: str = "ascii"
	i: int = 0

	def __setitem__(self, n, v):
		if isinstance(v, int):
			v = (v % (1<<(n*8))).to_bytes(n, "little")
		v2 = self.dt[self.i:self.i+n]
		if v != v2:
			try: a = f" ({v.decode(self.encoding).translate(chars)})"
			except: a = ""
			try: b = f" ({v2.decode(self.encoding).translate(chars)})"
			except: b = ""
			raise ValueError(f"At 0x{self.i:04x}: expected '{B(v)!s}'{a}, found '{B(v2)!s}'{b}")
		self.i += len(v)

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
	def __bool__(self): return self.remaining != 0

	def __len__(self): return len(self.dt)

	def one(self, dtype):
		return self.some(1, dtype)[0]
	__call__ = one
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

	def dump(self, *,
			start=None, lines=None, length=None, end=None,
			width=None, encoding="auto", mark=frozenset(), file=sys.stderr):
		if start is None:
			start = self.i

		mark = frozenset(mark)

		if encoding == "auto":
			encoding = self.encoding
		if width is None:
			width = 72 if encoding is None else 48

		assert (lines is not None) + (length is not None) + (end is not None) <= 1
		if length is not None:
			length = start + length
		elif end is not None:
			length = end - start
		elif lines is not None:
			length = lines * width
		else:
			length = width
		del lines
		del end

		fmt = ""
		def format(f):
			nonlocal fmt
			if f != fmt:
				hl.append("\x1B[m")
				hl.append(fmt := f)

		hl = []
		for i in range(start, start+length, width):
			chunk = self.dt[i:min(i+width, start+length)]
			if not chunk: break

			for j, b in enumerate(chunk, i):
				if   0x00 == b       : newfmt = "\x1B[2m"
				elif 0x20 <= b < 0x7F: newfmt = "\x1B[38;5;10m"
				elif 0xFF == b       : newfmt = "\x1B[38;5;9m"
				else:                   newfmt = ""

				format(newfmt)
				hl.append("%02X" % b)

				if j+1 == self.i:
					format("\x1B[7m")
				elif j+1 in mark:
					format("")

				hl.append("•" if j+1 in mark else " ")

			if encoding is not None:
				format("")
				hl.append(chunk.decode(encoding, errors="replace").translate(chars))
			else:
				hl.pop() # Trailing space
			hl.append("\n")

		if 0 < length <= width:
			hl.pop()
		format("")
		print("".join(hl), file=file)

	def at(self, i=None):
		return dataclasses.replace(self, i=i if i is not None else self.i)

	@classmethod
	@contextmanager
	def open(cls, file, *args, **kwargs):
		with open(file, "rb") as f:
			yield cls(mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ), *args, **kwargs)

	def u1(self): return self.byte()
	def u2(self): return self.u1() | self.u1() <<  8
	def u4(self): return self.u2() | self.u2() << 16
	def u8(self): return self.u4() | self.u4() << 32
	def s1(self): return _sign(self.u1(), 1<< 7)
	def s2(self): return _sign(self.u2(), 1<<15)
	def s4(self): return _sign(self.u4(), 1<<31)
	def s8(self): return _sign(self.u8(), 1<<63)
	def f4(self): return float(self(self._f4))
	_f4 = np.dtype("f4")
	def zstr(self, size=None, encoding=None, errors="strict"):
		return self.until(b"\0", size).decode(encoding or self.encoding, errors=errors)

	def __iter__(self):
		while self.remaining:
			yield self.byte()

def _sign(x, y): return x - 2*(x & y)
