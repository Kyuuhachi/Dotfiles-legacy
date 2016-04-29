import i3py
from i3py import util
import subprocess
import sys

class Apt(util.Timer, i3py.Segment):
	interval = 300

	updates = 0
	def run(self):
		output = subprocess.check_output(["aptitude", "search", "~U"])
		self.updates = len(output.splitlines())

	def getOutput(self):
		if self.updates == 0: return None
		return "Updates: %d" % self.updates
	
	def click(self, button):
		if button == 1:
			subprocess.Popen(["mate-terminal", "-x", "sudo", "aptitude"])
			self.updates = 0
