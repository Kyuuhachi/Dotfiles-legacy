import i3py.bar
import i3py.util
import subprocess
import sys

class Apt(i3py.util.Timer, i3py.bar.Segment):
	interval = 300

	updates = 0
	def run(self):
		output = subprocess.check_output(["aptitude", "search", "~U"])
		self.updates = len(output.splitlines())

	def getOutput(self):
		if self.updates == 0: return None
		return "Updates: {}".format(self.updates)
	
	def click(self, button):
		if button == 1:
			subprocess.Popen(["mate-terminal", "-x", "sudo", "aptitude", "upgrade"])
			self.updates = 0
