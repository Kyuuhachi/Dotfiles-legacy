/* global webpackJsonp */
/* exported Modules  */
"use strict";

const Modules = (() => {
	const require = webpackJsonp([], {
		"__extra_id__": (module, exports, require) => exports.default = require
	}, ["__extra_id__"]).default;
	const {c:cache, m:modules} = require;
	delete modules["__extra_id__"];
	delete cache["__extra_id__"];

	const _byFields = (fields, module) => module && fields.every(f => module[f] !== undefined);
	const Filters = {
		byFields: (...fields) => (module) => _byFields(fields, module),
		byPrototypeFields: (...fields) => (module) => _byFields(fields, module.prototype),
		byCode: (search, selector = x => x) => (module) => {
			const method = selector(module);
			if(!method) return false;
			return method.toString().search(search) !== -1;
		},
	};

	function findMatching(filter) {
		for(let i in cache)
			if(cache.hasOwnProperty(i))
				try {
					let m = cache[i].exports;
					if(m && m.__esModule && m.default && filter(m.default))
						return m.default;
					if(m && filter(m))
						return m;
				} catch(e) {
					console.error(e);
				}
	}

	const callbacks = new Map();
	let timer = undefined;

	function updateCallbacks() {
		callbacks.forEach((callback, filter) => { // How convenient. The order is reversed.
			const module = findMatching(filter);
			if(module) {
				callback(module);
				callbacks.delete(filter);
			}
		});
		if(!callbacks.size)
			timer = clearInterval(timer);
	}

	function find(filter) {
		const module = findMatching(filter);
		let callback;
		const promise = new Promise(resolve => callback = resolve);
		if(module) callback(module);
		else {
			callbacks.set(filter, callback);
			if(!timer) timer = setInterval(updateCallbacks, 1000);
		}
		return promise;
	}

	const Modules = { find, Filters, require };

	for(const k in Filters)
		Modules[k] = (...arg) => Modules.find(Filters[k](...arg));

	return Modules;
})();
