/* global Components */
/* exported EXPORTED_SYMBOLS */
"use strict";

const EXPORTED_SYMBOLS = [];

const { classes: Cc, interfaces: Ci, utils: Cu } = Components;
const {require} = Cu.import("resource://devtools/shared/Loader.jsm");
const {Services} = Cu.import("resource://gre/modules/Services.jsm");

Services.obs.addObserver(w => {
	w.addEventListener("DOMContentLoaded", e => {
		const window = e.originalTarget.defaultView;
		if(window.location.href != "chrome://browser/content/browser.xhtml") return;
		enko(window);
	});
}, "domwindowopened");

function enko(window) {
	const document = window.document;
	const gBrowser = window._gBrowser;
	const XUL_NS = "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul";

	function addFrameScript(func) {
		window.messageManager.loadFrameScript(
			"data:application/javascript;charset=UTF-8," + encodeURIComponent("\"use strict\";("+func.toString()+")()"),
			true);
	}

	function addStylesheet(sheet) {
		const sss = Cc["@mozilla.org/content/style-sheet-service;1"].getService(Ci.nsIStyleSheetService);
		
		sss.loadAndRegisterSheet(
			Services.io.newURI("data:text/css;charset=UTF-8," + encodeURIComponent(sheet)),
			sss.AGENT_SHEET);
	}

	addStylesheet`
	@-moz-document url("chrome://browser/content/browser.xhtml") {
		findbar {
			transition: none !important;
		}

		.enko-link-overlay {
			filter: url('data:image/svg+xml, \
				<svg xmlns="http://www.w3.org/2000/svg"> \
					<filter id="filter"> \
						<feColorMatrix type="matrix" values=" \
							0 0 0 255 0 \
							0 0 0 255 0 \
							0 0 0 255 0 \
							0 0 0 0 .5" /> \
						<feMerge> \
							<feMergeNode /> \
							<feMergeNode in="SourceGraphic" /> \
						</feMerge> \
					</filter> \
				</svg> \
			#filter');
			-moz-user-focus: normal;
			z-index: 999;
		}
		.enko-link {
			-moz-stack-sizing: ignore;
			position: absolute;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		.enko-link.enko-link-match {
			background: rgba(255, 255, 255, 0.01);
			box-shadow: rgba(255, 255, 255, 0.01) 0 0 2px;
		}

		.enko-link-label {
			text-shadow: #000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,
						 #000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px,#000 0 0 1px;
			font-family: monospace;
			color: #FFFFFF;
			font-weight: bold;
			display: block;
		}
		.enko-link-label::first-letter {
			color: #FFFF00;
		}
	}
	`;

	addFrameScript(function() {
		/* global addMessageListener, content, sendAsyncMessage */
		addMessageListener("enko@unfocus", () => {
			content.document.activeElement.blur();
		});

		let links = null;
		let linkselector = `input:not([type=hidden]), a[href], area, textarea, button, select, summary,
			[onclick], [onmouseover], [onmousedown], [onmouseup], [oncommand], [role='link'], [role='button'], [role='checkbox'],
			[role='combobox'], [role='listbox'], [role='listitem'], [role='menuitem'], [role='menuitemcheckbox'],
			[role='menuitemradio'], [role='option'], [role='radio'], [role='scrollbar'], [role='slider'], [role='spinbutton'],
			[role='tab'], [role='textbox'], [role='treeitem'], [tabindex]`;

		addMessageListener("enko@link_start", () => {
			let els = [];
			let boxes = [];
			for(let el of content.document.querySelectorAll(linkselector)) {
				if(el.disabled) continue;
				for(let {left, top, right, bottom} of el.getClientRects()) {
					if(right < 0 || left > content.innerWidth) continue;
					if(bottom < 0 || top > content.innerHeight) continue;
					els.push(el);
					boxes.push([boxes.length, left, top, right, bottom]);
				}
			}
			links = els;
			sendAsyncMessage("enko@link_show", boxes);
		});

		addMessageListener("enko@link_click", ({data: id}) => {
			let link = links[id];
			if(!link) return; // Shouldn't happen, but no promises
			link.focus();
			link.click();
		});

		addMessageListener("enko@go_rel", ({data: rel}) => {
			let els = content.document.querySelectorAll(`[rel*=${rel}]`);
			if(els.length > 0) {
				let el = els[els.length-1];
				if(el.name == "link") content.document.location = el.href;
				else el.click();
			}
		});
	});

	let keys, gKeys, topKeys;

	let closeTab = n => {
		let tab = gBrowser.selectedTab;
		gBrowser.tabContainer.advanceSelectedTab(n);
		gBrowser.removeTab(tab, { animate: true });
	};

	let openUrl = url => {
		window.openUILink(url, null, {
			ignoreButton: true,
			triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()
		});
	};

	topKeys = {
		"o": () => window.openLocation(),
		"F6": () => window.openLocation(),
		"t": () => window.BrowserOpenTab(),
		"T": () => window.OpenBrowserWindow(),

		"r": () => window.BrowserReload(),
		"R": () => window.BrowserReloadSkipCache(),

		"d": () => closeTab(1),
		"D": () => closeTab(-1),

		"^Q": () => window.closeWindow(true),

		"u": () => window.undoCloseTab(),
		"U": () => window.undoCloseWindow(),

		"h": () => window.goDoCommand("cmd_scrollLeft"),
		"j": () => window.goDoCommand("cmd_scrollLineDown"),
		"k": () => window.goDoCommand("cmd_scrollLineUp"),
		"l": () => window.goDoCommand("cmd_scrollRight"),
		"g": () => keys = gKeys,
		"G": () => window.goDoCommand("cmd_scrollBottom"),

		"H": () => gBrowser.goBack(),
		"L": () => gBrowser.goForward(),

		"+": () => window.FullZoom.enlarge(),
		"=": () => window.FullZoom.enlarge(),
		"-": () => window.FullZoom.reduce(),
		"0": () => window.FullZoom.reset(),

		"[": () => goRel("prev"),
		"]": () => goRel("next"),

		"^Escape": () => keys = {
			"^Escape": () => keys = topKeys
		},
	};

	gKeys = {
		"g": () => window.goDoCommand("cmd_scrollTop"),
		"t": () => gBrowser.tabContainer.advanceSelectedTab(1, true),
		"T": () => gBrowser.tabContainer.advanceSelectedTab(-1, true),
		"0": () => gBrowser.selectedTab = gBrowser.tabContainer._firstTab,
		"$": () => gBrowser.selectedTab = gBrowser.tabContainer._lastTab,
		"p": () => gBrowser.selectedTab.pinned ? gBrowser.unpinTab(gBrowser.selectedTab) : gBrowser.pinTab(gBrowser.selectedTab),
		"d": () => gBrowser.selectedTab = gBrowser.duplicateTab(gBrowser.selectedTab),
		"r": () => document.getElementById("reader-mode-button")?.click(),
		once: true,
	};

	function goRel(rel) {
		gBrowser.selectedBrowser.messageManager.sendAsyncMessage("enko@go_rel", rel);
	}



	keys = topKeys;


	// {{{1 f
	{
		let stack = null, boxes = null, string = null;
		topKeys["f"] = () => {
			gBrowser.selectedBrowser.messageManager.sendAsyncMessage("enko@link_start");
		};

		window.messageManager.addMessageListener("enko@link_show", ({data: els}) => {
			let w = gBrowser.selectedBrowser.clientWidth;
			let h = gBrowser.selectedBrowser.clientHeight;
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
			stack.classList.add("enko-link-overlay");
			gBrowser.selectedBrowser.parentNode.append(stack);
			stack.addEventListener("blur", () => {
				stack.remove();
				stack = boxes = string = null;
			});

			document.commandDispatcher.focusedElement = stack;

			boxes = [];
			let len = els2.length.toString(4).length;
			for(let [id,l,u,r,d] of els2) {
				let box = document.createElementNS("http://www.w3.org/1999/xhtml", "div");
				box.classList.add("enko-link");
				box.setAttribute("style", `position: absolute; left: ${l}px; top: ${u}px; width: ${r-l}px; height: ${d-u}px`);
				box.label = boxes.length.toString(4).padStart(len, "0").replace(/./g, n => "asdf"[n]);
				box.id = id;
				let label = document.createElementNS("http://www.w3.org/1999/xhtml", "div");
				label.classList.add("enko-link-label");
				box.append(label);

				stack.append(box);
				boxes.push(box);
			}

			string = "";
			stack.addEventListener("keypress", e => {
				e.stopPropagation();
				e.preventDefault();
				if("asdf".indexOf(e.key) != -1)
					string += e.key;
				else if(e.key == "Backspace" && string)
					string = string.substring(0, string.length-1);
				else
					return gBrowser.selectedBrowser.focus();
				let [result, rest] = updateLabels();
				if(!rest) {
					gBrowser.selectedBrowser.focus();
					if(result) gBrowser.selectedBrowser.messageManager.sendAsyncMessage("enko@link_click", result.id);
				}
			});
			updateLabels();
		});

		function updateLabels() {
			let matches = [];
			for(let box of boxes) {
				let [label] = box.getElementsByClassName("enko-link-label");
				if(box.label.startsWith(string)) {
					box.classList.add("enko-link-match");
					label.textContent = box.label.substring(string.length);
					matches.push(box);
				} else {
					box.classList.remove("enko-link-match");
					label.textContent = "";
				}
			}
			return matches;
		}
	}
	// {{{1 Focus
	{
		topKeys["Escape"] = () => {
			gBrowser.selectedBrowser.messageManager.sendAsyncMessage("enko@unfocus");
			document.commandDispatcher.focusedElement = document.documentElement;
		};

		window.addEventListener("blur", () => keys = topKeys);
		gBrowser.tabContainer.addEventListener("TabSelect", () => keys = topKeys);
	}
	// {{{1 Findbar
	{
		keys["n"] = () => gBrowser.getFindBar().then(b => b.onFindAgainCommand(false));
		keys["N"] = () => gBrowser.getFindBar().then(b => b.onFindAgainCommand(true));
		keys["/"] = () => gBrowser.getFindBar().then(b => b.startFind(1));
		keys["?"] = () => gBrowser.getFindBar().then(b => b.startFind(2)); // Links, rather than reverse
		keys["^f"] = () => gBrowser.getFindBar().then(b => b.startFind(1));
		keys["^F"] = () => gBrowser.getFindBar().then(b => b.startFind(0));
	}

	// // {{{1 Open-in-tab
	// { // This doesn't quite work. It seems that although whereToOpenLink *is* called on normal <a> clicks, it opens the link in the current tab as well
	// 	let nextTab = null;
	// 	const whereTo = window.whereToOpenLink.bind(window);
	// 	window.whereToOpenLink = (...args) => {
	// 		let n = nextTab;
	// 		window.setTimeout(() => nextTab = null, 1);
	// 		return n || whereTo(...args);
	// 	};
	// 	topKeys["^t"] = () => nextTab = "tab";
	// 	topKeys["^T"] = () => nextTab = "tabshifted";
	// }
	// {{{1 Url manipulation
	{
		function modUrl(f) {
			const ioService = Cc["@mozilla.org/network/io-service;1"].getService(Ci.nsIIOService);
			let url = gBrowser.selectedBrowser.currentURI;

			if(url.spec.startsWith("about:reader?url=")) {
				let theUrl = decodeURIComponent(url.query.split("=")[1]);
				theUrl = f(ioService.newURI(theUrl)).spec;
				url = url.mutate().setQuery("?url=" + encodeURIComponent(theUrl)).finalize();
			} else url = f(url);

			if(url.spec != gBrowser.selectedBrowser.currentURI.spec)
				openUrl(url.spec);
		}
		
		function incrementUrl(url, count) {
			return url.mutate().setSpec(url.spec.replace(/(?<!%.?)\d+(?!.*(?<!%.?)\d+)/, s => {
				let s2 = String(Math.max(parseInt(s, 10) + count, 0));
				return s.startsWith(0) ? s2.padStart(s.length, "0") : s2;
			})).finalize();
		}
		
		function goUp(url) {
			let eTLD = Cc["@mozilla.org/network/effective-tld-service;1"].getService(Ci.nsIEffectiveTLDService);

			let mut = url.mutate();
			if(url.spec.startsWith("view-source:")) mut.setSpec(url.spec.substring(12));
			else if(url.ref) mut.setRef(null);
			else if(url.query) mut.setQuery(url.query.replace(/(^|&)[^&]*$/, ""));
			else if(url.pathQueryRef != "/") mut.setPathQueryRef(url.pathQueryRef.replace(/[/][^/]+[/]*$/, ""));
			else if(url.host != eTLD.getBaseDomain(url)) mut.setHost(url.host.replace(/^[^.]*[.]/, ""));
			return mut.finalize();
		}
		
		function goTop(url) {
			while(!url.equals(url = goUp(url)));
			return url;
		}

		topKeys["A"] = () => modUrl(url => incrementUrl(url, 1));
		topKeys["X"] = () => modUrl(url => incrementUrl(url, -1));
		gKeys["u"] = () => modUrl(goUp);
		gKeys["U"] = () => modUrl(goTop);
	}

	// {{{1 Devtools
	{
		const {gDevToolsBrowser} = require("devtools/client/framework/devtools-browser");

		topKeys["^I"] = topKeys["F12"] = () =>
			gDevToolsBrowser.onKeyShortcut(window, "toggleToolbox", Cu.now());
		const Launcher = Cu.import("resource://devtools/client/framework/browser-toolbox/Launcher.jsm", {});
		topKeys["^!I"] = () => {
			if(Launcher.processes.size)
				Launcher.processes.values().next().value.close();
			else
				Launcher.BrowserToolboxLauncher.init();
		};
		gKeys["f"] = () => window.BrowserViewSource(gBrowser.selectedBrowser);
	}

	// {{{1 Clipboard
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
	function copyUrl(escape) {
		let url = gBrowser.selectedBrowser.currentURI.spec;
		if(!escape) url = decodeURI(url).replace(" ", "%20");
		copy(url);
		let ol = window.XULBrowserWindow.overLink;
		let new_ol = "Copied " + encodeURIComponent(url);
		window.XULBrowserWindow.setOverLink(new_ol, null);
		setTimeout(() => {
			if(window.XULBrowserWindow.overLink == new_ol)
				window.XULBrowserWindow.setOverLink(ol, null);
		}, 1000);
	}
	topKeys["y"] = () => copyUrl(false);
	topKeys["Y"] = () => copyUrl(true);
	topKeys["p"] = () => openUrl(paste());


	// {{{1 Key handler
	let evt = null;
	window.addEventListener("keypress", e => evt = e, {capture: true, mozSystemGroup: true});

	for(let k of document.getElementsByTagName("key")) {
		k.removeAttribute("key");
		k.removeAttribute("keycode");
		k.removeAttribute("charcode");
	}

	for(let k in window.KeyEvent) {
		if(!k.startsWith("DOM_VK_")) continue;
		let key = document.createElementNS(XUL_NS, "key");
		key.setAttribute("keycode", k.substring(4));
		key.setAttribute("modifiers", "shift,alt,meta,os,control,any");
		key.addEventListener("command", () => keypress(evt));
		key.setAttribute("oncommand", "void 0;");
		document.getElementById("mainKeyset").prepend(key);
	}

	function keypress(e) {
		let h = undefined;
		if(!h && e.ctrlKey) h = keys["^" + "!".repeat(e.altKey) + e.key];
		if(!h)              h = keys[      "!".repeat(e.altKey) + e.key];
		if(keys.once) keys = topKeys;
		// console.log(e, h);
		if(h) h();
	}
}
