#v.20191230.
# -*- coding: utf-8 -*-

import re, glob, os
from logging import getLogger, handlers, Formatter, StreamHandler, DEBUG
import argparse
import urllib.request
import urllib.parse
import http.cookiejar
import requests

class Urlutil:
	def __init__(self, url_ref = ""):
		self.ua = [
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		]
		self.setOpener(url_ref)

	def setOpener(self, url_ref):
		cookiejar = http.cookiejar.CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
		opener.addheaders = [('User-Agent', self.ua[0],)]
		opener.addheaders = [('Referer',url_ref)]
		urllib.request.install_opener(opener)

	def getSoup(self, url_soup):
		try:
			from bs4 import BeautifulSoup
		except Exception as e:
			logger.debug('BeautifulSoup import Err: ' + str(e))
			return None
		try:
			response = urllib.request.urlopen(url_soup)
		except Exception as e:
			logger.debug('getSoup: ' + url_soup + ': ' + str(e) + ': ' + response.text)
			return None
		html = response.read().decode('utf-8', errors='ignore')
		soup = BeautifulSoup(html, 'html.parser')
		return soup

	def findTag(self, soup, tag, attr = None, query = None):
		try:
			if attr is "href":
				pages = soup.find_all(tag, href=re.compile(query))
			elif attr is "src":
				pages = soup.find_all(tag, src=re.compile(query))
			elif attr is "class":
				pages = soup.find_all(tag, class_=re.compile(query))
			elif attr is "title":
				pages = soup.find_all(tag, title=re.compile(query))
			elif attr is "id":
				pages = soup.find_all(tag, id=re.compile(query))
			else:
				pages = soup.find_all(tag)
		except Exception as e:
			logger.debug('getSoup: ' + str(e))
			return None
		return pages

	def checkLink(self, url_ck):
		parse = urllib.parse.urlparse(url_ck)
		loc = parse.scheme + "://" + parse.netloc + "/"
		locs = []
		try:
			links = self.getSoup(url_ck, "a")
			for i in links:
				link = i.get("href")
				if re.compile("^\/").search(link):
					url = loc + link.replace('/','')
				elif not re.compile("^http").search(link):
					url = loc + link
				else:
					continue
				locs.append(url)
			return locs
		except Exception as e:
			logger.debug('checkLink: ' + str(e))
			return None

	def getTicket(self, url_page, url_wild):
		if os.path.dirname(url_page) in url_wild:
			url_wild = url_wild.replace(os.path.dirname(url_page) + "/", "")
		self.setOpener(url_page)
		soup = self.getSoup(url_page)
		pages = self.findTag(soup, "img", attr = "src", query = url_wild)
		for i in pages:
			print(i)

	def getImgs(self, url_page, path):
		self.setOpener(url_page)
		soup = self.getSoup(url_page)
		pages = self.findTag(soup, "img")
		for i in pages:
			if "http" in i["src"]:
				url_file = i["src"]
			else:
				url_file = os.path.dirname(url_page) + "/" + i["src"]
			download(url_file, path, os.path.basename(i["src"]))

	def postPass(self, url_post, params):
		#link = self.getSoup(url_post, "input", "type", "password")
		#for i in link:
		#       print(i)
		s = requests.Session()
		#params={'username':'user','password':'pass','mode':'login'}
		r = s.post(url_post, params=params)
		res = requests.get()
		with open(pwd + file_name, 'w') as f:
		       f.write(r.text)
		return r

def download(url_file, path, file_name):
	file_name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', file_name)
	if file_name[0] == "/":
		file_name = file_name[1:]
	if path[-1:] != "/":
		path = path + "/"
	if glob.glob(path + file_name + "*"):
		print(file_name + " exitsts.")
	try:
		urllib.request.urlretrieve(url_file, path + file_name)
	except Exception as e:
		logger.debug('download: ' + str(e))

def _help():
	print("""class
	Urlutil()
method
	setOpener(url_ref)      Build opener.
	getSoup(url)	      Return soup.
	findTag(soup, tag, attr = None, query = None)   Find tag,attr,search-query on soup.
	checkLink(url)	  Check local-link, return list.
	getTicket(url_page, url_wild)	Print Ticket-numbers.
	getImgs(url_page, path)		Download 'img's to path.
	postPass(url_post, params)	      Return response. eg, {'username':'user','password':'pass','mode':'login'}
function
	download(url, path, file_name)""")

def _logger():
	logger = getLogger(__name__)
	logger.setLevel(DEBUG)
	formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")
	handler_console = StreamHandler()
	handler_console.setLevel(DEBUG)
	handler_console.setFormatter(formatter)
	logger.addHandler(handler_console)
	handler_file = handlers.RotatingFileHandler(filename='./this.log',maxBytes=1048576,backupCount=3)
	handler_file.setFormatter(formatter)
	logger.addHandler(handler_file)
	logger.propagate = False
	return logger

def _parser():
	parser = argparse.ArgumentParser(
		usage="""python3 urlutil.py mode
	python3 urlutil.py
	python3 urlutil.py searchWord2Json [screen_name] --keyword '<search_word> --output <output_file>'""",
		add_help=True,
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument("mode", help="", type=str, metavar="[mode]")
	parser.add_argument("screen_name", help="", type=str, metavar="[screen_name]")
	parser.add_argument("--user_id", help="", type=int, metavar="<user_id>")
	parser.add_argument("--keyword", help="", type=str, nargs='*', metavar="'<keyword>'")
	parser.add_argument("--output", help="", type=str, metavar="'<output_file>'")
	return parser.parse_args()

def _main():
	cmd_args = _parser()
	obj = Urlutil()

if __name__ == '__main__':
	logger = _logger()
	_main()
else:
	logger = _logger()
	print("* Try 'urlutil.help()'.")
