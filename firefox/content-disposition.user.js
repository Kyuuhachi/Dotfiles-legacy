/* global Components */
/* exported EXPORTED_SYMBOLS */
const EXPORTED_SYMBOLS = [];
const { interfaces: Ci, utils: Cu, classes: Cc } = Components;

const {Services} = Cu.import("resource://gre/modules/Services.jsm");

if(Services._content_disposition)
	Services.obs.removeObserver(Services._content_disposition, "http-on-examine-response");

Services._content_disposition = {
	observe: s => {
		const http = s.QueryInterface(Ci.nsIHttpChannel);
		const mimeService = Cc["@mozilla.org/mime;1"].getService(Ci.nsIMIMEService);
		const mime = mimeService.getFromTypeAndExtension(http.contentType, http.URI?.fileExtension ?? http.originalURI.fileExtension);
		if(mime.hasDefaultHandler)
			http.setResponseHeader("content-disposition", "", false);
	}
};

Services.obs.addObserver(Services._content_disposition, "http-on-examine-response");
