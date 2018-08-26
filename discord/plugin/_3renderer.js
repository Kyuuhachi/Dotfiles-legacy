/* global MonkeyPatch */
/* exported Renderer */
"use strict";

const Renderer = (() => {
	function getInternalInstance(e) { return e[Object.keys(e).find(k => k.startsWith("__reactInternalInstance"))]; }
	const reactRootInternalInstance = getInternalInstance(document.getElementById("app-mount").firstElementChild);

	function* recursiveComponents(instance=reactRootInternalInstance) {
		yield instance;
		if(instance.sibling)
			yield* recursiveComponents(instance.sibling);
		if(instance.child)
			yield* recursiveComponents(instance.child);
	}

	function doOnEachComponent(componentType, action) {
		for(const component of recursiveComponents())
			if(componentType == undefined || component.constructor == componentType || component.constructor.displayName == componentType)
				action(component);
	}

	function rebindMethods(component, ...methods) {
		function rebind(that) {
			for(let method of methods)
				that[method] = component.prototype[method].bind(that);
			that.forceUpdate();
		}
		doOnEachComponent(component, rebind);
		if(!component.prototype.componentWillMount) component.prototype.componentWillMount = ()=>{};
		MonkeyPatch(component.prototype, "componentWillMount", { after: ({that}) => { rebind(that); } });
	}

	return { recursiveComponents, doOnEachComponent, rebindMethods };
})();

