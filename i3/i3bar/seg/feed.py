import i3bar
import i3bar.util
from urllib.request import urlopen
import threading

__all__ = ["Feeds", "RSSFeed", "FFNFeed"]

class Feeds(i3bar.Segment):
	interval = 3600

	def __init__(self, feeds):
		self.names = [feed.name for feed in feeds]
		self.feeds = {feed.name: feed for feed in feeds}
		self.entries = {k: {} for k in self.names}
		self.latest = {k: None for k in self.names}
		self.fetchTimer = i3bar.util.Timer(60 * 60, self.fetchFeeds, "fetchFeeds")
		self.checkTimer = i3bar.util.Timer(5, self.checkHistory, "checkHistory")

	def start(self):
		self.fetchTimer.start()
		self.checkTimer.start()

	def fetchFeeds(self):
		def clean_url(url):
			from urllib.parse import urlparse, urlunparse
			parse = urlparse(url)
			return urlunparse(parse._replace(netloc=parse.netloc.lower()))

		@i3bar.util.OtherThread
		def download(feed):
			threading.current_thread().name = feed.name
			urls = feed.load_feed(urlopen(feed.url))
			self.entries[feed.name] = [clean_url(url) for url in urls]
		for name in self.names:
			download(self.feeds[name])

	def checkHistory(self):
		entries = dict(self.entries) # Don't update while we're working
		urls = []
		for name in self.names:
			urls += entries[name]
		visited = hist(urls)

		for name in self.names:
			i = -1
			for url in entries[name]:
				if url in visited:
					break
				i += 1

			if i == -1:
				self.latest[name] = None
			else:
				if self.feeds[name].seq:
					i += 1
				if i >= len(entries[name]):
					self.latest[name] = self.feeds[name].url
				else:
					self.latest[name] = entries[name][i]

	def getOutput(self):
		for name in self.names:
			if self.latest[name] is not None:
				yield {"full_text": name, "name": name}

	def click(self, button, name):
		import webbrowser
		if button == 1 and self.latest[name]:
			webbrowser.open(self.latest[name])
		if button == 3 and self.feeds[name].url:
			webbrowser.open(self.feeds[name].url)

class RSSFeed:
	def __init__(self, name, url, seq=True, match=lambda e: True):
		self.name = name
		self.url = url
		self.seq = seq
		self._match = match

	def load_feed(self, data):
		import feedparser
		parser = feedparser.parse(data)
		entries = []
		for e in parser.entries:
			if hasattr(e, "feedburner_origlink"):
				e.link = e.feedburner_origlink
			if self._match(e):
				entries.append(e.link)
		return entries

class FFNFeed:
	def __init__(self, name, id, seq=True):
		self.name = name
		self.url = "https://www.fanfiction.net/s/{}".format(id)
		self.seq = seq

	def load_feed(self, data):
		import bs4
		soup = bs4.BeautifulSoup(data, features="lxml")
		chap_select = soup.find(id="chap_select")
		name = chap_select["onchange"].split()[-1][2:-2]
		entries = ["{}/{}/{}".format(self.url, opt.get("value"), name) for opt in chap_select.find_all("option")[::-1]]
		return entries

def hist(urls):
	import os.path
	import sqlite3
	import configparser

	def getProfilePath(): # TODO cache?
		FF_PATH = os.path.expanduser("~/.mozilla/firefox")

		ini = configparser.ConfigParser()
		ini.read(FF_PATH + "/profiles.ini")

		for sec in ini:
			if "default" in ini[sec]:
				return FF_PATH + "/" + ini[sec]["path"]

	with sqlite3.connect(getProfilePath() + "/places.sqlite") as sql:
		cur = sql.cursor()
		query = "SELECT url FROM moz_places WHERE url IN ({})".format(",".join(["?"] * len(urls)))
		cur.execute(query, urls)
		rows = cur.fetchall()
		return set(row[0] for row in rows)
