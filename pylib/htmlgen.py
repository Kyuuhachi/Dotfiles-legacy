import typing as T
from dataclasses import dataclass, field
from functools import partial

from markupsafe import Markup
M = Markup

__all__ = [
	"Node", "Markup", "M"
]

T_Child = T.Union["Node", T.Text]
T_TNode = T.TypeVar("T_TNode", bound="Node")
T_Attr = T.Any

@T.runtime_checkable
class Html(T.Protocol):
	def __html__(self) -> str: ...

@T.runtime_checkable
class HtmlStream(T.Protocol):
	def __html_stream__(self) -> T.Iterable[str]: ...

def mangleAttr(k: str) -> str:
	if k == "cl": return "class"
	if k.startswith("d_"): return "data-" + k[2:]
	if k.startswith("_"): return k[1:]
	return k

def mangleAttrs(attrs: T.Dict[str, T_Attr]) -> T.Dict[str, T_Attr]:
	return { mangleAttr(k): v for k, v in attrs.items() }

@dataclass
class TagData:
	name:     T.Optional[str]
	attrs:    T.Dict[str, T_Attr]         = field(default_factory=dict)
	children: T.Optional[T.List[T_Child]] = field(default_factory=list) # type: ignore # Mypy thinks List[_T] isn't an Optional[List[T_Child]]

def attrprop(name: str, f: T.Callable[[T.Any], T.Any] = lambda self: self) -> T.Any:
	return property(
		lambda self:    getattr(f(self), name),
		lambda self, v: setattr(f(self), name, v),
		lambda self:    delattr(f(self), name),
	)

class Node:
	@T.overload
	def __init__(self, data: TagData, /): ...
	@T.overload
	def __init__(self, name: T.Optional[str] = None, /, *children: T_Child, **attrs: T_Attr): ...

	def __init__(self, fst: T.Union[TagData, T.Optional[str]] = None, /, *args: T.Any, **kwargs: T.Any):
		if isinstance(fst, TagData):
			def _init_1(data: TagData) -> None:
				self._stack = [data]
			_init_1(*args, **kwargs)
		else:
			(T, str) # Workaround for bpo-39215
			def _init_2(name: T.Optional[str] = None, /, *children: T_Child, **attrs: T_Attr) -> None:
				self._stack = [TagData(name, mangleAttrs(attrs), list(children))]
			_init_2(fst, *args, **kwargs)

	stackprop = partial(attrprop, f=lambda self: self._stack[-1])
	name:     T.Optional[str]             = stackprop("name")
	attrs:    T.Dict[str, T_Attr]         = stackprop("attrs")
	children: T.Optional[T.List[T_Child]] = stackprop("children")
	del stackprop

	def append(self, *children: T_Child) -> None:
		if self.children is None: raise TypeError("Node is leaf")
		for child in children:
			if child is None: raise ValueError(child) # Won't happen in well-typed programs, but all programs aren't well-typed
			self.children.append(child)
	def extend(self, children: T.Iterable[T_Child]) -> None:
		self.append(*children)

	def text(self, *s: T.Text) -> None: self.append(*s)
	def raw(self, *s: T.Text) -> None: self.extend(s if isinstance(s, Html) else M(s) for s in s)

	def pop(self, n: int = -1) -> T_Child:
		if self.children is None: raise TypeError("Node is leaf")
		return self.children.pop(n)

	def __setitem__(self, k: str, v: T_Attr) -> None:
		self.attrs[k] = v
	def __getitem__(self, k: str) -> T_Attr:
		return self.attrs[k]
	def __hasitem__(self, k: str) -> bool:
		return k in self.attrs
	def __delitem__(self, k: str) -> None:
		del self.attrs[k]
	def attr(self, **attrs: T_Attr) -> None:
		self.attrs.update(mangleAttrs(attrs))
	def update(self, attrs: T.Dict[str, T_Attr]) -> None:
		self.attrs.update(attrs)

	def root(self) -> "Node":
		return Node(self._stack[0])
	def this(self) -> "Node":
		return Node(self._stack[-1])
	def here(self) -> "Node":
		return self.node(None)

	def node(self: T_TNode, name: T.Optional[str], /, *children: T_Child, **attrs: T_Attr) -> T_TNode:
		node = type(self)(name, *children, **attrs)
		node._parent = self
		self.append(node)
		return node

	def leaf(self: T_TNode, name: str, /, **attrs: T_Attr) -> T_TNode:
		node = self.node(name, **attrs)
		node.children = None
		return node

	_parent: T.Optional["Node"] = None
	def __enter__(self: T_TNode) -> T_TNode:
		if self._parent is None or not self._parent.children or self._parent.children[-1] is not self:
			raise RuntimeError("Not last child of parent, can't enter")
		self._parent._stack.append(self._stack[-1])
		return self

	def __exit__(self: T_TNode, *e: T.Any) -> None:
		if self._parent is None or self._parent._stack[-1] is not self._stack[-1]:
			raise RuntimeError("Not last child of parent, can't exit")
		assert self._parent._stack.pop() is self._stack[-1]

	def __str__(self) -> M:
		return self.__html__()
	def __repr__(self) -> str:
		return str(self._stack)

	def __html__(self) -> M:
		return T.cast(M, M("").join(self.__html_stream__())) # Why is M.join untyped? Must be a bug.

	def __html_stream__(self) -> T.Iterable[M]:
		root = self._stack[0]
		if root.name is not None:
			yield M("<")
			yield M.escape(root.name)
			for k, v in root.attrs.items():
				yield M(" ")
				yield M.escape(k)
				if v is not None:
					yield M("=\"")
					if isinstance(v, (list, tuple)):
						if any(not isinstance(v, str) or " " in v for v in v):
							raise ValueError(v)
						yield M.escape(" ".join(v))
					else:
						yield M.escape(v)
					yield M("\"")
			if root.children is None:
				yield M(" /")
			yield M(">")
		else:
			assert not root.attrs, repr(self)

		if root.children is not None:
			for ch in root.children:
				if isinstance(ch, HtmlStream):
					yield from ch.__html_stream__()
				else:
					yield M.escape((ch))
			if root.name is not None:
				yield M("</")
				yield M.escape(root.name)
				yield M(">")
