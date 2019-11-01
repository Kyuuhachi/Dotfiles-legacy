local type = _ENV.type
local pairs, next = _ENV.pairs, _ENV.next
local tostring = _ENV.tostring
local getmetatable, setmetatable = _ENV.getmetatable, _ENV.setmetatable
local insert, remove, concat
do
	local table = _ENV.table
	insert, remove, concat = table.insert, table.remove, table.concat
end
local format, rep, find, gsub, byte, char
do
	local string = _ENV.string
	format, rep, find, gsub, byte, char = string.format, string.rep, string.find, string.gsub, string.byte, string.char
end
local getinfo, getlocal, getupvalue
do
	local debug = _ENV.debug or {}
	getinfo, getlocal, getupvalue = debug.getinfo, debug.getlocal, debug.getupvalue
end
local huge = _ENV.math.huge


local repr

local kwds = {}
for _,w in pairs{"and", "break", "do", "else", "elseif", "end", "false", "for", "function", "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while" -- end end
} do
	kwds[w] = true
end

local function chain(obj)
	return setmetatable({}, {__index=obj, __name = "chain"})
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

repr = {
	table = setmetatable({
		index = function(buf,obj,parent)
			if parent then insert(buf,parent) end
			if find(obj, "^[%a_][%w_]*$") and not kwds[obj] then
				if parent then insert(buf, ".") end
				return insert(buf, obj)
			else
				insert(buf, "[")
				repr.string(buf, obj)
				return insert(buf, "]")
			end
		end
	}, {
		__call = function(table,buf,obj,cache,pretty,level)
			if cache[obj] then return insert(buf, "{::}") end
			-- if cache[obj] then return "::"..cache[o].."::" end
			cache[obj] = true

			do
				local tostr = gettostr(obj)
				if tostr ~= nil then return insert(buf, tostr(obj)) end
			end

			do
				local mt = getmetatable(obj)
				if mt then
					local name = mt.__name
					if type(name) == "string" then
						insert(buf, name)
					else
						insert(buf, "?")
			end	end	end

			if next(obj) == nil then return insert(buf, "{}") end

			insert(buf, "{")
			local index = 1
			for k, v in pairs(obj) do
				if(level < pretty) then insert(buf, "\n"..rep("\t", level+1)) end
				if index == k then
					index = index + 1
				else
					index = nil
					if type(k) == "string" then
						table.index(buf,k)
						insert(buf, " = ")
					else
						insert(buf, "[")
						repr._any(buf, k, chain(cache), -1, 0)
						insert(buf, "] = ")
					end
				end
				repr._any(buf, v, chain(cache), pretty, level+1)
				if not pretty then
					insert(buf, ", ")
				else
					insert(buf, ",")
				end
			end
			remove(buf)
			if(level < pretty) then insert(buf, "\n"..rep("\t", level)) end
			return insert(buf, "}")
		end,
		__name = "repr.table"
	}),

	string = setmetatable((function()
		local function hex(ch)
			return format("\\x%02X", byte(ch))
		end
		local function const(obj)
			return function() return obj end
		end
		local function optquote(ch, quote)
			if quote == ch then return "\\"..ch else return ch end
		end

		local string = {}
		for i = 0, 31 do string[char(i)] = hex end
		for i = 127, 255 do string[char(i)] = hex end
		string["\a"] = const("\\a")
		string["\b"] = const("\\b")
		string["\t"] = const("\\t")
		string["\n"] = const("\\n")
		string["\v"] = const("\\v")
		string["\f"] = const("\\f")
		string["\r"] = const("\\r")
		string["\\"] = const("\\\\")
		string["\'"] = optquote
		string["\""] = optquote
		return string
	end)(), {
		__call = function(string,buf,obj)
			local sing = gsub(obj, ".", function(ch)
				if string[ch] then return string[ch](ch, "\'") else return ch end
			end)
			local doub = gsub(obj, ".", function(ch)
				if string[ch] then return string[ch](ch, "\"") else return ch end
			end)
			if #sing < #doub then
				insert(buf, "\'")
				insert(buf, sing)
				return insert(buf, "\'")
			else
				insert(buf, "\"")
				insert(buf, doub)
				return insert(buf, "\"")
			end
		end,
		__name = "repr.string",
		__tostring = function(t) return getmetatable(t).__name .. "{...}" end
	}),

	["function"] = setmetatable({
		getinfo = function(obj)
			local info = getinfo(obj, "Su")
			-- if info.what == "C" then return tostring(obj) end
			local params = {}
			for i= 1, info.nparams do
				params[i] = getlocal(obj, i)
			end
			info.params = params
			local ups = {}
			for i= 1, info.nups do
				ups[i] = getupvalue(obj, i)
			end
			info.ups = ups
			return info
		end,

		name = function(buf,info)
			insert(buf, info.short_src)
			local ln = info.linedefined
			if ln ~= -1  and info.what ~= "main" then
				insert(buf, ":")
				insert(buf, ln)
			end
		end,

		args = function(buf,info)
			local npar = info.nparams
			local par = info.params
			for i= 1, npar do
				insert(buf, par[i])
				insert(buf, ", ")
			end
			if info.isvararg then
				insert(buf, "...")
			elseif npar > 0 then
				remove(buf)
			end
		end,

		body = function(buf,info)
			insert(buf, "{")
			local nups = info.nups
			local ups = info.ups
			if nups > 0 then
				for i= 1, nups do
					local upn = ups[i]
					if upn == "" then
						insert(buf, "?")
					else
						insert(buf, upn)
					end
					insert(buf, ", ")
				end
				remove(buf)
			end
			insert(buf, "} ")
		end
	}, {
		__call = function(t,buf,obj)
			local info = t.getinfo(obj, "Su")
			if type(info) == "string" then return insert(buf, info) end
			insert(buf, "function ")
			t.name(buf,info)
			insert(buf,"(")
			t.args(buf,info)
			insert(buf,") ")
			t.body(buf,info)
			insert(buf, "end")
		end,
		__name = "repr.function" -- end
	}), -- end

	_any = function(buf,obj,cache,pretty,level)
		local tostr = gettostr(obj)
		if tostr then return insert(buf, tostr(obj)) end
		local mt = getmetatable(obj)
		local r = mt and mt._repr or repr[type(obj)] or repr._fallback
		return r(buf,obj,cache,pretty,level)
	end,

	_fallback = function(buf, obj)
		return insert(buf, tostring(obj))
	end,

	insert = function(buf,obj,pretty,cache,level)
		if not pretty then pretty = huge end
		cache = cache or {}
		level = level or 0
		return repr._any(buf,obj,cache,pretty,level)
	end
}

if not getinfo then
	repr["function"].getinfo = tostring -- end
end

return setmetatable(repr, {
	__call = function(r,obj,pretty)
		local buf = {}
		r.insert(buf, obj, pretty)
		return concat(buf)
	end,
	-- __tostring = repr,
	__name = "repr"
})
