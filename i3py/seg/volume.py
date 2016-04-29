import os
from i3pystatus.pulseaudio.pulse import *
from .pulse import *
import subprocess
import i3py

class Volume(i3py.Segment): #TODO clean plz
	sink = None
	volume = PA_CVOLUME()
	mute = False

	def __init__(self):
		self._context_notify_cb = PA_CONTEXT_NOTIFY_CB_T(self.context_notify_cb)
		self._sink_info_cb = PA_SINK_INFO_CB_T(self.sink_info_cb)
		self._context_subscribe_cb = PA_CONTEXT_SUBSCRIBE_CB_T(self.context_subscribe_cb)
		self._context_success_cb = PA_CONTEXT_SUCCESS_CB_T(self.context_success_cb)
		self._server_info_cb = PA_SERVER_INFO_CB_T(self.server_info_cb)

		mainloop = pa.threaded_mainloop_new()
		mainloop_api = pa.threaded_mainloop_get_api(mainloop)
		self.context = pa.context_new(mainloop_api, b"i3py")
		pa.context_connect(self.context, None, 0, None)

		pa.context_set_state_callback(self.context, self._context_notify_cb, None)
		pa.threaded_mainloop_start(mainloop)

	def request_client_update(self):
		pa.operation_unref(pa.context_get_sink_info_by_name(self.context, self.sink, self._sink_info_cb, None))

	def request_server_update(self):
		pa.operation_unref(pa.context_get_server_info(self.context, self._server_info_cb, None))

	def context_success_cb(self, context, success, userdata):
		pass

	def server_info_cb(self, context, server_info_p, userdata):
		self.sink = server_info_p.contents.default_sink_name
		self.request_client_update()

	def context_notify_cb(self, context, _):
		state = pa.context_get_state(self.context)

		if state == PA_CONTEXT_READY:
			self.request_server_update()
			pa.context_set_subscribe_callback(self.context, self._context_subscribe_cb, None)
			pa.operation_unref(pa.context_subscribe(self.context, PA_SUBSCRIPTION_MASK_SINK, self._context_success_cb, None))

	def context_subscribe_cb(self, context, t, idx, userdata):
		if t & PA_SUBSCRIPTION_EVENT_FACILITY_MASK == PA_SUBSCRIPTION_EVENT_SERVER:
			self.request_server_update()

		self.request_client_update()

	def sink_info_cb(self, context, sink_info_p, _, __):
		if sink_info_p:
			sink_info = sink_info_p.contents
			self.volume = sink_info.volume
			self.mute = sink_info.mute
			i3py.update(self)
	
	def getOutput(self):
		text = "♪ %d%%" % round(100 * self.volume.values[0] / 0x10000)
		color = "#7F7F7F" if self.mute else None
		return (text, color)
	
	def click(self, button):
		if button == 1: subprocess.Popen(['pactl', 'set-sink-mute', self.sink, "toggle"])
		if button == 4: subprocess.Popen(['pactl', 'set-sink-volume', self.sink, "--", "+5%"])
		if button == 5: subprocess.Popen(['pactl', 'set-sink-volume', self.sink, "--", "-5%"])
