import anyio
import simplei3

async def __main__():
	async with simplei3.i3ipc() as i3ipc:
		tree = await i3ipc.command(i3ipc.GET_TREE)
		scratch = [
			node["nodes"][0]
			for node in tree["nodes"] if node["name"] == "__i3"
			for node in node["nodes"] if node["name"] == "content"
			for node in node["nodes"] if node["name"] == "__i3_scratch"
			for node in node["floating_nodes"]
		]
		if scratch:
			await i3ipc.command(i3ipc.COMMAND, f"[con_id={scratch[-1]['id']}] focus")

if __name__ == "__main__":
	anyio.run(__main__)
