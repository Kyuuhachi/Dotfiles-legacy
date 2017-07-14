import i3bar
import os.path
import time

__all__ = ["Battery"]
class Battery(i3bar.Segment):
	def __init__(self, path):
		self.path = os.path.join(path, "uevent")

	def getOutput(self):
		battery = BatteryStatus(self.path)
		charge = battery.energy_now / battery.energy_full
		text = "{}{:.0f}%".format([" ", " ", " ", " ", " "][min(int(charge * 5), 4)], 100 * charge)

		if abs(battery.current) > 0.01:
			charging = battery.status == "Charging"
			symbol = {"Charging": "↑", "Discharging": "↓"}.get(battery.status, "")

			if charging:
				remaining = battery.energy_full - battery.energy_now
			else:
				remaining = battery.energy_now
			remainingTime = time.strftime("%H:%M", time.gmtime(remaining / battery.current * 60**2))
			text += " {}{:.2f}W ({})".format(symbol, battery.current, remainingTime)

		out = {}
		out["full_text"] = text
		if charge < 0.105: # Rounding
			out["urgent"] = True
		return out

class BatteryStatus:
	def __init__(self, path):
		import configparser
		cfg = configparser.ConfigParser()
		with open(path, "r") as f:
			cfg.read_string("[_]\n" + f.read())
		battery = {}
		for k in cfg["_"]:
			val = cfg["_"][k]
			try:
				val = int(val)
			except ValueError:
				pass
			battery[k.lower()[13:]] = val
		def get(*props):
			for prop in props:
				if prop in battery:
					return battery[prop]
			return None

		self.status = get("status")
		self.energy_now = get("energy_now", "charge_now") / 1000000
		self.energy_full = get("energy_full", "charge_full") / 1000000
		self.current = get("power_now", "current_now") / 1000000
