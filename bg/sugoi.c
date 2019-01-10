#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define PI 3.14159265

#define NUM_CELLS 64
#define PALETTE_LENGTH 2

#define DOWN 0
#define RIGHT 1
#define UP 2
#define LEFT 3

#define R() ((double)rand() / RAND_MAX)
#define r(x) (rand() % (x))
#define log(fmt, ...) fprintf(stderr, "%1.4f " fmt "\n", (double)clock() / CLOCKS_PER_SEC, ##__VA_ARGS__)
typedef unsigned int uint;

typedef struct {
	bool down;
	bool right;
} cell;

typedef struct {
	int x;
	int y;
	uint dir;
} pos;

int off_y(uint dir) {
	if(dir == DOWN) return 1;
	if(dir == UP) return -1;
	return 0;
}

int off_x(uint dir) {
	if(dir == RIGHT) return 1;
	if(dir == LEFT) return -1;
	return 0;
}

pos offset(pos p) {
	p.x += off_x(p.dir);
	p.y += off_y(p.dir);
	return p;
}

bool is_open(cell maze[], uint w, uint h, pos p) {
	if(p.dir == DOWN)  return p.y < h-1 && maze[(p.x)   + w*(p.y)].down;
	if(p.dir == RIGHT) return p.x < w-1 && maze[(p.x)   + w*(p.y)].right;
	if(p.dir == UP)    return p.y > 0   && maze[(p.x)   + w*(p.y-1)].down;
	if(p.dir == LEFT)  return p.x > 0   && maze[(p.x-1) + w*(p.y)].right;
}

void open(cell maze[], uint w, uint h, pos *p) {
	if(p->dir == DOWN)  { maze[(p->x)   + w*(p->y)].down   = true; p->y++; }
	if(p->dir == RIGHT) { maze[(p->x)   + w*(p->y)].right  = true; p->x++; }
	if(p->dir == UP)    { maze[(p->x)   + w*(p->y-1)].down = true; p->y--; }
	if(p->dir == LEFT)  { maze[(p->x-1) + w*(p->y)].right  = true; p->x--; }
}

void shuffle(void* array, size_t n, size_t size) {
	char tmp[size];
	char* arr = array;
	size_t stride = size * sizeof(char);

	for(size_t i = 0; i < n - 1; i++) {
		size_t j = i + (size_t)(rand()) / (RAND_MAX / (n - i) + 1);

		memcpy(tmp, arr + j * stride, size);
		memcpy(arr + j * stride, arr + i * stride, size);
		memcpy(arr + i * stride, tmp, size);
	}
}

// {{{ randwall
bool randwall_can_open(bool used[], uint w, uint h, pos p) {
	if(p.dir == DOWN)  return p.y < h-1 && !used[(p.x)   + w*(p.y+1)];
	if(p.dir == RIGHT) return p.x < w-1 && !used[(p.x+1) + w*(p.y)];
	if(p.dir == UP)    return p.y > 0   && !used[(p.x)   + w*(p.y-1)];
	if(p.dir == LEFT)  return p.x > 0   && !used[(p.x-1) + w*(p.y)];
}

void randwall_generate(cell cells[], uint w, uint h) {
	bool* used = calloc(w*h, sizeof(bool));
	pos* walls = calloc(w*h*4, sizeof(pos));
	uint nwalls = 0;

	uint x = r(w);
	uint y = r(h);
	used[x + w*y] = true;
	walls[nwalls++] = (pos) {x, y, 0};
	walls[nwalls++] = (pos) {x, y, 1};
	walls[nwalls++] = (pos) {x, y, 2};
	walls[nwalls++] = (pos) {x, y, 3};

	while(nwalls) {
		uint idx = r(nwalls);
		pos p = walls[idx];
		walls[idx] = walls[--nwalls];
		if(randwall_can_open(used, w, h, p)) {
			open(cells, w, h, &p);
			used[p.x + w*p.y] = true;
			for(uint i = 0; i < 4; i++) {
				p.dir = i;
				if(randwall_can_open(used, w, h, p))
					walls[nwalls++] = p;
			}
		}
	}
	free(walls);
	free(used);
}
// }}}

// {{{ Union-Find
// {{{ Data structure
typedef struct {
	uint* id;
	uint* sz;
} uf;

uf uf_create(uint length) {
	uf uf;
	uf.id = calloc(length, sizeof(uint));
	uf.sz = calloc(length, sizeof(uint));
	for(int i = 0; i < length; i++) {
		uf.id[i] = i;
		uf.sz[i] = 1;
	}
	return uf;
}

void uf_destroy(uf* uf) {
	free(uf->id);
	free(uf->sz);
	uf->id = 0;
	uf->sz = 0;
}

uint uf_root(uf* uf, uint a) {
	while(a != uf->id[a])
		a = uf->id[a] = uf->id[uf->id[a]];
	return a;
}

bool uf_find(uf* uf, uint a, uint b) {
	return uf_root(uf, a) == uf_root(uf, b);
}

void uf_unite(uf* uf, uint a, uint b) {
	a = uf_root(uf, a);
	b = uf_root(uf, b);
	if(uf->sz[a] < uf->sz[b]) {
		uf->id[a] = b;
		uf->sz[b] += uf->sz[a];
	} else {
		uf->id[b] = a;
		uf->sz[a] += uf->sz[b];
	}
}
// }}}

void unionfind_generate(cell cells[], uint w, uint h) {
	uf uf = uf_create(w*h);
	pos* walls = calloc(w*h*2, sizeof(pos));
	uint nwalls = 0;
	for(uint x = 0; x < w; x++)
		for(uint y = 0; y < h; y++) {
			if(x != w-1) walls[nwalls++] = (pos) {x, y, RIGHT};
			if(y != h-1) walls[nwalls++] = (pos) {x, y, DOWN};
		}
	while(nwalls) {
		uint idx = r(nwalls);
		pos p = walls[idx];
		walls[idx] = walls[--nwalls];
		uint a = p.x + w*p.y;
		uint b = (p.x+off_x(p.dir)) + w*(p.y+off_y(p.dir));
		if(!uf_find(&uf, a, b)) {
			open(cells, w, h, &p);
			uf_unite(&uf, a, b);
		}
	}
	uf_destroy(&uf);
	free(walls);
}
// }}}

// {{{ corridors
void corridors_generate(cell cells[], uint w, uint h) {
	bool* used = calloc(w*h, sizeof(bool));
	pos* walls = calloc(w*h*4, sizeof(pos));
	uint nwalls = 0;

	uint x = r(w);
	uint y = r(h);
	used[x + w*y] = true;
	walls[nwalls++] = (pos) {x, y, 0};
	walls[nwalls++] = (pos) {x, y, 1};
	walls[nwalls++] = (pos) {x, y, 2};
	walls[nwalls++] = (pos) {x, y, 3};

	while(nwalls) {
		uint idx = r(nwalls);
		pos p = walls[idx];
		walls[idx] = walls[--nwalls];
		while(randwall_can_open(used, w, h, p)) {
			open(cells, w, h, &p);
			used[p.x + w*p.y] = true;
			for(uint i = 0; i < 4; i++) {
				pos p2 = p;
				p2.dir = i;
				if(randwall_can_open(used, w, h, p2))
					walls[nwalls++] = p2;
			}
		}
	}
	free(walls);
	free(used);
}
// }}}

// {{{ Calculate distance
typedef struct {
	uint x;
	uint y;
	uint val;
	uint which;
} dist_cell;

typedef struct {
	uint distance;
	double dist_d;
	uint which;
} distance;

void calc_distance(distance dists[], cell maze[], uint w, uint h, uint n) {
	dist_cell* queue = calloc(w*h+n, sizeof(dist_cell));
	uint nqueue = 0;
	uint queue_pos = 0;
	for(uint i = 0; i < n; i++)
		queue[nqueue++] = (dist_cell) {r(w), r(h), 0, i};
	while(queue_pos != nqueue) {
		dist_cell cell = queue[queue_pos++];
		if(dists[cell.x + w*cell.y].distance > cell.val) {
			dists[cell.x + w*cell.y] = (distance) {cell.val, -1, cell.which};
			for(int i = 0; i < 4; i++)
				if(is_open(maze, w, h, (pos) {cell.x, cell.y, i})
						&& dists[(cell.x+off_x(i)) + w*(cell.y+off_y(i))].distance > cell.val)
					queue[nqueue++] = (dist_cell) {cell.x + off_x(i), cell.y + off_y(i), cell.val+1, cell.which};
		}
	}
	free(queue);
}
// }}}

// {{{ Drawing the image
typedef struct { double r, g, b; } rgb;
typedef struct { double h, s, v; } hsv;
typedef struct { hsv* pixels; uint w, h; } image;

uint rgb2i(rgb rgb) {
	if(rgb.r < 0) rgb.r = 0;
	if(rgb.r > 1) rgb.r = 1;
	if(rgb.g < 0) rgb.g = 0;
	if(rgb.g > 1) rgb.g = 1;
	if(rgb.b < 0) rgb.b = 0;
	if(rgb.b > 1) rgb.b = 1;
	return ((uint)(rgb.r*255) << 16) | ((uint)(rgb.g*255) << 8) | ((uint)(rgb.b*255) << 0);
}

rgb hsv2rgb(hsv hsv) {
	double h = hsv.h, s = hsv.s, v = hsv.v;

	double V = v*sqrt(v);
	double S = sqrt(s);
#define cos1(t) cos(2*PI*(t))
#define calc(c) (V - V*S/2 + V*S/2*cos1(h - (double)c/3))

	double r = calc(0);
	double g = calc(1);
	double b = calc(2);

	return (rgb) {r, g, b};
}

void gen_palette(hsv palette[]) {
	if(PALETTE_LENGTH == 2) {
		palette[0] = (hsv) {0, 0.2, 1};
		palette[1] = (hsv) {0, 1, 0.4};
		palette[2] = (hsv) {0, 0.5, 0.5};
	} else {
		for(int i = 0; i <= PALETTE_LENGTH; i++) {
			bool isfg = i < PALETTE_LENGTH;
			double _h = (R()*2-1)/360*12*isfg;
			double _s = R()*0.3+0.3*isfg;
			double _v = R()*0.5+0.3*isfg;
			palette[i] = (hsv) {_h, _s, _v};
		}
	}
}

hsv get_gradient(double ang, uint which, hsv palette[]) {
	if(isnan(ang))
		return (hsv) {NAN};
	double state = ang * (PALETTE_LENGTH-1);
	uint idx = (int)state;
	hsv a = palette[0+idx];
	hsv b = palette[1+idx];
	double tween = state - (int)state;
	hsv out = {a.h+(b.h-a.h)*tween, a.s+(b.s-a.s)*tween, a.v+(b.v-a.v)*tween};
	out.h += ((double)which / NUM_CELLS-0.5)/3;
	return out;
}

void draw_maze(image* img, cell maze[], distance dists[], uint w, uint h, hsv palette[]) {
	img->w = 2*w;
	img->h = 2*h;
	img->pixels = calloc(img->w*img->h, sizeof(hsv));

	for(int i = 0; i < img->w*img->h; i++)
		img->pixels[i] = palette[0];

	for(int x = 0; x < w; x++)
		for(int y = 0; y < h; y++) {
			uint midx = x+w*y;
			uint iidx = (2*x+1)+img->w*(2*y+1);
			hsv pixel = get_gradient(dists[midx].dist_d, dists[midx].which, palette);
			img->pixels[iidx] = pixel;
			if(maze[midx].down)
				img->pixels[iidx+img->w] = pixel;
			if(maze[midx].right)
				img->pixels[iidx+1] = pixel;
		}
}

void draw_image(image* img, cell maze[], distance dists[], uint w, uint h, hsv palette[]) {
	img->w = w;
	img->h = h;
	img->pixels = calloc(img->w*img->h, sizeof(hsv));

	for(int x = 0; x < w; x++)
		for(int y = 0; y < h; y++) {
			uint idx = x+w*y;
			img->pixels[idx] = get_gradient(dists[idx].dist_d, dists[idx].which, palette);
		}
}

void dump(cell maze[], uint w, uint h) {
	for(int x = 0; x <= w*2; x++)
		printf("#");
	printf("\n");
	for(int y = 0; y < h; y++) {
		printf("#");
		for(int x = 0; x < w; x++) {
			printf(" ");
			printf(maze[x+y*w].right ? " " : "#");
		}
		printf("\n");
		printf("#");
		for(int x = 0; x < w; x++) {
			printf(maze[x+y*w].down ? " " : "#");
			printf("#");
		}
		printf("\n");
	}
}
// }}}

int main(int argc, char** argv) {
	uint w = atoi(argv[1]);
	uint h = atoi(argv[2]);
	srand(atoi(argv[3]));
	double hue = atof(argv[4]);

	uint type = r(3);
	log("Generating maze of type %d", type);
	cell* maze = calloc(w*h, sizeof(cell));
	switch(type) {
		case 0: randwall_generate(maze, w, h); break;
		case 1: unionfind_generate(maze, w, h); break;
		case 2: corridors_generate(maze, w, h); break;
	}

	if(false) {
		log("Calculating distances");
		distance* dists = calloc(w*h, sizeof(distance));
		for(uint i = 0; i < w*h; i++)
			dists[i].distance--;
		calc_distance(dists, maze, w, h, NUM_CELLS);
		uint maxdist = 0;
		for(int i = 0; i < w*h; i++)
			if(dists[i].distance > maxdist && dists[i].distance != -1)
				maxdist = dists[i].distance;
		for(int i = 0; i < w*h; i++) {
			dists[i].dist_d = (double)dists[i].distance / (maxdist+1);
			if(dists[i].distance == -1)
				dists[i].dist_d = NAN;
		}

		log("Drawing image");
		hsv palette [PALETTE_LENGTH+1];
		gen_palette(palette);
		image img; // The pixels are allocated inside the function
		draw_image(&img, maze, dists, w, h, palette);

		log("Converting to RGB");
		uint* pixels =  calloc(img.w*img.h, sizeof(uint));
		for(int i = 0; i < img.w*img.h; i++) {
			if(isnan(img.pixels[i].h))
				pixels[i] = 0xFF0000;
			else {
				img.pixels[i].h += hue;
				pixels[i] = rgb2i(hsv2rgb(img.pixels[i]));
			}
		}

		log("Writing output");
		fwrite(&img.w, sizeof(uint), 1, stdout);
		fwrite(&img.h, sizeof(uint), 1, stdout);
		fwrite(pixels, sizeof(uint), img.w*img.h, stdout);

		log("Done!");
		free(img.pixels);
		free(pixels);
		free(dists);
	} else dump(maze, w, h);

	free(maze);
}
