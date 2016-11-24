import i3bar
import configparser
import time

__all__ = ["Battery"]
class Battery(i3bar.Segment):
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
			battery[k.lower()[13:]] = val

		percent = 100 * battery["energy_now"] / battery["energy_full"]
		if battery.get("power_now", 0) > 0:
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
			if percent < 10:
				out["urgent"] = True
			return out
		else:
			return "⚡ {:.0f}%".format(percent)
