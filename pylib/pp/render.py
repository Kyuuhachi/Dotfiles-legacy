from . import sdoctypes as sd
from . import color as c
def render(tokens, color=True):
	s = []
	color = [c.RESET]
	for t in tokens:
		if isinstance(t, sd.SLine):
			s.append("\n"+" "*t.indent)

		elif isinstance(t, sd.SAnnotationPush):
			if isinstance(t.value, c.Color) and color:
				color.append(color[-1] + t.value)
				s.append(f"\x1B[{color[-1]}m")

		elif isinstance(t, sd.SAnnotationPop):
			if isinstance(t.value, c.Color) and color:
				color.pop()
				s.append(f"\x1B[{color[-1]}m")
		else:
			s.append(t)
	return "".join(s)
