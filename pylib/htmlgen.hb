import contextlib.(contextmanager)

local mangleAttr = fun k:
	if k == "cl": return "class"
	if k.startswith("d_"): return "data-" + k[2:]
	if k.startswith("_"): return k[1:]
	return k

global Tag = class:
	def __init__ = fun @, tag, *children, _open=False, **kwargs:
		@_tag = tag
		@_attrs = {}
		for (k, v) in kwrgs.items:
			@[k] = v
		@_children = children ! list
		@_open = _open

	def name = fun @, tag:
		@_tag = tag

	def add = fun @, *s:
		@_children.extend(s)
	def raw = fun @, s:
		self.add(RawString(s ! str))
	def text = add

	def pop = fun @, n = -1:
		del @_children[n] -- Don't really like this syntax

	def open = fun @, *args, **kwargs:
		@tag(*args, **kwargs, _open=true)

	def __setitem__ = fun @, k, v:
		@_attrs[mangleAttr(k)] = v
	def __getitem__ = fun @, k:
		@_attrs[mangleAttr(k)]
	def __hasitem__ = fun @, k:
		mangleAttr(k) in @_attrs

	def tag = fun @, tag, *args, **kwargs:
		Tag(tag, *args, **kwargs) <! @add

	def __repr__ = fun @:
		`{@_tag}{@_attrs}{@_children}{"!"*@_open}`

	def tohtml = fun @:
		"".join $ @_tohtml()

	def _tohtml = fun @ gen:
		yield "<"
		yield @_tag
		for (k, v) in @_attrs.items():
			yield " "
			yield k
			if v !== None:
				yield "=\""
				yield str(v).replace("&", "&amp;").replace("\"", "&quot;")
				yield "\""
		yield ">"
		if @_open:
			assert not @_children
		else:
			for ch in @_children:
				if hasattr(ch, "_tohtml"): -- Should this be `ch?._append_html`?
					yield* ch._tohtml()
				else:
					yield str(ch).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
			yield "</"
			yield @_tag
			yield ">"

local RawString = class str:
	def _tohtml = fun @:
		yield @

global HtmlStack:
	def __init__ = fun @, *args, doctype="<!DOCTYPE html>", **kwargs:
		@_root = Tag(*args, **kwargs)
		@_stack = [@_root]
		@doctype = doctype

	def tag = fun @, *args, **kwargs:
		local tag = @_stack[-1].tag(*args, **kwargs)
		(contextmanager $ fun gen:
			@_stack.append(tag)
			yield tag
			@_stack.pop()
		)()

	def __getattr__ = fun @, k:
		@_stack[-1].`{k}`

	def __repr__ = fun @, k:
		"HtmlStack" + [*@_stack ! map@(fun a: `{a._tag}{a._attrs}{"!"*a._open}1)]

	def _tohtml = fun @:
		yield* @_root._tohtml()

	def tohtml = fun @:
		@doctype + "\n" + @_root.tohtml() + "\n"
