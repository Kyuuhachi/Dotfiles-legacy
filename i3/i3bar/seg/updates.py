import i3bar
import i3bar.util
import subprocess
import shlex
from collections import namedtuple

__all__ = ["Provider", "Updates", "Apt", "Pip", "Pacaur"]
Provider = namedtuple("Provider", "name check upgrade")

class Updates(i3bar.util.Timer, i3bar.Segment):
	interval = 3600

	def __init__(self, *providers):
		self.providers = providers
		self.updates = {p.name: 0 for p in providers}

	def run(self):
		for p in self.providers:
			try:
				out = subprocess.check_output(p.check, shell=True).decode()
				self.updates[p.name] = len(out.splitlines())
			except:
				pass

	def getOutput(self):
		out = []
		for p in self.providers:
			if self.updates[p.name]:
				out.append("%s: %d" % (p.name, self.updates[p.name]))
		return ", ".join(out) or None

	def click(self, button, name):
		if button == 1:
			cmd = []
			for p in self.providers:
				if self.updates[p.name]:
					cmd.append(p.upgrade)
					self.updates[p.name] = 0
			cmd.append("read")
			cmd = "; ".join(cmd)
			subprocess.Popen(["x-terminal-emulator", "-x", "sh", "-c", cmd])

Apt = Provider("Apt", "aptitude search ~U", "sudo aptitude upgrade")
Pacaur = Provider("Pacaur", "checkupdates; pacaur -Qu", "pacaur -Syu")
Pip = Provider("Pip", "pip list -o --format=freeze", "pip list -o --format=freeze | cut -d= -f1 | xargs sudo pip install -U")
