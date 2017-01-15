import pkgutil

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__): # noqa F821; __path__ sure does exist
	module = loader.find_module(name).load_module(name)
	for key in module.__all__:
		globals()[key] = getattr(module, key)
		__all__.append(key)
