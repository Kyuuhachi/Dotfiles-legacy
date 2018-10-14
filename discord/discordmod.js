/* eslint-env node */
"use strict";

let fs = require("fs");

function discordmod(win) {
	const cssFile = __dirname + "/discord.css";
	const cssSource = fs.readFileSync(cssFile, "utf8");
	win.webContents.executeJavaScript(`
	(()=>{
		let link = document.createElement("style");
		link.innerHTML=${JSON.stringify(cssSource)};
		document.head.appendChild(link);
	})();
	`);
}

module.exports = discordmod;
