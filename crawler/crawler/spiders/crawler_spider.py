from crawler.crawler_items import CrawlerItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import sys

class CrawlerSpider(BaseSpider):
    name = "crawler"
    allowed_domains = ''
    start_urls = ''

    def __init__(self, domain=None, start_urls=None):
        self.allowed_domains = domain
	self.start_urls = start_urls 

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//input")
        item = CrawlerItem()
        item["form"] = ''
        item["url"] = sys.argv[2]
        for title in titles:
            item["form"].append(title.extract())
        return item
