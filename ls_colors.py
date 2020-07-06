from pathlib import Path

p = Path(__file__).parent / "ls_colors"
for line in p.read_text().splitlines():
	words = line.split("#")[0].split()
	if words and words[0] == "def":
		for w in words[2:]:
			if not w.startswith(".") and not w.startswith("*") and w != w.upper():
				w = "*" + w
			print(w, words[1])
	else:
		print(line)
