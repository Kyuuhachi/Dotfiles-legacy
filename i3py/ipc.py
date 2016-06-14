import os
import socket
import i3py.util

class Ipc:
	server_address = '/tmp/i3py'

	def __init__(self):
		self.handlers = {}
	
	def start(self):
		try:
			os.unlink(self.server_address)
		except OSError:
			if os.path.exists(self.server_address):
				raise
		i3py.util.OtherThread(self.run)()

	def run(self):
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.bind(self.server_address)
		sock.listen(1)
		while True:
			connection, client_address = sock.accept()
			try:
				f = connection.makefile()
				print(dir(f))
				for line in f:
					split = line.split()
					if split[0] in self.handlers:
						self.handlers[split[0]](*split[1:])
			finally:
				connection.shutdown(socket.SHUT_RDWR)
				connection.close()

	def register(self, command, handler):
		self.handlers[command] = handler
