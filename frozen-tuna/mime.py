from collections import defaultdict
from fnmatch import fnmatch
import os
import os.path
from util import isBinaryString, getFiles

__all__ = [
	"ALIASES",
	"ICONS",
	"SUBCLASSES",
	"match",
	"match_globs",
	"match_magic",
	"match_basic",
	"MAGIC_MAXLEN",
]

ALIASES = defaultdict(lambda: None)
for path in getFiles("mime/aliases"):
	with open(path, "r") as file:
		for line in file.read().splitlines():
			mime, alias = line.split(" ")
			ALIASES[mime] = alias
ALIASES = dict(ALIASES)

ICONS = defaultdict(lambda: None)
for path in getFiles("mime/generic-icons"):
	with open(path, "r") as file:
		for line in file.read().splitlines():
			mime, icon = line.split(":")
			ICONS[mime] = icon
ICONS = dict(ICONS)

SUBCLASSES = defaultdict(list)
for path in getFiles("mime/subclasses"):
	with open(path, "r") as file:
		for line in file.read().splitlines():
			mime, subclass = line.split(" ")
			if subclass not in SUBCLASSES[mime]:
				SUBCLASSES[mime].append(subclass)
SUBCLASSES = dict(SUBCLASSES)

GLOB_EXTENSIONS = defaultdict(list)
GLOB_LITERALS = {}
GLOB_MATCHES = [] # (Weight, mime, glob, flags)
for path in getFiles("mime/globs2"):
	with open(path, "r") as file:
		for line in file.read().splitlines():
			if line.startswith("#"): continue

			[weight, mime, glob, flags, *_] = line.split(":") + [""]
			flags = flags.split(",")

			if "*" not in glob and "?" not in glob and "[" not in glob:
				GLOB_LITERALS[glob] = mime
			elif glob.startswith("*.") and "cs" not in flags:
				extension = glob[1:]
				if "*" not in extension and "?" not in extension and "[" not in extension:
					GLOB_EXTENSIONS[extension].append((int(weight), mime))
			else:
				GLOB_MATCHES.append((int(weight), mime, glob, flags))
GLOB_EXTENSIONS = dict(GLOB_EXTENSIONS)

class P: # Very simple binary parser/reader with one byte readahead
	def __init__(self, file):
		self._file = file
		self._peek = None
		self._i = 0

	def peek(self):
		if self._peek is None:
			self._peek = self._file.read(1)
		return self._peek

	def get(self):
		self._i += 1
		if self._peek is not None:
			a = self._peek
			self._peek = None
			return a
		return self._file.read(1)[0]

	def gets(self, len):
		return bytes(self.get() for _ in range(len))

	def test(self, c):
		if self.peek() == c:
			self.get()
			return True
		return False

	def num(self):
		ret = bytearray()
		while self.peek().isdigit():
			ret.append(self.get()[0])
		return int(ret)

class MagicRule(object):
	def __init__(self, p):
		self.next = None

		self.nest = 0
		self.startOffset = None
		self.value = None
		self.mask = None
		self.wordSize = 1
		self.rangeLength = 1

		if p.peek() != b">": self.nest = p.num()
		if p.test(b">"): self.startOffset = p.num()
		if p.test(b"="): self.value = p.gets(p.get() << 8 | p.get())
		if p.test(b"&"): self.mask = p.gets(len(self.value))
		if p.test(b"~"): self.wordSize = p.num()
		if p.test(b"+"): self.rangeLength = p.num()

		if self.startOffset is None: raise ValueError("No offset for magic line")
		if self.value is None: raise ValueError("No value for magic line")
		if not p.test(b"\n"): raise ValueError("Malformed MIME magic line: %r" % p.peek())

	def match(self, buffer):
		for o in range(self.rangeLength):
			s = self.startOffset + o
			if self.mask: test = bytes([a & b for (a, b) in zip(buffer[s:], self.mask)])
			else: test = buffer[s:s+len(self.value)]
			if test == self.value:
				if self.next:
					return self.next.match(buffer)
				return True

MAGIC_TYPES = {}
MAGIC_MAXLEN = 0
for path in getFiles("mime/magic"):
	with open(path, "rb") as file:
		if file.read(12) != b"MIME-Magic\0\n":
			raise ValueError("Bad header for file %r" % path)
		p = P(file)

		while p.peek():
			if not p.test(b"["): raise ValueError("Expected heading opening, found %r" % p.peek())
			pri = p.num()
			if not p.test(b":"): raise ValueError("Expected heading colon, found %r" % p.peek())
			mimeB = bytearray()
			while not p.test(b"]"):
				mimeB.append(p.get()[0])
			mime = bytes(mimeB).decode()
			if not p.test(b"\n"): raise ValueError("Expected heading newline, found %r" % p.peek())

			topRules = []
			lastRule = None
			while p.peek() and p.peek() != b"[]"[:1]: # Vim's formatting breaks if I just say b"["
				rule = MagicRule(p)

				if rule.nest != 0 and lastRule:
					if rule.nest < lastRule.nest:
						lastRule.next = rule
				else:
					topRules.append(rule)
					lastRule = rule # Should this be unindented?

				length = rule.startOffset + len(rule.value) + rule.rangeLength
				if length > MAGIC_MAXLEN:
					MAGIC_MAXLEN = length

			if pri not in MAGIC_TYPES:
				MAGIC_TYPES[pri] = []
			MAGIC_TYPES[pri].append((mime, topRules))

def match_globs(path):
	name = os.path.basename(path)
	if name in GLOB_LITERALS:
		return [GLOB_LITERALS[name]]
	if name.lower() in GLOB_LITERALS:
		return [GLOB_LITERALS[name.lower()]]

	ext = os.path.splitext(name)[1]
	matches = None
	if ext in GLOB_EXTENSIONS:
		matches = GLOB_EXTENSIONS[ext]
	elif ext.lower() in GLOB_EXTENSIONS:
		matches = GLOB_EXTENSIONS[ext.lower()]
	else:
		matches = []
		for w, m, g, f in GLOB_MATCHES:
			if fnmatch(name, g) or ("cs" not in f and fnmatch(name.lower(), g)):
				matches.append((w + len(g) / 128, m))
	return sorted(matches, reverse=True)

def match_magic(data):
	matches = []
	for priority in MAGIC_TYPES.keys():
		for (mime, rules) in MAGIC_TYPES[priority]:
			for rule in rules:
				if rule.match(data):
					matches.append((priority, mime))
	return sorted(matches, reverse=True)

def match_basic(data):
	if not data:
		return "inode/x-empty"
	elif not isBinaryString(data):
		return "text/plain"
	else:
		return "application/octet-stream"

def match(path, data):
	glob = match_globs(path) if path else []
	magic = match_magic(data) if data else []
	basic = [match_basic(data)] if data else []

	magic_hi = [m[1] for m in magic if m[0] >= 80]
	glob_    = [m[1] for m in glob]
	magic_lo = [m[1] for m in magic if m[0] < 80]
	return magic_hi + glob_ + magic_lo + basic

def get_all_mimes(mimes):
	allMimes = set()
	allIcons = set()
	def fill_mimes(m):
		while m in ALIASES:
			m = ALIASES[m]
		if m not in allMimes:
			allMimes.add(m)
			for m2 in SUBCLASSES.get(m, []):
				fill_mimes(m2)
	for m in mimes:
		fill_mimes(m)
	return allMimes, allIcons
