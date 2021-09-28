console.trace(this);
console.trace(nsContextMenu);
console.trace(this.nsContextMenu);

console.log("AAAAAAAAAAAAAAA")
console.log("AAAAAAAAAAAAAAA2")
console.log("AAAAAAAAAAAAAAA3")
console.log("AAAAAAAAAAAAAAA4")
console.log("AAAAAAAAAAAAAAA5")
nsContextMenu.prototype.viewMedia = function viewMedia(e) {
	let where = whereToOpenLink(e, false, false);
	let referrerInfo = this.contentData.referrerInfo;
	let systemPrincipal = Services.scriptSecurityManager.getSystemPrincipal();
	if (this.onCanvas) {
		this._canvasToBlobURL(this.targetIdentifier).then(function(blobURL) {
			openUILinkIn(blobURL, where, {
				referrerInfo,
				triggeringPrincipal: systemPrincipal,
			});
		}, Cu.reportError);
	} else {
		urlSecurityCheck(
			this.mediaURL,
			this.principal,
			Ci.nsIScriptSecurityManager.DISALLOW_SCRIPT
		);

		openUILinkIn(this.mediaURL, where, {
			referrerInfo,
			forceAllowDataURI: true,
			triggeringPrincipal: this.principal,
			csp: this.csp,
		});
	}
};
// });
