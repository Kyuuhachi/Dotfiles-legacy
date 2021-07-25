import pynvim as neovim
import inotipy

import typing as T
import asyncio
import os
import os.path

@neovim.plugin
class Stalk:
	def __init__(self, nvim: neovim.api.nvim.Nvim) -> None:
		self.nvim = nvim
		self.running = False
		self.watcher = inotipy.Watcher.create()
		self.buffers = {}

	# If 'backup' is on, then the old file is moved to ~/.vim-backup/ before
	# saving. This obviously doesn't work very well with stalking, so I disable
	# it in BufWritePre and reenable it in BufWritePost.

	# There's no actual reason to disable it in the other *Pre events, it's just
	# for consistency. Can't hurt I guess.

	locals().update({
		f"event_{e}":
			neovim.autocmd(e, eval="[expand('<abuf>'), expand('<afile>:p')]")
				(lambda self, val: self.assoc(int(val[0]), val[1]))
		for e in [ "BufNew", "BufAdd", "BufReadPost", "BufFilePost", "BufWritePost" ]
	})

	locals().update({
		f"event_{e}":
			neovim.autocmd(e, eval="[expand('<abuf>')]")
				(lambda self, val: self.clear(int(val[0])))
		for e in [ "BufUnload", "BufReadPre", "BufFilePre", "BufWritePre" ]
	})

	def start(self) -> None:
		if not self.running:
			self.running = True
			asyncio.ensure_future(self.run(), loop=self.nvim.loop)

	async def run(self):
		while True:
			event = await self.watcher.get()
			for buf, (fd, watch) in self.buffers.items():
				if watch is event.watch:
					newname = os.readlink("/proc/self/fd/%d" % fd.fileno())
					self.nvim.async_call(self.rename, buf, newname)
					break

	def rename(self, buf, newname) -> None:
		# :w demands a confirmation after this; there doesn't seem to be any way around that.
		self.nvim.buffers[buf].name = os.path.relpath(newname)

	def assoc(self, abuf: int, afile: str) -> None:
		self.clear(abuf)
		self.start()
		try:
			file = open(afile, "rb")
		except FileNotFoundError:
			return
		try:
			watch = self.watcher.watch(afile, inotipy.IN.MOVE_SELF)
		except Exception:
			file.close()
			raise
		self.buffers[abuf] = (file, watch)

	def clear(self, abuf: int) -> None:
		if abuf in self.buffers:
			file, watch = self.buffers.pop(abuf)
			watch.remove()
			file.close()
