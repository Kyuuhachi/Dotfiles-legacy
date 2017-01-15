import i3bar
import i3bar.util
import subprocess

__all__ = ["Apt"]
class Apt(i3bar.util.Timer, i3bar.Segment):
	interval = 300

	updates = 0
	def run(self):
		output = subprocess.check_output(["aptitude", "search", "~U"])
		self.updates = len(output.splitlines())

	def getOutput(self):
		if self.updates == 0:
			return None
		return "Updates: {}".format(self.updates)

	def click(self, button, name):
		if button == 1:
			subprocess.Popen(["x-terminal-emulator", "-x", "sudo", "aptitude", "upgrade"])
			self.updates = 0
