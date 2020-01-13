# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClojuriansSlackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    channel = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    thread = scrapy.Field()
    username = scrapy.Field()
    text = scrapy.Field()

