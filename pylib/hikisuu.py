from dataclasses import dataclass, field
import sys

class Sentinel:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return self.name

OMIT = Sentinel("OMIT")

class Group(dict):
	def arg(self, *names, **kwargs):
		assert names
		val = Argument(**kwargs)
		for name in names:
			self[name] = val
		return val

	def pos(self, name, **kwargs):
		val = Positional(**kwargs)
		self[name] = val
		return val

	def group(self, name, **kwargs):
		val = Group(**kwargs)
		self[name] = val
		return val

	def _init_parser(self, impl, _):
		for k, item in self.items():
			item._init_parser(impl, k)

@dataclass
class Parser(Group):
	def parse_args(self, argv=None):
		if argv is None: argv = sys.argv
		impl = ParserImpl()
		self._init_parser(impl, None)
		return impl.parse(argv)

