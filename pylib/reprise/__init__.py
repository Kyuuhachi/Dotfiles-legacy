import typing as T
import types
from . import asm
import contextvars
import re
import inspect

__all__ = ("reprise_split", "reprise", "reprise_bind", "parse_call")

AnyTuple = T.Tuple[T.Any, ...]
A = T.TypeVar("A")

current_list = contextvars.ContextVar[list[T.Any]]("current_list")

placeholder = "\1%s\2"

def modify_top(f: T.Callable[[A], A]) -> T.Iterator[asm.AnyOp]:
	yield asm.op.LOAD_CONST(f)
	yield asm.op.ROT_TWO
	yield asm.op.CALL_FUNCTION(1)

def modify_call(n: int) -> T.Iterator[asm.AnyOp]:
	yield asm.op.BUILD_TUPLE(n)
	yield asm.op.ROT_TWO
	yield from modify_top(wrapf)
	yield asm.op.ROT_TWO
	yield asm.op.UNPACK_SEQUENCE(n)
	yield asm.op.BUILD_TUPLE(n)
	yield asm.op.UNPACK_SEQUENCE(n)

def modify_format(with_fmt: bool) -> T.Iterator[asm.AnyOp]:
	if with_fmt: yield asm.op.ROT_TWO
	yield from modify_top(Proxy)
	if with_fmt: yield asm.op.ROT_TWO

def modify_modulo() -> T.Iterator[asm.AnyOp]:
	yield asm.op.BUILD_TUPLE(2)
	yield from modify_top(wrap_modulo)
	yield asm.op.UNPACK_SEQUENCE(2)
	yield asm.op.BUILD_TUPLE(2)
	yield asm.op.UNPACK_SEQUENCE(2)

def modify(ops: list[asm.AnyOp]) -> T.Iterator[asm.AnyOp]:
	for op in ops:
		if isinstance(op, asm.Op):
			# The LOAD/CALL_METHOD ops place the callable at a runtime-variable
			# offset, which I think is impossible to deal with correctly. So
			# let's not use those ops.
			if op.op == "LOAD_METHOD": op.op = "LOAD_ATTR"
			if op.op == "CALL_METHOD": op.op = "CALL_FUNCTION"

			# Pass through to called functions
			# Does not work on native functions, including instance creation
			if op.op == "CALL_FUNCTION":    yield from modify_call(op.arg)
			if op.op == "CALL_FUNCTION_KW": yield from modify_call(op.arg+1)
			if op.op == "CALL_FUNCTION_EX": yield from modify_call(1+(op.arg&1))

			# {!r} in f-strings
			if op.op == "FORMAT_VALUE" and op.arg & 3 == 2: yield from modify_format(op.arg & 4 != 0)

			# str % x
			if op.op == "BINARY_MODULO":  yield from modify_modulo()
			if op.op == "INPLACE_MODULO": yield from modify_modulo()
		yield op

def wrap_modulo(ab: tuple[T.Any, T.Any]) -> tuple[T.Any, T.Any]:
	a, b = ab
	if not isinstance(a, str): return a, b
	if isinstance(b, tuple): return a, tuple(Proxy(v) for v in b)
	return a, Proxy(b)

def wrapf(func: T.Callable[..., A]) -> T.Callable[..., A]:
	if isinstance(func, types.FunctionType):
		f = func
		co = f.__code__
		g = types.FunctionType(
			asm.asm(
				list(modify(asm.disasm(co))),
				# I think I only increase the stack by 1, but let's be safe
				co.replace(co_stacksize=co.co_stacksize+2),
			),
			f.__globals__, name=f.__name__,
			argdefs=f.__defaults__, closure=f.__closure__,
		)
		g.__dict__.update(f.__dict__)
		return g

	if isinstance(func, types.MethodType):
		return types.MethodType(wrapf(func.__func__), func.__self__)

	if isinstance(func, types.MethodDescriptorType):
		return lambda self, /, *args, **kwargs: \
			wrapf(func.__get__(self))(*args, **kwargs)

	if isinstance(func, types.BuiltinMethodType):
		if func.__qualname__ == "str.format":
			return lambda *args, **kwargs: \
				func.__self__.format(
					*(Proxy(x) for x in args),
					**{k: Proxy(v) for k, v in kwargs.items()},
				)

		if func.__qualname__ == "str.format_map":
			return lambda mapping, /: \
				func.__self__.format_map(Proxy(mapping))

	if func is repr:
		return tracerepr # type: ignore # mypy doesn't understand that `is` implies type is equal

	return func

class Proxy:
	def __init__(self, value: T.Any) -> None: self.__value = value
	def __getitem__(self, k: T.Any) -> T.Any: return Proxy(self.__value[k])
	def __getattr__(self, k: str)   -> T.Any: return Proxy(getattr(self.__value, k))
	def __format__(self, fmt: str)  -> str:   return format(self.__value, fmt)
	def __str__(self)               -> str:   return str(self.__value)
	def __repr__(self)              -> str:   return tracerepr(self.__value)

def tracerepr(value: T.Any) -> str:
	current_list.get().append(value)
	return placeholder % (len(current_list.get())-1)

def _reprise_raw(obj: T.Any) -> tuple[str, AnyTuple]:
	tok = current_list.set(values := list[T.Any]())
	try:
		a = wrapf(type(obj).__repr__)(obj)
	finally:
		current_list.reset(tok)
	return a, tuple(values)

# Frontend
def _reprise_extract(a: str, values: AnyTuple, subst: str) -> tuple[str, AnyTuple]:
	real_values = []
	def get_value(match: re.Match[str]) -> str:
		real_values.append(values[int(match.group(1))])
		return subst
	return re.sub(placeholder % r"(\d+)", get_value, a), tuple(real_values)

def reprise_split(obj: T.Any) -> tuple[tuple[str, ...], AnyTuple]:
	a, values = _reprise_raw(obj)
	_, real_values = _reprise_extract(a, values, "")	
	return tuple(re.split(placeholder % r"\d+", a)), real_values

def reprise(obj: T.Any, style: T.Literal["%", "{}"] = "{}") -> tuple[str, AnyTuple]:
	a, values = _reprise_raw(obj)
	if style == "%":
		a = a.replace("%", "%%")
	else:
		a = a.replace("{", "{{").replace("}", "}}")
	return _reprise_extract(a, values, "%r" if style == "%" else "{!r}")

def reprise_bind(obj: T.Any, ignore_name: bool = False, partial: bool = False) -> tuple[type, inspect.BoundArguments]:
	t = type(obj)
	name, arguments = parse_call(reprise_split(obj))
	if name not in [t.__name__, t.__qualname__]:
		...

	args = list[T.Any]()
	kwargs = dict[str, T.Any]()
	for argname, argval in arguments:
		if argname is not None:
			if argname in kwargs:
				raise TypeError(f"duplicate kwarg {argname}")
			kwargs[argname] = argval
		else:
			if kwargs:
				raise TypeError("positional args following keyword")
			args.append(argval)

	sig = inspect.signature(t)
	return t, (sig.bind_partial if partial else sig.bind)(*args, **kwargs)

arg_rx = re.compile(r"""
(?:(?:(\w+)\s*=\s*)?\x00)
""", re.VERBOSE)

call_rx = re.compile(fr"""^
\s*
(?P<name>[\w.<>]+) \s*
\( \s*
	(?:{arg_rx.pattern}\s*,\s*)*{arg_rx.pattern}? \s*
\) \s*
$""", re.VERBOSE)

def parse_call(value: tuple[tuple[str, ...], AnyTuple]) -> tuple[str, T.Sequence[tuple[T.Optional[str], T.Any]]]:
	a, values = value
	if any("\0" in b for b in a):
		raise TypeError("repr contains NUL")
	format = "\0".join(a)
	m = call_rx.match(format)
	if m is None:
		raise TypeError("repr does not look like a function call")
	return m.group("name"), [(m.group(1), val) for m, val in zip(arg_rx.finditer(format), values)]

# Limitations:
#   Does not descend into constructors (methods on constructed objects are fine)
#   Does not handle built-in functions, other than those explicitly shimmed
#   Will break in strange ways if something tries to manipulate the repr() output
