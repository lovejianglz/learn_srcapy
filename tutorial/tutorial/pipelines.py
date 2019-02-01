# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item["text"]:
            if len(item["text"]) > self.limit:
                item["text"] = item["text"][0:self.limit].rstrip() + "..."
            return item
        else:
            return DropItem("Missing Text")


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.setting.get("MONGO_URI"),
            mongo_db = crawler.setting.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pym