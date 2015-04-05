from crawler.crawler_items import CrawlerItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import sys
import scrapy
import ast

class CrawlerSpider(BaseSpider):
    name = "crawler"

    def __init__(self, domain=None, start_urls=None, cookies=None):
        self.allowed_domains = [domain]
        self.start_urls = [start_urls]        
        self.cookies = ast.literal_eval(cookies)	      	      
	      
    def start_requests(self):
        return [scrapy.Request(url=self.start_urls[0], cookies=self.cookies, callback=self.parse_2)]

    def parse_2(self, response):        
        print "Entered"
        item = CrawlerItem()
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//input")        
        item["form"] = []
        item["url"] = response.url
        for title in titles:
            item["form"].append(title.extract())            
        return item