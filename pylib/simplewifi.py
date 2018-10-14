import socket
import fcntl
import struct
import array
import os

# see /usr/include/linux/if.h and sockios.h
SIOCGIWESSID = 0x8B1B
SIOCGIWSTATS = 0x8B0F
SIOCGIFFLAGS = 0x8913
SIOCGIFADDR = 0x8915
SIOCGIFHWADDR = 0x8927

SIOCGIFCONF = 0x8912

IFF_UP = 1<<0

def ioctl_ptr(sock, ctl, name, buffer):
	fmt = "<16sQHH"
	buf = array.array("B", struct.pack(fmt, name, buffer.buffer_info()[0], len(buffer), 0))
	fcntl.ioctl(sock.fileno(), ctl, buf)
	buffer_len = struct.unpack(fmt, buf)[2]
	return buffer.tobytes()[:buffer_len]

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

import ctypes as c
import ctypes.util

P = c.POINTER

class struct_sockaddr(c.Structure):
	_fields_ = [ ('family', c.c_ushort), ('data', c.c_byte * 14) ]

class struct_sockaddr_in(c.Structure):
	_fields_ = [ ('family', c.c_ushort), ('port', c.c_uint16), ('addr', c.c_byte * 4) ]

class struct_sockaddr_in6(c.Structure):
	_fields_ = [ ('family', c.c_ushort), ('port', c.c_uint16), ('flowinfo', c.c_uint32), ('addr', c.c_byte * 16), ('scope_id', c.c_uint32) ]

class struct_sockaddr_ll(c.Structure):
	_fields_ = [ ('family', c.c_ushort), ('protocol', c.c_ushort), ('ifindex', c.c_int), ('hatype', c.c_ushort), ('pkttype', c.c_byte), ('halen', c.c_byte), ('addr', c.c_ubyte * 8) ]

class union_ifa_ifu(c.Union):
	_fields_ = [ ('broadaddr', P(struct_sockaddr)), ('dstaddr', P(struct_sockaddr)) ]

class struct_ifaddrs(c.Structure): pass
struct_ifaddrs._fields_ = [ ('next', P(struct_ifaddrs)), ('name', c.c_char_p), ('flags', c.c_uint), ('addr', P(struct_sockaddr)), ('netmask', P(struct_sockaddr)), ('ifu', union_ifa_ifu), ('data', c.c_void_p) ]

libc = c.CDLL(ctypes.util.find_library('c'))

def ifap_iter(ifap):
	ifa = ifap.contents
	while True:
		yield ifa
		if not ifa.next:
			break
		ifa = ifa.next.contents

def getifaddrs(name):
	ifap = P(struct_ifaddrs)()
	if libc.getifaddrs(c.pointer(ifap)) != 0:
		raise OSError(c.get_errno())
	try:
		ipv4 = ipv6 = mac = None
		for ifa in ifap_iter(ifap):
			if name != ifa.name:
				continue
			fam = ifa.addr.contents.family
			if fam == socket.AF_INET:
				sa = c.cast(ifa.addr, c.POINTER(struct_sockaddr_in)).contents
				ipv4 = socket.inet_ntop(sa.family, sa.addr)
			elif fam == socket.AF_INET6:
				sa = c.cast(ifa.addr, c.POINTER(struct_sockaddr_in6)).contents
				ipv6 = socket.inet_ntop(sa.family, sa.addr)
			elif fam == socket.AF_PACKET:
				sa = c.cast(ifa.addr, c.POINTER(struct_sockaddr_ll)).contents
				mac = ":".join(f"{x:02x}" for x in sa.addr[:sa.halen])
		return ipv4, ipv6, mac
	finally:
		libc.freeifaddrs(ifap)

def wifi_status():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for name in os.listdir("/sys/class/net"):
		if not os.path.exists(f"/sys/class/net/{name}/wireless"): continue
		try:
			up = get_up(s, name.encode())
			essid = get_essid(s, name.encode())
			try:
				quality = get_quality(s, name.encode())
			except OSError:
				quality = None
			ipv4, ipv6, mac = getifaddrs(name.encode())
			yield (name, up, essid, quality, ipv4, ipv6, mac)
		except OSError:
			import traceback
			traceback.print_exc()
			pass
	s.close()
