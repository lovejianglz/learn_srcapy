# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['*']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
