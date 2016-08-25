#!/usr/bin/env python3
# vim: foldmethod=marker

from urllib.parse import urlparse
import os, sys

import subprocess
# {{{ Bar
import i3py.bar
from i3py.bar.seg.clock import Clock
from i3py.bar.seg.apt import Apt
from i3py.bar.seg.temp import Temp
from i3py.bar.seg.battery import Battery
from i3py.bar.seg.ram import Ram
from i3py.bar.seg.network import Network
from i3py.bar.seg.cpugraph import CpuGraph
from i3py.bar.seg.volume import Volume
from i3py.bar.seg.totem import Totem
from i3py.bar.seg.feed import Feed
from i3py.bar.seg.feed import FFNFeed

i3py.bar.add(Clock())
i3py.bar.add(Apt())
i3py.bar.add(Temp())
i3py.bar.add(Battery())
i3py.bar.add(Network())
i3py.bar.add(Ram())
i3py.bar.add(CpuGraph())
i3py.bar.add(Volume())

i3py.bar.add(Feed("MSPA", "http://mspaintadventures.com/rss/rss.xml"))
i3py.bar.add(Feed("PXS", "http://paradoxspace.com/rss.atom"))
i3py.bar.add(Feed("xkcd", "http://xkcd.com/rss.xml", seq=False))
i3py.bar.add(Feed("what-if", "http://what-if.xkcd.com/feed.atom", seq=False))
i3py.bar.add(Feed("Error'd", "http://syndication.thedailywtf.com/TheDailyWtf", seq=False, match=lambda e: e.category == "Error'd"))
i3py.bar.add(Feed("Gaia", "http://www.sandraandwoo.com/gaia/feed/", match=lambda e: e.category == "Comic"))
i3py.bar.add(Feed("SaW", "http://www.sandraandwoo.com/feed/", seq=False, match=lambda e: e.category == "Comic"))
i3py.bar.add(Feed("EGS", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/index.php"))
i3py.bar.add(Feed("EGS-NP", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/egsnp.php"))
i3py.bar.add(Feed("GC", "http://www.gunnerkrigg.com/rss.xml"))
i3py.bar.add(Feed("CQ", "http://cucumber.gigidigi.com/feed/"))
i3py.bar.add(Feed("SD", "http://www.sdamned.com/feed/"))
i3py.bar.add(Feed("AD", "http://feeds.feedburner.com/AvasDemon?format=xml"))
i3py.bar.add(Feed("PQ", "http://www.prequeladventure.com/feed/"))
i3py.bar.add(Feed("BtC", "http://www.beyondthecanopy.com/feed/"))
i3py.bar.add(Feed("OotS", "http://www.giantitp.com/comics/oots.rss"))

#TODO add actual names
i3py.bar.add(FFNFeed("HPPK", 10870770)) #HP+Poke
i3py.bar.add(FFNFeed("HP20", 8096183)) #HP+DnD
i3py.bar.add(FFNFeed("FtA", 9173821)) #HP+Poke
i3py.bar.add(FFNFeed("WoD", 10604571)) #HP+Poke
i3py.bar.add(FFNFeed("MO", 10552390)) #HP+SAO
i3py.bar.add(FFNFeed("MKO", 11815818)) #HP+SAO
i3py.bar.add(FFNFeed("FDD", 8679666)) #SAO
i3py.bar.add(FFNFeed("AEA", 11146312)) #HP+Poke
i3py.bar.add(FFNFeed("SA", 9236537)) #SAO+Poke
i3py.bar.add(FFNFeed("ISDSC", 10613753)) #HP+Poke
i3py.bar.add(FFNFeed("HPNFP", 2636963)) #HP
i3py.bar.add(FFNFeed("HPJI", 8914586)) #HP, Harry Potter: Junior Inquisitor
i3py.bar.add(FFNFeed("CLV", 8730465)) #HP, C'est La Vie

i3py.bar.add(Totem())

i3py.bar.start()
# }}}
# {{{ Keybind
import i3py.keybind
from i3py.keybind import i3, run, mode
keys = {
	None: {
		"XF86_MonBrightnessUp":   run("xbacklight -inc 20 -time 0"),
		"XF86_MonBrightnessDown": run("xbacklight -dec 20 -time 0"),
		"XF86_AudioMute":         run("echo mute | nc -U /tmp/i3py"),
		"XF86_AudioRaiseVolume":  run("echo inc  | nc -U /tmp/i3py"),
		"XF86_AudioLowerVolume":  run("echo dec  | nc -U /tmp/i3py"),

		"w-Print":   run("scrot    '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),
		"w-s-Print": run("scrot -u '%Y-%m-%d_%H-%M-%S.png' -e 'mv $f ~/Screenshots'"),

		"w-Return": run("i3-sensible-terminal"),
		"w-d": run("dmenu_run"),
		"w-u": run("compose ~/dot/htmlent.txt"),

		"w-c": i3("reload"),
		"w-s-c": i3("restart"),
		"w-z": i3py.reload,
		"c-a-BackSpace": i3("exit"),

		"w-x": i3("kill"),
		"w-s-x": i3("focus parent;" * 10 + "kill"),

		"w-f": i3("fullscreen"),
		"w-a": i3("focus parent"),
		"w-s-a": i3("focus child"),
		"w-space": i3("focus mode_toggle"),
		"w-s-space": i3("floating toggle"),

		"w-r": mode("resize"),
	},
	"resize": {
		"<name>": "Resize",
		"w-s": i3("layout splith"),
		"w-v": i3("layout splitv"),
		"w-s-s": i3("layout stacking"),
		"w-s-t": i3("layout tabbed"),

		"h": i3("resize shrink width  10 px"),
		"j": i3("resize grow   height 10 px"),
		"k": i3("resize shrink height 10 px"),
		"l": i3("resize grow   width  10 px"),

		"s-h": i3("resize shrink width  1 px"),
		"s-j": i3("resize grow   height 1 px"),
		"s-k": i3("resize shrink height 1 px"),
		"s-l": i3("resize grow   width  1 px"),

		"Escape": mode(None)
	}
}
for n in range(1, 11):
	keys[None]["w-%d" % (n%10)] = i3("workspace %d" % n)
	keys[None]["w-s-%d" % (n%10)] = i3("move container to workspace %d; workspace %d" % (n, n))
for k, d in zip("hjkl", ["left", "down", "up", "right"]):
	keys[None]["w-%s" % k] = i3("focus %s" % d)
	keys[None]["w-s-%s" % k] = i3("move %s" % d)
del i3, run, mode
i3py.keybind.start(keys)
# }}}
