from lualex import LuaLex
class LexIter:
	def __init__(self, v):
		self.items = list(v)
		self.pos = -1
	def __iter__(self):
		return self
	def __next__(self):
		self.pos += 1
		if self.pos >= len(self.items): raise StopIteration
		return self.items[self.pos]
	def peek(self, n=1):
		if self.pos+n >= len(self.items): return None
		return self.items[self.pos+n][0]
	def back(self):
		self.pos -= 1

class Var:
	def __init__(self, name, p, type):
		self.name = name
		self.type = type
		self.p = p
		self.refs = []

	def ref(self, p, how):
		self.refs.append((p, how))

	def __repr__(self):
		return self.name.decode() + "{" + self.type + "}" + str(self.p) + "@" + str(self.refs)

class Scope:
	def __init__(self, parent, func=False):
		self.vars = {}
		self.parent = parent
		self.func = func
		self.varlist = parent.varlist
	def new(self, name, p, how="local"):
		self.vars[name] = Var(name, p, how)
		self.varlist.append(self.vars[name])
	def ref(self, name, p, how="local"):
		if name in self.vars:
			self.vars[name].ref(p, how)
		elif name == b"..." and self.func:
			self.new(name, p, how="error")
		else:
			self.parent.ref(name, p, "upvalue" if self.func else how)
class GlobalScope:
	def __init__(self, varlist):
		self.vars = {}
		self.varlist = varlist
	def ref(self, name, p, how="local"):
		if name not in self.vars:
			self.vars[name] = Var(name, p, "global")
			self.varlist.append(self.vars[name])
		self.vars[name].ref(p, "global")

def walkGlobal(vars, it):
	scope = GlobalScope(vars)
	scope = Scope(scope)
	scope.vars[b"_ENV"] = Var(b"_ENV", (-1, -1, -1), "env")
	scope.varlist.append(scope.vars[b"_ENV"])
	scope = Scope(scope, True)
	while it.pos < len(it.items):
		walkStatements(it, scope)
		it.pos += 1

def walkStatements(it, scope):
	for tok, p in it:
		if tok == "function":
			if type(it.peek()) == bytes:
				name, p = next(it)
				scope.ref(name, p)
			walkFunction(it, scope)
		elif tok == "do":
			walkStatements(it, Scope(scope))
		elif tok == "while":
			walkExpression(it, scope)
			if it.peek() == "do":
				next(it)
				walkStatements(it, Scope(scope))
		elif tok == "for":
			walkFor(it, scope)
		elif tok == "if" or tok == "elseif":
			walkExpression(it, scope)
			if it.peek() == "then":
				next(it)
				walkStatements(it, Scope(scope))
			if it.peek() == "else":
				next(it)
				walkStatements(it, Scope(scope))
		elif tok == "local":
			walkLocal(it, scope)
		elif tok == "end":
			break
		elif tok == "else" or tok == "elseif":
			it.back()
			break
		else:
			it.back()
			idx = it.pos
			walkExpression(it, scope)
			if it.pos == idx:
				next(it)

def walkFor(it, scope):
	scope2 = Scope(scope)
	for tok, p in it:
		if type(tok) == bytes:
			scope2.new(tok, p, "loop")
		else:
			it.back()
			break
		if it.peek() == ",":
			next(it)
		else:
			break
	if it.peek() == "in" or it.peek() == "=":
		next(it)
		for tok, p in it:
			walkExpression(it, scope)
			if it.peek() == ",":
				next(it)
			else:
				break
		if it.peek() == "do":
			next(it)
			walkStatements(it, Scope(scope2))

def walkLocal(it, scope):
	if it.peek() == "function":
		next(it)
		if type(it.peek()) == bytes:
			name, p = next(it)
			scope.new(name, p)
		walkFunction(it, scope)
	else:
		new = []
		for tok, p in it:
			if type(tok) == bytes:
				new.append((tok, p))
			else:
				walkExpression(it, scope)
			if it.peek() == ",":
				next(it)
			else:
				break
		if it.peek() == "=":
			for tok, p in it:
				walkExpression(it, scope)
				if it.peek() == ",":
					next(it)
				else:
					break
		for tok, p in new:
			scope.new(tok, p)

def walkFunction(it, scope):
	scope = Scope(scope, True)
	if it.peek() == "(":
		next(it)
		for tok, p in it:
			if type(tok) == bytes:
				scope.new(tok, p, "arg")
			elif tok == ",":
				pass
			elif tok == ")":
				break
			else:
				it.back()
				break
	walkStatements(it, scope)

def walkExpression(it, scope):
	while it.peek() in ["not", "#", "-", "~"]:
		next(it)
	if not it.peek(): return
	tok, p = next(it)

	if type(tok) == bytes:
		scope.ref(tok, p)
	elif tok == "junk":
		pass
	elif tok == "{":
		walkTable(it, scope)
		if it.peek() == "}":
			next(it)
	elif tok == "(":
		walkExpression(it, scope)
		if it.peek() == ")":
			next(it)
	elif tok == "function":
		walkFunction(it, scope)
	else:
		it.back()
		return

	for tok, p in it:
		if tok == "junk":
			pass
		elif tok == "{":
			walkTable(it, scope)
			if it.peek() == "}":
				next(it)
		elif tok == "(" or tok == "[":
			walkExpression(it, scope)
			if it.peek() == ")" or tok == "]":
				next(it)
		else:
			it.back()
			break

	if it.peek() in ["..", "and", "or", "not"]:
		next(it)
		walkExpression(it, scope)
	elif it.peek() in "+-*/^%&~|<>=~#":
		while it.peek() in "+-*/^%&~|<>=~#":
			next(it)
		walkExpression(it, scope)

def walkTable(it, scope):
	for tok, p in it:
		if type(tok) == bytes and it.peek() == "=" and it.peek(2) != "=":
			next(it)
			continue
		elif tok == "[":
			walkExpression(it, scope)
			if tok == "]":
				next(it)
		elif it.peek() == ",":
			continue
		elif it.peek() == "}":
			it.back()
			break
		else:
			it.back()
			idx = it.pos
			walkExpression(it, scope)
			if it.pos == idx:
				next(it)


f = open("foo.lua", "rb").read()
state = 0
vars = []
def lines(f, toks):
	line = 0
	lineStart = -1
	lineEnd = -1
	for tok, (s, e) in toks:
		while s > lineEnd:
			lineStart = lineEnd+1
			lineEnd = f.find(b"\n", lineStart)
			line += 1
		assert e <= lineEnd
		yield tok, (line, s-lineStart+1, e-lineStart)
walkGlobal(vars, LexIter(lines(f, LuaLex(f).lex())))
for v in vars:
	print(v)
