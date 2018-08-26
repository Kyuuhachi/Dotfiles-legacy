import ctypes as c
import struct
import functools

class asound:
	__init__ = None

	P = c.POINTER
	p = c.pointer
	def errno(i):
		if i != 0:
			raise ValueError(i)
	def fn(f, ret, *args):
		f.restype = ret
		f.argtypes = args
		return f
	asound = c.CDLL("libasound.so")

	chanid = c.c_int

	mixp = c.c_void_p
	selem = c.c_void_p
	open            = fn(asound.snd_mixer_open,            errno, P(mixp), c.c_int)
	attach          = fn(asound.snd_mixer_attach,          errno, mixp, c.c_char_p)
	selem_register  = fn(asound.snd_mixer_selem_register,  errno, mixp, c.c_void_p, P(c.c_void_p))
	load            = fn(asound.snd_mixer_load,            errno, mixp)

	find_selem                       = fn(asound.snd_mixer_find_selem,                       selem, mixp, c.c_void_p)

	selem_has_playback_channel       = fn(asound.snd_mixer_selem_has_playback_channel,       c.c_bool, selem, chanid)

	selem_get_playback_dB            = fn(asound.snd_mixer_selem_get_playback_dB,            errno, selem, chanid, P(c.c_long))
	selem_set_playback_dB            = fn(asound.snd_mixer_selem_set_playback_dB,            errno, selem, chanid, c.c_long)
	selem_set_playback_dB_all        = fn(asound.snd_mixer_selem_set_playback_dB_all,        errno, selem, c.c_long)

	selem_get_playback_switch        = fn(asound.snd_mixer_selem_get_playback_switch,        errno, selem, chanid, P(c.c_bool))
	selem_set_playback_switch        = fn(asound.snd_mixer_selem_set_playback_switch,        errno, selem, chanid, c.c_bool)
	selem_set_playback_switch_all    = fn(asound.snd_mixer_selem_set_playback_switch_all,    errno, selem, c.c_bool)

	selem_get_playback_dB_range      = fn(asound.snd_mixer_selem_get_playback_dB_range,      errno, selem, P(c.c_long), P(c.c_long))

	class pollfd(c.Structure):
		_fields_ = [
			("fd", c.c_int),
			("events", c.c_short),
			("revents", c.c_short),
		]
	poll_descriptors = fn(asound.snd_mixer_poll_descriptors, c.c_int, mixp, P(pollfd), c.c_uint)
	poll_descriptors_count = fn(asound.snd_mixer_poll_descriptors_count, c.c_int, mixp)

	elem_callback = c.CFUNCTYPE(c.c_int, mixp, c.c_uint)
	elem_set_callback = fn(asound.snd_mixer_elem_set_callback, None, selem, elem_callback)
	handle_events = fn(asound.snd_mixer_handle_events, mixp)

class _alsa_array:
	__slots__ = ["__selem", "__get", "__set", "__setall", "__type"]
	def __init__(self, selem, get, set, setall, type):
		self.__selem = selem
		self.__get = get
		self.__set = set
		self.__setall = setall
		self.__type = type
	def __setitem__(self, k, v):
		return self.__set(self.__selem.handle, k, v)
	def __getitem__(self, k):
		p = self.__type()
		self.__get(self.__selem.handle, k, p)
		return p.value
	def __iter__(self):
		for a in range(32):
			if a in self.__selem:
				yield self[a]
	@property
	def all(self):
		return max(self)
	@all.setter
	def all(self, v):
		self.__setall(self.__selem.handle, v)

class Selem:
	__slots__ = ["handle", "_gc"]
	def __init__(self, alsa, name, idx=0):
		self.handle = asound.find_selem(alsa.handle, struct.pack("<60sI", name.encode(), idx))
		self._gc = []

	@property
	def mB(self): # The ALSA functions are named dB, but they actually use millibel.
		return _alsa_array(self, asound.selem_get_playback_dB, asound.selem_set_playback_dB, asound.selem_set_playback_dB_all, c.c_long)

	@property
	def switch(self):
		return _alsa_array(self, asound.selem_get_playback_switch, asound.selem_set_playback_switch, asound.selem_set_playback_switch_all, c.c_bool)

	@property
	def mB_range(self):
		p1, p2 = c.c_long(), c.c_long()
		asound.selem_get_playback_dB_range(self.handle, p1, p2)
		return int(p1.value), int(p2.value)

	def __contains__(self, k):
		return asound.selem_has_playback_channel(self.handle, k)

	def callback(self, func):
		@functools.wraps(func)
		def func2(ptr, mask):
			print("foob")
			return func(mask) or 0
		func3 = asound.elem_callback(func2)
		self._gc.append(func3)
		asound.elem_set_callback(self.handle, func3)

class Alsa:
	__slots__ = ["handle"]
	def __init__(self, card, idx=0):
		self.handle = c.c_void_p()
		asound.open(self.handle, idx)
		asound.attach(self.handle, card.encode())
		asound.selem_register(self.handle, None, None)
		asound.load(self.handle)

	def selem(self, name, idx=0):
		return Selem(self, name, idx=0)

	def fds(self):
		nfds = asound.poll_descriptors_count(self.handle)
		fds = (asound.pollfd * nfds)()
		asound.poll_descriptors(self.handle, fds, nfds)
		return list(fds)

	def handle_events(self):
		asound.handle_events(self.handle)
