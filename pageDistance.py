import urllib.request as urlr
import urllib.parse as urlp
import re
import queue
from html.parser import HTMLParser

class Page:
	def __init__(self, url, level, parent):
		self.url = url
		self.links = []
		self.level = level
		self.reachable = True
		self.parent = parent

	def addLink(link):
		self.links.append(link)

class myHTMLParser(HTMLParser):
	def __init__(self, baseurl, output_list = None):
		HTMLParser.__init__(self)
		self.baseurl = baseurl
		if output_list is None:
			self.output_list = []
		else:
			self.output_list = output_list
	def handle_starttag(self, tag, attrs):
		if tag == "a":
			rel = (dict(attrs).get("href"))
			self.output_list.append(urlp.urljoin(self.baseurl, rel))

def crawl(page, visited, limit, queue, found):
	print("Crawling at " + page.url)
	try:
		text = str(urlr.urlopen(page.url).read())
	except:
		print(page.url + " is currently unreachable")
		page.reachable = False
		return
	if "georgia" in text.lower():
		print("Georgia has been found on " + page.url + " at a level of " + str(page.level))
		print("Path: ")
		pathPage = page
		while (pathPage.parent != None):
			print(pathPage.parent.url)
			pathPage = pathPage.parent
		return True
	parser = myHTMLParser(page.url)
	parser.feed(text)
	links = parser.output_list
	for link in links:
		if link not in visited:
			newPage = Page(link, page.level + 1, page)
			visited[link] = newPage
			if newPage.level <= limit:
				queue.put(newPage)

visited = {}
queue = queue.Queue()
start = Page(input("Please input a starting url: "), 0, None)
queue.put(start)
found = False
while not queue.empty() and not found:
	if crawl(queue.get(), visited, 5, queue, found) == True:
		found = True
if not found:
	print("Georgia was never found!")
