/* exported MonkeyPatch */
"use strict";

const MonkeyPatch = (what, methodName, options) => {
	const {before, after, instead} = options;
	const origMethod = what[methodName];
	what[methodName] = function() {
		const data = {
			that: this,
			args: arguments,
			originalMethod: origMethod,
			call: () => data.ret = data.originalMethod.apply(data.that, data.args)
		};
		if(instead)
			return instead(data);
		else {
			if(before) before(data);
			data.call();
			if(after) after(data);
		}
		return data.ret;
	};
};
