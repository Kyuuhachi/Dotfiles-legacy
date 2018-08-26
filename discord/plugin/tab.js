/* global Modules, MonkeyPatch */
"use strict";

(async function() {
	let fakestr = s => s && ({replace: (pat, rep) => pat.source === "\\t" ? s : fakestr(s.replace(pat, rep)) });

	const fields = ["parse", "parseAllowLinks", "parseTopic", "parseEmbedTitle", "parseReturnTree"];
	let Parser = await Modules.byFields(...fields);
	fields.forEach(field => MonkeyPatch(Parser, field, { before: ({args}) => args[0] = fakestr(args[0]) }));
})();
