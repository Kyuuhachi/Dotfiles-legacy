from . import reprise, reprise_split

if __name__ == "__main__":
	class Newtype:
		def __repr__(self) -> str:
			mro = type(self).__mro__
			cls = mro[mro.index(Newtype)+1]
			return f"{type(self).__name__}({cls(self)!r})"

	class Translate(Newtype, str): pass

	class A:
		def __repr__(self) -> str:
			if () == ():
				return f"{'aaa'}({4!r})" \
					+ "{%s!}" \
					+ repr(4) \
					+ ("%s%r" % ("a","b")) \
					+ str.format("[{!r}]", "asdf") \
					+ "[{[a]!r}]".format({"a":"b"}) \
					+ "[{bees[bzz]!r}]".format_map({"bees":{"bzz": {"b", "z", "z"}}})

	# print(repr(repr(A())))
	# print(reprise(A()))
	# print(reprise(A(), style="%"))
	# print(reprise_split(A()))

	x = Translate("foobar")
	print(repr(repr(x)))
	print(reprise(x))
	print(reprise(x, style="%"))
	print(reprise_split(x))
