import i3bar
import i3bar.pulse as pa_ # TODO
from i3bar.pulse import pa
import subprocess
from collections import namedtuple

__all__ = ["Volume"]

def Pulse(name, callback, threaded=True): # Pretends to be a class, since C doesn't know what a class is
	def nogarb(func):
		nogarb.l.append(func)
		return func
	nogarb.l = []

	@nogarb
	@pa_.CONTEXT_SUCCESS_CB_T
	def context_success_cb(context, success, data):
		pass

	@nogarb
	@pa_.SERVER_INFO_CB_T
	def server_info_cb(context, server_info_p, data):
		sink = server_info_p.contents.default_sink_name
		pa.operation_unref(pa.context_get_sink_info_by_name(context, sink, sink_info_cb, None))

	@nogarb
	@pa_.CONTEXT_NOTIFY_CB_T
	def context_notify_cb(context, data):
		if pa.context_get_state(context) == pa_.CONTEXT_READY:
			pa.operation_unref(pa.context_get_server_info(context, server_info_cb, None))
			pa.context_set_subscribe_callback(context, context_subscribe_cb, None)
			mask = 0
			mask |= pa_.SUBSCRIPTION_MASK_SINK # Volume
			mask |= pa_.SUBSCRIPTION_MASK_SERVER # Change default card
			pa.operation_unref(pa.context_subscribe(context, mask, context_success_cb, None)) # TODO

	@nogarb
	@pa_.CONTEXT_SUBSCRIBE_CB_T
	def context_subscribe_cb(context, t, idx, data):
		event = t & pa_.SUBSCRIPTION_EVENT_FACILITY_MASK
		if event == pa_.SUBSCRIPTION_EVENT_SERVER:
			pa.operation_unref(pa.context_get_server_info(context, server_info_cb, None))
		if event == pa_.SUBSCRIPTION_EVENT_SINK:
			pa.operation_unref(pa.context_get_sink_info_by_name(context, sink, sink_info_cb, None))

	@nogarb
	@pa_.SINK_INFO_CB_T
	def sink_info_cb(context, sink_info_p, eol, data):
		if sink_info_p:
			callback.sinkInfo(sink_info_p.contents)

	sink = None

	if threaded:
		mainloop = pa.threaded_mainloop_new()
		mainloop_api = pa.threaded_mainloop_get_api(mainloop)
	else:
		mainloop = pa.mainloop_new()
		mainloop_api = pa.mainloop_get_api(mainloop)

	context = pa.context_new(mainloop_api, name)
	pa.context_set_state_callback(context, context_notify_cb, None)
	pa.context_connect(context, None, 0, None)

	def start():
		if threaded:
			pa.threaded_mainloop_start(mainloop)
		else:
			pa.mainloop_run(mainloop)

	def stop():
		if threaded:
			pa.threaded_mainloop_stop(mainloop)
		else:
			pa.mainloop_quit(mainloop, 0)

	return namedtuple("Pulse", "start stop nogarb")(start, stop, nogarb)

class Volume(i3bar.Segment):
	def start(self):
		self.pulse = Pulse("i3py", self)
		self.pulse.start()

	volume = 0
	mute = 0

	def sinkInfo(self, sink_info):
		self.volume = sink_info.volume.values[0]
		self.mute = sink_info.mute
		i3bar.update(self)

	def getOutput(self):
		text = "♪ {}%".format(round(100 * self.volume / 0x10000))
		color = "#7F7F7F" if self.mute else None
		return {"full_text": text, "color": color}

	def click(self, button, name):
		if button == 1:
			subprocess.Popen(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
		if button == 3:
			subprocess.Popen(["pavucontrol"])
		if button == 4:
			subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
		if button == 5:
			subprocess.Popen(['pactl', "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
