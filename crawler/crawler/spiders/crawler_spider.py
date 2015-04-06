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
        return [scrapy.Request(url=self.start_urls[0], cookies=self.cookies, callback=self.parse_1)]

    def parse_2(self, response):        
        print "Entered"
        item = CrawlerItem()
        titles = response.xpath("//input")
        item["form"] = []
        item["url"] = response.url
        for title in titles:
            item["form"].append(title.extract())            
        return item

    def parse_1(self, response):
        path = urlparse(response.url).scheme + '://' + urlparse(response.url).netloc
        for url in response.xpath('//a/@href').extract():
            if str(path) in url:
            	self.urlItem["links"].append(url)
            else:
                url = str(path)+url
                self.urlItem["links"].append(str(path)+url)
            yield scrapy.Request(url, callback=self.parse_1)
