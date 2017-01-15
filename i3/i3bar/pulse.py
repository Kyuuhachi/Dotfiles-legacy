# flake8: noqa E701
# Mostly stolen from pulsectl, but made to fit my needs better
import ctypes as c
p = c.POINTER

VOLUME_NORM = 0x10000
VOLUME_MAX = (2**32 - 1) // 2
VOLUME_INVALID = 2**32 - 1

VOLUME_UI_MAX = 2927386

CHANNELS_MAX = 32
USEC_T = c.c_uint64

CONTEXT_NOAUTOSPAWN = 0x0001
CONTEXT_NOFAIL = 0x0002

CONTEXT_UNCONNECTED = 0
CONTEXT_CONNECTING = 1
CONTEXT_AUTHORIZING = 2
CONTEXT_SETTING_NAME = 3
CONTEXT_READY = 4
CONTEXT_FAILED = 5
CONTEXT_TERMINATED = 6

SUBSCRIPTION_MASK_NULL = 0x0000
SUBSCRIPTION_MASK_SINK = 0x0001
SUBSCRIPTION_MASK_SOURCE = 0x0002
SUBSCRIPTION_MASK_SINK_INPUT = 0x0004
SUBSCRIPTION_MASK_SOURCE_OUTPUT = 0x0008
SUBSCRIPTION_MASK_MODULE = 0x0010
SUBSCRIPTION_MASK_CLIENT = 0x0020
SUBSCRIPTION_MASK_SAMPLE_CACHE = 0x0040
SUBSCRIPTION_MASK_SERVER = 0x0080
SUBSCRIPTION_MASK_AUTOLOAD = 0x0100
SUBSCRIPTION_MASK_CARD = 0x0200
SUBSCRIPTION_MASK_ALL = 0x02ff

SUBSCRIPTION_EVENT_SINK = 0x0000
SUBSCRIPTION_EVENT_SOURCE = 0x0001
SUBSCRIPTION_EVENT_SINK_INPUT = 0x0002
SUBSCRIPTION_EVENT_SOURCE_OUTPUT = 0x0003
SUBSCRIPTION_EVENT_MODULE = 0x0004
SUBSCRIPTION_EVENT_CLIENT = 0x0005
SUBSCRIPTION_EVENT_SAMPLE_CACHE = 0x0006
SUBSCRIPTION_EVENT_SERVER = 0x0007
SUBSCRIPTION_EVENT_AUTOLOAD = 0x0008
SUBSCRIPTION_EVENT_CARD = 0x0009
SUBSCRIPTION_EVENT_FACILITY_MASK = 0x000F
SUBSCRIPTION_EVENT_NEW = 0x0000
SUBSCRIPTION_EVENT_CHANGE = 0x0010
SUBSCRIPTION_EVENT_REMOVE = 0x0020
SUBSCRIPTION_EVENT_TYPE_MASK = 0x0030

class CONTEXT(c.Structure): pass
class IO_EVENT(c.Structure): pass
class MAINLOOP(c.Structure): pass
class MAINLOOP_API(c.Structure): pass
class OPERATION(c.Structure): pass
class PROPLIST(c.Structure): pass
class SIGNAL_EVENT(c.Structure): pass
class STREAM(c.Structure): pass
class THREADED_MAINLOOP(c.Structure): pass

class SAMPLE_SPEC(c.Structure): _fields_ = [
	('format', c.c_int),
	('rate', c.c_uint32),
	('channels', c.c_uint32)
]

class CHANNEL_MAP(c.Structure): _fields_ = [
	('channels', c.c_uint8),
	('map', c.c_int * CHANNELS_MAX)
]

class CVOLUME(c.Structure): _fields_ = [
	('channels', c.c_uint8),
	('values', c.c_uint32 * CHANNELS_MAX)
]

class PORT_INFO(c.Structure): _fields_ = [
	('name', c.c_char_p),
	('description', c.c_char_p),
	('priority', c.c_uint32),
]

class SINK_INPUT_INFO(c.Structure): _fields_ = [
	('index', c.c_uint32),
	('name', c.c_char_p),
	('owner_module', c.c_uint32),
	('client', c.c_uint32),
	('sink', c.c_uint32),
	('sample_spec', SAMPLE_SPEC),
	('channel_map', CHANNEL_MAP),
	('volume', CVOLUME),
	('buffer_usec', USEC_T),
	('sink_usec', USEC_T),
	('resample_method', c.c_char_p),
	('driver', c.c_char_p),
	('mute', c.c_int),
	('proplist', p(PROPLIST)),
	('corked', c.c_int),
	('has_volume', c.c_int),
	('volume_writable', c.c_int),
]

class SINK_INFO(c.Structure): _fields_ = [
	('name', c.c_char_p),
	('index', c.c_uint32),
	('description', c.c_char_p),
	('sample_spec', SAMPLE_SPEC),
	('channel_map', CHANNEL_MAP),
	('owner_module', c.c_uint32),
	('volume', CVOLUME),
	('mute', c.c_int),
	('monitor_source', c.c_uint32),
	('monitor_source_name', c.c_char_p),
	('latency', USEC_T),
	('driver', c.c_char_p),
	('flags', c.c_int),
	('proplist', p(PROPLIST)),
	('configured_latency', USEC_T),
	('base_volume', c.c_int),
	('state', c.c_int),
	('n_volume_steps', c.c_int),
	('card', c.c_uint32),
	('n_ports', c.c_uint32),
	('ports', p(p(PORT_INFO))),
	('active_port', p(PORT_INFO)),
]

class SOURCE_OUTPUT_INFO(c.Structure): _fields_ = [
	('index', c.c_uint32),
	('name', c.c_char_p),
	('owner_module', c.c_uint32),
	('client', c.c_uint32),
	('source', c.c_uint32),
	('sample_spec', SAMPLE_SPEC),
	('channel_map', CHANNEL_MAP),
	('buffer_usec', USEC_T),
	('source_usec', USEC_T),
	('resample_method', c.c_char_p),
	('driver', c.c_char_p),
	('proplist', p(PROPLIST)),
	('corked', c.c_int),
	('volume', CVOLUME),
	('mute', c.c_int),
	('has_volume', c.c_int),
	('volume_writable', c.c_int),
]

class SOURCE_INFO(c.Structure): _fields_ = [
	('name', c.c_char_p),
	('index', c.c_uint32),
	('description', c.c_char_p),
	('sample_spec', SAMPLE_SPEC),
	('channel_map', CHANNEL_MAP),
	('owner_module', c.c_uint32),
	('volume', CVOLUME),
	('mute', c.c_int),
	('monitor_of_sink', c.c_uint32),
	('monitor_of_sink_name', c.c_char_p),
	('latency', USEC_T),
	('driver', c.c_char_p),
	('flags', c.c_int),
	('proplist', p(PROPLIST)),
	('configured_latency', USEC_T),
	('base_volume', c.c_int),
	('state', c.c_int),
	('n_volume_steps', c.c_int),
	('card', c.c_uint32),
	('n_ports', c.c_uint32),
	('ports', p(p(PORT_INFO))),
	('active_port', p(PORT_INFO)),
]

class CLIENT_INFO(c.Structure): _fields_ = [
	('index', c.c_uint32),
	('name', c.c_char_p),
	('owner_module', c.c_uint32),
	('driver', c.c_char_p),
]

class CARD_PROFILE_INFO(c.Structure): _fields_ = [
	('name', c.c_char_p),
	('description', c.c_char_p),
	('n_sinks', c.c_uint32),
	('n_sources', c.c_uint32),
	('priority', c.c_uint32),
]

class CARD_INFO(c.Structure): _fields_ = [
	('index', c.c_uint32),
	('name', c.c_char_p),
	('owner_module', c.c_uint32),
	('driver', c.c_char_p),
	('n_profiles', c.c_uint32),
	('profiles', p(CARD_PROFILE_INFO)),
	('active_profile', p(CARD_PROFILE_INFO)),
	('proplist', p(PROPLIST)),
]

class POLLFD(c.Structure): _fields_ = [
	('fd', c.c_int),
	('events', c.c_short),
	('revents', c.c_short),
]

class SERVER_INFO(c.Structure): _fields_ = [
	('user_name', c.c_char_p),
	('host_name', c.c_char_p),
	('server_version', c.c_char_p),
	('server_name', c.c_char_p),
	('sample_spec', SAMPLE_SPEC),
	('default_sink_name', c.c_char_p),
	('default_source_name', c.c_char_p),
	('cookie', c.c_uint32),
	('channel_map', CHANNEL_MAP),
]

POLL_FUNC_T             = c.CFUNCTYPE(c.c_void_p, p(POLLFD), c.c_ulong, c.c_int, c.c_void_p)
SIGNAL_CB_T             = c.CFUNCTYPE(c.c_void_p, p(MAINLOOP_API), p(c.c_int), c.c_int, c.c_void_p)
CONTEXT_NOTIFY_CB_T     = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), c.c_void_p)
CLIENT_INFO_CB_T        = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(CLIENT_INFO), c.c_int, c.c_void_p)
SINK_INPUT_INFO_CB_T    = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(SINK_INPUT_INFO), c.c_int, c.c_void_p)
SINK_INFO_CB_T          = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(SINK_INFO), c.c_int, c.c_void_p)
SOURCE_OUTPUT_INFO_CB_T = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(SOURCE_OUTPUT_INFO), c.c_int, c.c_void_p)
SOURCE_INFO_CB_T        = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(SOURCE_INFO), c.c_int, c.c_void_p)
CONTEXT_DRAIN_CB_T      = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), c.c_void_p)
CONTEXT_SUCCESS_CB_T    = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), c.c_int, c.c_void_p)
CARD_INFO_CB_T          = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(CARD_INFO), c.c_int, c.c_void_p)
CONTEXT_SUBSCRIBE_CB_T  = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), c.c_int, c.c_int, c.c_void_p)
SERVER_INFO_CB_T        = c.CFUNCTYPE(c.c_void_p, p(CONTEXT), p(SERVER_INFO), c.c_void_p)

class LibPulse:
	func_defs = {
		"context_connect":                      ('pa_gt',   [p(CONTEXT), c.c_char_p, c.c_int, p(c.c_int)]),
		"context_disconnect":                   (None,      [p(CONTEXT)]),
		"context_drain":                        ('pa_op',   [p(CONTEXT), CONTEXT_DRAIN_CB_T, c.c_void_p]),
		"context_errno":                        (c.c_int,   [p(CONTEXT)]),
		"context_get_card_info_by_index":       ('pa_op',   [p(CONTEXT), c.c_uint32, CARD_INFO_CB_T, c.c_void_p]),
		"context_get_card_info_list":           ('pa_op',   [p(CONTEXT), CARD_INFO_CB_T, c.c_void_p]),
		"context_get_client_info":              ('pa_op',   [p(CONTEXT), c.c_uint32, CLIENT_INFO_CB_T, c.c_void_p]),
		"context_get_client_info_list":         ('pa_op',   [p(CONTEXT), CLIENT_INFO_CB_T, c.c_void_p]),
		"context_get_server_info":              ('pa_op',   [p(CONTEXT), SERVER_INFO_CB_T, c.c_void_p]),
		"context_get_sink_info_by_index":       ('pa_op',   [p(CONTEXT), c.c_uint32, SINK_INFO_CB_T, c.c_void_p]),
		"context_get_sink_info_by_name":        ('pa_op',   [p(CONTEXT), c.c_char_p, SINK_INFO_CB_T, c.c_void_p]),
		"context_get_sink_info_list":           ('pa_op',   [p(CONTEXT), SINK_INFO_CB_T, c.c_void_p]),
		"context_get_sink_input_info":          ('pa_op',   [p(CONTEXT), c.c_uint32, SINK_INPUT_INFO_CB_T, c.c_void_p]),
		"context_get_sink_input_info_list":     ('pa_op',   [p(CONTEXT), SINK_INPUT_INFO_CB_T, c.c_void_p]),
		"context_get_source_info_by_index":     ('pa_op',   [p(CONTEXT), c.c_uint32, SOURCE_INFO_CB_T, c.c_void_p]),
		"context_get_source_info_list":         ('pa_op',   [p(CONTEXT), SOURCE_INFO_CB_T, c.c_void_p]),
		"context_get_source_output_info":       ('pa_op',   [p(CONTEXT), c.c_uint32, SOURCE_OUTPUT_INFO_CB_T, c.c_void_p]),
		"context_get_source_output_info_list":  ('pa_op',   [p(CONTEXT), SOURCE_OUTPUT_INFO_CB_T, c.c_void_p]),
		"context_get_state":                    (c.c_int,   [p(CONTEXT)]),
		"context_kill_source_output":           ('pa_op',   [p(CONTEXT), c.c_uint32, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_move_sink_input_by_index":     ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_uint32, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_move_source_output_by_index":  ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_uint32, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_new":                          (p(CONTEXT), [p(MAINLOOP_API), c.c_char_p]),
		"context_set_card_profile_by_index":    ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_char_p, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_input_mute":          ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_input_volume":        ('pa_op',   [p(CONTEXT), c.c_uint32, p(CVOLUME), CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_mute_by_index":       ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_mute_by_name":        ('pa_op',   [p(CONTEXT), c.c_char_p, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_port_by_index":       ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_char_p, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_volume_by_index":     ('pa_op',   [p(CONTEXT), c.c_uint32, p(CVOLUME), CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_sink_volume_by_name":      ('pa_op',   [p(CONTEXT), c.c_char_p, p(CVOLUME), CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_source_mute_by_index":     ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_source_output_mute":       ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_source_output_volume":     ('pa_op',   [p(CONTEXT), c.c_uint32, p(CVOLUME), CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_source_port_by_index":     ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_char_p, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_source_volume_by_index":   ('pa_op',   [p(CONTEXT), c.c_uint32, p(CVOLUME), CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_set_state_callback":           (None,      [p(CONTEXT), CONTEXT_NOTIFY_CB_T, c.c_void_p]),
		"context_set_subscribe_callback":       (None,      [p(CONTEXT), CONTEXT_SUBSCRIBE_CB_T, c.c_void_p]),
		"context_subscribe":                    ('pa_op',   [p(CONTEXT), c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_suspend_sink_by_index":        ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),
		"context_suspend_source_by_index":      ('pa_op',   [p(CONTEXT), c.c_uint32, c.c_int, CONTEXT_SUCCESS_CB_T, c.c_void_p]),

		"mainloop_dispatch":                    ('pa_gt',   [p(MAINLOOP)]),
		"mainloop_free":                        (None,      [p(MAINLOOP)]),
		"mainloop_get_api":                     (p(MAINLOOP_API), [p(MAINLOOP)]),
		"mainloop_iterate":                     ('pa_gt',   [p(MAINLOOP), c.c_int, p(c.c_int)]),
		"mainloop_new":                         (p(MAINLOOP), []),
		"mainloop_poll":                        ('pa_gt',   [p(MAINLOOP)]),
		"mainloop_prepare":                     ('pa_gt',   [p(MAINLOOP), c.c_int]),
		"mainloop_quit":                        (None,      [p(MAINLOOP), c.c_int]),
		"mainloop_run":                         (c.c_int,   [p(MAINLOOP), p(c.c_int)]),
		"mainloop_set_poll_func":               (None,      [p(MAINLOOP), POLL_FUNC_T, c.c_void_p]),
		"mainloop_wakeup":                      (None,      [p(MAINLOOP)]),

		"threaded_mainloop_accept":             (None,      [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_free":               (None,      [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_get_api":            (p(MAINLOOP_API), [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_get_retval":         (c.c_int,   [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_in_thread":          (c.c_int,   [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_lock":               (None,      [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_new":                (p(THREADED_MAINLOOP), []),
		"threaded_mainloop_signal":             (None,       [p(THREADED_MAINLOOP), c.c_int]),
		"threaded_mainloop_start":              (c.c_int,    [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_stop":               (None,       [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_unlock":             (None,       [p(THREADED_MAINLOOP)]),
		"threaded_mainloop_wait":               (None,       [p(THREADED_MAINLOOP)]),

		"channel_map_snprint":                  (c.c_char_p, [c.c_char_p, c.c_int, p(CHANNEL_MAP)]),
		"operation_unref":                      (c.c_int,    [p(OPERATION)]),
		"proplist_gets":                        (c.c_char_p, [p(PROPLIST), c.c_char_p]),
		"proplist_iterate":                     (c.c_char_p, [p(PROPLIST), p(c.c_void_p)]),
		"signal_done":                          (None,       []),
		"signal_init":                          ('pa_gt',    [p(MAINLOOP_API)]),
		"signal_new":                           (None,       [c.c_int, SIGNAL_CB_T, p(SIGNAL_EVENT)]),
		"strerror":                             (c.c_char_p, [c.c_int]),
	}

	class CallError(Exception): pass

	def __init__(self):
		def _func_wrapper(name, func, ret_type, args):
			func.args = args
			if isinstance(ret_type, str):
				if ret_type == 'pa_gt':
					func.restype = c.c_int
				elif ret_type == 'pa_op':
					func.restype = p(OPERATION)
				else:
					raise ValueError(ret_type)
			else:
				func.restype = ret_type

			def _wrapper(*args):
				res = func(*args)
				if isinstance(ret_type, str):
					if (ret_type == 'pa_gt' and res < 0) or (ret_type == 'pa_op' and not res):
						err = [name]
						if args and hasattr(args[0], "contents") and isinstance(args[0].contents, CONTEXT):
							err.append(self.strerror(self.context_errno(args[0])))
						else:
							err.append("Return value check failed: {} ({})".format(ret_type, res))
						raise self.CallError(*err)
				return res

			_wrapper.__name__ = name
			return _wrapper
		dll = c.CDLL("libpulse.so.0")

		self.funcs = dict()
		for name, sig in self.func_defs.items():
			self.funcs[name] = _func_wrapper(name, getattr(dll, "pa_" + name), sig[0], sig[1])

	def __getattr__(self, k):
		return self.funcs[k]

pa = LibPulse()
