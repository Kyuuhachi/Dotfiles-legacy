/* global ChromeUtils */
/* exported EXPORTED_SYMBOLS */
"use strict";
const EXPORTED_SYMBOLS = [];

const { UrlbarInput } = ChromeUtils.import("resource:///modules/UrlbarInput.jsm");

UrlbarInput.prototype.handleRevert = function() {
	this.window.gBrowser.userTypedValue = null;
    this.searchMode = null;
	this.setURI(null, true);
	this.blur();
};

UrlbarInput.prototype._maybeSelectAll = function() {};
