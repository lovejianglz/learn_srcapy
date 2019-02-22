# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import scrapy.pipelines.images
import scrapy.exceptions


class ImagePipeline(scrapy.pipelines.images.ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item.get('url'))

    def item_completed(self, results, item, info):
        # results 的格式
        #  [(True, {'url': 'http://p1.so.qhimgs1.com/t0183893a8b17d29eb1.jpg',
        #           'path': 'full/f3a23192521fbca26ef9f29d728cbef95d81a970.jpg',
        #           'checksum': '70e4dbdfe96c359bf785106314a52c6a'})]
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise scrapy.exceptions.DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class PicDownloadPipeline(object):
    def process_item(self, item, spider):
        return item


class Save2FilePipeline():
    def open_spider(self, spider):
        self.f = open("pic.txt", "w")

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write("title:{},label:{},tag{}\n".format(item["title"], item["label"], item["tag"]))
        return item


class MongoPipeline():
    def __init__(self, uri, db):
        self.mongo_uri = uri
        self.mongo_db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(uri=crawler.settings.get("MONGO_URI"), db=crawler.settings.get("MONGO_DB"))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection].insert_one(dict(item))
        return item


if __name__ == "__main__":
    pass
