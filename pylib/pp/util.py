class dfsqueue:
	def __init__(self, init=()):
		self.stack = list(init)
		self.top = None

	def append(self, *item):
		self.stack.extend(item)

	def extend(self, items):
		self.stack.extend(items)

	def __iter__(self):
		assert self.top is None, "Multiple concurrent iterations not supported"
		s = self.stack
		self.top = 0
		while s:
			s[self.top:] = s[self.top:][::-1]
			val = s.pop()
			self.top = len(s)
			yield val
		self.top = None

	@property
	def items(self):
		stack = list(self.stack)
		stack[self.top:] = stack[self.top:][::-1]
		return stack[::-1]

	def __repr__(self):
		return f"dfsqueue({self.items!r})"
