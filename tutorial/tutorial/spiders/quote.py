# -*- coding: utf-8 -*-
import scrapy
import tutorial.items

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            item = tutorial.items.QuoteItem()
            item["text"] = quote.css(".text::text").extract()[0]
            item["author"] = quote.css(".author::text").extract_first()
            item["tags"] = quote.css(".tags a::text").extract()
            yield item
        next_page_url = response.css(".next a::attr('href')").extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
