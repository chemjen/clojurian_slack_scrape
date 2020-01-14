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
        # list comprehension to construct all urls, do not include leading '/' in channel
        channel_urls = [response.url + channel[1:] for channel in channels]
        # Yield the requests to different slack channel urls, 
        # using parse_channel_page function to parse the response.
        for url in channel_urls:
            yield Request(url=url, callback=self.parse_channel_page)

    def parse_channel_page(self, response):
        #get the link texts on the page, of form 'YYYY-MM-DD (num_messages)'
        links = response.xpath('/html/body/div/ul/li/a/text()').extract()

        # each date page has a url of 'https://clojurians-log.clojureverse.org/channel/YYYY-MM-DD'
        dates = [link.split()[0] for link in links]
        date_urls = [response.url + '/' + date for date in dates]        
        for url in date_urls:
            yield Request(url=url, callback=self.parse_date_page)

    def parse_date_page(self, response):
        #get each message
        messages = response.xpath('/html/body/div[2]/div[2]/div')
       
        thread = 0
        for message in messages:

            #decide if it's part of a thread or not
            if message.xpath('./@class').extract_first() == "message":
                thread += 1
            else: 
                continue
            
            # get useful info
            username = message.xpath('./a[@class="message_username"]/text()').extract_first() 
            timestamp = message.xpath('./span[@class="message_timestamp"]/a/text()').extract_first()
            text = message.xpath('./span[@class="message_content"]/p[2]/text()').extract_first()

            # yield an item for each message
            item = ClojuriansSlackItem()
            item['channel'] = response.url.split('/')[3]
            item['date'] = response.url.split('/')[4]
            item['url'] = response.url
            item['timestamp'] = timestamp
            item['thread'] = thread
            item['username'] = username
            item['text'] = text
            yield item
            








