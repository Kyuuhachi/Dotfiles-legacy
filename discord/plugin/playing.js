/* global Modules, MonkeyPatch */
"use strict";

(async function(){
	function fixActivity(a) {
		a = a || {};
		a.type = 3; // Watching
		a.name = "( ͡° ͜ʖ ͡°)";
		return a;
	}
	const Presence = await Modules.byFields("getPresence", "getStatus", "getActivity");
	MonkeyPatch(Presence, "getPresence", { after: data => data.ret.activity = fixActivity(data.ret.activity) });
	MonkeyPatch(Presence, "getActivity", { after: data => data.ret = fixActivity(data.returnValue) });
	Modules.byFields("dirtyDispatch").then(Dispatcher => Dispatcher.dirtyDispatch({ type: "RESUME", settings: {} }));
})();
