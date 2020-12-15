// ==UserScript==
// @name        HideCrapSearch
// @include     http*://duckduckgo.com/?*
// @include     http*://start.duckduckgo.com/?*
// @include     http*://safe.duckduckgo.com/?*
// @grant       none
// ==/UserScript==

/* global DDG */

function cleanup(results) {
	return results.filter(({u}) => !/^https?:\/\/docs.python.org\/2\//.test(u));
}

const origLoad = DDG.pageLayout.load;
DDG.pageLayout.load = function() {
	if(arguments[0] == "d")
		arguments[1] = cleanup(arguments[1]);
	origLoad.apply(this, arguments);
};
