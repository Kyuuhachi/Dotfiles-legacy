import widgets
import widgets.ws

HEIGHT = 21

CSS = """
#fg { font-family: monospace; font-size: 9.5pt }
"""

def left():
	yield widgets.ws.Workspaces(widgets.ws.i3())

def right():
	yield widgets.Clock()
	yield widgets.IBus({"kkc": "日本語"})
	yield widgets.Battery("/sys/class/power_supply/BAT0", verbose=2)
	yield widgets.Temperature("coretemp-isa-0000", "Package id 0", 45)
	yield widgets.Wifi()
	yield widgets.RAM()
	yield widgets.CPUGraph()
	yield widgets.AlsaVolume()
