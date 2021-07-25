# Much is copied (but greatly changed) from tommikaikkonen/prettyprinter
try:
	import wcwidth
except ImportError:
	class wcwidth:
		wcswidth = len

from . import util
from . import doc as d
from . import sdoctypes as sd

def check_fit(stack, *, width, ribbon_width, column):
	stack = util.dfsqueue(stack)
	for indent, prio, inline, doc in stack:
		if doc is d.NIL: continue
		elif doc is d.HARDLINE: column = indent
		elif isinstance(doc, d.Str): column += wcwidth.wcswidth(doc.str)
		elif isinstance(doc, d.Concat):     stack.extend((indent, prio, inline, doc) for doc in doc.docs)
		elif isinstance(doc, d.FlatChoice): stack.append((indent, prio, inline, doc.inline if inline else doc.block))
		elif isinstance(doc, d.Nest):       stack.append((indent + doc.indent * (not inline), prio, inline, doc.doc))
		elif isinstance(doc, d.Contextual): stack.append((indent, prio, inline, doc.func(indent, column, width, ribbon_width)))
		elif isinstance(doc, d.AlwaysBreak): return False
		elif isinstance(doc, d.Group):
			dprio = doc.prio**1.5/(column+1)**0.5
			if dprio < prio: stack.append((indent, max(prio, dprio), True, doc.doc))
		elif isinstance(doc, d.Annotate):   stack.append((indent, prio, inline, doc.doc))
		else: raise ValueError((indent, prio, inline, doc))

		if column > max(width, indent + ribbon_width): return False
	return True

def layout(doc, *, width=79, ribbon_frac=0.9):
	def do_check_fit(stack):
		return check_fit(
			stack,
			width=width,
			ribbon_width=ribbon_width,
			column=column,
		)

	ribbon_width = max(0, min(width, round(ribbon_frac * width)))
	column = 0

	stack = util.dfsqueue([(0, 0, False, doc)])
	for indent, prio, inline, doc in stack:
		if doc is d.NIL: continue
		elif doc is d.HARDLINE: yield sd.SLine(indent); column = indent
		elif isinstance(doc, d.Str): yield doc.str; column += wcwidth.wcswidth(doc.str)
		elif isinstance(doc, d.Concat):      stack.extend((indent, prio, inline, child) for child in doc.docs)
		elif isinstance(doc, d.FlatChoice):  stack.append((indent, prio, inline, doc.inline if inline else doc.block))
		elif isinstance(doc, d.Nest):        stack.append((indent + doc.indent * (not inline), prio, inline, doc.doc))
		elif isinstance(doc, d.Contextual):  stack.append((indent, prio, inline, doc.func(indent, column, width, ribbon_width)))
		elif isinstance(doc, d.AlwaysBreak): stack.append((indent, prio, False, doc.doc))
		elif isinstance(doc, d.Group):
			dprio = doc.prio**1.5/(column+1)**0.5
			fits = do_check_fit([(indent, dprio, True, doc.doc)])
			# if fits: yield "\x1B[1;2;32;40m"
			# else: yield "\x1B[1;2;31;40m"
			# yield f"{dprio:.4}"
			# yield "\x1B[m"
			stack.append((indent, prio if fits else dprio, fits, doc.doc))
		elif isinstance(doc, d.Annotate):
			yield sd.SAnnotationPush(doc.annotation)
			stack.append((indent, prio, inline, doc.doc))
			stack.append((indent, prio, inline, sd.SAnnotationPop(doc.annotation)))
		elif isinstance(doc, sd.SAnnotationPop): yield doc
		else: raise ValueError((indent, prio, inline, doc))
