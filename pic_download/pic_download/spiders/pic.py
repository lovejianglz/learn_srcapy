# -*- coding: utf-8 -*-
import scrapy
import json
import pic_download.items
import urllib.parse


class PicSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/z?ch=photography']
    base_url = "http://image.so.com/z"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/41.0.2228.0 Safari/537.36"
    }

    def start_requests(self):
        param = {"ch": "photography"}
        url = self.base_url + "?" + urllib.parse.urlencode(param)
        yield scrapy.Request(url=url, callback=self.first_parse)

    def first_parse(self, response):
        pic_data = response.css("#initData::text").extract_first()
        pic_data = json.loads(pic_data).setdefault("data", None)
        if pic_data:
            pic_list = pic_data.setdefault("list", None)
            if not pic_list:
                self.logger.warning("no pic list found")
            else:
                for each_pic in pic_list:
                    item = self.parse_pic(each_pic)
                    yield item
            if not pic_data.setdefault("end", True):
                param = {
                    "ch": "photography",
                    "sn": pic_data.setdefault("lastid", 30),
                    "listtype": "new",
                    "temp": "1"
                }
                url = self.base_url + "j?" + urllib.parse.urlencode(param)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response_data = json.loads(response.body)
        for each_pic in response_data.get("list", list()):
            yield self.parse_pic(each_pic)
        param = {
            "ch": "photography",
            "sn": response_data["lastid"],
            "listtype": "new",
            "temp": "1"
        }
        url = self.base_url + "j?" + urllib.parse.urlencode(param)
        if int(param["sn"]) < 100:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_pic(self, e_pic):
        item = pic_download.items.PicItem()
        item["title"] = e_pic["group_title"]
        item["tag"] = e_pic["tag"]
        item["label"] = e_pic.setdefault("label", "")
        item["url"] = e_pic["qhimg_url"]
        item["index"] = e_pic["index"]
        return item
