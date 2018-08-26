import socket
import fcntl
import struct
import array
import ipaddress

# see /usr/include/linux/if.h and sockios.h
SIOCGIWESSID = 0x8B1B
SIOCGIWSTATS = 0x8B0F
SIOCGIFFLAGS = 0x8913
SIOCGIFADDR = 0x8915
SIOCGIFHWADDR = 0x8927

SIOCGIFCONF = 0x8912

IFF_UP = 1<<0

def ioctl_ptr(sock, ctl, name, buffer, flags=0):
	fmt = "<16sQHH"
	buf = array.array("B", struct.pack(fmt, name, buffer.buffer_info()[0], len(buffer), 0))
	fcntl.ioctl(sock.fileno(), ctl, buf)
	buffer_len = struct.unpack(fmt, buf)[2]
	return buffer.tobytes()[:buffer_len]

def get_name(sock):
	buffer = array.array('B', bytes(40*32))
	buf = array.array("B", struct.pack("IN", 1024, buffer.buffer_info()[0]))
	fcntl.ioctl(sock.fileno(), SIOCGIFCONF, buf)
	size = struct.unpack("IN", buf)[0]
	for a in reversed(range(0, size, 40)):
		yield bytes(buffer[a:a+16])

def get_up(sock, name):
	fmt = "<16sH"
	buf = array.array("B", struct.pack(fmt, name, 0))
	fcntl.ioctl(sock.fileno(), SIOCGIFFLAGS, buf)
	flags = struct.unpack(fmt, buf)[1]
	return bool(flags & IFF_UP)

def get_essid(sock, name):
	buf = array.array('B', bytes(32))
	return ioctl_ptr(sock, SIOCGIWESSID, name, buf).decode()

def get_quality(sock, name):
	buf = array.array('B', bytes(32))
	ret = ioctl_ptr(sock, SIOCGIWSTATS, name, buf)
	return ret[2]

def get_ipv4(sock, name):
	fmt = "<16sH2s4s"
	buf = array.array("B", struct.pack(fmt, name, 0, b"", b""))
	fcntl.ioctl(sock.fileno(), SIOCGIFADDR, buf)
	a = struct.unpack(fmt, buf)[3]
	return str(ipaddress.IPv4Address(int.from_bytes(a, "big")))

def get_ipv6(sock, name):
	with open("/proc/net/if_inet6") as f:
		inet6 = f.read().strip().split("\n")
		for line in inet6:
			addr, id, prefix, scope, flags, name_ = line.split()
			if name_ == name:
				return str(ipaddress.IPv6Address(int(addr, 16)))

def get_mac(sock, name):
	fmt = "<16sH6s"
	buf = array.array("B", struct.pack(fmt, name, 0, b""))
	fcntl.ioctl(sock.fileno(), SIOCGIFHWADDR, buf)
	a = struct.unpack(fmt, buf)[2]
	return ":".join("%02x" % i for i in a)

def wifi_status():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for name in get_name(s):
		try:
			up = get_up(s, name)
			essid = get_essid(s, name)
			quality = get_quality(s, name)
			ipv4 = get_ipv4(s, name)
			ipv6 = get_ipv6(s, name)
			mac = get_mac(s, name)
			yield (name.rstrip(b'\0').decode(), up, essid, quality, ipv4, ipv6, mac)
		except OSError:
			pass
	s.close()
