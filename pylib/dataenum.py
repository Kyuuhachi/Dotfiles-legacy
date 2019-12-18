import dataclasses
from dataclasses import dataclass, field, fields
from functools import partial, wraps

### Data enums

class DataEnumMeta(type):
	def __call__(cls, *a, **kw):
		if hasattr(cls, "_enum"): raise TypeError("Cannot instantiate data enum")
		return super().__call__(*a, **kw)

	def __iter__(cls):       return iter(cls._enum)
	def __len__(cls):        return len(cls._enum)
	def __reversed__(cls):   return reversed(cls._enum or []) # Workaround for #38525

	def __repr__(cls):
		return f"<enum {cls.__name__}%s>" % "".join(f" {k!r}:{cls._enum[k]}" for k in cls)

class DataEnum(metaclass=DataEnumMeta):
	def __class_getitem__(cls, k): return cls._enum[k]

def dataenum(cls=None, /, **kwargs):
	if not cls: return lambda cls: dataenum(cls, **kwargs)

	kwargs.setdefault("frozen", True)
	kwargs.setdefault("repr", False)
	kwargs.setdefault("eq", False)
	t = kwargs.pop("type", int)
	mixin = kwargs.pop("mixin", DataEnum)

	if not hasattr(cls, "__annotations__"): cls.__annotations__ = {}

	items = []
	for name, v in list(cls.__annotations__.items()):
		if type(v) is t:
			args = getattr(cls, name, ())
			if type(args) != tuple: args = (args,)
			items.append((name, v, args))
			del cls.__annotations__[name]
			if hasattr(cls, name): delattr(cls, name)

	@dataclass(**kwargs)
	class _Fields:
		_index: int  = field(repr=False)
		_name:  str  = field(repr=False)
		_value: None = field(repr=False)
		def __repr__(self): return self._name
		def __eq__(a, b): (type(a), a._index) == (type(b), b._index)
		def __hash__(self): return hash((type(self), self._index))

	dataclass(**kwargs)(cls)

	@dataclass(**kwargs)
	@wraps(cls, ["__module__", "__name__", "__qualname__", "__doc__", "__annotations__"], [])
	class enum(cls, mixin, _Fields):
		def __init_subclass__(cls, *a, **kw): raise TypeError("Cannot extend data enum class")

	_enum = {}
	for i, (name, v, args) in enumerate(items):
		if v in _enum: raise KeyError(f"Duplicate _enum value {v}")
		setattr(enum, name, enum(i, name, v, *args))
		_enum[v] = getattr(enum, name)
		enum.__annotations__[name] = enum
	enum._enum = _enum

	return enum

### Data flags

class BaseDataFlag:
	def __eq__(a, b): return (a._cls, a._value) == (b._cls, b._value)
	def __hash__(a): return hash((a._cls, a._value))

	def __or__ (a, b): return BaseDataFlag._merge(a, b, lambda a, b: a|b)
	def __and__(a, b): return BaseDataFlag._merge(a, b, lambda a, b: a&b)
	def __xor__(a, b): return BaseDataFlag._merge(a, b, lambda a, b: a^b)

	@staticmethod
	def _merge(a, b, f):
		if a._cls != b._cls: raise TypeError((a._cls, b._cls))
		return DataFlagSet(a._cls, f(a._value, b._value))

	def __invert__(a):
		all = a._value
		for b in a._cls:
			all = all | a._cls._enum[b]._value
		return DataFlagSet(a._cls, all ^ a._value)

	def __iter__(self):
		val = self._value
		for v in self._cls:
			if val & v == v:
				yield self._cls._enum[v]
				try:
					val = val & ~v
				except TypeError:
					val -= v
		if val: raise KeyError(val)

	def __len__(self):  return sum(1 for _ in self)

class DataFlagSet(BaseDataFlag):
	def __init__(self, cls, value): self._cls, self._value = cls, value

	def __repr__(self):
		if hasattr(self._cls, "__reprs__"): return self._cls.__reprs__(self)
		s = []
		try:
			for a in self:
				s.append(repr(a))
		except KeyError as e:
			s.append(f"<{e}>")
		return '|'.join(s) or f"<empty>"


class DataFlagMeta(DataEnumMeta):
	def __instancecheck__(cls, val):
		if isinstance(val, DataFlagSet): return issubclass(val._cls, cls)
		return super().__instancecheck__(val)

class DataFlag(BaseDataFlag, metaclass=DataFlagMeta):
	def __class_getitem__(cls, val): return DataFlagSet(cls, val)
	@property
	def _cls(self): return self.__class__

dataflag = partial(dataenum, mixin=DataFlag)

### Test

if __name__ == "__main__":
	@dataflag
	class StatGuard:
		# a:int=1
		POISON : 1 << 0
		FREEZE : 1 << 1
		PETRIFY: 1 << 2
		SLEEP  : 1 << 3
		MUTE   : 1 << 4
		BLIND  : 1 << 5
		SEAL   : 1 << 6
		CONFUSE: 1 << 7
		FAINT  : 1 << 8
		DEATH  : 1 << 9
		RAGE   : 1 << 11

		# def __repr__(self): return "b"

	print(StatGuard[0xFFF])
	print(StatGuard[0])
	print(StatGuard[1] | StatGuard.FREEZE)
	print(list(StatGuard.POISON))
	print(len(StatGuard.POISON))
	print(~StatGuard.POISON)
	print(bool(StatGuard.POISON))
	print(bool(StatGuard[1]))
	print(isinstance(StatGuard.POISON, StatGuard))
	print(isinstance(StatGuard[0], StatGuard))
	print(isinstance(StatGuard[0xFFFF], StatGuard))

	print(StatGuard[1] == StatGuard.POISON)
	print({StatGuard[1], StatGuard[1], StatGuard.POISON, StatGuard.POISON})
