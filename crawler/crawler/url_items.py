from scrapy.item import Field, Item


class UrlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    links = Field()

