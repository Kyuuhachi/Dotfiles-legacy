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
add(Feed("Error'd", "http://syndication.thedailywtf.com/TheDailyWtf", seq=False, match=lambda e: e.title.startswith("Error'd:")))
add(Feed("Gaia", "http://www.sandraandwoo.com/gaia/feed/", match=lambda e: hasattr(e, "feedburner_origlink")))
add(Feed("SaW", "http://www.sandraandwoo.com/feed/", seq=False, match=lambda e: hasattr(e, "feedburner_origlink")))
add(Feed("PR", "http://www.praguerace.com/rss.php"))
add(Feed("EGS", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/index.php"))
add(Feed("EGS-NP", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/egsnp.php"))
add(Feed("GC", "http://www.gunnerkrigg.com/rss.xml"))
add(Feed("PN", "http://www.paranatural.net/rss.php"))
add(Feed("CQ", "http://cucumber.gigidigi.com/feed/"))
add(Feed("SD", "http://www.sdamned.com/feed/"))
add(Feed("AD", "http://feeds.feedburner.com/AvasDemon?format=xml"))
add(Feed("PQ", "http://www.prequeladventure.com/feed/"))
add(Feed("BC", "http://www.bigcrystals.net/feed/"))
add(Feed("BtC", "http://www.beyondthecanopy.com/feed/"))
add(Feed("MT", "http://megatokyo.com/rss/megatokyo.xml", match=lambda e: e.title.startswith("Comic")))
add(Feed("OotS", "http://www.giantitp.com/comics/oots.rss"))

add(FFNFeed("HPPK", 10870770))
add(FFNFeed("HP20", 8096183))

add(Totem())

start()
