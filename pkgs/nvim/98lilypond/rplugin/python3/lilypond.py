import neovim
import ly
import ly.document
import ly.indent
import ly.words

alignable_words = {
	"and", "or", "cond", "begin"
	"<", "<=", "=", "=>", '>', "eq?", "eqv?", "equal?",
}

def is_alignable(self, token):
	return isinstance(token, ly.lex.scheme.Word) and token in alignable_words
ly.indent.Line.is_alignable_scheme_keyword = is_alignable
del is_alignable

@neovim.plugin
class LilypondIndent:
	def __init__(self, nvim):
		self.nvim = nvim # type: neovim.api.nvim.Nvim

	@neovim.function("LilypondIndent", range=True, sync=True)
	def indent(self, args, range): # TODO this really should work relatively, not absolutely.
		i = ly.indent.Indenter()
		i.indent_width = self.nvim.current.buffer.options["ts"]
		i.indent_tabs = False
		lnum = self.nvim.vvars["lnum"] - 1
		text = "\n".join(self.nvim.current.buffer)
		indent = ly.document.Document(text)
		i.indent(ly.document.Cursor(indent))
		indent = i.get_indent(indent, indent[lnum])
		return len(indent.expandtabs(i.indent_width))
