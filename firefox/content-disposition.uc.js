Services.obs.addObserver({
	observe: (s,t,d) => {
		let http = s.QueryInterface(Ci.nsIHttpChannel);
		http.setResponseHeader("content-disposition", "", false);
	}
}, "http-on-examine-response");
