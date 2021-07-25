import sys

for line in sys.stdin:
	words = line.split("#")[0].split()
	if words[:1] == ["def"]:
		for w in words[2:]:
			if not w.startswith(".") and not w.startswith("*") and w != w.upper():
				w = "*" + w
			print(w, words[1])
	else:
		print(line)
