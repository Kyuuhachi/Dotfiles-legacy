import os
import socket
import i3py.util

_server_address = '/tmp/i3py'
_handlers = {}

def start():
	try:
		os.unlink(_server_address)
	except OSError:
		if os.path.exists(_server_address):
			raise
	_run()

@i3py.util.OtherThread
def _run():
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.bind(_server_address)
	sock.listen(1)
	while True:
		connection, client_address = sock.accept()
		try:
			f = connection.makefile()
			for line in f:
				split = line.split()
				if split[0] in _handlers:
					_handlers[split[0]](*split[1:])
		finally:
			connection.shutdown(socket.SHUT_RDWR)
			connection.close()

def register(command, handler):
	_handlers[command] = handler

start()
