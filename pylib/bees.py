import numpy as np
from contextlib import contextmanager
import mmap
import sys

chars = str.maketrans("".join(map(chr, range(32))) + "\x7F", "·␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟␡")

bstr = [f"{x:02X}" for x in range(256)]
def out():
	bstr[0] = f"\x1B[2m{bstr[0]}\x1B[m"
	for x in range(0x20, 0x7F):
		bstr[x] = f"\x1B[38;5;10m{bstr[x]}\x1B[m"
	bstr[255] = f"\x1B[38;5;9m{bstr[255]}\x1B[m"
	np.set_printoptions(suppress=True, linewidth=200, edgeitems=100)

class B(bytes):
	def __repr__(self):
		return " ".join(bstr[x] for x in self)
	__str__ = __repr__

class R:
	def __init__(self, dt, encoding="ascii"):
		self.dt = dt
		self.i = 0
		self.encoding = encoding

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

	def dump(self, n=32, m=48, text=True, encoding=None):
		i = self.i
		for _ in range(n):
			s = self[min(m, self.remaining)]
			if not s and n != 1: break
			print(s, text*s.decode(encoding or self.encoding, errors="replace").translate(chars), file=sys.stderr)
		if n > 1:
			print(file=sys.stderr)
		self.i = i

	def seek(self, i, x=None):
		(i, self.i) = (self.i, i)
		@contextmanager
		def cm():
			yield x
			self.i = i
		return cm()

	def peek(self, t=None):
		if t is None:
			return self._peek()
		else:
			with self._peek():
				return t()
	@contextmanager
	def _peek(self):
		with self.seek(self.i):
			yield

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

def _sign(x, y): return x - 2*(x & y)
