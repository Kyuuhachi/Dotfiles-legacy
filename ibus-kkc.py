#!/usr/bin/env python3
っ = "bcdfghjklmpqrstvwy"
ん = {
	"n":  ["", "ん\u20E6", "ン\u20E6", "ん", "ン"],
	"nn": ["n", "ん"],
	"n'": ["", "ん"],
}
basic = {
	"a":  "あ", "i":   "い", "u":   "う", "e":  "え", "o":  "お",
	"ka": "か", "ki":  "き", "ku":  "く", "ke": "け", "ko": "こ",
	"sa": "さ", "shi": "し", "su":  "す", "se": "せ", "so": "そ",
	"ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
	"na": "な", "ni":  "に", "nu":  "ぬ", "ne": "ね", "no": "の",
	"ha": "は", "hi":  "ひ", "fu":  "ふ", "he": "へ", "ho": "ほ",
	"ma": "ま", "mi":  "み", "mu":  "む", "me": "め", "mo": "も",
	"ya": "や",              "yu":  "ゆ",             "yo": "よ",
	"ra": "ら", "ri":  "り", "ru":  "る", "re": "れ", "ro": "ろ",
	"wa": "わ",                                       "wo": "を",
	"ga": "が", "gi":  "ぎ", "gu":  "ぐ", "ge": "げ", "go": "ご",
	"za": "ざ", "ji":  "じ", "zu":  "ず", "ze": "ぜ", "zo": "ぞ",
	"da": "だ", "dji": "ぢ", "du":  "づ", "de": "で", "do": "ど",
	"ba": "ば", "bi":  "び", "bu":  "ぶ", "be": "べ", "bo": "ぼ",
	"pa": "ぱ", "pi":  "ぴ", "pu":  "ぷ", "pe": "ぺ", "po": "ぽ",

	"kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
	"sha": "しゃ", "shu": "しゅ", "sho": "しょ",
	"sya": "しゃ", "syu": "しゅ", "syo": "しょ",
	"cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
	"tya": "ちゃ", "tyu": "ちゅ", "tyo": "ちょ",
	"nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
	"hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
	"mya": "みゃ", "myu": "みゅ", "myo": "みょ",
	"rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
	"gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
	"ja":  "じゃ", "ju":  "じゅ", "jo":  "じょ",
	"dja": "ぢゃ", "dju": "ぢゅ", "djo": "ぢょ",
	"bya": "びゃ", "byu": "びゅ", "byo": "びょ",
	"pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",

	"kA": "きゃ", "kU": "きゅ", "kO": "きょ",
	"sA": "しゃ", "sU": "しゅ", "sO": "しょ",
	"cA": "ちゃ", "cU": "ちゅ", "cO": "ちょ",
	"tA": "ちゃ", "tU": "ちゅ", "tO": "ちょ",
	"nA": "にゃ", "nU": "にゅ", "nO": "にょ",
	"hA": "ひゃ", "hU": "ひゅ", "hO": "ひょ",
	"mA": "みゃ", "mU": "みゅ", "mO": "みょ",
	"rA": "りゃ", "rU": "りゅ", "rO": "りょ",
	"gA": "ぎゃ", "gU": "ぎゅ", "gO": "ぎょ",
	"zA": "じゃ", "zU": "じゅ", "zO": "じょ",
	"jA": "じゃ", "jU": "じゅ", "jO": "じょ",
	"dA": "ぢゃ", "dU": "ぢゅ", "dO": "ぢょ",
	"bA": "びゃ", "bU": "びゅ", "bO": "びょ",
	"pA": "ぴゃ", "pU": "ぴゅ", "pO": "ぴょ",

	"she": "しぇ",
	"je":  "じぇ",
	"che": "ちぇ",
	"tsa": "つぁ",
	"tse": "つぇ",
	"tso": "つぉ",
	"ti":  "てぃ",
	"di":  "でぃ",
	"dyu": "でゅ",
	"fa":  "ふぁ",
	"fi":  "ふぃ",
	"fe":  "ふぇ",
	"fo":  "ふぉ",

	"hu": "ふ", "tu": "つ", "si": "し",
	"ca": "ちゃ", "ci": "ち", "cu": "ちゅ", "ce": "ちぇ", "co": "ちょ",
	"wi": "うぃ", "we": "うぇ",
	"zwi": "ゐ", "zwe": "ゑ",

	# "va": "う゛ぁ", "vi": "う゛ぃ", "vu": "う゛", "ve": "う゛ぇ", "vo": "う゛ぉ",
	"va": "ゔぁ", "vi": "ゔぃ", "vu": "ゔ", "ve": "ゔぇ", "vo": "ゔぉ",

	"la":  "ぁ", "li":  "ぃ", "lu":  "ぅ", "le":  "ぇ", "lo":  "ぉ",
	"lya": "ゃ", "lyu": "ゅ", "lyo": "ょ", "ltsu": "っ",
	"lwa": "ゎ", "lka": "ゕ", "lke": "ゖ",

	"zD": "゛", "zd": "\u3099",
	"zH": "゜", "zh": "\u309A",
}
punctuation = {
	"0":  "０", "1":  "１", "2":  "２", "3": "３",
	"4":  "４", "5":  "５", "6":  "６", "7": "７",
	"8":  "８", "9":  "９",

	"[":  "「", "]":  "」",
	"{":  "『", "}":  "』",
	"[[": "《", "]]": "》",
	"{{": "【", "}}": "】",

	" ": "　", "-": "ー", ".": "。", ",": "、", "!": "！", "?": "？",
	"%": "％", "~": "〜", "/": "／", "(": "（", ")": "）", "\"": "＂",
	"<": "﹅", ">": "・", "_": "ー",
	"..": "。", "...": "⋯",
}

def hira2kata(t):
	if ord(t) in range(0x3041, 0x3097):
		return chr(ord(t) + 0x60)
	return t

def toKatakana(text):
	return "".join(hira2kata(ch) for ch in text).replace("ウ゛", "ヴ")

def addKatakana(romkana):
	for k, v in dict(romkana).items():
		k2 = "".join(a.lower() if a.isupper() else a.upper() for a in k)
		if k2 != k and k2 in romkana:
			print(k2)
		if k2 not in romkana:
			romkana[k2] = [toKatakana(text).upper() for text in v]

romkana = {}
for t in っ:
	romkana[t+t] = [t, "っ"]
	romkana[t+"'"] = ["", "っ"]
	romkana[t+'"'] = ["", "っ"]
for k, v in ん.items():
	romkana[k] = v
for k, v in punctuation.items():
	romkana[k] = ["", v, v, v, v]
for k, v in basic.items():
	romkana[k] = ["", v]
addKatakana(romkana)

import json # noqa
out = """
{"define": {"rom-kana": {
%s
}}}
""".strip() % ",\n".join("%s: %s" % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in romkana.items())
import pathlib
pathlib.Path("~/.config/ibus-kkc/rules/default/rom-kana/default.json").expanduser().write_text(out)
