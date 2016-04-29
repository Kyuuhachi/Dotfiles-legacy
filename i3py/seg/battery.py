import i3py
import configparser
from types import SimpleNamespace
import time

class Battery(i3py.Segment):
	file = "/sys/class/power_supply/BAT0/uevent"

	def getOutput(self):
		cfg = configparser.ConfigParser()
		with open(self.file, "r") as f:
			cfg.read_string("[_]\n" + f.read())
		battery = {}
		for k in cfg["_"]:
			val = cfg["_"][k]
			try:
				val = int(val)
			except ValueError:
				pass
			battery[k.lower()[13:]] = val;

		percent = 100 * battery["energy_now"] / battery["energy_full"]
		if "power_now" in battery and battery["power_now"] > 0:
			charging = battery["status"] == "Charging"
			symbol = "↑" if charging else "↓"

			cons = battery["power_now"] / 10**6
			remaining = battery["energy_now"]
			if charging: remaining = battery["energy_full"] - remaining
			remaining = remaining / battery["power_now"] * 60**2
			remainingTime = time.strftime("%H:%M", time.gmtime(remaining))

			text = "⚡ %.0f%% %s%.2fW (%s)" % (percent, symbol, cons, remainingTime)
			out = {}
			out["full_text"] = text
			if percent < 10: out["urgent"] = True
			return out
		else:
			return "⚡ %.0f%%" % percent
