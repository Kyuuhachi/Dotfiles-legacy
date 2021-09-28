"use strict";
const { ChromeUtils, Services, SessionStore, CustomizableUI } = window;

const bundle_ = Services.strings.createBundle("chrome://98vertical/locale/vertical.properties");
const bundle = {
	getString(key) { return bundle_.GetStringFromName(key); },
	getFormattedString(key, array) { return bundle_.formatStringFromName(key, array); },
};

const { TabsPanel } = ChromeUtils.import("resource:///modules/TabsList.jsm");
const TabsListBase = Object.getPrototypeOf(TabsPanel);

// {{{1 HTML factory methods
const _make = isHtml => new Proxy((...children) => ({children}), {
	get(_, name) {
		const o = {[name](attrs={}, ...children) {
			Object.assign(o.attrs, attrs);
			o.children.push(...children);
			return o;
		}}[name];
		o.html = isHtml;
		o.attrs = Object.create(null);
		o.children = [];
		return o;
	}
});

const E = _make(false);
const Eh = _make(true);

function setAttributes(element, attrs) {
	for(const [name, value] of Object.entries(attrs)) {
		if(value)
			element.setAttribute(name, value);
		else
			element.removeAttribute(name);
	}
}

function make(document, ...e) {
	document = document.ownerDocument ?? document;
	const out = Object.create(null);
	function _make(e) {
		const el
			= e.children == null ? document.createTextNode(e)
			: e.name == null ? document.createDocumentFragment()
			: e.html ? document.createElement(e.name)
			: document.createXULElement(e.name);
		if(e.attrs) {
			setAttributes(el, e.attrs);
			if(e.attrs.id) out[e.attrs.id] = el;
			if(e.attrs.anonid) {
				out[e.attrs.anonid] = el;
				el.removeAttribute("anonid");
			}
		}
		for(const c of e.children ?? [])
			el.append(_make(c));
		return el;
	}
	out["root"] = _make({children: e});
	return out;
}
// }}}1

const ID = {
	widget:    "vertical-tabs-widget",
	pane:      "vertical-tabs-pane",
	context:   "vertical-tabs-context-menu",
	splitter:  "vertical-tabs-splitter",

	buttons:   "vertical-tabs-button-row",
	newTabButton: "vertical-tabs-new-tab-button",
	pinned:    "vertical-tabs-pinned",
	scrollbox: "vertical-tabs-scrollbox",
};

function makeWidget() {
	// The widget definition is global across all windows, so it must not
	// refer to the module-scope VerticalTabs, since the module is instanced
	if(CustomizableUI.getWidget("vertical-tabs-button")) return;
	CustomizableUI.createWidget({
		id: ID.widget,
		defaultArea: CustomizableUI.AREA_TABSTRIP,
		label: bundle.getString("sidebar.label"),
		tooltiptext: bundle.getString("sidebar.label"),
		localized: false,
		onCommand(e) {
			e.target.ownerGlobal.VerticalTabs.toggle();
		},
		onCreated(node) {
			node.append(make(node,
				E.observes({element: ID.pane, attribute: "checked"}),
				E.observes({element: ID.pane, attribute: "positionstart"}),
			).root);
		},
	});
}
makeWidget();

class VTabsList extends TabsListBase {
	constructor(...args) {
		super(...args);
		this.observer = new window.MutationObserver(mut => mut.forEach(({target: tab, attributeName: attr}) => {
			if(!["style"].includes(attr))
				if(tab.hasAttribute(attr))
					tab.vtab.setAttribute(attr, tab.getAttribute(attr));
				else
					tab.vtab.removeAttribute(attr);
		}));
	}

	_createRow(tab) {
		let { doc } = this;

		let vtab = doc.createXULElement("tab", {is: "vertical-tab"});
		vtab.tab = tab;
		tab.vtab = vtab;

		this._setRowAttributes(vtab, tab);

		this.observer.observe(tab, { attributes: true });
		for(const attr of tab.attributes)
			vtab.setAttribute(attr.name, attr.value);

		this.tabToElement.set(tab, vtab);
		return vtab;
	}

	_setRowAttributes(vtab, tab) {
		// for(const attr of row.attributes)
		// 	row.removeAttribute(attr.name);
		// for(const attr of tab.attributes)
		// 	row.setAttribute(attr.name, attr.value);
	}
}

const VerticalTabs = window.VerticalTabs = new class VerticalTabs {
	constructor() {
		this.atexit = [];
		window.addEventListener("unload", this.uninit.bind(this));

		const {
			root,
			[ID.pane]: pane,
			[ID.scrollbox]: scrollbox,
			[ID.pinned]: pinned,
			[ID.newTabButton]: newTabDummy,
		} = make(document,
			E.vbox(
				{
					class: "chromeclass-extrachrome",
					id: ID.pane,
					context: ID.context,
					hidden: true,
					width: 350,
				},
				E.observes({ "element": "TabsToolbar", "attribute": "brighttext" }),
				E.toolbar(
					{id: ID.buttons, mode: "icons", fullscreentoolbar: "true"},
					E.toolbartabstop({ "aria-hidden": true }),
					E.dummy({anonid: ID.newTabButton}),
				),
				E.toolbarseparator,
				E.arrowscrollbox({
					id: ID.scrollbox,
					class: "vertical-tabs-container",
					tooltip: "vertical-tabs-tooltip",
					context: "tabContextMenu",
					orient: "vertical",
					clicktoscroll: "true",
					flex: "1",
				}),
			),
			E.splitter(
				{ class: "chromeclass-extrachrome sidebar-splitter", id: ID.splitter },
				E.observes({ "element": ID.pane, "attribute": "hidden" }),
			)
		);

		// // Scrollbox tweaks
		// scrollbox._canScrollToElement = a => !a.tab.pinned;

		// scrollbox.shadowRoot.addEventListener("underflow", e => {
		// 	if(e.originalTarget != scrollbox.scrollbox || e.detail == 0 || !this.hasAttribute("overflow"))
		// 		return;

		// 	this.removeAttribute("overflow");
		// 	this._positionPinnedTabs();
		// }, true);

		// scrollbox.shadowRoot.addEventListener("overflow", e => {
		// 	if(e.originalTarget != scrollbox.scrollbox || e.detail == 0)
		// 		return;

		// 	this.setAttribute("overflow", "true");
		// 	this._positionPinnedTabs();
		// 	this._handleTabSelect(true);
		// });


		{
			const newTabButton = document.getElementById("new-tab-button").cloneNode(true);
			newTabButton.id = ID.newTabButton;
			newTabButton.tooltipText =
				window.gNavigatorBundle.getFormattedString("newTabButton.tooltip",
					[window.ShortcutUtils.prettifyShortcut(document.getElementById("key_newNavigatorTab"))]
				);

			const gBrowser = window._gBrowser;
			function updateNewTab() {
				gBrowser.tabContainer.observe.call({newTabButton}, null, "nsPref:changed", "privacy.userContext.enabled");
			}
			Services.prefs.addObserver("privacy.userContext", updateNewTab);
			this.atexit.push(() => Services.prefs.removeObserver("privacy.userContext", updateNewTab));
			updateNewTab();

			newTabDummy.replaceWith(newTabButton);
		}


		const browser = document.getElementById("browser");
		browser.insertBefore(root, browser.firstChild);

		this.pane = pane;
		this.pinned = pinned;
		this.scrollbox = scrollbox;
	}

	delayedInit() {
		this.initState();

		new VTabsList({
			containerNode: this.scrollbox,
			filterFn: tab => !tab.hidden,
		})._populate();

		this.setPositionalAttributes();
	}

	setPositionalAttributes() {

	}

	// get selectedItem() {
	// 	return window.gBrowser.tabbar.
	// }

	_handleTabSelect(aInstant) {
		let selectedTab = this.selectedItem;
		if(this.getAttribute("overflow") == "true")
			this.scrollbox.ensureElementIsVisible(selectedTab, aInstant);
	}

	initState() {
		const opener = window.opener;
		if(opener) {
			if(opener.closed || opener.location.protocol != "chrome:"
					|| !window.SidebarUI.windowPrivacyMatches(opener, window)) {
				return;
			}
			const other = opener.VerticalTabs;
			if(other) {
				this.pane.width = other.box.width;
				this.isOpen = other.isOpen;
				return;
			}
		}

		this.pane.width = Services.xulStore.getValue(document.documentURI, ID.pane, "width");
		this.isOpen = Services.xulStore.getValue(document.documentURI, ID.pane, "checked");
	}

	uninit() {
		const enumerator = Services.wm.getEnumerator("navigator:browser");
		if(!enumerator.hasMoreElements()) {
			if(this.pane.hasAttribute("checked")) Services.xulStore.persist(this.pane, "checked");
			else Services.xulStore.removeValue(document.documentURI, ID.pane, "checked");
			Services.xulStore.persist(this.pane, "width");
		}

		for(const ae of self.atexit) ae();
	}

	get root() {
		return this._root || (this._root = document.documentElement);
	}

	get isOpen() {
		return !this.pane.hidden;
	}

	set isOpen(val) {
		if(val && !this.isOpen) this.open();
		else if(!val && this.isOpen) this.close();
	}

	toggle() {
		this.isOpen = !this.isOpen;
	}

	open() {
		this.pane.hidden = false;
		this.pane.setAttribute("checked", true);
		this.root.setAttribute("vertical-tabs", true);
	}

	close() {
		this.pane.hidden = true;
		this.pane.removeAttribute("checked");
		this.root.removeAttribute("vertical-tabs");
	}
}();

SessionStore.promiseInitialized.then(() => !window.closed && VerticalTabs.delayedInit());
