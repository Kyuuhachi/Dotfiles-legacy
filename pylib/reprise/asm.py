from __future__ import annotations
import typing as T
import dis
import types
import sys
from collections.abc import Hashable
from collections import defaultdict
import dataclasses as dc
from enum import IntFlag

CO = IntFlag("CO", {k: v for v, k in dis.COMPILER_FLAG_NAMES.items()}) # type: ignore

def create_argtype() -> dict[str, T.Optional[str]]:
	argtype = dict[str, T.Optional[str]]()
	for k, v in dis.opmap.items():
		if v < dis.HAVE_ARGUMENT:
			argtype[k] = None
		else:
			argtype[k] = "int"
			for type in ["const", "free", "name", "jrel", "jabs", "local", "compare"]:
				if v in getattr(dis, f"has{type}"):
					argtype[k] = type
	return argtype
argtype = create_argtype()

AnyOp = T.Union["Op", "Label", "Line"]

@dc.dataclass
class Op:
	op: str
	arg: T.Any

	def __repr__(self) -> str:
		s = f"op.{self.op}"
		if argtype[self.op] is not None: s += f"({self.arg!r})"
		return s

if T.TYPE_CHECKING:
	class CallableOp(Op):
		def __call__(self, arg: T.Any) -> Op: ...

class OpTable:
	__slots__ = ()
	def __getattribute__(self, name: str) -> CallableOp:
		if name not in argtype:
			raise AttributeError
		if argtype[name] is None:
			return Op(name, 0) # type: ignore
		else:
			return lambda arg: Op(name, arg) # type: ignore
op = OpTable()

@dc.dataclass(frozen=True)
class Label:
	key: object = dc.field(default_factory=object)

@dc.dataclass
class Line:
	n: int

def disasm(co: types.CodeType) -> list[AnyOp]:
	ext = 0
	ops = list[tuple[int, Op]]()
	labels = dict[int, Label]()
	for i in range(0, len(co.co_code), 2):
		name, arg = dis.opname[co.co_code[i]], co.co_code[i+1]
		arg += 0x100 * ext
		ext = 0
		if name == "EXTENDED_ARG":
			ext = arg
		else:
			argt = argtype[name]
			if argt == "const": arg2 = co.co_consts[arg]
			elif argt == "name": arg2 = co.co_names[arg]
			elif argt in ["jrel", "jabs"]:
				if argt == "jrel": arg += i+2
				arg2 = labels.setdefault(arg, Label(len(labels)))
			else:
				arg2 = arg
			ops.append((i, Op(name, arg2)))

	lno = {}
	curl = co.co_firstlineno
	curo = 0
	lno[curo] = curl
	for o, l in zip(co.co_lnotab[0::2], co.co_lnotab[1::2]):
		l -= 2*(l&0x80)
		curo += o
		curl += l
		if l != 0:
			lno[curo] = curl

	ops2 = list[AnyOp]()
	for i, op in ops:
		if i in labels: ops2.append(labels[i])
		if i in lno: ops2.append(Line(lno[i]))
		ops2.append(op)
	return ops2

def dump(co: types.CodeType, d: int = 0) -> str:
	co = dis._get_code_object(co) # type: ignore # it does exist
	ops = disasm(co)

	out = []
	out.append("asm([")
	for op in ops:
		out.append("\n" + "\t"*d + "\t")
		if isinstance(op, Op):
			out.append(f"op.{op.op}")
			if argtype[op.op] is not None:
				out.append("(")
				if argtype[op.op] == "const" and isinstance(op.arg, types.CodeType):
					out.append(dump(op.arg, d+1))
				else:
					out.append(repr(op.arg))
				out.append(")")
		else:
			out.append(repr(op))
		out.append(",")
	out.append("\n" + "\t"*d +"]")

	fields = []
	for f in types.CodeType.__dict__:
		if not f.startswith("co_"): continue
		if f in ("co_code", "co_lnotab"):
			fields.append(f'{f}=b""')
		elif f in ("co_names", "co_consts"):
			fields.append(f'{f}=()')
		else:
			fields.append(f'{f}={getattr(co, f)!r}')

	out.append(f", CodeType({', '.join(fields)}))")
	return "".join(out)

@dc.dataclass
class _AsmOp:
	op: str
	arg: int
	pos: int = 0

	def add(self, out: bytearray) -> None:
		assert not self.arg >> 32
		if self.arg > 0xFFFFFF: out.extend([dis.EXTENDED_ARG, (self.arg >> 24) & 0xFF])
		if self.arg > 0xFFFF:   out.extend([dis.EXTENDED_ARG, (self.arg >> 16) & 0xFF])
		if self.arg > 0xFF:     out.extend([dis.EXTENDED_ARG, (self.arg >>  8) & 0xFF])
		out.extend([dis.opmap[self.op], self.arg & 0xFF])
		self.pos = len(out)

@dc.dataclass
class _AsmLabel:
	refs: list[tuple[_AsmOp, bool]]

	def add(self, out: bytearray) -> None:
		for op, isrel in self.refs:
			op.arg = len(out)-op.pos if isrel else len(out)

@dc.dataclass
class _AsmLine:
	line: int
	pos: int = 0

	def add(self, out: bytearray) -> None:
		self.pos = len(out)

_AnyAsmOp = T.Union[_AsmOp, _AsmLabel, _AsmLine]

@dc.dataclass
class _AsmData:
	ops: list[_AnyAsmOp]
	consts: list[T.Any]
	names: list[str]
	nlocals: int

def _asm_ops(ops: list[AnyOp]) -> _AsmData:
	labels = defaultdict[Label, list[tuple[_AsmOp, bool]]](list)

	consts = defaultdict[T.Any, int](lambda: len(consts))
	names = defaultdict[str, int](lambda: len(names))

	aops = list[_AnyAsmOp]()
	nlocals = 0
	for op in ops:
		if isinstance(op, Op):
			argt = argtype[op.op]
			if argt == "const": 
				assert isinstance(op.arg, Hashable)
				arg = consts[op.arg]
			elif argt == "name":
				arg = names[op.arg]
			elif argt in ["jrel", "jabs"]:
				arg = 0
			else:
				if argt == "local":
					nlocals = max(nlocals, op.arg+1)
				arg = op.arg

			assert isinstance(arg, int)
			aop = _AsmOp(op.op, arg)
			aops.append(aop)

			if argt == "jrel":
				labels[op.arg].append((aop, True))
			if argt == "jabs":
				labels[op.arg].append((aop, False))

		elif isinstance(op, Label):
			aops.append(_AsmLabel(labels[op]))

		elif isinstance(op, Line):
			aops.append(_AsmLine(op.n))

	return _AsmData(aops, list(consts), list(names), nlocals)

def _asm_lnotab(lines: T.Sequence[_AsmLine]) -> tuple[int, bytes]:
	lasto = 0
	lastn = first = -1
	lnotab = bytearray()
	for line in lines:
		if line.pos == 0 and first == -1:
			lastn = first = line.line
			continue

		while line.pos - lasto > 0xFF:
			lnotab.extend([0xFF, 0])
			lasto += 0xFF
		lnotab.extend([line.pos - lasto, 0])
		lasto = line.pos

		while line.line - lastn > 0x7F:
			lnotab.extend([0, 0x7F])
			lastn += 0x7F
		while line.line - lastn < -0x80:
			lnotab.extend([0, 0x80])
			lastn += -0x80
		lnotab.extend([0, line.line - lastn & 0xFF])
		lastn = line.line
	return first, bytes(lnotab)

def asm(ops: list[AnyOp], co: types.CodeType) -> types.CodeType:
	data = _asm_ops(ops)

	bytecode = b""
	for a in range(10):
		out = bytearray()
		for op in data.ops:
			op.add(out)
		if bytecode == out:
			break
		bytecode = out
	else:
		raise ValueError("Failed to assemble")

	first_line, lnotab = _asm_lnotab([op for op in data.ops if isinstance(op, _AsmLine)])

	return co.replace(
		co_code = bytes(bytecode),
		co_nlocals = int(data.nlocals),
		co_consts = tuple(data.consts),
		co_names = tuple(data.names),
		co_firstlineno = int(first_line),
		co_lnotab = bytes(lnotab),
	)
