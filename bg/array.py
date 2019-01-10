class Array:
	def __init__(self, w, h, init=lambda:None):
		self.w = w
		self.h = h
		self.data = [[init() for _ in range(h)] for _ in range(w)]

	def _pos(self, pos):
		if isinstance(pos, complex):
			return round(pos.real), round(pos.imag)
		elif isinstance(pos, tuple):
			return pos
		else:
			raise TypeError(pos)

	def __setitem__(self, pos, v):
		x, y = self._pos(pos)
		self.data[x][y] = v
	def __getitem__(self, pos):
		x, y = self._pos(pos)
		return self.data[x][y]
	def __hasitem__(self, pos):
		x, y = self._pos(pos)
		return 0 <= x < self.w and 0 <= y < self.h

# class Array:
# 	def __init__(self, w, h, init=lambda:None):
# 		from collections import defaultdict
# 		self.data = defaultdict(init)

# 	def __setitem__(self, pos, v):
# 		self.data[pos] = v
# 	def __getitem__(self, pos):
# 		return self.data[pos]
