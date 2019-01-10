from gi.repository import Gtk, Gdk
import util
import subprocess
import asyncio
import aiohttp
import aiosqlite

import configparser
from pathlib import Path
import bs4

icon = Gtk.IconTheme.get_default().load_icon("application-rss+xml", 16, 0)
iconGray = icon.copy()
iconGray.saturate_and_pixelate(iconGray, 0, False)

def clean_url(url):
	from urllib.parse import urlparse, urlunparse
	parse = urlparse(url)
	return urlunparse(parse._replace(netloc=parse.netloc.lower()))

def clean_all_urls(feed):
	name, url, items = feed
	return (name, clean_url(url), [(name, clean_url(url)) for (name, url) in items])

browser = lambda _, url: subprocess.Popen(["xdg-open", url])

class Feeds(Gtk.EventBox):
	def __init__(self, hist, feeds, spacing=3):
		super().__init__()

		self.icon = Gtk.Label("")
		self.text = Gtk.Label()
		box = Gtk.Box(spacing=spacing)
		box.pack_start(self.icon, False, False, 0)
		box.pack_start(self.text, False, False, 0)
		self.add(box)

		self.menu = Gtk.Menu(take_focus=False)
		util.popupify(self.menu.get_parent(), self)

		(self.sql_path, self.sql_query) = hist

		self.imgs = []

		self.event_fetch = asyncio.Event()
		self.event_hist = asyncio.Event()

		menus, feeds = self.build_top_menu(self.menu, feeds)
		asyncio.ensure_future(self.run(menus, feeds))
		asyncio.ensure_future(self.update_hist())

		popup = lambda: self.menu.popup_at_widget(self, Gdk.Gravity.NORTH, Gdk.Gravity.SOUTH)
		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect("button-press-event", lambda _, e: (e.type, e.button) == (Gdk.EventType.BUTTON_PRESS, 1) and popup())
		self.connect("button-press-event", lambda _, e: (e.type, e.button) == (Gdk.EventType.BUTTON_PRESS, 2) and self.event_fetch.set())

	async def run(self, menus, feeds):
		async def load_feed(session, feed):
			async with session.get(feed.url) as response:
				return feed(await response.read())

		assert len(feeds) == len(menus)

		async with aiohttp.ClientSession() as session:
			while True:
				feeds_ = await asyncio.gather(*(load_feed(session, feed) for feed in feeds), return_exceptions=True)
				self.imgs = []
				for menu, feed in zip(menus, feeds_):
					if isinstance(feed, BaseException):
						util.print_exc(feed)
						menu.set_tooltip_text(f"{type(feed).__name__}: {feed}")
						menu.set_image(None)
						menu.set_submenu(None)
					else:
						menu.set_tooltip_text(None)
						submenu, img = self.build_menu(clean_all_urls(feed))
						menu.set_image(img)
						menu.set_submenu(submenu)

				self.event_hist.set()
				await asyncio.wait([self.event_fetch.wait()], timeout=60*60)
				self.event_fetch.clear()

	async def update_hist(self):
		async with aiosqlite.connect(self.sql_path) as db:
			while True:
				urls = {url for img, url, top in self.imgs}
				query = self.sql_query.format(",".join("?" for _ in urls))
				visited = set()

				cursor = await db.cursor()
				await cursor.execute(query, list(urls))
				for (url,) in await cursor.fetchall():
					visited.add(url)

				num = 0
				for img, url, top in self.imgs:
					if url in visited:
						img.set_from_pixbuf(iconGray)
					else:
						img.set_from_pixbuf(icon)
						num += top

				self.set_opacity(0.5 if not num else 1)
				self.text.set_text(str(num))
				self.text.set_visible(bool(num))

				await asyncio.wait([self.event_hist.wait()], timeout=5)
				self.event_hist.clear()

	def build_top_menu(self, menu, feeds):
		menus = []
		feeds2 = []
		for feed in feeds:
			if feed is None:
				menu.add(Gtk.SeparatorMenuItem(visible=True))
				continue
			menuitem = Gtk.ImageMenuItem(label=feed.name, always_show_image=True, visible=True)
			menu.add(menuitem)
			menus.append(menuitem)
			feeds2.append(feed)
		return menus, feeds2

	def build_menu(self, feed):
		img = Gtk.Image()
		if feed[2]:
			self.imgs.append((img, feed[2][0][1], True))
		menu = Gtk.Menu()
		menuitem = Gtk.MenuItem(label=feed[0])
		menuitem.connect("activate", browser, feed[1])
		menu.add(menuitem)
		menu.add(Gtk.SeparatorMenuItem())
		for e in feed[2]:
			img2 = Gtk.Image()
			mitem = Gtk.ImageMenuItem(label=e[0], always_show_image=True, image=img2)
			mitem.connect("activate", browser, e[1])
			self.imgs.append((img2, e[1], False))
			menu.add(mitem)
		menu.show_all()
		return menu, img

class Feed:
	def __init__(self, name, url, max=20):
		self.name = name
		self.url = url
		self.funcs = []
		self.max = max

	def __call__(self, data):
		feed = self.load(data)
		[f(feed) for f in self.funcs]
		return (feed[0], feed[1], feed[2][:self.max])
	def load(self, data): raise NotImplementedError()

	def map(self, f):
		self.funcs.append(f)
		return self

class RSSFeed(Feed):
	def __init__(self, name, url, **kwargs):
		super().__init__(name, url, **kwargs)
		self.prefuncs = []

	def load(self, data):
		feed = parse_rss(data)
		[f(feed) for f in self.prefuncs]
		return (feed.title, feed.link, [(e.title, e.link) for e in feed.entries])

	def premap(self, func):
		self.prefuncs.append(func)
		return self

#{{{1 RSS parsing
class _RSSObj:
	__SLOTS__ = ["data", "junk"]
	def __init__(self, data, junk):
		super().__setattr__("data", data)
		super().__setattr__("junk", junk)
	def __getitem__(self, k):
		return self.junk[k]
	def __setitem__(self, k, v):
		self.junk[k] = v
	def __contains__(self, k):
		return k in self.junk
	def __getattr__(self, k):
		return self.data[k]
	def __setattr__(self, k, v):
		self.data[k] = v
	def __hasattr__(self, k):
		return k in self.data
	def __repr__(self):
		return f"{type(self).__name__}({self.data}, {self.junk})"
class _RSSFeed(_RSSObj):
	__SLOTS__ = ["entries"]
	def __init__(self, data, junk, entries):
		super().__init__(data, junk)
		super().__setattr__("entries", entries)
	def __repr__(self):
		return f"_RSSFeed({self.data}, {self.entries}, {self.junk})"

class _RSSEntry(_RSSObj): pass

def parse_rss(source):
	from lxml import etree
	def feedparse(elem, data, junk):
		qn = etree.QName(elem.tag)
		elem.getparent().remove(elem)
		elem.tag = qn.localname
		etree.cleanup_namespaces(elem)
		if qn.namespace is None and not len(elem):
			if elem.tag in data:
				if isinstance(data[elem.tag], list):
					data[elem.tag].append(elem.xpath("string()"))
				else:
					raise ValueError(f"'{elem.tag}' already exists!")
			else:
				data[elem.tag] = elem.xpath("string()")
		else:
			junk.setdefault(qn.namespace, [])
			junk[qn.namespace].append(elem)

	xml = etree.fromstring(source, etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True))
	assert xml.tag == "rss"
	assert xml.get("version") == "2.0"
	assert len(xml) == 1
	channel = xml[0]
	assert channel.tag == "channel"
	data = {}
	junk = {}
	entries = []
	for elem in channel:
		if etree.iselement(elem):
			if elem.tag == "item":
				edata = {"category": []}
				ejunk = {}
				for item in elem:
					if etree.iselement(item):
						feedparse(item, edata, ejunk)
				entries.append(_RSSEntry(edata, ejunk))
			else:
				feedparse(elem, data, junk)
	return _RSSFeed(data, junk, entries)
#}}}1

class FFNFeed(Feed):
	def __init__(self, name, id, **kwargs):
		super().__init__(name, "https://www.fanfiction.net/s/{}".format(id), **kwargs)

	def load(self, data):
		soup = bs4.BeautifulSoup(data, features="lxml")
		title = soup.find(id="profile_top").find("b").text
		urlname = soup.find("link", rel="canonical")["href"].split("/")[-1]
		chap_select = soup.find(id="chap_select")
		if chap_select is not None:
			chapters = [(opt["value"], opt.text) for opt in chap_select.find_all("option")][::-1]
		else:
			chapters = [(1, "Only chapter")]

		return (title, self.url, [
			(text, f"{self.url}/{idx}/{urlname}")
			for (idx, text) in chapters
		])

def Firefox(profile=None):
	FF_PATH = Path("~/.mozilla/firefox").expanduser()

	ini = configparser.ConfigParser()
	ini.read(FF_PATH / "profiles.ini")

	if profile is not None:
		profile = ini[profile]
	else:
		for sec in ini:
			if "default" in ini[sec]:
				profile = ini[sec]

	sql = str(FF_PATH / profile["path"] / "places.sqlite")
	query = "SELECT url FROM moz_places WHERE url IN ({})"
	return sql, query

def Luakit(path=None):
	sql = str(Path("~/.local/share/luakit/history.db" if path is None else path).expanduser())
	query = "SELECT uri FROM history WHERE uri IN ({})"
	return sql, query
