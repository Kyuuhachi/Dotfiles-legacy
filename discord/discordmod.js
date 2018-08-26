/* eslint-env node */
"use strict";

let fs = require("fs");

function discordmod(win) {
	const web = win.webContents;
	const plugindir = __dirname + "/plugin/";

	function execJS(str) {
		web.executeJavaScript(str);
	}
	function execCSS(str) {
		execJS(`
		(()=>{
			let link = document.createElement("style");
			link.innerHTML=${JSON.stringify(str)};
			document.head.appendChild(link);
		})();
		`);
	}
	if(!fs.existsSync(plugindir))
		fs.mkdirSync(plugindir);
	web.on("dom-ready", () => {
		fs.readdirSync(plugindir).forEach(name => {
			if(name.endsWith(".js"))  execJS(fs.readFileSync(plugindir + name, "utf8"));
			if(name.endsWith(".css")) execCSS(fs.readFileSync(plugindir + name, "utf8"));
		});
	});
}

module.exports = discordmod;
