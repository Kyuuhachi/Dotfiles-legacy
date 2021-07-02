from gi.repository import Gdk
import asyncio
from .workspaces import WSProvider, WSState
from icebar.lib.simplei3 import i3ipc

__all__ = ["i3"]

class i3(WSProvider):
	def __init__(self):
		super().__init__()
		asyncio.ensure_future(self.start())

	async def start(self):
		self.__i3_keepalive = i3ipc()
		self.i3 = await self.__i3_keepalive.__aenter__()

		await self.i3.command(i3ipc.SUBSCRIBE, ["workspace", "barconfig_update"])
		self.i3.on_event(self.on_event)

		await self.get_workspaces()
		for bar in await self.i3.command(i3ipc.GET_BAR_CONFIG):
			self.barconfig(await self.i3.command(i3ipc.GET_BAR_CONFIG, bar))

	async def get_workspaces(self):
		ws = []
		for w in await self.i3.command(i3ipc.GET_WORKSPACES):
			ws.append((w["name"], WSState.focused * w["focused"] + WSState.focused_other * w["visible"] + WSState.urgent * w["urgent"]))
		self.emit("workspaces", ws)

	def barconfig(self, barconfig):
		if "focused_workspace_bg" in barconfig["colors"]:
			color = Gdk.RGBA()
			color.parse(barconfig["colors"]["focused_workspace_bg"])
			self.emit("color", tuple(color))

	async def on_event(self, type, payload):
		if type == i3ipc.E_WORKSPACE:
			if payload["change"] in ["focus", "urgent"]:
				await self.get_workspaces()
		if type == i3ipc.E_BARCONFIG_UPDATE:
			self.barconfig(payload)

	def set_workspace(self, name):
		asyncio.ensure_future(self.i3.command(i3ipc.COMMAND, "workspace " + name))
