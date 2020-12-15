from dataclasses import dataclass, field
from functools import partial, wraps

### Data enums

@dataclass(frozen=True)
class ClassAttribute:
	val: None
	def __get__(self, instance, owner):
		if instance is None: return self.val
		raise AttributeError()

class DataEnumMeta(type):
	def __call__(cls, *a, **kw):
		if hasattr(cls, "_enum"): raise TypeError("Cannot instantiate data enum")
		return super().__call__(*a, **kw)

	def __iter__(cls):       return iter(cls._enum.values())
	def __contains__(cls, k):
		try:
			cls[k]
			return True
		except KeyError:
			return False
	def __len__(cls):        return len(cls._enum)
	def __reversed__(cls):   return reversed(cls._enum or []) # Workaround for #38525

	def __repr__(cls):
		return f"<enum {cls.__name__}%s>" % "".join(f" {k!r}:{k}" for k in cls)

class DataEnum(metaclass=DataEnumMeta):
	def __class_getitem__(cls, k):
		if k in cls._enum:
			return cls._enum[k]
		raise KeyError(f"{k} is not in {cls.__name__}")

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
		if isinstance(v, t):
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
		def __eq__(a, b): return type(a) == type(b) and a._index == b._index
		def __hash__(self): return hash((type(self), self._index))

	dataclass(**kwargs)(cls)

	@dataclass(**kwargs)
	@wraps(cls, ["__module__", "__name__", "__qualname__", "__doc__", "__annotations__"], [])
	class enum(cls, mixin, _Fields):
		def __init_subclass__(cls, *a, **kw): raise TypeError("Cannot extend data enum class")

	_enum = {}
	_byidx = []
	for i, (name, v, args) in enumerate(items):
		if v in _enum: raise KeyError(f"Duplicate _enum value {v}")
		_enum[v] = enum(i, name, v, *args)
		_byidx.append(_enum[v])
		setattr(enum, name, ClassAttribute(_enum[v]))
		enum.__annotations__[name] = enum
	enum._type = t
	enum._enum = _enum
	enum._byidx = _byidx

	return enum

### Data flags

class BaseDataFlag:
	def __eq__(a, b):
		try: return a._cls == b._cls and a._value == b._value
		except Exception: return False
	def __hash__(a): return hash((a._cls, a._value))

	@staticmethod
	def _merge(a, b, f):
		if a._cls != b._cls: raise TypeError((a._cls, b._cls))
		return DataFlagSet(a._cls, f(a._value, b._value))
	def __or__ (a, b): return BaseDataFlag._merge(a, b, lambda a, b: a|b)
	def __and__(a, b): return BaseDataFlag._merge(a, b, lambda a, b: a&b)
	def __xor__(a, b): return BaseDataFlag._merge(a, b, lambda a, b: a^b)
	def __minus__(a, b):return a & ~b
	def __invert__(a): return a._cls._ALL ^ a

	def __iter__(self):
		val = self._value
		for en in self._cls:
			v = en._value
			if val & v == v:
				yield en
				try:
					val = val & ~v
				except TypeError:
					val -= v
		assert not val

	def __len__(self): return sum(1 for _ in self)

	def __getattr__(self, k):
		if hasattr(self._cls, k): return bool(getattr(self._cls, k) & self)
		else: return getattr(super(), k)

class DataFlagSet(BaseDataFlag):
	def __init__(self, cls, value):
		self._cls, self._value = cls, value

	def __repr__(self):
		if hasattr(self._cls, "__reprs__"):
			return self._cls.__reprs__(self)
		s = []
		for a in self:
			s.append(repr(a))
		return '|'.join(s) or "_NONE"

	def __bool__(self): return bool(self._value)


class DataFlagMeta(DataEnumMeta):
	def __instancecheck__(cls, val):
		if isinstance(val, DataFlagSet): return issubclass(val._cls, cls)
		return super().__instancecheck__(val)

	@property
	def _NONE(cls):
		return cls._type()

	@property
	def _ALL(cls):
		val = cls._NONE
		for v in cls:
			val |= v._value
		return DataFlagSet(cls, val)

class DataFlag(BaseDataFlag, metaclass=DataFlagMeta):
	def __class_getitem__(cls, val):
		val2 = val
		for en in cls:
			v = en._value
			if val2 & v == v:
				try:
					val2 = val2 & ~v
				except TypeError:
					val2 -= v
		if val2:
			raise KeyError(f"{val2} is not in {cls.__name__} (from {val})")
		return DataFlagSet(cls, val)

	@property
	def _cls(self): return self.__class__

dataflag = partial(dataenum, mixin=DataFlag)
