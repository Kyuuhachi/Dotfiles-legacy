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

i3bar.add(s.Feeds([
	s.RSSFeed("MSPA", "http://mspaintadventures.com/rss/rss.xml"),
	s.RSSFeed("xkcd", "http://xkcd.com/rss.xml", seq=False),
	s.RSSFeed("what-if", "http://what-if.xkcd.com/feed.atom", seq=False),
	s.RSSFeed("Error'd", "http://syndication.thedailywtf.com/TheDailyWtf", seq=False, match=lambda e: e.category == "Error'd"),
	s.RSSFeed("SaW", "http://www.sandraandwoo.com/feed/", seq=False, match=lambda e: e.category == "Comics"),
	s.RSSFeed("EGS", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/index.php"),
	s.RSSFeed("EGS-NP", "http://www.egscomics.com/rss.php", match=lambda e: urlparse(e.link).path == "/egsnp.php"),
	s.RSSFeed("GC", "http://www.gunnerkrigg.com/rss.xml"),
	s.RSSFeed("CQ", "http://cucumber.gigidigi.com/feed/"),
	s.RSSFeed("SD", "http://www.sdamned.com/feed/"),
	s.RSSFeed("AD", "http://feeds.feedburner.com/AvasDemon?format=xml"),
	s.RSSFeed("OotS", "http://www.giantitp.com/comics/oots.rss"),
	s.RSSFeed("defan", "https://defan752.wordpress.com/feed/", seq=False, match=lambda e: e.category == "Sword Art Online"),

	s.FFNFeed("HPGTT", 10870770), # HP+Poke, Harry Potter and the Grand Trainer Tournament (changing)
	s.FFNFeed("HP20", 8096183), # HP+DnD, Harry Potter and the Natural 20
	s.FFNFeed("FtA", 9173821), # HP+Poke, From the Ashes
	s.FFNFeed("WoD", 10604571), # HP+Poke, On the Wings of Death
	s.FFNFeed("MO", 10552390), # HP+SAO, Magic Online
	s.FFNFeed("MKO", 11815818), # HP+SAO, Mystic Knight Online
	s.FFNFeed("AEA", 11146312), # HP+Poke, An Epic Adventure
	s.FFNFeed("SA", 9236537), # SAO+Poke, Soul Ablaze
	s.FFNFeed("HPNFP", 2636963), # HP, Harry Potter and the Nightmares of Futures Past
	s.FFNFeed("HPJI", 8914586), # HP, Harry Potter: Junior Inquisitor
	s.FFNFeed("HP&G", 11950816), # HP, Harry Potter & the Game
	s.FFNFeed("TBL", 2217186), # Poke, The Black Latios
	s.FFNFeed("LotCO", 11998973), # Poke, Loss of the Chosen One
	s.FFNFeed("DtM", 11923423), # Poke, Denki to Mizu (電気と水)
	s.FFNFeed("LoJ", 10364015), # Poke, Legends of Johto (changing)
]))

i3bar.add(s.MPD(dmenu_color="#00AF5F"))

i3bar.start()
