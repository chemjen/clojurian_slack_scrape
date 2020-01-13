from clojurians_slack.items import ClojuriansSlackItem
from scrapy import Spider, Request
import re
import math

class ClojurianSlackSpider(Spider):
    name = 'convo_spider'
    allowed_urls = ['https://clojurians-log.clojureverse.org/']
    start_urls = ['https://clojurians-log.clojureverse.org/']
    def parse(self, response):
        #extract slack channel sub-url
        channels = response.xpath('/html/body/div/ul/li/a/@href').extract() 
        # list comprehension to construct all urls
        channel_urls = [response.url + channel[1:] for channel in channels]  
        print(len(channels))
        print('='*50)
        # Yield the requests to different slack channel urls, 
        # using parse_channel_page function to parse the response.
        for url in channel_urls:
            yield Request(url=url, callback=self.parse_channel_page)


    def parse_channel_page(self, response):
        pass
