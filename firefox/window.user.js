/* global Components */
/* exported EXPORTED_SYMBOLS */
"use strict";

const EXPORTED_SYMBOLS = [];
const { interfaces: Ci, utils: Cu, classes: Cc } = Components;

const { BrowserWindowTracker: BWT } = Cu.import("resource:///modules/BrowserWindowTracker.jsm");
const { PrivateBrowsingUtils: PBU } = Cu.import("resource://gre/modules/PrivateBrowsingUtils.jsm");
const { Services } = Cu.import("resource://gre/modules/Services.jsm");

morph(BWT, {
	getTopWindow({allowPopups, private: private_} = {}) {
		return this.orderedWindows.find(win =>
			!win.closed
			&& (allowPopups || win.toolbar.visible)
			&& (private_ === undefined || PBU.permanentPrivateBrowsing || PBU.isWindowPrivate(win) == private_)
		);
	},

	windowCreated(_browser) { },

	get windowCount() { return this.orderedWindows.length; },
	get orderedWindows() { return [...Services.wm.getEnumerator("navigator:browser")]; },
	// getAllVisibleTabs() {}, unused

	track(win) {
		const handlers = [
			[win, "activate", () => updateId(window.gBrowser.selectedBrowser)],
			[win.gBrowser.tabContainer, "TabSelect", e => updateId(e.target.linkedBrowser)],
			[win.gBrowser.tabContainer, "TabBrowserInserted", e => updateId(e.target.linkedBrowser)],
			[win, "unload", () => {
				for(const [obj, evt, hand] of handlers)
					obj.removeEventListener(evt, hand);
			}],
		];
		for(const [obj, evt, hand] of handlers)
			obj.addEventListener(evt, hand);
	},
});

function morph(from, to) {
	for(const key in from) delete from[key];
	for(const key in to) Object.defineProperty(from, key, Object.getOwnPropertyDescriptor(to, key));
}

// I don't know what this actually does, but probably safest to keep it
function updateId(browser) {
	let windowIDWrapper = Cc["@mozilla.org/supports-PRUint64;1"].createInstance(Ci.nsISupportsPRUint64);
	windowIDWrapper.data = browser.outerWindowID;
	Services.obs.notifyObservers(windowIDWrapper, "net:current-toplevel-outer-content-windowid");
}
