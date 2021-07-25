from . import prepr, pprint

import dataclasses
@dataclasses.dataclass
class Aaa:
	x: ...
	y: ...
	z: ...

def foo(a, /, d=3, *f, **g) -> int:
	...
def bar():
	return lambda x: 4
v = {
	"abdefghijklmnopqrstuvwxyz\nabdefghijklmnopqrstuvwxyz": "A\nA",
	"a\nb": "A\nB",
}
from PIL import Image as I
v = (v, Aaa(1,Aaa("b", (1,2,3), foo),Aaa("b", (1,2,3), {"a": bar(), "c": "d"})), I.Image)
print(prepr(v, width=60))
import re
pprint(re.compile(br"""
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
	'foo?b\(a\)\\ 
""", re.VERBOSE), width=200)

pprint(b"\x01\x02\x03")
