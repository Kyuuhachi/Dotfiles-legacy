"use strict"; {

const XUL_NS = "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul";
const {require} = Cu.import("resource://devtools/shared/Loader.jsm", {});
const {gDevTools} = require("devtools/client/framework/devtools");
const {TargetFactory} = require("devtools/client/framework/target");
const ToolboxProcess = Cu.import("resource://devtools/client/framework/ToolboxProcess.jsm", {});
const {UrlbarInput} = ChromeUtils.import("resource:///modules/UrlbarInput.jsm", {});

let keys, gKeys, topKeys;

let closeTab = n => {
	let tab = gBrowser.selectedTab;
	gBrowser.tabContainer.advanceSelectedTab(n)
	gBrowser.removeTab(tab, { animate: true });
};

let openUrl = url => {
	console.log(url);
	openUILink(url, null, { ignoreButton: true, triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal() });
};

topKeys = {
	"o": () => openLocation(),
	"t": () => BrowserOpenTab(),
	"r": () => BrowserReload(),
	"R": () => BrowserReloadSkipCache(),
	"d": () => closeTab(1),
	"D": () => closeTab(-1),
	"u": () => undoCloseTab(),
	"U": () => undoCloseWindow(),

	"h": () => goDoCommand("cmd_scrollLeft"),
	"j": () => goDoCommand("cmd_scrollLineDown"),
	"k": () => goDoCommand("cmd_scrollLineUp"),
	"l": () => goDoCommand("cmd_scrollRight"),
	"g": () => keys = gKeys,
	"G": () => goDoCommand("cmd_scrollBottom"),

	"H": () => gBrowser.goBack(),
	"L": () => gBrowser.goForward(),

	"n": () => gBrowser.getFindBar().then(b => b.onFindAgainCommand(false)),
	"N": () => gBrowser.getFindBar().then(b => b.onFindAgainCommand(true)),
	"/": () => gBrowser.getFindBar().then(b => b.startFind(1)),
	"^f": () => gBrowser.getFindBar().then(b => b.startFind(1)),
	// accessibility.typeaheadfind.manual → false for find to work (though I reimplement it to mean the same, so...)

	"+": () => FullZoom.enlarge(),
	"=": () => FullZoom.enlarge(),
	"-": () => FullZoom.reduce(),
	"0": () => FullZoom.reset(),
	"^+": () => FullZoom.enlarge(),
	"^=": () => FullZoom.enlarge(),
	"^-": () => FullZoom.reduce(),
	"^0": () => FullZoom.reset(),
};

gKeys = {
	"g": () => goDoCommand("cmd_scrollTop"),
	"t": () => gBrowser.tabContainer.advanceSelectedTab(1, true),
	"T": () => gBrowser.tabContainer.advanceSelectedTab(-1, true),
	"0": () => gBrowser.selectedTab = gBrowser.tabContainer._firstTab,
	"$": () => gBrowser.selectedTab = gBrowser.tabContainer._lastTab,
	"p": () => gBrowser.selectedTab.pinned ? gBrowser.unpinTab(gBrowser.selectedTab) : gBrowser.pinTab(gBrowser.selectedTab),
	"d": () => gBrowser.selectedTab = gBrowser.duplicateTab(gBrowser.selectedTab),
	once: true,
};

keys = topKeys;


// {{{1 Content-disposition
Services.obs.addObserver({
	observe: (s,t,d) => {
		let http = s.QueryInterface(Ci.nsIHttpChannel);
		http.setResponseHeader("content-disposition", "", false);
	}
}, "http-on-examine-response");
// {{{1 f
{
	let stack = null, boxes = null, string = null;
	topKeys["f"] = () => gBrowser.selectedBrowser.messageManager.sendAsyncMessage("kitsune@link_start");

	window.messageManager.addMessageListener("kitsune@link_show", ({data: els}) => {
		let w = gBrowser.selectedBrowser.clientWidth, h = gBrowser.selectedBrowser.clientHeight;
		let els2 = [];
		for(let [id,l,u,r,d] of els) {
			l = Math.max(l, 0);
			u = Math.max(u, 0);
			r = Math.min(r, w);
			d = Math.min(d, h);
			if(l < r && u < d)
				els2.push([id,l,u,r,d]);
		}

		stack && stack.remove(); // Shouldn't happen, but better safe than sorry.
		stack = document.createElementNS(XUL_NS, "stack");
		stack.classList.add("kitsune-link-overlay");
		gBrowser.selectedBrowser.parentNode.append(stack);
		stack.addEventListener("blur", () => {
			stack.remove();
			stack = boxes = string = null;
		});

		document.commandDispatcher.focusedElement = stack;

		boxes = [];
		let len = els2.length.toString(4).length
		for(let [id,l,u,r,d] of els2) {
			let box = document.createElementNS(XUL_NS, "hbox");
			box.classList.add("kitsune-link");
			box.setAttribute("left", l);
			box.setAttribute("top", u);
			box.setAttribute("width", r-l);
			box.setAttribute("height", d-u);
			box.label = boxes.length.toString(4).padStart(len, '0').replace(/./g, n => "asdf"[n]);
			box.id = id;
			let label = document.createElementNS("http://www.w3.org/1999/xhtml", "div");
			label.classList.add("kitsune-link-label");
			box.append(label);

			stack.append(box);
			boxes.push(box);
		}

		string = "";
		stack.addEventListener("keypress", e => {
			e.stopPropagation();
			e.preventDefault();
			console.log(e);
			if("asdf".indexOf(e.key) != -1)
				string += e.key;
			else if(e.key == "Backspace" && string)
				string = string.substring(0, string.length-1);
			else
				return gBrowser.selectedBrowser.focus();
			let [result, rest] = updateLabels();
			if(!rest) {
				gBrowser.selectedBrowser.focus();
				if(result) gBrowser.selectedBrowser.messageManager.sendAsyncMessage("kitsune@link_click", result.id)
			}
		});
		updateLabels();
	});

	function updateLabels() {
		let matches = [];
		for(let box of boxes) {
			let [label] = box.getElementsByClassName("kitsune-link-label");
			if(box.label.startsWith(string)) {
				box.classList.add("kitsune-link-match");
				label.textContent = box.label.substring(string.length);
				matches.push(box);
			} else {
				box.classList.remove("kitsune-link-match");
				label.textContent = "";
			}
		}
		return matches;
	}
}
// {{{1 Focus
{
	topKeys["Escape"] = () => {
		gBrowser.selectedBrowser.messageManager.sendAsyncMessage("kitsune@unfocus");
		document.commandDispatcher.focusedElement = document.documentElement;
	};

	window.addEventListener("blur", () => keys = topKeys);
	gBrowser.tabContainer.addEventListener("TabSelect", () => keys = topKeys);
		
	gBrowser.tabContainer.addEventListener("TabSelect", e => {
		for(let tab of [e.detail.previousTab, e.target]) {
			tab.linkedBrowser._urlbarFocused = tab._findBarFocused = false;
			tab.linkedBrowser.messageManager.sendAsyncMessage("kitsune@unfocus");
		}
	});

	UrlbarInput.prototype.handleRevert = function() {
		this.window.gBrowser.userTypedValue = null;
		this.window.URLBarSetURI(null, true);
		this.blur();
	}
}
// {{{1 Findbar
{
	gBrowser.getFindBar().then(b => {
		Object.getPrototypeOf(b)._finishFAYT = function(e) {
			this.browser.finder.focusContent();
			e && e.preventDefault();
			this.close();
			return true;
		};
	});
	gBrowser.tabContainer.addEventListener("TabFindInitialized", e => {
		let findBar = e.target._findBar;
		findBar._findField.addEventListener("keypress", e => {
			if(!e.altKey && e.ctrlKey && !e.metaKey && !e.shiftKey) {
				if(e.key == "i") { findBar.getElement("find-case-sensitive").click(); e.preventDefault(); }
				if(e.key == "b") { findBar.getElement("find-entire-word").click(); e.preventDefault(); }
			}
		});
	});
}
// {{{1 Open-in-tab
{ // This doesn't quite work. It seems that although whereToOpenLink *is* called on normal <a> clicks, it opens the link in the current tab as well
	let nextTab = null;
	window.whereToOpenLink_ = window.whereToOpenLink;
	window.whereToOpenLink = (...args) => {
		let n = nextTab;
		window.setTimeout(() => nextTab = null, 1);
		return n || window.whereToOpenLink_(...args);
	};
	topKeys["^t"] = () => nextTab = "tab";
	topKeys["^T"] = () => nextTab = "tabshifted";
}
// {{{1 Url manipulation
{
	function incrementURL(count) {
		let url = gBrowser.selectedBrowser.currentURI;
		let path = url.pathQueryRef;

		let start = -1, end = -1;
		for(var i = 1; i < path.length; i++)
			if(path[i] == '%')
				i += 2;
			else if(path[i].match(/\d/)) {
				start = i;
				while(i < path.length && path[i].match(/\d/)) i++;
				end = i;
			}
		if(start >= 0) {
			let pre = path.substring(0, start);
			let num = path.substring(start, end);
			let post = path.substring(end);
			let newNum = String(Math.max(parseInt(num, 10) + count, 0));
			if(num.match(/^0/))
				newNum = newNum.padStart(num.length, "0");
			url = url.mutate().setPathQueryRef(pre + newNum + post).finalize();
		}
		return url;
	}
	function goUp() {
		let eTLD = Cc["@mozilla.org/network/effective-tld-service;1"].getService(Components.interfaces.nsIEffectiveTLDService);
		let url = gBrowser.selectedBrowser.currentURI;

		let mut = url.mutate();
		if(url.ref) mut.setRef(null);
		else if(url.query) mut.setQuery(url.query.replace(/(^|&)[^&]*$/, ""));
		else if(url.pathQueryRef != "/") mut.setPathQueryRef(url.pathQueryRef.replace(/[/][^/]+[/]*$/, ""));
		else if(url.host != eTLD.getBaseDomain(url)) mut.setHost(url.host.replace(/^[^.]*[.]/, ""))
		url = mut.finalize();

		return url;
	}
	function goTop() {
		return gBrowser.selectedBrowser.currentURI.mutate().setPathQueryRef("/").finalize();
	}
	function goto(url) {
		if(url.spec != gBrowser.selectedBrowser.currentURI.spec)
			openUrl(url.spec);
	}
	topKeys["A"] = () => goto(incrementURL(1)); // ^A is reserved, use A instead
	topKeys["X"] = () => goto(incrementURL(-1));
	gKeys["u"] = () => goto(goUp());
	gKeys["U"] = () => goto(goTop());
}

// {{{1 Devtools
{
	topKeys["^I"] = topKeys["F12"] = () =>
		TargetFactory.forTab(gBrowser.selectedTab).then(t => {
			if(gDevTools.getToolbox(t))
				gDevTools.closeToolbox(t);
			else
				gDevTools.showToolbox(t, null, null, null, Cu.now());
		})
	topKeys["^!I"] = () => {
		if(ToolboxProcess.processes.size)
			ToolboxProcess.processes.values().next().value.close();
		else
			ToolboxProcess.BrowserToolboxProcess.init();
	}
	gKeys["f"] = () => BrowserViewSource(gBrowser.selectedBrowser);
}
// {{{1 Clipboard
{
	function copy(s) {
		let tf = Cc["@mozilla.org/widget/transferable;1"].createInstance(Ci.nsITransferable);
		tf.init(null);
		tf.addDataFlavor("text/unicode");

		let str = Cc["@mozilla.org/supports-string;1"].createInstance(Ci.nsISupportsString);
		str.data = s;
		tf.setTransferData("text/unicode", str);
		Services.clipboard.setData(tf, null, Services.clipboard.kGlobalClipboard);
	}
	function paste() {
		let tf = Cc["@mozilla.org/widget/transferable;1"].createInstance(Ci.nsITransferable);
		tf.init(null);
		tf.addDataFlavor("text/unicode");

		Services.clipboard.getData(tf, Services.clipboard.kGlobalClipboard);
		let str = {};
		tf.getTransferData("text/unicode", str);
		return str.value.QueryInterface(Ci.nsISupportsString).data;
	}
	topKeys["y"] = () => {
		let url = decodeURI(gBrowser.selectedBrowser.currentURI.spec);
		copy(url);
		let ol = XULBrowserWindow.overLink;
		let new_ol = "Copied " + url;
		XULBrowserWindow.setOverLink(new_ol, null);
		setTimeout(() => XULBrowserWindow.overLink == new_ol && XULBrowserWindow.setOverLink(ol, null), 1000);
	};
	topKeys["p"] = () => openUrl(paste());
}
// {{{1 Key handler
{
	let evt = null;
	window.addEventListener("keypress", e => evt = e, {capture: true, mozSystemGroup: true});

	for(let k of document.getElementsByTagName("key")) {
		k.removeAttribute("key");
		k.removeAttribute("keycode");
		k.removeAttribute("charcode");
	}

	for(let k in KeyEvent) {
		if(!k.startsWith("DOM_VK_")) continue;
		let key = document.createElementNS(XUL_NS, "key");
		key.setAttribute("keycode", k.substring(4));
		key.setAttribute("modifiers", "shift,alt,meta,os,control,any");
		key.addEventListener("command", () => keypress(evt));
		key.setAttribute("oncommand", "void 0;");
		document.getElementById("mainKeyset").prepend(key)
	}

	function keypress(e) {
		console.log(e);
		let h = keys["^".repeat(e.ctrlKey) + "!".repeat(e.altKey) + e.key];
		if(keys.once) keys = topKeys;
		h && h();
	}
}
// }}}1
}
