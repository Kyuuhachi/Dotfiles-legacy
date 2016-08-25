#!/usr/bin/env python3

from urllib.parse import urlparse
from i3py import add, start
from i3py.seg.clock import Clock
from i3py.seg.apt import Apt
from i3py.seg.temp import Temp
from i3py.seg.battery import Battery
from i3py.seg.ram import Ram
from i3py.seg.network import Network
from i3py.seg.cpugraph import CpuGraph
from i3py.seg.volume import Volume
from i3py.seg.totem import Totem

add(Clock())
add(Apt())
add(Temp())
add(Battery())
add(Network())
add(Ram())
add(CpuGraph())
add(Volume())

from i3py.seg.feed import Feed
from i3py.seg.feed import FFNFeed

add(Feed("MSPA", "http://mspaintadventures.com/rss/rss.xml"))
add(Feed("PXS", "http://paradoxspace.com/rss.atom"))
add(Feed("xkcd", "http://xkcd.com/rss.xml", seq=False))
add(Feed("what-if", "http://what-if.xkcd.com/feed.atom", seq=False))
add(Feed("Error'd", "http://syndication.thedailywtf.com/TheDailyWtf", seq=False, match=lambda e: e.category == "Error'd"))
add(Feed("Gaia", "http://www.sandraandwoo.com/gaia/feed/", match=lambda e: e.category == "Comic"))
add(Feed("SaW", "http://www.sandraandwoo.com/feed/", seq=False, match=lambda e: e.category == "Comic"))
add(Feed("EGS", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/index.php"))
add(Feed("EGS-NP", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/egsnp.php"))
add(Feed("GC", "http://www.gunnerkrigg.com/rss.xml"))
add(Feed("CQ", "http://cucumber.gigidigi.com/feed/"))
add(Feed("SD", "http://www.sdamned.com/feed/"))
add(Feed("AD", "http://feeds.feedburner.com/AvasDemon?format=xml"))
add(Feed("PQ", "http://www.prequeladventure.com/feed/"))
add(Feed("BtC", "http://www.beyondthecanopy.com/feed/"))
add(Feed("OotS", "http://www.giantitp.com/comics/oots.rss"))

#TODO add actual names
add(FFNFeed("HPPK", 10870770)) #HP+Poke
add(FFNFeed("HP20", 8096183)) #HP+DnD
add(FFNFeed("FtA", 9173821)) #HP+Poke
add(FFNFeed("WoD", 10604571)) #HP+Poke
add(FFNFeed("MO", 10552390)) #HP+SAO
add(FFNFeed("MKO", 11815818)) #HP+SAO
add(FFNFeed("FDD", 8679666)) #SAO
add(FFNFeed("AEA", 11146312)) #HP+Poke
add(FFNFeed("SA", 9236537)) #SAO+Poke
add(FFNFeed("ISDSC", 10613753)) #HP+Poke
add(FFNFeed("HPNFP", 2636963)) #HP
add(FFNFeed("HPJI", 8914586)) #HP, Harry Potter: Junior Inquisitor
add(FFNFeed("CLV", 8730465)) #HP, C'est La Vie

add(Totem())

start()
