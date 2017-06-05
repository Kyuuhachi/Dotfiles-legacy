import i3bar
import time

__all__ = ["Battery"]
class Battery(i3bar.Segment):
	file = "/sys/class/power_supply/BAT0/uevent"

	def getOutput(self):
		battery = BatteryStatus(self.file)
		charge = battery.energy_now / battery.energy_full
		text = "⚡ {:.0f}%".format(100 * charge)

		if battery.consumption:
			charging = battery.status == "Charging"
			symbol = {"Charging": "↑", "Discharging": "↓"}.get(battery.status, "")

			if charging:
				remaining = battery.energy_full - battery.energy_now
			else:
				remaining = battery.energy_now
			remainingTime = time.strftime("%H:%M", time.gmtime(remaining / battery.consumption * 60**2))
			text += " {}{:.2f}W ({})".format(symbol, battery.consumption, remainingTime)

		out = {}
		out["full_text"] = text
		if charge < 0.15: # Rounding
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
		self.consumption = get("power_now") / 1000000

