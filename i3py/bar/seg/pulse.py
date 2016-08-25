# Mostly stolen from pulsectl, but made to fit my needs better
from ctypes import *
p = POINTER

c_str_p = c_char_p

PA_VOLUME_NORM = 0x10000
PA_VOLUME_MAX = 2**32-1 // 2
PA_VOLUME_INVALID = 2**32-1

# pa_sw_volume_from_dB = lambda db:\
# 	min(PA_VOLUME_MAX, int(round(((10.0 ** (db / 20.0)) ** 3) * PA_VOLUME_NORM)))
PA_VOLUME_UI_MAX = 2927386 # pa_sw_volume_from_dB(+11.0)

PA_CHANNELS_MAX = 32
PA_USEC_T = c_uint64

PA_CONTEXT_NOAUTOSPAWN = 0x0001
PA_CONTEXT_NOFAIL = 0x0002

PA_CONTEXT_UNCONNECTED = 0
PA_CONTEXT_CONNECTING = 1
PA_CONTEXT_AUTHORIZING = 2
PA_CONTEXT_SETTING_NAME = 3
PA_CONTEXT_READY = 4
PA_CONTEXT_FAILED = 5
PA_CONTEXT_TERMINATED = 6

PA_SUBSCRIPTION_MASK_NULL = 0x0000
PA_SUBSCRIPTION_MASK_SINK = 0x0001
PA_SUBSCRIPTION_MASK_SOURCE = 0x0002
PA_SUBSCRIPTION_MASK_SINK_INPUT = 0x0004
PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT = 0x0008
PA_SUBSCRIPTION_MASK_MODULE = 0x0010
PA_SUBSCRIPTION_MASK_CLIENT = 0x0020
PA_SUBSCRIPTION_MASK_SAMPLE_CACHE = 0x0040
PA_SUBSCRIPTION_MASK_SERVER = 0x0080
PA_SUBSCRIPTION_MASK_AUTOLOAD = 0x0100
PA_SUBSCRIPTION_MASK_CARD = 0x0200
PA_SUBSCRIPTION_MASK_ALL = 0x02ff

PA_SUBSCRIPTION_EVENT_SINK = 0x0000
PA_SUBSCRIPTION_EVENT_SOURCE = 0x0001
PA_SUBSCRIPTION_EVENT_SINK_INPUT = 0x0002
PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT = 0x0003
PA_SUBSCRIPTION_EVENT_MODULE = 0x0004
PA_SUBSCRIPTION_EVENT_CLIENT = 0x0005
PA_SUBSCRIPTION_EVENT_SAMPLE_CACHE = 0x0006
PA_SUBSCRIPTION_EVENT_SERVER = 0x0007
PA_SUBSCRIPTION_EVENT_AUTOLOAD = 0x0008
PA_SUBSCRIPTION_EVENT_CARD = 0x0009
PA_SUBSCRIPTION_EVENT_FACILITY_MASK = 0x000F
PA_SUBSCRIPTION_EVENT_NEW = 0x0000
PA_SUBSCRIPTION_EVENT_CHANGE = 0x0010
PA_SUBSCRIPTION_EVENT_REMOVE = 0x0020
PA_SUBSCRIPTION_EVENT_TYPE_MASK = 0x0030

class PA_CONTEXT(Structure): pass
class PA_IO_EVENT(Structure): pass
class PA_MAINLOOP(Structure): pass
class PA_MAINLOOP_API(Structure): pass
class PA_OPERATION(Structure): pass
class PA_PROPLIST(Structure): pass
class PA_SIGNAL_EVENT(Structure): pass
class PA_STREAM(Structure): pass
class PA_THREADED_MAINLOOP(Structure): pass

class PA_SAMPLE_SPEC(Structure): _fields_ = [
	('format', c_int),
	('rate', c_uint32),
	('channels', c_uint32)
]

class PA_CHANNEL_MAP(Structure): _fields_ = [
	('channels', c_uint8),
	('map', c_int * PA_CHANNELS_MAX)
]

class PA_CVOLUME(Structure): _fields_ = [
	('channels', c_uint8),
	('values', c_uint32 * PA_CHANNELS_MAX)
]

class PA_PORT_INFO(Structure): _fields_ = [
	('name', c_char_p),
	('description', c_char_p),
	('priority', c_uint32),
]

class PA_SINK_INPUT_INFO(Structure): _fields_ = [
	('index', c_uint32),
	('name', c_char_p),
	('owner_module', c_uint32),
	('client', c_uint32),
	('sink', c_uint32),
	('sample_spec', PA_SAMPLE_SPEC),
	('channel_map', PA_CHANNEL_MAP),
	('volume', PA_CVOLUME),
	('buffer_usec', PA_USEC_T),
	('sink_usec', PA_USEC_T),
	('resample_method', c_char_p),
	('driver', c_char_p),
	('mute', c_int),
	('proplist', p(PA_PROPLIST)),
	('corked', c_int),
	('has_volume', c_int),
	('volume_writable', c_int),
]

class PA_SINK_INFO(Structure): _fields_ = [
	('name', c_char_p),
	('index', c_uint32),
	('description', c_char_p),
	('sample_spec', PA_SAMPLE_SPEC),
	('channel_map', PA_CHANNEL_MAP),
	('owner_module', c_uint32),
	('volume', PA_CVOLUME),
	('mute', c_int),
	('monitor_source', c_uint32),
	('monitor_source_name', c_char_p),
	('latency', PA_USEC_T),
	('driver', c_char_p),
	('flags', c_int),
	('proplist', p(PA_PROPLIST)),
	('configured_latency', PA_USEC_T),
	('base_volume', c_int),
	('state', c_int),
	('n_volume_steps', c_int),
	('card', c_uint32),
	('n_ports', c_uint32),
	('ports', p(p(PA_PORT_INFO))),
	('active_port', p(PA_PORT_INFO)),
]

class PA_SOURCE_OUTPUT_INFO(Structure): _fields_ = [
	('index', c_uint32),
	('name', c_char_p),
	('owner_module', c_uint32),
	('client', c_uint32),
	('source', c_uint32),
	('sample_spec', PA_SAMPLE_SPEC),
	('channel_map', PA_CHANNEL_MAP),
	('buffer_usec', PA_USEC_T),
	('source_usec', PA_USEC_T),
	('resample_method', c_char_p),
	('driver', c_char_p),
	('proplist', p(PA_PROPLIST)),
	('corked', c_int),
	('volume', PA_CVOLUME),
	('mute', c_int),
	('has_volume', c_int),
	('volume_writable', c_int),
]

class PA_SOURCE_INFO(Structure): _fields_ = [
	('name', c_char_p),
	('index', c_uint32),
	('description', c_char_p),
	('sample_spec', PA_SAMPLE_SPEC),
	('channel_map', PA_CHANNEL_MAP),
	('owner_module', c_uint32),
	('volume', PA_CVOLUME),
	('mute', c_int),
	('monitor_of_sink', c_uint32),
	('monitor_of_sink_name', c_char_p),
	('latency', PA_USEC_T),
	('driver', c_char_p),
	('flags', c_int),
	('proplist', p(PA_PROPLIST)),
	('configured_latency', PA_USEC_T),
	('base_volume', c_int),
	('state', c_int),
	('n_volume_steps', c_int),
	('card', c_uint32),
	('n_ports', c_uint32),
	('ports', p(p(PA_PORT_INFO))),
	('active_port', p(PA_PORT_INFO)),
]

class PA_CLIENT_INFO(Structure): _fields_ = [
	('index', c_uint32),
	('name', c_char_p),
	('owner_module', c_uint32),
	('driver', c_char_p),
]

class PA_CARD_PROFILE_INFO(Structure): _fields_ = [
	('name', c_char_p),
	('description', c_char_p),
	('n_sinks', c_uint32),
	('n_sources', c_uint32),
	('priority', c_uint32),
]

class PA_CARD_INFO(Structure): _fields_ = [
	('index', c_uint32),
	('name', c_char_p),
	('owner_module', c_uint32),
	('driver', c_char_p),
	('n_profiles', c_uint32),
	('profiles', p(PA_CARD_PROFILE_INFO)),
	('active_profile', p(PA_CARD_PROFILE_INFO)),
	('proplist', p(PA_PROPLIST)),
]

class POLLFD(Structure): _fields_ = [
	('fd', c_int),
	('events', c_short),
	('revents', c_short),
]

class PA_SERVER_INFO(Structure): _fields_ = [
	('user_name', c_char_p),
	('host_name', c_char_p),
	('server_version', c_char_p),
	('server_name', c_char_p),
	('sample_spec', PA_SAMPLE_SPEC),
	('default_sink_name', c_char_p),
	('default_source_name', c_char_p),
	('cookie', c_uint32),
	('channel_map', PA_CHANNEL_MAP),
]

PA_POLL_FUNC_T             = CFUNCTYPE(c_void_p, p(POLLFD), c_ulong, c_int, c_void_p)
PA_SIGNAL_CB_T             = CFUNCTYPE(c_void_p, p(PA_MAINLOOP_API), p(c_int), c_int, c_void_p)
PA_CONTEXT_NOTIFY_CB_T     = CFUNCTYPE(c_void_p, p(PA_CONTEXT), c_void_p)
PA_CLIENT_INFO_CB_T        = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_CLIENT_INFO), c_int, c_void_p)
PA_SINK_INPUT_INFO_CB_T    = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_SINK_INPUT_INFO), c_int, c_void_p)
PA_SINK_INFO_CB_T          = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_SINK_INFO), c_int, c_void_p)
PA_SOURCE_OUTPUT_INFO_CB_T = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_SOURCE_OUTPUT_INFO), c_int, c_void_p)
PA_SOURCE_INFO_CB_T        = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_SOURCE_INFO), c_int, c_void_p)
PA_CONTEXT_DRAIN_CB_T      = CFUNCTYPE(c_void_p, p(PA_CONTEXT), c_void_p)
PA_CONTEXT_SUCCESS_CB_T    = CFUNCTYPE(c_void_p, p(PA_CONTEXT), c_int, c_void_p)
PA_CARD_INFO_CB_T          = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_CARD_INFO), c_int, c_void_p) #restype was None for whatever reason
PA_CONTEXT_SUBSCRIBE_CB_T  = CFUNCTYPE(c_void_p, p(PA_CONTEXT), c_int, c_int, c_void_p)
PA_SERVER_INFO_CB_T        = CFUNCTYPE(c_void_p, p(PA_CONTEXT), p(PA_SERVER_INFO), c_void_p)



class LibPulse:
	func_defs = {
		"context_connect":                      ( 'pa_gt', [p(PA_CONTEXT), c_str_p, c_int, p(c_int)] ),
		"context_disconnect":                   ( None,    [p(PA_CONTEXT)] ),
		"context_drain":                        ( 'pa_op', [p(PA_CONTEXT), PA_CONTEXT_DRAIN_CB_T, c_void_p] ),
		"context_errno":                        ( c_int,   [p(PA_CONTEXT)] ),
		"context_get_card_info_by_index":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_CARD_INFO_CB_T, c_void_p] ),
		"context_get_card_info_list":           ( 'pa_op', [p(PA_CONTEXT), PA_CARD_INFO_CB_T, c_void_p] ),
		"context_get_client_info":              ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_CLIENT_INFO_CB_T, c_void_p] ),
		"context_get_client_info_list":         ( 'pa_op', [p(PA_CONTEXT), PA_CLIENT_INFO_CB_T, c_void_p] ),
		"context_get_server_info":              ( 'pa_op', [p(PA_CONTEXT), PA_SERVER_INFO_CB_T, c_void_p] ),
		"context_get_sink_info_by_index":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_SINK_INFO_CB_T, c_void_p] ),
		"context_get_sink_info_by_name":        ( 'pa_op', [p(PA_CONTEXT), c_str_p, PA_SINK_INFO_CB_T, c_void_p] ),
		"context_get_sink_info_list":           ( 'pa_op', [p(PA_CONTEXT), PA_SINK_INFO_CB_T, c_void_p] ),
		"context_get_sink_input_info":          ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_SINK_INPUT_INFO_CB_T, c_void_p] ),
		"context_get_sink_input_info_list":     ( 'pa_op', [p(PA_CONTEXT), PA_SINK_INPUT_INFO_CB_T, c_void_p] ),
		"context_get_source_info_by_index":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_SOURCE_INFO_CB_T, c_void_p] ),
		"context_get_source_info_list":         ( 'pa_op', [p(PA_CONTEXT), PA_SOURCE_INFO_CB_T, c_void_p] ),
		"context_get_source_output_info":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_SOURCE_OUTPUT_INFO_CB_T, c_void_p] ),
		"context_get_source_output_info_list":  ( 'pa_op', [p(PA_CONTEXT), PA_SOURCE_OUTPUT_INFO_CB_T, c_void_p] ),
		"context_get_state":                    ( c_int,   [p(PA_CONTEXT)] ),
		"context_kill_source_output":           ( 'pa_op', [p(PA_CONTEXT), c_uint32, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_move_sink_input_by_index":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_uint32, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_move_source_output_by_index":  ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_uint32, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_new":                          ( p(PA_CONTEXT), [p(PA_MAINLOOP_API), c_str_p] ),
		"context_set_card_profile_by_index":    ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_str_p, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_input_mute":          ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_input_volume":        ( 'pa_op', [p(PA_CONTEXT), c_uint32, p(PA_CVOLUME), PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_mute_by_index":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_mute_by_name":        ( 'pa_op', [p(PA_CONTEXT), c_str_p, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_port_by_index":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_str_p, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_volume_by_index":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, p(PA_CVOLUME), PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_sink_volume_by_name":      ( 'pa_op', [p(PA_CONTEXT), c_str_p, p(PA_CVOLUME), PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_source_mute_by_index":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_source_output_mute":       ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_source_output_volume":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, p(PA_CVOLUME), PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_source_port_by_index":     ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_str_p, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_source_volume_by_index":   ( 'pa_op', [p(PA_CONTEXT), c_uint32, p(PA_CVOLUME), PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_set_state_callback":           ( None,    [p(PA_CONTEXT), PA_CONTEXT_NOTIFY_CB_T, c_void_p] ),
		"context_set_subscribe_callback":       ( None,    [p(PA_CONTEXT), PA_CONTEXT_SUBSCRIBE_CB_T, c_void_p] ),
		"context_subscribe":                    ( 'pa_op', [p(PA_CONTEXT), c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_suspend_sink_by_index":        ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),
		"context_suspend_source_by_index":      ( 'pa_op', [p(PA_CONTEXT), c_uint32, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p] ),

		"mainloop_dispatch":                    ( 'pa_gt', [p(PA_MAINLOOP)] ),
		"mainloop_free":                        ( None,    [p(PA_MAINLOOP)] ),
		"mainloop_get_api":                     ( p(PA_MAINLOOP_API), [p(PA_MAINLOOP)] ),
		"mainloop_iterate":                     ( 'pa_gt', [p(PA_MAINLOOP), c_int, p(c_int)] ),
		"mainloop_new":                         ( p(PA_MAINLOOP), [] ),
		"mainloop_poll":                        ( 'pa_gt', [p(PA_MAINLOOP)] ),
		"mainloop_prepare":                     ( 'pa_gt', [p(PA_MAINLOOP), c_int] ),
		"mainloop_quit":                        ( None,    [p(PA_MAINLOOP), c_int] ),
		"mainloop_run":                         ( c_int,   [p(PA_MAINLOOP), p(c_int)] ),
		"mainloop_set_poll_func":               ( None,    [p(PA_MAINLOOP), PA_POLL_FUNC_T, c_void_p] ),
		"mainloop_wakeup":                      ( None,    [p(PA_MAINLOOP)] ),

		"threaded_mainloop_accept":             ( None,    [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_free":               ( None,    [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_get_api":            ( p(PA_MAINLOOP_API), [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_get_retval":         ( c_int,   [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_in_thread":          ( c_int,   [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_lock":               ( None,    [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_new":                ( p(PA_THREADED_MAINLOOP), [] ),
		"threaded_mainloop_signal":             ( None,    [p(PA_THREADED_MAINLOOP), c_int] ),
		"threaded_mainloop_start":              ( c_int,   [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_stop":               ( None,    [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_unlock":             ( None,    [p(PA_THREADED_MAINLOOP)] ),
		"threaded_mainloop_wait":               ( None,    [p(PA_THREADED_MAINLOOP)] ),

		"channel_map_snprint":                  ( c_str_p, [c_str_p, c_int, p(PA_CHANNEL_MAP)] ),
		"operation_unref":                      ( c_int,   [p(PA_OPERATION)] ),
		"proplist_gets":                        ( c_str_p, [p(PA_PROPLIST), c_str_p] ),
		"proplist_iterate":                     ( c_str_p, [p(PA_PROPLIST), p(c_void_p)] ),
		"signal_done":                          ( None,    [] ),
		"signal_init":                          ( 'pa_gt', [p(PA_MAINLOOP_API)] ),
		"signal_new":                           ( None,    [c_int, PA_SIGNAL_CB_T, p(PA_SIGNAL_EVENT)] ),
		"strerror":                             ( c_str_p, [c_int] ),
	}

	class CallError(Exception): pass

	def __init__(self):
		dll = CDLL("libpulse.so.0")

		self.funcs = dict()
		for name, sig in self.func_defs.items():
			self.funcs[name] = self._func_wrapper(name, getattr(dll, "pa_" + name), sig[0], sig[1])

	def _func_wrapper(self, name, func, ret_type, args):
		func.args = args
		if isinstance(ret_type, str):
			if ret_type == 'pa_gt': func.restype = c_int
			elif ret_type == 'pa_op': func.restype = p(PA_OPERATION)
			else: raise ValueError(ret_type)
		else:
			func.restype = ret_type

		def _wrapper(*args):
			res = func(*args)
			if isinstance(ret_type, str):
				if (ret_type == 'pa_gt' and res < 0) or (ret_type == 'pa_op' and not res):
					err = [name]
					if args and hasattr(args[0], "contents") and isinstance(args[0].contents, PA_CONTEXT):
						err.append(self.strerror(self.context_errno(args[0])))
					else:
						err.append("Return value check failed: {} ({})".format(ret_type, res))
					raise self.CallError(*err)
			return res

		_wrapper.__name__ = name
		return _wrapper

	def __getattr__(self, k):
		return self.funcs[k]

	def return_value(self):
		return pointer(c_int())

pa = LibPulse()
