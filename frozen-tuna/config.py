import appdirs
import lark
import os.path

fn = os.path.join(os.path.dirname(__file__), "config.g")
parser = lark.Lark(open(fn).read(), parser="lalr", lexer="contextual")

def parse(f):
	def parse_cond(c):
		if isinstance(c, lark.Tree):
			return (c.data, [parse_cond(c2) for c2 in c.children])
		return str(c)
	def parse_cmd(c, type):
		if type == "shcmd":
			return str(c.children[0])
		if type == "plaincmd":
			return [str(c2) for c2 in c.children]
	cfg = parser.parse(f.read())
	lines = []
	for l in cfg.children:
		cond, cmd = l.children
		cond = parse_cond(cond)
		cmd = parse_cmd(cmd, l.data)
		lines.append((cond, cmd))
	return lines

with open(appdirs.user_config_dir("frozen-tuna.cfg")) as f:
	config = parse(f)
del f
