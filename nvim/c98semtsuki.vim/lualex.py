ident = set(map(str.encode, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"))
keywords = {
	b"and", b"break", b"do", b"else", b"elseif", b"end", b"false", b"for", b"function", b"goto", b"if", b"in",
	b"local", b"nil", b"not", b"or", b"repeat", b"return", b"then", b"true", b"until", b"while"
}

class LuaLex:
	__slots__ = ["offset", "src"]

	def __init__(self, src):
		self.src = src
		self.offset = 0

	def peek(self, s):
		if isinstance(s, bytes):
			if self.src.startswith(s, self.offset):
				self.offset += len(s)
				return True
			return False
		if isinstance(s, int):
			return self.src[self.offset:self.offset+s]

	def skip_bracket(self):
		assert self.peek(b"[")
		n = 0
		while self.peek(b"="):
			n += 1
			self.offset += 1
		self.offset = self.src.find(b"=" * n + b"]", self.offset) % (len(self.src) + 1) + n+1

	def skip_string(self, quote):
		while self.offset < len(self.src):
			if self.peek(quote) or self.peek(b"\n"):
				break
			elif self.peek(b"\\"):
				if self.peek(b"\\") or self.peek(quote) or self.peek(b"\n"):
					pass
				elif self.peek(b"z"):
					while self.peek(1).isspace():
						self.offset += 1
			else:
				self.offset += 1

	def token(self):
		if self.peek(b"..."): return b"..."
		if self.peek(b".."): return ".."
		if self.peek(b".") or self.peek(b":"):
			while self.peek(1) in ident:
				self.offset += 1
			return None
		if self.peek(b"::"): return "::"
		if self.peek(2) in [b"[[", b"[="]: self.skip_bracket(); return "junk"
		if self.peek(b"\""): self.skip_string(b"\""); return "junk"
		if self.peek(b"\'"): self.skip_string(b"\'"); return "junk"
		if self.peek(b"--"):
			if self.peek(2) in [b"[[", b"[="]: self.skip_bracket()
			else: self.offset = self.src.find(b"\n", self.offset) + 1 % (len(self.src) + 1) + 1
			return None
		if self.peek(1).isdigit():
			while self.peek(b".") or self.peek(1) in ident:
				self.offset += 1
			return "junk"
		if self.peek(1) in ident:
			start = self.offset
			while self.peek(1) in ident:
				self.offset += 1
			word = self.src[start:self.offset]
			if word in [b"true", b"false", b"nil"]:
				return "junk"
			if word in [b"and", b"or", b"not"]:
				return "op"
			if word in keywords:
				return word.decode()
			return word
		ch = self.peek(1)
		self.offset += 1
		return ch.decode()

	def lex(self):
		if self.src.startswith(b"#"):
			self.offset = (self.src.find(b"\n") + 1) % (len(self.src) + 1)
		while True:
			while self.peek(1).isspace(): self.offset += 1
			start = self.offset
			t = self.token()
			if t is None: continue
			if t == "": break
			yield t, (start, self.offset)
