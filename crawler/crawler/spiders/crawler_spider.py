from crawler.crawler_items import CrawlerItem
from crawler.url_items import UrlItem
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from urlparse import urlparse
import sys
import scrapy
import ast

class CrawlerSpider(Spider):
    name = "crawler"

    def __init__(self, domain=None, start_urls=None, cookies=None):
        self.allowed_domains = [domain]
        self.start_urls = [start_urls]
        self.cookies = {}
        if cookies: 
            self.cookies = ast.literal_eval(cookies)
        self.urlItem = UrlItem()
        self.urlItem["links"] = [] 
	      
    def start_requests(self):
        return [scrapy.Request(url=self.start_urls[0], cookies=self.cookies, callback=self.parse_2)]

    def parse_2(self, response):        
        print "Entered"
        item = CrawlerItem()
        titles = response.xpath("//input")
        formTitle = response.xpath("//form/@action")        
        item["form"] = []
        item["url"] = response.url
        for formt in formTitle:
            item["form"].append("action::"+formt.extract())  
        for title in titles:
            item["form"].append(title.extract())                                 
        return item    
