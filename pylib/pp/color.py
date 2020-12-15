from dataclasses import dataclass
from . import doc as d

@dataclass(frozen=True)
class Color:
	num: tuple
	def __str__(self):
		return ";".join(map(str, self.num))

	def __add__(self, other):
		if other.num[0] == 0:
			return other
		return Color(self.num + other.num)

	def __call__(self, other):
		return d.Annotate(self, other)

RESET = Color((0,))
BOLD = Color((1,))
FAINT = Color((2,))
ITALIC = Color((3,))

CONSTANT   = Color((38,5,9)) # Red
STRING     = Color((38,5,12)) # Light blue
TAGGED     = Color((38,5,223)) # Tan
IDENTIFIER = Color((38,5,10)) # Light green
ARGUMENT   = Color((38,5,158)) # Pale cyan
