import i3bar
import subprocess
import re

_input_re = re.compile(r"^  temp\d+_input: (\d+\.\d+)$")
_max_re = re.compile(r"^  temp\d+_max: (\d+\.\d+)$")
_crit_re = re.compile(r"^  temp\d+_crit: (\d+\.\d+)$")

__all__ = ["Temp"]
class Temp(i3bar.Segment): # TODO use psutil
	def __init__(self, chip, which, idle, crit=None):
		self.chip = chip
		self.which = which
		self.idle = idle
		self.crit = crit

	def getOutput(self):
		out = subprocess.check_output(["sensors", "-uA", self.chip]).decode().splitlines()[1:]
		temp = None
		crit = self.crit
		for line in out:
			if line.endswith(":"):
				which = line[:-1]
			elif which == self.which:
				if not temp:
					_input = _input_re.match(line)
					if _input:
						temp = float(_input.group(1))
				if not crit:
					_max = _max_re.match(line)
					if _max:
						crit = float(_max.group(1))
				if not crit:
					_crit = _crit_re.match(line)
					if _crit:
						crit = float(_crit.group(1))

		fill = min(1, (temp-self.idle)/(crit-self.idle))
		i3bar.log((temp-self.idle), (crit-self.idle))
		text = "{}{:.0f}°C".format([" ", " ", " ", " ", " "][int(4*min(1, max(0, fill)))], temp)
		return {
			"full_text": text,
			"urgent": crit and temp > crit
		}
