#!/usr/bin/env python3
from urllib.parse import urlparse

import i3bar.seg as s
import i3bar

i3bar.add(s.Clock())
i3bar.add(s.Apt())
i3bar.add(s.Temp())
i3bar.add(s.Battery())
i3bar.add(s.Network())
i3bar.add(s.Ram())
i3bar.add(s.CpuGraph())
i3bar.add(s.Volume())

i3bar.add(s.RSSFeed("MSPA", "http://mspaintadventures.com/rss/rss.xml"))
i3bar.add(s.RSSFeed("xkcd", "http://xkcd.com/rss.xml", seq=False))
i3bar.add(s.RSSFeed("what-if", "http://what-if.xkcd.com/feed.atom", seq=False))
i3bar.add(s.RSSFeed("Error'd", "http://syndication.thedailywtf.com/TheDailyWtf", seq=False, match=lambda e: e.category == "Error'd"))
i3bar.add(s.RSSFeed("SaW", "http://www.sandraandwoo.com/feed/", seq=False, match=lambda e: e.category == "Comics"))
i3bar.add(s.RSSFeed("EGS", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/index.php"))
i3bar.add(s.RSSFeed("EGS-NP", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/egsnp.php"))
i3bar.add(s.RSSFeed("GC", "http://www.gunnerkrigg.com/rss.xml"))
i3bar.add(s.RSSFeed("CQ", "http://cucumber.gigidigi.com/feed/"))
i3bar.add(s.RSSFeed("SD", "http://www.sdamned.com/feed/"))
i3bar.add(s.RSSFeed("AD", "http://feeds.feedburner.com/AvasDemon?format=xml"))
i3bar.add(s.RSSFeed("OotS", "http://www.giantitp.com/comics/oots.rss"))

# TODO add actual names
i3bar.add(s.FFNFeed("HPPK", 10870770)) # HP+Poke
i3bar.add(s.FFNFeed("HP20", 8096183)) # HP+DnD
i3bar.add(s.FFNFeed("FtA", 9173821)) # HP+Poke
i3bar.add(s.FFNFeed("WoD", 10604571)) # HP+Poke
i3bar.add(s.FFNFeed("MO", 10552390)) # HP+SAO
i3bar.add(s.FFNFeed("MKO", 11815818)) # HP+SAO
i3bar.add(s.FFNFeed("AEA", 11146312)) # HP+Poke
i3bar.add(s.FFNFeed("SA", 9236537)) # SAO+Poke
i3bar.add(s.FFNFeed("ISDSC", 10613753)) # HP+Poke
i3bar.add(s.FFNFeed("HPNFP", 2636963)) # HP
i3bar.add(s.FFNFeed("HPJI", 8914586)) # HP, Harry Potter: Junior Inquisitor
# i3bar.add(s.FFNFeed("CLV", 8730465)) # HP, C'est La Vie - gone?
i3bar.add(s.FFNFeed("EOL", 10972919)) # HP, The Evil Overlord List
i3bar.add(s.FFNFeed("HP&G", 11950816)) # HP, Harry Potter & the Game

i3bar.add(s.Totem())

i3bar.start()
