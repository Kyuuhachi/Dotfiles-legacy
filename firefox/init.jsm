/* global Components */
/* exported EXPORTED_SYMBOLS */
const EXPORTED_SYMBOLS = [];
const { classes: Cc, interfaces: Ci, utils: Cu, } = Components;

const {OS} = Cu.import("resource://gre/modules/osfile.jsm");
const {Services} = Cu.import("resource://gre/modules/Services.jsm");

const defaultIncludes = [
	"chrome://browser/content/browser.xhtml",
];

function listFiles(dir) {
	const files = [];
	const it = dir.directoryEntries.QueryInterface(Ci.nsISimpleEnumerator);
	while(it.hasMoreElements())
		files.push(it.getNext().QueryInterface(Ci.nsIFile));
	return files.sort((a,b) => a.path > b.path);
}

function readFile(file) {
	const stream = Cc["@mozilla.org/network/file-input-stream;1"].createInstance(Ci.nsIFileInputStream);
	stream.init(file, 0x01, 0, 0);
	const cvstream = Cc["@mozilla.org/intl/converter-input-stream;1"].createInstance(Ci.nsIConverterInputStream);
	cvstream.init(stream, "UTF-8", 1024, Ci.nsIConverterInputStream.DEFAULT_REPLACEMENT_CHARACTER);
	let content = "";
	const data = {};
	while(cvstream.readString(1024, data))
		content += data.value;
	cvstream.close();
	return content;
}

function loadAllScripts(url, scope) {
	for(const file of listFiles(Services._userDir())) {
		if(!/.*\.user\.jsm?$/.test(file.leafName)) continue;
		
		const text = readFile(file);
		const matches = [...text.matchAll(/^\s*\/\/@\s*ON\s+(\S+)\s*$/gm)];
		const includes = new Set(matches.length ? matches.map(([_, a]) => a) : defaultIncludes);
		if(includes.has(url))
			try {
				Services.scriptloader.loadSubScript(
					`${OS.Path.toFileURI(file.path)}?${Date.now()}`,
					scope(),
					"UTF-8",
				);
			} catch(e) {
				console.error(e);
			}
	}
}

const observer = {
	observe(window) {
		window.addEventListener("DOMContentLoaded", this, true);
	},

	receiveMessage(x) {
		// console.log(x)
		// console.log(Services.mm.broadcastAsyncMessage("Extension:Execute", { options: {
		// 	frameId: x.data.frameId,
		// 	wantReturnValue: true,
		// 	matchAboutBlank: true,
		// 	jsCode: "alert(404)",
		// 	runAt: "document_start",
		// }}));
	},

	handleEvent(e) {
		let document = e.originalTarget;
		let window = document.defaultView;
		loadAllScripts(window.location.href, () => ({
			window: window,
			document: document,
		}));
	}
};


if(!Services.appinfo.inSafeMode) {
	Services.obs.addObserver(observer, "chrome-document-global-created", false);
	Services.mm.addMessageListener("Extension:DocumentChange", observer);
}
