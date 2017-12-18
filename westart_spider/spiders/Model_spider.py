# -*- coding: utf-8 -*-
import json

import scrapy
from bs4 import BeautifulSoup

from westart_spider.itemprocesser.ItemProcesser import parse_item


class ModelSpider(scrapy.Spider):
    name = "taobao_md"
    allowed_domains = ["taobao.com"]
    start_urls = []

    def __init__(self):
        url = "https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8&pp=%s" % json.dumps({
            "viewFlag": "A",
            "sortType": "default",
            "searchRegion": "city:北京",
            "currentPage": 1,
            "pageSize": 100
        })
        self.start_urls.append(url)

    def parse(self, response):
        isjson, jsonobj = self.is_json(response.body)
        if isjson and (jsonobj.get("status") == 1):
            data_json = jsonobj.get("data")
            searchDOList = data_json.get("searchDOList")
            for user_info in searchDOList:
                item = parse_item(user_info)
                yield item

            totalCount = data_json.get("totalCount")
            currentPage = data_json.get("currentPage")
            totalPage = data_json.get("totalPage")
            if currentPage <= totalPage:
                next_page = currentPage + 1
                url = response.url + "&pp=%s" % json.dumps({
                    "viewFlag": "A",
                    "sortType": "default",
                    "searchRegion": "city:北京",
                    "currentPage": next_page,
                    "pageSize": 100
                })
                yield scrapy.Request(url=url, dont_filter=True)
                # yield scrapy.Request(url=url, dont_filter=False)
        else:
            soup = BeautifulSoup(response.body, 'html.parser')
            print soup

    def is_json(self, string):
        try:
            return True, json.loads(string)
        except ValueError:
            return False, None
