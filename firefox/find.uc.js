/* global gBrowser */
gBrowser.tabContainer.addEventListener("TabFindInitialized", e => {
	console.log(e.target);
	console.log(e.target._findBar);
	let findbar = e.target._findBar;
	findbar._finishFAYT = function(e) {
		this.browser.finder.focusContent();
		e && e.preventDefault();
		this.close();
		return true;
	};
	findbar.findMode = 1;
	findbar._findField.addEventListener("keypress", e => {
		if(!e.altKey && e.ctrlKey && !e.metaKey && !e.shiftKey) {
			if(e.key == "i") { findbar.getElement("find-case-sensitive").click(); e.preventDefault(); }
			if(e.key == "b") { findbar.getElement("find-entire-word").click(); e.preventDefault(); }
			if(e.key == "e") { findbar.getElement("find-match-diacritics").click(); e.preventDefault(); }
			if(e.key == "h") { findbar.getElement("highlight").click(); e.preventDefault(); }
		}
	});
});
