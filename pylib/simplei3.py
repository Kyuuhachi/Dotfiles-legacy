import json
import asyncio
import struct

class i3ipc:
	COMMAND, GET_WORKSPACES, SUBSCRIBE, GET_OUTPUTS, GET_TREE, GET_MARKS, GET_BAR_CONFIG, GET_VERSION, GET_BINDING_MODES = range(9)
	E_WORKSPACE, E_OUTPUT, E_MODE, E_WINDOW, E_BARCONFIG_UPDATE, E_BINDING = range(6)

	_MAGIC = b"i3-ipc"
	_FORMAT = "=6sII"

	async def __new__(cls, *args):
		self = super().__new__(cls)
		await self._start()
		self._queue = asyncio.Queue()
		self._eventhandlers = []
		asyncio.ensure_future(self._read())
		return self

	async def _start(self):
		proc = await asyncio.create_subprocess_exec("i3", "--get-socketpath", stdout=asyncio.subprocess.PIPE)
		await proc.wait()
		stdout, _ = await proc.communicate()
		self._r, self._w = await asyncio.open_unix_connection(stdout.decode().strip())

	async def _read(self):
		while True:
			msgtype, payload = await self.recvmsg()
			if msgtype & 0x80000000:
				msgtype &= 0x7FFFFFFF
				asyncio.gather(*(f(msgtype, payload) for f in self._eventhandlers))
			else:
				msgtype2, fut = await self._queue.get()
				assert msgtype2 == msgtype
				fut.set_result(payload)

	async def recvmsg(self):
		magic, length, msgtype = struct.unpack(self._FORMAT, await self._r.read(14))
		assert magic == self._MAGIC
		payload = await self._r.read(length)
		return msgtype, json.loads(payload)

	async def command(self, msgtype, payload=None):
		if payload is None:
			payload = b""
		elif isinstance(payload, (list, dict)):
			payload = json.dumps(payload).encode()
		elif isinstance(payload, str):
			payload = payload.encode()
		else:
			raise ValueError(type(payload))
		fut = asyncio.Future()
		await self._queue.put((msgtype, fut))
		self._w.write(struct.pack(self._FORMAT, self._MAGIC, len(payload), msgtype))
		self._w.write(payload)
		return await fut

	def on_event(self, f):
		self._eventhandlers.append(f)
