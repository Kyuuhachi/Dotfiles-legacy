from simplei3 import i3ipc
import asyncio
import Xlib.display

def change(name):
	print(name)

async def main():
	i3 = await i3ipc()

	await i3.command(i3ipc.SUBSCRIBE, ["workspace"])
	@i3.on_event
	async def on_event(type, payload):
		if payload["change"] == "focus":
			print(payload["current"]["name"])
	for ws in await i3.command(i3ipc.GET_WORKSPACES):
		if ws["focused"]:
			change(ws["name"])

display = Xlib.display.Display()
def on_event():
	while display.pending_events():
		display.next_event()
asyncio.get_event_loop().add_reader(display.fileno(), on_event)

asyncio.ensure_future(main())
asyncio.get_event_loop().run_forever()
