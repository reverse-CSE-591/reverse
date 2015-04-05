import scrapy
from crawler_spider import CrawlerSpider

def crawler_test():
    spid = CrawlerSpider()
    import pdb; pdb.set_trace()
    req = scrapy.Request("https://www.google.com/", callback=spid.parse)
    
    print dir(req)
    
if __name__ == "__main__":
    crawler_test()
    