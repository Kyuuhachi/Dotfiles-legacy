import timeit as ti
import warnings

units = { "s": 1e0, "ms": 1e3, "μs": 1e6, "ns": 1e9 }

def timeit(func=None, /, **kwargs):
	unit = kwargs.pop("unit", "μs")
	if unit == "us": unit = "μs"
	if units not in units:
		warnings.warn(f"unknown unit {unit!r}, using μs")
		unit = "μs"

	globals = dict(kwargs.pop("globals", {}))

	num = kwargs.get("number", ti.default_number)

	def wrapper(func):
		t = ti.timeit(
			**kwargs,
			globals={**globals, "__func__": func},
			stmt="__func__()",
		) * units[unit] / num
		print(f"{func.__name__} execution avg: {t} {unit}")

	if func is None:
		return wrapper
	else:
		return wrapper(func)
