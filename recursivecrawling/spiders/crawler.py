from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from recursivecrawling.items import RecursivecrawlingItem
from scrapy.http import Request
import re
import urlparse
import ast

class MySpider(BaseSpider):
	name = "ReverseCrawler" 

	def __init__(self, domain=None, start_urls=None, cookies=None):
       		self.allowed_domains = [domain]
        	self.start_urls = [start_urls]
        	self.cookies = {}
        	if cookies: 
        	    self.cookies = ast.literal_eval(cookies)
        	self.listOfCrawledLinks = []
		self.FormItem = []
		self.crawledURLs = open("crawledURLs.txt","w")
	
	def start_requests(self):
	        return [Request(url=self.start_urls[0], cookies=self.cookies, callback=self.parse1)]

	def parse1(self, response):		
  		hxs = HtmlXPathSelector(response)	
 		links = hxs.select("//a/@href").extract()
		forms = hxs.select("//form")
		scripts = hxs.select("//script/text()").extract()
		self.FormItem = RecursivecrawlingItem()
		self.FormItem['target'] = None
		self.FormItem['form'] = []
		self.FormItem['source'] = ''
		for script in scripts:
			if "window.location" in script:
				SplitParts = script.split('"')
				links.append(urlparse.urljoin(response.url,SplitParts[1]))
		for form in forms:
			 self.FormItem['source'] = form.extract()
			 action = form.xpath("//@action").extract()
			 if not action or action[0] == '':
				self.FormItem['target'] = response.url
			 else:
				self.FormItem['target'] = urlparse.urljoin(response.url,action[0].replace("//","/"))
			 Names = form.xpath("//input/@name").extract()
			 Types = form.xpath("//input/@type").extract()
			 TextAreas = form.xpath("//textarea/@name").extract() 			
			 for Name,Type in zip(Names,Types):
				inputElementDictionary = {}
				inputElementDictionary['name'] = Name
				inputElementDictionary['type'] = Type
				print inputElementDictionary
				self.FormItem['form'].append(inputElementDictionary)
			 for TextArea in TextAreas:
				inputElementDictionary = {}
				inputElementDictionary['name'] = TextArea
				inputElementDictionary['type'] = "Textarea"
				print inputElementDictionary
				self.FormItem['form'].append(inputElementDictionary)
			 links.append(urlparse.urljoin(response.url,self.FormItem['target'])) 
			 yield self.FormItem
	
		for link in links:
			link.replace("//","/")
			URLParts = list(urlparse.urlparse(response.url))
			URLParts[2] = URLParts[2].replace("//","/")
			link = urlparse.urljoin(urlparse.urlunparse(URLParts),link)
			if not link in self.listOfCrawledLinks:
				self.crawledURLs.write(link+"\n")
				self.listOfCrawledLinks.append(urlparse.urljoin(response.url,link))
				yield Request(url = link, cookies = self.cookies, callback = self.parse1, dont_filter = True)
 
