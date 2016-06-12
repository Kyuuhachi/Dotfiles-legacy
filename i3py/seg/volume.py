#!/usr/bin/env python3
import sys
import subprocess
from collections import namedtuple
if __name__ == "__main__":
	from pulse import *
else:
	from i3py.seg.pulse import *
	import i3py

def Pulse(name, callback, threaded=True): #Pretends to be a class, since C doesn't know what a class is
	def nogarb(func):
		nogarb.l.append(func)
		return func
	nogarb.l = []

	@nogarb
	@PA_CONTEXT_SUCCESS_CB_T
	def context_success_cb(context, success, data):
		pass

	@nogarb
	@PA_SERVER_INFO_CB_T
	def server_info_cb(context, server_info_p, data):
		sink = server_info_p.contents.default_sink_name
		callback.setSink(sink)
		pa.operation_unref(pa.context_get_sink_info_by_name(context, sink, sink_info_cb, None))

	@nogarb
	@PA_CONTEXT_NOTIFY_CB_T
	def context_notify_cb(context, data):
		if pa.context_get_state(context) == PA_CONTEXT_READY:
			pa.operation_unref(pa.context_get_server_info(context, server_info_cb, None))
			pa.context_set_subscribe_callback(context, context_subscribe_cb, None)
			mask = 0
			mask |= PA_SUBSCRIPTION_MASK_SINK #Volume
			mask |= PA_SUBSCRIPTION_MASK_SERVER #Change default card (i hope)
			pa.operation_unref(pa.context_subscribe(context, mask, context_success_cb, None)) #TODO

	@nogarb
	@PA_CONTEXT_SUBSCRIBE_CB_T
	def context_subscribe_cb(context, t, idx, data):
		event = t & PA_SUBSCRIPTION_EVENT_FACILITY_MASK
		if event == PA_SUBSCRIPTION_EVENT_SERVER:
			pa.operation_unref(pa.context_get_server_info(context, server_info_cb, None))
		if event == PA_SUBSCRIPTION_EVENT_SINK:
			pa.operation_unref(pa.context_get_sink_info_by_name(context, sink, sink_info_cb, None))

	@nogarb
	@PA_SINK_INFO_CB_T
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
			pa_threaded_mainloop_stop(mainloop)
		else:
			pa.mainloop_quit(mainloop, 0)

	return namedtuple("Pulse", "start stop nogarb")(start, stop, nogarb)

if __name__ == "__main__":
	class CLI:
		def __init__(self, op):
			self.op = op
			self.pulse = Pulse("i3py-cli", self, threaded=False)
			self.pulse.start()

		def setSink(self, sink):
			if self.op == "mute": subprocess.Popen(['pactl', 'set-sink-mute', sink, "toggle"])
			if self.op == "inc":  subprocess.Popen(['pactl', 'set-sink-volume', sink, "--", "+5%"])
			if self.op == "dec":  subprocess.Popen(['pactl', 'set-sink-volume', sink, "--", "-5%"])
			self.pulse.stop()
			exit(0) #For some reason, pa_mainloop_quit causes a segfault

		def sinkInfo(self, sink_info):
			pass

	if len(sys.argv) != 2:
		print("Bad command")
		exit(1)
	CLI(sys.argv[1])
else:
	class Volume(i3py.Segment):
		def start(self):
			self.pulse = Pulse("i3py", self)
			self.pulse.start()

		sink = None
		volume = 0
		mute = 0

		def setSink(self, sink):
			self.sink = sink

		def sinkInfo(self, sink_info):
			self.volume = sink_info.volume.values[0]
			self.mute = sink_info.mute
			i3py.update(self)

		def getOutput(self):
			text = "♪ {}%".format(round(100 * self.volume / 0x10000))
			color = "#7F7F7F" if self.mute else None
			return (text, color)

		def click(self, button):
			if button == 1: subprocess.Popen(['pactl', 'set-sink-mute', self.sink, "toggle"])
			if button == 3: subprocess.Popen(['pavucontrol'])
			if button == 4: subprocess.Popen(['pactl', 'set-sink-volume', self.sink, "--", "+5%"])
			if button == 5: subprocess.Popen(['pactl', 'set-sink-volume', self.sink, "--", "-5%"])
