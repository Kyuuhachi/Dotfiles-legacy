/* global Modules, MonkeyPatch, Renderer, SyncPromise */
/* exported ReactComponents */
"use strict";

const ReactComponents = (() => {
	const components = {};
	const listeners = {};
	const noNameComponents = new Set();
	const newNamedComponents = new Set();
	const nameSetters = {};

	const namesClushMessage = (oldName, newName) => `Several name setters for one component is detected! Old name is ${oldName}, new name is ${newName}. Only new name will be available as displayName, but all getters will resolve`;

	function put(component) {
		if(typeof component === "function") {
			const name = component.displayName;
			if(name) {
				if(!components[name]) {
					components[name] = component;
					if(listeners[name]) {
						listeners[name].forEach(f => f(component));
						delete listeners[name];
					}
					if(nameSetters[name])
						delete nameSetters[name];
				}
			} else if(!noNameComponents.has(component)) {
				for(const [name, filter] of Object.entries(nameSetters)) {
					if(filter(component)) {
						if(component.displayName)
							console.warn(namesClushMessage(component.displayName, name), component);

						component.displayName = name;
						delete nameSetters[name];
						put(component);
					}
				}
				(component.displayName ? newNamedComponents : noNameComponents).add(component);
			}
		}
	}

	function setName(name, filter) {
		if(!components[name])
			for(let component of noNameComponents)
				if(filter(component)) {
					component.displayName = name;
					noNameComponents.delete(component);
					newNamedComponents.add(component);
					put(component);
					break;
				}
		if(!components[name])
			for(let component of newNamedComponents)
				if(filter(component)) {
					console.warn(namesClushMessage(component.displayName, name), component);
					component.displayName = name;
					put(component);
					break;
				}
		if(!components[name])
			nameSetters[name] = filter;
		return get(name);
	}

	function get(name) { return new SyncPromise(resolve => {
		if(components[name]) {
			resolve(components[name]);
		} else {
			if(!listeners[name]) listeners[name] = [];
			listeners[name].push(resolve);
		}
	});}

	Modules.byFields("Component", "PureComponent", "Children", "createElement", "cloneElement")
		.then(React => MonkeyPatch(React, "createElement", { before: ({args:[c]}) => put(c) }));

	Renderer.doOnEachComponent(component => component.stateNode && put(component.stateNode.constructor));

	return {get, setName};
})();
