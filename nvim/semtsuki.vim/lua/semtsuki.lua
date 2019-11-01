local require = _G.require
local VarChecker = require"varchecker"
local parser = require"parser"

local Semtsuki = {}
function Semtsuki.run(source)
	local source2 = {
		get_codepoint = function(self, idx) return string.byte(source, idx) end,
		get_substring = function(self, from, to) return string.sub(source, from, to) end,
		get_length = function(a) return #a end,
		find = function(self, pattern, from) return string.find(source, pattern, from) end,
		get_printable_substring = function(self, from, to) return source:sub(from, to):gsub("[^\32-\126]", function(byte) return ("\\x%02X"):format(sbyte(byte)) end) end
	}
	local line_offsets = {}
	local line_lengths = {}
	local ast = parser.parse(source2, line_offsets, line_lengths)
	local vc = VarChecker()
	vc:walk(ast)
	return vc.vars
end
return Semtsuki
