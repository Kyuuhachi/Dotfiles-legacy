from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

local_d = display.Display()
rec_d = display.Display()

assert rec_d.has_extension("RECORD")
rec = rec_d.record_get_version(0, 0)

import pickle

with open("/home/yuki/keylog.bin", "ab") as f:
	def callback(reply):
		if reply.category != record.FromServer: return
		if reply.client_swapped: return
		if not reply.data: return
		assert len(reply.data) == 32
		window = local_d.get_input_focus().focus
		while window is not None:
			wmname = window.get_wm_name(), window.get_wm_class()
			if wmname is not None: break
			window = window.query_tree().parent
		event, () = rq.EventField(None).parse_binary_value(reply.data, local_d.display, None, None)
		if event.type == 2:
			if event.sequence_number:
				type = 2
			else:
				type = 1
		else:
			type = 0
		v = (type, wmname, event.detail, event.state, event.time)
		# print(v)
		pickle.dump(v, f)

	ctx = rec_d.record_create_context(
		0,
		[record.AllClients],
		[
			((0,0), (0,0), (0,0,0,0), (0,0,0,0), (0,0), (X.KeyPress, X.KeyPress), (0, 0), False, False,),
			((0,0), (0,0), (0,0,0,0), (0,0,0,0), (0,0), (X.KeyRelease, X.KeyRelease), (0, 0), False, False,),
		])
	rec_d.record_enable_context(ctx, callback)
	rec_d.record_free_context(ctx)
