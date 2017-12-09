#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from incrdindia.items import IncrdindiaItem


class SpiderinrdindiaSpider(scrapy.Spider):

    name = 'SpiderInrdIndia'
    allowed_domains = ['http://www.incredibleindiatour.net']
    start_urls = ['http://www.incredibleindiatour.net/states/']

    # rules=[
    # ....Rule(LinkExtractor(
       #  ....restrict_xpaths=('//div[@class=""]')),
       #  ....callback='parse',
       #  ....follow=True),
    # ]
    # def start_urls(self):
    #     names=response.css('a.citylink::text').extract()
    #     for names in namess:
    #         url = 'http://www.incredibleindiatour.net/states/{names}'
    #         yield Request(url, dont_filter=True)

    def parse(self, response):

        urle = \
            response.css('div.col-md-3.hidden-xs.hidden-sm > div > a::attr(href)'
                         ).extract()
        for urls in urle:

            yield scrapy.Request(url=urls, callback=self.parse_info,
                                 dont_filter=True)

        continue_link = response.css('a.citylink::text').extract_first()
        if continue_link:
            continue_link = response.urljoin(continue_link)
            yield scrapy.Request(url=continue_link, callback=self.parse)

    def parse_info(self, response):
        yield {'heads': response.css('div.container.mg-tp > div.col-md-9 > h1::text'
               ).extract(), 'visfor': response.css('p::text').extract()}


