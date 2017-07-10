import scrapy
from scrapy.item import Item, Field

class StackItem(Item):
    title = Field()
    description = Field()
    url = Field()