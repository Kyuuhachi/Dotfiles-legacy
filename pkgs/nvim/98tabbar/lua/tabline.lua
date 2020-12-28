local _ENV = _G -- luacheck: ignore
local ipairs = _ENV.ipairs
local tostring = _ENV.tostring
local concat = _ENV.table.concat
local format = _ENV.string.format
local unpack = _ENV.unpack
local floor = _ENV.math.floor
local insert = _ENV.table.insert

local nvim = _ENV.setmetatable({}, { __index = function(_, key) return _ENV.vim.api["nvim_" .. key] end })
local vim = _ENV.setmetatable({}, { __index = function(_, key) return function(...) return nvim.call_function(key, {...}) end end })
local function command(a, ...) nvim.command(concat({a, ...}, " ")) end

local function initColors()
	local function hi(a, b, fg, bg)
		command("hi", "clear", "TabSep"..a..b)
		local args = {}
		if bg ~= "" then args[#args+1] = "ctermbg="..bg end
		if fg ~= "" then args[#args+1] = "ctermfg="..fg end
		if #args > 0 then
			command("hi", "TabSep"..a..b, unpack(args))
		end
	end
	local function bg(name)
		return vim.synIDattr(vim.synIDtrans(vim.hlID(name)), "bg")
	end
	local lbg = bg("TabL")
	local rbg = bg("TabR")
	for ai = 1,4 do
		local a = tostring(ai)
		local abg = bg("Tab"..a)
		hi(a, a, "black", abg)
		for bi = ai+1,4 do
			local b = tostring(bi)
			local bbg = bg("Tab"..b)
			hi(a, b, abg, bbg)
		end
		hi("l", a, lbg, abg)
		hi(a, "R", abg, rbg)
	end
end

initColors()

local function fcomp_default(a, b) return a < b end
local function bininsert(t, value, fcomp)
	fcomp = fcomp or fcomp_default
	local iStart, iEnd, iMid, iState = 1, #t, 1, 0
	while iStart <= iEnd do
		iMid = floor((iStart+iEnd)/2)
		if fcomp(value, t[iMid]) then
			iEnd, iState = iMid - 1, 0
		else
			iStart, iState = iMid + 1, 1
		end
	end
	insert(t, iMid+iState, value)
	return iMid + iState
end

local function listBuffers()
	local function compfn(a, b)
		return vim.matchstr(vim.bufname(a), "[^/]*$") < vim.matchstr(vim.bufname(b), "[^/]*$")
	end
	local seen = {}
	local function add(where, buf)
		if seen[buf] then return end
		seen[buf] = true
		bininsert(where, buf, compfn)
	end
	local current = {}
	local currenttab = {}
	local othertabs = {}
	local hidden = {}
	add(current, nvim.get_current_buf())
	for _, win in ipairs(nvim.tabpage_list_wins(nvim.get_current_tabpage())) do
		add(currenttab, nvim.win_get_buf(win))
	end
	for _, tab in ipairs(nvim.list_tabpages()) do
		for _, win in ipairs(nvim.tabpage_list_wins(tab)) do
			local buf = nvim.win_get_buf(win)
				add(othertabs, buf)
		end
	end
	for _, buf in ipairs(nvim.list_bufs()) do
		add(hidden, buf)
	end
	return { current, currenttab, othertabs, hidden }
end

local function getTabLine()
	local maxwidth = nvim.get_option("columns")
	local width = 0
	local lastC = "L"
	local out = {"%#TabL#"}
	local function append(s)
		if width + nvim.strwidth(s) <= maxwidth then
			out[#out+1] = s
			width = width + nvim.strwidth(s)
		elseif width <= maxwidth then
			for _, c in ipairs(vim.split(s, "\\zs")) do
				width = width + nvim.strwidth(c)
				if width <= maxwidth then
					out[#out+1] = c
				else
					break
				end
			end
		end
	end
	local function sep(to)
		width = width + 1
		if width <= maxwidth then
			out[#out+1] = format("%%#TabSep%s%s#%s%%#Tab%s#", lastC, to, lastC == to and "" or "", to)
		end
		lastC = to
	end

	if #nvim.list_tabpages() > 1 then
		append(format(" [%s/%s] ", nvim.tabpage_get_number(nvim.get_current_tabpage()), #nvim.list_tabpages()))
	end
	for c, list in ipairs(listBuffers()) do
		for _, buf in ipairs(list) do
			if vim.buflisted(buf) and nvim.buf_get_option(buf, "buftype") == "" and nvim.buf_is_loaded(buf) then
				sep(c)
				local flags = {}
				if nvim.buf_get_option(buf, "modified") then flags[#flags+1] = "*" end
				if nvim.buf_get_name(buf) ~= "" then
					append(" "..concat(flags)..vim.matchstr(vim.bufname(buf), "[^/]\\+$").." ")
				else
					append("❰"..concat(flags)..tostring(buf).."❱")
				end
				if width > maxwidth then goto exit end
			end
		end
	end
	sep("R")
	::exit::

	return concat(out)
end

return getTabLine
