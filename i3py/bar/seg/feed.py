import i3py.bar
import i3py.util

import os.path
import configparser
from urllib.parse import urlparse, urlunparse
import sqlite3
import feedparser
import re

def getProfilePath():
	FF_PATH = os.path.expanduser("~/.mozilla/firefox")

	ini = configparser.ConfigParser()
	ini.read(FF_PATH + "/profiles.ini")

	for sec in ini:
		if "default" in ini[sec]:
			return FF_PATH + "/" + ini[sec]["path"]

def cleanUrls(urls):
	""" FF's history stores domains in lowercase. Some feeds (OotS) don't. """
	for url in urls:
		parse = urlparse(url)
		yield urlunparse(parse._replace(netloc=parse.netloc.lower()))

def hist(urls):
	urls = list(cleanUrls(urls))
	with sqlite3.connect(getProfilePath() + "/places.sqlite") as sql:
		cur = sql.cursor()
		query = "SELECT url FROM moz_places WHERE url IN ({})".format(",".join("?" for a in range(len(urls))))
		cur.execute(query, urls)
		rows = cur.fetchall()
		hist = [row[0] for row in rows]
		return [(url, url in hist) for url in urls]

class Feed(i3py.util.Timer, i3py.bar.Segment):
	interval = 3600

	link = None
	entries = []
	mainPage = None

	def __init__(self, name, url, seq=True, match=lambda e: True):
		self.name = name
		self.url = url
		self.seq = seq
		self.match = match

	def run(self):
		parser = feedparser.parse(self.url)
		self.entries = []
		for e in parser.entries:
			if hasattr(e, "feedburner_origlink"):
				e.link = e.feedburner_origlink
			if self.match(e):
				self.entries.append(e.link)

		if hasattr(parser.feed, "link"):
			self.mainPage = parser.feed.link
		else:
			self.mainPage = self.url

	def check(self):
		visited = hist(self.entries)
		i = -1
		for (link, vis) in visited:
			if vis: break
			i += 1

		if i == -1:
			self.output = None
			self.link = None
		else:
			if self.seq:
				i += 1
			if i >= len(visited):
				self.link = self.mainPage
			else:
				self.link = visited[i][0]

	def getOutput(self):
		self.check()
		return self.name if self.link else None

	def click(self, button):
		import webbrowser
		self.check()
		if button == 1 and self.link: #Left
			webbrowser.open(self.link)
		if button == 2 and self.mainPage: #Mid
			webbrowser.open(self.mainPage)
		if button == 3 and self.url: #Right
			webbrowser.open(self.url)

import lxml.html
from urllib.request import urlopen
class FFNFeed(Feed):
	def __init__(self, name, id, seq=True):
		self.name = name
		self.id = id
		self.seq = seq
		self.url = "https://www.fanfiction.net/s/{}".format(id)
		self.mainPage = self.url

	def run(self):
		tree = lxml.html.parse(urlopen(self.url))
		chap_select = tree.xpath("//select[@id='chap_select']")[0]
		name = chap_select.get("onchange").split()[-1][2:-2]
		self.entries = ["{}/{}/{}".format(self.url, opt.get("value"), name) for opt in chap_select.xpath("./option")[::-1]]

