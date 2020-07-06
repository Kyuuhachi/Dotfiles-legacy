/* global ChromeUtils */
const {UrlbarInput} = ChromeUtils.import("resource:///modules/UrlbarInput.jsm", {});

UrlbarInput.prototype.handleRevert = function() {
	this.window.gBrowser.userTypedValue = null;
	this.setURI(null, true);
	this.blur();
};

UrlbarInput.prototype._maybeSelectAll = function() {};
