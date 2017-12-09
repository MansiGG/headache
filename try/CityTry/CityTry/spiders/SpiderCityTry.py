#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy


class SpidercitytrySpider(scrapy.Spider):
	# name of the spider
    name = 'SpiderCityTry'
    # website which are allowes
    allowed_domains = ['http://indiacitiesinformation.org/']
    # from which page scraping should be start
    start_urls = ['http://indiacitiesinformation.org/']

    # handling url Request and response is done here
    def parse(self, response):
    	# gets the list of all cities available with their urls
        urle = \
            response.css('div.boxed > div.site-content > div.container > div.row > aside.col-md-3.sidebar.islemag-content-right > div#categories-4 > ul > li > a::attr(href)'
                         ).extract()
        # looping through the list and passing control to the next page is done here     
        for urls in urle:
            yield scrapy.Request(url=urls, callback=self.parse_page,
                                 dont_filter=True)

        # continue_link = \
        #     response.css('div.boxed > div.site-content > div.container > div.row > aside.col-md-3.sidebar.islemag-content-right > div#categories-4 > ul > li > a::text'
        #                  ).extract_first()
        # if continue_link:
        #     continue_link = response.urljoin(continue_link)
        #     yield scrapy.Request(url=continue_link, callback=self.parse)

    # gets the link for page which contains the actual information
    def parse_page(self, response):
    	# gets the link which redirect to the information page
        next_page_url = \
            response.css('div.boxed > div.site-content > div.container > div.row > div.islemag-content-left.col-md-9> article > h2.entry-title > a::attr(href)'
                         ).extract()
        # loops through the list of and passes control to the function which extracts information
        for curl in next_page_url:
            yield scrapy.Request(url=curl, callback=self.parse_info,
                                 dont_filter=True)

    # function responsible for extracting content from webpage and storing into the variable
    def parse_info(self, response):
        yield {'title': response.css('div.boxed > div.site-content > div.content-area > div.islemag-content-left.col-md-9 > main.site-main > div.row > div.col-md-12 > article > h2.entry-title::text' 
               ).extract(),
               'content': response.css('div.boxed > div.site-content > div.content-area > div.islemag-content-left.col-md-9 > main.site-main > div.row > div.col-md-12 > article > div.entry-content > p::text'
               ).extract()}


