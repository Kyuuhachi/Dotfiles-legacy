"use strict";

addMessageListener("kitsune@unfocus", () => {
	content.document.activeElement.blur();
});

{
	let links = null;
	let linkselector = `input:not([type=hidden]), a, area, iframe, textarea, button, select, summary,
	[onclick], [onmouseover], [onmousedown], [onmouseup], [oncommand], [role='link'], [role='button'], [role='checkbox'],
	[role='combobox'], [role='listbox'], [role='listitem'], [role='menuitem'], [role='menuitemcheckbox'],
	[role='menuitemradio'], [role='option'], [role='radio'], [role='scrollbar'], [role='slider'], [role='spinbutton'],
	[role='tab'], [role='textbox'], [role='treeitem'], [tabindex]`

	addMessageListener("kitsune@link_start", () => {
		let n = 0;
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
		sendAsyncMessage("kitsune@link_show", boxes);
	});

	addMessageListener("kitsune@link_click", ({data: id}) => {
		let link = links[id];

		if(!link) return; // Shouldn't happen, but no promises
		link.focus();
		link.click();
	});
}
