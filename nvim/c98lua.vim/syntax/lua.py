for line in open("lua0.vim").read().splitlines():
	line = line.replace("nextgroup", "skipwhite skipempty nextgroup")
	if "←" in line or "→" in line or "↑" in line:
		for a in range(6):
			n = (a+1)%6
			print(line.replace("←", str(a)).replace("→", str(n)).replace(" ↑", " contained" if a else ""))
	else:
		print(line)
