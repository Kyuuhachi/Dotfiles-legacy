from contextlib import contextmanager

def mangleAttr(k):
	if k == "cl": return "class"
	if k.startswith("d_"): return "data-" + k[2:]
	if k.startswith("_"): return k[1:]
	return k

class Tag:
	def __init__(self, tag, *children, _open=False, **kwargs):
		self._tag = tag
		self._attrs = {}
		for k, v in kwargs.items():
			self[k] = v
		self._children = list(children)
		self._open = _open

	def name(self, tag):
		self._tag = tag

	def add(self, *s):
		self._children.extend(s)
	def raw(self, s):
		self.add(RawString(str(s)))
	text = add

	def pop(self, n=-1):
		del self._children[n]

	def open(self, *args, **kwargs):
		return self.tag(*args, **kwargs, _open=True)

	def __setitem__(self, k, v):
		self._attrs[mangleAttr(k)] = v
	def __getitem__(self, k):
		return self._attrs[mangleAttr(k)]
	def __hasitem__(self, k):
		return mangleAttr(k) in self._attrs

	def tag(self, tag, *args, **kwargs):
		tag = Tag(tag, *args, **kwargs)
		self.add(tag)
		return tag

	def __repr__(self):
		return f"{self._tag}{self._attrs}{self._children}{'!'*self._open}"

	def tohtml(self):
		s = []
		self._append_html(s)
		return "".join(s)

	def _append_html(self, s):
		s.append("<")
		s.append(self._tag)
		for k, v in self._attrs.items():
			s.append(" ")
			s.append(k)
			if v is not None:
				s.append("=\"")
				s.append(str(v).replace("&", "&amp;").replace("\"", "&quot;"))
				s.append("\"")
		s.append(">")
		if self._open:
			assert not self._children
		else:
			for ch in self._children:
				if hasattr(ch, "_append_html"):
					ch._append_html(s)
				else:
					s.append(str(ch).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
			s.append("</")
			s.append(self._tag)
			s.append(">")

class RawString(str):
	def _append_html(self, s):
		s.append(self)

class HtmlStack:
	def __init__(self, *args, doctype="<!DOCTYPE html>", **kwargs):
		self._root = Tag(*args, **kwargs)
		self._stack = [self._root]
		self.doctype = doctype

	def tag(self, *args, **kwargs):
		tag = self._stack[-1].tag(*args, **kwargs)
		@contextmanager
		def f():
			self._stack.append(tag)
			yield tag
			self._stack.pop()
		return f()
	__call__ = tag

	def __getattr__(self, k):
		return getattr(self._stack[-1], k)

	def __repr__(self):
		return "HtmlStack" + str([f"{x._tag}{x._attrs}{'!'*x._open}" for x in self._stack])

	def _append_html(self, s):
		self._root._append_html(s)

	def tohtml(self):
		return self.doctype + "\n" + self._root.tohtml() + "\n"
