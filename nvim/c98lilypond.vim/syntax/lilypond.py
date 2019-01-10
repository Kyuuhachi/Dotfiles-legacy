import lilywords

trie = {}
for k, v in vars(lilywords).items():
	if k.startswith("_"): continue
	trie[k] = {}
	for w in v:
		t = trie[k]
		for ch in w:
			t.setdefault(ch, {})
			t = t[ch]
		t[""] = {}

cache = {}
def trieregex(trie, prefix=""):
	if not trie:
		return prefix
	if (id(trie),prefix) in cache:
		return cache[(id(trie),prefix)]

	out = "\\|".join(trieregex(v, prefix=prefix+k) for k, v in trie.items())
	if len(trie) > 1:
		out = min(out, prefix + "\\%(" + "\\|".join(trieregex(v,prefix=k) for k, v in trie.items()) + "\\)", key=len)
	cache[(id(trie),prefix)] = out
	return out

def highlight():
	def commands(name, words, **kwargs):
		syn_match(name, r"\V\\\\\%({}\)\a\@!".format(trieregex(trie[words])), **kwargs)

	def mode(name, start, contains, mode_top=False, **kwargs):
		syn_match(name, r"\v\\{}\s*".format(start), nextgroup=name+"Body", **kwargs)
		syn_cluster(name, contains + [name+"Body"])
		syn_region(name+"Body", "{", "}", contains="@"+name, contained=not mode_top)
		syn_region(name+"Body", "<<", ">>", contains="@"+name, contained=not mode_top)

	def kw(kwargs):
		for k, v in kwargs.items():
			if v is True: yield k
			elif v is False: pass
			else: yield f"{k}={v}"

	def rx(s):
		if isinstance(s, bytes):
			return s.decode()
		for ch in "/&|!~":
			if ch not in s:
				return ch+s+ch
		raise ValueError(s)

	def syn_cluster(name, vals, **kwargs):
		print("syn", "cluster", name, f"contains={','.join(vals)}", *kw(kwargs))

	def syn_match(name, regex, **kwargs):
		print("syn", "match", name, f"{rx(regex)}", *kw(kwargs))

	def syn_region(name, start, end, *, matchgroup=None, matchgroup2=None, **kwargs):
		def mg(b):
			return [f"matchgroup={b}"] if b else []
		mg1 = matchgroup or matchgroup2
		mg2 = matchgroup2 or matchgroup
		print("syn", "region", name, *mg(mg1), f"start={rx(start)}", *mg(mg2), f"end={rx(end)}", *kw(kwargs))

	syn_match("lilyCustomFunction", r"\\\w\+")
	commands("lilyBuiltin", "builtins")
	commands("lilyMusicCommand", "functions")
	commands("lilyDeclaration", "declarations")
	commands("lilyGrace", "graces")
	commands("lilyArticulation", "articulations")
	syn_match("lilyArticulation", r'\v[\-\^_]([\^+\-!>._]|"@=)')
	commands("lilyScript", "scripts")
	commands("lilyDynamic", "dynamics")
	commands("lilySpanner", "spanners")
	commands("lilyProperty", "properties")
	commands("lilyDeclaration", "declarations")
	commands("lilyScale", "scales")
	syn_match("lilySymbol", r"[|[\]~()]")
	syn_match("lilySymbol", r"\\[!()><[\]!\\]")

	syn_match("lilyNumber", r"\v-?\d+([./]\d+)?")
	noteLength = r"\v\d@<!\s*\zs(128|64|32|16|8|4|2|1|\\breve|\\longa|\\maxima)\.*\d@!"
	syn_match("lilyDuration", noteLength, nextgroup="lilyDurationMul")
	syn_match("lilyRDuration", noteLength, nextgroup="lilyDurationMul", contained=True)
	syn_match("lilyDurationMul", r"\v\s*\*\s*\d+(/\d+)?", nextgroup="lilyDurationMul", contained=True)
	syn_match("lilyNumber", r"\v\d+/\d+")
	syn_region("lilyString", '"', '"', contains="@Spell")
	syn_region("lilyComment", "%{", "%}")
	syn_region("lilyComment", r"%{\@!", "$")

	syn_cluster("lilyFunction", [
		"lilyCustomFunction",
		"lilyBuiltin", "lilyMusicCommand", "lilyArticulation",
		"lilyOrnament", "lilyFermata", "lilyInstrumentScript",
		"lilyRepeat", "lilyAncient", "lilyScales", "lilyMidiInstrument",
		"lilyRepeatType", "lilyAccidentalStyle", "lilyClef",
	])
	syn_cluster("lilyMode", [
		"lilyNotemode", "lilyLyricmode", "lilyChordmode",
		"lilyDrummode", "lilyFiguremode",
	])
	syn_cluster("lilyGlobal", [
		"lilyDuration", "lilyNumber", "lilyString",
		"lilyComment", "lilyScheme", "@lilyFunction",
		"lilyMarkup", "lilySymbol",
	])

	commands("lilyMarkupFunction", "markups", contained=True)
	mode("lilyMarkup", r"markup", [
		"@lilyGlobal", "lilyMarkupFunction"
	])

	syn_match("lilyPitch", r"\v"
		r"\a@<!%([a-g]%(%(es)?%(e[hs])?|%(is)?%(i[hs])?)|[ae]s%(es)?)\a@!" # Pitch
		r"%(%(\s*')+|%(\s*,)+|)" # Octave
		r"%(\s*!)*%(\s*\?)*") # Modifiers
	syn_match("lilyError", r"[!?,']")
	syn_match("lilyRest", r"\v\a@<![rRs]\a@!", nextgroup="lilyRDuration")
	syn_region("lilyChord", r"<\@<!<<\@!", ">", contains="lilyPitch,@lilyFunction,lilyScheme,lilyError")
	syn_match("lilyChordRepeat", r"\v\a@<!q\a@!")
	mode("lilyNotemode", r"notemode", ["TOP"], mode_top=True)

	syn_match("lilyLyric", r"\w\+", contained=True)
	syn_match("lilyLyricHyphen", r"\a\@<!--\w\@!", contained=True)
	syn_match("lilyLyricExtender", r"\a\@<!__\w\@!", contained=True)
	mode("lilyLyricmode", "lyric(mode|s)", [ "@lilyGlobal", "@lilyMode", "lilyLyric", "lilyLyricHyphen", "lilyLyricExtender" ])

	syn_match("lilyChordname", r"", contained=True)
	mode("lilyChordmode", "chord(mode|s)", [ "@lilyGlobal", "@lilyMode", "lilyChordname", "lilyRest" ])

	syn_match("lilyDrum", r"\V\a\@<!\%({}\)\a\@!".format(trieregex(trie["drums"])), contained=True)
	mode("lilyDrummode", r"drum(mode|s)", [ "@lilyGlobal", "@lilyMode", "lilyDrum", "lilyRest" ])

	syn_match("lilyFigure", r"", contained=True)
	mode("lilyFiguremode", r"figure(mode|s)", [ "@lilyGlobal", "@lilyMode", "lilyFigure", "lilyRest" ])

	syn_match("lilyVar", r"\v[a-zA-Z-]+\ze\s*\=", contained=True)
	mode("lilyHeader", r"header", [ "@lilyGlobal", "lilyVar" ])
	mode("lilyPaper", r"paper", [ "@lilyGlobal", "lilyVar" ])
	mode("lilyLayout", r"layout", [ "@lilyGlobal", "lilyVar", "lilyContextMod" ])
	mode("lilyMidi", r"midi", [ "@lilyGlobal", "lilyVar", "lilyContextMod" ])
	mode("lilyContextMod", r"context", [ "@lilyGlobal" ], contained=True)
	mode("lilyWith", r"with", [ "@lilyGlobal", "lilyVar" ])

	START = r"[^()\"\n\t ]\@1<!"
	END = r"[^()\"\n\t ]\@!"
	syn_match("lilySchemeChar", START + r"#\\." + END, contained=True)
	syn_match("lilySchemeChar", START + r"\v#\i\\%(nul|soh|stx|etx|eot|enq|ack|bel|bs|ht|newline|vt|np|cr|so|si|dle|dc1|dc2|dc3|dc4|nak|syn|etb|can|em|sub|esc|fs|gs|rs|us|space|sp|nl|tab|backspace|return|page|null|del)>" + END, contained=True)
	syn_match("lilySchemeComment", START + r";.*$", contained=True)
	syn_region("lilySchemeComment", START + r"#!", r"#!", contained=True)
	syn_match("lilySchemeBoolean", START + r"#[tTfF]" + END, contained=True)
	syn_region("lilySchemeString", r'"',  r'"', skip=r'/\\"/', contained=True)
	syn_match("lilySchemeKeyword", START + r"#:\s*.\+" + END, contained=True)
	# syn_region("lilySchemeExtSymbol", START + r"#{", r"#}", skip=r"/}}/", contained=True) # Not sure if this works with lily
	syn_match("lilySchemeArray", START + r"#[0-9a-zA-z:@]*(\@<=", contained=True, nextgroup="lilySchemeArrayElt")
	syn_region("lilySchemeArrayElt", br"/(/rs=e", br"/)/re=s", contained=True, contains="lilySchemeArrayElt", transparent=True, extend=True)
	syn_region("lilySchemeLily", START + "#{", "#}", matchgroup="lilySchemeLilyStart", contains="@lilyNotemode", contained=True)

	syn_match("lilySchemeNumber", START + r"[+-]\(inf\|nan\)\.0" + END, contained=True)
	prefix = r"#[ei]#C|#C|#C#[ei]"
	num = r"[+-]?R(\@[+-]?R)?|%([+-]?R)?[+-]R?i"
	real = r"%(D+(\.D*)?|\.D+)|D+/D+"
	syn_match("lilySchemeNumber", (START + r"\v\cPN\m" + END).replace("P", f"%({prefix})").replace("C", "b").replace("N", f"%({num})").replace("R", f"%({real})").replace("D", r"[01]"), contained=True)
	syn_match("lilySchemeNumber", (START + r"\v\cPN\m" + END).replace("P", f"%({prefix})").replace("C", "o").replace("N", f"%({num})").replace("R", f"%({real})").replace("D", r"\o"), contained=True)
	syn_match("lilySchemeNumber", (START + r"\v\cPN\m" + END).replace("P", f"%({prefix})").replace("C", "x").replace("N", f"%({num})").replace("R", f"%({real})").replace("D", r"\x"), contained=True)
	prefix += r"|#[ei]|"
	real = r"%(D+%(\.D*)?|\.D+)%(e[+-]?\D+)?|D+/D+"
	syn_match("lilySchemeNumber", (START + r"\v\cPN\m" + END).replace("P", f"%({prefix})").replace("C", "d").replace("N", f"%({num})").replace("R", f"%({real})").replace("D", r"\d"), contained=True)

	def functions(name, words, **kwargs):
		syn_match(name, (START + r"\V\%({}\)\m" + END).format(trieregex(trie[words])), **kwargs)

	functions("lilySchemeVar", "vars", contained=True)
	functions("lilySchemeFunc", "funcs", contained=True)
	functions("lilySchemeMacro", "macros", contained=True)

	syn_cluster("lilySchemeRoot", [
		"lilySchemeChar", "lilySchemeComment", "lilySchemeBoolean", "lilySchemeString", "lilySchemeKeyword",
		"lilySchemeExtSymbol", "lilySchemeArray", "lilySchemeNumber", "lilySchemeLily"
	])

	for a in range(0, 6):
		n = (a+1) % 6
		syn_match(f"lilySchemeQuote{a}", r"['`]\s*", nextgroup=f"@lilySchemeRoot,lilySchemeQuoted{n},lilySchemeUnquote{n},lilySchemeQuote{n}", contained=True)
		syn_match(f"lilySchemeUnquote{a}", r",@\?\s*", nextgroup=f"@lilySchemeRoot,lilySchemeVar,lilySchemeFunc,lilySchemeMacro,lilySchemeStruc{n},lilySchemeQuote{n}", contained=True)
		syn_region(f"lilySchemeQuoted{a}", "(", ")", contains=f"@lilySchemeRoot,lilySchemeQuoted{n},lilySchemeUnquote{a},lilySchemeQuote{a}", matchgroup=f"lilySchemeDelimiter{a}", contained=True)
		syn_region(f"lilySchemeStruc{a}", "(", ")", contains=f"@lilySchemeRoot,lilySchemeVar,lilySchemeFunc,lilySchemeMacro,lilySchemeStruc{n},lilySchemeQuote{a}", matchgroup=f"lilySchemeDelimiter{a}", contained=True)

	syn_match("lilyScheme", r"[#$]@\?", nextgroup="@lilySchemeRoot,lilySchemeVar,lilySchemeFunc,lilySchemeMacro,lilySchemeStruc4,lilySchemeQuote5")
if __name__ == "__main__":
	highlight()
