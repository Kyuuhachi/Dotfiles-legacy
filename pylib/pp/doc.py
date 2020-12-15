class DocMeta(type):
	def __call__(cls, *a, **kw):
		return cls.__new__(cls, *a, **kw)

class Doc(metaclass=DocMeta):
	__slots__ = ()

	def __new__(cls, *a, **kw):
		if cls is Doc:
			def __new__(cls, /, arg):
				if isinstance(arg, cls): return arg
				if isinstance(arg, str): return Str(arg)
				raise ValueError(arg)
			return __new__(cls, *a, **kw)
		else:
			v = object.__new__(cls)
			v.__init__(*a,**kw)
			return v


class NIL(Doc):
	""" An empty token. Probably little reason to use this externally. """
	__slots__ = ()
	def __repr__(self):
		return "NIL"
NIL = NIL()


class Str(Doc):
	""" Wraps a string. Shouldn't be used externally. """
	__slots__ = ("str",)

	def __init__(self, s):
		self.str = s

	def __new__(cls, s):
		assert isinstance(s, str)
		if s == "": return NIL
		return super().__new__(cls, s)
	
	def __repr__(self):
		return repr(self.str)

class Group(Doc):
	""" Tries to layout its child on one line if possible, otherwise breaks it. """
	__slots__ = ("prio", "doc",)

	def __init__(self, prio, doc):
		self.prio = prio
		self.doc = doc

	def __new__(cls, prio, doc):
		assert isinstance(prio, (int, float))
		doc = Doc(doc)
		if doc is NIL: return NIL
		if isinstance(doc, AlwaysBreak): return doc
		return super().__new__(cls, float(prio), doc)

	def __repr__(self):
		return f"Group({self.prio!r}, {self.doc!r})"


class Concat(Doc):
	""" Concatenates its children. """
	__slots__ = ("docs",)

	def __init__(self, docs):
		self.docs = docs

	def __new__(cls, docs):
		docs_ = []
		for doc in docs:
			doc = Doc(doc)
			if doc is NIL: continue
			elif isinstance(doc, Concat): docs_.extend(doc.docs)
			else: docs_.append(doc)

		if len(docs_) == 0: return NIL
		if len(docs_) == 1: return docs_[0]

		return super().__new__(cls, docs_)

	def __repr__(self):
		return f"Concat({self.docs!r})"


class Annotate(Doc):
	"""Annotates ``doc`` with the arbitrary value ``annotation``"""
	__slots__ = ("doc", "annotation")

	def __init__(self, annotation, doc):
		self.annotation = annotation
		self.doc = doc

	def __new__(cls, ann, doc):
		return super().__new__(cls, ann, Doc(doc))

	def __repr__(self):
		return f"Annotate({self.annotation!r}, {self.doc!r})"


class Contextual(Doc):
	"""Returns a Doc that is lazily evaluated when deciding the layout.
	
	``fn`` must be a function that accepts four arguments:
	- ``indent`` (``int``): the current indentation level, 0 or more
	- ``column`` (``int``) the current output column in the output line
	- ``page_width`` (``int``) the requested page width (character count)
	- ``ribbon_width`` (``int``) the requested ribbon width (character count)
	"""
	__slots__ = ("func",)

	def __init__(self, func):
		self.func = func

	def __new__(cls, func):
		import inspect
		inspect.signature(func).bind(0, 0, 0, 0)
		return super().__new__(cls, func)

	def __repr__(self):
		return f"Contextual({self.func!r})"


def Align(doc):
	""" Aligns each new line in ``doc`` with the first new line. """
	def align(indent, column, page_width, ribbon_width):
		return Nest(column - indent, doc)
	return Contextual(align)

def Hang(i, doc):
	return Align(Nest(i, doc))

class Nest(Doc):
	__slots__ = ("indent", "doc")
	def __init__(self, indent, doc):
		self.indent = indent
		self.doc = doc

	def __new__(cls, indent, doc):
		assert isinstance(indent, int)
		return super().__new__(cls, indent, Doc(doc))

	def __repr__(self):
		return f"Nest({self.indent!r}, {self.doc!r})"


class FlatChoice(Doc):
	"""
	Allows different rendering depending on whether the object is rendered inline or block.
	"""
	__slots__ = ("block", "inline")
	def __init__(self, block, inline):
		self.block = block
		self.inline = inline

	def __new__(cls, block, inline):
		return super().__new__(cls, Doc(block), Doc(inline))

	def __repr__(self):
		return f"FlatChoice({self.block!r}, {self.inline!r})"


class HARDLINE(Doc):
	__slots__ = ()
	def __repr__(self):
		return "HARDLINE"
HARDLINE = HARDLINE()
LINE = FlatChoice(HARDLINE, " ")
SOFTLINE = FlatChoice(HARDLINE, NIL)


class AlwaysBreak(Doc):
	__slots__ = ("doc",)

	def __init__(self, doc):
		assert isinstance(doc, Doc), type(doc)
		self.doc = doc

	def __new__(cls, doc):
		doc = Doc(doc)
		if doc is NIL: return NIL
		if isinstance(doc, AlwaysBreak): return doc
		return super().__new__(cls, doc)

	def __repr__(self):
		return f"AlwaysBreak({self.doc!r})"
