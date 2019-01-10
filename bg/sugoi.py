import draw
from array import Array

class Maze:
	__slots__ = ["gridx", "gridy", "w", "h"]
	def __init__(self, w, h):
		self.w, self.h = w, h
		self.gridx = Array(w, h, lambda: False)
		self.gridy = Array(w, h, lambda: False)

	def is_open(self, pos, d):
		# if not self.can_open(pos, d): return False
		if d == 1:   return self.gridx[pos]
		if d == -1:  return self.gridx[pos+d]
		if d == 1j:  return self.gridy[pos]
		if d == -1j: return self.gridy[pos+d]

	def open(self, pos, d):
		if d == 1:   self.gridx[pos] = True
		if d == -1:  self.gridx[pos+d] = True
		if d == 1j:  self.gridy[pos] = True
		if d == -1j: self.gridy[pos+d] = True

	def can_open(self, pos, d):
		pos += d
		return 0 <= pos.real < self.w and 0 <= pos.imag < self.h

	def dump(self):
		s = []
		for y in range(self.h+1):
			for x in range(self.w+1):
				s.append("█" if y < self.h and not self.is_open((x+y*1j), -1) else "▀")
				s.append("▀" if x < self.w and not self.is_open((x+y*1j), -1j) else " ")
			s.pop()
			s.append("\n")
		s.pop()
		return "".join(s)

def __main__():
	import argparse
	import random
	argp = argparse.ArgumentParser()
	argp.add_argument("w", type=int)
	argp.add_argument("h", type=int)
	argp.add_argument("seed", type=int)
	argp.add_argument("hue", type=float)
	args = argp.parse_args()
	rand = random.Random(args.seed)

	maze = Maze(args.w, args.h)
	rand.choice([randwall(False), randwall(True), unionfind])(rand, maze)
	print(maze.dump())

	# num_cells = 32
	# dist = draw.calc_distance(maze, draw.initpts(maze, rand, num_cells))
	# maxdist = {}
	# for (w, d) in (b for a in dist.data for b in a):
	# 	maxdist[w] = max(maxdist.get(w, 1), d)
	# imgdata = draw.draw_maze(maze, dist)
	# print(maxdist)

	# from PIL import Image
	# img = Image.new("RGB", (imgdata.w, imgdata.h))
	# def gradient(which, dist):
	# 	if which == -1:
	# 		return draw.hsv2rgb(args.hue, 0.5, 0.5)
	# 	dist /= maxdist[which]
	# 	return draw.hsv2rgb(args.hue + (which/num_cells - 0.5)/3, 0.2 + 0.8*dist, 1 - 0.6*dist)
	# for x in range(imgdata.w):
	# 	for y in range(imgdata.h):
	# 		img.putpixel((x, y), gradient(*imgdata[x, y]))
	# img.show()

def randwall(corridor):
	def randwall(rand, maze):
		def can_open(pos, d):
			return (pos + d) not in used and maze.can_open(pos, d)
		def add(pos):
			used.add(pos)
			for d in [1,-1,1j,-1j]:
				if can_open(pos, d):
					walls.append((pos, d))
		used = set()
		walls = []
		add(rand.randrange(maze.w)+rand.randrange(maze.h)*1j)
		while walls:
			idx = rand.randrange(len(walls))
			walls[-1], walls[idx] = walls[idx], walls[-1]
			pos, d = walls.pop()
			while can_open(pos, d):
				maze.open(pos, d)
				pos += d
				add(pos)
				if not corridor: break
	return randwall

class UnionFind:
	def __init__(self):
		self._id = {}
		self._sz = {}

	def _root(self, a):
		i = self._id
		if a not in i:
			self._id[a] = a
			self._sz[a] = 1
			return a
		while a != i[a]:
			b = i[a]; i[a] = i[b]; a = b
		return a

	def union(self, *args):
		args = [self._root(a) for a in args]
		root = max(*args, key=self._sz.__getitem__)
		sz = 0
		for a in args:
			self._id[a] = root
			sz += self._sz[a]
			del self._sz[a]
		self._sz[root] = sz

	def find(self, *args):
		args = [self._root(a) for a in args]
		return all(x == args[0] for x in args)

def unionfind(rand, maze):
	uf = UnionFind()
	walls = []
	walls += [((x+y*1j), 1) for x in range(maze.w-1) for y in range(maze.h)]
	walls += [((x+y*1j), 1j) for x in range(maze.w) for y in range(maze.h-1)]
	while walls:
		idx = rand.randrange(len(walls))
		walls[-1], walls[idx] = walls[idx], walls[-1]
		pos, d = walls.pop()
		pos2 = pos + d
		if not uf.find(pos, pos2):
			maze.open(pos, d)
			uf.union(pos, pos2)

if __name__ == "__main__": __main__()
