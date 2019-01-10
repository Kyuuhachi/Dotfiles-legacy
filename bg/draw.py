from array import Array
def initpts(maze, rand, n):
	return [rand.randrange(maze.w) + rand.randrange(maze.h)*1j for _ in range(n)]

def calc_distance(maze, queue):
	dist = Array(maze.w, maze.h, lambda: None)
	def proc(pos):
		for d in [1, -1, 1j, -1j]:
			if not maze.is_open(pos, d): continue
			p, ds = dist[pos]
			if not dist[pos+d]:
				dist[pos+d] = (p, ds+1)
				queue.append(pos+d)
	for k, pos in enumerate(queue):
		dist[pos] = (k, 0)
	for pos in queue:
		proc(pos)
	return dist


def draw_maze(maze, dist):
	img = Array(maze.w*2+1, maze.h*2+1, lambda: (-1, -1))
	for x in range(maze.w):
		for y in range(maze.h):
			pos = x+y*1j
			ipos = x*2+y*2j+1+1j
			img[ipos] = dist[pos]
			if maze.is_open(pos, 1):
				img[ipos+1] = dist[pos]
			if maze.is_open(pos, 1j):
				img[ipos+1j] = dist[pos]
	return img

def draw_image(maze, dist):
	return dist

def hsv2rgb(h, s, v):
	from math import cos, pi as π
	V = v**1.5
	S = s**0.5
	cos1 = lambda t: cos(2*π*t)
	calc = lambda c: round((V + V*S/2*(cos1(h-c/3)-1)) * 255)
	return calc(0) << 16 | calc(1) << 8 | calc(2) << 0
