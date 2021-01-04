import json
import struct
import contextlib
import anyio

class i3ipc:
	[ COMMAND
	, GET_WORKSPACES
	, SUBSCRIBE
	, GET_OUTPUTS
	, GET_TREE
	, GET_MARKS
	, GET_BAR_CONFIG
	, GET_VERSION
	, GET_BINDING_MODES
	, GET_CONFIG
	, SEND_TICK
	, SYNC
	, GET_BINDING_STATE
	] = range(13)

	[ E_WORKSPACE
	, E_OUTPUT
	, E_MODE
	, E_WINDOW
	, E_BARCONFIG_UPDATE
	, E_BINDING
	, E_SHUTDOWN
	, E_TICK
	] = range(8)

	_MAGIC = b"i3-ipc"
	_FORMAT = "=6sII"

	def __init__(self):
		self._handlers = None
		self._command_lock = None
		self._pending = None
		self._group = None
		self._sock = None
		self.__cmgr = None

	@contextlib.asynccontextmanager
	async def __new__(cls):
		self = super().__new__(cls)
		self._handlers = []
		self._command_lock = anyio.create_lock()
		import sys
		self._keepalive = sys._getframe()
		async with anyio.create_task_group() as self._group:
			proc = await anyio.run_process(["i3", "--get-socketpath"])
			path = proc.stdout.decode().strip()
			async with await anyio.connect_unix(path) as self._sock:
				await self._group.spawn(self._loop)
				yield self
				await self._group.cancel_scope.cancel()

	async def _loop(self):
		while True:
			msgtype, payload = await self._recvmsg()
			if msgtype & 0x80000000:
				msgtype &= 0x7FFFFFFF
				for f in self._handlers:
					await self._group.spawn(f, msgtype, payload)
			else:
				assert msgtype == self._pending["msgtype"]
				self._pending["response"] = payload
				await self._pending["event"].set()

	async def _recvmsg(self):
		magic, length, msgtype = struct.unpack(self._FORMAT, await self._sock.receive(14))
		assert magic == self._MAGIC
		payload = await self._sock.receive(length)
		assert len(payload) == length
		return msgtype, json.loads(payload)

	async def command(self, msgtype, payload=b""):
		if isinstance(payload, (list, dict)):
			payload = json.dumps(payload).encode()
		elif isinstance(payload, str):
			payload = payload.encode("utf-8")
		elif isinstance(payload, bytes):
			pass
		else:
			raise ValueError(type(payload))

		async with self._command_lock:
			try:
				self._pending = {
					"event": anyio.create_event(),
					"msgtype": msgtype,
					"response": None,
				}
				await self._sock.send(struct.pack(self._FORMAT, self._MAGIC, len(payload), msgtype))
				await self._sock.send(payload)
				await self._pending["event"].wait()
				return self._pending["response"]
			finally:
				self._pending = None

	def on_event(self, f):
		self._handlers.append(f)
