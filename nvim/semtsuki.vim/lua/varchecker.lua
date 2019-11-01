local ipairs = _G.ipairs
local insert = _G.table.insert
local setmetatable = _G.setmetatable
local type = _G.type

local VarChecker
VarChecker = setmetatable({}, {
	__name = "VarCheckerMeta",
	__call = function()
		local self = setmetatable({}, { __name = "VarChecker", __index = VarChecker })
		self:init()
		return self
	end
})

function VarChecker:init()
	self.vars = { { name = "_ENV" } }
	self.scopes = { self:globalscope() }
	self:push()
end

function VarChecker:globalscope()
	local cache = {}
	return {
		get = function(k)
			if k == "_ENV" then return 1, "upvalue" end
			if not cache[k] then
				insert(self.vars, { name = k, type = "global" })
				cache[k] = #self.vars
			end
			return cache[k], "global"
		end
	}
end

function VarChecker:scope(prev, omode)
	local cache = {}
	return {
		cache = cache,
		get = function(k)
			if cache[k] then return cache[k] end
			local v, mode = prev.get(k)
			return v, mode or omode
		end
	}
end

function VarChecker:push(omode)
	insert(self.scopes, self:scope(self.scopes[#self.scopes], omode))
end

function VarChecker:pop()
	self.scopes[#self.scopes] = nil
end

function VarChecker:ref(node, type)
	local idx, mode = self.scopes[#self.scopes].get(node[1])
	insert(self.vars[idx], {type, mode, node})
end

function VarChecker:new(node, type)
	insert(self.vars, { name=node[1], type=type})
	self.scopes[#self.scopes].cache[node[1]] = #self.vars
	self:ref(node, "decl")
end

local VarCheckerW = {}
function VarCheckerW:Id(node)
	self:ref(node, "read")
end
VarCheckerW.Dots = VarCheckerW.Id
function VarCheckerW:Set(node)
	for _, v in ipairs(node[1]) do if v.tag ~= "Id" then self:walk(v) end end
	for _, v in ipairs(node[2]) do self:walk(v) end
	for _, v in ipairs(node[1]) do if v.tag == "Id" then self:ref(v, "write") end end
end
function VarCheckerW:Local(node)
	for _, v in ipairs(node[2] or {}) do self:walk(v) end
	for _, v in ipairs(node[1]) do self:new(v) end
end
function VarCheckerW:Localwalk(node)
	for _, v in ipairs(node[1]) do self:new(v) end
	for _, v in ipairs(node[2]) do self:walk(v) end
end
function VarCheckerW:If(node)
	for i=1,#node-1,2 do self:walk(node[i]) end
	for i=2,#node,2 do self:push(); self:walk(node[i]); self:pop() end
	if #node % 2 == 1 then self:push(); self:walk(node[#node]); self:pop() end
end
function VarCheckerW:Do(node)
	self:push()
	self:walk(node[1])
	self:pop()
end
function VarCheckerW:While(node)
	self:walk(node[1])
	self:push()
	self:walk(node[2])
	self:pop()
end
function VarCheckerW:Repeat(node)
	self:push()
	self:walk(node[1])
	self:pop()
	self:walk(node[2])
end
function VarCheckerW:Fornum(node)
	for i=2,#node-1 do self:walk(node[i]) end
	self:push()
	self:new(node[1], "loop")
	self:walk(node[#node])
	self:pop()
end
function VarCheckerW:Forin(node)
	for _, v in ipairs(node[2]) do self:walk(v) end
	self:push()
	for _, v in ipairs(node[1]) do self:new(v, "loop") end
	self:walk(node[3])
	self:pop()
end
function VarCheckerW:Function(node)
	self:push("upvalue")
	for _, v in ipairs(node[1]) do self:new(v, "arg") end
	for _, v in ipairs(node[2]) do self:walk(v) end
	self:pop()
end
function VarCheckerW:default(node)
	for _, v in ipairs(node) do self:walk(v) end
end

function VarChecker:walk(node)
	if type(node) == "table" then
		(VarCheckerW[node.tag] or VarCheckerW.default)(self, node)
	end
end

return VarChecker
