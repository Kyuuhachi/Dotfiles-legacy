import os.path
import io
import mime
import tempfile
peek_len = max(1024, mime.MAGIC_MAXLEN)

from functools import wraps
from collections import defaultdict

def once(f):
	key = f"_once_{f.__name__}"
	@wraps(f)
	def wrapper(self):
		if hasattr(self, key):
			return getattr(self, key)
		else:
			result = f(self)
			setattr(self, key, result)
			return result
	return wrapper

class Handler:
	def __init__(self, url):
		self.url = url

	@property
	def mime(self): raise NotImplementedError()

	@property
	def filename(self): raise NotImplementedError()

	@property
	def hosts(self): return []

	def _open(self): raise NotImplementedError()

	@once
	def open(self):
		f = self._open()
		self._peek = b""
		return f
		if f is None:
			self._peek = None
			return None
		else:
			br = io.BufferedReader(self._open(), peek_len)
			self._peek = br.peek(peek_len)
		return br

	@property
	@once
	def mimes(self):
		print(id(self.open()))
		m = mime.match(self.filename, self._peek)
		m2 = self.mime
		if m2 is not None:
			m = [*m2, *m]
		return m

	@once
	def read(self):
		f = self.open()
		if f is None:
			return None
		return f.read()

	@property
	@once
	def path(self):
		data = self.read()
		if data is None:
			return None
		dir = tempfile.mkdtemp(prefix="frozentuna-")
		fname = self.filename
		if fname:
			fname = fname.replace("/", "-")
			if fname[0] in ".-": fname = "_" + fname[1:]
		fname = f"{dir}/{fname}"
		open(fname, "wb").write(data)
		return fname

class UnknownHandler(Handler):
	@property
	def mime(self): return []

	@property
	def filename(self): return None

	def open(self): return None

	@property
	def mimes(self): return []

	def read(self): return []

	@property
	def path(self): return None

registry = defaultdict(lambda: UnknownHandler)
def register(scheme):
	def registrar(f):
		registry[scheme] = f
		return f
	return registrar

@register("")
class FileHandler(Handler):
	path = None
	def __init__(self, path):
		import pathlib
		super().__init__(pathlib.Path(path).absolute().as_uri())
		self.path = path

	@property
	@once
	def mime(self):
		import os
		import stat
		try:
			mode = os.stat(self.path).st_mode
			if os.path.ismount(self.path): yield "inode/mount-point"
			if stat.S_ISBLK(mode):         yield "inode/blockdevice"
			if stat.S_ISCHR(mode):         yield "inode/chardevice"
			if stat.S_ISDIR(mode):         yield "inode/directory"
			if stat.S_ISFIFO(mode):        yield "inode/fifo"
			if stat.S_ISLNK(mode):         yield "inode/symlink"
			if stat.S_ISSOCK(mode):        yield "inode/socket"
		except IOError:
			return

	@property
	def filename(self):
		return os.path.basename(self.path.rstrip("/"))

	def _open(self):
		try:
			return open(self.path, "rb")
		except OSError:
			return None

@register("file")
class FileUrlHandler(FileHandler):
	def __init__(self, url):
		import urllib.parse
		super().__init__(urllib.parse.unquote(url[7:]))

@register("http")
@register("https")
class HttpHandler(Handler):
	def __init__(self, url):
		super().__init__(url)
		import requests
		import util
		util.notify(f"Getting HTTP...", url)
		self.response = requests.get(url, stream=True)
		self.response.raw.decode_content = True

	@property
	@once
	def mime(self):
		yield self.response.headers["content-type"].split(";")[0]

	@property
	@once
	def filename(self):
		import urllib.parse
		if "content-disposition" in self.response.headers:
			try:
				import rfc6266
			except ImportError as e:
				print(e)
				print("Couldn't import rfc6266; not using content-disposition header")
			else:
				return rfc6266.parse_headers(self.response.headers["content-disposition"]).filename_unsafe
		return os.path.basename(urllib.parse.urlparse(self.url).path) or "index.html"

	def _open(self):
		return self.response.raw

	@property
	@once
	def hosts(self):
		import urllib.parse
		domain = urllib.parse.urlparse(self.url).hostname
		def tails(s):
			if "." in s:
				return [s] + tails(s[s.find(".")+1:])
			else:
				return [s]
		return tails(domain)
