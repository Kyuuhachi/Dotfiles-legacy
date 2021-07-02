import os.path

def prop(name):
	def getter(self):
		return self.uevent[name]
	getter.__name__ = name
	return property(getter)
def prop_int(name, xps=None):
	def getter(self):
		if xps is not None and xps in self.uevent:
			return int(self.uevent[xps]) / 100000
		if name in self.uevent:
			return int(self.uevent[name]) / 1000000
		return 0
	getter.__name__ = name
	return property(getter)

class BatteryStatus:
	__slots__ = ["uevent"]
	def __init__(self, path):
		self.uevent = {}
		with open(os.path.join(path, "uevent"), "r") as f:
			for line in f.read().splitlines():
				assert line.startswith("POWER_SUPPLY_")
				k, v = line[13:].split("=", 1)
				self.uevent[k.lower()] = v

	status = prop("status")
	energy_now = prop_int("energy_now", xps="charge_now")
	energy_full = prop_int("energy_full", xps="charge_full")
	energy_design = prop_int("energy_full_design", xps="charge_full_design")
	current_ = prop_int("power_now", xps="current_now")
	voltage_now = prop_int("voltage_now")
	voltage_design = prop_int("voltage_min_design")
	@property
	def discharging(self):
		return self.status == "Discharging"
	@property
	def current(self):
		if self.discharging:
			return -self.current_
		return self.current_
	@property
	def remaining(self):
		if self.discharging:
			remaining = self.energy_now
		else:
			remaining = self.energy_full - self.energy_now
		return remaining / abs(self.current) * 3600
del prop
del prop_int
