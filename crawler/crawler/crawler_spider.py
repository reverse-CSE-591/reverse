from crawler_items import CrawlerItem
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
import sys

class CrawlerSpider(Spider):
    name = "crawler"    
  
    def parse(self, response):
        print 'herE!'
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//input")
        item = CrawlerItem()
        item["form"] = ''
        item["url"] = 'test'
        for title in titles:
            item["form"].append(title.extract())
            print item
        return item
