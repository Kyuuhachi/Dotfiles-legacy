local type = _ENV.type
local pairs, ipairs = _ENV.pairs, _ENV.ipairs
local getmetatable = _ENV.getmetatable
local insert, concat, unpack
do
	local table = _ENV.table
	insert, concat, unpack = table.insert, table.concat, table.unpack
end
local rep, find
do
	local string = _ENV.string
	rep, find = string.rep, string.find
end
local huge = _ENV.math.huge

local repr0 = _ENV.require"repr"

local function flatten(buf, tree)
	if type(tree) == "table" then
		for _, v in ipairs(tree) do
			flatten(buf, v)
		end
	else
		insert(buf, tree)
	end
end

local function gettostr(obj)
	local mt = getmetatable(obj)
	if mt ~= nil then
		local tostr = mt.__tostring
		if tostr ~= repr then
			return tostr
		end
	end
end

local kwds = {}
for _,w in ipairs{"and", "break", "do", "else", "elseif", "end", "false", "for", "function", "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while"} do -- end end
	kwds[w] = true
end

local function formatKey(buf, obj, hasParent)
	if type(obj) == "table" then
		insert(buf, "[?]")
	elseif type(obj) == "string" and find(obj, "^[%a_][%w_]*$") and not kwds[obj] then
		if hasParent then insert(buf, ".") end
		insert(buf, obj)
	else
		insert(buf, "[")
		repr0.insert(buf, obj)
		insert(buf, "]")
	end
end

local function ref2str(obj)
	if not obj then return "_TOP" end
	local o = {}
	while obj do
		o[#o+1], obj = unpack(obj)
	end
	local buf = {}
	for i=#o,1,-1 do
		formatKey(buf, o[i], #buf > 0)
	end
	return concat(buf)
end

local function doKey(cache, obj, buf)
	if cache[obj]then
		insert(buf, "[::")
		insert(buf, cache[obj])
		insert(buf, "::]")
	else
		formatKey(buf, obj)
	end
end

local function doVal(cache, keyQ, valQ, pretty, obj, buf, depth, ref)
	if type(obj) ~= "table" then
		repr0.insert(buf, obj)
	elseif cache[obj] then
		insert(buf, "::")
		insert(buf, cache[obj])
		insert(buf, "::")
	else
		cache[obj] = ref2str(ref)

		local tostr = gettostr(obj)
		local mt = getmetatable(obj)
		if tostr ~= nil then
			insert(buf, tostr(obj))
		else
			if mt then
				local name = mt.__name
				if type(name) == "string" then
					insert(buf, name)
				else
					insert(buf, "?")
				end
				if depth >= pretty then insert(buf, " ") end
			end

			insert(buf, "{")
			local idx = 1
			local comma = ""
			for k, v in pairs(obj) do
				insert(buf, comma)
				comma = ","
				if depth >= pretty then
					insert(buf, " ")
				else
					insert(buf, "\n"..rep("\t", depth+1))
				end

				if k == idx then
					idx = idx + 1
				else
					local kbuf = {}
					insert(buf, kbuf)
					insert(keyQ, {k, kbuf})
					insert(buf, " = ")
				end

				local vbuf = {}
				insert(buf, vbuf)
				insert(valQ, {v, vbuf, depth+1, {k, ref}})
			end
			if comma ~= "" then
				if depth >= pretty then
					insert(buf, " ")
				else
					insert(buf, "\n"..rep("\t", depth))
				end
			end
			insert(buf, "}")
		end
	end
end

local function repr(obj, pretty)
	if pretty == nil then pretty = huge end

	local topbuf = {}
	local keyQ = {} -- {obj, buf}
	local valQ = { {obj, topbuf, 0, nil} } -- {obj, buf, depth, ref}
	local cache = {}

	for _, val in ipairs(valQ) do
		local obj, buf, depth, ref = unpack(val)
		doVal(cache, keyQ, valQ, pretty, obj, buf, depth, ref)
	end

	for _, val in ipairs(keyQ) do
		local obj, buf = unpack(val)
		doKey(cache, obj, buf)
	end

	local buf = {}
	flatten(buf, topbuf)
	return concat(buf)
end

return repr
-- print(repr(_ENV, 2))
-- print(repr(_ENV))
-- print(repr("670132\x1B"))
