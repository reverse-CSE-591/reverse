from crawler.crawler_items import CrawlerItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import sys

class CrawlerSpider(BaseSpider):
    name = "crawler"

    def __init__(self, domain=None, start_urls=None):
        self.allowed_domains = [domain]
	self.start_urls = [start_urls] 

    def parse(self, response):
        print "Entered"
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//input")
        item = CrawlerItem()
        item["form"] = []
        item["url"] = response.url
        for title in titles:
            item["form"].append(title.extract())
        return item
