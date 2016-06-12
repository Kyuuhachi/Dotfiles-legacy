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

			consumption = battery["power_now"] / 10**6

			if charging:
				remaining = battery["energy_full"] - battery["energy_now"]
			else:
				remaining = battery["energy_now"]
			remainingTime = time.strftime("%H:%M", time.gmtime(remaining / battery["power_now"] * 60**2))

			out = {}
			out["full_text"] = "⚡ {:.0f}% {}{:.2f}W ({})".format(percent, symbol, consumption, remainingTime)
			if percent < 10: out["urgent"] = True
			return out
		else:
			return "⚡ {:.0f}%".format(percent)
